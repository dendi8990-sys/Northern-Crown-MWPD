from __future__ import annotations
import numpy as np
from scipy.stats import norm

VERSION = "ZSEP_v0.3-RC1_DEPLOYMENT_AFFINE_HYBRID"
MIN_NULL_POOL = 5000
ZSEP_CLIP = 5.0
PRIOR_STRENGTH = 5000.0
DEPLOYMENT_LOCAL_NULL_REPS = 20
HELDOUT_QA_NULL_REPS = 20
MIN_CALIBRATION_POINTS = 200

class AdaptiveNullReference:
    def __init__(self, size, M, min_pool=MIN_NULL_POOL):
        self.null_size = np.asarray(size, np.int32)
        self.null_M = np.asarray(M, float)
        self.min_pool = int(min_pool)
        if len(self.null_size) != len(self.null_M) or len(self.null_M) == 0:
            raise ValueError("invalid null reference arrays")
        self.by_n = {int(n): np.sort(self.null_M[self.null_size == n]) for n in np.unique(self.null_size)}
        self.nmin = min(self.by_n)
        self.nmax = max(self.by_n)
        self._cache = {}

    @classmethod
    def from_npz(cls, path, min_pool=MIN_NULL_POOL):
        z = np.load(path, allow_pickle=False)
        obj = cls(z["size"], z["M"], min_pool=min_pool)
        z.close()
        return obj

    def pool(self, n):
        n = int(n)
        if n in self._cache:
            return self._cache[n]
        d = 0
        while True:
            if n < self.nmin:
                lo, hi = self.nmin, min(self.nmax, self.nmin + d)
            elif n > self.nmax:
                lo, hi = max(self.nmin, self.nmax - d), self.nmax
            else:
                lo, hi = max(self.nmin, n - d), min(self.nmax, n + d)
            parts = [self.by_n[k] for k in range(lo, hi + 1) if k in self.by_n]
            count = sum(len(x) for x in parts)
            if count >= self.min_pool or (lo == self.nmin and hi == self.nmax):
                pool = np.sort(np.concatenate(parts))
                self._cache[n] = pool
                return pool
            d += 1

    def tail_p_and_pooln(self, M, n_members):
        M = np.asarray(M, float)
        n = np.asarray(n_members, int)
        p = np.empty(len(M), float)
        nn = np.empty(len(M), int)
        for nv in np.unique(n):
            idx = np.flatnonzero(n == nv)
            pool = self.pool(int(nv))
            pos = np.searchsorted(pool, M[idx], side="left")
            pp = (1.0 + (len(pool) - pos)) / (1.0 + len(pool))
            p[idx] = np.clip(pp, 1.0 / (len(pool) + 1.0), len(pool) / (len(pool) + 1.0))
            nn[idx] = len(pool)
        return p, nn

    def z_sep(self, M, n_members):
        p, _ = self.tail_p_and_pooln(M, n_members)
        return np.clip(norm.isf(p), -ZSEP_CLIP, ZSEP_CLIP)

def hybrid_zsep_raw(global_ref, local_ref, M, n_members, prior_strength=PRIOR_STRENGTH):
    """v0.2 hybrid score before the v0.3 target-local calibration layer."""
    pg, _ = global_ref.tail_p_and_pooln(M, n_members)
    pl, nl = local_ref.tail_p_and_pooln(M, n_members)
    w = nl / (nl + float(prior_strength))
    p = w * pl + (1.0 - w) * pg
    return np.clip(norm.isf(p), -ZSEP_CLIP, ZSEP_CLIP)

def fit_deployment_affine(global_ref, local_ref, deployment_reps, prior_strength=PRIOR_STRENGTH):
    """Fit location/scale using deployment nulls only; held-out nulls must never enter here."""
    chunks = []
    for size, M in deployment_reps:
        chunks.append(hybrid_zsep_raw(global_ref, local_ref, M, size, prior_strength=prior_strength))
    if not chunks:
        raise ValueError("deployment_reps is empty")
    pooled = np.concatenate(chunks)
    if len(pooled) < MIN_CALIBRATION_POINTS:
        raise ValueError(f"insufficient deployment calibration points: {len(pooled)} < {MIN_CALIBRATION_POINTS}")
    mu = float(np.mean(pooled))
    sigma = float(np.std(pooled, ddof=1))
    if not np.isfinite(mu) or not np.isfinite(sigma) or sigma <= 0:
        raise ValueError("invalid deployment affine calibration")
    return {"mu": mu, "sigma": sigma, "n": int(len(pooled))}

def calibrated_zsep(global_ref, local_ref, M, n_members, calibration, prior_strength=PRIOR_STRENGTH):
    raw = hybrid_zsep_raw(global_ref, local_ref, M, n_members, prior_strength=prior_strength)
    mu = float(calibration["mu"])
    sigma = float(calibration["sigma"])
    if not np.isfinite(mu) or not np.isfinite(sigma) or sigma <= 0:
        raise ValueError("invalid calibration")
    return np.clip((raw - mu) / sigma, -ZSEP_CLIP, ZSEP_CLIP)

def pooled_heldout_qa(z_reps):
    """Primary v0.3 QA: pool held-out candidates; per-replicate values are descriptive only."""
    reps = [np.asarray(x, float) for x in z_reps]
    if not reps or any(len(x) == 0 for x in reps):
        raise ValueError("empty held-out null replicate")
    z = np.concatenate(reps)
    med = float(np.median(z))
    sd = float(np.std(z, ddof=1))
    upper5 = float(np.mean(z >= 1.6448536269514722))
    passed = bool(abs(med) <= 0.15 and 0.9 <= sd <= 1.1 and 0.035 <= upper5 <= 0.065)
    return {"n": int(len(z)), "median_z": med, "sd_z": sd, "upper5": upper5, "PASS": passed}
