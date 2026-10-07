from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
from .detector import detect, candidates_to_records, verify_frozen_payload, frozen_payload_hashes
from .io import load_npz_catalogue, sha256_file, write_json_atomic

def _payload_digest():
    import hashlib
    h=hashlib.sha256()
    for k,v in sorted(frozen_payload_hashes().items()): h.update((k+":"+v+"\n").encode())
    return h.hexdigest()

def run_detection(input_path, output_path, variant='D', resume=False):
    inp=Path(input_path); out=Path(output_path); receipt=out.with_suffix(out.suffix+'.receipt.json')
    integrity=verify_frozen_payload()
    if not integrity['PASS']: raise RuntimeError(f"frozen payload hash mismatch: {integrity['mismatches']}")
    input_sha=sha256_file(inp); payload_sha=_payload_digest()
    if resume and out.exists() and receipt.exists():
        old=json.loads(receipt.read_text(encoding='utf-8'))
        if old.get('input_sha256')==input_sha and old.get('science_payload_sha256')==payload_sha and old.get('output_sha256')==sha256_file(out):
            print('RESUME_SKIP: hashes validated')
            return 0
    ids,X=load_npz_catalogue(inp)
    candidates=candidates_to_records(detect(ids,X,variant=variant))
    result={"schema_version":"northern-crown-candidates-v1","method":"Northern Crown v0.4-RC1","release":"0.4.0","variant":variant,"input_count":int(len(ids)),"candidate_count":len(candidates),"candidates":candidates}
    write_json_atomic(out,result)
    rec={"status":"COMPLETE","input_sha256":input_sha,"science_payload_sha256":payload_sha,"output_sha256":sha256_file(out),"candidate_count":len(candidates),"variant":variant}
    write_json_atomic(receipt,rec)
    print(f"COMPLETE: {len(candidates)} candidates -> {out}")
    return 0

def make_demo(path):
    rng=np.random.default_rng(42)
    ids=np.arange(400,dtype=np.int64)
    X=np.vstack([rng.normal([-.2,0,0],.05,(130,3)),rng.normal([.2,0,0],.05,(130,3)),rng.normal([0,.25,0],.05,(140,3))])
    np.savez_compressed(path,ids=ids,X=X)

def main(argv=None):
    p=argparse.ArgumentParser(prog='northern-crown')
    sub=p.add_subparsers(dest='cmd',required=True)
    d=sub.add_parser('detect',help='run the frozen detector on an NPZ catalogue')
    d.add_argument('input'); d.add_argument('-o','--output',required=True); d.add_argument('--variant',default='D',choices=['A','D']); d.add_argument('--resume',action='store_true')
    demo=sub.add_parser('demo',help='create and run a deterministic synthetic example')
    demo.add_argument('--dir',default='northern_crown_demo')
    v=sub.add_parser('verify',help='verify frozen science payload SHA-256 values')
    a=p.parse_args(argv)
    if a.cmd=='verify':
        r=verify_frozen_payload(); print(json.dumps(r,indent=2,sort_keys=True)); return 0 if r['PASS'] else 2
    if a.cmd=='demo':
        dr=Path(a.dir); dr.mkdir(parents=True,exist_ok=True); inp=dr/'synthetic_input.npz'; out=dr/'candidates.json'; make_demo(inp); return run_detection(inp,out)
    return run_detection(a.input,a.output,a.variant,a.resume)

if __name__=='__main__': raise SystemExit(main())
