## Context

`app/sensitivity.py` drives `compute_frag_field_3d` (fragmentation.py), a single-cylinder model that collapses the entire shell into one belt with a user-supplied `spray_half_angle`. The `frag-field-3d-geometry` merge added `src/arty/zones.py` which provides:

- `compute_shell_zones(shell)` → `ShellZones` — decomposes the shell into four zones using drawing-derived arc geometry (Tier-1) or CRH/fraction fallback (Tier-2).
- `four_zone_field(zones, aof_deg, h_b, posture, drag_lam_grid, m_grid, ...)` → `(X, Y, pk_grid)` — P(kill) ground field using per-zone spray angles.

The app currently drops the ogive geometry fields when constructing `ShellParams` from sliders, and has no way to compare old vs new models.

## Goals / Non-Goals

**Goals:**

- Add a Model radio (Single-zone / Four-zone) so both models are accessible
- Side-by-side heatmaps + diff map when Four-zone is active
- Zone Breakdown section: grouped bar (V₀/N₀/spray angle per zone) + per-zone P(kill) vs cross-range
- Thread ogive geometry from the selected preset into `ShellParams`
- Keep headline metrics meaningful for both models; label "(cyl zone)" on four-zone path
- Tier badge in sidebar when Four-zone is active

**Non-Goals:**

- Per-zone sliders (ogive geometry is drawing-derived)
- Modifying `zones.py` or `fragmentation.py` physics
- Zone breakdown visible in Single-zone mode

## Decisions

### 1. Model radio drives layout branching

A `st.radio("Model", ["Single-zone (legacy)", "Four-zone (new)"])` in the sidebar controls which compute path is used. In Single-zone mode the app is identical to the current state. In Four-zone mode the heatmap section and Zone Breakdown section appear. This avoids always computing both (expensive) while making the comparison opt-in.

**Alternatives considered:** Always compute both and show comparison. Rejected — doubles compute cost per interaction; caching still requires two sets of params to be stable.

### 2. Side-by-side heatmaps in Four-zone mode

When Four-zone is active, `st.columns(2)` holds the legacy heatmap (left) and the four-zone heatmap (right). A full-width difference heatmap (Pk_4z − Pk_1z, diverging colorscale centred at 0) spans below. Both heatmaps use the same grid extent so subtraction is direct.

**Rationale:** Seeing the absolute fields plus the signed diff gives an immediate sense of magnitude and spatial pattern of the improvement.

### 3. Cylinder zone as representative headline metric in Four-zone mode

V₀, N₀, μ headline metrics use `zones.cylinder` values, labelled "(cyl zone)". Mass-weighted average rejected — harder to interpret, deviates from what the experiment notebook already presents.

### 4. Per-zone P(kill) cross-range: extracted from the full grid

Each zone's contribution to `field_N` is extracted by running `four_zone_field` with a single-zone `ShellZones` (all other zones zeroed) — but that would require four extra calls. Instead: during the single call we accumulate per-zone `field_N_z` arrays alongside the total. This requires a small helper `_four_zone_field_split` that returns `(X, Y, pk_total, pk_by_zone)` with `pk_by_zone` a dict keyed by zone name. The cross-range slice (column nearest x=0) of each `pk_by_zone[z]` gives the per-zone P(kill) curve.

**Alternative:** Four separate calls each with a single-zone ShellZones. Rejected — 4× the compute cost; adding the split helper is cheap.

### 5. Zone bar chart: three grouped bar traces per zone

The grouped bar chart has one `go.Bar` trace per metric (V₀, N₀, spray angle), x-axis = zone name. This is a single Plotly figure with `barmode="group"`. N₀ and V₀ are on different scales so the chart uses a secondary y-axis for N₀ (fragment count), primary for V₀ [m/s] and spray angle [°].

**Simpler alternative:** Three separate charts. Rejected — wastes vertical space; grouped bar conveys relative magnitude across zones at a glance.

### 6. Ogive fields always taken from preset; no sliders

The `ShellParams` constructor call passes `ogive_outer_R`, `ogive_inner_R`, `ogive_len`, `ogive_tip_dia`, `cylinder_len`, `boattail_len`, `boattail_angle_deg`, `boattail_inner_dia`, `base_thickness`, `has_boattail`, `base_treatment`, `ogive_crh` from `preset` verbatim. Only the five editable scalars (mass_total, mass_filler, caliber, wall_t, steel params) remain slider-driven.

### 7. Cache keying

Two `@st.cache_data` functions — `_compute_legacy` and `_compute_zones` — each keyed on their actual inputs. `_compute_legacy` takes the same arguments as before. `_compute_zones` takes `shell_name` (string) plus the scalar editables; the ogive fields are looked up from `SHELLS[shell_name]` inside the function, so the cache key remains compact and collision-free.

## Risks / Trade-offs

`four_zone_field` at `n_grid=60` is ~200 ms on a modern laptop; side-by-side requires the legacy field at the same resolution, so total cold-compute is ~250 ms. Cached reuse means this only fires on param change. Acceptable.

The `_four_zone_field_split` helper must exactly reproduce the aggregation logic of `four_zone_field`. Any divergence causes inconsistency between the total heatmap and the per-zone charts. → **Mitigation**: assert `abs(pk_total_split - pk_total_direct).max() < 1e-9` in a debug guard.

The diff heatmap `Pk_4z − Pk_1z` compares results computed on grids of the same `(n_grid, max_radius)` but with different geometry models; they are subtractable directly since they share the same `(X, Y)` meshgrid from `np.linspace(-max_radius, max_radius, n_grid)`.
