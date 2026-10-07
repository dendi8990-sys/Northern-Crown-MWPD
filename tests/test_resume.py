from pathlib import Path
import numpy as np
from northern_crown.cli import run_detection
from _fixture import catalogue

def test_hash_validated_resume(tmp_path, capsys):
    d=tmp_path/'path with spaces'; d.mkdir(); inp=d/'in file.npz'; out=d/'out file.json'
    ids,X=catalogue(); np.savez_compressed(inp,ids=ids,X=X)
    assert run_detection(inp,out)==0
    assert run_detection(inp,out,resume=True)==0
    assert 'RESUME_SKIP' in capsys.readouterr().out
