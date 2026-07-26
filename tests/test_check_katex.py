"""
Tests for src/utils/check-katex.py

Coverage map
============

scan_text
  • Clean, valid LaTeX produces no findings.
  • Double-escaped command (\\\\frac) flagged with correct line number.
  • Over-escaped subscript/superscript (\\_ / \\^) flagged.
  • Unescaped \\left{ / \\right} brace flagged.
  • A genuine \\\\ row-separator (followed by whitespace, not a letter) is NOT flagged.
  • `$` inside a fenced code block is ignored (no false positive).
  • Odd count of $ / $$ in a file is flagged as an unmatched delimiter.

fix_text
  • Repairs double-escaped commands, over-escaped sub/superscripts, and
    unescaped left/right braces.
  • Re-scanning fixed text leaves no fixable findings.
  • Does not touch content outside math spans or inside fenced code blocks.
"""

import importlib.util
from pathlib import Path

_CHECKER = Path(__file__).parent.parent / "src" / "utils" / "check-katex.py"
_spec = importlib.util.spec_from_file_location("check_katex", _CHECKER)
assert _spec is not None and _spec.loader is not None
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

scan_text = _mod.scan_text
fix_text = _mod.fix_text
CHECK_DOUBLE_ESCAPED = _mod.CHECK_DOUBLE_ESCAPED
CHECK_OVER_ESCAPED_SUBSUP = _mod.CHECK_OVER_ESCAPED_SUBSUP
CHECK_UNESCAPED_LEFT_RIGHT_BRACE = _mod.CHECK_UNESCAPED_LEFT_RIGHT_BRACE
CHECK_UNMATCHED_DELIMITER = _mod.CHECK_UNMATCHED_DELIMITER


def _kinds(findings):
    return [f["kind"] for f in findings]


class TestScanTextClean:
    def test_no_math_no_findings(self):
        assert scan_text("Just some prose with no math at all.\n") == []

    def test_valid_display_and_inline_math_no_findings(self):
        text = (
            "Some prose with inline math $N(m) = N_0 e^{-m/\\mu}$ here.\n\n"
            "$$\n"
            "v_r = \\frac{2\\pi\\mu}{\\rho a \\gamma}\n"
            "$$\n"
        )
        assert scan_text(text) == []

    def test_genuine_row_separator_not_flagged(self):
        text = "$$\\begin{aligned} a &= b \\\\\n c &= d \\end{aligned}$$\n"
        assert scan_text(text) == []

    def test_dollar_in_fenced_code_ignored(self):
        text = "```\nprice = $5 and another $10\n```\n"
        assert scan_text(text) == []


class TestScanTextDoubleEscapedCommand:
    def test_flags_double_backslash_before_letter(self):
        text = "$$N(m) = N_0 \\\\exp \\\\left( -\\\\frac{m}{\\\\mu} \\\\right)$$\n"
        findings = scan_text(text)
        assert findings
        assert all(f["kind"] == CHECK_DOUBLE_ESCAPED for f in findings)
        assert all(f["lineno"] == 1 for f in findings)

    def test_correct_line_number_on_later_line(self):
        text = "line one\nline two\n$$a = \\\\frac{1}{2}$$\n"
        findings = scan_text(text)
        assert findings[0]["lineno"] == 3


class TestScanTextOverEscapedSubsup:
    def test_flags_escaped_underscore(self):
        text = "$$m_i = \\sum\\_{j=1}^n \\mu_j$$\n"
        findings = scan_text(text)
        assert any(f["kind"] == CHECK_OVER_ESCAPED_SUBSUP for f in findings)

    def test_flags_escaped_caret(self):
        text = "$a\\^{2} + b^2 = c^2$\n"
        findings = scan_text(text)
        assert any(f["kind"] == CHECK_OVER_ESCAPED_SUBSUP for f in findings)


class TestScanTextUnescapedLeftRightBrace:
    def test_flags_raw_brace_after_left_right(self):
        text = "$$p = 1 - \\exp \\left{ -\\int_0^s C\\,ds \\right}.$$\n"
        findings = scan_text(text)
        kinds = _kinds(findings)
        assert kinds.count(CHECK_UNESCAPED_LEFT_RIGHT_BRACE) == 2

    def test_escaped_brace_not_flagged(self):
        text = "$$p = 1 - \\exp \\left\\{ -\\int_0^s C\\,ds \\right\\}.$$\n"
        findings = scan_text(text)
        assert CHECK_UNESCAPED_LEFT_RIGHT_BRACE not in _kinds(findings)


class TestScanTextUnmatchedDelimiter:
    def test_odd_dollar_flagged(self):
        text = "Some $unterminated math here.\n"
        findings = scan_text(text)
        assert any(f["kind"] == CHECK_UNMATCHED_DELIMITER for f in findings)

    def test_odd_double_dollar_flagged(self):
        text = "$$unterminated display math\n"
        findings = scan_text(text)
        assert any(f["kind"] == CHECK_UNMATCHED_DELIMITER for f in findings)

    def test_balanced_delimiters_not_flagged(self):
        text = "$a$ and $$b$$ and $c$\n"
        findings = scan_text(text)
        assert CHECK_UNMATCHED_DELIMITER not in _kinds(findings)


class TestFixText:
    def test_fixes_double_escaped_command(self):
        text = "$$N_0 \\\\exp(-m/\\\\mu)$$\n"
        fixed = fix_text(text)
        assert "\\\\exp" not in fixed
        assert "\\exp" in fixed
        assert scan_text(fixed) == []

    def test_fixes_over_escaped_subsup(self):
        text = "$$m_i = \\sum\\_{j=1}^n \\mu_j$$\n"
        fixed = fix_text(text)
        assert "\\_{" not in fixed
        assert "_{j=1}" in fixed
        assert scan_text(fixed) == []

    def test_fixes_unescaped_left_right_brace(self):
        text = "$$p = 1 - \\exp \\left{ -x \\right}.$$\n"
        fixed = fix_text(text)
        assert "\\left\\{" in fixed
        assert "\\right\\}" in fixed
        assert scan_text(fixed) == []

    def test_fixes_all_classes_together_realistic_fixture(self):
        text = (
            "$$N(m) = N\\_{0} \\\\exp \\\\left( -\\\\frac{m}{\\\\mu} \\\\right)$$ (1)\n\n"
            "In equation 1, $N(m)$ is the number of fragments, $N\\_{0}$ is the total.\n"
        )
        fixed = fix_text(text)
        assert scan_text(fixed) == []
        assert "N_{0}" in fixed
        assert "\\exp" in fixed and "\\\\exp" not in fixed
        assert "\\frac" in fixed and "\\\\frac" not in fixed

    def test_does_not_touch_prose_outside_math(self):
        text = "See the repo at https://example.com/path\\\\ for details.\n$a\\_b$\n"
        fixed = fix_text(text)
        assert "https://example.com/path\\\\ for details." in fixed

    def test_does_not_touch_fenced_code(self):
        text = "```\nsome_var\\_name = \\\\notreal\n```\n$x\\_1$\n"
        fixed = fix_text(text)
        assert "some_var\\_name = \\\\notreal" in fixed
        assert "$x_1$" in fixed

    def test_leaves_unmatched_delimiter_unfixed(self):
        text = "Some $unterminated \\\\frac{1}{2} math here.\n"
        fixed = fix_text(text)
        remaining = scan_text(fixed)
        assert any(f["kind"] == CHECK_UNMATCHED_DELIMITER for f in remaining)
