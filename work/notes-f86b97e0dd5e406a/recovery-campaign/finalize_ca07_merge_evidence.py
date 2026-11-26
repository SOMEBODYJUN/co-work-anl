#!/usr/bin/env python3
"""Bind verified replacement rasters and explicit comparison-source edges."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[3]
P = ROOT/"work/notes-f86b97e0dd5e406a/notes/CA07/project"
sys.path.insert(0,str(ROOT))
from tools.catalog_note_evidence import catalog
from tools.build_note_ledger import build

plan = json.loads((P/"content-plan.json").read_text())
ledger = json.loads((P/"ledger.json").read_text())
if ledger["final_rounds"] or any(o["pass"]==2 for o in plan["observations"]):
    raise SystemExit("This pre-review metadata fix refuses an accepted/final version.")
reconciliation = json.loads((P/"audit/boss-recovery-4/renderer-reconciliation.json").read_text())
new = catalog(P,{
    "text_files":["audit/boss-recovery-4/renderer-reconciliation.json"],
    "crop_indexes":["audit/boss-recovery-4/crop-index.json"]
})
old_by_path = {a["path"]:a for a in plan["evidence_artifacts"]}
replacements = {}
removed = []
for row in reconciliation["replacements"]:
    old = old_by_path[row["original_path"]]
    replacements["artifact:"+old["id"]] = new["path_to_evidence_id"][row["canonical_path"]]
    removed.append(old["id"])
plan["evidence_artifacts"] = [
    a for a in plan["evidence_artifacts"] if a["id"] not in removed
] + new["evidence_artifacts"]

def replace_refs(value):
    if isinstance(value,str):
        return replacements.get(value,value)
    if isinstance(value,list):
        return [replace_refs(v) for v in value]
    if isinstance(value,dict):
        return {k:replace_refs(v) for k,v in value.items()}
    return value

plan = replace_refs(plan)
reconciliation_eid = new["path_to_evidence_id"]["audit/boss-recovery-4/renderer-reconciliation.json"]
for recovery in plan["recoveries"]:
    if recovery["id"] in ["CA07-R018","CA07-R030"]:
        recovery["evidence_ids"] = sorted(set(recovery["evidence_ids"]+[reconciliation_eid]))
        for k in ["forward_validation","backward_validation","return_to_image"]:
            recovery[k]["evidence_ids"] = sorted(set(recovery[k]["evidence_ids"]+[reconciliation_eid]))

t = {b["id"]:b for b in plan["transcription_blocks"]}
s = {b["id"]:b for b in plan["study_blocks"]}
for b,source in [(t["CA07-TRANSCRIPTION-033"],"CA07-P001-U10"),
                 (t["CA07-TRANSCRIPTION-034"],"CA07-P003-U06"),
                 (s["CA07-STUDY-016"],"CA07-P001-U10")]:
    b["source_ids"] = sorted(set(b["source_ids"]+[source]))
    b["explanation"] += "；补登记字形对照中直接引用的同篇原字来源。"
by_path = {a["path"]:"artifact:"+a["id"] for a in plan["evidence_artifacts"]}
for blocks in [plan["transcription_blocks"],plan["study_blocks"]]:
    for b in blocks:
        b["evidence_ids"] = sorted(set(b.get("evidence_ids",[])+[
            by_path[f"audit/source-units-800/{sid}-800.png"] for sid in b["source_ids"]
        ]))
(P/"content-plan.json").write_text(json.dumps(plan,ensure_ascii=False,indent=2)+"\n")
result = build(P)
result["canonical_raster_replacements"] = len(replacements)
result["independent_acceptance_generated"] = False
print(json.dumps(result,ensure_ascii=False,indent=2))
