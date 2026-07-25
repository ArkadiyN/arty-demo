import argparse
import re
import sys
from pathlib import Path

# $$...$$ (display) or $...$ (inline, no embedded $ or newline) math spans.
_MATH_SPAN_RE = re.compile(r"\$\$(?P<disp>.*?)\$\$|\$(?P<inline>[^$\n]*?)\$", re.DOTALL)
_FENCE_RE = re.compile(r"^```")

# A literal LaTeX row-separator \\ is always followed by whitespace, `[`, or
# end-of-string/line — never directly by a letter. `\\` immediately before a
# letter is always a double-escaped command (\\frac, \\exp, ...).
_DOUBLE_ESCAPED_CMD_RE = re.compile(r"\\\\(?=[A-Za-z])")
# Underscore/caret never need escaping in math mode; \_ / \^ is always a
# leftover from an over-eager formatter escaping subscript/superscript markers.
_OVER_ESCAPED_SUBSUP_RE = re.compile(r"\\([_^])")
# \left{ / \right} (raw, unescaped brace) is invalid LaTeX -- the brace
# delimiter itself needs escaping: \left\{ / \right\}.
_UNESCAPED_LEFT_RIGHT_BRACE_RE = re.compile(r"\\(left|right)([{}])")

CHECK_DOUBLE_ESCAPED = "double_escaped_command"
CHECK_OVER_ESCAPED_SUBSUP = "over_escaped_subsup"
CHECK_UNESCAPED_LEFT_RIGHT_BRACE = "unescaped_left_right_brace"
CHECK_UNMATCHED_DELIMITER = "unmatched_dollar_delimiter"

FIXABLE_CHECKS = {CHECK_DOUBLE_ESCAPED, CHECK_OVER_ESCAPED_SUBSUP, CHECK_UNESCAPED_LEFT_RIGHT_BRACE}


def _blank_fenced_code(text):
    """Replace fenced code block bodies with NUL padding, same length/lines, so
    `$`/math-lookalikes inside code blocks are never mistaken for real math."""
    out = []
    in_fence = False
    for line in text.splitlines(keepends=True):
        if _FENCE_RE.match(line.strip()):
            in_fence = not in_fence
            out.append(line)
            continue
        out.append("\x00" * (len(line) - 1) + line[-1] if in_fence and line else line)
    return "".join(out)


def _line_at(text, offset):
    return text.count("\n", 0, offset) + 1


def find_math_spans(text):
    """Yield (start, end, is_display, content) for each math span, skipping fenced code."""
    masked = _blank_fenced_code(text)
    for m in _MATH_SPAN_RE.finditer(masked):
        is_display = m.group("disp") is not None
        content = m.group("disp") if is_display else m.group("inline")
        yield m.start(), m.end(), is_display, content


def _snippet(content, pos, width=18):
    return content[max(0, pos - width) : pos + width].strip()


def scan_text(text):
    """Return a list of finding dicts: {lineno, kind, snippet}, worst-first order not applied here."""
    findings = []
    for start, _end, _is_display, content in find_math_spans(text):
        for regex, kind in (
            (_DOUBLE_ESCAPED_CMD_RE, CHECK_DOUBLE_ESCAPED),
            (_OVER_ESCAPED_SUBSUP_RE, CHECK_OVER_ESCAPED_SUBSUP),
            (_UNESCAPED_LEFT_RIGHT_BRACE_RE, CHECK_UNESCAPED_LEFT_RIGHT_BRACE),
        ):
            for m in regex.finditer(content):
                findings.append(
                    {
                        "lineno": _line_at(text, start + m.start()),
                        "kind": kind,
                        "snippet": _snippet(content, m.start()),
                    }
                )

    masked = _blank_fenced_code(text)
    without_display = masked.replace("$$", "")
    if masked.count("$$") % 2 != 0:
        findings.append({"lineno": None, "kind": CHECK_UNMATCHED_DELIMITER, "snippet": "odd count of $$ in file"})
    if without_display.count("$") % 2 != 0:
        findings.append({"lineno": None, "kind": CHECK_UNMATCHED_DELIMITER, "snippet": "odd count of $ in file"})

    findings.sort(key=lambda f: (f["lineno"] is None, f["lineno"] or 0))
    return findings


def fix_text(text):
    """Return text with the fixable corruption classes repaired inside math spans.
    Unmatched-delimiter findings are never auto-fixed (ambiguous which side is wrong)."""
    masked = _blank_fenced_code(text)
    out = []
    last_end = 0
    for m in _MATH_SPAN_RE.finditer(masked):
        start, end = m.start(), m.end()
        out.append(text[last_end:start])
        is_display = m.group("disp") is not None
        content = m.group("disp") if is_display else m.group("inline")
        fixed = _DOUBLE_ESCAPED_CMD_RE.sub(r"\\", content)
        fixed = _OVER_ESCAPED_SUBSUP_RE.sub(r"\1", fixed)
        fixed = _UNESCAPED_LEFT_RIGHT_BRACE_RE.sub(r"\\\1\\\2", fixed)
        delim = "$$" if is_display else "$"
        out.append(delim + fixed + delim)
        last_end = end
    out.append(text[last_end:])
    return "".join(out)


def scan_paths(paths):
    """Scan markdown/qmd files. Returns [(path, findings)], worst-first."""
    report = []
    for f in paths:
        text = f.read_text(encoding="utf-8", errors="replace")
        if not text:
            continue
        findings = scan_text(text)
        if findings:
            report.append((str(f), findings))
    report.sort(key=lambda r: -len(r[1]))
    return report


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Check LaTeX/KaTeX math spans ($...$ / $$...$$) in Markdown/Quarto files for "
            "escaping corruption: double-escaped commands (\\\\frac), over-escaped "
            "subscripts/superscripts (\\_ / \\^), unescaped \\left{/\\right} braces, and "
            "unmatched $ / $$ delimiter counts."
        )
    )
    parser.add_argument(
        "path",
        nargs="*",
        default=["doc-reference"],
        help="Files and/or directories to scan for .md/.qmd files (directories are scanned "
        "recursively). Multiple values are accepted so this can run as a pre-commit hook with "
        "pass_filenames: true. Defaults to doc-reference/ when nothing is given.",
    )
    parser.add_argument(
        "--fail-on-flag",
        action="store_true",
        help="Exit with status 1 if any file is flagged (for use as a pipeline gate).",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Rewrite files in place, repairing the fixable corruption classes "
        "(double-escaped commands, over-escaped sub/superscripts, unescaped left/right braces). "
        "Unmatched-delimiter findings are left for manual review.",
    )
    args = parser.parse_args()

    paths = set()
    for p in args.path:
        target = Path(p)
        if target.is_file():
            paths.add(target)
        elif target.is_dir():
            paths.update(target.rglob("*.md"))
            paths.update(target.rglob("*.qmd"))
    paths = sorted(paths)

    if args.fix:
        fixed_count = 0
        for f in paths:
            text = f.read_text(encoding="utf-8", errors="replace")
            if not text:
                continue
            fixed = fix_text(text)
            if fixed != text:
                f.write_text(fixed, encoding="utf-8")
                fixed_count += 1
                print(f"fixed: {f}")
        print(f"\n{fixed_count} file(s) modified")

    report = scan_paths(paths)

    for path, findings in report:
        print(f"{path}")
        for finding in findings:
            loc = f"L{finding['lineno']}" if finding["lineno"] is not None else "file"
            print(f"    {loc}: {finding['kind']}: {finding['snippet']!r}")

    print(f"\n{len(report)} / {len(paths)} file(s) flagged")

    if args.fail_on_flag and report:
        sys.exit(1)


if __name__ == "__main__":
    main()
