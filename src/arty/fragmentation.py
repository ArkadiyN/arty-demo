from __future__ import annotations

from dataclasses import dataclass

import numpy as np

# ---------------------------------------------------------------------------
# Parameter structs
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ShellParams:
    caliber: float = 0.105  # outer diameter [m]
    wall_t: float = 0.011  # cylindrical wall thickness [m]
    mass_total: float = 14.97  # total projectile mass [kg]
    mass_filler: float = 2.18  # explosive filler mass [kg]
    mass_deductions: float = 0.75  # fuze + rotating band [kg]
    gurney_const: float = 2700.0  # Gurney constant sqrt(2E) [m/s]
    rho_steel: float = 7850.0  # steel density [kg/m³]


@dataclass(frozen=True)
class MottParams:
    gamma: float = 65.0  # Mott statistical fragmentation parameter [-]
    sigma_f: float = 800e6  # dynamic flow stress at fracture [Pa]


@dataclass(frozen=True)
class DragParams:
    C_D: float = 0.65  # drag coefficient, tumbling irregular fragment
    C_shape: float = 0.90  # presented-area shape factor
    rho_air: float = 1.225  # air density [kg/m³]


@dataclass(frozen=True)
class TargetParams:
    w: float = 0.5  # presented width of target [m]


# ---------------------------------------------------------------------------
# Result struct
# ---------------------------------------------------------------------------


@dataclass
class FragFieldResult:
    r: np.ndarray  # radial distance from burst [m]
    p_kill: np.ndarray  # p_kill at each r
    r50: float  # range at which p_kill = 0.5 [m]
    ke_by_mass: dict[float, np.ndarray]  # {mass_g: KE array [J]}
    field_x: np.ndarray  # 2D meshgrid X [m]
    field_y: np.ndarray  # 2D meshgrid Y [m]
    field_pk: np.ndarray  # p_kill on 2D grid
    N0: float  # total fragment count
    mu: float  # Mott half-mass [kg]
    V0: float  # initial fragment velocity [m/s]


# ---------------------------------------------------------------------------
# ES-310 Pk|hit anchors (FAS/Navy 1998)
# ---------------------------------------------------------------------------

_PK_E = np.array([100.0, 1000.0, 4000.0])  # KE anchors [J]
_PK_VAL = np.array([0.10, 0.50, 0.90])  # corresponding Pk|hit [-]


# ---------------------------------------------------------------------------
# Internal geometry helper
# ---------------------------------------------------------------------------


def _shell_geometry(shell: ShellParams) -> tuple[float, float, float, float]:
    r_outer = shell.caliber / 2.0
    r_inner = r_outer - shell.wall_t
    r_inner_bu = r_inner * np.sqrt(3.0)
    r_outer_bu = np.sqrt(r_inner_bu**2 + (r_outer**2 - r_inner**2))
    r_bu = 0.5 * (r_inner_bu + r_outer_bu)
    mass_shell = shell.mass_total - shell.mass_filler - shell.mass_deductions
    return r_outer, r_inner, r_bu, mass_shell


# ---------------------------------------------------------------------------
# Physics functions
# ---------------------------------------------------------------------------


def gurney_velocity(shell: ShellParams) -> float:
    _, _, _, mass_shell = _shell_geometry(shell)
    return shell.gurney_const / np.sqrt(mass_shell / shell.mass_filler + 0.5)


def mott_params(shell: ShellParams, mott: MottParams, V0: float) -> tuple[float, float]:
    _, _, r_bu, mass_shell = _shell_geometry(shell)
    mu = (
        np.sqrt(2.0 / shell.rho_steel)
        * (mott.sigma_f / mott.gamma) ** 1.5
        * (r_bu / V0) ** 3
    )
    N0 = mass_shell / (2.0 * mu)
    return mu, N0


def retardation_coeff(m: np.ndarray, drag: DragParams, rho_steel: float) -> np.ndarray:
    return (
        drag.rho_air
        * drag.C_D
        * drag.C_shape
        / (2.0 * rho_steel ** (2.0 / 3.0))
        * m ** (-1.0 / 3.0)
    )


def pk_given_hit(E: np.ndarray) -> np.ndarray:
    logE = np.log10(np.clip(np.asarray(E, dtype=float), 1e-3, None))
    return np.interp(logE, np.log10(_PK_E), _PK_VAL, left=0.0, right=0.9)


def expected_kills(
    r: np.ndarray,
    N0: float,
    mu: float,
    V0: float,
    drag: DragParams,
    rho_steel: float,
    w: float,
    n_mass: int = 300,
) -> np.ndarray:
    m_grid = np.logspace(-6, np.log10(0.5), n_mass)
    pdf = N0 / (2.0 * np.sqrt(mu * m_grid)) * np.exp(-np.sqrt(m_grid / mu))
    lam = retardation_coeff(m_grid, drag, rho_steel)
    out = np.empty_like(r, dtype=float)
    for i, ri in enumerate(r):
        E = 0.5 * m_grid * (V0 * np.exp(-lam * ri)) ** 2
        integrand = pdf * pk_given_hit(E) * w / (2.0 * np.pi * ri)
        out[i] = np.trapezoid(integrand, m_grid)
    return out


# ---------------------------------------------------------------------------
# Top-level entry point
# ---------------------------------------------------------------------------


def compute_frag_field(
    shell: ShellParams = ShellParams(),
    mott: MottParams = MottParams(),
    drag: DragParams = DragParams(),
    target: TargetParams = TargetParams(),
    max_radius: float = 300.0,
    n_r: int = 200,
) -> FragFieldResult:
    V0 = gurney_velocity(shell)
    mu, N0 = mott_params(shell, mott, V0)

    r = np.linspace(1.0, max_radius, n_r)
    N_eff = expected_kills(r, N0, mu, V0, drag, shell.rho_steel, target.w)
    pk = 1.0 - np.exp(-N_eff)

    # R₅₀: distance from burst where p_kill crosses 0.5
    idx50 = np.argmin(np.abs(pk - 0.5))
    r50 = float(r[idx50])

    # KE vs distance from burst for three representative masses
    rep_masses_g = [0.5, 5.0, 50.0]
    rep_masses_kg = np.array([m * 1e-3 for m in rep_masses_g])
    lam_rep = retardation_coeff(rep_masses_kg, drag, shell.rho_steel)
    ke_by_mass: dict[float, np.ndarray] = {}
    for m_g, lam_j in zip(rep_masses_g, lam_rep):
        ke_by_mass[m_g] = 0.5 * (m_g * 1e-3) * (V0 * np.exp(-lam_j * r)) ** 2

    # 2D field (radially symmetric, interpolated from 1D result)
    grid_n = 120
    xy = np.linspace(-max_radius, max_radius, grid_n)
    X, Y = np.meshgrid(xy, xy)
    R_grid = np.sqrt(X**2 + Y**2)
    pk_grid = np.interp(R_grid.ravel(), r, pk, left=float(pk[0]), right=0.0)
    field_pk = pk_grid.reshape(R_grid.shape)

    return FragFieldResult(
        r=r,
        p_kill=pk,
        r50=r50,
        ke_by_mass=ke_by_mass,
        field_x=X,
        field_y=Y,
        field_pk=field_pk,
        N0=N0,
        mu=mu,
        V0=V0,
    )
