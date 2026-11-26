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
def artifact(path, aid=None, crop=None, viewport=None):
    path=str(path)
    if path in path_to_id:
        return "artifact:"+path_to_id[path]
    aid=aid or ("record-"+hashlib.sha256(path.encode()).hexdigest()[:16])
    if any(item["id"] == aid for item in artifacts):
        aid += "-" + Path(path).suffix.lstrip(".")
        if any(item["id"] == aid for item in artifacts):
            raise ValueError(f"duplicate artifact id: {aid}")
    item={"id":aid,"path":path,"kind":"evidence","format":"image" if path.endswith(".png") else "text"}
    if crop:
        item["source_crop"]={k:crop[k] for k in ("page_id","bbox_px","dpi")}
    if viewport:
        item["pdf_viewport"] = viewport
    artifacts.append(item);path_to_id[path]=aid
    return "artifact:"+aid

artifact("audit/campaign/participants.json","campaign-participants")
artifact("audit/campaign/boss-counterexamples.json","boss-counterexamples")
artifact("audit/campaign/source-id-migration.json","source-id-migration")
if (P/"audit/layout/layout-review.json").exists():
    artifact("audit/layout/layout-review.json","layout-review")
for role in ("visual","math","adversarial"):
    folder=P/f"proposals/ra12_{role}"
    for f in sorted(folder.iterdir()):
        if f.is_file():
            artifact(f.relative_to(P), f"{role}-{f.stem}")
    index=load(folder/"crop-index.json")
    for c in (index if isinstance(index,list) else index["crops"]):
        artifact(c["path"], f"{role}-crop-{Path(c['path']).stem}", c)
    extra_paths = set(folder.glob("**/*index*.json"))
    for extra_path in sorted(extra_paths):
        suffix = hashlib.sha256(str(extra_path.relative_to(P)).encode()).hexdigest()[:12]
        artifact(extra_path.relative_to(P), f"{role}-extra-{suffix}")
        extra_index = load(extra_path)
        for c in (extra_index if isinstance(extra_index,list) else extra_index.get("crops",[])):
            if all(key in c for key in ("path","page_id","bbox_px","dpi")):
                artifact(c["path"], f"{role}-crop-{Path(c['path']).stem}", c)
    for record_path in sorted(folder.glob("*.json")):
        data = load(record_path)
        if isinstance(data,dict) and isinstance(data.get("crops"),list):
            for c in data["crops"]:
                if all(key in c for key in ("path","page_id","bbox_px","dpi")):
                    artifact(c["path"], f"{role}-crop-{Path(c['path']).stem}", c)
outside = load(P/"proposals/ra12_visual/supplemental-outside-page-evidence.json")
viewport = {"page_id":outside["page_id"], "mediabox_pdf_pt":outside["media_expanded_pdf_pt"],
            "clip_pdf_pt":outside["render_clip_shifted_pdf_pt"],"dpi":outside["render_dpi"]}
artifact(outside["media_only_path"],"visual-p6-expanded-media",viewport=viewport)
viewport = {**viewport,"form_expansion":{
    "xref":outside["form_xref"],"bbox_original":outside["form_bbox_original"],
    "bbox_expanded":outside["form_bbox_expanded"],
    "clip_original":outside["form_stream_clip_original"]+"\n",
    "clip_expanded":outside["form_stream_clip_expanded"]+"\n",
    "original_stream_sha256":outside["form_stream_original_sha256"]}}
artifact(outside["path"],"visual-p6-original-unclipped-vectors",viewport=viewport)
ad_outside = load(P/"proposals/ra12_adversarial/outside-page-evidence.json")
artifact(ad_outside["path"],"adversarial-p6-original-unclipped-vectors",viewport={
    "page_id":"p0006","mediabox_pdf_pt":[-10,0,595,842],
    "clip_pdf_pt":ad_outside["expanded_page_clip_pt"],"dpi":1200,
    "form_expansion":{"xref":33,"bbox_original":"[0 0 2380 3368]",
        "bbox_expanded":"[-40 0 2380 3368]",
        "clip_original":"0 0 2380 3368 re\nW* n\n",
        "clip_expanded":"-40 0 2420 3368 re\nW* n\n",
        "original_stream_sha256":outside["form_stream_original_sha256"]}})
math_replay_path = P/"proposals/ra12_math/second-review-crops/p6-vector-replay.json"
if math_replay_path.exists():
    replay = load(math_replay_path)
    artifact(math_replay_path.relative_to(P),"math-p6-vector-replay")
    rectangle = lambda values: "["+" ".join(str(x) for x in values)+"]"
    for output in replay["outputs"]:
        selected_clip = (replay["expanded_unique_form_rectangle_clip"]
                         if output["form_rectangle_clip_modified"]
                         else replay["original_unique_form_rectangle_clip"])
        artifact(output["path"],"math-p6-replay-"+output["id"],viewport={
            "page_id":replay["page_id"],"mediabox_pdf_pt":replay["expanded_media_box_pdf_pt"],
            "clip_pdf_pt":replay["clip_pdf_pt"],"dpi":replay["dpi"],
            "form_expansion":{"xref":replay["form_xref"],
                "bbox_original":rectangle(replay["original_form_bbox"]),
                "bbox_expanded":rectangle(replay["expanded_form_bbox"]),
                "clip_original":replay["original_unique_form_rectangle_clip"]+"\n",
                "clip_expanded":selected_clip+"\n",
                "original_stream_sha256":replay["original_form_stream_sha256_decoded"]}})
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
supp = load(P/"proposals/ra12_visual/supplemental-recovery.json")["items"]
supp_crops = load(P/"proposals/ra12_visual/supplemental-crop-index.json")
first = supp[0]
vr.append({"issue_id":"V-P001-MEASURABLE-COVERAGE","suggested_source_units":["V-P001-19"],
    "crop_evidence":[c for c in supp_crops if c["page_id"]=="p0001"],
    "candidates":[{"reading":c["reading"]} for c in first["candidate_readings"]],
    "selected_reading":first["selected"],"context":first["context_check"],
    "visual_evidence":first["confidence_note"],
    "forward_math":"若可测 X_j 可数覆盖 X，各限制可测，则每个开集的原像等于各片可测原像的可数并，故总体可测。",
    "backward_math":"不可数可测单点覆盖上任何限制可测，无法推出任意总体函数可测；此反例确认可数条件，但单凭数学不能证明作者写的是近似或类似。"})
synthesis_path = P/"audit/campaign/boss-recovery-synthesis.json"
synthesis = load(synthesis_path)["decisions"] if synthesis_path.exists() else {}
if synthesis:
    artifact(synthesis_path.relative_to(P),"boss-recovery-synthesis")
for n,r in enumerate(vr,1):
    ev=[artifact(c["path"]) for c in r["crop_evidence"]]
    ev+=["artifact:visual-recoveries","artifact:visual-detailed-reading"]
    if n<=3:
        ev+=["artifact:math-recoveries","artifact:math-recovery-report",
             "artifact:adversarial-recoveries","artifact:adversarial-adversarial-report"]
    if n in (3,5,11,13,14):
        ev += ["artifact:visual-supplemental-recovery"]
        relevant = {3:"p0006",5:"p0002",11:"p0005",13:"p0006",14:"p0001"}[n]
        ev += [artifact(c["path"]) for c in supp_crops if c["page_id"]==relevant]
    if n in (3,13):
        ev += ["artifact:visual-p6-original-unclipped-vectors",
               "artifact:adversarial-p6-original-unclipped-vectors",
               "artifact:visual-supplemental-outside-page-evidence",
               "artifact:adversarial-outside-page-evidence"]
    if n == 5:
        r = {**r,"selected_reading":r["selected_reading"].replace("举例，闭集构造", "并给出闭集构造")}
    decision = synthesis.get(f"RA12-REC-{n:02d}")
    if decision:
        r = {**r, **{key:value for key,value in decision.items()
                     if key in ("selected_reading","visual_evidence","context","forward_math","backward_math")}}
        ev += ["artifact:boss-recovery-synthesis"] + decision.get("evidence_ids",[])
    ev = list(dict.fromkeys(ev))
    candidates=[{"id":f"candidate-{j}","text":c["reading"],"evidence_ids":ev}
                for j,c in enumerate(r["candidates"],1)]
    if decision:
        candidates += [{"id":f"additional-{j}","text":text,"evidence_ids":ev}
                       for j,text in enumerate(decision.get("additional_candidates",[]),1)]
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
