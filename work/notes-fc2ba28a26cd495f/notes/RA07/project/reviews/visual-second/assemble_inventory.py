import hashlib
import json
from pathlib import Path
from PIL import Image, ImageChops

P = Path("/workspace/scratch/5eb228b78d49/co-work-anl-notes/work/notes-fc2ba28a26cd495f/notes/RA07/project")
OUT = P / "reviews/visual-second"
RID = "/root/ra07_visual_second"
EXPECTED_SOURCE_SHA = "c053b24757b997ab489d1c18371df9ba44137919d53596b7158856ac1e8746c8"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write_text(path, value):
    path.write_text(value.rstrip() + "\n", encoding="utf-8")

def json_write(path, data):
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2))

def overlaps(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]

manifest = json.loads((P / "manifest.json").read_text(encoding="utf-8"))
# Approved crop input: only these four positional fields are used.
crop_input = json.loads((P / "proposals/rebuild/crops.json").read_text(encoding="utf-8"))
crop_rows = crop_input if isinstance(crop_input, list) else crop_input["crops"]
source_crops = {c["id"]: {key: c[key] for key in ("id", "path", "page_id", "bbox_px")} for c in crop_rows}
del crop_input, crop_rows
assert len(manifest["pages"]) == 13
assert sha(P / "source.pdf") == EXPECTED_SOURCE_SHA
assert manifest["source_pdf"]["sha256"] == EXPECTED_SOURCE_SHA

page_map = {x["id"]: x for x in manifest["pages"]}
image_records = []
crop_records = []
pages = []
all_units = []
source_crop_ids_seen = set()
metadata_checks = []

def image_metadata(rel, bbox, expected=None):
    path = P / rel
    actual_sha = sha(path)
    if expected:
        assert actual_sha == expected, rel
    with Image.open(path) as im:
        size = list(im.size)
    assert size == [bbox[2] - bbox[0], bbox[3] - bbox[1]], (rel, size, bbox)
    return {
        "path": rel,
        "absolute_path": str(path),
        "sha256": actual_sha,
        "bbox_px": bbox,
        "image_size_px": size,
        "actual_view_completed": True,
        "viewer": "tools.view_image",
        "display": "image(result.image_url)",
        "reviewer_id": RID,
        "session_id": RID,
    }

for number in range(1, 14):
    pid = f"p{number:04d}"
    checkpoint = OUT / f"page-{pid}.json"
    own = json.loads(checkpoint.read_text(encoding="utf-8"))
    assert own["reviewer_id"] == RID and own["session_id"] == RID
    assert len(own["regions"]) == 6
    mp = page_map[pid]
    page_image = image_metadata(mp["image"]["path"], mp["image"]["bbox_px"], mp["image"]["sha256"])
    page_image.update({"id": pid, "kind": "full_page", "view_order": "before all six default regions"})
    image_records.append(page_image)
    page = {key: own[key] for key in ("page_id", "reviewer_id", "session_id", "layout", "first_visible", "last_visible", "blank_observation", "continuation")}
    page["page_number"] = number
    page["page_image"] = page_image
    page["manual_checkpoint"] = {"path": str(checkpoint.relative_to(P)), "sha256": sha(checkpoint)}
    region_map = {r["id"].split("-", 1)[1]: r for r in mp["regions"]}
    page["regions"] = []
    for row in own["regions"]:
        assert len(row) == 6, (pid, row)
        short_id, first, last, checks, blank, continuation = row
        assert short_id in region_map, (pid, short_id)
        mr = region_map[short_id]
        meta = image_metadata(mr["image"]["path"], mr["bbox_px"], mr["image"]["sha256"])
        meta.update({"id": mr["id"], "kind": "default_region", "page_id": pid})
        image_records.append(meta)
        region = dict(meta)
        region.update({"first_visible": first, "last_visible": last, "specific_observations": checks, "blank_observation": blank, "continuation": continuation})
        page["regions"].append(region)
    page["crops"] = []
    for observation in own["crops"]:
        cid = observation["id"]
        if cid in source_crops:
            positional = source_crops[cid]
            source_crop_ids_seen.add(cid)
            origin = "existing_source_evidence_crop"
        else:
            positional = {key: observation[key] for key in ("id", "path", "page_id", "bbox_px")}
            origin = "independent_reviewer_crop"
        assert positional["page_id"] == pid
        meta = image_metadata(positional["path"], positional["bbox_px"])
        meta.update({"id": cid, "kind": "crop", "page_id": pid, "origin": origin})
        with Image.open(P / mp["image"]["path"]) as source_image:
            expected_pixels = source_image.crop(positional["bbox_px"]).convert("RGB")
            with Image.open(P / positional["path"]) as actual_image:
                assert ImageChops.difference(expected_pixels, actual_image.convert("RGB")).getbbox() is None, cid
        meta["pixels_match_unscaled_page_crop"] = True
        meta["parent_page_sha256"] = page_image["sha256"]
        image_records.append(meta)
        crop_records.append(meta)
        detail = dict(meta)
        for key in ("first_visible", "last_visible", "observation"):
            detail[key] = observation[key]
        page["crops"].append(detail)
    page["content_units"] = []
    for unit in own["units"]:
        assert len(unit) == 6, (pid, unit)
        uid, bbox, kind, source_text, status, notes = unit
        assert 0 <= bbox[0] < bbox[2] <= mp["width_px"], (pid, uid)
        assert 0 <= bbox[1] < bbox[3] <= mp["height_px"], (pid, uid)
        u = {
            "id": f"RA07-VS-{pid}-{uid}", "page_id": pid, "reviewer_id": RID, "session_id": RID,
            "position": {"bbox_px": bbox, "precision": "manually located content area; not glyph segmentation"},
            "kind": kind, "visible_source_content": source_text, "reading_status": status, "uncertainty_and_notes": notes,
            "full_page_image": page_image["path"],
            "intersecting_viewed_regions": [r["id"] for r in page["regions"] if overlaps(bbox, r["bbox_px"])],
            "intersecting_viewed_crops": [c["id"] for c in page["crops"] if overlaps(bbox, c["bbox_px"])],
        }
        page["content_units"].append(u)
        all_units.append(u)
    pages.append(page)
    metadata_checks.append({"page_id": pid, "image_hashes_match_manifest": True, "six_regions_present": True, "units": len(own["units"])})

assert source_crop_ids_seen == set(source_crops)
assert len(image_records) == 105
assert len(crop_records) == 14
assert len(all_units) == 168
assert len({x["id"] for x in all_units}) == 168
assert len({x["path"] for x in image_records}) == 105

record = {
    "schema": "ra07-independent-blind-observations-v1",
    "phase": "VISUAL_SECOND phase 1: blind source-only inventory",
    "reviewer_id": RID, "session_id": RID,
    "source_pdf": {"path": "source.pdf", "absolute_path": str(P / "source.pdf"), "sha256": EXPECTED_SOURCE_SHA, "physical_pages": 13},
    "manifest": {"path": "manifest.json", "sha256": sha(P / "manifest.json")},
    "scope": {
        "source_only": True, "drafts_read": False, "ledger_read": False, "mapping_read": False,
        "author_observations_read": False, "handoff_read": False,
        "crop_manifest_fields_used": ["id", "path", "page_id", "bbox_px"],
        "canonical_identity_is_only_available_session_identity": True,
        "scope_note": "所有内容观察为独立手工看图记录；脚本只汇集自有逐页记录、真实元数据与结构检查。",
        "failed_display_note": "p0006曾一次批量显示因上下文过长被截断，该次不计阅读完成；其六区和三裁图随后小批重新实际打开并完成观察。",
        "phase_gate": "本阶段不是最终三轮中的任何一轮；未获Boss明确followup前不读取两份稿件与映射。",
    },
    "coverage": {
        "full_pages_actually_viewed": 13, "default_regions_actually_viewed": 78,
        "existing_source_crops_actually_viewed": 11, "independent_reviewer_crops_actually_viewed": 3,
        "distinct_images_actually_viewed": 105, "hand_recorded_content_units": 168,
        "blank_physical_pages": ["p0013"], "partially_written_final_page": "p0012",
        "all_six_regions_per_page_viewed": True,
        "blank_verification": "每一空白位置均经过全页和对应高清区两层实际观察；p0013全页及全部六区均空白。",
        "image_hash_checks_are_metadata_only": True,
        "synthetic_selftest": "47项通过；不作为阅读原图的替代或证据。",
    },
    "pages": pages, "viewed_image_manifest": image_records, "crop_manifest": crop_records,
    "metadata_validation": metadata_checks, "phase_1_complete": True,
}
json_write(OUT / "blind-observations.json", record)

def code(value):
    return chr(96) + str(value).replace(chr(96), "'") + chr(96)

def cell(value):
    return str(value).replace("|", "\\|").replace("\n", " ")

lines = [
    "# RA07 独立原图清单 — VISUAL_SECOND 第一阶段", "",
    f"reviewer_id：{code(RID)}", "",
    f"session_id：{code(RID)}。工具未提供额外会话UUID，未另造身份。", "",
    "## 阶段与来源", "",
    f"原PDF：{code('source.pdf')}；SHA256：{code(EXPECTED_SOURCE_SHA)}；13个物理页。", "",
    "本清单在读取任何正文稿、学习稿、ledger、映射、作者观察或交接之前独立形成。只使用原PDF、manifest、全页图、六区图、evidence PNG，以及补充裁图清单的四个位置字段。逐页checkpoint中的观察为人工逐图记录，随后脚本仅汇集字段、哈希及坐标。", "",
    "每页先实际打开全页，再逐张打开6个默认高清重叠区；现有11张补充裁图全部实际打开。另生成并实际打开3张独立裁图，均保持原像素不缩放，源图未改动。p0006一次过长的批量显示被截断，不计该次；随后逐个小批重开6区及3裁图完成检查。", "",
    "**实际覆盖：13个全页 + 78个默认区 + 11个现有裁图 + 3个独立裁图 = 105张不同图像；168个手工内容单元。** 空白位置先在全页观察，再在对应高清区复核。第13页整页空白；第12页只有左上四行，其余空白及跨区长竖尾均有单独记录。", "",
    "图像和区域坐标为真实元数据；内容单元坐标是手工定位区域，不宣称逐笔分割。所有截图均由 tools.view_image 打开并以 image(result.image_url) 显示。47项工具合成自检通过，该检查不替代看图。", "",
    "此阶段仅完成盲读清单，不是最终三轮复核中的任何一轮。第二阶段等待Boss明确followup。", "",
    "## 覆盖一览", "",
    "| 物理页 | 全页 | 默认区 | 现有裁图 | 独立裁图 | 内容单元 |",
    "| --- | --- | --- | --- | --- | --- |",
]
for page in pages:
    existing = sum(c["origin"] == "existing_source_evidence_crop" for c in page["crops"])
    own_count = sum(c["origin"] == "independent_reviewer_crop" for c in page["crops"])
    lines.append(f"| {page['page_id']} | 已实际查看 | 6/6 | {existing} | {own_count} | {len(page['content_units'])} |")

for page in pages:
    lines += [
        "", f"## {page['page_id']} — 物理第{page['page_number']}页", "",
        f"全页图：{code(page['page_image']['path'])}，SHA256 {code(page['page_image']['sha256'])}。", "",
        f"**版面：** {page['layout']}", "", f"**首见：** {page['first_visible']}", "",
        f"**末见：** {page['last_visible']}", "", f"**空白与页边：** {page['blank_observation']}", "",
        f"**接续与重复：** {page['continuation']}", "", "### 六区逐图记录", "",
    ]
    for r in page["regions"]:
        lines += [
            f"#### {r['id']}", "",
            f"图像 {code(r['path'])}；bbox_px {code(r['bbox_px'])}；SHA256 {code(r['sha256'])}。", "",
            f"首见：{r['first_visible']}。末见：{r['last_visible']}。", "",
            f"实际核对：{r['specific_observations']}", "", f"空白：{r['blank_observation']}", "",
            f"接续：{r['continuation']}", "",
        ]
    if page["crops"]:
        lines += ["### 补充裁图逐图记录", ""]
        for c in page["crops"]:
            lines += [
                f"#### {c['id']}", "",
                f"图像 {code(c['path'])}；bbox_px {code(c['bbox_px'])}；SHA256 {code(c['sha256'])}。", "",
                f"类型：{c['origin']}；原像素裁图与全页对应区域一致，已实际打开。", "",
                f"首见：{c['first_visible']}。末见：{c['last_visible']}。", "",
                f"实际观察：{c['observation']}", "",
            ]
    lines += ["### 手工内容单元", ""]
    if not page["content_units"]:
        lines += ["本页无数学或文字内容单元。空白已在全页和六区分别实见，不用占位公式充数。", ""]
    else:
        for u in page["content_units"]:
            lines += [
                f"#### {u['id']} — {u['kind']}", "",
                f"定位 bbox_px {code(u['position']['bbox_px'])}；相交已阅区域：{', '.join(u['intersecting_viewed_regions'])}。", "",
                f"原笔内容：{u['visible_source_content']}", "",
                f"识读状态：**{u['reading_status']}**。{u['uncertainty_and_notes']}", "",
            ]
lines += [
    "## 裁图位置与哈希总表", "",
    "| 裁图ID | 原页 | bbox_px | 路径 | SHA256 |",
    "| --- | --- | --- | --- | --- |",
]
for c in crop_records:
    lines.append("| " + " | ".join(cell(v) for v in (c["id"], c["page_id"], c["bbox_px"], c["path"], c["sha256"])) + " |")
lines += [
    "", "## 第一阶段封存说明", "",
    "13页均有独立版面、首末内容、空白及接续观察；78个默认区均有不同位置的实际记录；11个现有裁图与3个独立裁图均有首末及具体识读结果。图形中的集合标签、交叠分区、数字和缺少的箭头/阴影均按可见信息描述。疑字、截断、原笔省略、数学上可疑之处与可确认内容分开记录。", "",
    "第二阶段尚未开始。此文件与 blind-observations.json 的 SHA256 在提交消息中报告，不将文件自身哈希写入自身以形成循环。",
]
write_text(OUT / "independent-inventory.md", "\n".join(lines))

# Structural and whitespace checks only; these do not certify visual reading.
for path in [OUT / "blind-observations.json", OUT / "independent-inventory.md"]:
    raw = path.read_bytes()
    assert raw.endswith(b"\n") and not raw.endswith(b"\n\n")
    assert raw == raw.rstrip() + b"\n"
    assert all(line == line.rstrip() for line in raw.splitlines())
print(json.dumps({
    "pages": len(pages), "regions": sum(len(x["regions"]) for x in pages),
    "source_crops": len(source_crop_ids_seen),
    "own_crops": sum(x["origin"] == "independent_reviewer_crop" for x in crop_records),
    "distinct_viewed_images": len(image_records), "content_units": len(all_units),
    "files": [{"path": str(path.relative_to(P)), "sha256": sha(path), "bytes": path.stat().st_size}
        for path in [OUT / "independent-inventory.md", OUT / "blind-observations.json"]],
}, ensure_ascii=False, indent=2))
