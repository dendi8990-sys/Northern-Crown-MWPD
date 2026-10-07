from pathlib import Path
import numpy as np
from northern_crown import detect, candidates_to_records

rng=np.random.default_rng(42)
ids=np.arange(400,dtype=np.int64)
X=np.vstack([
    rng.normal([-.2,0,0],.05,(130,3)),
    rng.normal([ .2,0,0],.05,(130,3)),
    rng.normal([0,.25,0],.05,(140,3)),
])
candidates=candidates_to_records(detect(ids,X))
print(f"input={len(ids)} candidates={len(candidates)}")
print(candidates[0] if candidates else "no candidates")
