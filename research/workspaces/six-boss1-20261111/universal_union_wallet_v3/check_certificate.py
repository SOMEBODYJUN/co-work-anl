#!/usr/bin/env python3
"""Independent literal source and exact certificate checker; no optimizer."""
import sys
sys.dont_write_bytecode=True
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from math import lcm
import hashlib,json
from literal_sources import old_rows,literal_tail

HERE=Path(__file__).resolve().parent;RUN=HERE.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inp=json.loads((HERE/"exact_input.json").read_text());protected=json.loads((HERE/"prior_frozen_hashes.json").read_text())
assert all(sha(RUN/n)==h for n,h in protected.items())
assert all(sha(RUN/n)==h for n,h in inp["source_sha256"].items())
assert sha(HERE/"source_review.md")==inp["source_review_sha256"]
atoms=[tuple(r["a"])+(r["x"],r["o"]) for r in inp["atom_columns"]]
assert atoms==list(product((0,1),repeat=8))
assert inp["K_column"]==256 and inp["nonnegative_columns"]==list(range(257))
semantic=[]
for j,v in enumerate(atoms):
    r=old_rows(v);c=sum(v[:6]);u1=F(v[0],c) if c else F(0)
    u4=F(v[3],c) if c else F(0);u5=F(v[4],c) if c else F(0)
    vals=[literal_tail(v,y,t) for y,t in product((0,1),repeat=2)];m=min(vals)
    assert m==F(inp["tail_minima"][str(j)])
    r["ROOT_BRANCH_NEW"]=10980*u1-87*v[7]
    r["TRUE_X_TAIL_CUT"]=4096*u4+900*u5+F(1700*v[6],sum(v[:4])+1)-m
    r["ROOT_SIZE_FEEDBACK"]=67140*u1-627*v[7]
    r["ROOT_TRUE_TAIL"]=112944305160*u1-2178783435*v[7]
    semantic.append(r)
kr=old_rows((0,)*8,F(1))
kr.update({"ROOT_BRANCH_NEW":-F(1658),"TRUE_X_TAIL_CUT":F(71),"ROOT_SIZE_FEEDBACK":-F(9878),"ROOT_TRUE_TAIL":-F(11595684007)})
semantic.append(kr)
raw={r["name"]:r for r in inp["raw_rows"]}
assert len(raw)==len(inp["raw_rows"])==221 and set(raw)==set(semantic[0])
for j in range(257):
    for name,row in raw.items():assert F(row["a"].get(str(j),"0"))==semantic[j][name],(j,name)
for name,row in raw.items():
    expected=-F(1) if name.startswith("OPT6_omit_") or name in ("K_le_1","W_le_1") else F(0)
    assert F(row["rhs"])==expected
assert inp["objective"]=={str(j):"1" for j,v in enumerate(atoms) if any(v[:6])}
assert inp["equality"]["a"]=={str(j):"1" for j,v in enumerate(atoms) if v[7]}
assert F(inp["equality"]["rhs"])==1

# Reconstruct the feedback row's128-type inequality and literal positive payment.
eta_min=None
for bits in product((0,1),repeat=7):
    p,y2,y3,y4,y5,t,o=bits;n=y2+y3+y4+y5;load=p+n+t;theta=F(o,6)
    v=F(p,load) if load else F(0);s=F(y5,load) if load else F(0);w=F(t,load) if load else F(0)
    tau=F(n,2)+t-7*p+25*v-w-theta/(1+5*p)+theta/(1+p+n)
    delta=v-s+theta/(p+n-y5+2)-F(o,12)+F(p,18)
    rho=delta+F(12,5)*tau;eta=F(65,84)*rho-tau-F(5,12)*(p-y5)
    assert tau>=0 and rho>=0 and eta>=0
    paid=(-67140*v+2340*(s-theta/(p+n-y5+2))-1296*(y2+y3+y4)-2556*y5
          -2592*t+2592*(w-theta/(1+p+n))+360*p*(1-o)+3024*eta)
    assert paid+18914*p+627*o==0
    eta_min=eta if eta_min is None else min(eta_min,eta)

# Independently reconstruct the10 positive maximal-root budgets, including36 pairs.
source_cert=json.loads((RUN/"maximal_root_tail_wallet/exact_certificate.json").read_text())
main_check=json.loads((RUN/"main_maximal_root_tail_check.json").read_text())
weights={"ROOT_IC":112944305160,"CAP_B2":939131055,"CAP_B3":6218848680,"CAP_B4":6200167680,
         "CAP_B5":6031687680,"CAP_B6":6390005760,"SAFE_j3|Omean":5324085000,
         "SAFE_j4|Omean":5380128000,"SAFE_j6|Omean":2508226560,"PAIR|Omean|Omean":3881779200}
assert {n:str(w) for n,w in weights.items()}==source_cert["dual"]["integer_row_weights"]
pi_p=37375524862;pi_o=2178783435;NN=112944305160;AA=11595684007;BB=2178783435
assert source_cert["dual"]["integer_equality_multipliers"]==[str(pi_p),str(pi_o)]
caps=sum(weights[f"CAP_B{j}"] for j in range(2,7))
assert caps==25779840855 and pi_p-caps==AA
assert weights["ROOT_IC"]==NN and -pi_o==-BB
root_res=[]
for idx,h in enumerate(product((0,1),repeat=7)):
    ll=list(h[:6]);o=h[6];c=sum(ll);pay=[F(v,c) if c else F(0) for v in ll]
    r={"ROOT_IC":-pay[0]}
    for j in range(2,7):r[f"CAP_B{j}"]=-F(ll[j-1])
    for j in (3,4,6):r[f"SAFE_j{j}|Omean"]=pay[j-1]-F(o,6*(sum(ll[:j-1])+7-j))
    DD=1+sum(ll[:4]);query=[o,0,0,0,0,0]
    pairs=sum(F(q+s,DD)-F(q*s,DD*(DD+1)) for q in query for s in query)/36
    assert pairs==F(o,3*DD)-F(o,36*DD*(DD+1))
    r["PAIR|Omean|Omean"]=pay[4]+pay[5]+F(ll[4],DD*(DD+1))-pairs
    rem=-sum(weights[n]*value for n,value in r.items())-pi_p*ll[0]-pi_o*o
    assert rem>=0
    assert rem==NN*F(source_cert["dual"]["column_residuals"][str(idx)])
    assert main_check["residuals"][idx]["bits"]==list(h)
    assert rem==F(main_check["residuals"][idx]["integer_scaled_residual"])
    root_res.append(rem)
assert sum(r==0 for r in root_res)==13 and sum(r>0 for r in root_res)==115
assert F(source_cert["dual"]["column_residuals"]["128"])==0
for DD in range(1,6):
    for count in range(7):
        o=int(count>0)
        full=F(count,3*DD)-F(count*count,36*DD*(DD+1))
        weak=F(o,3*DD)-F(o,36*DD*(DD+1));assert full>=weak

seen={};order=[];zero=[]
for row in inp["raw_rows"]:
    key=(tuple(F(row["a"].get(str(j),"0")) for j in range(257)),F(row["rhs"]))
    if not any(key[0]) and key[1]==0:zero.append(row["name"])
    elif key in seen:seen[key].append(row["name"])
    else:seen[key]=[row["name"]];order.append(row["name"])
assert len(seen)==209 and zero==inp["removed_zero_rows"]
assert [r["name"] for r in inp["unique_rows"]]==order
for row in inp["unique_rows"]:
    key=(tuple(F(row["a"].get(str(j),"0")) for j in range(257)),F(row["rhs"]))
    assert row["aliases"]==seen[key]
baseline=json.loads((HERE/"baseline_dual_extension.json").read_text());alpha2=F(baseline["objective"])
by={n:F(v) for n,v in baseline["row_weights"].items()}
for j in range(257):
    c=F(j<256 and any(atoms[j][:6]));o=F(atoms[j][7]) if j<256 else F(0)
    rem=c-alpha2*o-sum(w*semantic[j][n] for n,w in by.items())
    assert rem>=0 and rem==F(baseline["nonnegative_column_residual"].get(str(j),"0"))
source_report={"status":"PASS","scope":"literal source preflight of221 rows and all256 types; no optimization",
    "input_sha256":sha(HERE/"exact_input.json"),"matrix_coefficient_equalities":221*257,
    "raw_rows":221,"unique_rows":209,"columns":257,"all256_types_retained":True,
    "feedback_types_checked":128,"feedback_eta_min":str(eta_min),
    "true_root_budget_count":10,"true_root_atom_columns":128,"true_root_free_parameter_columns":3,
    "true_root_positive_residuals":115,"true_root_zero_residuals":13,
    "K_equality_multiplier":str(pi_p),"cap_weight_sum":str(caps),"root_K_coefficient":str(-AA),
    "root_union_mean_weakening_checks":35,"v2_baseline_bound":str(alpha2),"baseline_columns_checked":257,
    "prior_frozen_files_unchanged":len(protected),"optimizer_imported":False}
(HERE/"source_check.json").write_text(json.dumps(source_report,indent=2)+"\n")
if not (HERE/"exact_certificate.json").exists():
    print(json.dumps(source_report,indent=2));raise SystemExit(0)

cert=json.loads((HERE/"exact_certificate.json").read_text());assert cert["input_sha256"]==sha(HERE/"exact_input.json")
z=[F(cert["primal"].get(str(j),"0")) for j in range(257)];assert all(v>=0 for v in z)
O=sum(z[j]*atoms[j][7] for j in range(256));W=sum(z[j] for j,v in enumerate(atoms) if any(v[:6]))
assert O==1 and W==F(cert["objective"])
slacks={n:sum(z[j]*semantic[j][n] for j in range(257))-F(row["rhs"]) for n,row in raw.items()}
assert all(v>=0 for v in slacks.values()) and {n:str(v) for n,v in slacks.items()}==cert["raw_row_slacks"]
y={n:F(v) for n,v in cert["dual"]["row_weights"].items()};assert all(v>0 for v in y.values())
nu=F(cert["dual"]["normalization_multiplier"])
assert nu+sum(w*F(raw[n]["rhs"]) for n,w in y.items())==W==F(cert["dual"]["objective"])
res=[]
for j in range(257):
    c=F(j<256 and any(atoms[j][:6]));o=F(atoms[j][7]) if j<256 else F(0)
    rem=c-nu*o-sum(w*semantic[j][n] for n,w in y.items());assert rem>=0 and rem*z[j]==0
    assert rem==F(cert["dual"]["nonnegative_column_residual"].get(str(j),"0"));res.append(rem)
assert all(slacks[n]*w==0 for n,w in y.items()) and W>=alpha2
scale=lcm(nu.denominator,*(v.denominator for v in y.values()));scaled=[v*scale for v in res];mult=lcm(*(v.denominator for v in scaled))
identity={"scale":str(scale),"objective_numerator":str(W*scale),"integer_budget_weights":{n:str(v*scale) for n,v in y.items()},
          "residual_integer_multiplier":mult,"K_residual":str(scaled[256]),"smallest_positive_scaled_residual":str(min(v for v in scaled if v>0))}
assert all((v*scale).denominator==1 for v in y.values()) and (W*scale).denominator==1
(HERE/"global_identity.json").write_text(json.dumps(identity,indent=2)+"\n")
with (HERE/"dual_column_checks.tsv").open("w") as out:
    out.write("column\ta1a2a3a4a5a6\tx\to\texact_residual\n")
    for j,v in enumerate(res):
        t=atoms[j] if j<256 else None
        out.write(f'{j}\t{"".join(map(str,t[:6])) if t else "K"}\t{t[6] if t else "-"}\t{t[7] if t else "-"}\t{v}\n')
with (HERE/"integer_residual_table.tsv").open("w") as out:
    out.write("a1a2a3a4a5a6\tx0_o0\tx0_o1\tx1_o0\tx1_o1\n")
    for mask in range(64):
        vals=[scaled[4*mask+k]*mult for k in range(4)];assert all(v.denominator==1 and v>=0 for v in vals)
        out.write("".join(map(str,atoms[4*mask][:6]))+"\t"+"\t".join(map(str,vals))+"\n")
report={**source_report,"status":"PASS: exact matching primal/dual on unscaled221 rows and all257 columns",
        "scope":"v3 full literal source and exact certificate check; no optimizer",
        "objective":str(W),"objective_decimal":float(W),"half_gap":str(F(1,2)-W),
        "positive_primal_atoms":sum(v>0 for v in z[:256]),"K":str(z[256]),"positive_dual_rows":len(y),
        "dual_columns_checked":257,"zero_duality_gap":True,
        "zero_dual_columns":[j for j,v in enumerate(res) if v==0],"positive_dual_columns":sum(v>0 for v in res),
        "new_row_slacks":{n:str(slacks[n]) for n in ["ROOT_SIZE_FEEDBACK","ROOT_TRUE_TAIL"]},
        "new_row_dual_weights":{n:str(y.get(n,F(0))) for n in ["ROOT_SIZE_FEEDBACK","ROOT_TRUE_TAIL"]}}
(HERE/"checker_output.json").write_text(json.dumps(report,indent=2)+"\n")
assert all(sha(RUN/n)==h for n,h in protected.items())
print(json.dumps(report,indent=2))
