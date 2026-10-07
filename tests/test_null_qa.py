import numpy as np
from northern_crown.frozen import zsep_v0_3_rc1 as z3
from northern_crown.frozen import zr_v0_3_rc1 as r3

def test_v04_calibration_modules_smoke():
    rng=np.random.default_rng(1); size=np.repeat(np.arange(5,10),100); M=rng.normal(size=len(size))
    g=z3.AdaptiveNullReference(size,M,min_pool=50); l=z3.AdaptiveNullReference(size,M+0.1,min_pool=50)
    cal=z3.fit_deployment_affine(g,l,[(size,M+0.1),(size,M+0.1)])
    z=z3.calibrated_zsep(g,l,M,size,cal); assert np.isfinite(z).all()
    q=z3.pooled_heldout_qa([rng.normal(size=5000),rng.normal(size=5000)])
    assert set(q)=={'n','median_z','sd_z','upper5','PASS'}
    r=r3.score_from_zsep(z,rng.random(len(z)),rng.random(len(z))); assert np.isfinite(r).all()
