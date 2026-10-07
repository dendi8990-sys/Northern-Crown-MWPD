from __future__ import annotations
import numpy as np
from scipy.stats import norm, rankdata

VERSION = "Z_R_v0.3-RC1"
W_LIFESPAN = 0.75
W_COMPACT = 0.75

def normal_score(values, higher=True):
    values = np.asarray(values, float)
    r = rankdata(values, method="average")
    u = (r - 0.5) / len(values)
    z = norm.ppf(u)
    return z if higher else -z

def score_from_zsep(zsep, lifespan, radius_local):
    zsep = np.asarray(zsep, float)
    lifespan = np.asarray(lifespan, float)
    radius_local = np.asarray(radius_local, float)
    if not (len(zsep) == len(lifespan) == len(radius_local)):
        raise ValueError("equal lengths required")
    if len(zsep) == 0:
        return np.empty(0, float)
    lz = normal_score(lifespan, True)
    cz = normal_score(radius_local, False)
    raw = (zsep + W_LIFESPAN * lz + W_COMPACT * cz) / np.sqrt(1.0 + W_LIFESPAN**2 + W_COMPACT**2)
    return normal_score(raw, True)
