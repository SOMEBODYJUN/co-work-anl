#!/usr/bin/env python3
"""Independent source and certificate checker. Standard library only."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from math import lcm
import hashlib,json

HERE=Path(__file__).resolve().parent;RUN=HERE.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
inp=json.loads((HERE/"exact_input.json").read_text())
protected=json.loads((HERE/"prior_frozen_hashes.json").read_text())
assert all(sha(RUN/name)==digest for name,digest in protected.items())
for name,digest in inp["source_sha256"].items():assert sha(RUN/name)==digest,(name,"source hash changed")
assert sha(HERE/"source_review.md")==inp["source_review_sha256"]
atoms=[tuple(r["a"])+(r["x"],r["o"]) for r in inp["atom_columns"]]
assert atoms==list(product((0,1),repeat=8))
assert inp["K_column"]==256 and inp["nonnegative_columns"]==list(range(257))


def old_rows(v,K=F(0)):
    a=list(v[:6]);x,o=v[6:];c=sum(a);P=sum(a[:4]);D=P+1
    us=[F(q,c) if c else F(0) for q in a]
    pure=a+[x];theta=list(map(F,pure))+[F(o,6)];fs=[q/D for q in theta]
    r={}
    for i in range(6):
        for j in range(8):r[f"SAFE_{i+1}_{j+1}"]=us[i]-theta[j]/(sum(a[:i])+6-i)
    for i,C in enumerate((31,25,19,10)):
        b=sum(a[:i]);cap=b+6-i
        r[f"UP_{i+1}"]=C*us[i]-F((C-1)*x,cap)-F(o*x,6*cap)-F(o*(1-x),6*(b+1))
    for j in list(range(6))+[7]:
        r[f"FMAX_{j+1}"]=fs[6]-fs[j]
        r[f"MX_{j+1}"]=us[4]-theta[j]/(D+x)
    for l in range(8):
        for rr in range(l,8):
            if rr<7:right=F(pure[l]+pure[rr],D)-F(pure[l]*pure[rr],D*(D+1))
            elif l<7:right=F(pure[l],D)+F(o,6*D)-F(pure[l]*o,6*D*(D+1))
            else:right=F(o,3*D)-F(o,36*D*(D+1))
            r[f"RC_{l+1}_{rr+1}"]=us[4]+fs[6]-right
            r[f"PAIR_{l+1}_{rr+1}"]=us[4]+us[5]+F(a[4],D*(D+1))-right
    for omit in range(7):r[f"OPT6_omit_{omit+1}"]=-F(any(bit for j,bit in enumerate(pure) if j!=omit))
    for j in range(7):r[f"K_ge_size_{j+1}"]=K-pure[j]
    r["K_le_1"]=-K
    for i in range(6):r[f"SIZE_FLOOR_{i+1}"]=us[i]-K/6
    r["W_le_1"]=-F(c>0)
    r["ROOT_NEAR"]=150*us[0]-F(139,6)*K-o
    for anchor in range(7):
        for query in range(8):r[f"ROOT_RIG_{anchor+1}_{query+1}"]=25*us[0]+3*K-7*pure[anchor]-theta[query]+F(5,6)*pure[anchor]*theta[query]
    return r


def literal_tail(v,y,t):
    """Weighted original six row LHS, using the actual common branch load."""
    a=list(v[:6]);x,o=v[6:];b=sum(a[:3]);P=b+a[3];D=P+1;d=b+x+1
    load=b+x+y+t;theta=F(o,6)
    v4=F(x,load) if load else F(0)
    fifth=F(y,load) if load else F(0)
    sixth=F(t,load) if load else F(0)
    source_ic=v4
    global_max=F(y,D)
    global_cap=F(t)
    terminal_BR=theta/(b+x+y+1)-sixth
    pair_query=(F(a[5],d)+theta/d-F(a[5],d*(d+1))*theta)
    pair_wallet=fifth+sixth+F(y,d*(d+1))
    actual_RC=F(t,D)+theta/D-F(t,D*(D+1))*theta
    return (4096*source_ic+800*global_max+71*global_cap+384*terminal_BR
            +512*(pair_query-pair_wallet)+900*actual_RC)


semantic=[];mins=[];state_count=0
tail_cert=json.loads((RUN/"universal_true_x_tail/exact_certificate.json").read_text())
for j,v in enumerate(atoms):
    r=old_rows(v);c=sum(v[:6]);u1=F(v[0],c) if c else F(0)
    u4=F(v[3],c) if c else F(0);u5=F(v[4],c) if c else F(0)
    values=[literal_tail(v,y,t) for y,t in product((0,1),repeat=2)]
    m=min(values);mins.append(m);state_count+=len(values)
    assert all(value-m>=0 for value in values)
    assert m==F(inp["tail_minima"][str(j)])
    r["ROOT_BRANCH_NEW"]=10980*u1-87*v[7]
    r["TRUE_X_TAIL_CUT"]=4096*u4+900*u5+F(1700*v[6],sum(v[:4])+1)-m
    assert r["TRUE_X_TAIL_CUT"]==F(tail_cert["universal_cut"]["cut_z"][str(j)])
    semantic.append(r)
kr=old_rows((0,)*8,F(1));kr["ROOT_BRANCH_NEW"]=-F(1658);kr["TRUE_X_TAIL_CUT"]=F(71)
semantic.append(kr)
assert F(tail_cert["universal_cut"]["cut_K"])==71
raw={r["name"]:r for r in inp["raw_rows"]}
assert len(raw)==len(inp["raw_rows"])==219 and set(raw)==set(semantic[0])
for j in range(257):
    for name,row in raw.items():assert F(row["a"].get(str(j),"0"))==semantic[j][name],(j,name)
for name,row in raw.items():
    expected=-F(1) if name.startswith("OPT6_omit_") or name in ("K_le_1","W_le_1") else F(0)
    assert F(row["rhs"])==expected
assert inp["objective"]=={str(j):"1" for j,v in enumerate(atoms) if any(v[:6])}
assert inp["equality"]["a"]=={str(j):"1" for j,v in enumerate(atoms) if v[7]}
assert F(inp["equality"]["rhs"])==1

# Independently check Main's root-branch residuals and both paid identities.
tau_min=None;rho_min=None;kappa_min=None
for bits in product((0,1),repeat=7):
    p,y2,y3,y4,y5,t,o=bits;n=y2+y3+y4+y5;load=p+n+t;theta=F(o,6)
    v=F(p,load) if load else F(0);s=F(y5,load) if load else F(0);w=F(t,load) if load else F(0)
    tau=F(n,2)+t-7*p+25*v-w-theta/(1+5*p)+theta/(1+p+n)
    delta=v-s+theta/(p+n-y5+2)-F(o,12)+F(p,18)
    rho=delta+F(12,5)*tau
    assert tau>=0 and rho>=0
    H_atom=-150*v-3*n-6*t+6*w-6*theta/(1+p+n)+6*tau+F(5*p*(1-o),6)
    assert H_atom+F(247*p,6)+o==0
    paid_atom=(-61*v+s-theta/(p+n-y5+2)-F(6*n,5)-F(12*t,5)
               +F(12,5)*(w-theta/(1+p+n))+F(p*(1-o),3)+rho)
    assert paid_atom+F(36*p,5)==-F(829*p,90)-F(29*o,60)
    kappa=F(65,84)*rho-tau-F(5,12)*(p-y5)
    assert kappa>=0
    refined_paid=(-67140*v+2340*(s-theta/(p+n-y5+2))-1296*(y2+y3+y4)-2556*y5
                  -2592*t+2592*(w-theta/(1+p+n))+360*p*(1-o)+3024*kappa)
    assert refined_paid+18914*p+627*o==0
    tau_min=tau if tau_min is None else min(tau_min,tau)
    rho_min=rho if rho_min is None else min(rho_min,rho)
    kappa_min=kappa if kappa_min is None else min(kappa_min,kappa)

seen={};order=[];zero=[]
for row in inp["raw_rows"]:
    key=(tuple(F(row["a"].get(str(j),"0")) for j in range(257)),F(row["rhs"]))
    if not any(key[0]) and key[1]==0:zero.append(row["name"])
    elif key in seen:seen[key].append(row["name"])
    else:seen[key]=[row["name"]];order.append(row["name"])
assert len(seen)==207 and zero==inp["removed_zero_rows"]
assert [r["name"] for r in inp["unique_rows"]]==order
for row in inp["unique_rows"]:
    key=(tuple(F(row["a"].get(str(j),"0")) for j in range(257)),F(row["rhs"]))
    assert row["aliases"]==seen[key]

baseline=json.loads((HERE/"baseline_dual_extension.json").read_text())
alpha1=F(baseline["bound"])
by={name:F(value) for name,value in baseline["row_weights"].items()}
assert all(v>=0 for v in by.values())
for j in range(257):
    c=F(j<256 and any(atoms[j][:6]));o=F(atoms[j][7]) if j<256 else F(0)
    rem=c-alpha1*o-sum(w*semantic[j][name] for name,w in by.items())
    assert rem>=0 and rem==F(baseline["nonnegative_column_residual"].get(str(j),"0"))
source_report={"status":"PASS","scope":"preflight source formulas and complete219x257 matrix; no optimization",
    "input_sha256":sha(HERE/"exact_input.json"),"matrix_coefficient_equalities":219*257,
    "all256_old_types_present":True,"unique_inequalities":207,"raw_inequalities":219,
    "root_branch_types":128,"root_tau_min":str(tau_min),"root_rho_min":str(rho_min),
    "root_paid_identities_checked":256,"literal_tail_state_coefficients":state_count,
    "tail_minima_checked":256,"tail_cut_K":"71","tail_negative_minima":sum(m<0 for m in mins),
    "Main_strict_baseline":str(alpha1),"Main_baseline_columns_checked":257,
    "prior_frozen_files_unchanged":len(protected),"optimizer_imported":False}
(HERE/"source_check.json").write_text(json.dumps(source_report,indent=2)+"\n")
if not (HERE/"exact_certificate.json").exists():
    print(json.dumps(source_report,indent=2));raise SystemExit(0)

# Full rational certificate check after the one discovery solve.
cert=json.loads((HERE/"exact_certificate.json").read_text())
assert cert["input_sha256"]==sha(HERE/"exact_input.json")
z=[F(cert["primal"].get(str(j),"0")) for j in range(257)]
assert all(value>=0 for value in z)
O=sum(z[j]*atoms[j][7] for j in range(256));W=sum(z[j] for j,v in enumerate(atoms) if any(v[:6]))
assert O==1 and W==F(cert["objective"])
slacks={name:sum(z[j]*semantic[j][name] for j in range(257))-F(row["rhs"]) for name,row in raw.items()}
assert all(value>=0 for value in slacks.values())
assert {name:str(value) for name,value in slacks.items()}==cert["raw_row_slacks"]
y={name:F(value) for name,value in cert["dual"]["row_weights"].items()}
assert all(value>0 for value in y.values())
nu=F(cert["dual"]["normalization_multiplier"])
dual_value=nu+sum(weight*F(raw[name]["rhs"]) for name,weight in y.items())
assert dual_value==W==F(cert["dual"]["objective"])
res=[]
for j in range(257):
    c=F(j<256 and any(atoms[j][:6]));o=F(atoms[j][7]) if j<256 else F(0)
    rem=c-nu*o-sum(weight*semantic[j][name] for name,weight in y.items())
    assert rem>=0 and rem==F(cert["dual"]["nonnegative_column_residual"].get(str(j),"0"))
    assert rem*z[j]==0
    res.append(rem)
assert all(slacks[name]*weight==0 for name,weight in y.items())
assert W>=alpha1
global_scale=lcm(nu.denominator,*(value.denominator for value in y.values()))
scaled_res=[value*global_scale for value in res]
integer_multiplier=lcm(*(value.denominator for value in scaled_res))
global_identity={"scale":str(global_scale),"objective_numerator":str(W*global_scale),
    "integer_budget_weights":{name:str(value*global_scale) for name,value in y.items()},
    "residual_integer_multiplier":integer_multiplier,
    "smallest_positive_scaled_residual":str(min(value for value in scaled_res if value>0)),
    "K_residual":str(scaled_res[256])}
assert all((value*global_scale).denominator==1 for value in y.values())
assert (W*global_scale).denominator==1
(HERE/"global_identity.json").write_text(json.dumps(global_identity,indent=2)+"\n")
with (HERE/"integer_residual_table.tsv").open("w") as out:
    out.write("a1a2a3a4a5a6\tx0_o0\tx0_o1\tx1_o0\tx1_o1\n")
    for mask in range(64):
        values=[scaled_res[4*mask+k]*integer_multiplier for k in range(4)]
        assert all(value.denominator==1 and value>=0 for value in values)
        bits="".join(map(str,atoms[4*mask][:6]))
        out.write(bits+"\t"+"\t".join(map(str,values))+"\n")
appendix=json.loads((HERE/"root_refinement_diagnostic.json").read_text())
assert appendix["included_in_219_row_input"] is False
u1=sum(z[j]*F(atoms[j][0],sum(atoms[j][:6])) for j in range(256) if sum(atoms[j][:6]))
H=150*u1-F(139,6)*z[256]-O;L=10980*u1-1658*z[256]-87*O
J=67140*u1-9878*z[256]-627*O
assert H==F(appendix["point_H"])>0 and L==0 and J==F(appendix["point_J"])<0
assert J==13*L-504*H and kappa_min==0
assert "ROOT_REFINEMENT_APPENDIX" not in raw
with (HERE/"dual_column_checks.tsv").open("w") as out:
    out.write("column\ta1a2a3a4a5a6\tx\to\texact_nonnegative_residual\n")
    for j,value in enumerate(res):
        t=atoms[j] if j<256 else None
        out.write(f'{j}\t{"".join(map(str,t[:6])) if t else "K"}\t{t[6] if t else "-"}\t{t[7] if t else "-"}\t{value}\n')
final={**source_report,"status":"PASS: exact matching primal/dual; all sources and columns independently checked",
    "scope":"complete source and exact primal/dual certificate check; checker performs no optimization",
    "objective":str(W),"objective_decimal":float(W),"half_gap":str(F(1,2)-W),
    "primal_positive_atoms":sum(v>0 for v in z[:256]),"primal_K":str(z[256]),
    "positive_dual_rows":len(y),"dual_columns_checked":257,"zero_duality_gap":True,
    "new_row_slacks":{name:str(slacks[name]) for name in ["ROOT_BRANCH_NEW","TRUE_X_TAIL_CUT"]},
    "new_row_dual_weights":{name:str(y.get(name,F(0))) for name in ["ROOT_BRANCH_NEW","TRUE_X_TAIL_CUT"]},
    "zero_dual_columns":[j for j,value in enumerate(res) if value==0],
    "positive_dual_columns":sum(value>0 for value in res),
    "separate_appendix_128_kappa_checks":True,"separate_appendix_not_in219":True,
    "point_refinement_violation":str(J),
    "original_model_scope":"universal lower bound from the nonnegative dual; primal point remains only a necessary-system point"}
(HERE/"checker_output.json").write_text(json.dumps(final,indent=2)+"\n")
assert all(sha(RUN/name)==digest for name,digest in protected.items())
print(json.dumps(final,indent=2))
