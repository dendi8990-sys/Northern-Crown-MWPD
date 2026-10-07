# Reproducibility

## Frozen bytes

Run:

```bash
northern-crown verify
```

The command recalculates SHA-256 for each frozen science file and compares it with the v0.4-RC1 method-freeze record.

## Determinism and row-order contract

The frozen detector canonicalizes input by stable object ID before graph construction. Tests cover identical-input determinism and input-permutation invariance.

## Synthetic reproduction

```bash
northern-crown demo --dir demo_output
```

The fixture uses a fixed NumPy seed and requires no TNG or Abacus dataset. Synthetic results are engineering/reproducibility evidence only, not cosmological validation evidence.

## Formal validation evidence

The repository ships compact immutable audit records and target summaries under `release/evidence/`. Heavy raw TNG/Abacus datasets and the ~5 GB Full Garage provenance archive are intentionally not part of the Git working tree.

## Resume contract

`--resume` skips a completed output only when the current input SHA-256, frozen science-payload digest, and existing output SHA-256 all match the receipt.

## Live official-server acceptance

On 2026-10-06 UTC, the exact v0.4.0 wheel (SHA-256 `20f293177371de245b7fc2fa8f0707097e8e4f8a4609fb49aa212da73b27aac8`) passed manual official-server replay on both Abacus and TNG. Exact input-content fingerprints, candidate counts, membership fingerprints, and byte-identical repeat outputs matched the frozen engineering references.

This replay uses known historical targets and therefore does not add scientific validation targets. See `release/evidence/live-acceptance/LIVE_ACCEPTANCE_SUMMARY.md`.
