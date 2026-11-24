"""One-time mapping of actual second-reader split proposals into RA06 v2.

Computes geometry and current source ID coverage, not new reading claims.
The original first-pass observations and compared drafts remain unchanged.
"""
from pathlib import Path
import copy
import json
import re

RUN = Path(__file__).resolve().parent.parent
P = RUN / "notes/RA06/project"
V = P / "proposals/integration-v2"
review = json.loads((P / "reviews/visual-second/revision-tasks.json").read_text())
sources = json.loads((V / "source-units.json").read_text())
assert len(sources) == 62, "One-time mapping only"
mapping = json.loads((V / "mapping.json").read_text())
manifest = json.loads((P / "manifest.json").read_text())
pages = {p["id"]: p for p in manifest["pages"]}
splits = {x["current_source_id"]: x for x in review["source_split_proposals"]}
assert len(splits) == 16

def overlap(a, b):
    return max(a[0], b[0]) < min(a[2], b[2]) and max(a[1], b[1]) < min(a[3], b[3])

new_sources = []
id_map = {}
split_log = []
for source in sources:
    parts = splits.get(source["id"], {}).get("parts")
    if not parts:
        new_sources.append(source)
        continue
    new_ids = []
    for i, part in enumerate(parts):
        item = copy.deepcopy(source)
        item["id"] = source["id"] if i == 0 else source["id"] + "-B"
        item["bbox_px"] = part["suggested_bbox_px"]
        # The short label identifies the actual object; the independent blind
        # wording and any later disagreement remain in the reviewer's files.
        item["label"] = part["blind_observation"]
        new_ids.append(item["id"])
        new_sources.append(item)
        split_log.append({"previous_source_id": source["id"],
                          "new_source_id": item["id"],
                          "independent_id": part["independent_id"],
                          "bbox_px": item["bbox_px"]})
    id_map[source["id"]] = new_ids

index = {s["id"]: s for s in new_sources}
label_updates = {
    "RA06-P001-U03": "第二可数蕴含Lindeloff及原词逆不真",
    "RA06-P001-U08": "由T1、由T2及共同半径不交球",
    "RA06-P001-U09-B": "有限子覆盖及原有界括注",
    "RA06-P001-U10-B": "有限并交空及闭集括注；原球心y未见下标i",
    "RA06-P002-U01": "有限[Q006]提要；iff列紧与闭集有界关系",
    "RA06-P002-U01-B": "可以定义有限[Q006]及某些教材备注",
    "RA06-P002-U02": "原括注闭传递性；Q001已据局部笔画恢复",
    "RA06-P002-U02-B": "紧空间的闭子集仍紧的完整引理",
    "RA06-P002-U04": "有界性选初始方块；右端点Q002a与指数Q002b待辨",
    "RA06-P002-U07": "二等分所得存在一个闭集无有限子覆盖，原记Qm",
    "RA06-P003-U06": "覆盖开集内取球；半径delta右下附笔Q007",
    "RA06-P003-U07-B": "点列距离与方块直径分别小于delta/2",
    "RA06-P003-U13": "浅色正向等式链：闭包=导集=导集并Iso；Iso不属于导集",
    "RA06-P003-U15": "浅色Q008连接语与导集闭、闭集导集包含关系",
    "RA06-P003-U16": "闭集旁注分解，E的小上标Q009待辨",
    "RA06-P003-U16-B": "浅色另行E导集包含于E",
    "RA06-P004-U02": "Ex1实数底集能[Q003]拓扑及原数值2^c",
    "RA06-P004-U03": "原∀空集=U及开集标注；等号按可见双横保留",
    "RA06-P004-U12": "可读断言(alpha,beta)属于区间族Gx",
    "RA06-P004-U12-B": "且后半Q004关系式；beta后的不属于号可辨",
    "RA06-P004-U14-B": "端点结论的未完成反证起步：反证，若不然",
    "RA06-P005-U10": "Ex1实区间[Q010]题头",
    "RA06-P005-U11": "pf：p进制小数至多有两种展开；Q005局部恢复"
}
for ident, label in label_updates.items():
    index[ident]["label"] = label
index["RA06-P003-U16-B"]["status"] = "resolved"
index["RA06-P004-U12"]["status"] = "resolved"
index["RA06-P004-U12-B"]["status"] = "unresolved"

for source in new_sources:
    regs = [r["id"] for r in pages[source["page_id"]]["regions"]
            if overlap(source["bbox_px"], r["bbox_px"])]
    extra = [e for e in source["evidence_ids"] if e.startswith("artifact:")]
    source["evidence_ids"] = ["image:" + source["page_id"]] + ["image:" + r for r in regs] + extra
for target in mapping["targets"]:
    target["source_ids"] = [new for old in target["source_ids"] for new in id_map.get(old, [old])]

def parse(path):
    parts = re.split(r"(?m)^<!-- unit: ([^\s]+) -->\n", path.read_text())
    assert not parts[0].strip()
    return [(parts[i], parts[i + 1].strip()) for i in range(1, len(parts), 2)]

docs = {typ: parse(V / fn) for typ, fn in
        [("T", "source-transcript.md"), ("N", "study-notes.md")]}
target_index = {t["id"]: t for t in mapping["targets"]}

def setbody(ident, text):
    arr = docs[ident[0]]
    at = next(i for i, v in enumerate(arr) if v[0] == ident)
    arr[at] = (ident, text.strip())

def split_body(old, new, first, second, first_source, second_source):
    setbody(old, first)
    arr = docs[old[0]]
    at = next(i for i, v in enumerate(arr) if v[0] == old)
    arr.insert(at + 1, (new, second))
    target_index[old]["source_ids"] = [first_source]
    target_index[old]["status"] = index[first_source]["status"]
    t = copy.deepcopy(target_index[old])
    t.update(id=new, source_ids=[second_source], status=index[second_source]["status"],
             explanation="按独立读图定位将同一原行中已辨与未决部分拆开；不删除任一原片段。")
    mapping["targets"].append(t)
    target_index[new] = t

for typ in ["T", "N"]:
    split_body(
        typ + "-p3-16", typ + "-p3-16-b",
        r"""闭，
$$\overline E=E=E^{\text{[Q009]}}\cup\partial E.$$
〔Q009 定位并号前 $E$ 的小上标；起首“闭”按原笔保留。〕""",
        r"""原稿浅色下一行另记
$$E'\subset E.$$""",
        "RA06-P003-U16", "RA06-P003-U16-B")
    split_body(
        typ + "-p4-12", typ + "-p4-12-b",
        r"断言 $(\alpha,\beta)\in G_x$。",
        r"""且〔Q004：本行右半关系式尚未唯一辨定〕。

原笔可辨 $\beta$ 及其后的 $\notin$；前半变量、第一关系符和两处 $G$ 的下标另存候选与精确局部图位置。""",
        "RA06-P004-U12", "RA06-P004-U12-B")

target_index["N-p3-closure-scope"]["source_ids"] = ["RA06-P003-U16"]
target_index["N-p2-closed-proof"]["source_ids"] = ["RA06-P002-U02-B"]
target_index["N-p1-cover-bounded-note"]["source_ids"] = ["RA06-P001-U09-B"]
target_index["N-p1-index-and-conclusion"]["source_ids"] = ["RA06-P001-U10", "RA06-P001-U10-B"]
target_index["N-interval-connected-proof"]["explanation"] = "保留完整上确界证明，作为题头Q010的明确候选题意解答；原进制提示已另有完整补证。"
for target in mapping["targets"]:
    if target["source_ids"]:
        states = {index[s]["status"] for s in target["source_ids"]}
        assert len(states) == 1, (target["id"], states)
        target["status"] = states.pop()
    if target["id"] == "N-base-expansion-proof":
        body = next(t for ident, t in docs["N"] if ident == target["id"])
        setbody(target["id"], body.replace("非终止型的多数数值只有一种表示",
                "不具有有限 p 进展开的数只可能有一种表示"))

# Original page and region prose is kept as historical first-reading evidence;
# only the current fine-grained IDs are calculated from already observed pixels.
obs = json.loads((P / "proposals/rebuild/observations.json").read_text())
for entry in obs["page_checks"]:
    ps = [s for s in new_sources if s["page_id"] == entry["page_id"]]
    entry["source_unit_ids"] = [s["id"] for s in ps]
    entry["cross_region_unit_ids"] = [
        s["id"] for s in ps
        if sum(overlap(s["bbox_px"], r["bbox_px"]) for r in pages[s["page_id"]]["regions"]) > 1]
    entry["observation"] = ("原作者首遍当时观察（读法差异以独立第二遍和整合记录订正；原始记录另存 rebuild）："
                            + entry["observation"])
for entry in obs["region_checks"]:
    page_id = entry["region_id"].split("-")[0]
    region = next(r for r in pages[page_id]["regions"] if r["id"] == entry["region_id"])
    entry["source_unit_ids"] = [
        s["id"] for s in new_sources if s["page_id"] == page_id and overlap(s["bbox_px"], region["bbox_px"])]
    entry["observation"] = ("原作者首遍当时观察（保留历史判读；现稿修订另记）："
                            + entry["observation"])

issues = json.loads((P / "proposals/rebuild/issues.json").read_text())
issue_index = {i["id"]: i for i in issues}
issue_index["Q001"].update(status="resolved",
    description="闭子集引理前括注的字词恢复。",
    related_ids=["RA06-P002-U02"],
    resolution="第二位独立读者回看全页、高清区域及top裁图，亻起笔与辶回折支持原词闭传递性；正文保留课堂用词，标准名称仅在蓝色说明。正式恢复记录另附。")
issue_index["Q002"].update(
    description="初始方块右端点Q002a与指数Q002b的笔形未唯一辨定；数学恢复[-a,a]^n单独给出。",
    related_ids=["RA06-P002-U04"])
issue_index["Q004"].update(
    related_ids=["RA06-P004-U12-B"],
    description="最大区间断言右半关系式Q004的变量、第一关系与G的下标未决；已辨左半断言独立建源。")
issue_index["Q005"].update(status="resolved",
    description="p进制小数提示的中间字词恢复。",
    resolution="独立回图支持至多有两种展开，首符按字母p排版；两正文保留原提示和原未完证明状态，学习稿补全存在性、至多两种及p等分闭区间套路线。")
new_issues = [
    ("Q006", "两处有限后的字：有限性/有限维仍未唯一辨定。", ["RA06-P002-U01", "RA06-P002-U01-B"], "p0002"),
    ("Q007", "开球半径delta右下点状附笔：可能为0下标或落笔点。", ["RA06-P003-U06"], "p0003"),
    ("Q008", "导集闭浅色补记前缀的连接语尚未唯一恢复。", ["RA06-P003-U15"], "p0003"),
    ("Q009", "闭集分解式并号前E的小上标：内部圆圈与导号仍有歧义。", ["RA06-P003-U16"], "p0003"),
    ("Q010", "实区间末题标题均连/构造的草写尚未唯一辨定。", ["RA06-P005-U10"], "p0005"),
]
for ident, description, sids, pid in new_issues:
    issues.append(dict(id=ident, status="open", description=description,
                       related_ids=sids, evidence_ids=["image:" + pid, "artifact:uncertainties"],
                       resolution=""))

uncertain = """# RA06 识读与恢复位置（整合版）

保留独立读者的候选和判断，不把数学正确作为字形已经读清的证据。编号是中性定位，普通空白页不构成未决知识单元。

| 编号 | 页与位置 | 当前状态 | 候选及已做判断 |
| --- | --- | --- | --- |
| Q001 | p2 [105,590,585,722] | 已恢复 | 原词闭传递性；亻起笔与辶回折支持传递，非把标准名闭遗传性直接替换进原文。 |
| Q002a/b | p2初始方块右端点与指数；原源 [130,1110,1740,1350] | 未唯一恢复 | 右端点 a/n；指数 n/c。后文维数与有界性支持数学式 [-a,a]^n，原笔读数仍分开。 |
| Q003 | p4 Ex1 [90,590,940,845] | 未唯一恢复 | 能有多少拓扑 / 能构造拓扑。原2^c保留；通常开集数c、基数2^c、所有拓扑2^(2^c)分别有完整蓝色说明。 |
| Q004 | p4 [1010,2410,1720,2640] | 未唯一恢复 | 前变量alpha/gamma，首关系属于/不属于，G下标x/gamma。第二个不属于较清楚；不能用最大区间正确结论代替原符号串。 |
| Q005 | p5 [100,2780,1450,3040] | 已恢复 | p进制小数至多有两种展开；首符按字母p排版。至多不能改为恰好；完整数学证明另以蓝色给出。 |
| Q006 | p2 [130,325,1340,470]及[130,475,1140,600] | 未唯一恢复 | 有限性 / 有限维；与同页性字比较后仍不足唯一排除。列紧可读；有限维候选的量词与Riesz完整证明已补。 |
| Q007 | p3开球行，源[140,1660,1020,1840]附近delta右下 | 未唯一恢复 | delta_0 / delta加落笔点。后文明确delta不排除前一处下标；蓝色补证统一正半径记号。 |
| Q008 | p3浅色补记，源[790,2790,1810,2955]中的前缀 | 未唯一恢复 | 前文证过 / 需证…；后半E导集是闭及闭集导集包含关系可读，已给独立完整补证。 |
| Q009 | p3 [1030,2930,1665,3100]的小上标 | 未唯一恢复 | 内部圆圈 / 导号；一般度量空间与通常实轴两种数学范围已分别检验，仍不代定笔迹。 |
| Q010 | p5 [105,2570,780,2730] | 未唯一恢复 | 均连 / 构造；比较同页构成、连通后倾向均连，但不能唯一排除。完整的两条区间连通路线与进制展开证明均保留。 |

其余直接修正的首稿差异另见独立第二遍任务清单与integration-progress：逆不真、T1/T2、有界括注、球心漏下标、闭集用词、完整浅色等号链、原空集等号、黑/蓝归属及原未完证明位置。已恢复或修正的历史项不删除。
"""
# Replace approximate old bbox strings in the location table with exact current
# source boxes; the independent recovery files retain their tighter local crops.
for old, sid in [("[130,1110,1740,1350]", "RA06-P002-U04"),
                 ("[140,1660,1020,1840]", "RA06-P003-U06"),
                 ("[790,2790,1810,2955]", "RA06-P003-U15")]:
    uncertain = uncertain.replace(old, json.dumps(index[sid]["bbox_px"], separators=(",", ":")))
(V / "unresolved.md").write_text(uncertain.rstrip() + "\n")
(V / "editorial-record.md").write_text(
    "# RA06 整合编辑记录\n\n"
    "作者为 /root 与 /root/startup_inspection；VISUAL_SECOND 是 /root/ra06_visual_second，独立盲读先于对稿，未参与正文编辑。"
    "本版由 /root 按23项实际发现整合；原 compared rebuild 两稿及ledger-first-pass.json保留不改。\n\n"
    "黑色保留原稿，蓝色写出补证/订正/明确候选题意的答案，红色只保留原稿明写proof或反证却未完成的位置；p6普通空白仅在页区来源记录中。"
    "16处来源按独立读者bbox拆成78个原对象，未删除原文。两处已辨/未决混合行在两稿同步拆目标；原记录ID保留给第一部分，第二部分加-B。\n\n"
    "首遍观察原文按历史保留，仅把已观察像素对象映射到细化后的当前来源ID；独立第二遍的真实观察和恢复另由该读者提供，不由脚本生成。"
    "新增有限维刻画、Riesz工具与进制存在/唯一性、闭区间套为独立数学补充，有完整推导与精确例子输入输出；不据它们强行恢复字形。\n")

config = json.loads((P / "ledger-config.json").read_text())
for art in config["artifacts"]:
    if art["path"].startswith("proposals/rebuild/"):
        art["path"] = art["path"].replace("proposals/rebuild/", "proposals/integration-v2/")
for ident, filename in [
    ("finite-dimensional-candidate", "finite-dimensional-candidate.md"),
    ("base-expansion-candidate", "base-expansion-candidate.md"),
    ("base-expansion-finite-check", "base-expansion-finite-check.json")]:
    config["artifacts"].append(dict(id=ident, path="research/" + filename, kind="evidence", format="text"))
config.update(source_units="proposals/integration-v2/source-units.json",
              mapping="proposals/integration-v2/mapping.json",
              observations="proposals/integration-v2/observations-author.json",
              issues="proposals/integration-v2/issues.json",
              output="ledger-integration-v2.json")
for name, data in [
    ("source-units.json", new_sources), ("mapping.json", mapping),
    ("observations-author.json", obs), ("issues.json", issues),
    ("source-split-adoption.json", split_log)]:
    (V / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
for typ, filename in [("T", "source-transcript.md"), ("N", "study-notes.md")]:
    text = "\n\n".join(f"<!-- unit: {uid} -->\n{body}" for uid, body in docs[typ])
    (V / filename).write_text(text.rstrip() + "\n")
(P / "ledger-config-v2.json").write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"sources": len(new_sources), "targets": len(mapping["targets"]),
                  "open_distinct_issues": sum(i["status"] == "open" for i in issues),
                  "split_objects": len(split_log)}))
