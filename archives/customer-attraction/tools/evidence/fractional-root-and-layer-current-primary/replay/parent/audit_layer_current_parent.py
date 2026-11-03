"""Independent role-cut audit; arbitrary policies, not SPE assertions."""
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
import json

def run(old,beta):
    m=4; letters='ab' if old else 'abcd'; covered={'a'} if old else {'a','c'}
    pol={h:'b' for n in range(m) for h in product(letters,repeat=n)}
    if old:
        pol.update({('a',):'a',('a','a'):'b',('b','a'):'a',('a','a','b'):'a',('b','a','a'):'b',('b','b','a'):'a'})
    else:
        for h in pol:
            if h and set(h)!={'b'}:
                pol[h]='a' if 'd' in h else letters[(sum((j+1)*letters.index(a) for j,a in enumerate(h))+len(h))%4]
    @lru_cache(None)
    def end(h):return h if len(h)==m else end(h+(pol[h],))
    def cv(w):return {j for j,a in enumerate(w) if a in covered}
    B=end(()); assert not cv(B)
    sources=[(0,'a',F(1))] if old else [(i,a,F(1,16)) for i in range(m) for a in letters]
    incoming=defaultdict(F); src=[]
    for i,a,p in sources:
        W=end(B[:i]+(a,)); C=cv(W); c=len(C); future={j for j in C if j>i}
        for j in future:incoming[W[:j]]+=p/c
        src.append((i,a,p,c,len(future)))
    initial=sum(incoming.values(),F()); rows=[]
    for k in range(m):
        for g in [g for g in list(incoming) if len(g)==k and incoming[g]]:
            h=incoming[g]; V=end(g); A=end(B[:k]+(pol[g],)); C=cv(V); E=cv(A)
            assert k in C and min(E)==k
            out=F()
            for j in E-{k}:
                z=h/len(E)*(F(1) if j not in C else beta)
                incoming[A[:j]]+=z;out+=z
            current=h-out;tail=h*len({j for j in C if j>=k});norm=len(E)*current
            assert 0<=norm<=tail
            rows.append((k,pol[g],current,norm,tail,len(C)*h))
    assert sum((z[2] for z in rows),F())==initial
    layers=[]
    for k in range(m):
        bound=sum((p*f/c for i,a,p,c,f in src if i<k and c),F())
        norm=sum((r[3] for r in rows if r[0]==k),F())
        tail=sum((r[4] for r in rows if r[0]==k),F())
        density=sum((r[5] for r in rows if r[0]==k),F())
        assert norm<=tail<=bound<=1
        layers.append({'k':k,'normalized':str(norm),'future_density':str(tail),'bound':str(bound),'old_density':str(density)})
    if old and beta==0:
        assert F(layers[3]['old_density'])==F(7,6) and F(layers[3]['normalized'])==F(5,12)
    return {'old_reentry':old,'common_fraction':str(beta),'layers':layers,
            'noncover_query_positive_future':sum(a not in covered and f>0 for i,a,p,c,f in src),
            'zero_cover_sources':sum(c==0 for i,a,p,c,f in src)}

out={'scope':'Two arbitrary policies; not SPE or HALF evidence.',
     'cases':[run(old,beta) for old in [True,False] for beta in [F(),F(1,2),F(1)]]}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'cases':len(out['cases']),'all_cut_bounds_passed':True,'general_noncover_sources_checked':True}))
