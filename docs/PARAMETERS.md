# Parameters

## Scientific frozen values

Examples of frozen detector constants include `K_LOCAL=8`, `GRAPH_K=24`, `MIN_MEMBERS=5`, `CORE_THRESHOLD=0.60`, relative scales `[0.70,0.85,1.00,1.20,1.40]`, tracking Jaccard `0.50`, duplicate Jaccard `0.70`, plus the frozen filtration arrays embedded in the detector source.

Z_sep v0.3-RC1 freezes prior strength 5000, minimum null pool 5000, 20 deployment calibration replicates, 20 held-out QA null replicates and output clipping at ±5. `Z_R` freezes weights 1.0 / 0.75 / 0.75. `T_env64` freezes `K_ENV=64`.

These are science parameters. Editing them creates a scientifically different method and is outside the v0.4.0 release contract.

## Engineering/runtime settings

CLI input/output paths, `--resume`, and the output directory for the synthetic demo are engineering settings and do not modify the frozen method.
