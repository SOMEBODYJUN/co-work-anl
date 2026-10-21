"""Self-contained Fraction verification; reads only local 41-client packet."""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from pathlib import Path
import json

def verify():
    data=json.loads(Path(__file__).with_name('all_optimal_query_failure_41.json').read_text())
    n=data['players'];k=len(data['topics']);customers=data['customers']
    sigma={tuple(z['history']):z['action'] for z in data['actions']}
    expected={h for d in range(n) for h in product(range(k),repeat=d)}
    assert set(sigma)==expected
    def utility(a,z):
        return sum((F(t['multiplicity'],sum(t['mask']>>b&1 for b in z)) for t in customers if t['mask']>>a&1),F(0))
    def terminal(h):
        while len(h)<n:h+=(sigma[h],)
        return h
    comparisons=0;minimum=None
    for h in expected:
        a=sigma[h];u=utility(a,terminal(h))
        for b in range(k):
            gap=u-utility(b,terminal(h+(b,)))
            assert gap>=0,(h,b,gap)
            comparisons+=1;minimum=gap if minimum is None else min(minimum,gap)
    z=terminal(());assert z==(0,4,4)
    u=[utility(a,z) for a in z];assert u==[F(10),F(19,2),F(19,2)]
    W=sum(u);assert W==29
    backgrounds=list(combinations_with_replacement(range(k),n-1))
    f={B:[utility(a,B+(a,)) for a in range(k)] for B in backgrounds}
    v=F(19,2);cap=tuple(data['static_cap_background'])
    assert f[cap]==[F(13,2),v,v,v,v]
    bad=list(map(F,data['bad_optimal_query']));good=list(map(F,data['good_optimal_query']))
    for p in (bad,good):
        assert sum(p)==1 and min(p)>=0
        assert min(sum(p[a]*f[B][a] for a in range(k)) for B in backgrounds)==v
    # The cap and either primal query match, so v is the exact static value.
    R=[]
    for a in range(k):
        R.append(sum(utility(a,z[:i]+(a,)+z[i+1:]) for i in range(n)))
    assert R==[F(23),F(32),F(32),F(32),F(79,3)]
    rb=sum(p*r for p,r in zip(bad,R));rg=sum(p*r for p,r in zip(good,R))
    assert rb==F(446,15)>W and rg==F(57,2)<W
    # For EVERY optimal p: positive pure cap slack forces p0=0. Its 44 row then
    # gives 13*(1-p4)+(22/3)*p4>=19/2, hence p4<=21/34. Therefore R(p)
    # =32-(17/3)*p4 >=57/2. The explicit good query attains this bound.
    assert f[(4,4)]==[F(10),F(13),F(13),F(13),F(22,3)]
    assert F(13)-F(19,2)==(F(13)-F(22,3))*F(21,34)
    assert F(32)-F(17,3)*F(21,34)==rg
    opt=max(sum(t['multiplicity'] for t in customers if any(t['mask']>>a&1 for a in T)) for T in combinations_with_replacement(range(k),n))
    assert opt==37
    return dict(scope=data['scope'],unit_customers=sum(t['multiplicity'] for t in customers),histories=len(expected),comparisons=comparisons,minimum_spe_gap=str(minimum),terminal=z,payoffs=list(map(str,u)),welfare=str(W),opt=opt,security=str(v),R_values=list(map(str,R)),bad_query_R=str(rb),bad_gap=str(rb-W),minimum_R_over_optimal_face=str(rg),good_gap=str(rg-W),aggregate_security_margin=str(W-n*v))

if __name__=='__main__':
    report=verify();print(json.dumps(report,ensure_ascii=False,indent=2))
    Path(__file__).with_name('all_optimal_query_failure_41_verified.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
