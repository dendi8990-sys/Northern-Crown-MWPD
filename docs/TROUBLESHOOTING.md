# Troubleshooting

## Frozen payload mismatch

Run `northern-crown verify`. A mismatch means the release science bytes have been modified or corrupted; do not treat that installation as canonical v0.4.0.

## NPZ field error

The CLI requires `ids` and `X`. `X` must be finite and shape `(N,3)`; IDs must be unique.

## Resume does not skip

`--resume` intentionally reruns unless input SHA-256, science-payload digest and output SHA-256 all match the existing receipt.

## Large catalogues

The detector uses spatial trees and sparse graph operations and can require substantial memory. Test on a representative subset/environment before a large production run. Historical batch runners contained environment-specific memory guards; the compact public CLI does not silently install dependencies or alter the science payload.

## Paths with spaces

They are supported by the CLI; quote paths in your shell as usual.

## Official-server acceptance harness portability

The separate V5 acceptance harness is designed for managed notebook/HPC environments: it excludes generated Python cache files from immutable manifests, ignores host/user pip configuration during its isolated local wheel install, does not require GNU `/usr/bin/time`, records resources with a Python standard-library wrapper, and creates a compact debug ZIP on the first failing stage.
