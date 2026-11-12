#!/usr/bin/env python3
"""ROOT270 equality and a true C30-branch capacity completion. No optimizer."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import os

HERE=Path(__file__).resolve().parent
REPO=Path(os.environ.get("ROOT270_SOURCE_REPO","/workspace/scratch/b0fef5ec503f/co-work-anl-boss1"))
WS=REPO/"research/workspaces/six-boss1-20261111"
STATES=list(product((0,1),repeat=7))
TAILS=list(product((0,1),repeat=3))
NAMES=["ROOT_IC","CAP_B2","CAP_B3","CAP_B4","CAP_B5","CAP_B6","SAFE6_OMEAN","PAIR30","C30_CAP_R4","P25_4_B6_OMEAN"]
WEIGHTS=list(map(F,[67510295447690880,622403086173831,3736778489617071,3696167188982850,3608286607200810,3553563630176244,1712829042623520,2292281651099340,24602518440,61096128288912]))
DB=WEIGHTS[0]
BC=F(22380459227386502)
BO=F(1349360725088052)
ETA=F(1087978231314917,84387869309613600)
AK=F(883952004100291,8438786930961360)
AO=F(37482242363557,1875285984658080)
EPS=F(215,3)
SOURCE_PATHS=[
 "archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md",
 "archives/customer-attraction/state/引理/六标签真实第三源重查询与根收益投影--引理.md",
 "research/workspaces/six-boss1-20261111/main_root270_strict_outside/proof.md",
 "research/workspaces/six-boss1-20261111/main_root270_strict_outside/ROOT270_STRICT_C_OUTSIDE.json",
]


def encode(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [encode(v) for v in x]
    return x


def save(name,value):
    (HERE/name).write_text(json.dumps(encode(value),ensure_ascii=False,indent=2)+"\n")


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def pins():
    current=[{"path":p,"sha256":sha(REPO/p)} for p in SOURCE_PATHS]
    p=HERE/"source_pins.json"
    if p.exists():assert json.loads(p.read_text())["sources"]==current
    else:save("source_pins.json",{"repo_override_environment":"ROOT270_SOURCE_REPO","sources":current,"no_global_candidate_or_optimal_face_file_is_an_input":True})
    return current


def phi(h,q,r,y,t):
    c,b2,b3,b4,b5,b6,o=h
    b=c+b2;D=1+b+q+r
    return (
        F(126000*q,b+1+r+y+t)
        +F(43*r+31218*y+34458*t,b+b3+3)
        +F(1654*(r+y+t),b+b3+b4+b5+1)
        +5400*F(F(o,6)-t,D+y)
        +7740*(F(o,3*D)-F(y,D+t)-F(t,D+y)-F(y,D*(D+1)))
    )


def envelope(h,epsilon):
    aq=[];weak=[];costs=[]
    for q in (0,1):
        values=[phi(h,q,*tail)+epsilon*tail[0] for tail in TAILS]
        lo=min(values)
        aq.append(lo)
        weak.append([tail for tail,value in zip(TAILS,values) if value==lo])
        costs.append(values)
    assert aq[1]>aq[0]
    return aq[0]+F(h[6],6)*(aq[1]-aq[0]),aq,weak,costs


def row_coefficients(h,m):
    c,b2,b3,b4,b5,b6,o=h
    load=sum(h[:6])
    v=[F(bit,load) if load else F(0) for bit in h[:6]]
    D=1+sum(h[:4]);p=sum(h[:3])
    return (
        [-v[0]]+[-F(bit) for bit in h[1:6]]
        +[v[5]-F(o,6*(sum(h[:5])+1)),
          v[4]+v[5]+F(b5,D*(D+1))-F(o,3*D),
          126000*v[2]+65719*v[3]+4962*v[5]-m,
          25*v[3]-(F(3,2)+F(24,p+3))*b6-F(o,6*(p+1+2*b6))]
    )


def outer_weights(epsilon):
    weights=WEIGHTS.copy()
    for index,kappa in ((2,F(1,6)),(3,F(1)),(4,F(1)),(5,F(1))):
        weights[index]-=WEIGHTS[8]*epsilon*kappa
    assert all(w>0 for w in weights)
    return weights,BC-2*WEIGHTS[8]*epsilon


def root_remainder(h,epsilon):
    m0,_,_,_=envelope(h,F(0))
    me,_,_,_=envelope(h,epsilon)
    original=row_coefficients(h,m0)
    oldrho=(-sum(w*a for w,a in zip(WEIGHTS,original))-BC*h[0]-BO*h[6])/DB
    strict=oldrho-ETA*h[0]*(1-h[6])
    weights,newbc=outer_weights(epsilon)
    changed=row_coefficients(h,me)
    newrho=(-sum(w*a for w,a in zip(weights,changed))-newbc*h[0]-BO*h[6])/DB-ETA*h[0]*(1-h[6])
    extra=(me-m0)+epsilon*(2*h[0]-F(h[2],6)-h[3]-h[4]-h[5])
    assert newrho==strict+WEIGHTS[8]*extra/DB
    assert strict>=0 and newrho>=0
    return oldrho,strict,newrho,extra


def p25(h):
    p=sum(h[:3]);t=h[5];q=F(h[6],6)
    vals=[]
    for r,z in product((0,1),repeat=2):
        den=p+t+r+z
        first=F(25*t-z,den) if den else F(0)
        vals.append((first+F(r,2)+z+q/(p+t+r+1),(r,z)))
    lo=min(x for x,_ in vals)
    want=(F(3,2)+F(24,p+3))*t+q/(p+1+2*t)
    assert lo==want
    return {"p":p,"target_B6":t,"q":q,"minimum":lo,"all_attaining_tails":[tail for value,tail in vals if value==lo],"all_costs":[value for value,_ in vals]}


def all131(epsilon):
    weights,newbc=outer_weights(epsilon)
    newa=AK+WEIGHTS[8]*epsilon/(6*DB)
    checks=[]
    for code,h in enumerate(STATES):
        m,_,_,_=envelope(h,epsilon)
        _,_,rho,_=root_remainder(h,epsilon)
        right=sum(w*a/DB for w,a in zip(weights,row_coefficients(h,m)))+rho+newbc*h[0]/DB+BO*h[6]/DB
        left=-ETA*h[0]*(1-h[6])
        assert left==right
        checks.append({"column":code,"kind":"true_branch_customer","left":left,"right":right,"difference":0})
    rightu=weights[0]/DB
    rightk=(sum(weights[1:6])+F(3,2)*weights[9]+epsilon*weights[8]-newbc)/DB
    righto=-BO/DB
    for label,left,right in [("actual_u1",F(1),rightu),("independent_K",-newa,rightk),("independent_O",-AO,righto)]:
        assert left==right
        checks.append({"column":label,"left":left,"right":right,"difference":0})
    return checks


def make_visible_row():
    increment=WEIGHTS[8]*EPS/(6*DB)
    ak=AK+increment
    old=json.loads((WS/"main_root270_strict_outside/ROOT270_STRICT_C_OUTSIDE.json").read_text())
    coefficients={};checks=[]
    for col,atom in enumerate(list(product((0,1),repeat=9))+[None]):
        if atom is None:want=-ak;delta=-increment
        else:
            load=sum(atom[:6])
            u=F(atom[0],load) if load else F(0)
            want=u-AO*atom[7]-ETA*atom[8]*(1-atom[7])
            delta=F(0)
        assert want==F(old["a"].get(str(col),"0"))+delta
        coefficients[str(col)]=want
        checks.append({"column":col,"coefficient":want,"new_minus_old":delta,"difference_from_expected":0})
    save("ROOT270_C30_R4_CAP_STRICT.json",{
        "name":"ROOT270_C30_R4_CAP_STRICT","family":"TRUE_ROOT_C30_BRANCH_CAP_COMPLETION",
        "a":coefficients,"rhs":"0","numerical_divisor":"1","variables":513,
        "bit_order":["a1","a2","a3","a4","a5","a6","x","o","c"],"independent_K_column":512,
        "epsilon":EPS,"K_increment":increment,"C_outside_remainder":ETA,
        "model":"Six unit players, finite unit customers, finite nonempty labelled common catalogue, every complete ordered-history pure SPE; C a true maximum-size legal label; O any six legal query union.",
        "all_513_columns_preserved":True,"actual_root_income_is_not_branch_income":True,
    })
    save("all513_column_checks.json",checks)
    return increment,ak


def main():
    source_pins=pins()
    epsilon_events={}
    fixed_r=[];base_states=[]
    for code,h in enumerate(STATES):
        for q in (0,1):
            by_r=[];weak_r=[]
            for r in (0,1):
                values=[(phi(h,q,r,y,t),(r,y,t)) for y,t in product((0,1),repeat=2)]
                lo=min(value for value,_ in values)
                by_r.append(lo);weak_r.append([tail for value,tail in values if value==lo])
            threshold=by_r[0]-by_r[1]
            fixed_r.append({"h":code,"bits":h,"q":q,"min_at_r0":by_r[0],"min_at_r1":by_r[1],"all_minimizers_at_each_r":weak_r,"r_switch_epsilon":threshold})
            if 0<threshold<=EPS:epsilon_events.setdefault(threshold,[]).append((code,q))
            for tail in TAILS:base_states.append({"h":code,"q":q,"tail":tail,"cost":phi(h,q,*tail)})
    breaks=[F(0)]+sorted(epsilon_events)
    assert breaks==[F(0),F(43,6),F(215,12),F(301,15),F(215,3)]
    remainder_rows=[];envelopes=[];payments=[];all_zeros={}
    for epsilon in breaks:
        zeros=[]
        for code,h in enumerate(STATES):
            m,aq,weak,costs=envelope(h,epsilon)
            oldrho,strict,nr,extra=root_remainder(h,epsilon)
            if nr==0:zeros.append(code)
            envelopes.append({"epsilon":epsilon,"h":code,"a0":aq[0],"a1":aq[1],"moment_slope":aq[1]-aq[0],"m":m,"all_attaining_tails_by_q":weak})
            remainder_rows.append({"epsilon":epsilon,"h":code,"bits":h,"original_normalized_rho":oldrho,"strict_old_rho":strict,"cap_completion_extra":extra,"new_rho":nr})
        all_zeros[str(epsilon)]=zeros
        weights,newbc=outer_weights(epsilon)
        payments.append({"epsilon":epsilon,"ten_positive_integer_scale_weights":dict(zip(NAMES,weights)),"free_beta_C":newbc,"free_beta_O":BO,"new_K_coefficient":AK+WEIGHTS[8]*epsilon/(6*DB),"all131_checks":all131(epsilon)})
    zero_original=[code for code,h in enumerate(STATES) if root_remainder(h,F(0))[0]==0]
    zero_strict=all_zeros["0"]
    assert zero_original==[0,1,3,5,9,17,33,103,115,121,123,125]
    assert zero_strict==[0,1,3,5,9,17,33,102,103,115,121,123,125]
    equal_rows=[]
    for code in zero_strict:
        h=STATES[code];_,aq,weak,_=envelope(h,F(0))
        equal_rows.append({"h":code,"bits":h,"C30_a0_a1":aq,"C30_all_attaining_tails":weak,"P25":p25(h)})
        for q in (0,1):
            assert len({tail[0] for tail in weak[q]})==1
    # All feasible branch-customer types, not only equality-support types.
    p25_rows=[{"h":code,**p25(h)} for code,h in enumerate(STATES)]
    minimum_original_gap=min(envelope(h,F(0))[1][1]-envelope(h,F(0))[1][0] for h in STATES)
    assert minimum_original_gap==F(85250,3)
    increment,ak=make_visible_row()
    save("inputs.json",{
        "actual_agent_id":"/root/high_lambda_closure","stage":"root270_equality_stage",
        "run":"six-boss1-20261111","DB":DB,"original_weights":dict(zip(NAMES,WEIGHTS)),
        "beta_C":BC,"beta_O":BO,"original_K_coefficient":AK,"O_coefficient":AO,"eta":ETA,
        "epsilon_endpoint":EPS,"new_K_increment":increment,"new_K_coefficient":ak,
        "epsilon_interval":[0,EPS],"all128_customer_types":True,"optimizer_calls":0,
        "global_candidate_and_optimal_face_files_are_not_inputs":True,
        "prior_high_lambda_package_is_not_an_input_and_is_unchanged":True,
    })
    save("all2048_C30_base_states.json",base_states)
    save("epsilon_envelopes.json",{
        "fixed_r_formula":"a_q(epsilon)=min(min_r0, min_r1+epsilon)",
        "fixed_r_minima":fixed_r,"complete_breakpoints":breaks,
        "events":[{"epsilon":x,"states":ys} for x,ys in sorted(epsilon_events.items())],
        "all_endpoint_envelopes":envelopes,
        "global_first_breakpoint":F(43,6),
        "fixed_root_payment_first_upper_limit":EPS,
        "beyond_endpoint_obstruction":{"h":3,"valid_right_neighborhood_until":F(20855,3),"normalized_new_rho":"(L_C30/DB)*(5/6)*(215/3-epsilon)"},
    })
    save("all128_root_remainders.json",{
        "all_parameter_endpoints":remainder_rows,"zero_types_by_epsilon":all_zeros,
        "complete_original_zero_types":zero_original,"complete_strict_zero_types":zero_strict,
        "continuous_nonnegativity":"piecewise affine interpolation on every complete breakpoint interval",
    })
    save("all131_payments.json",{"payments":payments})
    save("equality_structure.json",{
        "old_strict_equality_types":equal_rows,"all128_P25_weak_tables":p25_rows,
        "core_mass_names":{"A":102,"B":103,"Cstar":115,"Dstar":121,"Estar":123,"Fstar":125,"X":1,"N":0},
        "positive_CAP_relations":{"w33":"0","w17":"A+B","w9":"A+B+Cstar","w5":"Cstar+Dstar+Estar","w3":"Dstar+Fstar","K":"A+B+Cstar+Dstar+Estar+Fstar"},
        "each_true_R4k_common_types":[1,3,5,9,125],
        "each_true_R4k_query_selected_types":[17,33,103,115,121,123],
        "exact_average_R4_size":"7*K/6 + X + B/6 + Cstar + Dstar + 5*Fstar/6",
        "strict_ROOT270_equality_implies":"K=0; hence every legal action has empty coverage, O=0, u1=0",
        "PAIR30_hidden_last_reply":"Every true J_k after fifth-source query Q_k contains B5; genuine maximum K and |B5|=K force the same coverage as B5",
        "P25_true_fifth_reply":"The actual fifth reply after the fourth-source forced B6 has precisely the coverage of B6; all weak sixth replies are retained",
    })
    save("true_history_contract.json",{
        "root_branch":"(C,B2,B3,B4,B5,B6) generated by the same complete-history strategy after the original actual root forces legal C",
        "C30_branches":"(C,B2,Qk,R4k,R5k,R6k), separately for k=1,...,6; same k is retained in every budget",
        "new_positive_budget":"(1/6)*sum_k (K-|R4k|), each R4k already a legal action in the common catalogue",
        "old_C30_requeries":"At (C,B2,B3), source4 queries each Rjk; at (C,B2,B3,B4,B5), source6 queries each Rjk; both are branch incomes v4,v6",
        "internal_legal_requery_obligations":"At each (C,B2,Qk), source4 can query C, any Bj, or any Ql; its own continuation must be followed. These are valid further constraints but are not spent in the present CAP completion.",
        "P25_branch":"At (C,B2,B3), force B6, use its own two true successors, all size caps and its own terminal menu BR",
        "no_actual_income_substitution":True,"all_weak_ties_and_label_repetitions_preserved":True,
    })
    assert source_pins==pins()
    report={
        "status":"PASS_TRUE_ROOT270_EQUALITY_AND_UNIFORM_CAP_COMPLETION",
        "actual_agent_id":"/root/high_lambda_closure","optimizer_calls":0,
        "all_original_root_types":128,"original_C30_true_states":2048,
        "parameter_breakpoints":breaks,"endpoint_envelopes":len(envelopes),
        "endpoint_131_column_identities":len(breaks)*131,
        "visible_columns":513,"original_zero_types":zero_original,
        "strict_zero_types":zero_strict,"new_zero_types":all_zeros[str(EPS)],
        "original_C30_minimum_moment_slope":minimum_original_gap,
        "uniform_K_gain":increment,
        "integer_strict_line":{"u1":84387869309613600,"K":8839887370271285,"O":1686700906360065,"C_outside_O":1087978231314917},
        "sources_unchanged":True,"full_SPE_construction_claimed":False,
    }
    save("generator_output.json",report)
    print(json.dumps(encode(report),ensure_ascii=False,indent=2))


if __name__=="__main__":main()
