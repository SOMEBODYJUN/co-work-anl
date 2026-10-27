"""Integer/Fraction, all-ordered-history verifier; no optimizer/SPE oracle."""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from itertools import product,combinations_with_replacement
from collections import Counter
import json,hashlib
HERE=Path(__file__).resolve().parent
def verify():
    raw=(HERE/'six_esm_embedding.json').read_bytes();d=json.loads(raw);inst=d['instance']
    p=len(inst['topics']);m=inst['players'];cs=[(frozenset(c['topics']),c['multiplicity']) for c in inst['customers']]
    strategy={tuple(v['history']):v['action'] for v in d['strategy']}
    expected={h for k in range(m) for h in product(range(p),repeat=k)}
    assert len(strategy)==len(d['strategy']) and set(strategy)==expected
    assert all(type(w) is int and w>0 for t,w in cs)
    assert all(type(a) is int and 0<=a<p for a in strategy.values())
    def counts(z):return tuple(z.count(a) for a in range(p))
    @lru_cache(None)
    def U(q,a):return sum((F(w,sum(q[t] for t in members)) for members,w in cs if a in members),F(0))
    @lru_cache(None)
    def finish(h):return h if len(h)==m else finish(h+(strategy[h],))
    slacks=[]
    for h in expected:
        z=finish(h);u=U(counts(z),z[len(h)])
        for a in range(p):
            slack=u-U(counts(finish(h+(a,))),a)
            assert slack>=0,(h,a,slack);slacks.append(slack)
    for a in range(p):
        for b in range(a):assert any((a in t)!=(b in t) for t,w in cs)
    z=finish(());assert z==tuple(d['actual_path'])
    prefix=tuple(d['examined_prefix']);assert z[:len(prefix)]==prefix
    r=m-len(prefix);a=strategy[prefix];assert a==d['examined_action']
    def P(q):return sum((w*sum((F(1,j) for j in range(1,sum(t in members for t in q)+1)),F(0)) for members,w in cs),F(0))
    baseline=P(prefix);profiles=list(combinations_with_replacement(range(p),r))
    rel=lambda q:P(prefix+q)-baseline
    pmax=max(map(rel,profiles));pforced=max(rel(q) for q in profiles if a in q)
    safe=sum((F(w,r+sum(t in members for t in prefix)) for members,w in cs if a in members),F(0))
    u=U(counts(z),a);E=pmax-pforced
    assert (pmax,pforced,u,safe,E-u+safe)==(F(801),F(754),F(166),F(120),F(1))
    W=sum(w for t,w in cs if any(a in t for a in z));OPT=max(sum(w for t,w in cs if any(a in t for a in q)) for q in combinations_with_replacement(range(p),m))
    assert 2*W>=OPT
    out={'status':'PASS_ALL_HISTORY_SIX_ACTUAL_PREFIX_AUXILIARY_OBSTRUCTION','input_sha256':hashlib.sha256(raw).hexdigest(),
         'unit_customers':sum(w for t,w in cs),'players':m,'topics':p,'histories':len(expected),
         'comparisons_including_self':len(slacks),'minimum_IC':str(min(slacks)),'actual_path':z,
         'actual_payoffs':[str(U(counts(z),a)) for a in z],'examined_prefix':prefix,'P3_background':str(pmax),
         'P3_background_forced_A':str(pforced),'E':str(E),'u_minus_safe':str(u-safe),'violation':str(E-u+safe),
         'W':W,'OPT6':OPT,'scope':'ESM only, not Q-CAG-HALF or total potential/copy-tax counterexample'}
    (HERE/'six_esm_embedding_audit.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));return out
if __name__=='__main__':verify()
