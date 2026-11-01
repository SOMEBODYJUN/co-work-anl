"""Exact unit-client verification of the 16-client PURE shortcut counterexample.

This author-side verification does not import the discovery program. The
construction branch performs a separate independent audit.
"""
from fractions import Fraction as F
from itertools import product
import json

COUNTS={2:1,14:1,16:1,18:1,29:3,38:1,41:1,43:2,45:2,47:1,49:1,52:1}
CLIENTS=[s for s,w in COUNTS.items() for _ in range(w)]
M,K=3,6
CHALLENGERS=(5,5,5,2,2,2)

def action(h):
    if not h:return 0
    if len(h)==1:return 3 if h[0]<3 else 0
    return next(a for a in (range(3) if h[1]<3 else range(3,6)) if a not in h)
def finish(h):
    while len(h)<M:h+=(action(h),)
    return h
def payoff(z,i):
    return sum((F(1,sum((s>>a)&1 for a in z)) for s in CLIENTS if (s>>z[i])&1),F(0))
def welfare(z):
    return sum(any((s>>a)&1 for a in z) for s in CLIENTS)

def audit():
    policy=[];gaps=[]
    for d in range(M):
        for h in product(range(K),repeat=d):
            policy.append({"history":h,"action":action(h)})
            for a in range(K):
                gaps.append(payoff(finish(h),d)-payoff(finish(h+(a,)),d))
    assert len(policy)==43 and len(gaps)==258 and min(gaps)>=0
    z=finish(())
    table=[];qrows=[];drows=[]
    for a in range(K):
        leaves=[finish(z[:i]+(a,)) for i in range(M)]
        qa=[sum((F(1,M*(M-1)) for i,y in enumerate(leaves) for j,v in enumerate(y) if j!=i and v==b),F(0)) for b in range(K)]
        g=[]
        for b in range(K):
            g.append(sum((F(1,1)/(1+(M-1)*sum(qa[v] for v in range(K) if (s>>v)&1)) for s in CLIENTS if (s>>b)&1),F(0)))
        qrows.append(qa);table.append(g)
        drows.append([payoff(y,i) for i,y in enumerate(leaves)])
    improvements=[table[a][b]-table[a][a] for a,b in enumerate(CHALLENGERS)]
    assert improvements==[F(3,8),F(1,35),F(3,56),F(9,28),F(1,12),F(1,12)]
    assert min(improvements)>0
    w=welfare(z);u=[payoff(z,i) for i in range(M)]
    assert all(M*table[a][a]<=sum(drows[a])<=w for a in range(K))
    return {"claim":"Every pure query fails self-consistency, not HALF or mixed-SC payment",
      "players":M,"topics":["X0","X1","X2","Y0","Y1","Y2"],
      "customer_mask_multiplicities":COUNTS,"unit_clients":len(CLIENTS),"policy":policy,
      "decision_nodes":len(policy),"ic_comparisons":len(gaps),"minimum_ic_gap":min(gaps),
      "actual_path":z,"utilities":u,"welfare":w,
      "optimum":max(welfare(t) for t in product(range(K),repeat=M)),
      "pool_marginal_rows":qrows,"query_value_matrix_rows_pure_trigger_columns_query":table,
      "pure_trigger_deviation_payoffs_by_position":drows,
      "challengers":CHALLENGERS,"strict_query_improvements":improvements,
      "diagonal_jensen_cap_verified":True}
if __name__=="__main__":
    print(json.dumps(audit(),default=str,indent=2))
