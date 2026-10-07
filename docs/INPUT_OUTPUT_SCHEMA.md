# Input / output schema

## Detector input

NPZ CLI input must contain:
- `ids`: one-dimensional length-N stable unique scalar/hashable IDs;
- `X`: finite numeric array `(N,3)`.

The frozen detector validates dimensionality, equal lengths, finite coordinates and ID uniqueness. Row order is canonicalized by stable ID.

The detector itself uses relative/local distances and does not attach physical units. Do not mix coordinate systems inside one catalogue.

## `T_env64` input

The frozen `T_env64` module expects `X_centered` periodic coordinates in `[-0.5,+0.5)` and stable IDs. It uses 64 nearest external non-member tracers and periodic minimum-image covariance.

## Candidate JSON output

The CLI emits schema `northern-crown-candidates-v1` with top-level method/release/variant/input count/candidate count and an array of candidate records. Frozen detector membership set `ids` is serialized as `member_IDs` for JSON.

Detector-level fields currently emitted by the frozen payload include `score`, `n`, `lifespan`, `boundary`, `certainty`, `support_eff`, `spread`, `spread_norm`, `global_scale`, and `Q`.

A sidecar `.receipt.json` contains input SHA-256, aggregate science-payload digest, output SHA-256, candidate count and completion status.
