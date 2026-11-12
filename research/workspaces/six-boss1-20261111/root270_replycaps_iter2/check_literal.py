#!/usr/bin/env python3
"""Independent true-budget and whole-parameter verification, standard library only."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib
import json
import os

P=Path(__file__).resolve().parent
REPO=Path(os.environ.get("ROOT270_SOURCE_REPO","/workspace/scratch/b0fef5ec503f/co-work-anl-boss1"))
H=list(product((0,1),repeat=7))
TAILS=list(product((0,1),repeat=3))


def read(name):return json.loads((P/name).read_text())
def enc(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,dict):return {str(k):enc(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [enc(v) for v in x]
    return x
def save(name,x):(P/name).write_text(json.dumps(enc(x),ensure_ascii=False,indent=2)+"\n")


def source_check():
    for item in read("source_pins.json")["sources"]:
        assert hashlib.sha256((REPO/item["path"]).read_bytes()).hexdigest()==item["sha256"]


def literal_cost(h,q,tail):
    c,b2,b3,b4,b5,b6,o=h
    r,y,z=tail
    b=c+b2
    end=1+b+q+r+y
    pair=1+b+q+r
    terms=[126000*Q(q,b+1+r+y+z)]
    terms.extend(weight*Q(bit,b+b3+3) for weight,bit in zip((43,31218,34458),tail))
    terms.extend(1654*Q(bit,b+b3+b4+b5+1) for bit in tail)
    terms.append(-5400*(Q(z,end)-Q(o,6*end)))
    terms.append(-7740*(Q(y,pair+z)+Q(z,pair+y)+Q(y,pair*(pair+1))-Q(o,3*pair)))
    terms.append(Q(215,3)*r)
    assert len(terms)==10
    return sum(terms,Q(0))


def p25_cost(h,tail):
    p=sum(h[:3]);t=h[5];r,z=tail;o=h[6];load=p+t+r+z
    source=25*Q(t,load) if load else Q(0)
    last=Q(z,load) if load else Q(0)
    return source-last+Q(r,2)+z+Q(o,6*(p+t+r+1))


def make_rows(h,m,pm):
    n=sum(h[:6])
    shares=[Q(bit,n) if n else Q(0) for bit in h[:6]]
    D=1+sum(h[:4])
    return [-shares[0]]+[-Q(x) for x in h[1:6]]+[
        shares[5]-Q(h[6],6*(sum(h[:5])+1)),
        shares[4]+shares[5]+Q(h[4],D*(D+1))-Q(h[6],3*D),
        126000*shares[2]+65719*shares[3]+4962*shares[5]-m,
        25*shares[3]-pm,
    ]


def linear_structures(rows):
    def totals(masses):
        sums=[sum((mass*H[h][j] for h,mass in masses.items()),Q(0)) for j in range(7)]
        profits=[sum((mass*Q(H[h][j],sum(H[h][:6])) for h,mass in masses.items() if sum(H[h][:6])),Q(0)) for j in range(6)]
        safe=sum((mass*rows[h][6] for h,mass in masses.items()),Q(0))
        pair=sum((mass*rows[h][7] for h,mass in masses.items()),Q(0))
        return sums,profits,safe,pair
    # Compare exact coefficients of three formal independent mass symbols.
    old_basis=[{102:Q(1),17:Q(1),9:Q(1)},{123:Q(1),5:Q(1)},{0:Q(1)}]
    for j,masses in enumerate(old_basis):
        sizes,profit,safe,pair=totals(masses)
        K=Q(j<2)
        assert sizes[:6]==[K]*6 and sizes[6]==2*K
        assert profit[0]==[Q(1,4),Q(1,5),Q(0)][j]
    endpoint_basis=[{123:Q(1),5:Q(1)},{1:Q(1)},{0:Q(1)}]
    coefficients=[]
    for j,masses in enumerate(endpoint_basis):
        sizes,profits,safe,pair=totals(masses)
        K=Q(j==0);X=Q(j==1)
        assert sizes[:6]==[K]*6 and sizes[6]==2*K+X
        assert profits[0]==K/5 and profits[4]==K and profits[5]==K/5
        assert safe==K/12-X/6
        assert pair==Q(13,10)*K-X/3
        assert pair-2*safe==Q(17,15)*K
        coefficients.append({"basis_symbol":["K","X","N"][j],"SAFE6":safe,"PAIR30":pair,"PAIR30_minus_2_SAFE6":pair-2*safe})
    save("literal_equality_structures.json",{
        "method":"formal linear coefficient comparison, not a feasible-point test",
        "old_A_E_N_structure":True,"new_K_X_N_structure":True,
        "endpoint_coefficients":coefficients,
        "h0_is_only_uncovered_by_recorded_labels":True,
        "extra_uniform_gap_from_endpoint_obstruction_claimed":False,
    })


def main():
    source_check()
    family=read("parameter_family.json")
    a1=Q(family["old_K_coefficient"]);a2=Q(family["new_K_coefficient"])
    b=Q(family["O_coefficient"]);eta=Q(family["eta"]);g=Q(family["g"])
    tstar=Q(family["t_star"]);sstar=Q(family["s_star"])
    base=list(map(Q,family["normalized_weights_constant"]))
    slope=list(map(Q,family["normalized_weights_slope"]))
    bc0=Q(family["C_equality_constant"]);bcs=Q(family["C_equality_slope"])
    assert g==Q(1,5)-a1-2*b>0 and Q(1,20)>eta
    assert b>eta and b<Q(1,30) and 2*b-Q(1,30)-eta<0
    assert sstar==tstar/(1+tstar)
    raw=read("true_state_tables.json")["all128_types"]
    stored={x["h"]:x for x in raw}
    dirs={x["h"]:x for x in read("direction_certificate.json")["all128"]}
    allrows={};rho={};directions={};newrho={};tailcount=0;menuchecks=0
    coefficient_checks=[]
    for code,h in enumerate(H):
        aq=[];weak=[]
        for q in(0,1):
            vals=[literal_cost(h,q,t) for t in TAILS]
            lo=min(vals);aq.append(lo)
            weak.append([list(t) for t,value in zip(TAILS,vals) if value==lo])
            assert vals==list(map(Q,stored[code]["C30_all_costs_by_q"][q]))
            tailcount+=8
        assert aq[1]>aq[0] and weak==stored[code]["C30_all_attaining_tails"]
        m=min(aq[0]+Q(h[6],6)*(aq[1]-aq[0]),aq[h[6]])
        assert m==Q(stored[code]["C30_CAP_m"])
        for menu in product((0,1),repeat=6):
            if bool(sum(menu))!=bool(h[6]):continue
            actual_min_average=sum((aq[q] for q in menu),Q(0))/6
            assert actual_min_average-m==Q(sum(menu)-h[6],6)*(aq[1]-aq[0])>=0
            menuchecks+=1
        ptails=list(product((0,1),repeat=2))
        pvals=[p25_cost(h,t) for t in ptails];pm=min(pvals)
        assert pvals==list(map(Q,stored[code]["P25_all_costs"]))
        assert [list(t) for t,v in zip(ptails,pvals) if v==pm]==stored[code]["P25_all_attaining_tails"]
        r=make_rows(h,m,pm);allrows[code]=r
        assert r==list(map(Q,stored[code]["ten_real_budget_customer_coefficients"]))
        residue=-sum((w*x for w,x in zip(base,r)),Q(0))-bc0*h[0]-b*h[6]-eta*h[0]*(1-h[6])
        assert residue==Q(dirs[code]["baseline_rho"])>=0
        # Independent trial identity: root IC and five caps weighted b.
        trial=[Q(1)]+[b]*5+[Q(0)]*4
        trialbc=Q(1,5)+3*b
        D=-sum((w*x for w,x in zip(trial,r)),Q(0))-trialbc*h[0]-b*h[6]-eta*h[0]*(1-h[6])
        assert D==Q(dirs[code]["direction_D"])
        L=sum(h[:6]);c=h[0];o=h[6]
        grouped=b*(L-o) if not c else Q(1,L)-Q(1,5)+b*(L-4-o)-eta*(1-o)
        assert D==grouped
        rho[code]=residue;directions[code]=D
        newrho[code]=(1-sstar)*residue+sstar*D
        assert newrho[code]==Q(dirs[code]["endpoint_rho"])>=0
        # Every customer column: compare constant and s coefficient literally.
        left=[-eta*c*(1-o),Q(0)]
        right=[sum(w*x for w,x in zip(base,r))+residue+bc0*c+b*o,
               sum(w*x for w,x in zip(slope,r))+D-residue+bcs*c]
        assert left==right
        coefficient_checks.append({"column":code,"constant":left[0],"slope":left[1],"all_coefficients_equal":True})
    negative=[h for h in range(128) if directions[h]<0]
    assert negative==[1,126,127]
    ratios={h:rho[h]/(-directions[h]) for h in negative}
    assert ratios[1]==tstar and ratios[126]>tstar and ratios[127]>tstar
    assert ratios[126]==Q(3412570310216371,1055010791163814)
    assert ratios[127]==Q(308367029847757,225245614125411)
    for L in range(1,6):
        assert b-Q(1,L*(L+1))<0
    oldzeros=[h for h in range(128) if rho[h]==0]
    newzeros=[h for h in range(128) if newrho[h]==0]
    assert oldzeros==[0,3,5,9,17,102,123]
    assert newzeros==[0,1,3,5,9,17,123]
    assert [h for h in oldzeros if directions[h]==0]==[0,3,5,9,17,123]
    linear_structures(allrows)
    Kweights=[Q(0)]+[Q(1)]*5+[Q(0),Q(0),Q(215,3),Q(3,2)]
    lefts=[[Q(1),Q(0)],[-a1,-g],[-b,Q(0)]]
    rights=[[base[0],slope[0]],
            [sum(w*x for w,x in zip(base,Kweights))-bc0,sum(w*x for w,x in zip(slope,Kweights))-bcs],
            [-b,Q(0)]]
    assert lefts==rights
    assert all(x+sstar*y>0 for x,y in zip(base,slope))
    # Complete domain: all D>=0 rows are convex combinations of nonnegative
    # endpoints; only the three explicitly negative rows provide upper bounds.
    assert 0<sstar<1
    visible=read("ROOT270_REPLY_CAP_REWEIGHTED.json")
    for col,atom in enumerate(list(product((0,1),repeat=9))+[None]):
        if atom is None:want=-a2
        else:
            income=Q(atom[0],sum(atom[:6])) if sum(atom[:6]) else Q(0)
            want=income-b*atom[7]-eta*atom[8]*(1-atom[7])
        assert want==Q(visible["a"][str(col)])
    assert a2==a1+sstar*g
    assert a2-a1==Q(13706626228836464340271835,190030779274772432897519093712)
    save("literal_all131_checks.json",{
        "customer_columns":coefficient_checks,"u_K_O_constant_and_slope":lefts,
        "all_scalar_coefficient_identities":262,"whole_parameter_identity":True,
    })
    source_check()
    result={
        "status":"PASS_INDEPENDENT_LITERAL_REWEIGHTING",
        "actual_agent_id":"/root/high_lambda_closure","optimizer_calls":0,
        "independent_of_generator_imports":True,"global_candidate_inputs":0,
        "C30_CAP_all_true_costs":tailcount,"P25_all_true_costs":512,
        "all_physical_menu_checks":menuchecks,"all128_direction_signs":128,
        "only_three_upper_bound_types":negative,"exact_t_bounds":ratios,
        "complete_t_domain":[0,tstar],"complete_s_domain":[0,sstar],
        "all131_scalar_coefficients":262,"all513_visible_columns":513,
        "new_K_gain":a2-a1,"baseline_zero_types":oldzeros,"endpoint_zero_types":newzeros,
        "endpoint_SAFE_PAIR_obstruction_verified":True,
        "no_additional_uniform_gain_claimed_from_endpoint_obstruction":True,
        "sources_unchanged":True,"no_new_true_budget_added":True,
    }
    save("literal_checker_output.json",result)
    print(json.dumps(enc(result),ensure_ascii=False,indent=2))


if __name__=="__main__":main()
