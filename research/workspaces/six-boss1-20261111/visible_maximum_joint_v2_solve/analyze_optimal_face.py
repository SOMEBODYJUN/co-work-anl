#!/usr/bin/env python3
"""Full-face symbolic algebra and exact cheap NS5/root diagnostics; no optimizer."""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import sympy as sp

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
SOURCE=BASE/"visible_maximum_joint_v2"
sha=lambda p:sha256(p.read_bytes()).hexdigest()
dump=lambda p,v:p.write_text(json.dumps(v,indent=2)+"\n")
fr=lambda x:F(int(x.p),int(x.q))
data=json.loads((SOURCE/"exact_input.json").read_text())
cert=json.loads((HERE/"exact_certificate.json").read_text())
assert sha(SOURCE/"exact_input.json")==cert["input_sha256"]
rows=data["raw_rows"]; atoms=data["atom_columns"]
z=list(map(F,cert["primal"]))
residual=list(map(F,cert["dual"]["nonnegative_column_residual"]))
allowed=[j for j,r in enumerate(residual) if not r]
positive=cert["dual"]["positive_raw_indices"]
equations=data["equalities"]+[rows[i] for i in positive]
eqnames=[e["name"] for e in equations]
matrix=sp.Matrix([[sp.Rational(e["a"].get(str(j),"0")) for j in allowed] for e in equations])
rhs=sp.Matrix([sp.Rational(e["rhs"]) for e in equations])
rref,pivots=matrix.row_join(rhs).rref()
assert len(allowed) not in pivots
freepos=[j for j in range(len(allowed)) if j not in pivots]
freecols=[allowed[j] for j in freepos]
P=len(freepos)
constant=[F(0)]*len(allowed)
coeff=[[F(0)]*P for _ in allowed]
for k,j in enumerate(freepos):coeff[j][k]=F(1)
for i,j in enumerate(pivots):
    constant[j]=fr(rref[i,-1])
    for k,f in enumerate(freepos):coeff[j][k]=-fr(rref[i,f])
pointparameters=[z[j] for j in freecols]
assert all(constant[k]+sum((coeff[k][t]*pointparameters[t] for t in range(P)),F(0))==z[j]
           for k,j in enumerate(allowed))

def restrict(vector,rhs=F(0)):
    av=[F(vector.get(str(j),"0")) for j in allowed]
    base=sum((a*v for a,v in zip(av,constant)),F(0))-rhs
    cs=[sum((av[k]*coeff[k][t] for k in range(len(allowed))),F(0)) for t in range(P)]
    return base,cs

pack=lambda b,cs:{"constant":str(b),"parameter_coefficients":[str(v) for v in cs]}

def fixed(name,vector,rhs_value=F(0)):
    base,cs=restrict(vector,rhs_value)
    assert all(v==0 for v in cs),(name,cs)
    target=sp.Matrix([sp.Rational(vector.get(str(j),"0")) for j in allowed])
    solutions=sp.linsolve((matrix.T,target))
    assert len(solutions)==1
    weights=list(map(fr,next(iter(solutions))))
    assert sum((w*F(e["rhs"]) for w,e in zip(weights,equations)),F(0))-rhs_value==base
    return {"name":name,"value":str(base),"decimal":float(base),
            "signed_equation_weights":[str(w) for w in weights],"subtracted_rhs":str(rhs_value),
            "domain":"Only on the full complementarity support; signed equality identity, not a universal nonnegative payment."}

Kvec={"512":"1"}
A1vec={str(v["index"]):str(v["a"][0]) for v in atoms if v["a"][0]}
Xvec={str(v["index"]):str(v["x"]) for v in atoms if v["x"]}
U2vec={str(v["index"]):str(F(v["a"][1],sum(v["a"]))) for v in atoms if v["a"][1]}
outsideCvec={str(v["index"]):"1" for v in atoms if v["c"] and not v["o"]}
gapvec=dict(U2vec);gapvec["512"]="-1/5"
fixed_values=[fixed("K",Kvec),fixed("size_A1",A1vec),fixed("size_X",Xvec),fixed("u2",U2vec),
              fixed("u2_minus_K_over5",gapvec),fixed("C_outside_O_mass",outsideCvec),
              fixed("old_P25_C_Omean_slack",rows[927]["a"],F(rows[927]["rhs"])),
              fixed("ROOT270_slack",rows[868]["a"],F(rows[868]["rhs"])),
              fixed("NS5_slack",rows[1002]["a"],F(rows[1002]["rhs"]))]
fixed_map={v["name"]:F(v["value"]) for v in fixed_values}
assert fixed_map["u2_minus_K_over5"]>0
assert fixed_map["C_outside_O_mass"]==fixed_map["ROOT270_slack"]==fixed_map["NS5_slack"]==0
assert fixed_map["old_P25_C_Omean_slack"]>0
restrictions=[]
for i,row in enumerate(rows):
    b,cs=restrict(row["a"],F(row["rhs"]))
    assert b+sum((v*p for v,p in zip(cs,pointparameters)),F(0))>=0
    restrictions.append({"raw_index":i,"name":row["name"],**pack(b,cs)})

support_implications={
    "all_visible_roles_inside_O":all(v["o"] or not(sum(v["a"]) or v["x"] or v["c"]) for v in atoms if v["index"] in allowed),
    "A1_subset_C":all(not v["a"][0] or v["c"] for v in atoms if v["index"] in allowed),
    "A1_disjoint_X":all(not(v["a"][0] and v["x"]) for v in atoms if v["index"] in allowed),
    "X_subset_A5_union_A6":all(not v["x"] or v["a"][4] or v["a"][5] for v in atoms if v["index"] in allowed),
    "A5_disjoint_A6":all(not(v["a"][4] and v["a"][5]) for v in atoms if v["index"] in allowed),
}
assert all(support_implications.values())
face={"status":"EXACT_WHOLE_OPTIMAL_FACE_PARAMETERIZATION","input_sha256":cert["input_sha256"],
      "certificate_sha256":sha(HERE/"exact_certificate.json"),"optimizer_calls_in_this_script":0,
      "objective":cert["objective"],"zero_residual_columns":allowed,
      "forced_zero_columns":[j for j in range(513) if j not in allowed],
      "positive_dual_raw_indices":positive,"equation_names":eqnames,"equation_rhs":[e["rhs"] for e in equations],
      "restricted_equation_rank":len(pivots),"unconstrained_affine_parameter_count":P,
      "parameters":[{"position":k,"name":"z"+str(j),"column":j} for k,j in enumerate(freecols)],
      "coordinates":[{"column":j,**pack(constant[k],coeff[k])} for k,j in enumerate(allowed)],
      "nonnegative_coordinates_required":allowed,"raw_inequality_restrictions":restrictions,
      "nonconstant_raw_indices":[x["raw_index"] for x in restrictions if any(F(v) for v in x["parameter_coefficients"])],
      "point_parameters":[str(v) for v in pointparameters],"fixed_functionals":fixed_values,
      "support_implications":support_implications,
      "characterization":"Exactly the optimal face: columns outside the zero-residual set vanish, all positive-dual rows are tight, both equalities hold, and every supplied coordinate/raw inequality is nonnegative. No claim that the whole containing affine space is feasible."}
dump(HERE/"optimal_face.json",face)

# Keep every endpoint zero state, including the extra c=0,o=1,0010 state.
theta=F(5,12); allstates=[]; min_types=[]; zero_states=[]
source_minima=json.loads((BASE/"main_source2_maximum_nested_safe/minimum_table.json").read_text())
for p,c,o in product([0,1],repeat=3):
    minimum=F(5*c,2)+F(24*c,p+5)+F(o,6*(p+4*c+1))+theta*(F(o,6*(p+3*c+2))-F(c,5))
    zeros=[]; values=[]
    for rr in product([0,1],repeat=4):
        r3,r4,r5,r6=rr; L=p+c+sum(rr)
        numerator=25*c-r6-theta*r5
        assert L or numerator==0
        share=numerator/L if L else F(0)
        cost=share+F(r3+r4+r5,2)+r6+F(o,6*(p+c+r3+r4+r5+1))+F(5*o,72*(p+c+r3+r4+2))
        v2=F(c,L) if L else F(0)
        excess=cost-minimum
        assert excess>=0
        record={"p":p,"c":c,"o":o,"tail":list(rr),"load":L,"cost":str(cost),
                "minimum":str(minimum),"local_excess":str(excess),"forced_C_source_payoff":str(v2)}
        allstates.append(record);values.append(cost)
        if not excess:
            assert v2==F(c,5)
            zero_states.append(record);zeros.append(list(rr))
    assert min(values)==minimum
    src=next(x for x in source_minima if (x["p"],x["c"],x["o"])==(p,c,o))
    assert zeros==src["zero_states"] and minimum==F(src["minimum"])
    min_types.append({"p":p,"c":c,"o":o,"minimum":str(minimum),"zero_states":zeros})
assert len(allstates)==128 and len(zero_states)==11
assert any(x["p"]==0 and x["c"]==0 and x["o"]==1 and x["tail"]==[0,0,1,0] for x in zero_states)

eta=F(1087978231314917,84387869309613600)
root_input_path=BASE/"maximal_root_tail_wallet_v3/exact_input.json"
root_cert_path=BASE/"maximal_root_tail_wallet_v3/exact_certificate.json"
root_input=json.loads(root_input_path.read_text())
root_cert=json.loads(root_cert_path.read_text())
assert root_input["semantic_bit_order"]==["C","B2","B3","B4","B5","B6","o"]
root_residual=root_cert["dual"]["column_residuals"]
root_reduced=[];outside_residuals=[]
for atom in root_input["atoms"]:
    j=atom["index"];outside=atom["bits"][0]*(1-atom["bits"][-1])
    old=F(root_residual[str(j)])
    reduced=old-eta*outside
    assert reduced>=0
    root_reduced.append({"column":j,"bits":atom["bits"],"old_residual":str(old),"new_residual":str(reduced)})
    if outside:outside_residuals.append(old)
assert len(root_reduced)==128 and len(outside_residuals)==32 and min(outside_residuals)==eta
dump(HERE/"root_strengthening_column_check.json",{
    "status":"PASS_128_ROOT_RESIDUALS_AFTER_C_OUTSIDE_O_REMAINDER","optimizer_calls":0,
    "root_input_sha256":sha(root_input_path),"root_certificate_sha256":sha(root_cert_path),
    "eta":str(eta),"C_outside_O_columns":32,"minimum_outside_residual":str(min(outside_residuals)),
    "all128_reduced_residuals":root_reduced,
    "v2_whole_face_ROOT270_slack":str(fixed_map["ROOT270_slack"]),
    "v2_whole_face_C_outside_O_mass":str(fixed_map["C_outside_O_mass"]),
    "scope":"Checks the supplied root strengthening and its lack of separation on this wholeface. Does not append an input row."})
diagnostic={"status":"WHOLE_OPTIMAL_FACE_EXCLUDED_BY_NS5_SOURCE_IC_EQUALITY","optimizer_calls":0,
    "input_sha256":cert["input_sha256"],"certificate_sha256":sha(HERE/"exact_certificate.json"),
    "face_sha256":sha(HERE/"optimal_face.json"),
    "positive_NS5_weight":cert["dual"]["raw_row_weights"][1002],
    "full128_local_cost_states":allstates,"all8_minimum_types":min_types,"all11_zero_states":zero_states,
    "extra_0010_zero_state_retained":True,
    "zero_state_source_payoff_identity":"Every local zero state, including c=0,o=1,0010, has c/(p+c+r3+r4+r5+r6)=c/5, with 0/0 interpreted as zero.",
    "integer_scale_real_payment_weights":{"source2_IC":"300","CAP_R3":"6","CAP_R4":"6","CAP_R5":"6","CAP_R6":"12","terminal_mean_BR":"12","true_internal_source5_mean_SAFE":"5","menu_projection_gap":"12","local_minimum_gap":"12","C_size_free_equality":"29"},
    "equality_argument":[
        "NS5 has strictly positive dual weight and is therefore zero at every cone optimum.",
        "Its exact real-budget identity and the C-size equality force source2 true IC to be tight and every positive-mass client's local envelope residual to be zero.",
        "Every one of the eleven zero states has forced-source payoff c/5; no weak zero state is deleted.",
        "Summing gives v2=|C|/5=K/5. The tight true source IC gives actual u2=v2.",
        "The whole face instead has the fixed strictly positive u2-K/5 below, hence no point on this face is a complete ordered pure SPE projection."],
    "uniform_contradiction_gap":str(fixed_map["u2_minus_K_over5"]),
    "uniform_contradiction_gap_decimal":float(fixed_map["u2_minus_K_over5"]),
    "known_root_strengthening_diagnostic":{"inequality":"ROOT270 >= eta*|C outside O|","eta":str(eta),
        "whole_face_ROOT270_slack":str(fixed_map["ROOT270_slack"]),"whole_face_C_outside_O":str(fixed_map["C_outside_O_mass"]),
        "outcome":"Both sides zero on the whole face; no additional exclusion. Not appended to input."},
    "old_P25_C_Omean_diagnostic":{"whole_face_slack":str(fixed_map["old_P25_C_Omean_slack"]),
        "outcome":"Strictly positive, so the previous P25(C,Omean) equality argument is unavailable here."},
    "scope":"Universal alpha bound and exact necessary-cone optimum; exact attainment is impossible for a genuine positive-OPT complete ordered pure SPE. No quantified larger infimum or half theorem follows from this equality-only argument."}
dump(HERE/"true_branch_equality_diagnostic.json",diagnostic)

oldcert=json.loads((BASE/"visible_maximum_joint_solve/exact_certificate.json").read_text())
oldpos=set(oldcert["dual"]["positive_raw_indices"]);newpos=set(positive)
change={"status":"EXACT_POSITIVE_PAYMENT_COMPARISON","old_certificate_sha256":sha(BASE/"visible_maximum_joint_solve/exact_certificate.json"),
        "new_certificate_sha256":sha(HERE/"exact_certificate.json"),"old_objective":oldcert["objective"],"new_objective":cert["objective"],
        "objective_improvement":str(F(cert["objective"])-F(oldcert["objective"])),
        "entered":[{"raw_index":i,"name":rows[i]["name"],"new_weight":cert["dual"]["raw_row_weights"][i]} for i in sorted(newpos-oldpos)],
        "exited":[{"raw_index":i,"name":rows[i]["name"],"old_weight":oldcert["dual"]["raw_row_weights"][i]} for i in sorted(oldpos-newpos)],
        "retained":[{"raw_index":i,"name":rows[i]["name"],"old_weight":oldcert["dual"]["raw_row_weights"][i],"new_weight":cert["dual"]["raw_row_weights"][i]} for i in sorted(oldpos&newpos)]}
dump(HERE/"positive_payment_changes.json",change)
print(json.dumps({"face_rank":len(pivots),"zero_residual_columns":allowed,"free_columns":freecols,
      "nonconstant_raw_constraints":len(face["nonconstant_raw_indices"]),"fixed_values":{k:str(v) for k,v in fixed_map.items()},
      "NS5_local_zero_states":len(zero_states),"extra0010_retained":True},indent=2))
