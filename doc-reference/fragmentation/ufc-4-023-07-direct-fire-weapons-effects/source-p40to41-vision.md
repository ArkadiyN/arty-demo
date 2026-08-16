# UFC 4-023-07 Pages 40–41 (Printed Pages 5-9 to 5-10)

## Vision-Verified Extraction

**Extraction method:** Rasterized to PNG via `pdftoppm`, then read directly from page image. No OCR or text-layer assumptions — equation and table structure read directly from rendered page.

______________________________________________________________________

## Equation 5-1. Wood Thickness to Prevent Projectile Perforation

$$T_w = 9837 \frac{v^{0.4113} w^{1.4897}}{\rho \left(\frac{\pi D^2}{4}\right)^{1.3596} H^{0.5414}}$$

**Where:**

- $T_w$ = thickness of wood necessary to prevent perforation (in)
- $v$ = projectile impact velocity (ft/s) (conservatively use muzzle velocity in appendix A)
- $w$ = projectile weight (lbs) (see appendix A)
- $D$ = projectile diameter (in²)
- $\rho$ = wood density (lbs/ft³) (see Table 5-5)
- $H$ = wood hardness (lbs) (see Table 5-5)

**Exponent verification:**

- **ρ exponent = 1.0** (no explicit superscript marker; appears in denominator)
- **H exponent = 0.5414** (explicit superscript)

______________________________________________________________________

## Table 5-5. Wood Properties

| Species        | Condition | Density (lbs./ft³) | Hardness (pounds) |
| -------------- | --------- | ------------------ | ----------------- |
| Pine           | Dry       | 23.5               | 38.7              |
| Pine           | Wet       | 30                 | 51.1              |
| Maple          | Dry       | 35                 | 76.9              |
| Maple          | Wet       | 40                 | 72                |
| Green Oak      | Dry       | 55                 | 88.1              |
| Green Oak      | Wet       | 55                 | 72.1              |
| Marine plywood | Dry       | 37                 | 68.7              |
| Marine plywood | Wet       | 37                 | 58.8              |
| Balsa          | Dry       | 6                  | 21                |
| Balsa          | Wet       | 6                  | 61.5              |
| Fir plywood    | Dry       | 30                 | 75                |
| Fir plywood    | Wet       | 30                 | 68.9              |
| Hickory        | Dry       | 50                 | 74.3              |
| Hickory        | Wet       | 55                 | 63.5              |

______________________________________________________________________

## Equation 5-2. Residual Velocity from Wood Target

$$v_r = v \left[1.0 - \left(\frac{t}{T_w}\right)^{0.5735}\right]$$

**Where:**

- $v_r$ = residual velocity (ft/s)
- $t$ = actual target thickness (in)
- $T_w$ = perforation-limit thickness (from Eq. 5-1)
