"""Independent literal-resource enumeration; no shared-repo imports or mutations."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


def frontier(bits):
    return sum(a != b for a, b in zip(bits, bits[1:])) <= 1


def gates(bits, v, degree):
    n = len(bits)
    cost = [F(0) for _ in bits]
    total = F(0)
    triggered = []
    for j in range(1, n-1):
        users = (0, j, j+1)
        sides = (bits[0], 1-bits[j], bits[j+1])
        counts = (sides.count(0), sides.count(1))
        for i, side in zip(users, sides):
            c = v[j] * F(counts[side], 3)**degree
            cost[i] += c
            total += c
        if max(counts) == 3:
            triggered.append(j)
    return cost, total, triggered


def run(n):
    alpha, B, p, rho, sigma, eps = F(2), F(1), 2, F(1,3), F(1,5), F(1,7)
    A = 2*alpha
    Q = 4*((alpha+p+1)*B+rho+sigma)
    S = sum(A**k for k in range(n-2))
    D = 1
    while F(2,3)**D*S > min(1/(4*alpha), eps/Q):
        D += 1
    v = {j: Q*A**(j-1) for j in range(1,n-1)}
    u = {j: v[j]*F(2,3)**D for j in v}
    z = {j: v[j]*F(1,3)**D for j in v}
    d = {j: 3*v[j]-2*u[j]-z[j] for j in v}
    U = [sum(u.values())] + [u.get(i-1,F(0))+u.get(i,F(0)) for i in range(1,n)]
    K = sum(2*u[j]+z[j] for j in v)
    for j in v:
        assert v[j]-alpha*(B+z[j]+v.get(j-1,F(0))) >= rho
        assert d[j]-d.get(j-1,F(0)) >= (p+1)*B+sigma
    assert alpha*(B+sum(u.values())) < min(v.values())
    assert K <= 3*eps
    states=list(product((0,1),repeat=n))
    repair_count=pair_count=escape_count=0
    min_repair_residual=None
    actual_pne=predicted_pne=[]
    # Literal actual congestion base: each player selects its own constant resource,
    # cost 1/5 in action0, 3/5 in action1. All weights1.
    actual_pne=[]
    predicted_pne=[]
    for s in states:
        g, W, tr=gates(s,v,D)
        assert (not tr)==frontier(s)
        assert W==K+sum(d[j] for j in tr)
        if tr:
            for j in tr:
                t=list(s); t[j]=s[0]; t=tuple(t)
                gt, Wt, tt=gates(t,v,D)
                assert set(tt)-set(tr) <= {j-1}
                assert j not in tt
                assert g[j]-alpha*(gt[j]+B) >= rho
                assert W-Wt >= (p+1)*B+sigma
                repair_count+=1
                residual=g[j]-alpha*(gt[j]+B)
                min_repair_residual=residual if min_repair_residual is None else min(min_repair_residual,residual)
        all_slacks=[]
        restricted_slacks=[]
        for i in range(n):
            t=list(s);t[i]=1-t[i];t=tuple(t)
            gt,_,_=gates(t,v,D)
            base_old=F(1+2*s[i],5)
            base_new=F(1+2*t[i],5)
            all_slacks.append(alpha*(base_new+gt[i])-(base_old+g[i]))
            if frontier(s) and frontier(t):
                assert g[i]==gt[i]==U[i]
                lhs=base_old-alpha*base_new
                rhs=(alpha-1)*U[i]
                assert (all_slacks[-1]>=0)==(lhs<=rhs)
                restricted_slacks.append(rhs-lhs)
                pair_count+=1
            elif frontier(s):
                assert alpha*gt[i] >= B+g[i]
                escape_count+=1
        if min(all_slacks)>=0:
            actual_pne.append(s)
        if frontier(s) and all(x>=0 for x in restricted_slacks):
            predicted_pne.append(s)
    assert actual_pne==predicted_pne
    return dict(n=n,degree=D,states=len(states),frontier=sum(frontier(s) for s in states),
                repair_moves_checked=repair_count,frontier_preserving_moves_checked=pair_count,
                frontier_escape_moves_checked=escape_count,exact_stable_set_match=True,
                alpha=str(alpha),stable_count=len(actual_pne),gate_baseline=str(K),
                epsilon=str(eps),min_individual_repair_margin=str(min_repair_residual))


def escape_without_coarse_E():
    n, D, alpha, B, p = 4, 2, F(1), F(1), 2
    v={1:F(4),2:F(8)}
    u={j:v[j]*F(2,3)**D for j in v}
    z={j:v[j]*F(1,3)**D for j in v}
    d={j:3*v[j]-2*u[j]-z[j] for j in v}
    assert all(v[j]-alpha*(B+z[j]+v.get(j-1,F(0)))>0 for j in v)
    assert all(d[j]-d.get(j-1,F(0))>(p+1)*B for j in v)
    assert B+sum(u.values()) > alpha*min(v.values())
    count=0
    for s in product((0,1), repeat=n):
        if not frontier(s):
            continue
        gs,_,_=gates(s,v,D)
        for i in range(n):
            t=list(s); t[i]=1-t[i]; t=tuple(t)
            gt,_,_=gates(t,v,D)
            if not frontier(t):
                assert gt[i]-gs[i] > B
                count+=1
    return dict(n=n,degree=D,alpha=str(alpha),RD=True,SD=True,coarse_E=False,
                all_escape_moves_raise_individual_cost_even_with_worst_base_drop=True,
                escape_moves=count)


if __name__=="__main__":
    result={"scope":"literal gate enumeration plus actual private constant-resource base; finite checks do not prove all n", "runs":[run(n) for n in range(3,8)], "escape_without_coarse_E":escape_without_coarse_E()}
    out=Path(__file__).with_name("sparse_gate_audit.json")
    out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
