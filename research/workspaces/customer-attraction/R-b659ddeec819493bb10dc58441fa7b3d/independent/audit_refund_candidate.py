"""Definition-level independent audit of the supplied data, not its proof."""
from fractions import Fraction as F
from itertools import product,combinations_with_replacement
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
data=json.loads((HERE.parent/'refund/prefixed_refund_counterexample.json').read_text())
p,m=7,3
interests=[]
for mask,n in data['rows']:
    assert 0<mask<1<<p and n>0
    interests += [frozenset(t for t in range(p) if mask>>t&1)]*n
topics=[frozenset(j for j,B in enumerate(interests) if t in B) for t in range(p)]
assert len(set(topics))==p
sigma={tuple(row['history']):row['action'] for row in data['actions']}
expected={h for d in range(m) for h in product(range(p),repeat=d)}
assert set(sigma)==expected
def continuation(h):
    h=tuple(h)
    while len(h)<m: h+=(sigma[h],)
    return h
def utility(z,i):
    return sum((F(1,sum(zj in B for zj in z)) for B in interests if z[i] in B),F())
ic=[]
for h in expected:
    i=len(h);z=continuation(h);u=utility(z,i)
    for a in range(p):
        zz=continuation(h+(a,));gap=u-utility(zz,i)
        assert gap>=0,(h,a,gap)
        ic.append(gap)
z=continuation(())
C=frozenset().union(*(topics[t] for t in z))
us=[utility(z,i) for i in range(m)]
all_tuples=list(combinations_with_replacement(range(p),m))
cover={q:frozenset().union(*(topics[t] for t in q)) for q in all_tuples}
opt=max(map(len,cover.values()))
opts={q:O for q,O in cover.items() if len(O)==opt}
all_omnibus=[]
for q,O in opts.items():
    D=O-C
    f=[0]+[max(len(D.intersection(frozenset().union(*(topics[t] for t in a)))) for a in product(range(p),repeat=r)) for r in range(1,m+1)]
    es=[sum((F(1,sum(zj in B for zj in z)) for j,B in enumerate(interests) if z[i] in B and j not in O),F()) for i in range(m)]
    comparisons=[{'i':i+1,'r':m-i,'u':str(us[i]),'e':str(es[i]),'lhs':str(us[i]+es[i]),'rhs':f[m-i]-f[m-i-1],'gap':str(us[i]+es[i]-f[m-i]+f[m-i-1])} for i in range(m)]
    all_omnibus.append({'optimal_tuple':q,'O_size':len(O),'D_size':len(D),'C_outside_O':len(C-O),'f':f,'comparisons':comparisons})
out={'unit_customers':len(interests),'topics_distinct':True,'histories':len(expected),'IC_checks_including_self':len(ic),'IC_min':str(min(ic)),'terminal':z,'profits':list(map(str,us)),'welfare':len(C),'optimal':opt,'unordered_optimal_tuples':list(opts),'distinct_optimal_unions':len(set(opts.values())),'all_optimal_comparisons':all_omnibus,'half_gap':2*len(C)-opt}
assert sum(us)==len(C)
(HERE/'refund_candidate_independent_audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
