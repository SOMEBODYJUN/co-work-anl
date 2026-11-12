#!/usr/bin/env python3
"""Independent literal reconstruction; no imports from the generator/project."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib
import json
import os

P=Path(__file__).resolve().parent
REPO=Path(os.environ.get("ROOT270_SOURCE_REPO","/workspace/scratch/b0fef5ec503f/co-work-anl-boss1"))
H=list(product((0,1),repeat=7))
T=list(product((0,1),repeat=3))


def read(name):return json.loads((P/name).read_text())
def cv(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,dict):return {str(k):cv(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [cv(v) for v in x]
    return x
def save(name,x):(P/name).write_text(json.dumps(cv(x),ensure_ascii=False,indent=2)+"\n")


def check_sources():
    for item in read("source_pins.json")["sources"]:
        assert hashlib.sha256((REPO/item["path"]).read_bytes()).hexdigest()==item["sha256"]


def costs_by_true_budgets(h,q,tail,epsilon=Q(0)):
    c,b2,b3,b4,b5,b6,o=h
    r,y,z=tail
    prefix2=c+b2
    old4=prefix2+b3+3
    old6=prefix2+b3+b4+b5+1
    new4prefix=prefix2+q
    before5=1+new4prefix+r
    new6prefix=before5+y
    # Cost of each of the nine true nonnegative budgets, then the new CAP.
    terms=[126000*Q(q,prefix2+1+r+y+z)]
    terms += [weight*Q(bit,old4) for weight,bit in zip([43,31218,34458],tail)]
    terms += [1654*Q(bit,old6) for bit in tail]
    end_slack=Q(z,new6prefix)-Q(o,6*new6prefix)
    pair_slack=Q(y,before5+z)+Q(z,before5+y)+Q(y,before5*(before5+1))-Q(o,3*before5)
    terms += [-5400*end_slack,-7740*pair_slack]
    assert len(terms)==9
    return sum(terms,Q(0))+epsilon*r


def minimum(h,epsilon):
    aq=[];weak=[]
    for q in (0,1):
        values=[costs_by_true_budgets(h,q,t,epsilon) for t in T]
        low=min(values);aq.append(low)
        weak.append([t for t,v in zip(T,values) if v==low])
    moment=min(aq[0]+Q(h[6],6)*(aq[1]-aq[0]),aq[h[6]])
    return moment,aq,weak


def p25_literal(h):
    prefix=sum(h[:3]);target=h[5];o=h[6]
    values=[]
    for middle,last in product((0,1),repeat=2):
        den=prefix+target+middle+last
        source=Q(25*target,den) if den else Q(0)
        last_actual=Q(last,den) if den else Q(0)
        middle_cap=Q(middle,2)
        last_cap=Q(last)
        terminal_query=Q(o,6*(prefix+target+middle+1))
        values.append((source-last_actual+middle_cap+last_cap+terminal_query,(middle,last)))
    low=min(x for x,_ in values)
    weak=[t for value,t in values if value==low]
    assert all(t[0]==target for t in weak)
    return low,weak


def true_rows(h,m):
    L=sum(h[:6]);v=[Q(x,L) if L else Q(0) for x in h[:6]]
    D=1+sum(h[:4])
    return [-v[0]]+[-Q(x) for x in h[1:6]]+[
        v[5]-Q(h[6],6*(sum(h[:5])+1)),
        v[4]+v[5]+Q(h[4],D*(D+1))-Q(h[6],3*D),
        126000*v[2]+65719*v[3]+4962*v[5]-m,
        25*v[3]-p25_literal(h)[0],
    ]


def equality_linear_identity(types):
    # Each list is a literal vector of coefficients of A,B,C*,D*,E*,F*,X,N.
    zero=[Q(0)]*8
    def unit(j):
        a=zero.copy();a[j]=Q(1);return a
    def plus(*args):return [sum(xs,Q(0)) for xs in zip(*args)]
    A,B,C,D,E,F,X,N=[unit(j) for j in range(8)]
    masses={h:zero.copy() for h in range(128)}
    for h,v in [(102,A),(103,B),(115,C),(121,D),(123,E),(125,F),(1,X),(0,N)]:
        masses[h]=v
    masses[17]=plus(A,B);masses[9]=plus(A,B,C)
    masses[5]=plus(C,D,E);masses[3]=plus(D,F)
    K=plus(A,B,C,D,E,F)
    for j in range(6):
        got=[sum((masses[h][a]*H[h][j] for h in range(128)),Q(0)) for a in range(8)]
        assert got==K
    rbar={}
    for h in types:
        _,_,weak=minimum(H[h],Q(0))
        by_q=[]
        for tails in weak:
            bits={t[0] for t in tails};assert len(bits)==1
            by_q.append(next(iter(bits)))
        rbar[h]=Q(by_q[0])+Q(H[h][6],6)*(by_q[1]-by_q[0])
    got=[sum((masses[h][a]*rbar.get(h,Q(0)) for h in range(128)),Q(0)) for a in range(8)]
    want=[Q(7,6)*K[a]+X[a]+B[a]/6+C[a]+D[a]+Q(5,6)*F[a] for a in range(8)]
    assert got==want
    save("literal_equality_identity.json",{
        "symbols":["A","B","Cstar","Dstar","Estar","Fstar","X","N"],
        "all_six_true_sizes_equal_K":True,"average_true_R4_coefficients":got,
        "claimed_average_size_coefficients":want,"coefficient_difference":[0]*8,
        "strict_equality_contradiction_for_K_positive":"average |R4k| >= 7K/6 while each legal R4k has size <= K",
    })


def main():
    check_sources()
    data=read("inputs.json")
    names=list(data["original_weights"]);W=[Q(data["original_weights"][n]) for n in names]
    expected=[67510295447690880,622403086173831,3736778489617071,3696167188982850,3608286607200810,3553563630176244,1712829042623520,2292281651099340,24602518440,61096128288912]
    assert W==list(map(Q,expected))
    DB=Q(data["DB"]);bc=Q(data["beta_C"]);bo=Q(data["beta_O"])
    eta=Q(data["eta"]);oldak=Q(data["original_K_coefficient"]);ob=Q(data["O_coefficient"]);ep=Q(data["epsilon_endpoint"])
    base=read("all2048_C30_base_states.json")
    assert len(base)==2048
    for state in base:
        assert costs_by_true_budgets(H[state["h"]],state["q"],tuple(state["tail"]))==Q(state["cost"])
    events={};minima_r={}
    for code,h in enumerate(H):
        for q in (0,1):
            a=[min(costs_by_true_budgets(h,q,(r,y,t)) for y,t in product((0,1),repeat=2)) for r in (0,1)]
            minima_r[code,q]=a
            change=a[0]-a[1]
            if 0<change<=ep:events.setdefault(change,[]).append([code,q])
    breaks=[Q(0)]+sorted(events)
    assert breaks==list(map(Q,read("epsilon_envelopes.json")["complete_breakpoints"]))
    assert breaks==[Q(0),Q(43,6),Q(215,12),Q(301,15),Q(215,3)]
    all_envelopes={(Q(x["epsilon"]),x["h"]):x for x in read("epsilon_envelopes.json")["all_endpoint_envelopes"]}
    residuals={(Q(x["epsilon"]),x["h"]):x for x in read("all128_root_remainders.json")["all_parameter_endpoints"]}
    oldrho={};strict={}
    for code,h in enumerate(H):
        m,_,_=minimum(h,Q(0))
        oldrho[code]=(-sum(w*a for w,a in zip(W,true_rows(h,m)))-bc*h[0]-bo*h[6])/DB
        assert oldrho[code]>=0
        strict[code]=oldrho[code]-eta*h[0]*(1-h[6]);assert strict[code]>=0
    assert min(oldrho[h] for h in range(128) if H[h][0] and not H[h][6])==eta
    original_zeros=[h for h in range(128) if oldrho[h]==0]
    strict_zeros=[h for h in range(128) if strict[h]==0]
    assert original_zeros==[0,1,3,5,9,17,33,103,115,121,123,125]
    assert strict_zeros==[0,1,3,5,9,17,33,102,103,115,121,123,125]
    equality_linear_identity(strict_zeros)
    physical_menu_checks=0;tail_checks=0;column131=0;all_zero={};slope_min=[]
    for epsilon in breaks:
        paid=W.copy()
        for index,kappa in [(2,Q(1,6)),(3,Q(1)),(4,Q(1)),(5,Q(1))]:paid[index]-=W[8]*epsilon*kappa
        assert all(w>0 for w in paid)
        newbc=bc-2*W[8]*epsilon;newak=oldak+W[8]*epsilon/(6*DB)
        zeros=[]
        for code,h in enumerate(H):
            m,aq,weak=minimum(h,epsilon)
            known=all_envelopes[epsilon,code]
            assert [Q(known["a0"]),Q(known["a1"])]==aq and Q(known["m"])==m
            assert known["all_attaining_tails_by_q"]==[[list(t) for t in tails] for tails in weak]
            assert aq[1]>aq[0];slope_min.append(aq[1]-aq[0])
            for q in (0,1):
                for tail in T:
                    assert costs_by_true_budgets(h,q,tail,epsilon)>=aq[q]
                    tail_checks+=1
            for menu in product((0,1),repeat=6):
                if bool(sum(menu))!=bool(h[6]):continue
                exact_min_average=sum((aq[q] for q in menu),Q(0))/6
                assert exact_min_average-m==Q(sum(menu)-h[6],6)*(aq[1]-aq[0])>=0
                physical_menu_checks+=1
            rows=true_rows(h,m)
            remainder=(-sum(w*a for w,a in zip(paid,rows))-newbc*h[0]-bo*h[6])/DB-eta*h[0]*(1-h[6])
            assert remainder>=0
            if remainder==0:zeros.append(code)
            assert remainder==Q(residuals[epsilon,code]["new_rho"])
            rhs=sum((w*a/DB for w,a in zip(paid,rows)),Q(0))+remainder+newbc*h[0]/DB+bo*h[6]/DB
            assert rhs==-eta*h[0]*(1-h[6]);column131+=1
        assert paid[0]/DB==1
        assert (sum(paid[1:6])+Q(3,2)*paid[9]+epsilon*paid[8]-newbc)/DB==-newak
        assert -bo/DB==-ob
        column131+=3;all_zero[str(epsilon)]=zeros
    # h=3 certifies the first upper obstruction of this fixed root payment.
    r0,r1=minima_r[3,0];q1r0,q1r1=minima_r[3,1]
    assert r0-r1==ep and q1r0-q1r1==Q(20855,3)
    originalm=minimum(H[3],Q(0))[0]
    postm_constant=Q(5,6)*r0+Q(1,6)*q1r1
    postm_slope=Q(1,6)
    assert postm_constant-originalm==Q(5,6)*ep
    assert postm_slope-1==-Q(5,6)
    # All PAIR30 menu weakenings, including empty and repeated-index patterns.
    pair_checks=0
    for D in range(1,6):
        for menu in product((0,1),repeat=6):
            d=sum(menu);o=int(d>0)
            exact=sum((Q(menu[k]+menu[l],D)-Q(menu[k]*menu[l],D*(D+1)) for k in range(6) for l in range(6) if l!=k),Q(0))/30
            assert exact==Q(d,3*D)-Q(d*(d-1),30*D*(D+1))
            assert exact-Q(o,3*D)>=0
            assert (exact-Q(o,3*D)==0)==(d in (0,1))
            pair_checks+=1
    p25known={x["h"]:x for x in read("equality_structure.json")["all128_P25_weak_tables"]}
    for code,h in enumerate(H):
        lo,weak=p25_literal(h)
        assert lo==Q(p25known[code]["minimum"])
        assert [list(x) for x in weak]==p25known[code]["all_attaining_tails"]
    newrow=read("ROOT270_C30_R4_CAP_STRICT.json")
    delta=W[8]*ep/(6*DB);newak=oldak+delta
    for col,atom in enumerate(list(product((0,1),repeat=9))+[None]):
        if atom is None:want=-newak
        else:
            u=Q(atom[0],sum(atom[:6])) if sum(atom[:6]) else Q(0)
            want=u-ob*atom[7]-eta*atom[8]*(1-atom[7])
        assert want==Q(newrow["a"][str(col)])
    assert delta==Q(14693170735,3375514772384544)
    assert newak*84387869309613600==8839887370271285
    assert ob*84387869309613600==1686700906360065
    assert eta*84387869309613600==1087978231314917
    check_sources()
    result={
        "status":"PASS_INDEPENDENT_LITERAL_TRUE_HISTORY_ROOT_CAP_COMPLETION",
        "actual_agent_id":"/root/high_lambda_closure","independent_of_generator_imports":True,
        "optimizer_calls":0,"global_candidate_or_optimal_face_inputs":0,
        "nine_budget_base_costs":2048,"complete_epsilon_breakpoints":breaks,
        "all_endpoint_true_tail_costs":tail_checks,"all_physical_menu_checks":physical_menu_checks,
        "all_PAIR30_index_checks":pair_checks,"P25_full_types":128,
        "full_131_column_identities":column131,"full_visible_columns":513,
        "old_original_zero_types":original_zeros,"old_strict_zero_types":strict_zeros,
        "new_zero_types":all_zero[str(ep)],"minimum_new_moment_slope_over_all_cells":min(slope_min),
        "fixed_payment_first_upper_obstruction":ep,"global_first_C30_envelope_breakpoint":Q(43,6),
        "uniform_K_gain":delta,"strict_equality_requires_K_zero":True,
        "sources_unchanged":True,"full_SPE_construction_claimed":False,
    }
    save("literal_checker_output.json",result)
    print(json.dumps(cv(result),ensure_ascii=False,indent=2))


if __name__=="__main__":main()
