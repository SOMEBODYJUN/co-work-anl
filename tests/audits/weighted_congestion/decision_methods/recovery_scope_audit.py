#!/usr/bin/env python3
"""Reproduce the factual scope comparison; no lost theorem is certified here."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import platform
import subprocess

ROOT = Path(__file__).resolve().parents[4]
PREVIOUS = "3efbaf6a65e04fd89c83baabb1c15f3ad3cf8951"
REFERENCE = "history/source/notes/weighted_congestion/structural_view_and_positive_results_reference.md"
REFERENCE_HASH = "c026cc8bf14bfcb5c669b3141ac5858dbca5ae4b0d9a24a701579ea6ea3e5e46"
MISSING = [
    "research/current/weighted_congestion/weight_bands/global_type_scale_compatibility.md",
    "research/current/weighted_congestion/global_weight_depth_threshold.md",
    "research/reviews/weighted_congestion/structural_depth_and_compatibility_review.md",
]


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True)


def forest(edges):
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    for u, v in edges:
        a, b = find(u), find(v)
        if a == b:
            return False
        parent[a] = b
    return True


def graphs(weights, users):
    incidence = [(('p', i), ('e', e)) for e, row in enumerate(users) for i in row]
    types = set()
    for row in users:
        values = sorted({weights[i] for i in row})
        types.update((a, b) for k, a in enumerate(values) for b in values[k + 1:])
    return dict(weights=weights, optional_users=users,
                incidence_forest=forest(incidence),
                type_forest=forest(sorted(types)), type_edges=sorted(types))


def run():
    assert sha256((ROOT / REFERENCE).read_bytes()).hexdigest() == REFERENCE_HASH
    missing = {p: git("cat-file", "-e", PREVIOUS + ":" + p).returncode == 0 for p in MISSING}
    assert not any(missing.values())
    proof = git("show", PREVIOUS + ":research/current/weighted_congestion/linear_degree_allstate_lower_bound.md")
    assert proof.returncode == 0 and b"p/10" in proof.stdout
    article = git("show", PREVIOUS + ":research/current/weighted_congestion/linear_threshold_article.tex")
    assert article.returncode == 0 and b"d/10" in article.stdout
    examples = [graphs([1, 2], [[0, 1], [0, 1]]), graphs([1, 2, 3], [[0, 1, 2]])]
    assert examples[0]["type_forest"] and not examples[0]["incidence_forest"]
    assert examples[1]["incidence_forest"] and not examples[1]["type_forest"]
    return dict(status="PASS", previous_commit=PREVIOUS,
                reference=dict(path=REFERENCE, sha256=REFERENCE_HASH),
                referenced_proofs_present_at_previous_commit=missing,
                previous_canonical_bound_contains="p/10; article d/10",
                forest_definitions_are_distinct=examples,
                python=platform.python_version(), source_sha256=sha256(Path(__file__).read_bytes()).hexdigest(),
                scope="File/snapshot and graph-definition checks only; does not reconstruct or prove the missing near-unit and structural theorems.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.dumps(run(), ensure_ascii=False, indent=2) + "\n"
    if args.output:
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(payload)
        print("PASS: recovery scope and graph distinctions checked")
    else:
        print(payload, end="")
