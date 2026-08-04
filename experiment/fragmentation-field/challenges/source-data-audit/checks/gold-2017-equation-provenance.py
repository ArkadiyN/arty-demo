"""Are the Gold 2017 equations `src/arty` implements the ones on the page?

Consumer: doc-reference/fragmentation/fragment-size-distribution-conwep/card.md
          ("Closure", "Equations as printed"), and
          experiment/fragmentation-field/challenges/source-data-audit/ledger.md
          section 24.

Gold 2017 carries no data series this repo consumes -- what it supplies is a
chain of *equations*, implemented in `src/arty/fragmentation.py:mott_params`
and `src/arty/zones.py`. So the fidelity question is not "was the right cell
read" but "was the right formula read", and it needs a different instrument.

Three parts, and the third is the one that matters.

1. PROVENANCE.  Every equation this repo cites is printed off the retained
   scan next to its greppable anchor sentence, so the `.md` extraction can be
   compared against the page without a second extraction.  The scan is
   gitignored (`doc-reference/**/*.pdf`); when it is absent this part reports
   `skipped` rather than failing, exactly as `sandia-cd-provenance.py` does.

2. WHY READING HARDER DOES NOT WORK.  The whole sign question turns on
   eq. (6)'s `alpha^(-2/3)`, and neither available surface can settle it:

   - The committed `.md`'s equations are *reconstructed LaTeX*, not
     transcribed text -- the raw text layer contains no LaTeX at all.  So the
     minus in `\alpha^{-2/3}` is a vision model's reading of the page, and
     Phase 7 of this audit established that this pipeline invents values.
   - The raw text layer cannot arbitrate, because it encodes the minus as an
     unmapped control character (`\x04`) that it also uses for hyphens --
     `Q\x04angle` is "Theta-angle", `a\x042=3` is `alpha^(-2/3)`.  Being
     non-printable, it is dropped by any printable-character filter, which
     silently yields the wrong-sign reading `alpha^(2/3)` with no glyph-level
     trace.  (`scan-extraction-quality.py` is exactly such a filter.)

   Guessing wrong costs a factor of alpha^2 in mu -- 14x to 32x across this
   model's break-up velocities -- in the direction that makes fragments
   smaller and more numerous.

3. CLOSURE.  The source closes the sign itself: eq. (5) is *stated* to be
   eq. (2) substituted into eq. (4), and only one exponent makes that
   substitution true.  This script recovers the exponent numerically from that
   requirement, rather than trusting either surface above.  It then checks that
   eq. (7) and eq. (16) are the same formula (the repo cites both names for
   it), and that the shipped `mott_params` composition reproduces eq. (4)
   evaluated directly -- which it can only do if its `alpha ** (-2/3)` is the
   sign the algebra demands.

   Note the shape: this is a closure invariant in the sense of
   `.claude/rules/source-data-fidelity.md`, but it closes a *formula* rather
   than a table, which none of that rule's four listed forms covers.

   Finally it records that the paper contradicts itself on the fragment count:
   eq. (1) states `N0 = M/2mu`, eq. (17) states `N0j = m_j/mu_j`.  These differ
   by exactly the factor of 2, and `mott_params` follows eq. (1).

    uv run python experiment/fragmentation-field/challenges/source-data-audit/checks/gold-2017-equation-provenance.py
"""

import pathlib

import numpy as np

from arty.fragmentation import ShellParams, _shell_geometry, mott_params

ROOT = pathlib.Path(__file__).resolve().parents[5]
DOC = ROOT / "doc-reference/fragmentation/fragment-size-distribution-conwep"
SCAN = DOC / "source.pdf"
EXTRACT = DOC / "1-s2.0-S221491471730079X-main.md"

# (label, greppable anchor).  Each anchor is the *sentence introducing* the
# equation, not the equation itself -- formulae render differently in every
# extractor, prose does not.  Each is verified unique in the extraction below.
ANCHORS = [
    ("eq. (1)  N(m) = N0 exp[-(m/mu)^1/2], N0 = M/2mu",
     "represents total number of fragments of mass greater than"),
    ("eq. (2)  x0 = (2 sigma_F / rho gamma')^1/2 (r/V)",
     "the average circumferential length of the resulting fragments is"),
    ("eq. (4)  mu = 1/2 alpha rho x0^3, alpha = (l0/x0)(t0/x0)",
     "the average fragment mass takes the following form"),
    ("eq. (5)  (2) substituted into (4)",
     "Substituting equation (2) into equation (4) results in"),
    ("eq. (6)  gamma = alpha^(-2/3) gamma'",
     "warrants knowledge of the average fragment mass but not the shape"),
    ("eq. (7)  mu in terms of gamma",
     "allows equation (5) to be put in a simpler and more useful form"),
    ("eq. (16)/(17)  per-segment mu_j and N0j",
     "the resulting fragment size distributions in each segment"),
    ("gamma = 50, the value _validation.qmd compares against",
     "All of these models employ the same value for"),
    ("the 3-volume-expansion break-up rule of thumb",
     "criterion is accepted as a rule of thumb"),
]


def provenance():
    """Print each cited equation off the page, located by its anchor."""
    print("1. PROVENANCE — the cited equations, off the retained scan\n")

    text = EXTRACT.read_text(encoding="utf-8")
    bad = [a for _, a in ANCHORS if text.count(a) != 1]
    if bad:
        print(f"    FAIL: anchors not unique in the extraction: {bad}")
        return 1
    print(f"    all {len(ANCHORS)} anchors unique in {EXTRACT.name}")

    if not SCAN.exists():
        print(f"    scan absent ({SCAN.relative_to(ROOT)}) — page comparison "
              "skipped.\n    The scan is gitignored by convention; re-supply "
              "it to re-run this part.")
        return 0

    import fitz  # noqa: PLC0415 — only needed when the scan is present

    with fitz.open(SCAN) as doc:
        pages = [p.get_text() for p in doc]
    print(f"    scan: {len(pages)} pages, all with a text layer "
          f"(min {min(len(p) for p in pages)} chars)\n")

    # The text layer mangles ligatures and renders signs as unmapped control
    # characters, so anchors are matched on a whitespace-collapsed reduction.
    # Anchors are prose for exactly this reason: prose survives, formulae do not.
    def reduce(s):
        return " ".join(s.replace("ﬁ", "fi").replace("ﬂ", "fl").split())

    flat = [reduce(p) for p in pages]
    for label, anchor in ANCHORS:
        key = reduce(anchor)
        hit = next((i for i, p in enumerate(flat) if key in p), None)
        where = f"p.{300 + hit}" if hit is not None else "NOT FOUND ON SCAN"
        print(f"    {label}")
        print(f"        {where}  anchor: {anchor!r}")
        if hit is None:
            return 1
    return 0


def sign_is_unreadable():
    """Show that neither available surface can settle eq. (6)'s sign.

    The card and ledger section 24a both rest on this: it is why a clean text
    layer is NOT sufficient here, and why the closure below has to be algebraic.
    Printed rather than asserted so the claim is auditable.

    Two independent reasons, both shown below: the committed extraction's
    equations are vision-reconstructed, and the raw text layer encodes the
    minus as a non-printable character it also uses for hyphens.
    """
    print("\n2. WHY A CLEAN TEXT LAYER IS NOT ENOUGH HERE\n")
    if not SCAN.exists():
        print("    scan absent — skipped.")
        return 0

    import fitz  # noqa: PLC0415

    print("    (a) The committed extraction's equations are RECONSTRUCTED,")
    print("        not transcribed — the .md carries LaTeX, and the raw text")
    print("        layer contains no LaTeX at all:\n")
    md = EXTRACT.read_text(encoding="utf-8")
    with fitz.open(SCAN) as doc:
        pages = [p.get_text() for p in doc]
    raw = "\n".join(pages)
    for probe in (r"\alpha^{-2/3} \gamma'", r"\frac{1}{2} \alpha \rho x_0^3"):
        print(f"        {probe!r:44}  .md: {probe in md}   text layer: "
              f"{probe in raw}")
    print("\n        So the sign on eq. (6) is a VISION MODEL'S READING of the")
    print("        page. Phase 7 of this audit established that this pipeline")
    print("        invents values; nothing here exempts an exponent.")

    print("\n    (b) The text layer cannot arbitrate, because it encodes the")
    print("        minus as an unmapped control character that it ALSO uses")
    print("        for hyphens — same byte, two meanings:\n")
    probes = [
        ("eq. (5)   ... rho^(1/3) alpha^(-2/3) gamma' ...", "r1=3a\x04"),
        ("eq. (6)   gamma = alpha^(-2/3) gamma'", "g \u00bc a\x04"),
        ("eq. (11)  ... Qj - p/2N ...", "Qj \x04 p"),
        ("eq. (11)  ... Qj + p/2N   (the PLUS, for contrast)", "\x01 Qi <"),
        ("prose     'Theta-angle'  — the same char as a hyphen", "\x04angle"),
    ]
    for label, needle in probes:
        hit = next((ln.strip() for p in pages for ln in p.splitlines()
                    if needle in ln), None)
        if hit is None:
            print(f"    {label}\n        probe {needle!r} NOT FOUND — the scan "
                  "may have been re-supplied in a different form")
            return 1
        print(f"        {label}")
        print(f"            extracts as: {hit!r}")

    print("\n        \\x04 is minus in eq. (6) and eq. (11), and a hyphen in")
    print("        'Theta-angle'. It is non-printable: any printable-character")
    print("        filter drops it, turning alpha^(-2/3) into alpha^(2/3) — the")
    print("        wrong-sign reading — with no glyph-level trace. (The plus in")
    print("        eq. (11) maps to a different char, so plus and minus are not")
    print("        literally identical; they are simply both unreadable as signs.)")
    print("\n    (c) The extraction-quality gate cannot see any of this, twice over:\n")
    c0_raw = sum(1 for ch in raw if ord(ch) < 32 and ch not in "\n\t\r")
    pua_raw = sum(1 for ch in raw if 0xE000 <= ord(ch) <= 0xF8FF)
    c0_md = sum(1 for ch in md if ord(ch) < 32 and ch not in "\n\t\r")
    print(f"        raw text layer:  {c0_raw:>3} C0 control chars, {pua_raw:>3} PUA glyphs")
    print(f"        committed .md:   {c0_md:>3} C0 control chars")
    print("\n        scan-extraction-quality.py flags PUA (U+E000-F8FF).  This")
    print("        font maps its unmapped glyphs into the C0 range instead, so")
    print("        the detector's range misses every one of them — and it runs")
    print("        on the .md, which the vision pass already laundered clean.")
    print("        It reports 0/2 files flagged for this document.")

    print("\n    -> Neither surface can settle a sign worth a factor of alpha^2,")
    print("       and no mechanical gate in this repo would notice.  Only the")
    print("       source's own algebra can, which is what part 3 does.")
    return 0


def alpha_exponent():
    """Recover the exponent on alpha in eq. (5) from the source's own algebra.

    eq. (5) is eq. (2) substituted into eq. (4).  Writing eq. (5) with an
    unknown exponent s,

        mu_5(s) = 1/2 (2 sigma_F / (rho^(1/3) alpha^s gamma'))^(3/2) (r/V)^3
                = mu_5(0) * alpha^(-3s/2)

    and requiring mu_5(s) == mu_4 = 1/2 alpha rho x0^3 gives s = -2/3 exactly.
    Solved numerically here at several alpha so the answer cannot come from
    the same reading it is meant to check.
    """
    print("\n3. CLOSURE — what exponent on alpha does eq. (5) require?\n")
    print("    Part 2 showed neither surface can settle the sign.  The source\n"
          "    can: eq. (5) is stated to BE eq. (2) substituted into eq. (4),\n"
          "    so solve that requirement for the exponent.\n")

    sigma_f, rho, gamma_p, r_over_v = 8.0e8, 7850.0, 47.0, 2.0e-5
    x0 = np.sqrt(2.0 * sigma_f / (rho * gamma_p)) * r_over_v

    print(f"    {'alpha':>8} {'mu via eq. (4)':>16} {'exponent s':>12}")
    exponents = []
    for alpha in (0.25, 0.5, 2.0, 3.6, 10.0):
        mu_4 = 0.5 * alpha * rho * x0**3
        mu_5_at_zero = 0.5 * (2.0 * sigma_f / (rho ** (1 / 3) * gamma_p)) ** 1.5 * r_over_v**3
        s = -(2.0 / 3.0) * np.log(mu_4 / mu_5_at_zero) / np.log(alpha)
        exponents.append(s)
        print(f"    {alpha:>8.2f} {mu_4:>16.6e} {s:>12.6f}")

    ok = np.allclose(exponents, -2.0 / 3.0)
    print(f"\n    -> s = {np.mean(exponents):+.6f}  "
          f"({'matches' if ok else 'DOES NOT MATCH'} eq. (6)'s alpha^(-2/3))")
    if not ok:
        return 1

    # The extraction must carry that sign; a positive exponent would be the
    # single-character defect this whole check exists to exclude.
    text = EXTRACT.read_text(encoding="utf-8")
    for want in (r"\alpha^{-2/3} \gamma'", r"\rho^{1/3} \alpha^{-2/3} \gamma'"):
        present = want in text
        print(f"    extraction carries {want!r}: {'yes' if present else 'NO'}")
        if not present:
            return 1
    print("    -> the .md's vision reconstruction agrees with the algebra. That")
    print("       agreement is what promotes it from an unchecked model reading")
    print("       to a checked one — it is not evidence on its own.")
    return 0


def eq7_is_eq16():
    """eq. (7) and eq. (16) are the same formula; the repo cites both names."""
    print("\n4. Is eq. (16) the same formula as eq. (7)?\n")
    rng = np.linspace(1.0, 4.0, 7)
    sigma_f, rho = 8.0e8 * rng, 7850.0 * (1.0 + 0.05 * rng)
    gamma, r_over_v = 47.0 * rng, 2.0e-5 * rng

    mu_7 = 0.5 * (2.0 * sigma_f / (rho ** (1 / 3) * gamma)) ** 1.5 * r_over_v**3
    mu_16 = np.sqrt(2.0 / rho) * (sigma_f / gamma) ** 1.5 * r_over_v**3

    rel = np.max(np.abs(mu_7 / mu_16 - 1.0))
    print(f"    max relative difference over {rng.size} parameter sets: {rel:.3e}")
    print(f"    -> {'identical' if rel < 1e-12 else 'DIFFERENT'}  "
          "(the 1/2 . 2^(3/2) = sqrt(2) collapse)")
    return 0 if rel < 1e-12 else 1


def shipped_composition():
    """Does mott_params reproduce eq. (4) evaluated directly?

    `mott_params` builds mu the long way -- eq. (2) for x0, then eq. (6) to
    fold alpha into gamma, then eq. (16).  Eq. (4) reaches the same mu in one
    step.  They agree only if the shipped exponent has the sign recovered
    above, so this is the shipped-code end of the same closure.
    """
    print("\n5. Does src/arty's composition equal eq. (4) evaluated directly?\n")
    shell = ShellParams()
    for v0 in (800.0, 1000.0, 1200.0):
        r_outer, r_inner, r_bu, mass_shell = _shell_geometry(shell)
        t_bu = shell.wall_t * 0.5 * (r_outer + r_inner) / r_bu
        x0 = np.sqrt(2.0 * shell.steel.sigma_f
                     / (shell.steel.rho * shell.steel.gamma)) * r_bu / v0
        alpha = shell.aspect_ratio * shell.breadth_factor**2 * t_bu / x0

        mu_eq4 = 0.5 * alpha * shell.steel.rho * x0**3      # the page, one step
        mu_shipped, n0_shipped = mott_params(shell, v0)     # the code, three

        rel = abs(mu_shipped / mu_eq4 - 1.0)
        n0_eq1 = mass_shell / (2.0 * mu_eq4)                # eq. (1)
        n0_eq17 = mass_shell / mu_eq4                       # eq. (17)
        print(f"    V0 = {v0:>6.0f} m/s   alpha = {alpha:.3f}   "
              f"mu eq.(4) = {mu_eq4:.6e} kg   shipped = {mu_shipped:.6e} kg   "
              f"rel = {rel:.2e}")
        print(f"{'':>21}N0: eq.(1) = {n0_eq1:>8.1f}   eq.(17) = {n0_eq17:>8.1f}"
              f"   shipped = {n0_shipped:>8.1f}")
        if rel > 1e-12:
            print("    -> FAIL: the shipped composition does not equal eq. (4)")
            return 1
        if abs(n0_shipped / n0_eq1 - 1.0) > 1e-12:
            print("    -> FAIL: shipped N0 follows neither eq. (1) nor eq. (17)")
            return 1

    print("\n    -> shipped mu matches eq. (4) exactly, which fixes the sign of")
    print("       the alpha exponent in the shipped code as well.")
    print("    -> shipped N0 follows eq. (1) (M/2mu).  The paper's own eq. (17)")
    print("       (m_j/mu_j) disagrees with eq. (1) by exactly 2 and would")
    print("       double every fragment count; the code does NOT use it.")
    print("       eq. (1) is the self-consistent one -- mu is defined two")
    print("       sentences earlier as HALF the average fragment mass, so a")
    print("       count of total mass over mu is a count of half-fragments.")
    return 0


def main():
    rc = (provenance() or sign_is_unreadable() or alpha_exponent()
          or eq7_is_eq16() or shipped_composition())
    print("\nRESULT: " + ("PASS — the equations src/arty implements are the "
                          "equations on the page." if rc == 0 else "FAIL"))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
