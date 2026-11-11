#!/usr/bin/env python3
"""Freeze the completed v2 one-call result and its full-face equality exclusion."""
from datetime import datetime,timezone
from hashlib import sha256
from pathlib import Path
from fractions import Fraction as F
import json
import re

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
BASE=HERE.parent
SOURCE=BASE/"visible_maximum_joint_v2"
sha=lambda p:sha256(p.read_bytes()).hexdigest()
dump=lambda p,v:p.write_text(json.dumps(v,indent=2)+"\n")
assert not (HERE/"freeze_manifest.json").exists(),"Already frozen."
pins=json.loads((HERE/"source_pins_at_solve.json").read_text())
for relative,digest in pins.items():
    assert sha(REPO/relative)==digest,(relative,"source changed")
cert=json.loads((HERE/"exact_certificate.json").read_text())
disc=json.loads((HERE/"discovery_output.json").read_text())
check=json.loads((HERE/"independent_check_result.json").read_text())
face=json.loads((HERE/"optimal_face.json").read_text())
branch=json.loads((HERE/"true_branch_equality_diagnostic.json").read_text())
assert cert["optimizer_calls"]==disc["optimizer_calls"]==1 and disc["success"]
assert check["status"].startswith("PASS")
assert face["certificate_sha256"]==branch["certificate_sha256"]==sha(HERE/"exact_certificate.json")
assert branch["face_sha256"]==sha(HERE/"optimal_face.json")
assert F(branch["uniform_contradiction_gap"])>0 and len(branch["all11_zero_states"])==11
assert branch["extra_0010_zero_state_retained"]
proof=(HERE/"proof.md").read_text()
den=F(cert["objective"]).denominator
table_records=re.findall(r"\| (\d+) \| `([^`]+)` \| (\d+) \|",proof)
assert len(table_records)==12
input_data=json.loads((SOURCE/"exact_input.json").read_text())
for index,name,numerator in table_records:
    i=int(index)
    assert input_data["raw_rows"][i]["name"]==name
    assert F(int(numerator),den)==F(cert["dual"]["raw_row_weights"][i])
assert len(input_data["raw_rows"])==1003 and input_data["variables"]==513
adjacent=BASE/"visible_maximum_joint_v2_solve.md"
textfiles=[p for p in HERE.iterdir() if p.is_file() and p.suffix in [".md",".py",".tsv",".json"]]+[adjacent]
for path in textfiles:
    assert not any(line.endswith((" ","\t")) for line in path.read_text().splitlines()),path.name
dump(HERE/"final_source_verification.json",{"status":"PASS_ALL_FROZEN_SOURCES_UNCHANGED",
    "optimizer_calls_in_verification":0,"source_count":len(pins),"sha256":pins,
    "proof_positive_payment_table_checked":12,"text_trailing_whitespace_lines":0})
artifacts={p.name:{"sha256":sha(p),"bytes":p.stat().st_size} for p in sorted(HERE.iterdir())
           if p.is_file() and p.name not in ["freeze_manifest.json","SHA256SUMS"]}
artifacts["../visible_maximum_joint_v2_solve.md"]={"sha256":sha(adjacent),"bytes":adjacent.stat().st_size}
manifest={"status":"FROZEN_EXACT_FULL1003_OPTIMUM_AND_NS5_FACE_EXCLUSION","owner":"Boss1","RUN":"six-boss1-20261111",
    "frozen_utc":datetime.now(timezone.utc).isoformat(),"input_sha256":cert["input_sha256"],
    "preparation_manifest_sha256":sha(SOURCE/"freeze_manifest.json"),
    "optimizer_calls_this_stage":1,"new_optimizer_calls_after_discovery":0,
    "raw_inequalities":1003,"nonnegative_columns":513,"equalities":2,
    "all_raw_rows_and_columns_preserved":True,"fixed_K":False,"support_restriction":False,"point_completion":False,
    "objective":cert["objective"],"objective_decimal":cert["objective_decimal"],
    "independent_full_fraction_check":check["status"],"positive_raw_rows":12,"positive_primal_coordinates":14,
    "zero_dual_residual_columns":21,"whole_optimal_face_restricted_rank":14,
    "whole_face_true_SPE_exclusion":"NS5 tight => actual u2=K/5; whole face has the strictly positive recorded u2-K/5.",
    "whole_face_contradiction_gap":branch["uniform_contradiction_gap"],"all11_NS5_zero_states_retained":True,
    "half_status":"OPEN","SPE_existence_claimed":False,"quantified_larger_infimum_claimed":False,
    "source_count_verified_unchanged":len(pins),"source_pins":pins,"artifacts":artifacts,
    "write_scope":["research/workspaces/six-boss1-20261111/visible_maximum_joint_v2_solve/",
                   "research/workspaces/six-boss1-20261111/visible_maximum_joint_v2_solve.md"]}
dump(HERE/"freeze_manifest.json",manifest)
entries=[(name,entry["sha256"]) for name,entry in artifacts.items()]
entries.append(("freeze_manifest.json",sha(HERE/"freeze_manifest.json")))
(HERE/"SHA256SUMS").write_text("".join(digest+"  "+name+"\n" for name,digest in sorted(entries)))
print(json.dumps({"status":manifest["status"],"manifest_sha256":sha(HERE/"freeze_manifest.json"),
    "certificate_sha256":sha(HERE/"exact_certificate.json"),"face_sha256":sha(HERE/"optimal_face.json"),
    "branch_diagnostic_sha256":sha(HERE/"true_branch_equality_diagnostic.json"),
    "SHA256SUMS_sha256":sha(HERE/"SHA256SUMS"),"artifacts":len(artifacts),"sources":len(pins)},indent=2))
