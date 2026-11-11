#!/usr/bin/env python3
"""Read-only source assembly and baseline extension; no optimizer."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json

HERE=Path(__file__).resolve().parent;RUN=HERE.parent;OLD=RUN/"universal_union_wallet_v2";ROOTTAIL=RUN/"maximal_root_tail_wallet"
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
pins={"universal_union_wallet_v2/exact_input.json":"bb7c66e141b9ab6080c5fbafe6c00f966a95247269ff54d2ae3abae7809f35f2",
      "universal_union_wallet_v2/exact_certificate.json":"12d4f059b7be021c8b3c89ed6adf3bde208750da6ce0eee79c383a813d50b36b",
      "maximal_root_tail_wallet/exact_input.json":"3c1a824ed0a17562da812db1d0bb12485f0b1c7f743577af7bc2ecf316d3ab65",
      "maximal_root_tail_wallet/exact_certificate.json":"80d9267b6ed9b5e47c4f8ea92523aaf1e73754eb28416e4117f8db754b88d771",
      "maximal_root_tail_wallet/freeze_manifest.json":"4bea954ad0b82adaf74e70cc381ad020372e42fc7a77b68b32fcc959ae8dbe55"}
assert all(sha(RUN/name)==digest for name,digest in pins.items())
old=json.loads((OLD/"exact_input.json").read_text());cert=json.loads((OLD/"exact_certificate.json").read_text())
release=json.loads((RUN/"main_universal_wallet_v2_check.json").read_text())
assert release["status"]=="PASS" and release["input_sha256"]==pins["universal_union_wallet_v2/exact_input.json"]
protected={}
for directory in [RUN/"universal_union_wallet_lp",RUN/"universal_max_label_completion",OLD]:
    for file in sorted(directory.iterdir()):
        if file.is_file():protected[str(file.relative_to(RUN))]=sha(file)
    summary=directory.with_suffix(".md");protected[str(summary.relative_to(RUN))]=sha(summary)
(HERE/"prior_frozen_hashes.json").write_text(json.dumps(protected,indent=2)+"\n")
atoms=[tuple(r["a"])+(r["x"],r["o"]) for r in old["atom_columns"]]


def newrow(name,family,U,K,O):
    a={}
    for j,v in enumerate(atoms):
        c=sum(v[:6]);u=F(v[0],c) if c else F(0);value=U*u-O*v[7]
        if value:a[str(j)]=str(value)
    a["256"]=str(-K)
    return {"name":name,"family":family,"a":a,"rhs":"0"}


raw=old["raw_rows"]+[
    newrow("ROOT_SIZE_FEEDBACK","ROOT_SIZE_FEEDBACK",67140,9878,627),
    newrow("ROOT_TRUE_TAIL","ROOT_TRUE_TAIL",112944305160,11595684007,2178783435),
]
assert len(raw)==221
seen={};unique=[];zero=[]
for r in raw:
    key=(tuple(F(r["a"].get(str(j),"0")) for j in range(257)),F(r["rhs"]))
    if not any(key[0]) and key[1]==0:zero.append(r["name"])
    elif key in seen:unique[seen[key]]["aliases"].append(r["name"])
    else:seen[key]=len(unique);unique.append({**r,"aliases":[r["name"]]})
sources={**old["source_sha256"],**pins}
for name in ["main_universal_wallet_v2_check.json","main_root_capacity_feedback.md","main_root_capacity_feedback.json",
             "main_maximal_root_tail_check.json","maximal_root_tail_wallet/proof.md"]:sources[name]=sha(RUN/name)
inp={"scope":"v3: full256 actual/X/O types and true global K; original219 rows plus exactly2 released root rows",
     "variables":257,"atom_columns":old["atom_columns"],"K_column":256,"nonnegative_columns":list(range(257)),
     "objective":old["objective"],"equality":old["equality"],"inequality_convention":"a dot z >= rhs",
     "raw_rows":raw,"unique_rows":unique,"raw_inequality_count":221,"unique_inequality_count":len(unique),
     "removed_zero_rows":zero,"tail_minima":old["tail_minima"],"source_sha256":sources,"source_review_sha256":sha(HERE/"source_review.md")}
(HERE/"exact_input.json").write_text(json.dumps(inp,indent=2,ensure_ascii=False)+"\n")
z=[F(cert["primal"].get(str(j),"0")) for j in range(257)]
diag={"optimizer_calls":0,"old_v2_W":cert["objective"],"old_v2_K":cert["K"],"new_row_slacks":{r["name"]:str(sum(F(a)*z[int(j)] for j,a in r["a"].items())) for r in raw[-2:]},"raw_rows":221,"unique_rows":len(unique),"variables":257}
assert all(F(v)<0 for v in diag["new_row_slacks"].values())
(HERE/"old_point_diagnostics.json").write_text(json.dumps(diag,indent=2)+"\n")
baseline={"scope":"v2 exact dual extended by zero weights on both new root rows; not v3 optimality",**cert["dual"],"optimizer_calls":0,"new_row_weights":{"ROOT_SIZE_FEEDBACK":"0","ROOT_TRUE_TAIL":"0"}}
weights={n:F(v) for n,v in baseline["row_weights"].items()};byname={r["name"]:r for r in raw};nu=F(baseline["normalization_multiplier"])
for j in range(257):
    value=F(inp["objective"].get(str(j),"0"))-nu*F(inp["equality"]["a"].get(str(j),"0"))-sum(w*F(byname[n]["a"].get(str(j),"0")) for n,w in weights.items())
    assert value>=0 and value==F(baseline["nonnegative_column_residual"].get(str(j),"0"))
(HERE/"baseline_dual_extension.json").write_text(json.dumps(baseline,indent=2)+"\n")
receipt={"decision":"Main explicitly released two new root rows and one257-column LP after source preflight",
         "authorized_by":"/root","source_pins":pins,"root_K_free_equality":"37375524862-25779840855=11595684007","no_extra_families":True,"input_sha256":sha(HERE/"exact_input.json")}
(HERE/"main_release.json").write_text(json.dumps(receipt,indent=2)+"\n")
assert all(sha(RUN/n)==h for n,h in protected.items())
print(json.dumps({**diag,"input_sha256":sha(HERE/"exact_input.json"),"prior_files_unchanged":len(protected)},indent=2))
