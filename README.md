# Northern Crown MWPD v0.4.0

Northern Crown MWPD is a multiscale persistent spatial-structure detector for 3-D catalogues. This public release packages the **byte-preserved Northern Crown v0.4-RC1 scientific payload** behind a small Python API and CLI.

## Validation status

The frozen v0.4-RC1 method is validated on the preregistered Abacus Batch-6: **6/6 target PASS**, with no tuning between targets. A separate TNG Batch-6 completed **6/6 computational PASS** and is retained as supplementary seen/overlapping revalidation. Across both completed batches the computational ledger is 12/12 target blocks PASS, 12/12 held-out null QA PASS, 60/60 positive DROP20 seeds, 12/12 matched HDBSCAN gate PASS, and 312/312 sufficient `T_env64` stress arms satisfying the frozen rule.

This scope supports deterministic candidate extraction, tested v0.4 null portability, `Z_R` candidate-identity robustness, the matched HDBSCAN comparator endpoint, and `T_env64` local environmental ridge-linearity/anisotropy transfer. It **does not** establish universal cosmic-web taxonomy, universal superiority over HDBSCAN or DisPerSE, exact filament geometry, or temporal material persistence.

See [docs/VALIDATION.md](docs/VALIDATION.md) and [docs/KNOWN_LIMITATIONS.md](docs/KNOWN_LIMITATIONS.md).

## Official-server release acceptance

The exact public v0.4.0 wheel was manually replayed on the official Abacus and TNG server environments and passed both engineering/reproducibility acceptance runs:

- AbacusSummit `base_c000_ph020`, z=0.500: 398,865,558 valid source rows → 165,412 frozen input objects → **11,790** candidates; run 1/run 2 byte-identical and exact canonical membership fingerprint reproduced.
- TNG300-2, snapshot 99: 2,605,111 FoF groups → 25,126 frozen input objects → **2,045** candidates; run 1/run 2 byte-identical and exact canonical membership fingerprint reproduced.

This is a release-integration/reproducibility replay of known historical targets, **not** new scientific validation. Compact receipts are under `release/evidence/live-acceptance/`.

## Install

```bash
python -m pip install .
```

Requirements: Python >=3.10, NumPy, SciPy.

## Quick start: one command

```bash
northern-crown demo --dir demo_output
```

This creates a deterministic synthetic 3-D catalogue, runs the frozen detector, and writes `candidates.json` plus a hash receipt.

For your own NPZ catalogue, provide arrays `ids` and `X` (`X.shape == (N,3)`):

```bash
northern-crown detect catalogue.npz -o candidates.json
# release default is validated detector variant D
```

To resume/skip an already completed run only after input/output/science-payload hash validation:

```bash
northern-crown detect catalogue.npz -o candidates.json --resume
```

Verify the frozen payload:

```bash
northern-crown verify
```

## Python API

```python
from northern_crown import detect, candidates_to_records
candidates = detect(ids, X)
records = candidates_to_records(candidates)
```

The frozen detector output includes candidate membership and detector-level fields such as `score`, `n`, `lifespan`, `boundary`, `certainty`, `support_eff`, `spread`, `spread_norm`, `global_scale`, and `Q`.

## Input contract

- `ids`: length-N unique scalar/hashable stable object IDs.
- `X`: finite numeric array of shape `(N,3)` in one internally consistent coordinate system.
- Row order is semantically irrelevant: the frozen detector canonicalizes by stable ID.
- The public detector API does not infer physical units or cosmological truth labels.
- `T_env64` has a stricter periodic convention documented in [docs/INPUT_OUTPUT_SCHEMA.md](docs/INPUT_OUTPUT_SCHEMA.md).

## Frozen science

The scientific core is copied byte-for-byte from `NORTHERN_CROWN_V04_RC1_METHOD_FREEZE_2026-09-29`. Exact hashes are in [release/FROZEN_SCIENCE_PAYLOAD.md](release/FROZEN_SCIENCE_PAYLOAD.md).

A scientific change to detector mathematics, gates, calibration, seed policy, comparator settings, or topology definition is **not** a v0.4.0 packaging change; it opens a new development version and requires new unseen validation.

## Research/negative results

Negative research branches are preserved, not hidden. In particular:

- `PERSIST01`: frozen FAIL; temporal material persistence is not a core release claim.
- `TRUTH03A`: completed direct DisPerSE correspondence campaign, **FAIL 2/3** under its preregistered 3/3 campaign gate. It does not establish direct filament truth and does not block the core detector release.

See `research/negative-results/`.

## Authorship and AI assistance

**Project Lead / Lead Researcher:** Vlad.

Research software engineering, calculations, QA, documentation, and release packaging were developed with assistance from **ChatGPT (OpenAI)**. Scientific decisions, interpretation, release approval, and authorship responsibility remain with Vlad. See [ACKNOWLEDGEMENTS.md](ACKNOWLEDGEMENTS.md).

## License

BSD-3-Clause. See [LICENSE](LICENSE).


## Public documentation language

The public repository, command-line help, release notes, reproducibility instructions, and official-server acceptance materials are maintained in **English**. Historical internal archives may contain other languages, but they are not part of the public working tree.
