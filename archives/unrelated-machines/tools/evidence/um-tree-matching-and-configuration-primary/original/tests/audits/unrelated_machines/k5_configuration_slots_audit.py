"""Self-contained exact K5 CONFIG/ST counterexample audit.

Reproduce:
python3 tests/audits/unrelated_machines/k5_configuration_slots_audit.py

No numerical solver, external package, or other audit module is used.
"""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


def ceil(q):
    return -((-q.numerator) // q.denominator)


def main():
    source = Path(__file__).resolve()
    sizes = (F(1), F(1, 3), F(1, 4), F(2, 9), F(3, 16))
    patterns = (
        ((1, 0, 0, 0, 0), F(1, 144)),
        ((0, 0, 1, 0, 4), F(1, 4)),
        ((0, 0, 4, 0, 0), F(3, 16)),
        ((0, 1, 0, 3, 0), F(1, 3)),
        ((0, 3, 0, 0, 0), F(2, 9)),
    )
    copies = tuple(max(a[t] for a, _ in patterns) for t in range(5))
    labels = [(t, r) for t, count in enumerate(copies) for r in range(count)]
    name = lambda label: f"j{label[0]}_{label[1]}"
    private = lambda label: f"P{label[0]}_{label[1]}"
    jobs = {name(label): {"H": sizes[label[0]], private(label): F(1)} for label in labels}
    configurations = {"H": []}
    for counts, weight in patterns:
        chosen = [name(label) for label in labels if label[1] < counts[label[0]]]
        configurations["H"].append((tuple(chosen), weight))

    x = {(machine, job): F(0) for job, options in jobs.items() for machine in options}
    for chosen, weight in configurations["H"]:
        for job in chosen:
            x["H", job] += weight
    for label in labels:
        job, machine = name(label), private(label)
        configurations[machine] = [((job,), 1 - x["H", job]), ((), x["H", job])]
        x[machine, job] = 1 - x["H", job]

    # Validate every configuration and the same global point's job coverage.
    max_count = 0
    config_report = {}
    reconstructed = {edge: F(0) for edge in x}
    for machine, row in configurations.items():
        assert sum(weight for _, weight in row) == 1
        config_report[machine] = []
        for chosen, weight in row:
            assert weight >= 0 and len(chosen) == len(set(chosen))
            cost = sum((jobs[job][machine] for job in chosen), F(0))
            assert cost <= 1
            if weight > 0:
                max_count = max(max_count, len(chosen))
            for job in chosen:
                reconstructed[machine, job] += weight
            config_report[machine].append({"jobs": chosen, "weight": str(weight), "load": str(cost)})
    assert reconstructed == x and max_count == 5
    for job, options in jobs.items():
        assert sum(x[machine, job] for machine in options) == 1
        assert all(0 <= x[machine, job] <= 1 for machine in options)
        values = sorted(options.values())
        assert values[-1] == 1 and len(options) == 2
        assert values[0] < 1 or values == [1, 1]

    # Construct the actual sorted interval/slot graph on all 16 machines.
    machines = ["H"] + [private(label) for label in labels]
    graph, intervals, slot_report = {}, {}, {}
    for machine in machines:
        eligible = [job for job, options in jobs.items() if machine in options]
        order = sorted(eligible, key=lambda job: (-jobs[job][machine], job))
        current = F(0)
        intervals[machine] = {}
        for job in order:
            right = current + x[machine, job]
            intervals[machine][job] = (current, right)
            current = right
        slot_report[machine] = []
        for k in range(ceil(current)):
            adjacent = []
            for job, (left, right) in intervals[machine].items():
                overlap = min(right, F(k + 1)) - max(left, F(k))
                if overlap > 0:
                    graph[machine, k + 1, job] = overlap
                    adjacent.append({"job": job, "overlap": str(overlap),
                                     "processing_time": str(jobs[job][machine])})
            assert adjacent
            slot_report[machine].append({"slot": k + 1, "adjacent": adjacent,
                "maximum_time": str(max(jobs[e["job"]][machine] for e in adjacent))})

    group_counts = [sum((x["H", name(label)] for label in labels if label[0] == t), F(0))
                    for t in range(5)]
    prefix_counts, current = [], F(0)
    for count in group_counts:
        current += count
        prefix_counts.append(current)
    margins = [count - t for t, count in enumerate(prefix_counts)]
    assert margins == [F(1, 144)] * 5
    maxima = [F(slot["maximum_time"]) for slot in slot_report["H"]]
    assert maxima == list(sizes)
    envelope = sum(maxima, F(0))
    assert envelope == F(287, 144)
    assert envelope - (2 - F(1, 120)) == F(1, 720)

    selected = {(0, 0): 1}
    selected.update({(t, copies[t] - 1): t + 1 for t in range(1, 5)})
    bad_matching = [("H", selected[label], name(label)) if label in selected
                    else (private(label), 1, name(label)) for label in labels]
    good_matching = [(private(label), 1, name(label)) for label in labels]

    def verify_matching(matching):
        assert len(matching) == len(jobs)
        assert len({job for _, _, job in matching}) == len(jobs)
        assert len({(machine, slot) for machine, slot, _ in matching}) == len(jobs)
        loads = {machine: F(0) for machine in machines}
        edges = []
        for machine, slot, job in matching:
            assert graph[machine, slot, job] > 0
            loads[machine] += jobs[job][machine]
            edges.append({"job": job, "machine": machine, "slot": slot,
                          "overlap": str(graph[machine, slot, job]),
                          "processing_time": str(jobs[job][machine])})
        return {"edges": edges, "loads": {m: str(v) for m, v in loads.items()},
                "makespan": str(max(loads.values()))}

    bad, good = verify_matching(bad_matching), verify_matching(good_matching)
    assert F(bad["makespan"]) == envelope and F(good["makespan"]) == 1
    assert all(graph["H", slot, name(label)] == F(1, 144) for label, slot in selected.items())
    unit_job = name((0, 0))
    assert set(jobs[unit_job].values()) == {F(1)}  # unconditional OPT >= 1
    result = {
        "title": "五任务配置的阶乘ST槽界反例：精确实际调度核验",
        "arithmetic": "Python fractions.Fraction; no floating point or solver",
        "reproduction_command": f"python {source}",
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "K": 5, "job_count": len(jobs), "machine_count": len(machines), "b": "1", "T_CONFIG": "1",
        "sizes": list(map(str, sizes)), "copies": copies,
        "primary_count_patterns": [{"counts": a, "weight": str(w)} for a, w in patterns],
        "jobs": {job: {m: str(p) for m, p in options.items()} for job, options in jobs.items()},
        "all_machine_configurations": config_report,
        "all_assignment_marginals": {m: {job: str(x[m, job]) for job in jobs if (m, job) in x} for m in machines},
        "primary_fractional_load": str(sum(jobs[job]["H"] * x["H", job] for job in jobs)),
        "primary_home_qualification_sum": str(sum(n * s for n, s in zip(copies[1:], sizes[1:]))),
        "group_counts": list(map(str, group_counts)), "prefix_counts": list(map(str, prefix_counts)),
        "strict_prefix_margins": list(map(str, margins)),
        "all_machine_intervals": {m: {j: list(map(str, pair)) for j, pair in row.items()} for m, row in intervals.items()},
        "all_ST_slots_and_positive_edges": slot_report,
        "primary_slot_maxima": list(map(str, maxima)), "primary_envelope": str(envelope),
        "refuted_factorial_bound": str(2 - F(1, 120)), "strict_excess": "1/720",
        "bad_actual_complete_ST_matching": bad, "good_actual_complete_ST_matching": good,
        "OPT": "1", "OPT_lower_bound": f"Task {unit_job} has processing time 1 at every finite endpoint.",
        "scope": "Refutes the universal 2-1/K! ST-envelope/all-matchings bound at K=5; does not refute choosing or repairing a matching.",
    }
    assert len(jobs) == 15 and len(machines) == 16
    result["reproduction_command"] = "python3 tests/audits/unrelated_machines/k5_configuration_slots_audit.py"
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
