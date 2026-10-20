#!/usr/bin/env python3
"""Build the human research catalogue from authored names and existing ledgers.

catalog.json records file identity and reading purpose, not mathematical truth.
Claim scope and review state remain in assets.json and review_status.json.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "research/catalog.json"
TOPICS = [
    ("topic_selection", "运筹学与优化理论重新选题", "topic_selection/README.md"),
    ("unrelated_machines", "不相关并行机与统一常数2壁垒", "current/unrelated_machines/README.md"),
    ("weighted_congestion", "加权原子拥塞博弈", "current/weighted_congestion/README.md"),
    ("positive_kernels", "正占用核、交互阶数与非负表示", "current/positive_kernels/README.md"),
    ("shared", "共同目录双设施", "current/shared/README.md"),
    ("heterogeneous", "异构目录双设施", "current/heterogeneous/README.md"),
    ("local_and_exact", "双设施局部均衡与精确算法", "current/local_and_exact/README.md"),
    ("multi_facility", "任意设施数与完整盒构造", "current/multi_facility/README.md"),
    ("customer_attraction", "顺序客户吸引与半覆盖", "current/customer_attraction/README.md"),
    ("foundation", "公共定义与精确命题登记", "current/README.md"),
    ("facility_review", "设施模型的独立审查", "reviews/README.md"),
    ("customer_attraction_review", "客户吸引的独立审查", "reviews/README.md"),
    ("publication", "历史投稿判断与旧方向选择", "../history/README.md"),
]
ROLES = {
    "account": "数学正文；按关联命题分别核对证明及审查",
    "algorithm": "算法与构造；适用类及复杂度见正文",
    "reduction": "精确归约；方向和编码合同见正文",
    "representation": "表示或证书接口；不自动给出待求系数",
    "certificate_account": "证书与核验正文；验证范围见合同",
    "source_guide": "来源与恢复指针；不代替缺失证明",
    "definition": "定义与模型；不隐含跨模型定理",
    "ledger": "精确命题登记；摘要不替代原陈述",
    "obstruction": "方法障碍；否定范围以正文为准",
    "counterexample": "反例；仅否定正文明确的命题",
    "candidate": "候选或未闭合义务；保存不升级状态",
    "question": "问题记录；开放/已闭合部分见用途及正文",
    "review": "实际审查记录；只覆盖所列版本与义务",
    "audit_code": "有限计算核验；不代替一般证明",
    "frozen_evidence": "冻结输入、证书或结果；不原位覆盖",
    "source": "来源或历史判断；不作为现行结论",
    "literature": "文献核对；与团队新结果分别引用",
    "navigation": "阅读导航；真值查精确正文及账本",
}
PACKAGE_TITLES = {
    "研究入口": "研究入口、精确状态与文件合同",
    "finite_action_certificates": "有限动作模板、全状态择证与精确对偶",
    "odd_ring": "奇环全状态下界、有限实现与精确证书包络",
    "source_envelope": "文献源族的锐包络与渐近",
    "source_topology": "对称两列拓扑的完整还原",
    "source_degree32": "固定次数源族的精确区间证书",
    "resource_support": "资源支持对固定小构造的限制",
    "weight_density": "稀疏权谱、密度势与矩界",
    "power_bridge": "资源局部势拼接与异质接口",
    "weight_bands": "局部窄权带、Shapley 势与选择器边界",
    "density_padding": "可选用户填充与密度参数边界",
    "crossover": "非对称有限构造、缩权族与极限运输",
    "quadratic_source": "二次源族的标量包络",
    "quadratic_triad": "三玩家二次整数障碍与来源欠账",
    "multicolumn": "补列、多列逃逸与非分离来源缺口",
    "polynomial_curvature": "多项式三负载曲率与三点包络",
    "heterogeneous_endpoint": "异权端点的精确还原",
    "step_dag": "辅助阶跃依赖 DAG 及迁移限制",
    "marginal_potentials": "固定边际势与任意乘子候选障碍",
    "ordinal_potentials": "序势候选、稠密桥与方法限制",
    "polynomial_endpoint": "保守多项式端点候选与侧列还原",
    "signed_columns": "带符号列、三元组与扩展候选",
    "协作程序": "协作、保存、启动与许可入口",
}


def load_data(path: Path = CATALOG) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(data: dict, root: Path = ROOT) -> None:
    if data.get("schema_version") != 1:
        raise ValueError("unsupported catalogue schema")
    known_topics = {key for key, _, _ in TOPICS}
    paths = set()
    resolved = set()
    for row in data["entries"]:
        path = row["path"]
        target = (root / path).resolve()
        parts = path.split("/")
        if (Path(path).is_absolute() or any(p in {"", ".", ".."} for p in parts)
                or "\\" in path or any(c in path for c in "\n\r<>")):
            raise ValueError(("asset path must be a canonical relative path", path))
        if (path in paths or target in resolved or not target.is_relative_to(root.resolve())
                or not target.is_file()):
            raise ValueError(("duplicate, missing or escaping asset", path))
        paths.add(path)
        resolved.add(target)
        if row["topic"] not in known_topics or row["role"] not in ROLES:
            raise ValueError(("unknown topic/role", path))
        title, purpose = row["title"], row["purpose"]
        if not re.search(r"[\u3400-\u9fff]", title) or title == Path(path).name:
            raise ValueError(("asset needs a human Chinese name", path))
        if len(purpose.strip()) < 12 or purpose.endswith("接口或来源复验时"):
            raise ValueError(("asset needs a specific reading purpose", path))
    required = {
        p.relative_to(root).as_posix()
        for group in ("research/current", "research/questions", "research/reviews")
        for p in (root / group).rglob("*.md")
    }
    required.update(p.relative_to(root).as_posix() for p in (root / "research").glob("*.md")
                    if p.name not in {"CATALOG.md", "source_crosswalk.md"})
    frontier = root / "research/weighted_congestion_frontier"
    required.update(p.relative_to(root).as_posix() for p in frontier.rglob("*.md")
                    if "upstream" not in p.relative_to(frontier).parts)
    integration = root / "research/weighted_congestion_frontier/INTEGRATION.json"
    if integration.exists():
        required.update(item["path"] for item in json.loads(integration.read_text())["classification"].values()
                        if "path" in item)
    if required - paths:
        raise ValueError(("research assets missing human names", sorted(required - paths)))
    for row in data["entries"]:
        if set(row.get("related_paths", [])) - paths:
            raise ValueError(("related asset is not named", row["path"]))
    for old, new in data.get("renamed_paths", {}).items():
        if (Path(old).is_absolute() or any(p in {"", ".", ".."} for p in old.split("/"))
                or new not in paths or (root / old).exists() or not (root / new).is_file()):
            raise ValueError(("stale or incomplete asset relocation", old, new))


def cell(value: str) -> str:
    return value.replace("|", r"\|").replace("\n", " ")


def claim_index(root: Path = ROOT) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    for asset in json.loads((root / "research/assets.json").read_text())["entries"]:
        for role in ("proof", "tests", "records", "examples", "reviews", "candidates", "sources", "implementation"):
            for path in asset.get(role, []):
                result.setdefault(path, set()).update(asset["claims"])
    return result


def render_rows(rows: list[dict], base: str, claims: dict[str, set[str]], names: dict[str, str]) -> list[str]:
    out = ["| 中文资产名 | 完整文件位置 | 解决什么、何时读取 | 身份与状态依据 |",
           "| --- | --- | --- | --- |"]
    for row in rows:
        path = row["path"]
        link = os.path.relpath(path, base)
        ids = sorted(claims.get(path, []))
        state = ROLES[row["role"]]
        if ids:
            ledger = os.path.relpath("research/assets.json", base)
            visible = "、".join(f"`{c}`" for c in ids[:3])
            suffix = f"（共 {len(ids)} 项）" if len(ids) > 3 else ""
            state += f"；关联 {visible}，[命题合同{suffix}]({ledger})"
        elif row["role"] in {"account", "obstruction", "counterexample"}:
            state += "；精确范围见本页正文"
        label = cell(row["title"]).replace("[", r"\[").replace("]", r"\]")
        purpose = cell(row["purpose"])
        for related in row.get("related_paths", []):
            related_label = cell(names[related]).replace("[", r"\[").replace("]", r"\]")
            purpose += f"；配套 [{related_label}](<{os.path.relpath(related, base)}>)"
        out.append(f"| [{label}](<{link}>) | `{path}` | {purpose} | {state} |")
    return out


def render_topic(data: dict, topic: str, base: str) -> str:
    rows = [r for r in data["entries"] if r["topic"] == topic]
    claims = claim_index()
    names = {r["path"]: r["title"] for r in data["entries"]}
    packages = list(dict.fromkeys(r.get("package", "") for r in rows))
    if topic == "weighted_congestion":
        order = list(PACKAGE_TITLES)
        packages.sort(key=lambda p: order.index(p) if p in order else len(order))
    lines = []
    for package in packages:
        selected = [r for r in rows if r.get("package", "") == package]
        if topic == "weighted_congestion":
            role_order = ["navigation", "definition", "ledger", "account", "algorithm", "reduction",
                          "representation", "certificate_account", "counterexample", "obstruction",
                          "candidate", "question", "literature", "review", "audit_code", "frozen_evidence",
                          "source_guide", "source"]
            selected.sort(key=lambda row: role_order.index(row["role"]))
        if package:
            lines += [f"### {PACKAGE_TITLES.get(package, package)}", ""]
        lines += render_rows(selected, base, claims, names) + [""]
    return "\n".join(lines)


def render(data: dict) -> str:
    lines = ["# 研究资产总目录：按数学问题找名字、正文与证据", "",
             "这里登记当前数学稿、问题、审查和已整合的拥塞核验资产。每个名称和用途经过逐文件整理；文件名、提交者代号与目录位置都不代替数学身份。",
             "先从下表选择问题，再进入专题的阅读路线。历史原稿按需从 [历史入口](../history/README.md) 与 [来源对应](source_crosswalk.md) 查询；规范程序和人类讲义从 [全仓资产入口](../ASSETS.md) 进入。", "",
             "证明、内部审查、外部审查和实现的真实状态分别保存在 [五轴账本](review_status.json)；精确量词在 [命题登记](current/claims.md) 和 [拥塞命题账本](weighted_congestion_frontier/CLAIMS.md)。下表只说明文件角色，不为整份文件授予统一的‘已证明’标签。", "",
             "| 数学专题 | 首读入口 | 逐文件目录 |", "| --- | --- | --- |"]
    for key, title, entry in TOPICS:
        if any(r["topic"] == key for r in data["entries"]):
            lines.append(f"| {title} | [研究说明]({entry}) | [中文资产名与用途](#{key}) |")
    lines += ["", "维护方法：先在 `catalog.json` 写具体名称和用途，再运行 `python3 research/build_catalog.py`；`--check` 同时拒绝漏登记、缺文件、无中文名称和过时生成稿。新增候选按原等级保存，不能为通过目录检查而升级结论。", ""]
    for key, title, _ in TOPICS:
        if any(r["topic"] == key for r in data["entries"]):
            lines += [f'<a id="{key}"></a>', "", f"## {title}", "", render_topic(data, key, "research")]
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = load_data()
    validate(data)
    rendered = render(data)
    target = ROOT / "research/CATALOG.md"
    if args.check:
        if not target.exists() or target.read_text(encoding="utf-8") != rendered:
            raise ValueError("run python3 research/build_catalog.py")
    else:
        target.write_text(rendered, encoding="utf-8")
    print(f"Validated {len(data['entries'])} named research assets and complete current/question/review coverage")


if __name__ == "__main__":
    main()
