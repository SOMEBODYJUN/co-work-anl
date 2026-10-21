"""Independent literal Cartesian audit of the arbitrary-load decomposition.

Uses heterogeneous arities3,4 and hence both two- and three-level backgrounds.
It does not import any pricing or joint-transport implementation.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from random import Random
import json

def comp(n,k):
    if k==1:yield(n,);return
    for x in range(n+1):
        for tail in comp(n-x,k-1):yield(x,)+tail

def expand(h,k):return tuple(z for z,n in zip(product((0,1),repeat=k),h) for _ in range(n))
def signature(h,k,p):
    data=expand(h,k);return tuple(tuple(sorted(p+sum(z[:-1]) for z in data if z[0]==t)) for t in (0,1))
def own(h,k,p):return sum((F(z[-1],p+sum(z[:-1])+1) for z in expand(h,k)),F(0))
def targetpart(L,h,k,components):
    data=expand(h,k);D=sum((F(1,c+1) for group in L for c in group),F(0));B=sum(weight*sum(z[pos] for z in data) for pos,kind,weight in components if kind=='O')
    ans=-B*D
    for t in (0,1):
        inv=sorted(F(1,c+1) for c in L[t]);scores=sorted(sum(weight*(-1 if kind=='D' else 1)*z[pos] for pos,kind,weight in components) for z in data if z[0]==t)
        ans+=sum((a*b for a,b in zip(inv,scores)),F(0))
    return ans

def run():
    rng=Random(127319);ks=(3,4);q=2;cases=[];comparisons=0
    H=[list(comp(q,2**k)) for k in ks]
    for trial in range(8):
        pref=(rng.randrange(2),rng.randrange(2));localcoef=[[rng.randrange(-4,5) for _ in range(2**k)] for k in ks]
        local=[{h:sum(a*b for a,b in zip(h,c)) for h in hh} for hh,c in zip(H,localcoef)]
        sig=[{h:signature(h,k,p) for h in hh} for hh,k,p in zip(H,ks,pref)]
        actual=[{h:own(h,k,p) for h in hh} for hh,k,p in zip(H,ks,pref)]
        rows=[]
        for source,target in ((0,1),(1,0)):
            for _ in range(3):
                components=tuple((rng.randrange(1,ks[target]),rng.choice(('D','O')),rng.randrange(1,4)) for _ in range(2));weight=rng.randrange(1,4);a=sum(v*(1 if kind=='D' else q-1) for _,kind,v in components)
                rows.append((source,target,components,weight,a))
        for d in range(q+1):
            hh=[[h for h in H[f] if len(sig[f][h][1])==d] for f in (0,1)];best=None
            for ha,hb in product(*hh):
                hs=(ha,hb);v=F(local[0][ha]+local[1][hb])
                for s,t,c,w,a in rows:v+=w*(a*actual[s][hs[s]]+targetpart(sig[s][hs[s]],hs[t],ks[t],c))
                best=v if best is None else max(best,v);comparisons+=1
            fibers=[]
            for f in (0,1):
                fs={}
                for h in hh[f]:fs.setdefault(sig[f][h],[]).append(h)
                fibers.append(fs)
            decomposed=None
            for L0,L1 in product(*[list(fs) for fs in fibers]):
                L=(L0,L1);v=F(0)
                for f in (0,1):
                    vmax=None
                    for h in fibers[f][L[f]]:
                        vv=F(local[f][h])
                        for s,t,c,w,a in rows:
                            if s==f:vv+=w*a*actual[f][h]
                            if t==f:vv+=w*targetpart(L[s],h,ks[f],c)
                        vmax=vv if vmax is None else max(vmax,vv)
                    v+=vmax
                decomposed=v if decomposed is None else max(decomposed,v)
            assert best==decomposed,(trial,d,best,decomposed)
            cases.append({'trial':trial,'d':d,'fixed_backgrounds':pref,'cartesian_optimum':str(best),'decomposed_optimum':str(decomposed),'signature_counts':[len(fs) for fs in fibers]})
    report={'scope':'Exact finite audit of load-signature representation; not a welfare theorem','trials':8,'equality_cases':len(cases),'literal_histogram_tuple_comparisons':comparisons,'arities':ks,'q':q,'background_load_levels':5,'all_exact_equal':True,'cases':cases}
    Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='cases'},indent=2))
if __name__=='__main__':run()
