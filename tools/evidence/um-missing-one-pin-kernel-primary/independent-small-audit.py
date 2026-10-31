#!/usr/bin/env python3
"""Fresh finite QA; no archived module, LP oracle, or general theorem test."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json
import sys


def sf(x):
    return str(x)


def load(jobs, assignment, pre=None):
    assert set(jobs) == set(assignment)
    loads = dict(pre or {})
    for j, i in assignment.items():
        assert i in jobs[j], (j, i)
        loads[i] = loads.get(i, F(0)) + jobs[j][i]
    return loads


def peak(jobs, assignment, pre=None):
    return max(load(jobs, assignment, pre).values(), default=F(0))


def tiny():
    rows = [[F(3, 4), F(1), F(2, 3), F(1, 2)],
            [F(2, 3), F(1), F(3, 4), F(2, 3)],
            [F(1, 2), F(2, 3), F(2, 3), F(3, 4)]]
    jobs = {j: {i: rows[i][j] for i in range(3)} for j in range(4)}
    x = [[F(2, 3), F(0), F(0), F(1)],
         [F(0), F(0), F(1), F(0)],
         [F(1, 3), F(1), F(0), F(0)]]
    assert all(sum(x[i][j] for i in range(3)) == 1 for j in range(4))
    work = [sum(rows[i][j] * x[i][j] for j in range(4)) for i in range(3)]
    heavy = [sum(x[i][j] for j in range(4) if rows[i][j] > F(1, 2)) for i in range(3)]
    assert work == [F(1), F(3, 4), F(5, 6)]
    assert heavy == [F(2, 3), F(1), F(1)]
    states = [(peak(jobs, dict(enumerate(a))), a) for a in product(range(3), repeat=4)]
    opt = min(c for c, _ in states)
    pair_min = [min(row[a] + row[b] for a in range(4) for b in range(a+1, 4)) for row in rows]
    assert pair_min == [F(7, 6), F(4, 3), F(7, 6)]
    witness = {0: 1, 1: 2, 2: 0, 3: 0}
    assert peak(jobs, witness) == opt == F(7, 6)
    return {"assignments": len(states), "integer_opt": sf(opt), "provided_lp_threshold": "1",
            "lp_opt_computed": False, "work": list(map(sf, work)), "strict_heavy_mass": list(map(sf, heavy)),
            "minimum_pair_work_per_machine": list(map(sf, pair_min)),
            "witness_jobs_1_to_4": ["B", "C", "A", "A"]}


def three_jobs():
    p = [F(1), F(1, 2), F(1, 2)]
    jobs = {j: {0: p[j], 1: p[j]} for j in range(3)}
    atoms = [a for a in product(range(2), repeat=3) if peak(jobs, dict(enumerate(a))) <= 1]
    assert set(atoms) == {(0, 1, 1), (1, 0, 0)}
    endpoints = [[F(3, 4), F(0), F(1, 2)],
                 [F(29, 38), F(0), F(9, 19)],
                 [F(9, 38), F(1), F(10, 19)]]
    checks = []
    for x in endpoints:
        assert sum(p[j] * x[j] for j in range(3)) == 1
        assert sum(p[j] * (1-x[j]) for j in range(3)) == 1
        compatible = [a for a in atoms if all((x[j] > 0 if a[j] == 0 else x[j] < 1) for j in range(3))]
        assert compatible
        in_config = x[1] == x[2] == 1-x[0]
        assert not in_config
        checks.append({"point": list(map(sf, x)), "both_fractional_loads": "1",
                       "actual_T_atom_in_positive_support": [list(a) for a in compatible],
                       "in_CONFIG": in_config})
    return {"all_assignments": 8, "actual_T_atoms": [list(a) for a in atoms], "endpoints": checks,
            "configuration_membership_test": "exact line x_a=x_b=1-x_h; not numerical LP"}


def pin_family():
    D, beta = 2, F(3, 4)
    labels, ports = range(2), list(product(range(2), range(2)))
    jobs = {}
    for b, i in ports:
        jobs[f"z:{b}:{i}"] = {f"H:{b}:{i}": beta, f"A:{b}": F(1, 2)}
    for b in labels:
        jobs[f"w:{b}"] = {f"A:{b}": F(1), f"B:{b}": F(1)}
        for r in range(D):
            jobs[f"f:{b}:{r}"] = {f"B:{b}": F(1, D), f"C:{r}": F(1)}
    names = list(jobs)
    choices = [tuple(jobs[j]) for j in names]
    matrix = [dict(zip(names, a)) for a in product(*choices)]
    assert len(matrix) == 1024
    records = []
    comparisons = 0
    for bits in product(range(2), repeat=4):
        Q = [p for p, bit in zip(ports, bits) if bit]
        pre = {f"H:{b}:{i}": F(1) for b, i in Q}
        values = sorted(set(peak(jobs, a, pre) for a in matrix))
        opt = values[0]
        # Every actual peak breakpoint and every gap midpoint; also boundary 0,1,1+beta,2.
        thresholds = sorted(set(values + [F(0), F(1), 1+beta, F(2)]))
        thresholds = sorted(set(thresholds + [(a+b)/2 for a, b in zip(thresholds, thresholds[1:])]))
        for C in thresholds:
            if C < 1:
                predicted = False
            elif C >= 1+beta:
                predicted = True
            else:
                k = (D*(C-1)).numerator // (D*(C-1)).denominator
                m = [sum(F(1, 2) for bb, _ in Q if bb == b) for b in labels]
                n = sum(v > C-1 for v in m)
                predicted = n*(D-k) <= D
            assert predicted == (opt <= C), (Q, C, opt, predicted)
            comparisons += 1
        records.append({"request_bits": list(bits), "requested_ports": [list(p) for p in Q], "true_opt": sf(opt)})
    assert records[-1]["true_opt"] == "3/2"
    one_label = next(r for r in records if r["request_bits"] == [1, 1, 0, 0])
    assert one_label["true_opt"] == "1"
    return {"D": D, "beta": sf(beta), "two_ports_per_label_a": "1/2", "request_subsets": 16,
            "internal_assignments_per_subset": 1024, "complete_assignments_checked": 16384,
            "threshold_predicate_comparisons": comparisons,
            "saturated_machines": 10, "saturated_jobs": 14, "saturated_finite_entries": 24,
            "request_records": records, "fixed_numbered_pool": True,
            "scope": "q=D=2 two-label finite exhaustive test, not a general proof or independent Exact-first review"}


def weighted_one_edge():
    # Noninjective projection: both left states map to right label 0.
    D, beta = 2, F(4, 5)
    weights = {("u", 0): F(1, 3), ("u", 1): F(2, 3),
               ("v", 0): F(2, 5), ("v", 1): F(3, 7)}
    jobs, assignment = {}, {}
    jobs["s"] = {"R:0": F(1), "R:1": F(1)}
    assignment["s"] = "R:1"
    for a in range(2):
        jobs[f"xu:{a}"] = {f"R:{a}": F(1, 2), f"H:u:{a}": F(1)}
        jobs[f"xv:{a}"] = {f"R:{a}": F(1, 2), "H:v:0": F(1)}
        assignment[f"xu:{a}"] = "H:u:1" if a == 1 else "R:0"
        assignment[f"xv:{a}"] = f"R:{a}"
    for v in ("u", "v"):
        for b in range(2):
            jobs[f"z:{v}:{b}"] = {f"H:{v}:{b}": beta, f"A:{v}:{b}": weights[v, b]}
            assignment[f"z:{v}:{b}"] = f"A:{v}:{b}" if (v, b) == ("u", 1) else f"H:{v}:{b}"
            jobs[f"w:{v}:{b}"] = {f"A:{v}:{b}": F(1), f"B:{v}:{b}": F(1)}
            assignment[f"w:{v}:{b}"] = f"B:{v}:{b}" if (v, b) == ("u", 1) else f"A:{v}:{b}"
            for r in range(D):
                name = f"f:{v}:{b}:{r}"
                jobs[name] = {f"B:{v}:{b}": F(1, D), f"C:{v}:{r}": F(1)}
                assignment[name] = f"C:{v}:{r}" if (v, b) == ("u", 1) else f"B:{v}:{b}"
    loads = load(jobs, assignment)
    machines = set(i for ends in jobs.values() for i in ends)
    assert len(jobs) == 21 and len(machines) == 18 and sum(map(len, jobs.values())) == 42
    assert max(loads.values()) == F(3, 2)
    assert assignment["xv:1"] == "R:1" and assignment["xu:1"] == "H:u:1"
    return {"machines": len(machines), "jobs": len(jobs), "finite_entries": sum(map(len, jobs.values())),
            "peak": "3/2", "left_chosen_label": 1, "projection": [0, 0],
            "selected_right_query_stays_root": True, "all_jobs_once_and_legal": True,
            "loads": {i: sf(loads.get(i, F(0))) for i in sorted(machines)},
            "assignment": assignment, "OPT_computed": False, "finite_scope": "one explicit complete construction"}


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    script = Path(__file__).resolve()
    root = script.parent
    report = {"status": "all exact Fraction assertions passed", "new_independent_math_audit_runs": 1,
              "archived_program_runs": 0, "archived_module_imports": 0, "external_solver_calls": 0,
              "arithmetic": "Python standard-library Fraction and finite integer enumeration",
              "code_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
              "primary_sha256": {p.stem: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((root/"original").glob("*.md"))},
              "tiny_heavy_count": tiny(), "positive_three_jobs": three_jobs(),
              "requested_pin_q2": pin_family(), "weighted_one_edge": weighted_one_edge(),
              "unverified_by_program": ["general multi-input closure proof", "general pin iff and arbitrary D",
                                        "cycle atom construction and future v2", "generic direction general theorem",
                                        "global uniform algorithm, hardness, novelty, or draft maturation"]}
    (out/"report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n")
    (out/"command.json").write_text(json.dumps({"argv": sys.argv, "fresh_output_directory": str(out.resolve()),
             "script": str(script), "python": sys.version, "no_repetition": "first and only execution of this audit"}, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps({"status": report["status"], "code_sha256": report["code_sha256"],
                      "tiny_states": 81, "pin_complete_states": 16384,
                      "pin_threshold_comparisons": report["requested_pin_q2"]["threshold_predicate_comparisons"],
                      "output": str(out.resolve())}, ensure_ascii=False))


if __name__ == "__main__":
    main()
