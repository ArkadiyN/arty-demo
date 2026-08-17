"""B(r) at 155 mm for the candidate breadth-variance factors k (Action C).

Consumer: experiment/fragmentation-field/updates/breadth-variance-factor-k/derivation.md
section 3.  Re-runs the committed sweep
experiment/fragmentation-field/updates/mass-dependent-fragment-shape/checks/bofr-at-new-mu.py
unmodified, with its C_VALUES replaced by c_155 * k for each candidate k, so the
comparison against the drag-gap-1944 Table 59 casualty card is like-for-like.

k candidates:
  1.00   shipped (A9.1 deferred)
  1.1375 Mott 1947 ruled-line MC, Mott's own scheme at l/x0 = 20
  1.1954 Mott 1947 ruled-line MC, exact Poisson at l/x0 = 200 (converged)
  2.00   Mott & Linfoot 1943 sect. 3 exponential-breadth assumption
"""

import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[5]
SRC = (
    ROOT
    / "experiment/fragmentation-field/updates/mass-dependent-fragment-shape/checks"
    / "bofr-at-new-mu.py"
)

C_155 = 1.2506  # shipped MOTT_ASPECT_MOMENT_C["155mm M107 HE"]
K_CANDIDATES = (1.00, 1.1375, 1.1954, 2.00)


def main():
    spec = importlib.util.spec_from_file_location("bofr_at_new_mu", SRC)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    c_values = tuple(round(C_155 * k, 4) for k in K_CANDIDATES)
    setattr(mod, "C_VALUES", c_values)
    print("k candidates      :", K_CANDIDATES)
    print("c_155 * k (=A_eff/1.6):", c_values, "\n")
    mod.main()


if __name__ == "__main__":
    main()
