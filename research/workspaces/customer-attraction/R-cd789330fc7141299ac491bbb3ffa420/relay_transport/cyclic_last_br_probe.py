from pathlib import Path
import itertools,json,numpy as np
from scipy.optimize import linprog
HERE=Path(__file__).resolve().parent

def rotation_orbits(k):
    full=(1<<k)-1;seen=set();out=[]
    for t in range(1,full+1):
        if t in seen:continue
        orb=[];v=t
        for _ in range(k):
            if v not in orb:orb.append(v)
            v=((v<<1)&full)|(v>>(k-1))
        seen.update(orb);out.append(orb)
    return out

def probe(k,r):
    masks=np.arange(1,1<<k);mem=np.array([[int(t>>a&1) for t in masks] for a in range(k)],float)
    orbs=rotation_orbits(k);summ=np.zeros((len(masks),len(orbs)))
    for j,orb in enumerate(orbs):summ[np.array(orb)-1,j]=1
    px=mem.mean(axis=0)
    sec=np.array([(px/(1+mem[list(q)].sum(axis=0)))@summ for q in itertools.combinations_with_replacement(range(k),r)])
    best=(-1,None);total=0
    for tail in itertools.product(range(1,k),repeat=r-1):
        # fix multiset of all but the last, preserving an arbitrary chosen terminal last action
        if tuple(sorted(tail[:-1]))!=tail[:-1]:continue
        total+=1;z=(0,*tail);load=mem[list(z)].sum(axis=0)
        root=mem[0]/np.maximum(load,1)@summ
        follows=np.array([mem[j]/np.maximum(load,1)@summ for j in tail])
        pre=mem[list(z[:-1])].sum(axis=0)
        last=mem[tail[-1]]/(1+pre)@summ
        br=np.array([last-mem[j]/(1+pre)@summ for j in range(k)])
        a=[np.r_[root,0],*[np.r_[-v,1] for v in follows],*[np.r_[-v,1] for v in sec],*[np.r_[-v,0] for v in br]]
        rhs=[1]+[0]*(len(a)-1)
        lp=linprog(np.r_[np.zeros(len(orbs)),-1],A_ub=a,b_ub=rhs,bounds=(0,None),method='highs')
        if lp.success and lp.x[-1]>best[0]+1e-8:
            best=(lp.x[-1],dict(k=k,r=r,tail=tail,t=lp.x[-1],orbits=orbs,weights=lp.x[:-1].tolist()))
            print('BEST',k,r,total,best[0],tail,flush=True)
            if best[0]>1+1e-7:break
    return dict(k=k,r=r,menus=total,best=best[0],witness=best[1])
if __name__=='__main__':
    out=[]
    for k,r in [(7,3),(8,3),(7,4)]:
        o=probe(k,r);out.append(o)
        if o['best']>1+1e-7:break
    (HERE/'cyclic_last_br_probe.json').write_text(json.dumps(out,indent=2)+'\n')
    print([(o['k'],o['r'],o['best'],o['menus']) for o in out])
