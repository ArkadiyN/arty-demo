import argparse
import re
import sys
from pathlib import Path

PUA_START = 0xE000
PUA_END = 0xF8FF
_SYMBOL_RUN_RE = re.compile(r"[-*_=~^]{4,}")
_THEMATIC_BREAK_RE = re.compile(r"^\s*([-*_])\s*(\1\s*){2,}$")
_TABLE_SEP_RE = re.compile(r"^\s*\|?[\s:|-]+\|?\s*$")
_SHORT_TOKEN_RE = re.compile(r"\b\w{1,2}\b")
_WORD_RE = re.compile(r"\b\w+\b")

# Calibrated against doc-reference/: flags files with PUA (Private Use Area)
# glyphs from broken cmap fonts, runs of suspicious symbol characters outside
# thematic breaks/table separators, or an abnormally high ratio of 1-2 char
# tokens (a symptom of garbled/fragmented word extraction).
SHORT_TOKEN_RATIO_THRESHOLD = 0.42
SHORT_TOKEN_MIN_WORDS = 200
SUSPECT_LINE_THRESHOLD = 3


def scan_text(text):
    """Return (flags, suspect_lines) for a single document's markdown text."""
    pua_positions = [i for i, ch in enumerate(text) if PUA_START <= ord(ch) <= PUA_END]

    suspect_lines = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        if not _SYMBOL_RUN_RE.search(line):
            continue
        if _THEMATIC_BREAK_RE.match(line) or _TABLE_SEP_RE.match(line):
            continue
        suspect_lines.append((lineno, line.strip()))

    words = _WORD_RE.findall(text)
    short_tokens = _SHORT_TOKEN_RE.findall(text)
    short_ratio = len(short_tokens) / max(1, len(words))

    flags = []
    if pua_positions:
        sample_line = text.count("\n", 0, pua_positions[0]) + 1
        flags.append(f"PUA glyphs={len(pua_positions)} first_at_line={sample_line}")
    if len(suspect_lines) > SUSPECT_LINE_THRESHOLD:
        flags.append(f"suspect_symbol_lines={len(suspect_lines)}")
    if short_ratio > SHORT_TOKEN_RATIO_THRESHOLD and len(words) > SHORT_TOKEN_MIN_WORDS:
        flags.append(f"short_token_ratio={short_ratio:.2f}")

    return flags, suspect_lines


def scan_paths(paths):
    """Scan a list of markdown file paths. Returns a report list, sorted worst-first."""
    report = []
    for f in paths:
        text = f.read_text(encoding="utf-8", errors="replace")
        if not text:
            continue
        flags, suspect_lines = scan_text(text)
        if flags:
            report.append((str(f), len(text), flags, suspect_lines[:4]))
    report.sort(key=lambda r: -len(r[2]))
    return report


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Scan extracted markdown for signs of broken PDF/XML extraction: "
            "Private Use Area glyphs (broken font cmaps), suspicious symbol-run "
            "lines, and abnormal short-token ratios (fragmented word extraction)."
        )
    )
    parser.add_argument(
        "path",
        nargs="?",
        default="doc-reference",
        help="A single .md file or a directory to scan recursively (default: doc-reference/)",
    )
    parser.add_argument(
        "--fail-on-flag",
        action="store_true",
        help="Exit with status 1 if any file is flagged (for use as a pipeline gate).",
    )
    args = parser.parse_args()

    target = Path(args.path)
    if target.is_file():
        paths = [target]
    else:
        paths = sorted(target.rglob("*.md"))

    report = scan_paths(paths)

    for path, n, flags, samples in report:
        print(f"{path}  ({n} chars)")
        for fl in flags:
            print(f"    {fl}")
        for lineno, line in samples:
            print(f"      L{lineno}: {line[:100]!r}")

    print(f"\n{len(report)} / {len(paths)} file(s) flagged")

    if args.fail_on_flag and report:
        sys.exit(1)


if __name__ == "__main__":
    main()
