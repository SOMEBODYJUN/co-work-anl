#!/usr/bin/env python3
"""Independent consistency checks for the frozen cartesian-menu audit exports.

This verifier consumes only the exported JSON files.  It checks the finite
instance shape, finite eligibility, witness schedule ownership/load data, and
the all-complementary-intersection certificate cardinalities.  It does not
turn the finite checks into a theorem for arbitrary t.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw"


def load(name: str):
    with (RAW / name).open() as f:
        return json.load(f)


def check_sparse(t: int, d: dict) -> dict:
    D = 2**t
    assert d["t"] == t
    assert d["time_denominator"] == D
    machines = d["machines"]
    jobs = d["jobs"]
    states = d["states"]
    assert len(machines) == 2 * D * D
    assert len(jobs) == D**3 + D
    assert len(states) == D * D
    kinds = {m["kind"] for m in machines}
    assert kinds == {"resource", "private"}
    selectors = [j for j in jobs if j["kind"] == "selector"]
    incidence = [j for j in jobs if j["kind"] == "incidence"]
    assert len(selectors) == D and len(incidence) == D**3
    assert all(len(j["finite"]) == D for j in selectors)
    assert all(all(e["time_units"] == D for e in j["finite"]) for j in selectors)
    assert all(len(j["finite"]) == 2 for j in incidence)
    assert all(sorted(e["time_units"] for e in j["finite"]) == [1, D] for j in incidence)
    assert sum(len(j["finite"]) for j in jobs) == D * D + 2 * D**3
    assert all(len(s["resource_machines"]) == D for s in states)
    return {
        "t": t,
        "groups": D,
        "states": D * D,
        "resource_machines": D * D,
        "private_machines": D * D,
        "jobs": D**3 + D,
        "finite_entries": D * D + 2 * D**3,
    }


def check_schedule(t: int, sparse: dict, schedule: dict) -> dict:
    D = 2**t
    assert schedule["t"] == t
    assert schedule["time_denominator"] == D
    jobs = {j["id"]: j for j in sparse["jobs"]}
    assignment = schedule["assignment"]
    assert len(assignment) == len(jobs)
    assert {a["job"] for a in assignment} == set(jobs)
    by_machine: dict[int, list[tuple[int, int, int]]] = {}
    for a in assignment:
        j = jobs[a["job"]]
        finite = {e["machine"]: e["time_units"] for e in j["finite"]}
        assert a["machine"] in finite
        assert a["time_units"] == finite[a["machine"]]
        assert a["finish_units"] - a["start_units"] == a["time_units"]
        by_machine.setdefault(a["machine"], []).append(
            (a["start_units"], a["finish_units"], a["job"])
        )
    loads = {x["machine"]: x["load_units"] for x in schedule["machine_load_units"]}
    assert len(loads) == len(sparse["machines"])
    for machine, entries in by_machine.items():
        entries.sort()
        assert all(entries[i][1] <= entries[i + 1][0] for i in range(len(entries) - 1))
        assert loads[machine] == sum(b - a for a, b, _ in entries)
    assert max(loads.values()) == schedule["makespan_units"] == D + 1
    assert schedule["makespan_rational"] == {"numerator": D + 1, "denominator": D}
    # The cyclic witness exports D-1 incidence jobs from each group.
    selected = schedule["selected_states"]
    assert len(selected) == D
    exported = [a for a in assignment if jobs[a["job"]]["kind"] == "incidence" and
                next(e for e in jobs[a["job"]]["finite"] if e["machine"] == a["machine"])["time_units"] == D]
    counts = {}
    for a in exported:
        g = tuple(jobs[a["job"]]["g"])
        counts[g] = counts.get(g, 0) + 1
    assert set(counts.values()) == {D - 1}
    assert len(counts) == D
    return {"t": t, "jobs_assigned": len(assignment), "peak_units": D + 1,
            "selected_export_count": len(exported), "exports_per_group": D - 1}


def check_intersections(t: int, d: dict) -> dict:
    D = 2**t
    assert d["t"] == t
    assert d["ordered_pairs_checked"] == D**3
    assert d["unordered_pairs_represented"] == D**3 // 2
    assert d["intersection_size_for_every_pair"] == 1
    assert len(d["certificates"]) == D**3
    return {"t": t, "ordered_pairs": D**3, "unordered_pairs": D**3 // 2,
            "certificates": len(d["certificates"]), "intersection_size": 1}


def main() -> None:
    sparse_by_t = {}
    schedule_names = {1: "9f20bd1fe1cb24a6611b.json", 2: "d31c8fb5a109166e917a.json",
                      3: "4749ddff3990fdd57b89.json", 4: "a255b68fc1fe411f65ac.json"}
    int_names = {1: "dff15670a727dd3abb9b.json", 2: "8a5d8529917979b0faf9.json",
                 3: "afcfbc027928d47d95db.json", 4: "7fadefe70c6decbeb63f.json"}
    sparse_names = {1: "3d813848364db08504d6.json", 2: "3de20e41c6f392f78253.json",
                    3: "bcb67b85cce5f09e3976.json", 4: "e84c459b64030e6ea3bc.json"}
    sparse_checks = []
    schedule_checks = []
    intersection_checks = []
    for t in range(1, 5):
        sparse = load(sparse_names[t])
        sparse_by_t[t] = sparse
        sparse_checks.append(check_sparse(t, sparse))
        schedule_checks.append(check_schedule(t, sparse, load(schedule_names[t])))
        intersection_checks.append(check_intersections(t, load(int_names[t])))
    opt = load("a95c81b2b07e0caa6fa9.json")
    assert opt["t"] == 1 and opt["complete_assignments_enumerated"] == 1024
    assert opt["exact_OPT_units"] == 3 and opt["time_denominator"] == 2
    out = {
        "scope": "independent JSON consistency checks; finite t=1..4 only",
        "source_exact_sha256": load("35dd9ecdc7697532b38a.json")["source_exact_sha256"],
        "sparse_checks": sparse_checks,
        "schedule_checks": schedule_checks,
        "intersection_checks": intersection_checks,
        "t1_opt_enumeration": {"assignments": 1024, "opt": "3/2"},
    }
    (ROOT / "verification.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
