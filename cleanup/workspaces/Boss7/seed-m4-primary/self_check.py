"""Validate staged links, receipt targets and lossless policy-table transcription.

No utility, IC, OPT or optimization computation occurs here.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--stage", type=Path, required=True)
    args = parser.parse_args()
    workspace = args.stage / "cleanup/workspaces/Boss7/seed-m4-primary"
    evidence = args.stage / "archives/customer-attraction/tools/evidence/four-player-root-defect-seed-plans-primary"
    structure = json.loads((evidence / "structure-and-differences.json").read_text())
    for row in structure["sources"]:
        raw = (args.repo / row["existing_frozen_copy"]).read_bytes()
        assert len(raw) == row["size"] and hashlib.sha256(raw).hexdigest() == row["sha256"]
    sections = {}
    current, fixed_first, table = None, None, None
    for line in (evidence / "ordered-action-tables.md").read_text().splitlines():
        if line.startswith("## "):
            current = re.search(r"\(([0-9a-f]{20})\)", line).group(1)
            sections[current] = {}
            continue
        if current is None:
            continue
        if line.startswith("根行动："):
            sections[current][()] = int(line.split("：")[1])
        elif line.startswith("第二位（"):
            values = list(map(int, re.search(r"`(.*)`", line).group(1).split(",")))
            assert len(values) == 6
            for a, action in enumerate(values):
                sections[current][(a,)] = action
        elif line == "第三位：":
            table = "third"
        elif line.startswith("末位，首行动="):
            fixed_first = int(re.search(r"=(\d+)", line).group(1))
            table = "last"
        elif line.startswith("| ") and re.match(r"\| [0-5] \|", line):
            cells = [int(cell.strip()) for cell in line.strip().strip("|").split("|")]
            assert len(cells) == 7
            row_index, values = cells[0], cells[1:]
            for column, action in enumerate(values):
                key = (row_index, column) if table == "third" else (fixed_first, row_index, column)
                assert key not in sections[current]
                sections[current][key] = action
    assert len(sections) == 4
    for row in structure["sources"]:
        obj = json.loads((args.repo / row["existing_frozen_copy"]).read_text())
        assert sections[row["id"]] == {tuple(h): a for h, a in obj["actions"]}
    receipts = json.loads((workspace / "semantic-receipts.json").read_text())
    assert len(receipts) == 4 and {r["id"] for r in receipts} == set(sections)
    required = {"id", "full_file_reviewed", "related_material_checked", "unique_content_accounted_for",
                "read_note", "comparison_note", "decision_note", "disposition", "targets"}
    for receipt in receipts:
        assert set(receipt) == required and receipt["disposition"] == "integrated"
        assert receipt["full_file_reviewed"] and receipt["related_material_checked"] and receipt["unique_content_accounted_for"]
        assert all((args.stage / p).is_file() for p in receipt["targets"])
        assert json.loads((workspace / "receipts" / (receipt["id"] + ".json")).read_text()) == receipt
    link_count = 0
    for path in args.stage.rglob("*.md"):
        rel = path.relative_to(args.stage)
        for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text()):
            if "://" in target or target.startswith("#"):
                continue
            destination = target.split("#")[0]
            stage_dest = (args.stage / rel.parent / destination).resolve()
            repo_dest = (args.repo / rel.parent / destination).resolve()
            assert stage_dest.exists() or repo_dest.exists(), (str(rel), target)
            link_count += 1
    for path in args.stage.rglob("*.json"):
        json.loads(path.read_text())
    output = {"four_source_byte_identity": True, "complete_policy_tables_round_trip": True,
              "transcribed_actions": sum(len(d) for d in sections.values()),
              "semantic_receipts": len(receipts), "resolved_markdown_links": link_count,
              "all_staged_json_parse": True, "IC_replays": 0, "OPT_enumerations": 0,
              "status": "passed"}
    (workspace / "self-check.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
