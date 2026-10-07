# Northern Crown MWPD v0.4.0

First public packaging release of the frozen Northern Crown v0.4-RC1 scientific payload.

## Validation

Formal promotion status: `V04_RC1_VALIDATED_ON_PREREGISTERED_ABACUS_BATCH6`.

- Preregistered Abacus Batch-6: 6/6 target PASS; no tuning between targets.
- Supplementary TNG Batch-6: 6/6 computational PASS.
- Combined computational ledger: 12/12 target blocks PASS, 12/12 held-out null QA PASS, 60/60 positive DROP20 seeds, 12/12 matched HDBSCAN gate PASS, 312/312 sufficient `T_env64` stress arms satisfying the frozen rule.

## Scope

This release supports the tested-scope claims for deterministic candidate extraction, v0.4 null portability, `Z_R` candidate-identity robustness, the matched HDBSCAN comparator endpoint, and `T_env64` local environmental ridge-linearity/anisotropy transfer.

It does not claim universal cosmic-web taxonomy, universal superiority over HDBSCAN/DisPerSE, direct filament truth, exact filament geometry recovery, or temporal material persistence.

## Preserved negative results

- `PERSIST01`: FAIL.
- `TRUTH03A`: FAIL 2/3; preregistered campaign gate required 3/3.

## Packaging

- BSD-3-Clause license.
- Python API and `northern-crown` CLI.
- Frozen-payload SHA-256 verification.
- Deterministic synthetic demo.
- Hash-validated resume.
- Tests and GitHub Actions CI.
- Compact immutable validation evidence; heavy Full Garage/raw datasets are not included in the working tree.

## Official-server acceptance

The exact release wheel passed manual live replay on both official server environments:

- AbacusSummit `base_c000_ph020`, z=0.500: 165,412 canonical input objects → 11,790 candidates, exact canonical membership fingerprint, byte-identical run repeat.
- TNG300-2 snapshot 99: 25,126 canonical input objects → 2,045 candidates, exact canonical membership fingerprint, byte-identical run repeat.

These are engineering/reproducibility acceptance replays of known historical targets, not new scientific validation.
