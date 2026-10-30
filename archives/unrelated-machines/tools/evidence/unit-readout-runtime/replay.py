#!/usr/bin/env python3
"""Replay frozen constructors and recheck literal inputs, matrices and schedules.

The checker below imports neither constructor nor the shared model kernel.
It does not implement a general OPT, configuration LP or forest search oracle.
Use a fresh --run-dir; all original stdout/stderr and explicit CLI inputs remain.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def dump(p, obj):
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def literal_model(data):
    """Reconstruct all original jobs directly from explicit leaf addresses."""
    k, h = int(data["k"]), int(data["h"])
    capacities = list(map(int, data["clause_capacities"]))
    nodes, tree_rows, roots, arity = {}, [], [], [0] * len(capacities)
    for v, variable in enumerate(data["variables"]):
        pair = []
        for sign, name in enumerate(("positive", "negative")):
            leaves = {tuple(row["path"]): row["clause"] for row in variable[name]}
            assert len(leaves) == len(variable[name])
            assert len(leaves) == k ** h
            parents = sorted({p[:depth] for p in leaves for depth in range(h)}, key=lambda p: (len(p), p))
            for p in parents:
                nodes[v, sign, p] = len(nodes)
            for p, c in leaves.items():
                assert len(p) == h and all(0 <= z < k for z in p)
                arity[c] += 1
            pair.append(nodes[v, sign, ()])
            tree_rows.append((v, sign, leaves, parents))
        roots.append(pair)
    internal = len(nodes)
    starts, cursor = [], internal
    for a in capacities:
        starts.append(cursor)
        cursor += a
    jobs = []
    for v, pair in enumerate(roots):
        jobs.append({"kind": "selector", "variable": v, "edges": [(u, F(1)) for u in pair]})
    for v, sign, leaves, parents in tree_rows:
        for parent in parents:
            for digit in range(k):
                path = parent + (digit,)
                small = nodes[v, sign, parent]
                row = {"kind": "port" if len(path) == h else "edge", "variable": v,
                       "sign": sign, "path": list(path), "parent": small,
                       "edges": [(small, F(1, k))]}
                if len(path) == h:
                    c = leaves[path]
                    row.update(clause=c, external={"start": starts[c], "count": capacities[c], "time": F(1)})
                    row["edges"] += [(starts[c] + z, F(1)) for z in range(min(capacities[c], arity[c]))]
                else:
                    child = nodes[v, sign, path]
                    row.update(child=child)
                    row["edges"].append((child, F(1)))
                jobs.append(row)
    listed = set(range(internal))
    for c, a in enumerate(capacities):
        listed.update(range(starts[c], starts[c] + min(a, arity[c])))
    if cursor == 0:
        listed.add(0)
    return jobs, roots, listed, max(1, cursor), internal


def literal_schedule(data, result, counts):
    jobs, roots, listed, machine_count, internal = literal_model(data)
    assert len(jobs) == len(result["jobs"]) == len(result["sigma"])
    assert roots == result["roots"]
    assert machine_count == result["full_machine_count"]
    assert internal == result["internal_machine_count"]
    load = Counter()
    for j, (expected, emitted, u) in enumerate(zip(jobs, result["jobs"], result["sigma"])):
        assert emitted["job"] == j
        for key, value in expected.items():
            if key == "edges":
                assert [(a, F(b)) for a, b in emitted[key]] == value
            elif key == "external":
                assert {**emitted[key], "time": F(emitted[key]["time"])} == value
            else:
                assert emitted[key] == value
        assert type(u) is int and 0 <= u < machine_count
        edges = dict(expected["edges"])
        if u in edges:
            p = edges[u]
        else:
            ext = expected["external"]
            assert ext["start"] <= u < ext["start"] + ext["count"]
            p = F(1)
        load[u] += p
        counts["literal_original_job_assignments"] += 1
    assert max(load.values(), default=F(0)) == F(result["makespan"]) <= F(result["bound"])
    assert {r["machine"] for r in result["listed_loads"]} == listed
    for row in result["listed_loads"]:
        assert F(row["load"]) == load[row["machine"]]
        counts["literal_listed_load_records"] += 1
    assert all(u in listed or value == 0 for u, value in load.items())
    assert F(result["omitted_unit_machine_load"]) == 0
    assert all(value <= 1 for u, value in load.items() if u >= internal)
    if "prescribed_signs" in result:
        assert all(result["sigma"][v] == roots[v][s] for v, s in enumerate(result["prescribed_signs"]))
    counts["literal_complete_schedules"] += 1


def sharp_profiles(path, counts):
    data = json.loads(path.read_text())
    assert set(data) == {"scope", "certificates"}
    assert data["scope"] == "prescribed all-positive profile only; global OPT is 1"
    rows = []
    for p, cert in enumerate(data["certificates"], 1):
        k, m, n = cert["k"], cert["num_machines"], cert["num_jobs"]
        assert cert["h"] == 1 and k == 2 * p - 1
        assert cert["num_variables"] == cert["num_given_schedules"] == p
        assert cert["clause_capacities"] == [k, (p - 1) * k]
        assert m == 2 * p + p * k and n == p + 2 * p * k
        assert cert["prescribed_root_machines"] == list(range(0, 2 * p, 2))
        assert cert["unavailable_edge"] is None
        assert F(cert["unconstrained_optimum"]) == 1
        bound = F(2) - F(1, k)
        assert F(cert["exact_prescribed_profile_optimum"]) == bound
        matrix = cert["processing_times_machine_by_job"]
        assert len(matrix) == m and all(len(row) == n for row in matrix)
        # Check every finite AND null cell against the explicit two-shared-clause family.
        for u, row in enumerate(matrix):
            for j, cell in enumerate(row):
                expected = None
                if j < p:
                    if u in (2 * j, 2 * j + 1): expected = F(1)
                else:
                    v, remainder = divmod(j - p, 2 * k)
                    sign = int(remainder >= k)
                    if u == 2 * v + sign: expected = F(1, k)
                    if sign == 0 and 2 * p <= u < 2 * p + k: expected = F(1)
                    if sign == 1 and 2 * p + k <= u < m: expected = F(1)
                actual = None if cell is None else F(cell)
                assert actual == expected
                counts["sharp_all_matrix_cells"] += 1
                counts["sharp_finite_matrix_cells"] += int(actual is not None)
        for i, record in enumerate(cert["given_yes"] + [cert["prescribed_output"]]):
            assert len(record["sigma"]) == n and len(record["loads"]) == m
            loads = [F(0)] * m
            for j, u in enumerate(record["sigma"]):
                assert type(u) is int and 0 <= u < m and matrix[u][j] is not None
                loads[u] += F(matrix[u][j])
                counts["sharp_job_assignments"] += 1
            assert loads == list(map(F, record["loads"]))
            counts["sharp_all_load_records"] += m
            if i < p:
                assert record["positive_variable"] == i
                assert record["sigma"][:p] == [2*v + int(v != i) for v in range(p)]
                assert max(loads) == 1
            else:
                assert record["sigma"][:p] == cert["prescribed_root_machines"]
                assert max(loads) == bound
            counts["sharp_complete_schedules"] += 1
        rows.append({"p": p, "machines": m, "jobs": n, "given_yes": p,
                     "profile_optimum": str(bound), "global_optimum": "1",
                     "lower_bound_method": "symbolic root/export counting, not enumeration"})
    assert len(rows) == 4
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    base = Path(__file__).resolve().parent
    original = base / "original"
    run = Path(args.run_dir).resolve()
    run.mkdir(parents=True, exist_ok=False)
    counts, commands = Counter(), []

    def command(name, script, arguments):
        cmd = [sys.executable, str(original / script), *arguments]
        process = subprocess.run(cmd, capture_output=True, text=True)
        (run / (name + ".stdout")).write_text(process.stdout)
        (run / (name + ".stderr")).write_text(process.stderr)
        commands.append({"name": name, "argv": cmd, "cwd": str(Path.cwd()), "exit_code": process.returncode,
                         "stdout": name + ".stdout", "stderr": name + ".stderr"})
        dump(run / "commands.json", commands)
        assert process.returncode == 0, name
        return json.loads((run / (name + ".json")).read_text())

    leaf = command("leaf-audit", "unit_readout_leaf_flow.py", ["--output", str(run / "leaf-audit.json")])
    mixing = command("mixing-audit", "unit_readout_selector_mixing.py", ["--output", str(run / "mixing-audit.json")])
    assert leaf["status"] == mixing["status"] == "passed"
    for case in leaf["cases"]:
        literal_schedule(case["input"], case["result"], counts)
    for case in mixing["full_original_certificates"]:
        literal_schedule(case["instance"], case["result"], counts)
        for sigma in case["yes_schedules"]:
            # Use a separately reconstructed literal result to check each given YES.
            jobs, roots, listed, full_m, internal = literal_model(case["instance"])
            loads = Counter()
            for job, u in zip(jobs, sigma):
                edges = dict(job["edges"])
                if u in edges: value = edges[u]
                else:
                    ext = job["external"]
                    assert ext["start"] <= u < ext["start"] + ext["count"]
                    value = F(1)
                loads[u] += value
            assert len(sigma) == len(jobs) and max(loads.values(), default=F(0)) <= 1
            counts["given_yes_complete_schedules"] += 1
            counts["given_yes_job_assignments"] += len(jobs)
    # Exercise both real --input/--output CLIs on saved explicit payloads.
    leaf_input = leaf["cases"][0]["input"]
    dump(run / "leaf-input.json", leaf_input)
    leaf_cli = command("leaf-cli", "unit_readout_leaf_flow.py", ["--input", str(run / "leaf-input.json"), "--output", str(run / "leaf-cli.json")])
    literal_schedule(leaf_input, leaf_cli, counts)
    first = mixing["full_original_certificates"][0]
    mixing_input = {key: first[key] for key in ("instance", "yes_schedules", "prescribed_signs")}
    dump(run / "mixing-input.json", mixing_input)
    mixing_cli = command("mixing-cli", "unit_readout_selector_mixing.py", ["--input", str(run / "mixing-input.json"), "--output", str(run / "mixing-cli.json")])
    literal_schedule(mixing_input["instance"], mixing_cli, counts)
    profiles = sharp_profiles(original / "unit_readout_selector_mixing_sharp_profiles.json", counts)
    report = {"status": "passed", "python": platform.python_version(), "counts": dict(counts),
              "leaf_audit_counts": leaf["counts"], "mixing_audit_counts": mixing["counts"],
              "leaf_cases": [{"name": case["name"], "b": case["result"]["b"], "r": case["result"]["r"], "makespan": case["result"]["makespan"]} for case in leaf["cases"]],
              "sharp_profiles": profiles, "commands": commands,
              "source_sha256": {p.name: sha(p) for p in sorted(original.iterdir()) if p.is_file()},
              "scope": "Exact finite original-input and matrix recheck. No general OPT/LP backend, no exhaustive schedule/forest enumeration, no new theorem or independent full-stack constructor."}
    dump(run / "verification.json", report)
    print(json.dumps({"status": report["status"], "counts": report["counts"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
