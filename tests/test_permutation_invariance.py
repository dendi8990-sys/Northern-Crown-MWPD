import numpy as np
from northern_crown import detect, candidates_to_records
from _fixture import catalogue

def test_input_permutation_invariance():
    ids,X=catalogue(); rng=np.random.default_rng(7); p=rng.permutation(len(ids))
    a=candidates_to_records(detect(ids,X)); b=candidates_to_records(detect(ids[p],X[p]))
    assert a==b
