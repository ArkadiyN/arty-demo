## Context

The notebook's §6 derives and implements a full 3D burst geometry: fragment rays from burst point `B = (0, 0, h_b)`, shell axis tilted by angle of fall α, belt spray at Θ = 90° ± δ, and posture-dependent presented area `A_p(γ) = w_perp·(h·cosγ + d·sinγ)`. This code lives only in the notebook (`experiment/fragmentation-field/fragmentation-field.qmd`). The library (`src/arty/fragmentation.py`) still exports only the 1D flat-trajectory API, and the app (`app/sensitivity.py`) uses only that old API.

## Goals / Non-Goals

**Goals:**

- Port 3D geometry API to `src/arty/fragmentation.py` as new public symbols (`BurstParams`, `PostureParams`, `STANDING`, `PRONE`, `compute_frag_field_3d`)
- Update `app/sensitivity.py` to expose burst height, AoF, spray angle, and posture controls
- Show the asymmetric 2D footprint in the heatmap
- Keep the old `compute_frag_field` intact (backward compat for any existing tests)

**Non-Goals:**

- Modifying Mott, Gurney, drag, or ES-310 logic
- Adding gravity, ricochet, or cover models (§9 future enhancements)
- Changing the notebook itself

## Decisions

**D1 — Extend `fragmentation.py` in-place, no new module.**
All 3D symbols go into `src/arty/fragmentation.py`. Keeps the import surface flat (`from arty.fragmentation import BurstParams, STANDING`). The file already has logical sections separated by comments — add a `# 3D burst geometry` section after the existing helpers.

**D2 — `BurstParams` dataclass.**

```python
@dataclass
class BurstParams:
    h_b: float = 2.0          # burst height [m]
    angle_of_fall: float = 30.0  # degrees, 0 = horizontal, 90 = vertical
    spray_half_angle: float = 15.0  # belt half-width δ [degrees]
```

**D3 — `PostureParams` dataclass + two named instances.**

```python
@dataclass
class PostureParams:
    w_perp: float   # body width [m]
    h: float        # vertical extent (standing) [m]
    d: float        # top-down extent (depth) [m]

STANDING = PostureParams(w_perp=0.5, h=1.7, d=0.3)
PRONE    = PostureParams(w_perp=0.5, h=0.3, d=1.8)
```

**D4 — `compute_frag_field_3d` returns `FragField3dResult`.**
New result dataclass extending the 1D info with 2D asymmetric footprint and burst metadata:

```python
@dataclass
class FragField3dResult:
    field_x: np.ndarray      # 2D meshgrid X [m]
    field_y: np.ndarray      # 2D meshgrid Y [m]
    field_pk: np.ndarray     # P(kill) on 2D grid
    r_cross: np.ndarray      # cross-range slice at x=0 [m]
    pk_cross: np.ndarray     # P(kill) along cross-range slice
    r50_cross: float         # R50 along cross-range [m]
    ke_by_mass: dict         # same as 1D result
    N0: float
    mu: float
    V0: float
    burst: BurstParams
    posture: PostureParams
```

The cross-range slice replaces the 1D radial curve (which is no longer symmetric).

**D5 — App sidebar structure.**
Add a new `"Burst Geometry"` expander with: `h_b` slider (0–20 m), `angle_of_fall` slider (0–90°), `spray_half_angle` slider (5–30°). Replace the `"Target"` expander's raw width slider with a posture radio button (`Standing` / `Prone`). Update title caption to remove "flat trajectory".

**D6 — 2D heatmap uses actual grid, not radial interpolation.**
The old `field_pk` was `np.interp` from a 1D result — it was always radially symmetric. The 3D result computes `field_pk` directly on the mesh from `compute_frag_field_3d`. Same grid resolution (120×120) for consistent performance.

## Risks / Trade-offs

- **Compute time**: `compute_frag_field_3d` on a 120×120 grid calls `expected_kills_3d` 14 400 times. Each call integrates over 300 mass bins. At h_b=0, AoF=0° many ground intercepts are skipped (no belt hit), keeping it fast; but at intermediate AoF and large grids it may be slow. Mitigate: use `n_grid=80` (6 400 points) as the default for the app, with a note.
- **Backward compat**: `compute_frag_field` and `FragFieldResult` are unchanged. No risk.
- **h_b ≈ 0 ground-burst limit**: The 3D model with h_b=0.001 m should match the 1D model closely (within ~5%) for AoF=0°. This is already checked in the notebook (Check 6.1) but should be a test in `test_fragmentation.py`.
