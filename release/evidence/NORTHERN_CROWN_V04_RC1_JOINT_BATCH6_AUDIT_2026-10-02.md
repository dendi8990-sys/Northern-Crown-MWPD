# Northern Crown MWPD — v0.4-RC1 Joint Batch-6 Audit

**Date:** 2026-10-02  
**Method:** `NORTHERN_CROWN_v0.4-RC1`  
**Previous status:** `METHOD_FROZEN_PENDING_UNSEEN_VALIDATION`  
**Audit decision:** `V04_RC1_VALIDATED_ON_PREREGISTERED_ABACUS_BATCH6`

## 1. Integrity and reconstruction

- Abacus reconstructed outer ZIP SHA-256: `6cd2da38db8c963f508c0de99b9ebbe73048c6a8213d98ad0725b9ad94488da8` — matches supplied split checksum record.
- TNG reconstructed outer ZIP SHA-256: `5cddeaf7dbe9741a84a54337b81e76437299d529a50dc4226ceb13111b99e7c4` — matches supplied split checksum record.
- Every uploaded split part matches its recorded SHA-256.
- Both outer ZIPs pass CRC/openability.
- All 12 nested target result ZIPs pass CRC/openability.
- All 12 nested target ZIP SHA-256 values match their respective `BATCH6_RECEIPT.json` records.

## 2. Frozen method and gate discipline

The embedded v0.4-RC1 preregistration keeps `PB2_V2E2_IDCANON`/`S_det` unchanged, uses 20 deployment nulls plus 20 separate held-out null tests per target, preserves the DROP20 designated and five-seed identity gates, the HDBSCAN matched comparator, and `T_env64` topology gates. The direct-filament claim remains explicitly outside this validation scope.

## 3. Abacus Batch-6 — promotion evidence

The Abacus protocol is explicitly `FROZEN_BEFORE_SCIENCE`. Historical `base_c000_ph000..ph019` and `hugebase_c000_ph000` were conservatively excluded. The six concrete targets were written before the first science worker; selection used only availability/path metadata; `science_output_inspected_for_selection=false`; no tuning occurred between targets.

| Target | N | Cand. | DROP20 ρ | p | 5-seed median ρ | Null QA | Crown J | HDBSCAN J | T_env64 |
|---|---:|---:|---:|---:|---:|---|---:|---:|---|
| AbacusSummit_base_c000_ph020 | 165,412 | 11,790 | 0.1579 | 2.847e-46 | 0.1585 | PASS | 0.8333 | 0.4545 | PASS |
| AbacusSummit_base_c000_ph021 | 164,350 | 11,771 | 0.1539 | 9.395e-44 | 0.1559 | PASS | 0.8333 | 0.4483 | PASS |
| AbacusSummit_base_c000_ph022 | 164,086 | 11,695 | 0.1611 | 2.007e-47 | 0.1571 | PASS | 0.8333 | 0.4500 | PASS |
| AbacusSummit_base_c000_ph023 | 165,445 | 11,841 | 0.1545 | 2.043e-44 | 0.1634 | PASS | 0.8333 | 0.4500 | PASS |
| AbacusSummit_base_c000_ph024 | 164,717 | 11,858 | 0.1648 | 2.020e-50 | 0.1648 | PASS | 0.8333 | 0.4444 | PASS |
| AbacusSummit_base_c001_ph000 | 160,310 | 11,381 | 0.1530 | 2.755e-42 | 0.1637 | PASS | 0.8333 | 0.4545 | PASS |

**Batch result:**
- target block PASS: **6/6**;
- exact determinism: **6/6**;
- designated identity gate: **6/6**;
- five-seed identity transfer: **6/6**, with **30/30 positive DROP20 seeds**;
- held-out null QA: **6/6**;
- Crown ≥ frozen HDBSCAN primary endpoint: **6/6**;
- `T_env64` topology: **6/6**, **156/156 sufficient stress arms** satisfying the frozen stress rule;
- designated DROP20 ρ range: **0.1530–0.1648**, median **0.1562**.

**Promotion decision:** the preregistered Abacus Batch-6 supplies the first valid unseen confirmation for v0.4-RC1. Project status is promoted to **`V04_RC1_VALIDATED_ON_PREREGISTERED_ABACUS_BATCH6`** for the stated candidate-identity/null-portability/topology-transfer scope.

This does **not** establish universal simulation-family validity, universal superiority over HDBSCAN/DisPerSE, or direct filament/node/wall/void truth.

## 4. TNG Batch-6 — supplementary revalidation

| Target | N | Cand. | DROP20 ρ | p | 5-seed median ρ | Null QA | Crown J | HDBSCAN J | T_env64 |
|---|---:|---:|---:|---:|---:|---|---:|---:|---|
| L205n1250TNG | 25,126 | 2,045 | 0.1862 | 2.467e-13 | 0.2066 | PASS | 0.7778 | 0.6000 | PASS |
| L205n1250TNG_DM | 25,697 | 2,088 | 0.1778 | 1.595e-12 | 0.1879 | PASS | 0.7778 | 0.6000 | PASS |
| L205n2500TNG | 158,558 | 12,857 | 0.1880 | 5.888e-77 | 0.1807 | PASS | 0.7778 | 0.6000 | PASS |
| L205n2500TNG_DM | 161,528 | 12,944 | 0.1722 | 5.592e-65 | 0.1867 | PASS | 0.7778 | 0.6000 | PASS |
| L205n625TNG | 3,446 | 295 | 0.1931 | 0.004302 | 0.1525 | PASS | 0.8333 | 0.5714 | PASS |
| L205n625TNG_DM | 3,575 | 305 | 0.2070 | 0.001713 | 0.1881 | PASS | 0.8333 | 0.5917 | PASS |

The TNG computation itself is strong: **6/6 block PASS**, 6/6 determinism, 6/6 identity, 6/6 held-out null QA, **30/30 positive DROP20 seeds**, 6/6 HDBSCAN comparator PASS, and **156/156** sufficient topology stress arms.

However, it is **not used as the formal unseen promotion evidence**. Its outer package contains the generic `BATCH6_UNSEEN_PROTOCOL_TEMPLATE` with status `TARGETS_NOT_YET_FROZEN`, rather than a concrete pre-science frozen six-target record. In addition, the simulations belong to the already-used TNG evidence family. Therefore this block is retained as **supplementary seen/overlapping cross-resolution and hydro/DMO revalidation**.

The two smallest TNG targets (`L205n625TNG`, `L205n625TNG_DM`) have N=3,446 and N=3,575; both satisfy the designated identity, held-out null, comparator and topology gates. This is useful evidence that the old TNG16 low-count failure is not a generic failure across every small TNG catalogue, but it does not define a universal low-N threshold.

## 5. Combined computational ledger

Across the two completed six-target runs:
- target blocks: **12/12 PASS**;
- held-out null QA: **12/12 PASS**;
- matched HDBSCAN benchmark gate: **12/12 PASS**;
- topology gate: **12/12 PASS**;
- DROP20 positive seeds: **60/60**;
- topology sufficient stress arms: **312/312**.

Only the **Abacus six** carry the formal unseen-promotion role in this audit.

## 6. Historical statuses preserved

The promotion does not rewrite prior evidence. Historical v2 remains `PARTIAL`; the v0.3 campaign remains `FAIL`; TNG16 v0.3 remains `FAIL`; PH019 v0.3 remains `PASS`; TNG17_BIG_R2 remains a `PASS_DIAGNOSTIC`. The current promotion is a new v0.4-RC1 validation record, not a retroactive repair of older campaigns.

## 7. Claim boundary and next version rule

Validated here: deterministic candidate extraction, v0.4 null portability under the tested targets, `Z_R` candidate-identity robustness under the frozen perturbation design, the matched HDBSCAN comparator endpoint, and `T_env64` local environmental ridge-linearity/anisotropy transfer.

Not validated here: direct physical filament truth, a universal cosmic-web taxonomy, or universal superiority over HDBSCAN/DisPerSE. Direct physical topology remains a separate `TRUTH03` program.

Any scientific change to detector mathematics, gates, calibration, seed policy, comparator settings, or topology definition after this record must open a new development branch/version and receive new unseen validation.
