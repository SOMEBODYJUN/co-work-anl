#!/usr/bin/env python3
"""Assemble only. No optimizer is imported or called by this file."""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import hashlib,json

HERE=Path(__file__).resolve().parent
RUN=HERE.parent
OLD=RUN/"universal_union_wallet_lp"
TAIL=RUN/"universal_true_x_tail"
OLD_INPUT_SHA="f87a60372dee7449332b17721be6aa70012fb3aca251825cb2e9dd755ff01e41"
OLD_CERT_SHA="ccc085060427e2999a8e4f00ac3414d7e20a1c6e66aeba8d3e658ae34cb16c85"
TAIL_INPUT_SHA="367ab0932172ce10e459bdf390121d0a5ad825a1475b30e5bb5ae6105b797375"
TAIL_CERT_SHA="467d2b0f7415c8b51cce1aebe0a5784ece6da31822ce6630b767ab001883837e"
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(OLD/"exact_input.json")==OLD_INPUT_SHA
assert sha(OLD/"exact_certificate.json")==OLD_CERT_SHA
assert sha(TAIL/"exact_input.json.gz")==TAIL_INPUT_SHA
assert sha(TAIL/"exact_certificate.json")==TAIL_CERT_SHA
old=json.loads((OLD/"exact_input.json").read_text())
point=json.loads((OLD/"exact_certificate.json").read_text())
tail=json.loads((TAIL/"exact_certificate.json").read_text())
face=json.loads((RUN/"main_universal_wallet_face.json").read_text())
atoms=list(product((0,1),repeat=8))
assert [tuple(r["a"])+(r["x"],r["o"]) for r in old["atom_columns"]]==atoms
protected={}
for directory in [OLD,RUN/"universal_max_label_completion"]:
    for file in sorted(directory.iterdir()):
        if file.is_file():protected[str(file.relative_to(RUN))]=sha(file)
for file in [RUN/"universal_union_wallet_lp.md",RUN/"universal_max_label_completion.md"]:
    protected[str(file.relative_to(RUN))]=sha(file)
(HERE/"prior_frozen_hashes.json").write_text(json.dumps(protected,indent=2)+"\n")


def ui(v,i):
    c=sum(v[:6]);return F(v[i],c) if c else F(0)


def psi(v,y,t):
    b=sum(v[:3]);D=b+v[3]+1;d=b+v[6]+1;theta=F(v[7],6)
    return (F(4096*v[6],b+1+y+t)+F(800*y,D)+71*t
      +384*(theta-t)/(d+y)
      +512*((v[5]+theta)/d-F(v[5],d*(d+1))*theta-F(y,d+t)-F(t,d+y)-F(y,d*(d+1)))
      +900*((t+theta)/D-F(t,D*(D+1))*theta))


minima=[];cut=[]
for v in atoms:
    values=[psi(v,y,t) for y,t in product((0,1),repeat=2)]
    m=min(values);minima.append(m)
    cut.append(4096*ui(v,3)+900*ui(v,4)+F(1700*v[6],sum(v[:4])+1)-m)
assert len(tail["universal_cut"]["cut_z"])==256
assert all(cut[j]==F(tail["universal_cut"]["cut_z"][str(j)]) for j in range(256))
assert F(tail["universal_cut"]["cut_K"])==71
new=[10980*ui(v,0)-87*v[7] for v in atoms]+[-F(1658)]
cut=cut+[F(71)]


def row(name,family,coeff):
    return {"name":name,"family":family,"a":{str(j):str(v) for j,v in enumerate(coeff) if v},"rhs":"0"}


raw=old["raw_rows"]+[
    row("ROOT_BRANCH_NEW","ROOT_BRANCH_NEW",new),
    row("TRUE_X_TAIL_CUT","TRUE_X_TAIL_CUT",cut),
]
assert len(raw)==219
unique=[];seen={};zero=[]
for r in raw:
    key=(tuple(F(r["a"].get(str(j),"0")) for j in range(257)),F(r["rhs"]))
    if not any(key[0]) and key[1]==0:zero.append(r["name"])
    elif key in seen:unique[seen[key]]["aliases"].append(r["name"])
    else:seen[key]=len(unique);unique.append({**r,"aliases":[r["name"]]})
sources={
    "universal_union_wallet_lp/exact_input.json":OLD_INPUT_SHA,
    "universal_union_wallet_lp/exact_certificate.json":OLD_CERT_SHA,
    "universal_true_x_tail/exact_input.json.gz":TAIL_INPUT_SHA,
    "universal_true_x_tail/exact_certificate.json":TAIL_CERT_SHA,
}
for name in ["main_root_near_strengthening.md","main_root_near_strengthening_check.json",
             "main_universal_wallet_face.md","main_universal_wallet_face.json","universal_true_x_tail/proof.md"]:
    sources[name]=sha(RUN/name)
inp={
    "scope":"all256 actual/X/optimal-union atom types plus true global K; original217 rows plus two released-source candidates",
    "variables":257,"atom_columns":old["atom_columns"],"K_column":256,
    "nonnegative_columns":list(range(257)),"objective":old["objective"],"equality":old["equality"],
    "inequality_convention":"a dot z >= rhs","raw_rows":raw,"unique_rows":unique,
    "raw_inequality_count":219,"unique_inequality_count":len(unique),"removed_zero_rows":zero,
    "tail_minima":{str(j):str(m) for j,m in enumerate(minima)},
    "source_sha256":sources,"source_review_sha256":sha(HERE/"source_review.md"),
    "solve_permission":"Main explicit cut release is required separately; this input is not permission to optimize",
}
(HERE/"exact_input.json").write_text(json.dumps(inp,indent=2,ensure_ascii=False)+"\n")
z=[F(point["primal"].get(str(j),"0")) for j in range(257)]
diagnostics={"optimizer_calls":0,"old_W":point["objective"],
    "ROOT_BRANCH_NEW":str(sum(new[j]*z[j] for j in range(257))),
    "TRUE_X_TAIL_CUT":str(sum(cut[j]*z[j] for j in range(257))),
    "tail_minimum_sign_counts":{s:sum((m>0)-(m<0)==k for m in minima) for s,k in [("negative",-1),("zero",0),("positive",1)]},
    "all_256_types_included":True,"raw_rows":219,"unique_rows":len(unique),"variables":257,
    "lp_not_started":not (HERE/"single_lp_started.txt").exists()}
assert F(diagnostics["ROOT_BRANCH_NEW"])==F(-1050450649759127201835,142891298915142483961)
assert F(diagnostics["TRUE_X_TAIL_CUT"])==F(tail["fixed_projection_cut_value"])
(HERE/"old_point_diagnostics.json").write_text(json.dumps(diagnostics,indent=2)+"\n")
baseline=face["constructive_strict_bound"]
weights={name:F(v) for name,v in baseline["old_row_weights"].items()}
weights["ROOT_BRANCH_NEW"]=F(baseline["new_root_row_weight"])
alpha=F(baseline["bound"])
names={r["name"]:r for r in raw}
res=[]
for j in range(257):
    c=F(inp["objective"].get(str(j),"0"));eq=F(inp["equality"]["a"].get(str(j),"0"))
    r=c-alpha*eq-sum(w*F(names[name]["a"].get(str(j),"0")) for name,w in weights.items())
    assert r>=0 and r==F(baseline["nonnegative_column_residual"].get(str(j),"0"))
    res.append(r)
assert all(w>=0 for w in weights.values())
baseline_out={"scope":"existing Main strict dual extended to v2 with zero TRUE_X_TAIL_CUT weight; not new optimality",
    "bound":str(alpha),"bound_decimal":float(alpha),"row_weights":{n:str(w) for n,w in weights.items()},
    "TRUE_X_TAIL_CUT_weight":"0","normalization_multiplier":str(alpha),
    "nonnegative_column_residual":{str(j):str(v) for j,v in enumerate(res) if v},
    "all257_columns_verified":True,"optimizer_calls":0}
(HERE/"baseline_dual_extension.json").write_text(json.dumps(baseline_out,indent=2)+"\n")
assert all(sha(RUN/name)==digest for name,digest in protected.items())
print(json.dumps({**diagnostics,"baseline_bound":str(alpha),"baseline_bound_decimal":float(alpha),
                  "input_sha256":sha(HERE/"exact_input.json"),"explicit_Main_release_present":(HERE/"main_cut_release.json").exists()},indent=2))
