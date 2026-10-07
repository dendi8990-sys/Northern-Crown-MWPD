# Manual official-server release acceptance

Status: engineering/reproducibility acceptance only. **This is not a new science campaign and cannot change the frozen scientific claims.**

## Completed live result

The exact v0.4.0 wheel passed the manual procedure on both official environments on 2026-10-06 UTC. Compact receipts are under `../evidence/live-acceptance/`.

- Abacus: 398,865,558 valid source rows → 165,412 canonical input objects → 11,790 candidates; exact expected membership; byte-identical repeat; PASS.
- TNG300-2 snapshot 99: 2,605,111 FoF groups → 25,126 canonical input objects → 2,045 candidates; exact expected membership; byte-identical repeat; PASS.

## What “manual, like a scientist” means

A researcher does **not** inspect the catalogue and hand-pick Northern Crown candidates. That would introduce selection bias. The human work is to predeclare the target and data cut, obtain the official data, record provenance and checksums, execute the frozen software, and transcribe the resulting measurements into a lab table. Northern Crown itself selects the candidate structures.

## Common operator sequence

1. Record date, server/source, simulation, snapshot/redshift, official file paths and software environment.
2. Record the selection rule before running Northern Crown.
3. Verify release science hashes with `northern-crown verify`.
4. Build the NPZ input from official fields only; save `ids` and `X`.
5. Record input row count and content/SHA-256 fingerprints.
6. Run `northern-crown detect input.npz -o candidates.json` with release-default variant D.
7. Record candidate count, membership fingerprint, output SHA-256, and resource receipt when available.
8. Repeat the same command once; output must be deterministic.
9. Compare with the frozen replay reference. Any mismatch is a release/integration finding; do not tune the science code.
10. Sign the row as PASS/FAIL with an explanation.

## Frozen replay references

Abacus: `AbacusSummit_base_c000_ph020`, z=0.500, fields `id` + `x_L2com`, ID-only SplitMix64 selection, expected N=165,412 and 11,790 candidates.

TNG: TNG300-2 snapshot 99, fields `GroupLenType` + `GroupPos`, keep `GroupLenType[:,1] >= 3951`, expected N=25,126 and 2,045 candidates.

Exact content and membership fingerprints are in `REFERENCE_REPLAY_TARGETS.json`.

## Acceptance rule

PASS requires official source identity, unchanged input construction rule, expected N, frozen hash PASS, variant D, expected candidate count, exact expected membership fingerprint, and byte-identical repeat. This replay does not add to or subtract from the existing v0.4-RC1 scientific evidence.

## Harness

The separately distributed V5 official-server acceptance harness incorporates only engineering portability fixes found during the successful manual V4 runs; the tested v0.4.0 wheel and frozen science bytes are unchanged.
