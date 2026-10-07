# Method

Public release `v0.4.0` packages the frozen `Northern Crown v0.4-RC1` method without changing its scientific bytes.

## Frozen architecture

- Detector: `PB2_V2E2_IDCANON`; detection/ranking axis `S_det` unchanged from v0.3. The public API/CLI default is **variant D**, matching the detector variant used by the frozen v0.4-RC1 validation runners.
- Separation calibration: `ZSEP_v0.3-RC1_DEPLOYMENT_AFFINE_HYBRID`.
- Identity robustness: `Z_R_v0.3-RC1`, weights `1.0 : 0.75 : 0.75` for calibrated Z_sep, lifespan normal-score, compactness normal-score.
- Environment/topology: `T_env64_v0.1-RC1`.

The v0.4 scientific change was a deployment-affine target-local calibration layer for Z_sep. It retains the global+target-local hybrid null reference and fits `mu` and sample `sigma` using deployment nulls only, then applies `clip((Zraw-mu)/sigma,-5,5)`. Held-out nulls are forbidden from this fit.

## Frozen validation protocol highlights

Per unseen target, the preregistered method used 20 deployment calibration nulls plus 20 separate held-out null tests. Identity gates, five-seed transfer, stress arms, matched HDBSCAN comparator settings and `T_env64` gates were frozen before unseen science.

`Z_R` is candidate identity robustness, not physical truth. `T_env64` is local environmental ridge-linearity/anisotropy transfer, not direct filament truth.

The exact preregistration is preserved under `release/evidence/`.
