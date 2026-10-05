#!/usr/bin/env python3
"""Check that the curated claims, code, evidence and moved sources still connect."""
from __future__ import annotations

import json
import hashlib
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str) -> dict:
    return json.loads((ROOT / "research" / name).read_text(encoding="utf-8"))


def require(condition: bool, message: object) -> None:
    if not condition:
        raise ValueError(message)


def check_learning(node_ids: set[str]) -> int:
    """Teaching routes reference claims but never substitute for proof assets."""
    manifest = json.loads((ROOT / "learning/manifest.json").read_text(encoding="utf-8"))
    require(manifest["schema_version"] == 1 and manifest["as_of"] and manifest["scope"],
            "incomplete learning manifest")
    paths = set()
    for module in manifest["modules"]:
        path = module["path"]
        require(path.startswith("learning/") and path.endswith(".md")
                and path not in paths and (ROOT / path).is_file(),
                ("invalid teaching file", path))
        paths.add(path)
        require(module["title"] and module["role"] and module["canonical_readings"], path)
        require(set(module["claims"]) <= node_ids, ("unknown teaching claim", path))
        for reading in module["canonical_readings"]:
            require(reading.startswith("research/current/") and (ROOT / reading).is_file(),
                    ("invalid canonical teaching source", path, reading))
        content = (ROOT / path).read_text(encoding="utf-8")
        for match in re.finditer(r"(?<!\\)\[[^\]\n]+\]\(([^)\s]+)\)", content):
            target = match.group(1)
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                continue
            filename = target.split("#", 1)[0]
            destination = ((ROOT / path).parent / filename).resolve()
            require(destination.is_relative_to(ROOT) and destination.exists(),
                    ("broken teaching link", path, target))
    actual = {p.relative_to(ROOT).as_posix() for p in (ROOT / "learning").rglob("*.md")}
    require(paths == actual, ("unclassified teaching files", sorted(actual - paths)))
    return len(paths)


def check() -> None:
    assets = load("assets.json")["entries"]
    graph = load("graph.json")
    review = load("review_status.json")
    migration = load("path_migration.json")
    node_ids = {node["id"] for node in graph["nodes"]}
    learning_count = check_learning(node_ids)
    for item in graph["nodes"] + graph["hyperedges"]:
        require(any(ref.startswith("research/current/") for ref in item["refs"]),
                ("mathematical relation lacks a current account", item["id"]))
    entry_ids = set()
    implementations = set()
    referenced = set()
    covered_claims = set()
    for entry in assets:
        require(entry["id"] not in entry_ids, entry["id"])
        entry_ids.add(entry["id"])
        require(entry["claims"] and set(entry["claims"]) <= node_ids, entry["id"])
        covered_claims.update(entry["claims"])
        require(entry["applies_when"] and entry["status"] and entry["produces"], entry["id"])
        require(entry["proof"] and entry["sources"] and entry["limit"], entry["id"])
        for field in ("implementation", "proof", "sources", "tests", "records", "examples"):
            for path in entry[field]:
                require((ROOT / path).is_file(), (entry["id"], path))
                expected = {"implementation": ("facility_spe/", "multi_facility_spe/"),
                            "proof": "research/current/",
                            "sources": "history/",
                            "tests": "tests/",
                            "records": "evidence/"}
                if field in expected:
                    require(path.startswith(expected[field]),
                            ("incorrect asset role", entry["id"], field, path))
                if field == "examples":
                    require(path.startswith(("examples/", "evidence/certificates/")),
                            ("incorrect example/certificate role", entry["id"], path))
                referenced.add(path)
                if field == "implementation":
                    implementations.add(path)
    all_claims = {node["id"] for node in graph["nodes"] if node["kind"] == "claim"}
    require(all_claims <= {row["id"] for row in review["entries"]},
            "claim-review ledger omits a graph claim")
    require(all_claims <= covered_claims,
            ("unclassified mathematical claim", sorted(all_claims - covered_claims)))
    canonical = {
        path.relative_to(ROOT).as_posix()
        for package in ("facility_spe", "multi_facility_spe")
        for path in (ROOT / package).rglob("*.py")
        if path.name != "__init__.py"
    }
    require(canonical <= implementations, ("unclassified implementation", canonical - implementations))
    for old, new in migration["moved"].items():
        require((ROOT / new).is_file(), (old, new))
        require(not (ROOT / old).exists(), ("retired path still exists", old))
    for old, new in migration["retired_code_paths"].items():
        require(not (ROOT / old).exists() and (ROOT / new).is_file(), (old, new))
    crosswalk = load("source_crosswalk.json")["entries"]
    originals = {row["original"]: row for row in crosswalk}
    expected_origins = {**migration["moved"], **migration["retired_code_paths"]}
    require(len(originals) == len(crosswalk) and set(originals) == set(expected_origins),
            "every original source/code path needs one current interpretation")
    for old, row in originals.items():
        require(row["preserved_at"] == expected_origins[old]
                and (ROOT / row["rewritten_in"]).is_file()
                and row["interpretation"], ("invalid source interpretation", old))
    for old, new in migration["first_curation_retired"].items():
        require(not (ROOT / old).exists() and (ROOT / new).is_file(), (old, new))
    for old, new in migration.get("reestablished_root_docs", {}).items():
        require((ROOT / old).is_file() and (ROOT / new).is_file(), (old, new))
    tracked = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT, text=True
    ).splitlines()
    roots = {"facility_spe", "multi_facility_spe", "tests", "examples", "evidence", "history", "research", "learning"}
    root_docs = {".gitignore", "AGENTS.md", "README.md", "ASSETS.md", "USAGE.md",
                 "RESEARCH_STATE.md", "CLAIMS.md", "FAILED_ROUTES.md"}
    unknown = {p for p in tracked if p.split("/", 1)[0] not in roots
               and p not in root_docs}
    require(not unknown, ("unclassified repository files", sorted(unknown)))
    for group in ("history/source/manuscripts", "history/source/notes",
                  "evidence", "examples", "research/current"):
        require(any(p.startswith(group + "/") for p in tracked), group)
    for manifest in (ROOT / "evidence/runs/2026-10-01").glob("*.json"):
        report = json.loads(manifest.read_text(encoding="utf-8"))
        require(report["schema_version"] == 1 and report["python_version"]
                and report["base_commit"] and report["replay_commands"]
                and report["source_sha256"] and report["limitations"],
                ("incomplete evidence manifest", manifest.name))
        for key in ("input", "certificate"):
            if key in report:
                source = ROOT / report[key]
                require(source.is_file() and hashlib.sha256(source.read_bytes()).hexdigest()
                        == report[key + "_sha256"],
                        ("evidence input/certificate changed", manifest.name, key))
    print(f"Validated {len(assets)} scoped asset routes, {len(implementations)} implementations, "
          f"{len(migration['moved'])} sourced files, "
          f"{len(crosswalk)} individually interpreted origins, "
          f"{len(tracked)} indexed paths, {learning_count} teaching routes and their local file links")


if __name__ == "__main__":
    check()
