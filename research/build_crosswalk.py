#!/usr/bin/env python3
"""Render and validate the per-original-source interpretation ledger."""
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SECTIONS = (
    ("原手稿、笔记、审计与旧路线", lambda p: p.startswith("history/")),
    ("输入、证书与冻结记录", lambda p: p.startswith(("examples/", "evidence/"))),
    ("测试和审查代码", lambda p: p.startswith("tests/")),
    ("规范实现", lambda p: p.startswith("facility_spe/")),
)


def render():
    data = json.loads((HERE / "source_crosswalk.json").read_text())
    migration = json.loads((HERE / "path_migration.json").read_text())
    all_old = set(migration["moved"]) | set(migration["retired_code_paths"])
    records = {row["original"]: row for row in data["entries"]}
    if len(records) != len(data["entries"]) or set(records) != all_old:
        raise ValueError("source crosswalk omits or duplicates an original path")
    for old, target in {**migration["moved"], **migration["retired_code_paths"]}.items():
        row = records[old]
        if row["preserved_at"] != target:
            raise ValueError(("mismatched source target", old))
        if not row["rewritten_in"].startswith(("research/current/", "research/questions/")):
            raise ValueError(("source lacks newly authored current account", old))
        if not row["interpretation"]:
            raise ValueError(("source lacks interpretation", old))
        for field in ("preserved_at", "rewritten_in"):
            if not (ROOT / row[field]).is_file():
                raise ValueError((old, row[field]))
    lines = [
        "# 逐文件来源解释表",
        "",
        "每一行把一个原始文件或旧代码入口连接到本轮重新撰写的现行数学内容。",
        "历史手稿保留原状供核对；证据、测试和唯一代码在其专门目录。",
        "这个表不把原稿自动当作已经证明的现行命题。",
        "",
    ]
    tick = chr(96)
    accounted = set()
    for title, predicate in SECTIONS:
        lines += ["## " + title, "", "| 原始路径 | 当前保存位置 | 新写的解释 | 判断 |",
                  "| --- | --- | --- | --- |"]
        for row in data["entries"]:
            path = row["preserved_at"]
            if not predicate(path) or row["original"] in accounted:
                continue
            accounted.add(row["original"])
            old = row["original"].replace("|", r"\|")
            note = row["interpretation"].replace("|", r"\|")
            lines.append(f"| {tick}{old}{tick} | [{path}](../{path}) | "
                         f"[{row['rewritten_in']}](../{row['rewritten_in']}) | {note} |")
        lines.append("")
    if accounted != all_old:
        raise ValueError(("unclassified source roles", sorted(all_old - accounted)))
    new_sources = data.get("new_sources", [])
    seen_new = set()
    if new_sources:
        lines += ["## 新增来源（不属于旧路径迁移）", "",
                  "对话摘录等新来源单独登记，不虚构原始文件路径或下载记录。", "",
                  "| 保存位置 | 来源 | 新写的解释 | 判断 |",
                  "| --- | --- | --- | --- |"]
    for row in new_sources:
        source, current = row["source"], row["rewritten_in"]
        if (source in seen_new or not source.startswith("history/")
                or not current.startswith(("research/current/", "research/questions/"))
                or not row["provenance"] or not row["interpretation"]):
            raise ValueError(("invalid new source record", source))
        seen_new.add(source)
        if not (ROOT / source).is_file() or not (ROOT / current).is_file():
            raise ValueError(("missing new source or current account", source, current))
        provenance = row["provenance"].replace("|", r"\|")
        note = row["interpretation"].replace("|", r"\|")
        lines.append(f"| [{source}](../{source}) | {provenance} | "
                     f"[{current}](../{current}) | {note} |")
    if new_sources:
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = render()
    output = HERE / "source_crosswalk.md"
    if args.check:
        if not output.is_file() or output.read_text() != result:
            raise ValueError("run research/build_crosswalk.py")
    else:
        output.write_text(result)
    data = json.loads((HERE / "source_crosswalk.json").read_text())
    print(f"Validated {len(data['entries'])} migrated source/code paths and "
          f"{len(data.get('new_sources', []))} new source records")


if __name__ == "__main__":
    main()
