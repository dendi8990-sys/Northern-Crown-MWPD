from __future__ import annotations
import numpy as np
from scipy.spatial import cKDTree

VERSION = "T_env64_v0.1-RC1"
K_ENV = 64
EPS = 1e-15

def _circular_center_unit(points_unit: np.ndarray) -> np.ndarray:
    """Periodic circular mean for coordinates in [0,1)."""
    pts=np.asarray(points_unit,float)
    ang=2.0*np.pi*pts
    return (np.arctan2(np.mean(np.sin(ang),axis=0),
                       np.mean(np.cos(ang),axis=0))/(2.0*np.pi)) % 1.0

def score_candidates(candidates, ids, X_centered, k_env: int = K_ENV):
    """
    Compute the self-contained local environmental ridge-linearity score.

    Input contract
    --------------
    ids: stable object IDs, length N.
    X_centered: Nx3 periodic coordinates in [-0.5,+0.5).
    candidates: Crown candidate dictionaries containing member_IDs.

    For candidate c:
      1. Convert coordinates to U=(X_centered+0.5) mod 1.
      2. Compute periodic circular center from candidate members.
      3. Exclude the candidate's own member objects.
      4. Take the k_env nearest external tracers in the periodic box.
      5. Form minimum-image displacement covariance C=(D^T D)/k.
      6. Let lambda1>=lambda2>=lambda3 be eigenvalues of C.
      7. T_env64=(lambda1-lambda2)/(lambda1+lambda2+lambda3).

    Interpretation
    --------------
    T_env64 near 1: a locally one-dimensional external environment.
    T_env64 near 0: no dominant 1-D axis (isotropic or sheet-like).
    This score does NOT use an external filament skeleton, S_det, Z_R,
    Z_sep, lifespan, or a truth label.
    """
    if int(k_env) < 3:
        raise ValueError("k_env must be >=3")
    ids=np.asarray(ids)
    X=np.asarray(X_centered,float)
    if X.ndim!=2 or X.shape[1]!=3 or len(ids)!=len(X):
        raise ValueError("ids/X shape mismatch")
    if not np.isfinite(X).all():
        raise ValueError("non-finite coordinates")
    U=(X+0.5)%1.0
    tree=cKDTree(U,boxsize=1.0)
    id_to_index={str(v):i for i,v in enumerate(ids)}
    out=np.full(len(candidates),np.nan,dtype=float)
    for ci,c in enumerate(candidates):
        midx=[id_to_index[str(v)] for v in c.get("member_IDs",[])
              if str(v) in id_to_index]
        if not midx:
            continue
        pts=U[np.asarray(midx,dtype=int)]
        cen=_circular_center_unit(pts)
        member_set=set(midx)
        kk=min(len(U), int(k_env)+len(member_set)+8)
        _,idxs=tree.query(cen,k=kk,workers=1)
        idxs=np.atleast_1d(idxs)
        ext=[int(i) for i in idxs if int(i) not in member_set][:int(k_env)]
        if len(ext)<int(k_env):
            continue
        D=U[np.asarray(ext,dtype=int)]-cen
        D=D-np.round(D)
        C=(D.T@D)/float(len(ext))
        vals=np.linalg.eigvalsh(C)[::-1]
        den=max(float(vals.sum()),EPS)
        out[ci]=float((vals[0]-vals[1])/den)
    return out
