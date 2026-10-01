#!/usr/bin/env python3
"""Check that the curated claims, code, evidence and moved sources still connect."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str) -> dict:
    return json.loads((ROOT / "research" / name).read_text(encoding="utf-8"))


def require(condition: bool, message: object) -> None:
    if not condition:
        raise ValueError(message)


def check() -> None:
    assets = load("assets.json")["entries"]
    graph = load("graph.json")
    migration = load("path_migration.json")
    node_ids = {node["id"] for node in graph["nodes"]}
    entry_ids = set()
    implementations = set()
    referenced = set()
    for entry in assets:
        require(entry["id"] not in entry_ids, entry["id"])
        entry_ids.add(entry["id"])
        require(entry["claims"] and set(entry["claims"]) <= node_ids, entry["id"])
        require(entry["applies_when"] and entry["status"] and entry["produces"], entry["id"])
        require(entry["proof"] and entry["limit"], entry["id"])
        for field in ("implementation", "proof", "tests", "records", "examples"):
            for path in entry[field]:
                require((ROOT / path).is_file(), (entry["id"], path))
                referenced.add(path)
                if field == "implementation":
                    implementations.add(path)
    canonical = {
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "facility_spe").rglob("*.py")
        if path.name != "__init__.py"
    }
    require(canonical <= implementations, ("unclassified implementation", canonical - implementations))
    for old, new in migration["moved"].items():
        require((ROOT / new).is_file(), (old, new))
        if (ROOT / old).exists():
            require((ROOT / old).read_text().startswith(
                "#!/usr/bin/env python3\n\"\"\"Compatibility entry point"
            ), ("unexpected old copy", old))
    for old, new in migration["canonical_code_with_compatibility_entrypoints"].items():
        require((ROOT / old).is_file() and (ROOT / new).is_file(), (old, new))
        require("Compatibility entry point" in (ROOT / old).read_text(), old)
    tracked = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT, text=True
    ).splitlines()
    roots = {"math", "manuscripts", "facility_spe", "tests", "examples",
             "evidence", "history", "research"}
    legacy = set(migration["canonical_code_with_compatibility_entrypoints"])
    legacy |= {old for old in migration["moved"] if (ROOT / old).exists()}
    root_docs = {".gitignore", "README.md", "MODEL.md", "CLAIMS.md", "ASSETS.md",
                 "RESEARCH_STATE.md", "FAILED_ROUTES.md", "EVIDENCE.md",
                 "PROVENANCE.md", "LITERATURE.md", "USAGE.md"}
    unknown = {p for p in tracked if p.split("/", 1)[0] not in roots
               and p not in legacy and p not in root_docs}
    require(not unknown, ("unclassified repository files", sorted(unknown)))
    for group in ("manuscripts", "math/proofs", "evidence", "examples", "history"):
        require(any(p.startswith(group + "/") for p in tracked), group)
    print(f"Validated {len(assets)} scoped asset routes, {len(implementations)} implementations, "
          f"{len(migration['moved'])} moved files, {len(tracked)} indexed paths")


if __name__ == "__main__":
    check()
