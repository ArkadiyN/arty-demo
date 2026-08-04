"""Gold (2017) eqs (2),(4),(5),(6),(7),(16) — the substitution closure.

Consumer: experiment/fragmentation-field/challenges/source-data-audit/
          review-provenance.md, item 2 (provenance gate).

WHY. `.claude/rules/source-data-fidelity.md` names this closure form: "a stated
equation is the substitution its source says it is ... doing that algebra IS the
closure ... it is the only form that survives a document whose glyphs are
unreliable, because it never reads the disputed character." Gold's `.md` is
vision-model output, so its LaTeX cannot be trusted glyph-by-glyph. The paper
states, verbatim at
doc-reference/fragmentation/fragment-size-distribution-conwep/
1-s2.0-S221491471730079X-main.md:

  L72  "In the equation (4) alpha = (l_0/x_0)(t_0/x_0). Substituting equation
        (2) into equation (4) results in"                       -> eq (5)
  L76  "Since the fragment distribution relationship (see equation (1))
        warrants knowledge of the average fragment mass but not the shape,
        introducing" gamma = alpha^(-2/3) gamma' (6) "allows equation (5) to
        be put in a simpler and more useful form"               -> eq (7)

Doing both substitutions is a pass/fail check on the extraction of all six
equations at once: a vision error in ANY of them breaks the identity.

The claim being tested (asserted in that folder's card.md, "What is *not*
certified"): Gold's gamma = 50 is the SHAPE-ABSORBED gamma of eq (6), not the
bare gamma'. The algebra settles the definition; the symbol usage at L190/L220
(gamma = 50 feeding eq (19)/(21), which carry the eq (16) form) settles which
slot the 50 enters.

No numbers are read off the page here -- the check is an algebraic identity,
evaluated at random positive points so a coincidence at one point cannot pass.

Usage:  uv run python experiment/_scratch/gold-2017-eq6-substitution-closure.py
Runtime: <1 s.
"""

import random

random.seed(20260803)

fails = 0


def report(label, ok, detail=""):
    global fails
    fails += not ok
    print(f"  {label:<58} {'PASS' if ok else 'FAIL'} {detail}")


def rel(a, b):
    return abs(a - b) / max(abs(a), abs(b))


worst = {"5": 0.0, "7": 0.0, "16": 0.0, "shape": 0.0}

for _ in range(2000):
    sF = random.uniform(0.1, 10.0)      # sigma_F, strength
    rho = random.uniform(0.1, 10.0)     # density
    gp = random.uniform(0.1, 10.0)      # gamma' (bare, eq 2)
    al = random.uniform(0.05, 20.0)     # alpha  = (l0/x0)(t0/x0), eq 4
    rV = random.uniform(0.1, 10.0)      # r / V

    # eq (2): x0 = (2 sigma_F / (rho gamma'))^(1/2) * r/V
    x0 = (2 * sF / (rho * gp)) ** 0.5 * rV
    # eq (4): mu = 1/2 alpha rho x0^3   <- the direct substitution
    mu_sub = 0.5 * al * rho * x0 ** 3

    # eq (5) as printed
    mu_5 = 0.5 * (2 * sF / (rho ** (1 / 3) * al ** (-2 / 3) * gp)) ** 1.5 * rV ** 3
    # eq (6)
    gam = al ** (-2 / 3) * gp
    # eq (7) as printed
    mu_7 = 0.5 * (2 * sF / (rho ** (1 / 3) * gam)) ** 1.5 * rV ** 3
    # eq (16) as printed (with r_j/V_j -> r/V, gamma_j -> gamma)
    mu_16 = (2 / rho) ** 0.5 * (sF / gam) ** 1.5 * rV ** 3

    worst["5"] = max(worst["5"], rel(mu_sub, mu_5))
    worst["7"] = max(worst["7"], rel(mu_5, mu_7))
    worst["16"] = max(worst["16"], rel(mu_7, mu_16))

    # The shape claim, stated as a limit: gamma == gamma' iff alpha == 1.
    worst["shape"] = max(worst["shape"], rel(gam, gp) if abs(al - 1) < 1e-12 else 0.0)

print("== Gold 2017: the substitutions the paper says it performs ==")
report("eq (2) into eq (4)  ==  eq (5) as printed", worst["5"] < 1e-12,
       f"worst relative residual {worst['5']:.2e} over 2000 random points")
report("eq (6) into eq (5)  ==  eq (7) as printed", worst["7"] < 1e-12,
       f"worst relative residual {worst['7']:.2e}")
report("eq (7)              ==  eq (16) as printed", worst["16"] < 1e-12,
       f"worst relative residual {worst['16']:.2e}")

# The cube limit the card relies on: alpha = 1 (l0 = t0 = x0) => gamma = gamma'.
gp = 50.0
for al, name in [(1.0, "cube  alpha=1"), (2.0, "alpha=2"), (0.5, "alpha=0.5")]:
    print(f"  gamma' = 50, {name:<14} -> gamma = alpha^(-2/3) gamma' = "
          f"{al ** (-2 / 3) * 50:.2f}")
print("  ...so reading Gold's gamma = 50 as a gamma' is exact ONLY at alpha = 1;")
print("     at alpha = 2 it understates gamma' by 37%, at alpha = 0.5 it")
print("     overstates it by 59%. Gold states no alpha, so the conversion is")
print("     unavailable and 50 must be used in the eq (6)/(7)/(16) gamma slot.")

print(f"\nRESULT: {fails} failure(s)")
raise SystemExit(1 if fails else 0)
