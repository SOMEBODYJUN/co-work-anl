#!/usr/bin/env python3
"""Validate selected-topic routing, provenance fields and local navigation.

This checks data integrity, never openness, novelty or theorem truth.
"""
from pathlib import Path
import ast
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
TOPIC = ROOT / "research/topic_selection"


def require(ok, message):
    if not ok:
        raise ValueError(message)


def check():
    manifest = json.loads((TOPIC / "branch_manifest.json").read_text())
    branch, board, save = (manifest[k] for k in ("research_branch", "board_branch", "save"))
    require(branch != board and branch != "main" and board != "wcg/board", "topic isolation")
    current = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT,
                             check=True, capture_output=True, text=True).stdout.strip()
    require(current == branch, "wrong research branch: " + current)
    program = ROOT / "research/weighted_congestion_frontier/tools/work.py"
    assignments = {}
    for node in ast.parse(program.read_text()).body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "RESEARCH_ENTRIES":
                    assignments[target.id] = ast.literal_eval(node.value)
    entry = assignments["RESEARCH_ENTRIES"][save]
    require(entry == {"research_entry": manifest["research_entry"],
                      "research_prompt": manifest["research_prompt"]}, "program receipt route")
    prompt = (ROOT / manifest["research_prompt"]).read_text()
    require(len(re.findall(r"(?ms)^~~~text\n(.*?)^~~~\s*$", prompt)) == 1, "pasteable prompt")
    for marker in (branch, board, save, "用户完整指导", "论文内化", "gpt-6.1-sol", "ultra"):
        require(marker in prompt, "prompt missing " + marker)
    links = 0
    paths = [ROOT / name for name in ("README.md", "RESEARCH_STATE.md", "CLAIMS.md",
                                      "FAILED_ROUTES.md", "AGENTS.md")]
    paths += list(TOPIC.rglob("*.md"))
    for path in paths:
        text = re.sub(r"(?ms)^(```|~~~).*?^\1\s*$", "", path.read_text())
        for ref in re.findall(r"(?<!\\)\[[^\]\n]+\]\(([^)\s]+)\)", text):
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", ref) or ref.startswith("#"):
                continue
            dest = (path.parent / ref.split("#", 1)[0]).resolve()
            require(dest.is_relative_to(ROOT) and dest.exists(), f"broken link {path}: {ref}")
            links += 1
    count, ids = 0, set()
    pool = TOPIC / "candidate_pool.json"
    if pool.exists():
        rows = json.loads(pool.read_text())
        for row in rows:
            for field in ("id", "title", "origin", "source_url", "source_location",
                          "exact_question", "minimal_target", "known_overlap", "fatal_risk", "status"):
                require(isinstance(row.get(field), str) and row[field].strip(),
                        f"incomplete {row.get('id')}: {field}")
            require(row["id"] not in ids, "duplicate candidate ID " + row["id"])
            require(row["origin"] in ("A", "B", "C"), "provenance category")
            require(row["status"] in ("probe", "reserve", "exclude", "needs_verification"), "status")
            require(row["source_url"].startswith("https://"), "source URL")
            ids.add(row["id"])
        count = len(rows)
    return {"research_branch": branch, "board_branch": board, "save": save,
            "checked_local_links": links, "candidates": count,
            "limits": "routing/schema checks only; no openness/novelty/proof certification"}


if __name__ == "__main__":
    print(json.dumps(check(), ensure_ascii=False, indent=2))
