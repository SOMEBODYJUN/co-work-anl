#!/usr/bin/env python3
"""Complete one-parameter reweighting of existing true ROOT270 reply-cap budgets."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import os

P=Path(__file__).resolve().parent
REPO=Path(os.environ.get("ROOT270_SOURCE_REPO","/workspace/scratch/b0fef5ec503f/co-work-anl-boss1"))
OLD=REPO/"research/workspaces/six-boss1-20261111/root270_reply_cap"
H=list(product((0,1),repeat=7))
TAILS=list(product((0,1),repeat=3))
DB=F(67510295447690880)
W=list(map(F,[67510295447690880,622403086173831,3736484626202371,3694404008494650,3606523426712610,3551800449688044,1712829042623520,2292281651099340,24602518440,61096128288912]))
NAMES=["ROOT_IC","CAP_B2","CAP_B3","CAP_B4","CAP_B5","CAP_B6","SAFE6_OMEAN","PAIR30","C30_CAP_R4","P25_4_B6_OMEAN"]
BC=F(22376932866410102)
BO=F(1349360725088052)
EPS=F(215,3)
A1=F(1767977474054257,16877573861922720)
B=F(37482242363557,1875285984658080)
ETA=F(1087978231314917,84387869309613600)
G=F(1,5)-A1-2*B
TSTAR=F(146931707350,112446727090671)
SSTAR=TSTAR/(1+TSTAR)
SOURCE_PATHS=[
 "archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md",
 "archives/customer-attraction/state/引理/六标签真实第三源重查询与根收益投影--引理.md",
 "research/workspaces/six-boss1-20261111/root270_reply_cap/proof.md",
 "research/workspaces/six-boss1-20261111/root270_reply_cap/ROOT270_C30_R4_CAP_STRICT.json",
 "research/workspaces/six-boss1-20261111/root270_reply_cap/all128_root_remainders.json",
 "research/workspaces/six-boss1-20261111/root270_reply_cap/all131_payments.json",
 "research/workspaces/six-boss1-20261111/root270_reply_cap/freeze_manifest.json",
]


def enc(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):enc(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [enc(v) for v in x]
    return x
def save(name,x):(P/name).write_text(json.dumps(enc(x),ensure_ascii=False,indent=2)+"\n")
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def pins():
    current=[{"path":x,"sha256":sha(REPO/x)} for x in SOURCE_PATHS]
    if (P/"source_pins.json").exists():assert json.loads((P/"source_pins.json").read_text())["sources"]==current
    else:save("source_pins.json",{"sources":current,"scope":"local proved budgets and frozen complete coefficients only; no global candidate or optimal face inputs"})
    return current


def phi(h,q,r,y,z):
    c,b2,b3,b4,b5,b6,o=h;s=c+b2;D=1+s+q+r
    return F(126000*q,s+1+r+y+z)+F(43*r+31218*y+34458*z,s+b3+3)+F(1654*(r+y+z),s+b3+b4+b5+1)+5400*F(F(o,6)-z,D+y)+7740*(F(o,3*D)-F(y,D+z)-F(z,D+y)-F(y,D*(D+1)))+EPS*r


def c30(h):
    aq=[];weak=[];costs=[]
    for q in(0,1):
        vals=[phi(h,q,*tail) for tail in TAILS];lo=min(vals)
        aq.append(lo);weak.append([tail for value,tail in zip(vals,TAILS) if value==lo]);costs.append(vals)
    assert aq[1]>aq[0]
    return aq[0]+F(h[6],6)*(aq[1]-aq[0]),aq,weak,costs


def p25(h):
    p=sum(h[:3]);target=h[5];q=F(h[6],6);costs=[]
    for r,z in product((0,1),repeat=2):
        load=p+target+r+z
        first=F(25*target-z,load) if load else F(0)
        costs.append(first+F(r,2)+z+q/(p+target+r+1))
    lo=min(costs)
    return lo,[tail for value,tail in zip(costs,product((0,1),repeat=2)) if value==lo],costs


def rows(h,m,p25m):
    L=sum(h[:6]);v=[F(z,L) if L else F(0) for z in h[:6]]
    D=1+sum(h[:4])
    return [-v[0]]+[-F(x) for x in h[1:6]]+[
        v[5]-F(h[6],6*(sum(h[:5])+1)),
        v[4]+v[5]+F(h[4],D*(D+1))-F(h[6],3*D),
        126000*v[2]+65719*v[3]+4962*v[5]-m,
        25*v[3]-p25m,
    ]


def direction(h):
    c=h[0];o=h[6];L=sum(h[:6])
    v=F(c,L) if L else F(0)
    return v-(F(1,5)+3*B)*c-B*o-ETA*c*(1-o)+B*sum(h[1:6])


def family_coefficients():
    base=[w/DB for w in W]
    slope=[F(0)]+[B-base[j] for j in range(1,6)]+[-base[j] for j in range(6,10)]
    bc0=BC/DB;bcs=F(1,5)+3*B-bc0
    assert base[0]==1 and all(base[j]+SSTAR*slope[j]>0 for j in range(10))
    return base,slope,bc0,bcs


def main():
    sources=pins()
    assert G==F(932856935786261,16877573861922720)>0
    assert F(1,20)>ETA and B>ETA and B<F(1,30) and 2*B-F(1,30)-ETA<0
    oldrho={x["h"]:F(x["new_rho"]) for x in json.loads((OLD/"all128_root_remainders.json").read_text())["all_parameter_endpoints"] if F(x["epsilon"])==EPS}
    base,slope,bc0,bcs=family_coefficients()
    states=[];cert=[];columns=[];oldzero=[];newzero=[];negative=[]
    for code,h in enumerate(H):
        m,aq,weak,costs=c30(h);pm,pweak,pcosts=p25(h);row=rows(h,m,pm)
        rho=-sum(w*x for w,x in zip(base,row))-bc0*h[0]-B*h[6]-ETA*h[0]*(1-h[6])
        assert rho==oldrho[code]>=0
        D=direction(h)
        end=(1-SSTAR)*rho+SSTAR*D
        assert end>=0
        if rho==0:oldzero.append(code)
        if end==0:newzero.append(code)
        ratio=rho/(-D) if D<0 else None
        if D<0:negative.append((code,ratio))
        const=sum(w*x for w,x in zip(base,row))+rho+bc0*h[0]+B*h[6]
        deriv=sum(w*x for w,x in zip(slope,row))+D-rho+bcs*h[0]
        assert const==-ETA*h[0]*(1-h[6]) and deriv==0
        columns.append({"column":code,"left_constant":-ETA*h[0]*(1-h[6]),"right_constant":const,"left_slope":0,"right_slope":deriv})
        states.append({"h":code,"bits":h,"C30_CAP_m":m,"C30_a0_a1":aq,"C30_all_costs_by_q":costs,"C30_all_attaining_tails":weak,"P25_min":pm,"P25_all_costs":pcosts,"P25_all_attaining_tails":pweak,"ten_real_budget_customer_coefficients":row})
        cert.append({"h":code,"bits":h,"baseline_rho":rho,"direction_D":D,"endpoint_rho":end,"t_upper_bound_if_negative":ratio})
    assert oldzero==[0,3,5,9,17,102,123]
    assert newzero==[0,1,3,5,9,17,123]
    assert [x[0] for x in negative]==[1,126,127] and min(ratio for _,ratio in negative)==TSTAR
    # All independent u,K,O columns, as constant-plus-slope identities in s.
    cap_k=[F(0)]+[F(1)]*5+[F(0),F(0),EPS,F(3,2)]
    for col,left0,left1,right0,right1 in [
        ("actual_u1",F(1),F(0),base[0],slope[0]),
        ("independent_K",-A1,-G,sum(w*x for w,x in zip(base,cap_k))-bc0,sum(w*x for w,x in zip(slope,cap_k))-bcs),
        ("independent_O",-B,F(0),-B,F(0)),
    ]:
        assert (left0,left1)==(right0,right1)
        columns.append({"column":col,"left_constant":left0,"right_constant":right0,"left_slope":left1,"right_slope":right1})
    delta=SSTAR*G;a2=A1+delta
    assert delta==F(13706626228836464340271835,190030779274772432897519093712)
    assert a2==F(66400039579513467522586981249,633435930915908109658396979040)
    visible={};visible_checks=[];prior=json.loads((OLD/"ROOT270_C30_R4_CAP_STRICT.json").read_text())
    for col,atom in enumerate(list(product((0,1),repeat=9))+[None]):
        if atom is None:constant=-A1;derivative=-G
        else:
            load=sum(atom[:6]);actual=F(atom[0],load) if load else F(0)
            constant=actual-B*atom[7]-ETA*atom[8]*(1-atom[7]);derivative=F(0)
        assert constant==F(prior["a"][str(col)])
        value=constant+SSTAR*derivative
        visible[str(col)]=value
        visible_checks.append({"column":col,"baseline":constant,"whole_family_slope":derivative,"new_value":value,"difference_from_prior":SSTAR*derivative})
    save("ROOT270_REPLY_CAP_REWEIGHTED.json",{
        "name":"ROOT270_REPLY_CAP_REWEIGHTED","family":"EXISTING_TRUE_REPLY_CAP_BUDGET_REWEIGHTING",
        "a":visible,"rhs":"0","numerical_divisor":"1","variables":513,"independent_K_column":512,
        "bit_order":["a1","a2","a3","a4","a5","a6","x","o","c"],
        "K_coefficient":a2,"O_coefficient":B,"C_outside_coefficient":ETA,
        "K_gain_over_reply_cap":delta,"t_parameter":TSTAR,"s_parameter":SSTAR,
        "new_true_budgets_added":False,"all_513_columns_preserved":True,
        "model":"Every complete ordered-history pure SPE in the six-player finite nonempty labelled common-catalogue model; C genuine maximum size; O any six legal query union.",
    })
    save("true_state_tables.json",{"all128_types":states,"all_weak_ties_retained":True})
    save("direction_certificate.json",{
        "formula":"D=c/L-(1/5+3b)c-bo-eta*c*(1-o)+b*(b2+b3+b4+b5+b6), with c/L=0 at zero load",
        "all128":cert,"only_negative_types":negative,
        "t_interval":[0,TSTAR],"s_interval":[0,SSTAR],
        "complete_domain_for_this_fixed_reweighting":True,
        "baseline_zero_types":oldzero,"endpoint_zero_types":newzero,
    })
    save("parameter_family.json",{
        "actual_agent_id":"/root/high_lambda_closure","run":"six-boss1-20261111",
        "old_K_coefficient":A1,"new_K_coefficient":a2,"O_coefficient":B,"eta":ETA,
        "g":G,"t_star":TSTAR,"s_star":SSTAR,"new_K_gain":delta,
        "s_definition":"s=t/(1+t)","full_domain_s":[0,SSTAR],"full_domain_t":[0,TSTAR],
        "budgets":NAMES,"normalized_weights_constant":base,"normalized_weights_slope":slope,
        "normalized_weights_at_endpoint":[x+SSTAR*y for x,y in zip(base,slope)],
        "C_equality_constant":bc0,"C_equality_slope":bcs,"O_equality_constant":B,"O_equality_slope":0,
        "root_income_is_actual_u1_only":True,"epsilon_stays_fixed":EPS,
        "optimizer_calls":0,"new_CAP_or_SAFE_budgets_added":False,
    })
    save("all131_affine_column_identities.json",{"parameter":"s","all_columns":columns,"scalar_coefficient_checks":2*len(columns)})
    save("all513_affine_column_checks.json",visible_checks)
    save("equality_structures.json",{
        "old_seven_zero_types":oldzero,
        "old_CAP_structure":{"A":"w102","E":"w123","K":"A+E","w17":"A","w9":"A","w5":"E","w3":"0","O":"2K","branch_v1":"A/4+E/5"},
        "old_root_equality_gap":"A*(g+1/20-eta)+E*g",
        "endpoint_zero_types":newzero,
        "endpoint_CAP_structure":{"E":"w123=K","X":"w1","w5":"K","w3":"0","w9":"0","w17":"0","O":"X+2K","branch_v1":"K/5","branch_v5":"K","branch_v6":"K/5"},
        "endpoint_SAFE6_slack":"K/12-X/6","endpoint_PAIR30_slack":"13K/10-X/3",
        "endpoint_exact_gap_identity":"PAIR30-2*SAFE6=17K/15",
        "endpoint_equality_requires_K_zero":True,
        "next_specific_obligation":"A uniform reweighting exploiting PAIR30-2*SAFE6=17K/15 on the complete endpoint equality structure, while paying all 128 other types; no new uniform gap from this identity is claimed here.",
        "h0_scope":"C, B2,...,B6 and the chosen O do not cover h0; unlisted legal labels may cover it until K=0 is proved.",
    })
    assert sources==pins()
    result={
        "status":"PASS_COMPLETE_TRUE_BUDGET_REWEIGHTING",
        "actual_agent_id":"/root/high_lambda_closure","optimizer_calls":0,
        "all128_true_types":128,"C30_CAP_true_costs":2048,"P25_true_costs":512,
        "only_negative_direction_types":[1,126,127],"complete_t_upper_bound":TSTAR,
        "full131_affine_identities":131,"full131_scalar_coefficients":262,
        "full_visible_columns":513,"new_K_coefficient":a2,"new_K_gain":delta,
        "no_new_true_budget_added":True,"source_pins_unchanged":True,
        "baseline_zero_types":oldzero,"endpoint_zero_types":newzero,
        "global_welfare_combination_performed":False,
    }
    save("generator_output.json",result)
    print(json.dumps(enc(result),ensure_ascii=False,indent=2))


if __name__=="__main__":main()
