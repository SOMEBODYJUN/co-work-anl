#!/usr/bin/env python3
"""Independent deterministic Fraction checker. No optimizer/builder imports."""
from fractions import Fraction as F
from itertools import combinations,product
from pathlib import Path
from collections import Counter
import hashlib
import json

HERE=Path(__file__).resolve().parent
RUN=HERE.parent
OLD=RUN/"universal_union_wallet_lp"
EXPECTED_INPUT="f87a60372dee7449332b17721be6aa70012fb3aca251825cb2e9dd755ff01e41"
EXPECTED_CERT="ccc085060427e2999a8e4f00ac3414d7e20a1c6e66aeba8d3e658ae34cb16c85"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert sha(OLD/"exact_input.json")==EXPECTED_INPUT
assert sha(OLD/"exact_certificate.json")==EXPECTED_CERT
parent_hashes=json.loads((HERE/"frozen_parent_hashes.json").read_text())
assert all(sha(RUN/name)==digest for name,digest in parent_hashes.items())
old_input=json.loads((OLD/"exact_input.json").read_text())
old_cert=json.loads((OLD/"exact_certificate.json").read_text())
inp=json.loads((HERE/"exact_input.json").read_text())
cert=json.loads((HERE/"exact_completion.json").read_text())
assert sha(HERE/"exact_input.json")==cert["input_sha256"]
assert inp["original_input_sha256"]==cert["original_input_sha256"]==EXPECTED_INPUT
assert inp["original_certificate_sha256"]==cert["original_certificate_sha256"]==EXPECTED_CERT
assert cert["optimizer_calls"]==0
atoms=[tuple(a["a"])+(a["x"],a["o"]) for a in old_input["atom_columns"]]
assert atoms==list(product((0,1),repeat=8))
z=[F(old_cert["primal"].get(str(j),"0")) for j in range(256)]
K=F(old_cert["primal"]["256"])
assert K==F(old_cert["K"])==F(inp["K"])==F(cert["K"])
support=[j for j in range(256) if z[j]>0]
assert len(support)==13
assert [r["index"] for r in inp["fixed_atoms"]]==support
for r in inp["fixed_atoms"]:
    j=r["index"]
    assert tuple(r["a"])+(r["x"],r["o"])==atoms[j]
    assert F(r["z"])==z[j]
    assert [F(v) for v in inp["bounds"][str(j)]]==[F(0),z[j]]
e=[F(cert["e"].get(str(j),"0")) for j in range(256)]
assert set(map(int,cert["e"]))==set(support)
assert all(0<=e[j]<=z[j] for j in range(256))
assert sum(e)==K
assert inp["equality"]["coefficients"]=={str(j):"1" for j in support}
assert F(inp["equality"]["rhs"])==K

# Confirm the explicit repair rather than trusting stored coordinates alone.
size_A4=sum(z[j]*atoms[j][3] for j in range(256))
delta=K-size_A4
assert delta>0 and delta==F(cert["delta"])
for j in range(256):
    expected=z[j]*atoms[j][3]
    if j==11: expected+=F(42,5)*delta
    if j==241: expected-=F(37,5)*delta
    assert e[j]==expected

P=[sum(t[:4]) for t in atoms]
D=[p+1 for p in P]
u=[sum(z[j]*F(atoms[j][i],sum(atoms[j][:6])) for j in range(256) if sum(atoms[j][:6]))
   for i in range(6)]
W=sum(z[j] for j in range(256) if any(atoms[j][:6]))
O=sum(z[j]*atoms[j][7] for j in range(256))
assert O==1 and W==F(old_cert["objective"])==F(cert["unchanged_W"])
q=[[F(t[r]) for t in atoms] for r in range(7)]+[[F(t[7],6) for t in atoms]]
f=[sum(z[j]*qr[j]/D[j] for j in range(256)) for qr in q]
sizes=[sum(z[j]*qr[j] for j in range(256)) for qr in q]
FX=f[6]
assert all(sizes[r]<=K for r in range(7))


def all_new_values(membership):
    """Independent direct functional evaluation of the 54 source formulas."""
    csize=sum(membership)
    fc=sum(membership[j]/D[j] for j in range(256))
    values={"FMAX_C":FX-fc}
    for i in range(6):
        gain=sum(membership[j]/(sum(atoms[j][:i])+6-i) for j in range(256))
        values[f"SAFE_{i+1}_C"]=u[i]-gain
    values["MX_C"]=u[4]-sum(membership[j]/(D[j]+atoms[j][6]) for j in range(256))
    for r,qr in enumerate(q,1):
        overlap=sum(membership[j]*qr[j]/(D[j]*(D[j]+1)) for j in range(256))
        values[f"RC_C_{r}"]=u[4]+FX-fc-f[r-1]+overlap
        query_outside=sum(z[j]*qr[j]-F(5,6)*membership[j]*qr[j] for j in range(256))
        values[f"RIG_C_{r}"]=25*u[0]+3*K-7*csize-query_outside
    self_overlap=sum(membership[j]/(D[j]*(D[j]+1)) for j in range(256))
    values["RC_C_C"]=u[4]+FX-2*fc+self_overlap
    values["RIG_C_C"]=25*u[0]+3*K-7*csize-csize/6
    for r in range(7):
        true_C_query=sum(membership[j]*(1-F(5,6)*atoms[j][r]) for j in range(256))
        values[f"RIG_{r+1}_C"]=25*u[0]+3*K-7*sizes[r]-true_C_query
    for subset in combinations(range(7),5):
        union_mass=F(0)
        for j in range(256):
            if any(atoms[j][r] for r in subset):
                union_mass+=z[j]
            else:
                union_mass+=membership[j]
        name="OPT6_C_"+"_".join(str(r+1) for r in subset)
        values[name]=1-union_mass
    assert len(values)==54
    return values


raw={r["name"]:r for r in inp["raw_rows"]}
base=all_new_values([F(0)]*256)
assert set(raw)==set(base) and len(raw)==54
for name in raw:
    assert F(raw[name]["constant"])==base[name]
for j in support:
    basis=[F(0)]*256;basis[j]=F(1)
    with_basis=all_new_values(basis)
    for name in raw:
        assert F(raw[name]["coefficients"][str(j)])==with_basis[name]-base[name]
seen={};ordered=[]
for r in inp["raw_rows"]:
    key=(F(r["constant"]),tuple(F(r["coefficients"][str(j)]) for j in support))
    if key in seen:
        seen[key].append(r["name"])
    else:
        seen[key]=[r["name"]];ordered.append(r["name"])
assert len(seen)==inp["unique_row_count"]==38
assert [r["name"] for r in inp["unique_rows"]]==ordered
for r in inp["unique_rows"]:
    key=(F(r["constant"]),tuple(F(r["coefficients"][str(j)]) for j in support))
    assert r["aliases"]==seen[key]
slacks=all_new_values(e)
assert all(v>=0 for v in slacks.values())
assert {name:str(value) for name,value in slacks.items()}==cert["new_row_slacks"]
assert set(cert["tight_new_rows"])=={name for name,value in slacks.items() if value==0}

# Old rows are unchanged and still all hold, evaluated directly from the pinned matrix.
old_point=z+[K]
old_slacks={}
for r in old_input["raw_rows"]:
    value=sum(F(coeff)*old_point[int(j)] for j,coeff in r["a"].items())-F(r["rhs"])
    assert value>=0
    assert value==F(old_cert["raw_row_slacks"][r["name"]])
    old_slacks[r["name"]]=value
assert len(old_slacks)==217

scale=F(cert["common_integer_scale"])
assert scale.denominator==1
for j in support:
    assert F(cert["split_C1"][str(j)])==e[j]
    assert F(cert["split_C0"][str(j)])==z[j]-e[j]
    assert e[j]*scale==F(cert["integer_split_C1"][str(j)])
    assert (z[j]-e[j])*scale==F(cert["integer_split_C0"][str(j)])
    assert (e[j]*scale).denominator==((z[j]-e[j])*scale).denominator==1
assert K*scale==F(cert["integer_K"])
fc=sum(e[j]/D[j] for j in range(256))
assert fc==F(cert["f_C"]) and FX==F(cert["F_X"])

with (HERE/"membership_split.tsv").open("w") as out:
    out.write("atom\ta1a2a3a4a5a6\tx\to\tz\te_C1\tz_minus_e_C0\tinteger_C1\tinteger_C0\n")
    for j in support:
        t=atoms[j]
        values=[j,"".join(map(str,t[:6])),t[6],t[7],z[j],e[j],z[j]-e[j],e[j]*scale,(z[j]-e[j])*scale]
        out.write("\t".join(map(str,values))+"\n")
family_summary={}
for family in sorted(set(r["family"] for r in raw.values())):
    selected=[slacks[name] for name,r in raw.items() if r["family"]==family]
    family_summary[family]={"rows":len(selected),"minimum_slack":str(min(selected)),"tight":sum(v==0 for v in selected)}

# A later Main result is checked separately, never inserted into this feasible family.
later=json.loads((HERE/"later_branch_comparison.json").read_text())
assert later["included_in_54_row_completion"] is False
H=150*u[0]-F(139,6)*K-O
new_branch_slack=10980*u[0]-1658*K-87*O
assert H==0 and new_branch_slack==F(later["exact_slack"])<0
assert new_branch_slack==F(3,5)*(63*K-23*O)
assert all(sha(RUN/name)==digest for name,digest in parent_hashes.items())
report={
    "status":"PASS: exact feasible largest-label membership completion for this fixed point",
    "optimizer_calls":0,"optimizer_imported":False,
    "pinned_original_input_sha256":EXPECTED_INPUT,"pinned_original_certificate_sha256":EXPECTED_CERT,
    "frozen_parent_files_unchanged":len(parent_hashes),
    "old_atom_columns_retained":256,"old_rows_rechecked":217,
    "new_membership_variables_on_positive_support":13,"forced_zero_membership_variables":243,
    "new_raw_rows":54,"new_unique_rows":38,
    "semantic_coefficients_rebuilt":54*13,"semantic_constants_rebuilt":54,
    "membership_lower_and_upper_bounds_checked":512,
    "positive_C_membership_atoms":sum(v>0 for v in e),
    "positive_split_atoms":sum(v>0 for v in e)+sum(z[j]>e[j] for j in range(256)),
    "sum_e":str(sum(e)),"K":str(K),"unchanged_W":str(W),
    "delta":str(delta),"f_C":str(fc),"F_X":str(FX),
    "tight_rows":sorted(name for name,value in slacks.items() if value==0),
    "family_summary":family_summary,"universal_cut_produced":False,
    "later_branch_row_included_in_completion":False,
    "later_branch_row_separately_verified_negative":str(new_branch_slack),
    "interpretation":"This exact old projection point survives the specified maximum-size-label membership repair; no complete SPE or general completion claim.",
}
(HERE/"checker_output.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2))
