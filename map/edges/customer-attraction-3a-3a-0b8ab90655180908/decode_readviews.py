"""Decode the fully displayed read views; compare JSON data without running research code."""
import argparse
import hashlib
import json
from pathlib import Path


def decode(view_path):
    view = json.loads(view_path.read_text(encoding="utf-8"))
    if view_path.name.startswith("matrix-"):
        data = [
            {"rivals_counts": [int(c) for c in history], "query_values": values}
            for history, values in view["rows"]
        ]
    elif view_path.name == "security-policy-reversible.json":
        dictionary = json.loads(
            (view_path.parent / view["strategy_dictionary_ref"]).read_text(encoding="utf-8")
        )
        histories = dictionary
        for part in view["strategy_dictionary_path"]:
            histories = histories[part]
        data = dict(view["metadata"])
        data["strategy"] = {
            "/".join(history): view["strategy_action"] for history in histories
        }
    else:
        data = dict(view["metadata"])
        data["policy"] = [
            {"history": [int(c) for c in history], "action": run["action"]}
            for run in view["runs"]
            for history in run["histories"]
        ]
    return view, data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo_root", type=Path)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    report = []
    for view_path in sorted(here.glob("*-reversible.json")):
        view, reconstructed = decode(view_path)
        raw = (args.repo_root / view["source"]).read_bytes()
        original = json.loads(raw)
        actual_sha = hashlib.sha256(raw).hexdigest()
        if actual_sha != view["source_sha256"] or reconstructed != original:
            raise ValueError("Read view does not reproduce source: " + view["source"])
        report.append({
            "source": view["source"],
            "source_sha256": actual_sha,
            "encoding": view_path.name,
            "decoded_equals_original_json": True,
        })
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
