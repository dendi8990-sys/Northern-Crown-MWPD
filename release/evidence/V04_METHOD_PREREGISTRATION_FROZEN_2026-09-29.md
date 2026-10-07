# Northern Crown v0.4-RC1 — method preregistration freeze — 2026-09-29

Status: **METHOD_FROZEN_PENDING_UNSEEN_VALIDATION**.

This freezes the v0.4 scientific method before the first new six-target batch. It does **not** promote v0.4 to a validated release. Historical v2 `PARTIAL` and v0.3 `FAIL` remain unchanged.

## Frozen architecture
- Detector: `PB2_V2E2_IDCANON` — byte-identical to v0.3.
- Detection/ranking: `S_det` — unchanged.
- Separation calibration: `ZSEP_v0.3-RC1_DEPLOYMENT_AFFINE_HYBRID`.
- Identity robustness: `Z_R_v0.3-RC1`; weights remain `1.0 : 0.75 : 0.75` for calibrated Z_sep, lifespan normal-score and compactness normal-score.
- Topology/environment: `T_env64_v0.1-RC1` — byte-identical and unchanged.

## The v0.4 change
The v0.2 hybrid null reference is retained (global + target-local, prior strength 5000). The new layer fits **only on deployment nulls**: pool the deployment hybrid Z_sep values, compute their mean `mu` and sample SD `sigma`, then use `clip((Zraw-mu)/sigma, -5, 5)` for that target. Held-out nulls may never be used to fit `mu` or `sigma`.

This is a calibration change, not a detector change. It was motivated by the TNG16 low-count null-centering drift. TNG16, PH019 and TNG17 are therefore **seen development evidence** for v0.4 and cannot validate it.

## Null protocol per unseen target
- 20 deployment radial-null replicates for calibration.
- 20 separate held-out radial-null replicates for the actual null QA.
- The user's requested **20 null tests per target are the 20 held-out tests**; the deployment 20 are calibration data, not held-out tests.
- Primary QA pools all held-out candidate scores across the 20 held-out reps. Per-rep diagnostics are retained but are secondary.
- PASS: `|pooled median| <= 0.15`, `0.9 <= pooled SD <= 1.1`, and `0.035 <= pooled upper-5% fraction <= 0.065`.

## Identity gates — unchanged
Designated DROP20 seed: partial Spearman rho >= 0.075 and two-sided p < 0.05, controlling for S_det, n_members and radius_local. Five-seed transfer: median DROP20 rho >= 0.075 and at least 4/5 positive. There is **no low-count exemption**. A low-N target that lacks significance is not silently promoted.

## Stress / comparator / topology
The 5×(DROP10/20/30/40) thinning matrix, positional noise 0.05/0.10/0.20 local-8NN sigma, density keep 0.90/0.80/0.60, and HDBSCAN fair-comparator settings remain unchanged. `T_env64` gates remain DROP20 median rho >= 0.20, >=4 positive seeds, every sufficient stress arm rho >= 0, and max median |delta| <= 0.10.

## Claim boundary
`Z_R` is candidate identity robustness, not physical truth. `T_env64` is local environmental ridge-linearity/anisotropy transfer, not direct filament truth. A physical filament claim requires a separate preregistered TRUTH03 program.

## Freeze rule
Once any unseen Batch-6 science output is inspected, no method/gate/seed/calibration/comparator/target-selection change is allowed for this RC. A scientific change opens a new development version.
