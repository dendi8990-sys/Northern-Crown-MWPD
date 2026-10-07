# Changelog

## 0.4.0
### Final release-candidate official-server acceptance (2026-10-06/07)
- Exact v0.4.0 wheel passed live manual engineering/reproducibility acceptance on official Abacus and TNG server environments.
- Abacus replay: 398,865,558 → 165,412 → 11,790; exact candidate membership and byte-identical repeat PASS.
- TNG replay: 2,605,111 → 25,126 → 2,045; exact candidate membership and byte-identical repeat PASS.
- Acceptance harness V5 removes host assumptions found during the manual procedure: generated `.pyc` files are excluded from manifests, GNU `/usr/bin/time` is not required, pip user configuration is neutralized for the local install, and shard/chunk progress is explicit.
- No frozen science bytes changed.

### Release-candidate QA correction (2026-10-06)
- Corrected the public API/CLI default from legacy variant A to validated variant D after direct replay against frozen TNG/Abacus validation inputs.
- Corrected numeric `member_IDs` serialization ordering to natural numeric order.
- No frozen science bytes were changed.
 — public packaging candidate

- Packages the byte-preserved v0.4-RC1 science payload behind a clean Python API/CLI.
- Records the formal promotion `V04_RC1_VALIDATED_ON_PREREGISTERED_ABACUS_BATCH6`.
- Preserves TNG Batch-6 as supplementary revalidation, not unseen promotion evidence.
- Adds frozen-payload SHA verification, deterministic synthetic demo, hash-validated resume, tests and CI.
- Uses BSD-3-Clause.
- Preserves negative research records: `PERSIST01` FAIL and `TRUTH03A` FAIL 2/3.

Historical states remain unchanged: historical v2 `PARTIAL`; v0.3 campaign `FAIL`; TNG17_BIG_R2 `PASS_DIAGNOSTIC`.
