#!/usr/bin/env python3
"""Check frozen CA07 receipts and catalog already-written evidence only."""
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[3]
P = ROOT / "work/notes-f86b97e0dd5e406a/notes/CA07/project"
D = P / "audit/recovery-merge"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(path, value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

declared = {
 "proposals/ca07_visual/post-recovery/boss-candidate-check.json":"e3a5f5256f7c56d7d1b9144112e6c7496538c08218cfe5aab6f74fdabbcccf5c",
 "proposals/ca07_visual/post-recovery/boss-candidate-check.md":"d857fa30878c427759eeb5fde0dfcfe060569defe01f57208efbac1f95078b55",
 "proposals/ca07_visual/post-recovery/p5-and-p3-followup.json":"4de9dcbe7c802e2ec9a0ef8eabefbd3ccd4a35624680fc98c3fed4475a912113",
 "proposals/ca07_visual/post-recovery/p5-and-p3-followup.md":"4fc1c14090f67020924ee82fc7ff6af19203a8174aee09fd1c325e16d94204f9",
 "proposals/ca07_visual/post-recovery/p3-first-index-native-1200.png":"8ffe96fd111d2981b23356929f479fced53af7fd1af8f51f90244a19a5cbe760",
 "proposals/ca07_visual/post-recovery/p5-multiply-verb-native-1200.png":"433bc1b57851691c9204bd147ae0b18af7074a977eb30f7c7541dc561d72afc8",
 "proposals/ca07_math/post-recovery/boss-candidate-check.json":"4673170853ddce6bfe064f2d0ce7dde50cc24d7e4a166a43b7bdd9b750033160",
 "proposals/ca07_math/post-recovery/boss-candidate-check.md":"ec422c6960485059086cac6bc4165c69b6c3b10c89da03160ade4dfae95d3634",
 "proposals/ca07_math/post-recovery/remaining-literals-check.json":"eaaed26fbcefe15e8825a23e5e2e18e1d9feaf4ba06b5ba84c194737e4c41650",
 "proposals/ca07_math/post-recovery/remaining-literals-check.md":"7e416cd578f327002eed08a683b5ebc1ca33767795e4cd9d228e48410a9b62a0",
 "proposals/ca07_math/post-recovery/zero-ring-note.md":"a25c54602a66eaf28b20833998e830b2ad6b1df8e8c6149da43635ed99ef0070",
 "proposals/ca07_math/post-recovery/intermediate-module-counterexample.md":"4693ad66295f1a2d4fee22fb8dbdd45b54f19d08de843682ccb2c0325a089b06",
 "proposals/ca07_adversarial/post-recovery/boss-candidate-check.json":"1390a8dcecbd175c3ea288bfe9da2733ef84968d0f79fae9bed64a1b29cb27a3",
 "proposals/ca07_adversarial/post-recovery/boss-candidate-check.md":"100e5d4d690f617f496def74737847ceb3edd8b7cb21df12ca4aa849a12d8214",
 "proposals/ca07_adversarial/post-recovery/additional-readings.json":"ccd15c17ca2960feb58c50b9e40c1c294e40de7051204d8c5681cf68280bd3dc",
 "proposals/ca07_adversarial/post-recovery/additional-readings.md":"0e98a94e02e4380461fabc9a0f32594d382819af433e61b7083f4a6c0dd1b889",
 "proposals/ca07_adversarial/post-recovery/additional-crop-index.json":"ef7d51a2f24cf05bb7bc40944a952a2848c5e93b25bec8ece74a9aa90933c82c",
}
verified = []
for rel, expected in declared.items():
    actual = sha(P/rel)
    if actual != expected:
        raise ValueError("Frozen-byte mismatch: "+rel)
    verified.append({"path":rel,"declared_sha256":expected,"actual_sha256":actual})

native = json.loads((P/"proposals/ca07_visual/post-recovery/p5-and-p3-followup.json").read_text())["native_crops"]
visual_index = []
for c in native:
    visual_index.append({
        "page_id":f"p{c['physical_page']:04d}",
        "bbox_px":c["crop_bbox_400dpi_px"],"dpi":c["dpi"],
        "path":c["path"],"sha256":c["sha256"]
    })
write(D/"visual-post-crop-index.json",visual_index)
for rel in ["proposals/ca07_adversarial/post-recovery/additional-crop-index.json",
            "audit/recovery-merge/visual-post-crop-index.json"]:
    for c in json.loads((P/rel).read_text()):
        if sha(P/c["path"]) != c["sha256"]:
            raise ValueError("Native crop byte mismatch: "+c["path"])
write(D/"post-proposal-receipts.json",{
    "note_id":"CA07","checks":"declared frozen bytes and indexed native image bytes",
    "metadata_check_only":True,"decisions_merged":False,"files":verified,
    "new_native_crop_count":11
})

observations = P/"proposals/ca07_visual/merge-observations/observations-merged.json"
labels = P/"proposals/ca07_visual/merge-observations/source-labels-merged.json"
if not observations.is_file() or not labels.is_file():
    raise SystemExit("Receipt verification done; waiting for actual visual observation handoff.")
for source,target in [(observations,D/"first-pass-observations.json"),
                      (labels,D/"source-labels.json")]:
    shutil.copyfile(source,target)
merged_labels = json.loads((D/"source-labels.json").read_text())
old_label = merged_labels["CA07-P003-U05"]
merged_labels["CA07-P003-U05"] = "φ_b(a_i) 展开中三处 a_i；首 d 下为 i、离体短横及长下笔，Boss按其无 j 大回钩的收势恢复为1并保留笔形限制；末为d_ri，省略处有两浅笔"
write(D/"source-labels.json",merged_labels)
write(D/"source-label-amendments.json",{
    "note_id":"CA07","author_id":"BossNotes-2ff3215d6446",
    "original_visual_labels_sha256":sha(labels),
    "amendments":[{
        "source_id":"CA07-P003-U05","prior_label":old_label,
        "merged_label":merged_labels["CA07-P003-U05"],
        "decision":"CA07-R018",
        "evidence_paths":["proposals/ca07_visual/post-recovery/p3-first-index-native-1200.png",
                          "audit/recovery-merge/boss-final-candidate-notes.md"]
    }]
})

text_files = []
for role in ["visual","math","adversarial"]:
    directory = P/f"proposals/ca07_{role}/recovery"
    for f in sorted(directory.rglob("*")):
        if f.is_file() and (f.suffix in [".md",".json",".txt"] or f.name=="SHA256SUMS"):
            text_files.append(f.relative_to(P).as_posix())
text_files += [p for p in declared if not p.endswith(".png")]
text_files += [p.relative_to(P).as_posix() for p in sorted(observations.parent.glob("*"))
               if p.suffix in [".json",".md"]]
for directory in ["audit/boss-recovery","audit/boss-recovery-2","audit/boss-recovery-3"]:
    for f in sorted((P/directory).glob("*")):
        if f.is_file() and f.suffix in [".md",".json",".txt"]:
            text_files.append(f.relative_to(P).as_posix())
text_files += [
    "audit/recovery-merge/frozen-proposal-receipts.json",
    "audit/recovery-merge/post-proposal-receipts.json",
    "audit/recovery-merge/boss-decisions.json",
    "audit/recovery-merge/boss-final-candidate-notes.md",
    "audit/recovery-merge/first-pass-observations.json",
    "audit/recovery-merge/source-labels.json",
    "audit/recovery-merge/source-label-amendments.json"
]
math_precheck = P/"proposals/ca07_math/post-recovery/merge-draft-math-check.md"
if math_precheck.is_file():
    text_files.append(math_precheck.relative_to(P).as_posix())
indexes = [
    "audit/boss-recovery/crop-index.json",
    "audit/boss-recovery-2/crop-index.json",
    "audit/boss-recovery-3/crop-index.json",
    "proposals/ca07_visual/recovery/crop-index.json",
    "proposals/ca07_math/recovery/crop-index.json",
    "proposals/ca07_adversarial/recovery/crop-index.json",
    "audit/recovery-merge/visual-post-crop-index.json",
    "proposals/ca07_adversarial/post-recovery/additional-crop-index.json",
    "assets/crop-index.json"
]
for rel in text_files+indexes:
    if not (P/rel).is_file():
        raise ValueError("An explicitly declared evidence file is absent: "+rel)
write(D/"catalog-inputs.json",{"text_files":sorted(set(text_files)),"crop_indexes":indexes})
print(json.dumps({"verified_declared_files":len(verified),
                  "catalog_text_files":len(set(text_files)),
                  "crop_indexes":len(indexes),"review_acceptance_generated":False}))
