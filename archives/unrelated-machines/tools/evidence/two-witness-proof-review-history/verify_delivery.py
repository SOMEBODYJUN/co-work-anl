#!/usr/bin/env python3
"""Check this source-history delivery's bytes, JSON and local Markdown links.

This script does not execute a mathematical audit or certify any theorem.
"""

import argparse
import hashlib
import json
from pathlib import Path
import re


def verify(repo, fallback=None):
    evidence = Path("archives/unrelated-machines/tools/evidence/two-witness-proof-review-history")
    workspace = Path("cleanup/workspaces/Boss4/two-witness-proof-review-history-next")
    records = []
    for name in ["source-manifest.json", "comparison-manifest.json"]:
        entries = json.loads((repo / evidence / name).read_text())
        for entry in entries:
            relative = Path(entry["local_path"])
            raw = (repo / relative).read_bytes()
            digest = hashlib.sha256(raw).hexdigest()
            if len(raw) != entry["size"] or digest != entry["sha256"]:
                raise ValueError("Source identity mismatch: " + str(relative))
            records.append({"id": entry["id"], "path": str(relative),
                            "bytes": len(raw), "sha256": digest})
    json_files = sorted(set((repo / evidence).glob("*.json")) |
                        set((repo / workspace).glob("*.json")))
    for path in json_files:
        json.loads(path.read_text())
    new_pages = [
        Path("archives/unrelated-machines/state/审查/双见证查询分离的染色证明与冻结审查边界--审查.md"),
        evidence / "README.md",
    ]
    links = []
    for relative in new_pages:
        text = (repo / relative).read_text()
        if text.count(r"\[") != text.count(r"\]") or text.count(r"\(") != text.count(r"\)"):
            raise ValueError("Unbalanced math delimiters: " + str(relative))
        for target in re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", text):
            if "://" in target or target.startswith("#"):
                continue
            target_path = target.split("#", 1)[0]
            actual = (repo / relative.parent / target_path).resolve()
            method = "delivery-root"
            if not actual.is_file() and fallback is not None:
                actual = (fallback / relative.parent / target_path).resolve()
                method = "existing-repository-dependency"
            if not actual.is_file():
                raise ValueError("Missing link: " + str(relative) + " -> " + target)
            links.append({"from": str(relative), "target": target, "resolved_by": method})
    return {"scope": "delivery bytes/JSON/local links only; no mathematical program executed",
            "source_count": len(records), "sources": records,
            "json_file_count": len(json_files), "links": links,
            "result": "pass"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument("--fallback-root", type=Path,
                        help="Only for an external staging tree before copying into the repository")
    parser.add_argument("--report", required=True, type=Path)
    args = parser.parse_args()
    report = verify(args.repo_root.resolve(),
                    args.fallback_root.resolve() if args.fallback_root else None)
    with args.report.open("x") as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(json.dumps({"result": report["result"], "source_count": report["source_count"],
                      "json_file_count": report["json_file_count"],
                      "local_link_count": len(report["links"]),
                      "scope": report["scope"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
