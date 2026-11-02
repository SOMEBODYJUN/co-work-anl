"""Static deliverable check only; no policy generation, IC or LP execution."""
import ast
import hashlib
import itertools
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[4]


def main():
    manifest = json.loads((ROOT / "artifact-manifest.json").read_text())
    for item in manifest["files"]:
        data = (REPO / item["path"]).read_bytes()
        assert len(data) == item["bytes"], item["path"]
        assert hashlib.sha256(data).hexdigest() == item["sha256"], item["path"]
    sources = json.loads((ROOT / "source-manifest.json").read_text())
    for item in sources["primary_sources"]:
        frozen = (REPO / item["saved_path"]).read_bytes()
        prior = (REPO / item["prior_related_copy"]).read_bytes()
        assert frozen == prior
        assert hashlib.sha256(frozen).hexdigest() == item["sha256"]
    json_files = list(ROOT.rglob("*.json"))
    for path in json_files:
        json.loads(path.read_text())
    py_files = list(ROOT.rglob("*.py"))
    for path in py_files:
        ast.parse(path.read_text(), filename=str(path))
    verification = json.loads((ROOT / "regenerated/verification.json").read_text())
    run = json.loads((ROOT / "regeneration-execution.json").read_text())
    script_sha = hashlib.sha256((ROOT / "regenerate_and_check.py").read_bytes()).hexdigest()
    assert verification["script_sha256"] == run["script_sha256"] == script_sha
    assert run["exit_code"] == 0
    assert verification["record_count"] == 12
    expected = {h for d in range(5) for h in itertools.product(range(7), repeat=d)}
    for record in verification["records"]:
        policy = json.loads((ROOT / record["policy"]["path"]).read_text())
        actions = {tuple(row["history"]): row["action"] for row in policy["actions"]}
        assert set(actions) == expected and len(policy["actions"]) == len(expected)
        assert all(0 <= a < 7 and a not in h for h, a in actions.items())
        assert policy["status"] == "current_seed_regeneration_not_historical_policy_bytes"
        assert record["historical_path_matches"]
    link_count = 0
    for md in manifest["markdown_files"]:
        file = REPO / md
        for link in re.findall(r"\]\(([^)]+)\)", file.read_text()):
            if "://" in link or link.startswith("#"):
                continue
            target = (file.parent / link.split("#", 1)[0]).resolve()
            assert target.exists(), (md, link)
            link_count += 1
    out = {"status": "static_checks_passed", "artifact_hashes_checked": len(manifest["files"]),
           "primary_source_copies_checked": len(sources["primary_sources"]),
           "json_files_parsed": len(json_files), "python_AST_files_checked": len(py_files),
           "complete_regenerated_policies_checked": 12, "local_links_checked": link_count,
           "original_or_math_entry_calls": 0, "LP_calls": 0,
           "excluded_from_artifact_manifest": ["artifact-manifest.json", "self-check.json"]}
    (ROOT / "self-check.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out))


if __name__ == "__main__":
    main()
