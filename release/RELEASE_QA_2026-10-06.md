# Northern Crown MWPD v0.4.0 — release-candidate QA

Date: 2026-10-06
Status: **LOCAL QA PASS; ABACUS LIVE PASS; TNG LIVE PASS**

## Frozen science integrity

All five frozen v0.4-RC1 payload files in `src/northern_crown/frozen/` match the canonical method-freeze SHA-256 values:

- PB2 detector: `7a6457862230def5ea5279487882c8faeeee5e4adb42bf88c95f3db80fc5e206`
- global reference: `3b6f040b2c62742401b0862a062ea263896a6bb8f96d0946b8abc50c477be78a`
- T_env64: `00c31925b0736a6fd28e036f9bd2acdb7b3639de73194947d85aa864db4ff679`
- Z_R: `635575247a218fab690dbe05b5290ca05c4c3ba4f0668c9a3d90418353e5d0d2`
- Z_sep: `dc5d37c4b6eb38f139d646b78f016e050d04f6d7038c16e522ce4d072c9489a4`

## Release-candidate correction found by replay

The first packaging draft exposed legacy detector variant `A` as the API/CLI default even though the frozen v0.4-RC1 validation runners executed detector variant `D`. A direct replay on the historical TNG300-2 validation input detected the mismatch (legacy A produced 2,422 candidates instead of the historical 2,045). The public default was therefore corrected to **variant D**. This is a packaging/API correction only; no frozen science file changed.

Numeric `member_IDs` serialization was also corrected to natural numeric order. This changes presentation only, not candidate membership.

## Local QA executed after correction

- Python module compile: PASS.
- Test suite: **11/11 PASS**.
- identical-input determinism: PASS.
- input-permutation invariance: PASS.
- bad shape / duplicate ID / non-finite input failure paths: PASS.
- frozen Z_sep/Z_R calibration smoke test: PASS.
- hash-validated resume: PASS, including paths containing spaces.
- frozen payload verifier: PASS.
- deterministic synthetic CLI E2E with validated default variant D: PASS; fixture produced 32 candidates.
- historical TNG300-2 / `L205n1250TNG` snapshot-99 input replay: **PASS**, N=25,126, candidate count=2,045, candidate membership exactly matches historical baseline; numerical frozen fields match to <=7.2e-15 absolute difference.
- historical AbacusSummit `base_c000_ph020`, z=0.500 input replay: **PASS**, N=165,412, candidate count=11,790, candidate membership exactly matches historical baseline; numerical frozen fields match to <=3.6e-15 absolute difference.

## Official-server acceptance

The exact public wheel SHA-256 `20f293177371de245b7fc2fa8f0707097e8e4f8a4609fb49aa212da73b27aac8` passed both manual live official-server replays. These are engineering/reproducibility acceptance tests on known historical targets, not new scientific evidence.

- **Abacus PASS:** `AbacusSummit_base_c000_ph020`, z=0.500; 34 source shards; 398,865,558 valid rows; frozen input N=165,412; run1=run2=11,790 candidates; exact expected membership fingerprint; run outputs byte-identical.
- **TNG PASS:** TNG300-2 (`L205n1250TNG`), snapshot 99; 100 source chunks; 2,605,111 FoF groups; frozen input N=25,126; run1=run2=2,045 candidates; exact expected membership fingerprint; run outputs byte-identical.

Compact public receipts are preserved under `release/evidence/live-acceptance/`. The full captured evidence archive SHA-256 values are recorded without publishing raw official datasets.

The manual procedure also found packaging portability assumptions (`.pyc` manifest inclusion in an earlier harness, missing GNU `/usr/bin/time` on Flatiron Binder, and pip `--user` configuration on TNG). Acceptance harness V5 corrects those engineering issues without changing the v0.4.0 wheel or frozen v0.4-RC1 science bytes.

## Research-history integration

- PERSIST01 remains frozen FAIL and is excluded from core claims.
- TRUTH03A remains frozen campaign FAIL 2/3 under its preregistered 3/3 gate.
- supplied TRUTH03A complete archive SHA-256: `a0194c77aa743ef20216cc9353cd3f13dab39ac9580c9bb55b042b8045ee5e50`.

## Publication metadata

- Author / Project Lead / Lead Researcher: **Vlad**.
- Public-facing language: **English**.
- License: **BSD-3-Clause**.
- ChatGPT (OpenAI) is acknowledged as an AI research/software-engineering assistant, not listed as a human author.
- Final repository URL and optional DOI/Zenodo metadata remain to be filled after publication.
