"""Exact, solver-free reconstruction and replay of all B mode certificates.
All rows are derived in B-all-orbits-proof.md; no floating point is used here.
"""
from fractions import Fraction as F
from itertools import product,permutations,combinations_with_replacement
from pathlib import Path
import json
BASE=Path(__file__).parent
PAIRS=list((a,y) for a,y in product(range(4),repeat=2) if a!=y)
TYPES=[(b,v) for b in range(7) for v in product((0,1),repeat=5) if b<6 or any(v)]
COLS=len(TYPES)+1

def build(pattern):
    def has(label,b,v):
        return int(b==label) if isinstance(label,int) else v[0] if label[0]=='E' else v[1+label[1]]
    def row(fn):return [F(fn(b,v)) for b,v in TYPES]+[F()]
    E=[row(lambda b,v:int(b==j)) for j in range(6)]
    atomsE=[row(lambda b,v:v[0]*int(b==j)) for j in range(4)]
    A=[row(lambda b,v:v[k]) for k in range(5)];rhs=[F(1)]*5
    names=['extra-cap-'+str(k) for k in range(5)]
    for j,index in enumerate(pattern):
        a,y=PAIRS[index];aa=('F',a);yy=('F',y)
        def base(b,v):return v[0]+int(4<=b<6)+int(b==j)
        def util(label,other):
            return row(lambda b,v:F(has(label,b,v),base(b,v)+has(label,b,v)+has(other,b,v)) if has(label,b,v) else 0)
        ua=util(aa,yy);uy=util(yy,aa)
        w=row(lambda b,v:F(1,base(b,v)+has(aa,b,v)+has(yy,b,v)) if b==j else 0)
        w[-1]=-1
        A.append(w);rhs.append(F());names.append(f'{j}:force')
        A.extend([[-x for x in ua],[-x for x in uy]]);rhs.extend([-F(7,12)]*2);names.extend([f'{j}:u5-floor',f'{j}:u6-floor'])
        labels=list(range(4))+[('E',0)]+[('F',k) for k in range(4)]
        for label in labels:
            query=row(lambda b,v:F(has(label,b,v),base(b,v)+has(aa,b,v)+1))
            A.append([x-y for x,y in zip(query,uy)]);rhs.append(F());names.append(f'{j}:last-query:{label}')
        for label in labels:
            query=row(lambda b,v:F(has(label,b,v),base(b,v)+2))
            A.append([x-y for x,y in zip(query,ua)]);rhs.append(F());names.append(f'{j}:penult-H:{label}')
        for k in range(4):
            if k==j:continue
            rr=[-ua[c]-atomsE[k][c]/2-sum((atomsE[l][c] for l in range(4) if l!=j and l!=k),F())/4 for c in range(COLS)]
            A.append(rr);rhs.append(F(-1));names.append(f'{j}:penult-deficit:{k}')
        for k,l in product(range(4),repeat=2):
            T=('F',k);Q=('F',l)
            rr=row(lambda b,v:F(has(T,b,v),base(b,v)+1)+F(has(Q,b,v),base(b,v)+has(T,b,v)+1))
            A.append([x-y for x,y in zip(rr,ua)]);rhs.append(F(1));names.append(f'{j}:TQ:{k}:{l}')
    assert len(A)==165 and len(E)==6 and COLS==224
    return A,rhs,E,names

def canonical(pattern):
    best=None
    for pi in permutations(range(4)):
        transformed=[PAIRS.index((pi[PAIRS[k][0]],pi[PAIRS[k][1]])) for k in pattern]
        order=tuple(sorted(range(4),key=lambda j:(transformed[j],j)))
        key=tuple(transformed[j] for j in order)
        choice=(key,pi,order)
        if best is None or choice<best:best=choice
    return best

def verify():
    bundle=json.loads((BASE/'B-all-orbit-rational-certificates.json').read_text())
    mapping=json.loads((BASE/'B-1365-to-69-orbit-map.json').read_text())
    all_modes=list(combinations_with_replacement(range(12),4))
    assert len(all_modes)==1365 and len(mapping['mapping'])==1365
    reps=sorted(set(canonical(p)[0] for p in all_modes));assert len(reps)==69
    assert mapping['representatives']==[list(p) for p in reps]
    for p,record in zip(all_modes,mapping['mapping']):
        key,pi,order=canonical(p)
        assert record=={'mode':list(p),'representative':reps.index(key),'extra_permutation':list(pi),'anchor_order':list(order)}
    certs=bundle['certificates'];assert len(certs)==69
    summaries=[]
    for expected,cert in zip(reps,certs):
        assert cert['mode']==list(expected)
        A,b,E,names=build(expected)
        lam={int(i):F(v) for i,v in cert['inequality_dual']}
        y=list(map(F,cert['equality_dual']))
        assert len(y)==6 and all(v<=0 for v in lam.values()) and all(0<=i<165 for i in lam)
        reduced=[]
        for c in range(COLS):
            val=F(int(c==COLS-1))-sum((v*A[i][c] for i,v in lam.items()),F())-sum((v*E[i][c] for i,v in enumerate(y)),F())
            assert val>=0,(expected,c,val)
            reduced.append(val)
        bound=sum((v*b[i] for i,v in lam.items()),F())+sum(y,F())
        assert bound>=F(1,2) and bound==F(cert['bound'])
        summaries.append({'mode':list(expected),'bound':str(bound),'nonzero_dual_rows':len(lam),'minimum_reduced_cost':str(min(reduced)),'zero_reduced_cost_columns':sum(v==0 for v in reduced)})
    return {'scope':'Exact solver-free certificate replay for all 69 S4 orbits covering all 1365 B pair multisets; no claim about A/C or original general half theorem.',
        'orbits':69,'multisets':1365,'client_types':223,'columns':224,'rows_per_mode':165,
        'minimum_dual_bound':str(min(F(v['bound']) for v in summaries)),'summaries':summaries}

if __name__=='__main__':
    r=verify();(BASE/'B-all-orbit-exact-replay.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='summaries'},indent=2))
