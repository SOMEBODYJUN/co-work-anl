"""Replay every root-copy row on full ordered SPE witnesses.

This checks row semantics and scaling on selected boundary inputs. It is not
an exhaustive game search, a universal welfare bound, or a proof of HALF(5).
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
import sys,json
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'customer_attraction/__init__.py').exists())
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(HERE)]
from customer_attraction import Instance,ExactSPESolver
from actual_root_copies import Universe,ROOTS,PATHS,SPECS

def check(themes,row_model=Universe,include_root=False):
    themes=tuple(frozenset(s) for s in themes);N=set().union(*themes)
    inst=Instance.from_topic_sets(themes,5);sol=ExactSPESolver(inst)
    cert=sol.worst_certificate();sigma=cert.actions
    def finish(h):
        while len(h)<5:h=h+(sigma[h],)
        return h
    def payoff(z,i):return sum((F(1,sum(x in themes[t] for t in z)) for x in themes[z[i]]),F(0))
    ic=0
    for depth in range(5):
        for h in product(range(len(themes)),repeat=depth):
            v=payoff(finish(h),depth)
            for t in range(len(themes)):
                assert v>=payoff(finish(h+(t,)),depth);ic+=1
    actual=finish(());A,B,C,D,E=actual
    second=finish((A,E));third=finish((A,B,E))
    label_topics=dict(zip('ABCDEUVWXY',(*actual,*second[2:],*third[3:])))
    opt=max(combinations_with_replacement(range(len(themes)),5),key=lambda ts:len(set().union(*(themes[t] for t in ts))))
    ab=[finish((A,B,t)) for t in opt];ae=[finish((A,E,t)) for t in opt];sb=[finish((A,t)) for t in opt]
    prefixes=[actual[:3],second[:3],third[:3]]
    lastmenus=[[finish(pref+(t,))[-1] for t in opt] for pref in prefixes]
    copies={}
    for s,(pre,forced) in SPECS.items():
        hh=tuple(label_topics[x] for x in pre)+(label_topics[forced],)
        copies[s]=finish(hh)[len(hh):]
    U=object.__new__(row_model);U.overlap=1
    rootpaths=[finish((t,)) for t in opt] if include_root else None
    sums={};atom_count=0
    for x in sorted(N):
        def bit(t):return int(x in themes[t])
        hs=[]
        for paths,positions in [(ab,(3,4)),(ae,(3,4)),(sb,(2,3,4))]:
            hist=[0]*(1<<(1+len(positions)))
            for t,z in zip(opt,paths):
                bits=[bit(t)]+[bit(z[i]) for i in positions];index=0
                for b in bits:index=2*index+b
                hist[index]+=1
            hs.append(hist)
        atom={'bits':''.join(str(bit(label_topics[s])) for s in 'ABCDEUVWXY'),'AB_hist':hs[0],'AE_hist':hs[1],'second_hist':hs[2],
              'menus_lh':[(sum(bit(t) for t in mm),sum(bit(t)*bit(z) for t,z in zip(opt,mm))) for mm in lastmenus],
              'copies':{s:[bit(t) for t in copies[s]] for s in ROOTS}}
        if include_root:
            hh=[0]*32
            for z in rootpaths:
                index=0
                for t in z:index=2*index+bit(t)
                hh[index]+=1
            atom['root_hist']=hh
        rows=U.atom_rows(atom)
        for n,v in rows.items():sums[n]=sums.get(n,F(0))+v
        atom_count+=1
    assert all(v>=0 for v in sums.values()),[(n,str(v)) for n,v in sums.items() if v<0][:10]
    return {'themes':[sorted(t) for t in themes],'actual':actual,'full_IC':ic,'unit_atoms':atom_count,'rows':len(sums),'minimum_slack':str(min(sums.values(),default=F(0)))}

if __name__=='__main__':
    cases=[check(ts) for ts in [[set()],[set(),{0},{0,1},{1,2}],[set(range(5)),{5},{6},{7},{8}],[{0,1},{1,2},{0,2,3},{3,4},{0,2,4}]]]
    result={'status':'passed','scope':__doc__,'cases':cases}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'passed','cases':len(cases),'full_IC':sum(c['full_IC'] for c in cases),'row_semantics':'all nonnegative'},indent=2))
