from __future__ import annotations
import numpy as np
from scipy.spatial import cKDTree
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

K_LOCAL=8; GRAPH_K=24; MIN_MEMBERS=5; CORE_THRESHOLD=.60
REL_SCALES=np.array([.70,.85,1.00,1.20,1.40])
FILTRATION_V11=np.array([.82,.72,.62,.52,.42,.32])
FILTRATION_A=np.array([.82,.77,.72,.67,.62,.57,.52,.47,.42,.37,.32])
TRACK_JACCARD=.50; DUPLICATE_JACCARD=.70

def jac(a,b):
    # Engineering-only exact Jaccard: avoid constructing the union set.
    inter=len(a&b)
    den=len(a)+len(b)-inter
    return inter/den if den else 0.

def jac_can_beat(a,b,best):
    # Exact pruning: J(A,B) cannot exceed min(|A|,|B|)/max(|A|,|B|).
    la=len(a); lb=len(b)
    if la==0 or lb==0:
        return -1.0
    if min(la,lb)/max(la,lb) <= best:
        return -1.0
    inter=len(a&b)
    den=la+lb-inter
    return inter/den if den else 0.0

def jac_gt(a,b,threshold):
    # Exact threshold predicate with a size-ratio upper bound.
    la=len(a); lb=len(b)
    if la==0 or lb==0:
        return False
    if min(la,lb)/max(la,lb) <= threshold:
        return False
    inter=len(a&b)
    return (inter/(la+lb-inter)) > threshold

def _graph(ids,X,anisotropic=False):
    ids=np.asarray(ids); X=np.asarray(X,float); n=len(X)
    tree=cKDTree(X)
    kq=min(GRAPH_K+2,n)
    dprobe,iprobe=tree.query(X,k=kq,workers=-1)
    if dprobe.ndim==1:
        dprobe=dprobe[:,None]; iprobe=iprobe[:,None]

    # Canonical local scale remains neighbours 4..8.
    hi=min(K_LOCAL,dprobe.shape[1]-1); lo=min(4,hi)
    ell=np.maximum(np.median(dprobe[:,lo:hi+1],axis=1),1e-6)

    # Exact-distance ties at the GRAPH_K boundary make "the first 24 neighbours"
    # mathematically non-unique and cKDTree may choose a different subset after row
    # permutation. In the generic continuous case there is no boundary tie and we
    # preserve the original vectorized path exactly. If a tie exists, include every
    # neighbour at the kth distance.
    basek=min(GRAPH_K,n-1)
    boundary_tie=np.zeros(n,dtype=bool)
    if n>GRAPH_K+1 and dprobe.shape[1]>GRAPH_K+1:
        dk=dprobe[:,GRAPH_K]
        dnext=dprobe[:,GRAPH_K+1]
        boundary_tie=np.isclose(dk,dnext,rtol=0.0,atol=1e-12*np.maximum(1.0,np.abs(dk)))

    if not np.any(boundary_tie):
        dists=dprobe[:,:min(GRAPH_K+1,dprobe.shape[1])]
        inds=iprobe[:,:min(GRAPH_K+1,iprobe.shape[1])]
        src=np.repeat(np.arange(n,dtype=np.int64),dists.shape[1]-1)
        dst=inds[:,1:].reshape(-1).astype(np.int64)
        dd=dists[:,1:].reshape(-1).astype(float)
        neigh=[inds[i,1:] for i in range(n)]
    else:
        srcs=[];dsts=[];dds=[];neigh=[]
        for i in range(n):
            if boundary_tie[i]:
                rk=float(dprobe[i,GRAPH_K])
                tol=1e-12*max(1.0,abs(rk))
                js=np.asarray(tree.query_ball_point(X[i],rk+tol),dtype=np.int64)
                js=js[js!=i]
                ds=np.linalg.norm(X[js]-X[i],axis=1)
                order=np.argsort(ds,kind='mergesort')
                js=js[order];ds=ds[order]
            else:
                lim=min(GRAPH_K+1,dprobe.shape[1])
                js=iprobe[i,1:lim].astype(np.int64)
                ds=dprobe[i,1:lim].astype(float)
            neigh.append(js)
            srcs.append(np.full(len(js),i,dtype=np.int64));dsts.append(js);dds.append(ds)
        src=np.concatenate(srcs) if srcs else np.empty(0,dtype=np.int64)
        dst=np.concatenate(dsts) if dsts else np.empty(0,dtype=np.int64)
        dd=np.concatenate(dds) if dds else np.empty(0,float)

    a=np.minimum(src,dst); b=np.maximum(src,dst); key=a*np.int64(n)+b
    order=np.argsort(key,kind='mergesort'); key=key[order]; a=a[order]; b=b[order]; dd=dd[order]
    starts=np.r_[0,1+np.flatnonzero(key[1:]!=key[:-1])]
    au=a[starts]; bu=b[starts]; mind=np.minimum.reduceat(dd,starts)
    u=mind/np.maximum(np.sqrt(ell[au]*ell[bu]),1e-12)

    if anisotropic:
        shape=np.empty((n,3,3),float); anis_ratio=np.ones(n,float); eye=np.eye(3)
        for i in range(n):
            nb=np.asarray(neigh[i],dtype=np.int64)
            D=X[nb]-X[i]
            C=(D.T@D)/max(len(D),1)
            tr=np.trace(C)/3.0
            shape[i]=C/max(tr,1e-12) if tr>0 else eye
            ev=np.linalg.eigvalsh(C)
            anis_ratio[i]=ev[-1]/max(ev[0],1e-12)
        delta=X[bu]-X[au]
        dhat=delta/np.maximum(np.linalg.norm(delta,axis=1)[:,None],1e-12)
        fa=np.einsum('ni,nij,nj->n',dhat,shape[au],dhat)
        fb=np.einsum('ni,nij,nj->n',dhat,shape[bu],dhat)
        directional=np.sqrt(np.maximum(fa,1e-6)*np.maximum(fb,1e-6))
        if anisotropic == 'gated':
            active=(anis_ratio[au] >= 5.0) & (anis_ratio[bu] >= 5.0)
            directional=np.where(active,directional,1.0)
        elif anisotropic == 'blend':
            lo=np.log(3.0); hi=np.log(15.0)
            ai=np.clip((np.log(np.maximum(anis_ratio,1.0))-lo)/(hi-lo),0.0,1.0)
            ae=np.sqrt(ai[au]*ai[bu])
            directional=np.exp(ae*np.log(np.maximum(directional,1e-6)))
        u=u/np.sqrt(np.maximum(directional,1e-6))
    geom=np.exp(-(u*u)); persist=(u[:,None]<=REL_SCALES[None,:]).mean(axis=1); omega=geom*persist
    keep=omega>0
    return au[keep],bu[keep],omega[keep],ell

def _detect_base(ids,X,variant='A'):
    ids=np.asarray(ids); X=np.asarray(X,float); n=len(X)
    if n<MIN_MEMBERS:return []
    if variant=='A': filt=FILTRATION_A; step=.05; anis=False
    elif variant=='B': filt=FILTRATION_V11; step=.10; anis=True
    elif variant=='C': filt=FILTRATION_V11; step=.10; anis='gated'
    elif variant=='D0': filt=FILTRATION_V11; step=.10; anis='blend'
    elif variant=='I': filt=FILTRATION_V11; step=.10; anis=False
    else: raise ValueError(variant)
    au,bu,omega,ell=_graph(ids,X,anisotropic=anis)
    snapshots=[]
    for tau in filt:
        sel=omega>=tau
        if np.any(sel):
            rr=np.r_[au[sel],bu[sel]]; cc=np.r_[bu[sel],au[sel]]
            A=csr_matrix((np.ones(len(rr),dtype=np.uint8),(rr,cc)),shape=(n,n)); _,lab=connected_components(A,directed=False)
        else: lab=np.arange(n)
        sizes=np.bincount(lab); comps=[]
        for label in np.where(sizes>=MIN_MEMBERS)[0]:
            idx=np.where(lab==label)[0]; pts=X[idx]; center=pts.mean(axis=0)
            comps.append({'idx':set(map(int,idx)),'center':center,'n':len(idx),'spread':float(np.mean(np.linalg.norm(pts-center,axis=1)))})
        snapshots.append((float(tau),comps))
    tracks=[]
    for tau,comps in snapshots:
        used=set()
        for tr in tracks:
            bj=-1;br=0.
            for j,c in enumerate(comps):
                if j in used:continue
                r=jac_can_beat(tr['last'],c['idx'],br)
                if r>br:br=r;bj=j
            if bj>=0 and br>=TRACK_JACCARD:
                c=comps[bj];tr['levels'].append((tau,c));tr['jaccards'].append(br);tr['last']=c['idx'];used.add(bj)
        for j,c in enumerate(comps):
            if j not in used:tracks.append({'levels':[(tau,c)],'jaccards':[],'last':c['idx']})
    candidates=[]
    for tr in tracks:
        if len(tr['levels'])<2:continue
        taus=[z[0] for z in tr['levels']]; comps=[z[1] for z in tr['levels']]; jacs=np.asarray(tr['jaccards'])
        counts=np.zeros(n)
        for c in comps:counts[list(c['idx'])]+=1
        probs=counts/len(comps); hard=np.where(probs>=CORE_THRESHOLD)[0]
        if len(hard)<MIN_MEMBERS:hard=np.argsort(probs)[::-1][:MIN_MEMBERS]
        pts=X[hard]; weights=np.maximum(probs[hard],1e-3); center=np.average(pts,axis=0,weights=weights)
        spread=float(np.average(np.linalg.norm(pts-center,axis=1),weights=weights))
        lifespan=float(max(taus)-min(taus)+step)
        boundary=float(np.mean(jacs))*np.exp(-float(np.var(jacs))) if len(jacs) else 0.
        active=probs>0; ambiguity=float(np.mean(4*probs[active]*(1-probs[active]))) if np.any(active) else 1.
        certainty=float(np.mean(probs[hard]))*np.exp(-ambiguity); support=float(np.sum(probs))
        # PB2-001: dimensionless compactness using the catalogue-wide canonical local-spacing scale.
        # This preserves the intended absolute-vs-background compactness comparison while making
        # S_det invariant to a uniform change of coordinate units.
        global_scale=float(np.median(ell)) if len(ell) else 1.0
        spread_norm=spread/max(global_scale,1e-12)
        Q=np.sqrt(max(support,1e-9))/(1+spread_norm)
        candidates.append({'ids':set(ids[hard]),'score':float(lifespan*boundary*certainty*Q),'n':len(hard),'lifespan':lifespan,'boundary':boundary,'certainty':certainty,'support_eff':support,'spread':spread,'spread_norm':spread_norm,'global_scale':global_scale,'Q':float(Q)})
    candidates.sort(key=lambda c:c['score'],reverse=True); kept=[]
    for c in candidates:
        if not any(jac_gt(c['ids'],p['ids'],DUPLICATE_JACCARD) for p in kept):kept.append(c)
    return kept


def _local_ell_anis(X):
    X=np.asarray(X,float); n=len(X)
    tree=cKDTree(X); dists,inds=tree.query(X,k=min(GRAPH_K+1,n),workers=-1)
    hi=min(K_LOCAL,dists.shape[1]-1); lo=min(4,hi)
    ell=np.maximum(np.median(dists[:,lo:hi+1],axis=1),1e-6)
    ratio=np.ones(n,float)
    for i in range(n):
        nb=inds[i,1:]
        D=X[nb]-X[i]
        C=(D.T@D)/max(len(D),1)
        ev=np.linalg.eigvalsh(C)
        ratio[i]=ev[-1]/max(ev[0],1e-12)
    return ell,ratio

def _detect_D(ids,X):
    """
    v1.2-D PREDECLARED development candidate.

    Main channel:
      continuous anisotropy mixture D0, alpha=0 for local PCA ratio<=3,
      alpha=1 for ratio>=15, log-linear between.

    Hierarchy guard:
      add an isotropic-channel candidate only if:
      n>=8,
      candidate median local PCA ratio <=4,
      candidate median local ell <=0.70 * catalogue-wide median ell,
      and it is not a Jaccard>0.70 duplicate of an existing D0 candidate.
    """
    ids=np.asarray(ids); X=np.asarray(X,float)
    main=_detect_base(ids,X,variant='D0')
    iso=_detect_base(ids,X,variant='I')
    ell,ratio=_local_ell_anis(X)
    id_to_idx={v:i for i,v in enumerate(ids)}
    global_ell=float(np.median(ell)) if len(ell) else 1.0
    guard=[]
    for c in iso:
        idx=np.array([id_to_idx[v] for v in c['ids'] if v in id_to_idx],dtype=int)
        if len(idx)<8: continue
        if float(np.median(ratio[idx])) > 4.0: continue
        if float(np.median(ell[idx])) > 0.70*global_ell: continue
        guard.append(c)
    out=list(main)
    for c in guard:
        if not any(jac_gt(c['ids'],q['ids'],DUPLICATE_JACCARD) for q in out):
            cc=dict(c); cc['hierarchy_guard']=True
            out.append(cc)
    out.sort(key=lambda c:c['score'],reverse=True)
    return out

def _canonical_id_order(ids):
    # v2 deterministic input contract: row order is semantically irrelevant.
    # Canonicalize by stable object ID before any floating reductions / graph ties.
    ids=np.asarray(ids)
    try:
        return np.argsort(ids,kind='mergesort')
    except (TypeError, ValueError):
        return np.asarray(sorted(range(len(ids)),key=lambda i:(type(ids[i]).__name__,repr(ids[i]))),dtype=np.int64)

def detect(ids,X,variant='A'):
    ids=np.asarray(ids)
    X=np.asarray(X,float)
    if X.ndim!=2 or X.shape[1]!=3:
        raise ValueError("X must have shape (N, 3)")
    if len(ids)!=len(X):
        raise ValueError("ids and X must have the same length")
    if not np.all(np.isfinite(X)):
        raise ValueError("X contains NaN or infinite coordinates")
    try:
        if len(set(ids.tolist()))!=len(ids):
            raise ValueError("ids must be unique")
    except TypeError as e:
        raise ValueError("ids must be scalar hashable values") from e
    order=_canonical_id_order(ids)
    ids=ids[order]; X=X[order]
    if variant=='D':
        return _detect_D(ids,X)
    return _detect_base(ids,X,variant=variant)
