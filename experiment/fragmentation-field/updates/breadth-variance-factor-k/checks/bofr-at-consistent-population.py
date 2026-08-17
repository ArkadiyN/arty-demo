"""B(r) at 155 mm for the population-consistent (c, k) pair (review.md fix B2).

Consumer: experiment/fragmentation-field/updates/breadth-variance-factor-k/
derivation.md section 3 (post-fix table).

Re-runs the committed sweep
experiment/fragmentation-field/updates/mass-dependent-fragment-shape/checks/
bofr-at-new-mu.py unmodified, with C_VALUES = c*k for four (c, k) pairs that
differ in WHICH POPULATION each moment is averaged over:

  A_eff/1.6 = c*k
  1.2506  shipped        c on the 1943-descended Mott spectrum, k = 1 (A9.1 open)
  1.4226  mixed          c on the Mott spectrum x k on the 1947 ruled line
                         (what the pre-fix derivation shipped; review B2 rejects)
  1.2802  ruled line     BOTH moments on the 1947 ruled-line population
                         (checks/c-on-ruled-line-population.py: c = 1.1254,
                          k = 1.1375)
  1.8748  1943 spectrum  BOTH moments on the Mott spectrum, at Table-3's 5-bin
                         resolution (spectrum-weighted-c-per-shell.py:
                          c = 1.2404, k = 1.5114); the bin-converged k = 1.74-1.98
                          would put this at c*k = 2.2-2.5 instead
"""

import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[5]
SRC = (
    ROOT
    / "experiment/fragmentation-field/updates/mass-dependent-fragment-shape/checks"
    / "bofr-at-new-mu.py"
)

PAIRS = {
    "shipped     (c=1.2506 spectrum, k=1)": 1.2506,
    "mixed       (c=1.2506 spectrum, k=1.1375 ruled)": 1.2506 * 1.1375,
    "ruled line  (c=1.1254 ruled,    k=1.1375 ruled)": 1.1254 * 1.1375,
    "ruled line, marginal closure (c=1.0372, k=1.1375)": 1.0372 * 1.1375,
    "1943 spec.  (c=1.2404 spectrum, k=1.5114 spectrum)": 1.2404 * 1.5114,
}


def main():
    spec = importlib.util.spec_from_file_location("bofr_at_new_mu", SRC)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    for label, ck in PAIRS.items():
        print(f"{label}   c*k = {ck:.4f}   A_eff = {1.6 * ck:.4f}")
    print()
    setattr(mod, "C_VALUES", tuple(round(v, 4) for v in PAIRS.values()))
    mod.main()


if __name__ == "__main__":
    main()
