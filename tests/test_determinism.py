from northern_crown import detect, candidates_to_records
from _fixture import catalogue

def test_exact_repeated_result():
    ids,X=catalogue()
    assert candidates_to_records(detect(ids,X)) == candidates_to_records(detect(ids,X))
