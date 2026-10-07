import numpy as np, pytest
from northern_crown import detect

def test_bad_shape():
    with pytest.raises(ValueError): detect(np.arange(4),np.zeros((4,2)))
def test_duplicate_ids():
    with pytest.raises(ValueError): detect(np.array([1,1,2]),np.zeros((3,3)))
def test_nonfinite():
    X=np.zeros((3,3)); X[0,0]=np.nan
    with pytest.raises(ValueError): detect(np.arange(3),X)
