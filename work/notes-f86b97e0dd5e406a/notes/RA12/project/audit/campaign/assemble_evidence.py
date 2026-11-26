"""Bind separately authored records to the RA12 draft; never creates a review."""
from pathlib import Path
import json
import hashlib

P = Path(__file__).resolve().parents[2]
load = lambda p: json.loads(p.read_text(encoding="utf-8"))
write = lambda p,v: p.write_text(json.dumps(v, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
plan=load(P/"authored-content.json")
ids=load(P/"audit/campaign/source-id-migration.json")
artifacts=[]
path_to_id={}
def artifact(path, aid=None, crop=None):
    path=str(path)
    if path in path_to_id:
        return "artifact:"+path_to_id[path]
    aid=aid or ("record-"+hashlib.sha256(path.encode()).hexdigest()[:16])
    item={"id":aid,"path":path,"kind":"evidence","format":"image" if path.endswith(".png") else "text"}
    if crop:
        item["source_crop"]={k:crop[k] for k in ("page_id","bbox_px","dpi")}
    artifacts.append(item);path_to_id[path]=aid
    return "artifact:"+aid

artifact("audit/campaign/participants.json","campaign-participants")
artifact("audit/campaign/boss-counterexamples.json","boss-counterexamples")
artifact("audit/campaign/source-id-migration.json","source-id-migration")
for role in ("visual","math","adversarial"):
    folder=P/f"proposals/ra12_{role}"
    for f in sorted(folder.iterdir()):
        if f.is_file():
            artifact(f.relative_to(P), f"{role}-{f.stem}")
    index=load(folder/"crop-index.json")
    for c in (index if isinstance(index,list) else index["crops"]):
        artifact(c["path"], f"{role}-crop-{Path(c['path']).stem}", c)
for c in load(P/"audit/campaign/boss-crop-index.json"):
    artifact(c["path"],"boss-crop-"+Path(c["path"]).stem,c)
artifact("audit/campaign/boss-crop-index.json","boss-crop-index")

obs=load(P/"proposals/ra12_visual/observations.json")
normalized={"pages":[],"regions":[]}
for pid,page in obs["pages"].items():
    region_text=[r["observation"] for rid,r in obs["regions"].items() if rid.startswith(pid+"-")]
    normalized["pages"].append({"page_id":pid,"assessment":"blank" if page["blank"] else "content",
        "observation":"整页与重叠分区实查："+(" ".join(region_text)),
        "layout_observation":page["layout"]})
for rid,r in obs["regions"].items():
    normalized["regions"].append({"region_id":rid,"assessment":"blank" if r["blank"] else "content",
                                 "observation":r["observation"]})
op="audit/campaign/first-pass-observations.json"
write(P/op,normalized)
artifact(op,"first-pass-observations")
plan["observations"]=[{"pass":1,"reviewer_id":"/root/ra12_visual","session_id":"/root/ra12_visual",
                       "path":op,"artifact_id":"first-pass-observations"}]

recoveries=[]
issues=[]
vr=load(P/"proposals/ra12_visual/recoveries.json")["records"]
for n,r in enumerate(vr,1):
    ev=[artifact(c["path"]) for c in r["crop_evidence"]]
    ev+=["artifact:visual-recoveries","artifact:visual-detailed-reading"]
    if n<=3:
        ev+=["artifact:math-recoveries","artifact:math-recovery-report",
             "artifact:adversarial-recoveries","artifact:adversarial-adversarial-report"]
    candidates=[{"id":f"candidate-{j}","text":c["reading"],"evidence_ids":ev}
                for j,c in enumerate(r["candidates"],1)]
    candidates.append({"id":"selected-reading","text":r["selected_reading"],"evidence_ids":ev})
    # The author of the initial proposal is recorded truthfully. The required
    # nonauthor review is pending and must replace this only after actual review.
    recovery={"id":f"RA12-REC-{n:02d}","source_ids":[ids[i] for i in r["suggested_source_units"]],
        "problem":r["issue_id"]+"："+r.get("context",r["visual_evidence"]),
        "candidates":candidates,"selected_candidate_id":"selected-reading","status":"unresolved",
        "evidence_ids":ev,
        "forward_validation":{"status":"pass","method":"从原定义与前文条件进行正向推导",
                              "inputs":r.get("context","原稿当前段与前后定义"),"result":r["forward_math"],"evidence_ids":ev},
        "backward_validation":{"status":"pass","method":"从结论反查候选并检验反例和必要条件",
                               "inputs":r["selected_reading"],"result":r["backward_math"],"evidence_ids":ev},
        "return_to_image":{"observation":r["visual_evidence"],"evidence_ids":ev},
        "reviewer_id":"/root/ra12_visual","session_id":"/root/ra12_visual"}
    recoveries.append(recovery)
    issues.append({"id":f"RA12-ISSUE-{n:02d}","status":"open",
        "description":r["issue_id"]+"：初始候选已合并，等待最新正文上的非作者恢复复核。",
        "related_ids":recovery["source_ids"]+[recovery["id"]],"evidence_ids":ev,"resolution":""})
plan["recoveries"]=recoveries;plan["issues"]=issues
for source in plan["sources"]:
    if any(source["id"] in r["source_ids"] for r in recoveries):
        source["status"]="unresolved"
for blocks in (plan["transcription_blocks"],plan["study_blocks"]):
    for b in blocks:
        if any(s["id"] in b["source_ids"] and s["status"]=="unresolved" for s in plan["sources"]):
            b["status"]="unresolved"
plan["evidence_artifacts"]=artifacts
write(P/"content-plan.json",plan)
print(json.dumps({"evidence_artifacts":len(artifacts),"recovery_proposals":len(recoveries),
                  "pending_nonauthor_review":True},ensure_ascii=False))
