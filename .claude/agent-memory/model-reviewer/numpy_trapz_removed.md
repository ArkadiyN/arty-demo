---
name: numpy-trapz-removed
description: This project's numpy has no np.trapz — use np.trapezoid in verification scripts
metadata:
  type: reference
---

`np.trapz` raises AttributeError in this project's uv-managed numpy; use
`np.trapezoid` for reference quadratures in ad-hoc verification scripts.
