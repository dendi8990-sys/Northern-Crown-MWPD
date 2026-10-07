# Northern Crown MWPD v0.4.0 — live official-server acceptance

Date: 2026-10-06 UTC  
Status: **ABACUS PASS + TNG PASS**

This record is an **engineering/reproducibility acceptance replay** of known historical targets. It is not a new scientific validation campaign and does not change the frozen Northern Crown v0.4-RC1 claim boundary.

## Exact release artifact under test

The bundled/public wheel used on both servers was byte-identical:

`northern_crown_mwpd-0.4.0-py3-none-any.whl`  
SHA-256: `20f293177371de245b7fc2fa8f0707097e8e4f8a4609fb49aa212da73b27aac8`

Frozen payload verification passed on both server environments before detector execution.

## Abacus live replay

Official target: `AbacusSummit_base_c000_ph020`, `z=0.500`, `halos/z0.500/halo_info`.

Observed live input reconstruction:

- source shards: 34;
- raw valid rows: 398,865,558;
- frozen selected input: 165,412;
- input content fingerprint: `4fafe32866a372580f327747ef157264e6934bd7d4318a0a14683b13d8d0b0c5`;
- input NPZ SHA-256: `0403b8b7ce66698ed93422f76ba7f413c658b07dfcf97d5ac4675d1773b96a81`.

Detector replay:

- run 1 candidates: 11,790;
- run 2 candidates: 11,790;
- membership fingerprint, both runs: `bb4116f6a0c52596aaef98d37ee142502a237941b42644c8b834de31f0095de3`;
- output SHA-256, both runs: `1c07f2e2511c66dd0eea572083a01b0a31cdfe683f2c23141927f19fc711888a`;
- byte-identical repeat: PASS;
- final acceptance checker: PASS.

## TNG live replay

Official target: TNG300-2 (`L205n1250TNG`), snapshot 99, `groups_099`.

Observed live input reconstruction:

- source chunks: 100;
- raw FoF groups: 2,605,111;
- BoxSize: 205000;
- redshift: approximately zero;
- frozen selected input: 25,126;
- input content fingerprint: `a431b040afc6bcd79c2e014dac229d08f0dd7914e8ac649057dd4d2925af6517`;
- input NPZ SHA-256: `0d388906a9da0d1372b34236d559931c009d9dbcf32c003a9c61938fc98d96db`.

Detector replay:

- run 1 candidates: 2,045;
- run 2 candidates: 2,045;
- membership fingerprint, both runs: `06ab8c8223a7a46e9a75a7a5f2264d3e67e38fcc58bb007636cf1af7f21142a5`;
- output SHA-256, both runs: `994fa436376aa7fe37ee3a54cb75096e6518178cd7f67cf0ac7398f382cf6dbf`;
- byte-identical repeat: PASS;
- final acceptance checker: PASS.

## Portability findings discovered by the manual procedure

The manual runs exposed engineering assumptions without changing the frozen science:

1. generated Python cache files must never be part of the immutable acceptance manifest;
2. GNU `/usr/bin/time` is not guaranteed on managed notebook servers;
3. host pip configuration may force `--user` and conflict with a local `--target` install;
4. the CLI verification subcommand is `verify`;
5. progress should be visible per shard/chunk for long input reconstruction.

These findings are addressed by official-server acceptance harness V5. The v0.4.0 wheel and all v0.4-RC1 frozen science bytes remain unchanged.

## Full evidence archive hashes

The compact public record here excludes raw input NPZ files, candidate catalogues, debug bundles, hostname/account identifiers, and official raw simulation data. Hashes of the full captured acceptance archives are stored in `FULL_EVIDENCE_ASSETS_SHA256.txt`.
