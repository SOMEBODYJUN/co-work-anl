#!/usr/bin/env python3
"""Structural exact replay for the contracted sparse input JSON."""
from __future__ import annotations
import argparse, collections, hashlib, json
from fractions import Fraction
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    raw = args.input.read_bytes()
    d = json.loads(raw)
    machines, jobs = d["machines"], d["jobs"]
    labels = collections.Counter(m[0] for m in machines)
    m_lengths = collections.Counter((m[0], len(m[2]) if len(m) >= 3 else 0) for m in machines if m[0] != "z")
    elig_counts = collections.Counter(len(j["eligible"]) for j in jobs)
    times = collections.Counter(v for j in jobs for _, v in j["eligible"])
    degrees = collections.Counter()
    for j in jobs:
        for mi, _ in j["eligible"]:
            if mi < 0 or mi >= len(machines): raise ValueError("machine index out of range")
            degrees[mi] += 1
    source_ids = [j["source_job_id"] for j in jobs]
    if len(set(source_ids)) != len(source_ids): raise ValueError("duplicate source_job_id")
    result = {
        "input_sha256": hashlib.sha256(raw).hexdigest(),
        "parameters": {k: d[k] for k in ("k", "H", "gamma", "threshold")},
        "machine_count": len(machines), "machine_labels": dict(labels),
        "machine_payload_length_counts": {f"{a}:{b}": n for (a, b), n in sorted(m_lengths.items())},
        "job_count": len(jobs), "job_eligibility_counts": dict(elig_counts),
        "finite_processing_time_counts": dict(times),
        "eligible_edge_count": sum(times.values()),
        "machine_degree_counts": dict(collections.Counter(degrees.values())),
        "zero_degree_machines": sum(1 for i in range(len(machines)) if degrees[i] == 0),
        "source_job_id_unique": True,
        "source_job_id_range": [min(source_ids), max(source_ids)],
        "scope": "structural exact replay of the contracted input; no probe or makespan claim by this script",
    }
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output: args.output.write_text(text)
    else: print(text, end="")


if __name__ == "__main__":
    main()
