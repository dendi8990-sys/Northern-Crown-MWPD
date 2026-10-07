from northern_crown import detect, candidates_to_records
from _fixture import catalogue

def test_release_default_is_validated_variant_d():
    ids, X = catalogue()
    assert candidates_to_records(detect(ids, X)) == candidates_to_records(detect(ids, X, variant='D'))

def test_numeric_member_ids_serialize_in_natural_order():
    rows = candidates_to_records([{'ids': {2, 10, 3}, 'score': 1.0}])
    assert rows[0]['member_IDs'] == [2, 3, 10]
