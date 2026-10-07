# Northern Crown v0.4-RC1 — Abacus Batch-6 V2 release QA
Date: 2026-09-29
Status: engineering QA PASS for release artifact construction.

## Why V1 was withdrawn before live use
Two concrete engineering defects were found during the requested re-audit:
1. `preflight.py` treated `effective_mem_available_mb()` as a scalar although the hardened memory helper returns `(effective, host, cgroup)`. This could raise a TypeError before science.
2. The batch wrapper treated topology worker return code 3 as an engineering crash. In this project rc=3 is a legitimate completed scientific `TOPOLOGY_FAIL` and must be recorded without aborting the preregistered six-target batch.

## V2 engineering-only corrections
- Correct cgroup-aware preflight memory unpacking and receipt.
- Accept topology rc=0 (PASS) and rc=3 (scientific FAIL) as completed topology executions; preserve the topology status in each target receipt.
- Automatic diagnostic ZIP on actual engineering failure.
- Root-cause failure propagation records inner failed stage and inner child return code, while also retaining the outer wrapper return code.
- Hash-validated whole-target resume using `TARGET_RECEIPT.json`.
- Existing complete Batch-6 artifact is preserved on accidental rerun.
- Synthetic 100% selection handles the uint64 threshold endpoint safely; live selection contract is unchanged.

## Full synthetic six-target E2E
A synthetic ASDF-compatible fixture supplied PH020-PH025 and used the same batch orchestrator and per-target pipeline.
Each target executed:
- preflight;
- 81/81 standard stages;
- 20 deployment calibration nulls;
- 20 held-out null QA realizations;
- Z_R v0.4;
- 20 thinning arms;
- noise/density stress;
- HDBSCAN baseline + five DROP20 arms;
- topology worker;
- per-target CRC package.

All six targets completed sequentially and the final `NORTHERN_CROWN_V04_ABACUS_BATCH6_COMPLETE.zip` was produced with CRC PASS. Synthetic scientific PASS/FAIL values are not validation evidence and were not used to alter science.

The synthetic topology worker returned rc=3 / `TOPOLOGY_FAIL` on all six artificial targets; V2 correctly recorded each result and continued through 6/6 instead of misclassifying it as an engineering crash.

## Resume test
After the completed batch, only the top-level batch receipt/final package was removed while the six per-target packages and receipts were retained. Restart produced 6/6 `TARGET-RESUME-SKIP` events after SHA validation and regenerated the final package without rerunning target science.

## Forced-failure diagnostic test
Engineering QA forced `B_BASELINE_A` to exit 97. Final batch state recorded:
- failed stage: `B_BASELINE_A`;
- root child return code: 97;
- wrapper return code: 1;
- exact error text;
- automatic `ENGINEERING_FAILURE_...zip` with CRC PASS and state/preflight/contract/resource/log evidence.

## Frozen scientific byte comparison
Byte-identical to the v0.4-RC1 method-freeze package:
- PB2 detector: `7a6457862230def5ea5279487882c8faeeee5e4adb42bf88c95f3db80fc5e206`
- Z_sep v0.4 provider source: `dc5d37c4b6eb38f139d646b78f016e050d04f6d7038c16e522ce4d072c9489a4`
- Z_R v0.4 source: `635575247a218fab690dbe05b5290ca05c4c3ba4f0668c9a3d90418353e5d0d2`
- global reference: `3b6f040b2c62742401b0862a062ea263896a6bb8f96d0946b8abc50c477be78a`
- T_env64: `00c31925b0736a6fd28e036f9bd2acdb7b3639de73194947d85aa864db4ff679`
- v0.4 method preregistration JSON: `87a8204099999d5a262042797ed97d7db582ebe60ff0f1ee505c97dbc107b436`

## Live boundary
Synthetic QA proves orchestration mechanics, not PH020-PH025 scientific outcomes or real-server availability. Live preflight still verifies the actual ASDF schema, dependency versions, memory and frozen hashes before science starts.
