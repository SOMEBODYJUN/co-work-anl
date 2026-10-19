"""Independent exact finite audit of the occurrence-cycle construction.

All times are multiplied by two: unit jobs have size 2, others size 1.
This enumerates *all* assignments using finite incidences; it imports no
repository implementation or proof.
"""

from collections import Counter, defaultdict
from itertools import product
import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys


DEFAULT_REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
CANONICAL_PROOF = Path("research/current/unrelated_machines/top_two_pair_witness_boundary.md")


def top_two_score(machine_jobs):
    """Full B_2 objective: include a singleton; use zero for an empty machine."""
    return max((sum(sorted(sizes, reverse=True)[:2])
                for sizes in machine_jobs), default=0)


def build(clauses):
    occurrences = []
    cycles = defaultdict(list)
    for c, clause in enumerate(clauses):
        for variable, positive in clause:
            i = len(occurrences)
            occurrences.append((c, variable, positive))
            cycles[variable].append(i)
    successor = {}
    for indices in cycles.values():
        for t, i in enumerate(indices):
            successor[i] = indices[(t + 1) % len(indices)]
    jobs = []
    for i in range(len(occurrences)):
        jobs.append((f"s{i}", 2, (2 * i, 2 * i + 1)))
    for i in range(len(occurrences)):
        jobs.append((f"f{i}", 1, (2 * i, 2 * successor[i] + 1)))
    for c in range(len(clauses)):
        ports = tuple(2 * i + (0 if positive else 1)
                      for i, (which, variable, positive) in enumerate(occurrences)
                      if which == c)
        jobs.append((f"u{c}", 1, ports))
    return occurrences, cycles, jobs


def decode(clauses, occurrences, cycles, jobs, assignment):
    n = len(occurrences)
    bits = tuple(assignment[i] % 2 for i in range(n))
    values = {}
    for variable, indices in cycles.items():
        assert len({bits[i] for i in indices}) == 1
        values[variable] = bits[indices[0]]
    for c in range(len(clauses)):
        machine = assignment[2 * n + c]
        i = machine // 2
        which, variable, positive = occurrences[i]
        assert which == c
        assert values[variable] == positive
    return values


def inspect(clauses):
    occurrences, cycles, jobs = build(clauses)
    n = len(occurrences)
    eligibility_degree = Counter(machine for _, _, ports in jobs for machine in ports)
    assert max(len(ports) for _, _, ports in jobs) <= 3
    assert max(eligibility_degree.values()) <= 3
    total = 0
    min_makespan = None
    min_pair = None
    exact_counts = Counter()
    decoder_count = 0
    witness = None
    for assignment in product(*(ports for _, _, ports in jobs)):
        machine_jobs = [[] for _ in range(2 * n)]
        for (_, size, _), machine in zip(jobs, assignment):
            machine_jobs[machine].append(size)
        makespan = max(sum(sizes) for sizes in machine_jobs)
        pair = top_two_score(machine_jobs)
        min_makespan = makespan if min_makespan is None else min(min_makespan, makespan)
        min_pair = pair if min_pair is None else min(min_pair, pair)
        exact_counts[(makespan, pair)] += 1
        total += 1
        if pair <= 2:  # exactly the same forbidden-pair set for all 1 <= rho < 3/2
            decode(clauses, occurrences, cycles, jobs, assignment)
            decoder_count += 1
        if witness is None or makespan < witness[0]:
            witness = makespan, assignment, tuple(sum(sizes) for sizes in machine_jobs)
    # Independently check all truth assignments against strict schedules.
    variables = sorted(cycles)
    sat = any(all(any(bool(values[variable]) == positive for variable, positive in clause)
                      for clause in clauses)
              for values in (dict(zip(variables, bits))
                             for bits in product((0, 1), repeat=len(variables))))
    assert (decoder_count > 0) == sat
    assert min_makespan == (2 if sat else 3)
    assert min_pair == (2 if sat else 3)
    return {
        "formula": clauses,
        "occurrences": n,
        "machines": 2 * n,
        "jobs": len(jobs),
        "finite_incidences": sum(len(ports) for _, _, ports in jobs),
        "max_machine_degree": max(eligibility_degree.values()),
        "max_job_degree": max(len(ports) for _, _, ports in jobs),
        "all_assignments_enumerated": total,
        "sat_by_truth_table": sat,
        "twice_opt": min_makespan,
        "twice_min_pair_objective": min_pair,
        "low_pair_assignments_decoded": decoder_count,
        "histogram_twice_makespan_twice_pair": {
            f"{c},{b}": count for (c, b), count in sorted(exact_counts.items())
        },
        "minimum_schedule": {
            "assignment": dict((job[0], machine)
                               for job, machine in zip(jobs, witness[1])),
            "twice_machine_loads": witness[2],
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True,
                        help="Explicit new JSON file; existing files are never overwritten.")
    parser.add_argument("--repository-root", type=Path,
                        default=DEFAULT_REPOSITORY_ROOT,
                        help="Repository read only for base commit and final-proof provenance.")
    args = parser.parse_args()
    out = args.output.expanduser().resolve()
    if out.exists():
        parser.error(f"refusing to overwrite existing output: {out}")
    if not out.parent.is_dir():
        parser.error(f"output parent directory does not exist: {out.parent}")
    repository_root = args.repository_root.expanduser().resolve()
    try:
        basecommit = subprocess.check_output(
            ["git", "-C", str(repository_root), "rev-parse", "HEAD"],
            text=True, stderr=subprocess.PIPE,
        ).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        parser.error(f"could not read repository base commit: {exc}")
    source_path = Path(__file__).resolve()
    proof_path = repository_root / CANONICAL_PROOF
    try:
        proof_hash = hashlib.sha256(proof_path.read_bytes()).hexdigest()
    except OSError as exc:
        parser.error(f"could not read canonical proof for provenance: {exc}")
    boundary_checks = {
        "empty_machine_list": top_two_score([]),
        "all_empty_machines": top_two_score([[], []]),
        "singleton_unit": top_two_score([[2], []]),
        "singleton_half": top_two_score([[], [1]]),
        "unit_and_half_pair": top_two_score([[2, 1], []]),
        "ignore_third_half_in_top_two": top_two_score([[2, 1, 1], []]),
    }
    assert boundary_checks == {
        "empty_machine_list": 0,
        "all_empty_machines": 0,
        "singleton_unit": 2,
        "singleton_half": 1,
        "unit_and_half_pair": 3,
        "ignore_third_half_in_top_two": 3,
    }
    cases = {
        "ring_length_one": [[("x", True), ("y", True), ("z", True)]],
        "ring_length_two": [[("x", True), ("x", False), ("y", True)]],
        "single_pure_clause": [[("x", True), ("x", True), ("x", True)]],
        "contradictory_pure_clauses": [
            [("x", True), ("x", True), ("x", True)],
            [("x", False), ("x", False), ("x", False)],
        ],
    }
    results = {name: inspect(clauses) for name, clauses in cases.items()}
    report = {
        "provenance": {
            "source_path": str(source_path),
            "source_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
            "PythonVersion": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "python_full_version": sys.version,
            "repository_root": str(repository_root),
            "basecommit": basecommit,
            "canonical_proof_path": str(proof_path),
            "canonical_proof_sha256": proof_hash,
            "time_scale": 2,
            "objective": "maximum over machines of the largest at most two assigned sizes; singleton included",
            "representation": "f_i uses positive port i and negative port successor; canonical implication cycle reverses the chosen cyclic ordering",
        },
        "twice_objective_boundary_checks": boundary_checks,
        "cases": results,
    }
    try:
        with out.open("x", encoding="utf-8") as handle:
            handle.write(json.dumps(report, indent=2) + "\n")
    except FileExistsError:
        parser.error(f"refusing to overwrite existing output: {out}")
    for name, result in results.items():
        print(name, {k: result[k] for k in (
            "all_assignments_enumerated", "sat_by_truth_table", "twice_opt",
            "twice_min_pair_objective", "low_pair_assignments_decoded")})
    print(out)


if __name__ == "__main__":
    main()
