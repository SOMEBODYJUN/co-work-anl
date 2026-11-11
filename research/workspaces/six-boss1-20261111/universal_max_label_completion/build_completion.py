#!/usr/bin/env python3
"""Deterministic exact C-membership construction. No optimizer is imported."""
from __future__ import annotations
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
from math import lcm
import hashlib
import json

HERE=Path(__file__).resolve().parent
RUN=HERE.parent
ROOT=HERE.parents[3]
OLD=RUN/"universal_union_wallet_lp"
EXPECTED_INPUT="f87a60372dee7449332b17721be6aa70012fb3aca251825cb2e9dd755ff01e41"
EXPECTED_CERT="ccc085060427e2999a8e4f00ac3414d7e20a1c6e66aeba8d3e658ae34cb16c85"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


assert sha(OLD/"exact_input.json")==EXPECTED_INPUT
assert sha(OLD/"exact_certificate.json")==EXPECTED_CERT
old_input=json.loads((OLD/"exact_input.json").read_text())
old_cert=json.loads((OLD/"exact_certificate.json").read_text())
release=json.loads((RUN/"main_universal_union_wallet_check.json").read_text())
assert release["status"]=="PASS" and release["input_sha256"]==EXPECTED_INPUT
assert release["certificate_sha256"]==EXPECTED_CERT
frozen_files=sorted(f for f in OLD.iterdir() if f.is_file())+[RUN/"universal_union_wallet_lp.md"]
frozen_hashes={str(f.relative_to(RUN)):sha(f) for f in frozen_files}
(HERE/"frozen_parent_hashes.json").write_text(json.dumps(frozen_hashes,indent=2)+"\n")

atoms={a["index"]:tuple(a["a"])+(a["x"],a["o"]) for a in old_input["atom_columns"]}
z={int(j):F(value) for j,value in old_cert["primal"].items() if int(j)<256}
support=sorted(z)
assert len(support)==13
K=F(old_cert["K"])
D={j:sum(atoms[j][:4])+1 for j in support}
u=[sum(z[j]*F(atoms[j][i],sum(atoms[j][:6]))
       for j in support if sum(atoms[j][:6])) for i in range(6)]
q={role:{j:F(atoms[j][role-1]) if role<8 else F(atoms[j][7],6)
         for j in support} for role in range(1,9)}
sizes={role:sum(z[j]*q[role][j] for j in support) for role in q}
f={role:sum(z[j]*q[role][j]/D[j] for j in support) for role in q}
FX=f[7]
raw=[]


def add(name,family,constant,coefficients):
    raw.append({"name":name,"family":family,"constant":F(constant),
                "coefficients":{j:F(coefficients(j)) for j in support}})


add("FMAX_C","FMAX",FX,lambda j:-F(1,D[j]))
for i in range(6):
    add(f"SAFE_{i+1}_C","SAFE",u[i],lambda j,i=i:-F(1,sum(atoms[j][:i])+6-i))
add("MX_C","MX",u[4],lambda j:-F(1,D[j]+atoms[j][6]))
for role in range(1,9):
    add(f"RC_C_{role}","RC",u[4]+FX-f[role],
        lambda j,role=role:-F(1,D[j])+q[role][j]/(D[j]*(D[j]+1)))
add("RC_C_C","RC",u[4]+FX,lambda j:-F(2,D[j])+F(1,D[j]*(D[j]+1)))
for role in range(1,9):
    add(f"RIG_C_{role}","RIG_C_ANCHOR",25*u[0]+3*K-sizes[role],
        lambda j,role=role:-7+F(5,6)*q[role][j])
add("RIG_C_C","RIG_C_ANCHOR",25*u[0]+3*K,lambda j:-F(43,6))
for role in range(1,8):
    add(f"RIG_{role}_C","RIG_C_QUERY",25*u[0]+3*K-7*sizes[role],
        lambda j,role=role:-1+F(5,6)*q[role][j])
for subset in combinations(range(1,8),5):
    bit={j:int(any(atoms[j][r-1] for r in subset)) for j in support}
    add("OPT6_C_"+"_".join(map(str,subset)),"OPT6",1-sum(z[j]*bit[j] for j in support),
        lambda j,bit=bit:bit[j]-1)
assert len(raw)==54

unique=[];seen={}
for r in raw:
    key=(r["constant"],tuple(r["coefficients"][j] for j in support))
    if key in seen:
        unique[seen[key]]["aliases"].append(r["name"])
    else:
        seen[key]=len(unique)
        unique.append({**r,"aliases":[r["name"]]})


def encode_row(r):
    return {**r,"constant":str(r["constant"]),
            "coefficients":{str(j):str(v) for j,v in r["coefficients"].items()}}


sources=[
    "archives/customer-attraction/state/引理/真实末回复的共同潜力上限与重叠参数端点--引理.md",
    "archives/customer-attraction/state/引理/任意人数近饱和根主题刚性--引理.md",
]
input_data={
    "scope":"membership completion of one true globally maximum-cardinality legal label C at one fixed necessary-projection point",
    "original_input_sha256":EXPECTED_INPUT,"original_certificate_sha256":EXPECTED_CERT,
    "main_release_sha256":sha(RUN/"main_universal_union_wallet_check.json"),
    "fixed_atoms":[{"index":j,"a":list(atoms[j][:6]),"x":atoms[j][6],"o":atoms[j][7],"z":str(z[j])} for j in support],
    "all_other_original_atom_masses":"0; their C-membership is forced to zero by 0<=e<=z",
    "K":str(K),"bounds":{str(j):["0",str(z[j])] for j in support},
    "equality":{"coefficients":{str(j):"1" for j in support},"rhs":str(K)},
    "row_convention":"constant + sum coefficients[j] * e[j] >= 0",
    "raw_rows":[encode_row(r) for r in raw],"unique_rows":[encode_row(r) for r in unique],
    "raw_row_count":len(raw),"unique_row_count":len(unique),
    "source_sha256":{p:sha(ROOT/p) for p in sources},
    "source_derivations_sha256":sha(HERE/"source_derivations.md"),
}
(HERE/"exact_input.json").write_text(json.dumps(input_data,indent=2,ensure_ascii=False)+"\n")

delta=K-sizes[4]
assert delta>0
e={j:z[j]*atoms[j][3] for j in support}
e[11]+=F(42,5)*delta
e[241]-=F(37,5)*delta
assert all(0<=e[j]<=z[j] for j in support)
assert sum(e.values())==K
slack={r["name"]:r["constant"]+sum(r["coefficients"][j]*e[j] for j in support) for r in raw}
assert all(s>=0 for s in slack.values())
den=lcm(*(value.denominator for value in list(z.values())+list(e.values())+[K]))
cert={
    "claim":"FEASIBLE membership completion for this exact old point and this requested necessary family only",
    "optimizer_calls":0,"discovery_method":"explicit A4 repair: add 42delta/5 at atom11, remove 37delta/5 at atom241",
    "input_sha256":sha(HERE/"exact_input.json"),"original_input_sha256":EXPECTED_INPUT,"original_certificate_sha256":EXPECTED_CERT,
    "delta":str(delta),"K":str(K),"e":{str(j):str(e[j]) for j in support},
    "positive_e":{str(j):str(e[j]) for j in support if e[j]},
    "split_C0":{str(j):str(z[j]-e[j]) for j in support},
    "split_C1":{str(j):str(e[j]) for j in support},
    "common_integer_scale":str(den),
    "integer_split_C0":{str(j):str((z[j]-e[j])*den) for j in support},
    "integer_split_C1":{str(j):str(e[j]*den) for j in support},
    "integer_K":str(K*den),"sum_e":str(sum(e.values())),
    "f_C":str(sum(e[j]/D[j] for j in support)),"F_X":str(FX),
    "new_row_slacks":{name:str(value) for name,value in slack.items()},
    "tight_new_rows":[name for name,value in slack.items() if value==0],
    "unchanged_W":old_cert["objective"],
    "not_claimed":["full catalog or SPE realization","new universal cut","half coverage","feasibility of every earlier optimal-face point"],
}
(HERE/"exact_completion.json").write_text(json.dumps(cert,indent=2)+"\n")
with (HERE/"exact_row_checks.tsv").open("w") as out:
    out.write("row\tfamily\texact_slack\tstatus\n")
    for r in raw:
        value=slack[r["name"]]
        out.write(f'{r["name"]}\t{r["family"]}\t{value}\t{"tight" if value==0 else "positive"}\n')
report={"status":"exact explicit completion found; no phase-I call needed","optimizer_calls":0,
        "variables":13,"raw_rows":len(raw),"unique_rows":len(unique),
        "delta":str(delta),"positive_C_membership_atoms":sum(v>0 for v in e.values()),
        "tight_rows":cert["tight_new_rows"],"f_C":cert["f_C"],"f_C_float":float(F(cert["f_C"])),
        "F_X_float":float(FX),"smallest_positive_slack":str(min(s for s in slack.values() if s>0)),
        "common_integer_scale":str(den)}
(HERE/"discovery_output.json").write_text(json.dumps(report,indent=2)+"\n")
assert all(sha(RUN/name)==value for name,value in frozen_hashes.items())
print(json.dumps(report,indent=2))
