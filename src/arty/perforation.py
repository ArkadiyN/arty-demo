"""Target-perforation thresholds: how much energy a fragment needs to get through.

Implements the plug-shear wood-perforation threshold (Option A″) derived and
validated in
``experiment/fragmentation-field/updates/sourced-wood-perforation-threshold/derivation.md``
§7.3 (model), §7.4 (validation), §7.6 (what this module inherits).

The governing form, derivation.md §7.3 eq. (9): a plug of diameter ``D``
shearing out of a panel of thickness ``t`` presents a cylindrical shear surface
``pi D (t - x)`` at displacement ``x``, so the work to push it through is

    E_thr(m) = int_0^t tau pi D(m) (t - x) dx = eta tau pi D(m) t²,  eta = 1/2

with ``D(m) = (6 m / (pi rho_s))^(1/3)`` the compact (sphere-equivalent)
fragment diameter, i.e. ``E_thr ∝ m^(1/3)`` and
``v50(m) = sqrt(2 E_thr / m) ∝ m^(-1/3)``.

Nothing here is fitted. ``t`` is Tolch's 1-inch panel, ``rho_s`` is steel,
``eta`` = 1/2 is the linear shear-area-decay geometry (``eta`` = 1 is the rigid
upper bound; per assumption A8 it is *not* free to be tuned to a count), and
``tau`` is a measured ASTM D143 coupon value from Sanborn et al. 2019 Table 2
(``doc-reference/fragmentation/sanborn2019-clt-ballistic-performance/source.md``,
greppable anchor ``Shear Strength Parallel to Grain, ASTM D143``).

Reference numbers this module must reproduce are printed by
``experiment/fragmentation-field/updates/sourced-wood-perforation-threshold/checks/plug-shear-perforation-threshold.py``.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

# Unit conversion, exact by definition of the pound-force and the inch.
_PSI_TO_PA = 6894.757

# --- Sanborn et al. 2019, Table 2 -------------------------------------------
# "Shear Strength Parallel to Grain, ASTM D143", solid-wood coupons (NOT the
# CLT bond-line rows, 399 / 880 psi, which measure a different plane).
# Table 2 prints both US and SI; the psi column is taken as primary and the
# printed SI values agree to <= 0.29% (admissibility closure, derivation.md
# §7.3 / check script §1).
TAU_SPFS = 1300.0 * _PSI_TO_PA   # spruce-pine-fir south [Pa]; printed 8.96 MPa
TAU_SYP = 1600.0 * _PSI_TO_PA    # southern yellow pine   [Pa]; printed 11.0 MPa
TAU_SPFS_COV = 0.27              # coefficient of variation [-], n = 14
TAU_SYP_COV = 0.13               # coefficient of variation [-], n = 19

T_PANEL_1IN = 0.0254             # Tolch's 1-inch softwood panel [m]
ETA_LINEAR = 0.5                 # linear shear-area decay [-] (derivation §7.3)
ETA_RIGID = 1.0                  # rigid upper bound [-], full tau pi D t travel

RHO_STEEL_DEFAULT = 7850.0       # fragment steel density [kg/m³]


@dataclass(frozen=True)
class WoodPanelTarget:
    """A softwood panel target for the plug-shear perforation threshold.

    tau       : shear strength of the panel material [Pa]
    t         : panel thickness [m]
    eta       : shear-area-decay geometry constant [-] (1/2 linear, 1 rigid bound)
    rho_steel : fragment steel density [kg/m³], sets D(m)

    Defaults are derivation.md §7.6: SPF-S solid-wood coupon tau, Tolch's 1-inch
    panel, eta = 1/2, steel at 7850 kg/m³.
    """

    tau: float = TAU_SPFS
    t: float = T_PANEL_1IN
    eta: float = ETA_LINEAR
    rho_steel: float = RHO_STEEL_DEFAULT


#: The panel the fragmentation-field work is anchored on (Tolch 1 in, SPF-S).
TOLCH_1IN_SOFTWOOD = WoodPanelTarget()


def compact_fragment_diameter(
    m: np.ndarray | float, rho_steel: float = RHO_STEEL_DEFAULT
) -> np.ndarray | float:
    """Sphere-equivalent diameter [m] of a compact fragment of mass m [kg].

    The compact-fragment closure logged in derivation.md §5.1: the fragment is
    treated as a sphere of the same mass and density,
    ``D = (6 m / (pi rho_steel))^(1/3)``. This is the *shape closure only* — it
    is deliberately not the drag shape factor ``C_shape`` in
    :mod:`arty.fragmentation`, which encodes a measured ballistic density for an
    irregular fragment.
    """
    return (6.0 * np.asarray(m, dtype=float) / (np.pi * rho_steel)) ** (1.0 / 3.0)


def perforation_threshold_energy(
    m: np.ndarray | float, target: WoodPanelTarget = TOLCH_1IN_SOFTWOOD
) -> np.ndarray | float:
    """Plug-shear energy [J] to perforate ``target`` with a fragment of mass m [kg].

    ``E_thr = eta tau pi D(m) t²`` — derivation.md §7.3 eq. (9), with
    ``D(m)`` from :func:`compact_fragment_diameter`. Rises as ``m^(1/3)``:
    a heavier (hence larger) fragment must shear a wider plug out of the panel.
    """
    D = compact_fragment_diameter(m, target.rho_steel)
    return target.eta * target.tau * np.pi * D * target.t * target.t


def ballistic_limit_velocity(
    m: np.ndarray | float, target: WoodPanelTarget = TOLCH_1IN_SOFTWOOD
) -> np.ndarray | float:
    """Ballistic-limit (v50) velocity [m/s] for mass m [kg] against ``target``.

    ``v50 = sqrt(2 E_thr(m) / m)`` — derivation.md §7.3 eq. (10). Falls as
    ``m^(-1/3)`` and diverges as ``m -> 0``: a very light fragment shears the
    same plug perimeter with far less momentum to spend.
    """
    m_arr = np.asarray(m, dtype=float)
    return np.sqrt(2.0 * perforation_threshold_energy(m_arr, target) / m_arr)
