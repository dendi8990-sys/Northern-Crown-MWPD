import numpy as np

def catalogue():
    rng=np.random.default_rng(42)
    ids=np.arange(400,dtype=np.int64)
    X=np.vstack([rng.normal([-.2,0,0],.05,(130,3)),rng.normal([.2,0,0],.05,(130,3)),rng.normal([0,.25,0],.05,(140,3))])
    return ids,X
