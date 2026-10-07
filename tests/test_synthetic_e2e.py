from northern_crown import detect
from _fixture import catalogue

def test_synthetic_detector_e2e():
    ids,X=catalogue(); out=detect(ids,X)
    assert len(out)>0
    assert {'ids','score','n','lifespan','spread_norm'} <= set(out[0])
