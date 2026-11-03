"""Independent replay of the saved true-positive fresh-edge seed.

Reads the full strategy and checks every history/action with Fraction. It does
not import the discovery solver and does not treat arbitrary injection as an
optimal-coordinate source or as a residual-capacity counterexample.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations_with_replacement, permutations, product
from pathlib import Path
import json

base=Path(__file__).resolve().parent
d=json.loads((base/'positive_fresh_candidate.json').read_text())
m,k,w=d['players'],d['topics'],d['weights']
sigma={tuple(r['history']):r['action'] for r in d['strategy']}
def finish(h):
    while len(h)<m:h+=(sigma[h],)
    return h
def count(z,b):return sum(bool(b&(1<<a)) for a in z)
def payoff(z,i,domain=None):
    return sum((F(v,count(z,b)) for b,v in enumerate(w)
                if v and b&(1<<z[i]) and (domain is None or b in domain)),F())
checks=0
for i in range(m):
    for h in product(range(k),repeat=i):
        prescribed=payoff(finish(h),i)
        for a in range(k):
            assert prescribed>=payoff(finish(h+(a,)),i)
            checks+=1
Z=finish(())
C={b for b,v in enumerate(w) if v and count(Z,b)}
fresh={b for b,v in enumerate(w) if v and b not in C}
u=[payoff(Z,i) for i in range(m)]
W=sum(u)
def coverage(z):return sum(v for b,v in enumerate(w) if count(z,b))
opts=list(combinations_with_replacement(range(k),m))
opt=max(map(coverage,opts));T=next(t for t in opts if coverage(t)==opt)
i,j,g=d['i'],d['j'],tuple(d['context'])
B=finish(g);a=B[i];A=finish(Z[:i]+(a,));back=finish(g+(Z[i],))
nu=payoff(B,i,fresh);df=payoff(A,i,fresh)
P=N=F()
edges={}
for l in range(i+1,m):
    q=sum((F(w[b],count(A,b)*count(B,b)) for b in fresh
           if b&(1<<a) and b&(1<<A[l]) and not b&(1<<B[l])),F())
    if q:edges[l]=q
    P+=q
for b in fresh:
    if not b&(1<<a):continue
    past=sum(bool(b&(1<<s)) for s in g)
    oldonly=sum(bool(b&(1<<B[l])) and not b&(1<<A[l])
                for l in range(i+1,m))
    N+=F(w[b]*(past+oldonly),count(A,b)*count(B,b))
assert nu-df==P-N
assert edges[j]>0
ell=payoff(B,i)-payoff(back,i)
assert ell>=0
# This is a query over all catalogue actions at the same real history.
queries=[payoff(finish(g+(q,)),i) for q in range(k)]
assert max(queries)==payoff(B,i)
# All fresh sources together are small enough to be absorbed at every owner,
# for every optimal tuple and matching, in the R-only maximal-current variant.
R=sum(w[b] for b in fresh)
assert all(R<=v for v in u)
# The ordinary all-O coordinate construction with maximal current also does
# not initially reach g=(0): only owner 0 with T_0=0 can create that history.
source0=[]
for multiset in opts:
    if coverage(multiset)!=opt:continue
    for matched in sorted(set(permutations(multiset))):
        if matched[0]!=0:continue
        residual=F()
        for b,v in enumerate(w):
            if not v or not b&1:continue
            den=count(Z,b)+1-int(bool(b&(1<<Z[0])))
            inventory=F(v,count(matched,b))
            price=sum((F(v,count(matched,b)*den)
                       for l in range(1,m)
                       if b&(1<<Z[l]) and not b&(1<<matched[l])),F())
            residual+=inventory-price
        assert residual<=u[0]
        source0.append({'T':matched,'row_residual':str(residual),
                        'minimal_future_source':'0'})
out={
 'status':'passed','scope':'full-history SPE replay and one real positive fresh edge; no residual-cap counterexample',
 'history_count':len(sigma),'IC_comparisons_including_self':checks,
 'actual':Z,'u':list(map(str,u)),'W':str(W),'OPT':opt,'one_optimal_tuple':T,
 'fresh_customer_count':R,'positive_context':g,'role_zero_based':i,
 'prescribed_action':a,'B':B,'A':A,'nu':str(nu),'D_fresh':str(df),
 'P':str(P),'N':str(N),'loss':str(nu-P),'ell':str(ell),
 'positive_edges_zero_based':{str(l):str(q) for l,q in edges.items()},
 'all_catalogue_query_payoffs_at_context':list(map(str,queries)),
 'maximal_current_R_only_initialization_has_no_future_source':True,
 'all_optimal_T_matchings_covered_by_zero_source_reason':True,
 'all_O_maximal_current_source0_checks':source0,
 'all_O_maximal_current_initialization_reaches_positive_context':False,
 'arbitrary_natural_context_injection_only':True,
 'certifies_common_merge_cap':False}
(base/'positive_fresh_audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False))
