"""Reproduce Mott 1947's ruled-line Monte Carlo and read off the breadth moments.

Consumer: experiment/fragmentation-field/updates/breadth-variance-factor-k/derivation.md
section 2.4 (Action A). Produces the mean breadth <x>/x0 (Mott finding (1): ~1.5),
the breadth-variance factor k = <x^2>/<x>^2, and the 0.4-x0 histogram Mott plots
in his figure 4.

Model (Mott 1947, "Fragmentation of shell cases", rspa.1947.0042, pp. 304-305):
  - ring of circumference l, periodic, lengths in units of the release-wave
    scale x0 = (2 P_y / rho v)^{1/2} r / v.
  - with sigma = gamma s and the normalisation (l C / gamma) e^{sigma_0} = 1,
    write tau = sigma - sigma_0.  Eq. (4) becomes  dn/dtau = f e^{tau},
    with f the still-stressed (unshielded) fraction of the ring; equivalently
    the nucleation rate per unit *unshielded* length is e^{tau} / l.
  - eq. (5): a crack born at tau_j shields  +/- sqrt(tau - tau_j)  around itself.
  - first crack at tau = 0; iterate until the ring is fully shielded (f = 0).
  - fragments are the gaps between adjacent cuts.

Two nucleation schemes are run as a cross-check that the result is Mott's model
and not Mott's quadrature:
  "mott"    - Mott's own deterministic increment  dtau = 1 / (f e^{tau})
  "poisson" - exact inhomogeneous Poisson thinning on the unshielded set
"""

from __future__ import annotations

import numpy as np

E = np.e


def _shielded_fraction(pos: np.ndarray, born: np.ndarray, tau: float, ell: float):
    """Return (unshielded fraction f, merged shielded arcs) on a ring of length ell."""
    if pos.size == 0:
        return 1.0, []
    rad = np.sqrt(np.maximum(tau - born, 0.0))
    lo = pos - rad
    hi = pos + rad
    if np.any(hi - lo >= ell):
        return 0.0, [(0.0, ell)]
    # unwrap onto [0, ell) by splitting arcs that cross the seam
    arcs = []
    for a, b in zip(lo, hi):
        width = b - a
        a %= ell
        b = a + width
        if b <= ell:
            arcs.append((a, b))
        else:
            arcs.append((a, ell))
            arcs.append((0.0, b - ell))
    arcs.sort()
    merged: list[list[float]] = []
    for a, b in arcs:
        if merged and a <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    covered = sum(b - a for a, b in merged)
    f = max(0.0, 1.0 - covered / ell)
    return f, merged


def _free_intervals(merged, ell):
    """Complement of the merged shielded arcs on [0, ell)."""
    free = []
    cursor = 0.0
    for a, b in merged:
        if a > cursor:
            free.append((cursor, a))
        cursor = max(cursor, b)
    if cursor < ell:
        free.append((cursor, ell))
    return free


def _sample_free(free, rng):
    lens = np.array([b - a for a, b in free])
    tot = lens.sum()
    if tot <= 0:
        return None
    u = rng.random() * tot
    for (a, b), L in zip(free, lens):
        if u < L:
            return a + u
        u -= L
    return free[-1][1]


def one_ring(ell: float, rng: np.random.Generator, scheme: str = "mott"):
    """Simulate one ring; return the array of fragment breadths in units of x0."""
    pos = [rng.random() * ell]
    born = [0.0]
    tau = 0.0
    while True:
        p = np.array(pos)
        b = np.array(born)
        f, merged = _shielded_fraction(p, b, tau, ell)
        if f <= 1e-12:
            break
        if scheme == "mott":
            tau_next = tau + 1.0 / (f * np.exp(tau))
        else:
            # thinning: rate per unit unshielded length is e^{tau}/ell, and the
            # unshielded length only shrinks, so f(tau) <= f is a valid bound.
            tau_next = tau
            while True:
                # integrate the bounding rate f e^{t} from tau_next -> invert exactly
                u = rng.random()
                # P(no event in [t, t+dt]) = exp(-f (e^{t+dt} - e^{t}))
                arg = 1.0 - np.log(u) / (f * np.exp(tau_next))
                if arg <= 0:
                    tau_next = np.inf
                    break
                tau_next = tau_next + np.log(arg)
                f_now, _ = _shielded_fraction(p, b, tau_next, ell)
                if f_now <= 1e-12:
                    tau_next = np.inf
                    break
                if rng.random() < f_now / f:
                    break
                f = f_now
            if not np.isfinite(tau_next):
                break
        f2, merged2 = _shielded_fraction(p, b, tau_next, ell)
        if f2 <= 1e-12:
            break
        x = _sample_free(_free_intervals(merged2, ell), rng)
        if x is None:
            break
        pos.append(x)
        born.append(tau_next)
        tau = tau_next
    q = np.sort(np.array(pos))
    gaps = np.diff(np.concatenate([q, [q[0] + ell]]))
    return gaps


def run(ell: float, n_rings: int, scheme: str, seed: int = 20260817):
    rng = np.random.default_rng(seed)
    out = [one_ring(ell, rng, scheme) for _ in range(n_rings)]
    return np.concatenate(out)


def report(x: np.ndarray, label: str):
    m1 = x.mean()
    m2 = (x**2).mean()
    k = m2 / m1**2
    n = x.size
    # bootstrap s.e. on k
    rng = np.random.default_rng(7)
    ks = []
    for _ in range(200):
        s = rng.choice(x, size=n, replace=True)
        ks.append((s**2).mean() / s.mean() ** 2)
    print(
        f"{label:28s} n={n:7d}  <x>/x0={m1:6.4f}  <x^2>/x0^2={m2:6.4f}  "
        f"k={k:6.4f} +/- {np.std(ks):.4f}   frac in [1,2]x0={np.mean((x >= 1) & (x <= 2)):.3f}"
    )
    return m1, k


if __name__ == "__main__":
    print("Mott 1947 ruled-line Monte Carlo -- breadth moments (units of x0)\n")
    for scheme in ("mott", "poisson"):
        for ell in (20.0, 50.0, 200.0):
            x = run(ell, n_rings=max(200, int(8000 / ell)), scheme=scheme)
            report(x, f"scheme={scheme:7s} l/x0={ell:5.0f}")
        print()

    x = run(20.0, n_rings=400, scheme="mott")
    edges = np.arange(0.0, 4.01, 0.4)
    h, _ = np.histogram(x, bins=edges)
    print("Mott figure-4 histogram, l/x0=20, 0.4 x0 bins (fraction of fragments):")
    for lo, hi, c in zip(edges[:-1], edges[1:], h):
        print(f"  {lo:4.1f}-{hi:4.1f} x0 : {c / x.size:6.3f}  {'#' * int(60 * c / x.size)}")

    print("\nReference: exponential breadths (Mott & Linfoot 1943 sect. 3) give k = 2 exactly.")
