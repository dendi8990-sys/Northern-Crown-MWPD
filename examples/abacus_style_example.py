"""Input-shape example only; no Abacus dataset is redistributed here."""
import numpy as np
from northern_crown import detect

# Replace with your own stable halo IDs and consistently normalized Nx3 coordinates.
ids=np.arange(1000,dtype=np.int64)
X=np.random.default_rng(1).uniform(-0.5,0.5,size=(1000,3))
candidates=detect(ids,X)
print(len(candidates))
