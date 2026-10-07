from __future__ import annotations
from pathlib import Path
import hashlib
import numpy as np
from .frozen import PB2_V2E2_IDCANON_detector_impl as _frozen

EXPECTED_FROZEN_SHA256 = {
    "PB2_V2E2_IDCANON_detector_impl.py": "7a6457862230def5ea5279487882c8faeeee5e4adb42bf88c95f3db80fc5e206",
    "ZR_GLOBAL_REFERENCE_V01.npz": "3b6f040b2c62742401b0862a062ea263896a6bb8f96d0946b8abc50c477be78a",
    "topology_env_v0_1_rc1.py": "00c31925b0736a6fd28e036f9bd2acdb7b3639de73194947d85aa864db4ff679",
    "zr_v0_3_rc1.py": "635575247a218fab690dbe05b5290ca05c4c3ba4f0668c9a3d90418353e5d0d2",
    "zsep_v0_3_rc1.py": "dc5d37c4b6eb38f139d646b78f016e050d04f6d7038c16e522ce4d072c9489a4",
}

def detect(ids, coordinates, variant: str = "D"):
    """Run the byte-preserved PB2_V2E2_IDCANON detector on an Nx3 catalogue.

    IDs must be unique scalar/hashable values. Coordinates must be finite Nx3
    values in one internally consistent coordinate system. The detector itself
    does not assign physical filament/node/wall/void truth labels.
    """
    return _frozen.detect(ids, coordinates, variant=variant)

def candidates_to_records(candidates):
    """Convert frozen detector candidate dictionaries into JSON-safe records."""
    out=[]
    for c in candidates:
        r={}
        for k,v in c.items():
            if k == "ids":
                vals=[_scalar(x) for x in v]
                try:
                    r["member_IDs"] = sorted(vals)
                except (TypeError, ValueError):
                    r["member_IDs"] = sorted(vals, key=lambda x: (type(x).__name__, repr(x)))
            else:
                r[k] = _scalar(v)
        out.append(r)
    return out

def _scalar(v):
    if isinstance(v, np.generic): return v.item()
    return v

def frozen_payload_hashes():
    base=Path(__file__).resolve().parent/'frozen'
    result={}
    for name in EXPECTED_FROZEN_SHA256:
        h=hashlib.sha256((base/name).read_bytes()).hexdigest()
        result[name]=h
    return result

def verify_frozen_payload():
    actual=frozen_payload_hashes()
    mismatches={k:{"expected":v,"actual":actual.get(k)} for k,v in EXPECTED_FROZEN_SHA256.items() if actual.get(k)!=v}
    return {"PASS": not mismatches, "files": actual, "mismatches": mismatches}
