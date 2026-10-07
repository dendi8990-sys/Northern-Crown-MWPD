from northern_crown import verify_frozen_payload

def test_frozen_payload_hashes():
    r=verify_frozen_payload()
    assert r['PASS'], r['mismatches']
