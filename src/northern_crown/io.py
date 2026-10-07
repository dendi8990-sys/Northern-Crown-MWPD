from __future__ import annotations
from pathlib import Path
import hashlib, json
import numpy as np

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''): h.update(chunk)
    return h.hexdigest()

def load_npz_catalogue(path):
    """Load an NPZ containing arrays `ids` and `X` (shape N x 3)."""
    with np.load(path, allow_pickle=False) as z:
        missing=[k for k in ('ids','X') if k not in z.files]
        if missing: raise ValueError(f"missing NPZ fields: {', '.join(missing)}")
        ids=np.asarray(z['ids']); X=np.asarray(z['X'],float)
    if X.ndim!=2 or X.shape[1]!=3: raise ValueError("X must have shape (N,3)")
    if len(ids)!=len(X): raise ValueError("ids and X must have equal lengths")
    return ids,X

def write_json_atomic(path, obj):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix(path.suffix+'.tmp')
    tmp.write_text(json.dumps(obj,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding='utf-8')
    tmp.replace(path)
