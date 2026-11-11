#!/usr/bin/env python3
"""Exact averaged-menu audit from true wallets; standard library only.

No optimizer, no numerical game point, no imported or executed Main program.
The restricted cone certificate is reconstructed from actual payment expressions.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

OUT=Path(__file__).resolve().parent
WS=OUT.parent
ROOT=OUT.parents[3]


def dump(name,obj):
    (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n")


def dot(a,b):
    assert len(a)==len(b)
    return sum((u*v for u,v in zip(a,b)),F(0))


def from_wallets(r,typ,p,u=F(0)):
    n,k,x,*tail=typ
    ys,t,d=tail[:-2],tail[-2],tail[-1]
    assert len(ys)==r-2 and len(p)==2*r
    theta=F(d,6)
    b=n-1
    C=sum(p[:r],F(0))
    kappa=F(x,b+r)
    Laverage=theta*(F(x,b+r)+F(1-x,b+1))
    target=C*u-(C-1)*kappa-Laverage
    # Source IC uses the actual continuation of force X.
    v=F(x,b+1+sum(ys)+t)
    budgets=p[0]*(u-v)
    # Each SAFE is the guaranteed denominator after its own source deviation;
    # each MAX uses the original actual P=b+k.
    for ell,member in enumerate(ys+[t]):
        budgets+=p[1+ell]*(u-F(member,b+r))
        budgets+=p[r+ell]*F(x-member,b+k+1)
    # Average six true last-node ICs. The denominator is common to all six.
    last_den=b+x+sum(ys)+1
    w=F(t,last_den)
    six_query_bits=[1]*d+[0]*(6-d)
    averaged_query=sum((F(q,last_den) for q in six_query_bits),F(0))/6
    assert averaged_query==theta/last_den
    budgets+=p[-1]*(w-averaged_query)
    return target-budgets


def shown_E(r,typ,p):
    n,k,x,*tail=typ
    ys,t,d=tail[:-2],tail[-2],tail[-1]
    theta=F(d,6)
    j,D=sum(ys),n+r-1
    C=sum(p[:r],F(0))
    return (p[0]*F(x,n+j+t)
            +sum((s*F(y,D) for s,y in zip(p[1:r],ys+[t])),F(0))
            -(C-1)*F(x,D)-theta*(F(x,D)+F(1-x,n))
            -sum((a*F(x-y,n+k) for a,y in zip(p[r:2*r-1],ys+[t])),F(0))
            -p[-1]*F(t-theta,n+x+j))


def candidate(r,a):
    m=r-2
    return [F(5*(r-1))]+[F(0)]*m+[F(r)]+[a]*m+[F(0),F(1)]


def penalty(r,n,k,d,a):
    vals=[j*(F(d,6*n*(n+j))-a/F(n+k)) for j in range(r-1)]
    val=max(vals)
    assert val>=0
    return val,[j for j,v in enumerate(vals) if v==val]


def affine(r,typ):
    zero=[F(0)]*(2*r)
    offset=from_wallets(r,typ,zero)
    coeff=[]
    for col in range(2*r):
        unit=zero.copy();unit[col]=F(1)
        coeff.append(from_wallets(r,typ,unit)-offset)
    return coeff,-offset


source_paths=[
    "archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md",
    "research/workspaces/six-boss1-20261111/main_prefix_safety_maxx_family.md",
    "research/workspaces/six-boss1-20261111/main_averaged_menu_prefix.md",
    "research/workspaces/six-boss1-20261111/main_averaged_menu_prefix.py",
    "research/workspaces/six-boss1-20261111/main_averaged_menu_prefix.json",
]
sources=[{"path":s,"sha256":hashlib.sha256((ROOT/s).read_bytes()).hexdigest()} for s in source_paths]
dump("source_manifest.json",{"sources":sources,"read_game_points":False})

# Every six-label Boolean membership pattern has one of the seven d values;
# replacing it by d uses only linearity of the same-node averaged query.
hist=[0]*7
for bits in product((0,1),repeat=6):
    d=sum(bits);hist[d]+=1
    for denom in range(1,7):
        assert sum((F(q,denom) for q in bits),F(0))/6==F(d,6*denom)
assert hist==[1,6,15,20,15,6,1]

results=[]
penalty_tables=[]
restricted_certificates=[]
for r in (4,5,6):
    m,N=r-2,7-r
    alpha=F(5*(r-1))
    Cbar=F(6*r-5)
    a0=F(r-1,12)
    astar=F(5*r-6,r*(r-1))
    afixed=(alpha-1+F(1,6))/F(r*(r-1))
    assert 0<a0<astar<afixed
    types=[(n,k,*bits,d) for n in range(1,N+1) for k in range(m+1)
           for bits in product((0,1),repeat=r) for d in range(7)]
    assert len(types)=={4:1008,5:1792,6:2240}[r]
    # Here the r bits are x, m ordered middle memberships, t.
    family=[]
    for name,a in (("a0",a0),("astar",astar)):
        p=candidate(r,a)
        assert sum(p[:r],F(0))==Cbar
        minima={"x1":None,"x0_t1":None,"corrected":None}
        negative=0;zero_corrected=0;min_positive=None
        for typ in types:
            n,k,x,*tail=typ
            ys,t,d=tail[:-2],tail[-2],tail[-1]
            j=sum(ys);theta=F(d,6)
            E=from_wallets(r,typ,p)
            assert E==shown_E(r,typ,p)==from_wallets(r,typ,p,F(1))
            Pi,_=penalty(r,n,k,d,a)
            corrected=E+(1-x)*Pi
            assert corrected>=0
            minima["corrected"]=corrected if minima["corrected"] is None else min(minima["corrected"],corrected)
            zero_corrected+=corrected==0
            if corrected>0:
                min_positive=corrected if min_positive is None else min(min_positive,corrected)
            negative+=E<0
            if x:
                assert E>=0
                minima["x1"]=E if minima["x1"] is None else min(minima["x1"],E)
            elif t:
                assert E>=0
                minima["x0_t1"]=E if minima["x0_t1"] is None else min(minima["x0_t1"],E)
            else:
                assert E==j*(a/F(n+k)-theta/F(n*(n+j)))
            if d<=1: assert E>=0 and Pi==0
        family.append({"parameter":name,"a":str(a),"customer_types":len(types),
                       "payment_equalities":2*len(types),"unpenalized_negative_types":negative,
                       "corrected_zero_types":zero_corrected,"min_positive_corrected":str(min_positive),
                       "minima":{k:str(v) for k,v in minima.items()}})
    penalty_rows=[]
    for n in range(1,N+1):
        assert (r-1)*n*(n+1)>=2*(n+m)
        for k in range(m+1):
            for d in range(7):
                bound=F(max(d-1,0)*m,6*n*(n+m))
                p0,arg0=penalty(r,n,k,d,a0)
                ps,args=penalty(r,n,k,d,astar)
                assert 0<=ps<=p0<=bound
                if d<=1: assert ps==p0==0
                # Exact minimum over hidden ordered memberships and t. Every j
                # has a Boolean representative, so no independence assumption.
                min_E=min(from_wallets(r,(n,k,0,*([1]*j+[0]*(m-j)),t,d),candidate(r,astar))
                          for j in range(m+1) for t in (0,1))
                assert min_E==-ps
                penalty_rows.append({"n":n,"k":k,"d":d,"Pi_a0":str(p0),"argmax_a0":arg0,
                    "Pi_astar":str(ps),"argmax_astar":args,"simple_bound":str(bound),
                    "minimum_x0_residual":str(min_E)})
    threshold=(12*astar/F(r-1)).numerator//(12*astar/F(r-1)).denominator
    assert threshold=={4:4,5:2,6:1}[r]
    assert all(F(v["Pi_astar"])==0 for v in penalty_rows if v["d"]<=threshold)
    witness_d=threshold+1
    witness_pi,_=penalty(r,1,m,witness_d,astar)
    witness_type=(1,m,0,1,*([0]*(m-1)),0,witness_d)
    witness_E=from_wallets(r,witness_type,candidate(r,astar))
    assert witness_E<0 and witness_pi==-witness_E=={4:F(1,36),5:F(1,80),6:F(1,150)}[r]
    G_endpoints=[astar*F((n+m)*(n+r-1),n) for n in (1,N)]
    assert all(g<=alpha-1 for g in G_endpoints)
    for n in range(1,N+1):
        assert astar*F((n+m)*(n+r-1),n)<=alpha-1
        assert afixed*F((n+m)*(n+r-1),n)<=alpha-1+F(1,6)

    # Full 2r coefficient cone restricted to constant theta=1/6.
    restricted_types=[typ for typ in types if typ[-1]==1]
    zero=[F(0)]*(2*r)
    basis=[zero]+[[F(int(j==c)) for c in range(2*r)] for j in range(2*r)]
    A=(1,0,0,*([0]*m),0,1)
    Z=(1,0,1,*([1]*m),1,1)
    G=(1,m,0,*([0]*m),1,1)
    H=(N,0,1,*([1]*m),0,1)
    for typ in (A,Z,G,H): assert typ in restricted_types
    for p in basis:
        assert from_wallets(r,A,p)==(p[-1]-1)/6
        assert from_wallets(r,Z,p)==F(5,6*r)*(1-p[-1])
        assert from_wallets(r,G,p)==p[r-1]/r+p[-2]/(r-1)-F(5,6)*p[-1]-F(1,6)
        assert from_wallets(r,H,p)==p[0]/30-p[r-1]/6-p[-2]/N+F(5,36)+p[-1]/36
    support=[("A",A,F(30*r-5)),("G",G,F(6*r)),("H",H,F(30))]
    B=F(30,N)-F(6*r,r-1)
    assert B=={4:F(2),5:F(15,2),6:F(114,5)}[r]>0
    cost=[F(1)]*r+[F(0)]*r
    rows=[]
    gt=[F(0)]*(2*r)
    dualvalue=F(0)
    for name,typ,w in support:
        coeff,h=affine(r,typ)
        rows.append({"name":name,"type":list(typ),"lambda":str(w),"G":list(map(str,coeff)),"h":str(h)})
        gt=[a+w*z for a,z in zip(gt,coeff)]
        dualvalue+=w*h
    reduced=[c-z for c,z in zip(cost,gt)]
    expected=[F(0)]+[F(1)]*m+[F(0)]+[F(0)]*m+[B,F(0)]
    assert reduced==expected and dualvalue==Cbar
    for p in basis:
        rhs=sum((w*from_wallets(r,typ,p) for _,typ,w in support),F(0))
        rhs+=sum(p[1:r-1],F(0))+B*p[-2]
        assert sum(p[:r],F(0))-Cbar==rhs
    payment_basis_checks=0
    for typ in restricted_types:
        for p in basis:
            assert from_wallets(r,typ,p)==shown_E(r,typ,p)
            payment_basis_checks+=1

    # Exact optimal face. Necessity uses each D_l and B_l separately.
    fixed=candidate(r,F(0))
    middle_basis=[fixed]
    for ell in range(m):
        p=fixed.copy();p[r+ell]=F(1);middle_basis.append(p)
    for ell in range(m):
        e=[int(j==ell) for j in range(m)]
        Dtype=(1,m,0,*e,0,1)
        Btype=(1,0,1,*(1-y for y in e),1,1)
        for p in middle_basis:
            assert from_wallets(r,Dtype,p)==p[r+ell]/(r-1)-F(1,12)
            assert from_wallets(r,Btype,p)==afixed-p[r+ell]
    # Sufficiency: the full box is convex, and every one of its corners is feasible.
    corners=[]
    corner_checks=0
    for choices in product((a0,afixed),repeat=m):
        p=fixed.copy();p[r:r+m]=choices
        vals=[from_wallets(r,typ,p) for typ in restricted_types]
        assert min(vals)>=0 and sum(p[:r],F(0))==Cbar
        corner_checks+=len(vals)
        corners.append({"a_middle":list(map(str,choices)),"min_E":str(min(vals)),
                        "zero_count":sum(v==0 for v in vals)})
    # The larger fixed-theta upper endpoint cannot be used universally without
    # changing the x=1 correction: the d=0 B type has a negative residual.
    bad_type=(1,0,1,0,*([1]*(m-1)),1,0)
    bad_E=from_wallets(r,bad_type,candidate(r,afixed))
    assert bad_E==-F(1,6*r*(r-1))
    restricted_certificates.append({"r":r,"variables":2*r,"types":len(restricted_types),
        "theta":"1/6","C":str(Cbar),"dual_support":rows,"dual_value":str(dualvalue),
        "dual_reduced_cost":list(map(str,reduced)),"B_terminal_MAX":str(B),
        "all_optimal_fixed":{"alpha":str(alpha),"s_middle":"0","sT":str(r),"aT":"0","delta":"1"},
        "exact_optimal_face":{"shape":"Independent closed intervals for all ordered middle MAX weights",
            "lower":str(a0),"upper":str(afixed),"dimension":m,"corners":corners},
        "payment_basis_checks":payment_basis_checks,"box_corner_type_checks":corner_checks,
        "universal_misuse_witness":{"type":list(bad_type),"a":str(afixed),"E":str(bad_E)}})
    penalty_tables.append({"r":r,"a0":str(a0),"astar":str(astar),"rows":penalty_rows})
    results.append({"r":r,"actual_source":7-r,"status":"PASS_AVERAGED_MENU_AND_RESTRICTED_CONE",
        "Cbar":str(Cbar),"alpha":str(alpha),"a0":str(a0),"astar":str(astar),
        "universal_parameter_interval":[str(a0),str(astar)],"family_endpoint_checks":family,
        "penalty_table_entries":len(penalty_rows),"penalty_exact_pointwise_minimum":True,
        "simple_bound_pass":True,"d_le_one_penalty_zero":True,"sharp_uniform_zero_penalty_d":threshold,
        "first_bad_d_witness":{"d":witness_d,"type":list(witness_type),"E":str(witness_E),"Pi":str(witness_pi)},
        "G_endpoints":list(map(str,G_endpoints)),"restricted_cone_optimum":str(Cbar),
        "restricted_optimal_middle_interval":[str(a0),str(afixed)],"restricted_optimal_face_dimension":m,
        "restricted_dual_support_count":3,"B_terminal_MAX":str(B),
        "improvement_from_previous_Cstar":str({4:F(61,3),5:F(121,4),6:F(206,5)}[r]-Cbar)})

# Compare with Main only after independently building all coefficients and bounds.
main=json.loads((WS/"main_averaged_menu_prefix.json").read_text())
assert main["status"]=="PASS" and main["optimizer_calls"]==main["point_reads"]==0
assert main["source_md_sha256"]==hashlib.sha256((WS/"main_averaged_menu_prefix.md").read_bytes()).hexdigest()
assert main["source_py_sha256"]==hashlib.sha256((WS/"main_averaged_menu_prefix.py").read_bytes()).hexdigest()
for saved,own,pt,cert in zip(main["families"],results,penalty_tables,restricted_certificates):
    r=own["r"]
    assert saved["r"]==r and str(saved["C"])==own["Cbar"] and str(saved["alpha"])==own["alpha"]
    assert saved["a_star"]==own["astar"] and saved["a_lower"]==own["a0"]
    endpoint=own["family_endpoint_checks"][1]
    assert saved["type_count"]==endpoint["customer_types"]
    assert saved["negative_without_correction"]==endpoint["unpenalized_negative_types"]
    assert saved["zero_after_correction"]==endpoint["corrected_zero_types"]
    assert saved["min_positive_after_correction"]==endpoint["min_positive_corrected"]
    assert saved["G_endpoints"]==own["G_endpoints"]
    assert saved["penalty_table"]==[{"n":row["n"],"k":row["k"],"d":row["d"],
           "Pi":row["Pi_astar"],"simple_upper":row["simple_bound"]} for row in pt["rows"]]
    assert saved["restricted_cone"]["dual_weights_A_G_H"]==[int(F(row["lambda"])) for row in cert["dual_support"]]
    assert saved["restricted_cone"]["terminal_MAX_reduced_cost"]==cert["B_terminal_MAX"]
    assert str(saved["restricted_cone"]["optimum"])==cert["C"]
for source in sources:
    assert hashlib.sha256((ROOT/source["path"]).read_bytes()).hexdigest()==source["sha256"]
dump("penalty_tables.json",penalty_tables)
dump("restricted_cone_certificate.json",restricted_certificates)
output={"status":"PASS_INDEPENDENT_AVERAGED_MENU_PREFIX_AUDIT","results":results,
        "six_label_membership_count_distribution":hist,"six_label_average_checks":64*6,
        "optimizer_calls":0,"game_point_reads":0,"Main_program_imports_or_executions":0,
        "source_hashes_stable":True,"Main_json_coefficients_and_penalty_tables_match":True,
        "arithmetic":"standard-library fractions.Fraction",
        "verifier_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "scope":"Universal averaged-six-menu inequality with explicit penalty; separate theta=1/6 cone optimum and exact optimal face. No real-SPE sharpness claim."}
dump("audit_result.json",output)
print(json.dumps(output,ensure_ascii=False,indent=2))
