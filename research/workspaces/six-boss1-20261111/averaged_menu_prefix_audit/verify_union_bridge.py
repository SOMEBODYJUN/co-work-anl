#!/usr/bin/env python3
"""Standalone exact coverage-union bridge and two-theta cone verifier.

Only standard-library Fraction; no optimizer, Main import, or game point.
This file does not import the averaged-menu verifier either.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

OUT=Path(__file__).resolve().parent
WS=OUT.parent
ROOT=OUT.parents[3]


def dump(name,value):
    (OUT/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n")


def dot(a,b):
    assert len(a)==len(b)
    return sum((x*y for x,y in zip(a,b)),F(0))


def payment_remainder(r,typ,p,u=F(0)):
    n,k,x,*tail=typ
    middle,t,o=tail[:-2],tail[-2],tail[-1]
    assert len(middle)==r-2 and o in (0,1) and len(p)==2*r
    b=n-1
    theta=F(o,6)
    C=sum(p[:r],F(0))
    target=C*u-(C-1)*F(x,b+r)-theta*(F(x,b+r)+F(1-x,b+1))
    source_income=F(x,b+1+sum(middle)+t)
    paid=p[0]*(u-source_income)
    for ell,z in enumerate(middle+[t]):
        paid+=p[ell+1]*(u-F(z,b+r))
        paid+=p[r+ell]*F(x-z,b+k+1)
    last_den=b+x+sum(middle)+1
    # The union query is a weaker budget derived from six legal last-node ICs.
    paid+=p[-1]*(F(t,last_den)-theta/last_den)
    return target-paid


def weights(r,a):
    return [F(5*(r-1))]+[F(0)]*(r-2)+[F(r)]+[a]*(r-2)+[F(0),F(1)]


source_paths=[
    "archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md",
    "research/workspaces/six-boss1-20261111/main_averaged_menu_prefix.md",
    "research/workspaces/six-boss1-20261111/main_averaged_menu_prefix.json",
    "research/workspaces/six-boss1-20261111/main_optimal_union_prefix.md",
    "research/workspaces/six-boss1-20261111/main_optimal_union_prefix.json",
]
sources=[{"path":p,"sha256":hashlib.sha256((ROOT/p).read_bytes()).hexdigest()} for p in source_paths]

# Do not assert a single-customer IC. Only the exact difference between the
# two budgets is pointwise nonnegative; the legal six-IC average is nonnegative
# after summation over customers by the true SPE hypothesis.
bridge_checks=0
for qs in product((0,1),repeat=6):
    d=sum(qs);o=int(d>0)
    for denom in range(1,7):
        for t in (0,1):
            actual_mean=F(t,denom)-sum((F(q,denom) for q in qs),F(0))/6
            weakened_union=F(t,denom)-F(o,6*denom)
            nonnegative_gap=F(d-o,6*denom)
            assert nonnegative_gap>=0
            assert weakened_union==actual_mean+nonnegative_gap
            bridge_checks+=1

cases=[]
certificates=[]
for r in (4,5,6):
    m,N=r-2,7-r
    a0=F(r-1,12)
    astar=F(5*r-6,r*(r-1))
    Cbar=F(6*r-5)
    alpha=F(5*(r-1))
    types=[(n,k,*bits,o) for n in range(1,N+1) for k in range(m+1)
           for bits in product((0,1),repeat=r) for o in (0,1)]
    assert len(types)=={4:288,5:512,6:640}[r]
    # Reconstruct every displayed candidate coefficient through target - wallets.
    endpoint_stats=[]
    for name,a in (("a0",a0),("astar",astar)):
        p=weights(r,a)
        vals=[]
        for typ in types:
            n,k,x,*tail=typ
            ys,t,o=tail[:-2],tail[-2],tail[-1]
            j,D=sum(ys),n+r-1
            theta=F(o,6)
            direct=(alpha*F(x,n+j+t)+F(r*t,D)-(Cbar-1)*F(x,D)
                    -theta*(F(x,D)+F(1-x,n))-a*F(m*x-j,n+k)
                    -F(t-theta,n+x+j))
            E=payment_remainder(r,typ,p)
            assert E==direct==payment_remainder(r,typ,p,F(1))
            assert E>=0
            vals.append(E)
        endpoint_stats.append({"name":name,"a":str(a),"type_checks":len(types),
            "zero_count":sum(v==0 for v in vals),"min_positive_E":str(min(v for v in vals if v>0))})
    # Three positive support multipliers remain valid because the enlarged
    # domain still contains all theta=1/6 rows.
    A=(1,0,0,*([0]*m),0,1)
    G=(1,m,0,*([0]*m),1,1)
    H=(N,0,1,*([1]*m),0,1)
    support=[("A",A,F(30*r-5)),("G",G,F(6*r)),("H",H,F(30))]
    assert all(typ in types for _,typ,_ in support)
    B=F(30,N)-F(6*r,r-1)
    assert B>0
    zero=[F(0)]*(2*r)
    basis=[zero]+[[F(int(c==j)) for c in range(2*r)] for j in range(2*r)]
    cost=[F(1)]*r+[F(0)]*r
    rows=[]
    gt=[F(0)]*(2*r)
    dual_value=F(0)
    for name,typ,w in support:
        constant=payment_remainder(r,typ,zero)
        coeff=[payment_remainder(r,typ,e)-constant for e in basis[1:]]
        h=-constant
        rows.append({"name":name,"type":list(typ),"lambda":str(w),"G":list(map(str,coeff)),"h":str(h)})
        gt=[z+w*g for z,g in zip(gt,coeff)]
        dual_value+=w*h
    reduced=[c-z for c,z in zip(cost,gt)]
    assert reduced==[F(0)]+[F(1)]*m+[F(0)]+[F(0)]*m+[B,F(0)]
    assert dual_value==Cbar
    for p in basis:
        right=sum((w*payment_remainder(r,typ,p) for _,typ,w in support),F(0))
        right+=sum(p[1:r-1],F(0))+B*p[-2]
        assert sum(p[:r],F(0))-Cbar==right
    # Necessary independent middle MAX bounds in the optimal slice.
    fixed=weights(r,F(0))
    middle_basis=[fixed]
    for ell in range(m):
        p=fixed.copy();p[r+ell]=F(1);middle_basis.append(p)
    bound_rows=[]
    for ell in range(m):
        e=[int(j==ell) for j in range(m)]
        Dtype=(1,m,0,*e,0,1)  # theta=1/6 forces the lower endpoint.
        Btype=(1,0,1,*(1-y for y in e),1,0)  # theta=0 forces the upper.
        assert Dtype in types and Btype in types
        for p in middle_basis:
            assert payment_remainder(r,Dtype,p)==p[r+ell]/(r-1)-F(1,12)
            assert payment_remainder(r,Btype,p)==astar-p[r+ell]
        bound_rows.append({"position":ell+1,"lower_type":list(Dtype),"upper_type":list(Btype)})
    corners=[]
    box_checks=0
    for avector in product((a0,astar),repeat=m):
        p=fixed.copy();p[r:r+m]=avector
        vals=[payment_remainder(r,typ,p) for typ in types]
        assert min(vals)>=0 and sum(p[:r],F(0))==Cbar
        box_checks+=len(types)
        corners.append({"middle_MAX":list(map(str,avector)),"min_E":str(min(vals)),
                        "zero_count":sum(v==0 for v in vals)})
    cases.append({"r":r,"source":7-r,"status":"PASS_UNIVERSAL_UNION_BRIDGE",
        "C":str(Cbar),"alpha":str(alpha),"theta_domain":["0","1/6"],"types":len(types),
        "endpoint_checks":endpoint_stats,"no_penalty":True,"restricted_cone_optimum":str(Cbar),
        "exact_optimal_middle_box":{"lower":str(a0),"upper":str(astar),"dimension":m},
        "box_corner_type_checks":box_checks,"all_optimal_fixed":{"alpha":str(alpha),
        "s_middle":"0","sT":str(r),"aT":"0","delta":"1"},
        "dual_support_count":3,"terminal_MAX_reduced_cost":str(B)})
    certificates.append({"r":r,"variable_count":2*r,"type_order":"n,k,x,y1,...,ym,t,o",
        "dual_support":rows,"dual_reduced_cost":list(map(str,reduced)),"dual_value":str(dual_value),
        "optimal_middle_bounds":bound_rows,"box_corners":corners})

assert sum(c["types"] for c in cases)==1440
assert sum(c["box_corner_type_checks"] for c in cases)==15488

# Coverage corollary, independently reconstructed from the first-source bound
# and each of the other five sources' genuine |R|/6 SAFE guarantee.
safe_denominator_checks=0
for i in range(1,7):
    for old in range(i):
        for later in range(7-i):
            assert 1<=old+1+later<=6 and F(1,old+1+later)>=F(1,6)
            safe_denominator_checks+=1
coverage_basis=[[F(0)]*4]+[[F(int(c==j)) for c in range(4)] for j in range(4)]
coverage_checks=0
for M,O,J,K in coverage_basis:
    first_rhs=F(30,6)*M+F(1,6)*(J/6+(O-J))
    assert first_rhs==5*M+O/6-5*J/36
    wM=(1110*M+6*O-5*J)/1116
    assert wM==first_rhs/31+5*M/6
    assert wM-(1105*M+6*O)/1116==5*(M-J)/1116
    assert (1105*M+6*O)/1116-O/2==(1105*M-552*O)/1116
    wK=(930*K+180*M+6*O-5*J)/1116
    assert wK==first_rhs/31+5*K/6
    assert wK-(930*K+175*M+6*O)/1116==5*(M-J)/1116
    assert (930*K+175*M+6*O)/1116-O/2==(930*K+175*M-552*O)/1116
    coverage_checks+=7
assert F(1105)*F(552,1105)==552
coverage={"status":"PASS_EXACT_CONDITIONAL_COVERAGE_LEMMA",
    "symbol_order":["M=|X|","O=|U|","J=|U intersect X|","K=max_catalog_size"],
    "first_source":"31*u1 >= 5*M + O/6 - 5*J/36",
    "using_X_exact":"W >= (1110*M+6*O-5*J)/1116",
    "using_X_relaxed":"W >= (1105*M+6*O)/1116",
    "half_condition_X":"1105*M >= 552*OPT6","threshold":"552/1105",
    "using_K_exact":"W >= (930*K+180*M+6*O-5*J)/1116",
    "using_K_relaxed":"W >= (930*K+175*M+6*O)/1116",
    "half_condition_K_X":"930*K+175*M >= 552*OPT6",
    "coefficient_identity_checks":coverage_checks,"SAFE_denominator_checks":safe_denominator_checks,
    "no_division_by_OPT6":True,"uses_J_le_M":True}
main_union=json.loads((WS/"main_optimal_union_prefix.json").read_text())
assert main_union["proof_sha256"]==hashlib.sha256((WS/"main_optimal_union_prefix.md").read_bytes()).hexdigest()
assert main_union["parent_type_audit_sha256"]==hashlib.sha256((WS/"main_averaged_menu_prefix.json").read_bytes()).hexdigest()
assert main_union["half_threshold"]==coverage["threshold"]
for source in sources:
    assert hashlib.sha256((ROOT/source["path"]).read_bytes()).hexdigest()==source["sha256"]
dump("union_bridge_certificates.json",certificates)
result={"status":"PASS_UNIVERSAL_OPT6_UNION_PREFIX_AND_EXACT_TWO_THETA_CONES",
    "bridge_identity":"B_union=B_six_legal_IC_average+sum[(d-o)/(6(n+x+j))]",
    "bridge_checks":bridge_checks,"pointwise_gap_nonnegative":True,
    "union_is_not_required_to_be_a_legal_label":True,"customers_or_legal_actions_changed":False,
    "conclusion":"For any six legal labels with union U, C u-(C-1)kappa_X >= (1/6)sum_{c in U}[x/D+(1-x)/n], C=6r-5.",
    "cases":cases,"coverage_corollary":coverage,"source_sha256":sources,"optimizer_calls":0,"game_point_reads":0,
    "other_program_imports_or_executions":0,"verifier_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "scope":"Universal source inequality for six-label coverage unions, including any OPT6 union. Cone sharpness is limited to the specified nonnegative 2r-weight all-type cone; no real-SPE sharpness or half closure claim."}
dump("union_bridge.json",result)
print(json.dumps(result,ensure_ascii=False,indent=2))
