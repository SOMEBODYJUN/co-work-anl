#!/usr/bin/env python3
"""三host单位预载接口的二色单调拼接与三半锐界。

Given two actual complete schedules of the same unrelated-machine jobs:
S1 has only host a free, S2 has only hosts b,c free, and their makespans
including blocked-host preload T are at most T.  The constructor returns
an actual complete schedule with only b or only c free and makespan at
most 3*T/2.  Internal machines have no additional external preload.

The polynomial constructor never searches for the two YES schedules.
It uses their original finite edges, nonnegative S1 row weights, and a
monotone binary bootstrap.  Other eligible edges remain available in the
input.  The exhaustive assignment oracle is nested in audit() only.

JSON input schema for --input:
  {"p": [["1/2", "1/2"], [1, null], [null, 1]],
   "S1": [0, 0], "S2": [1, 2], "T": 1,
   "hosts": {"a": 0, "b": 1, "c": 2}}
null denotes an unavailable edge.  Exact times are int, Fraction, or
integer/fraction strings; bool and float are rejected.  With no --input,
the finite reproducible audit is written to stdout as JSON.
"""
from __future__ import annotations

from fractions import Fraction
import re


def _rational(value):
    if type(value) in (int, Fraction):
        out = Fraction(value)
    elif type(value) is str and re.fullmatch(r"\+?\d+(?:/\+?\d+)?", value):
        try:
            out = Fraction(value)
        except (ValueError, ZeroDivisionError) as error:
            raise ValueError("invalid exact rational") from error
    else:
        raise ValueError("expected exact rational, not bool or float")
    if out < 0:
        raise ValueError("negative processing time or threshold")
    return out


def _matrix(p):
    if type(p) not in (list, tuple) or not p:
        raise ValueError("nonempty explicit machine matrix required")
    if any(type(row) not in (list, tuple) for row in p):
        raise ValueError("each matrix row must be a list or tuple")
    n = len(p[0])
    if any(len(row) != n for row in p):
        raise ValueError("rectangular machine matrix required")
    clean = [[None if value is None else _rational(value) for value in row]
             for row in p]
    if any(all(row[j] is None for row in clean) for j in range(n)):
        raise ValueError("a job has no finite eligible edge")
    return clean


def _assignment(p, sigma):
    m, n = len(p), len(p[0])
    if type(sigma) not in (list, tuple) or len(sigma) != n:
        raise ValueError("one machine ID is required for each job")
    out = list(sigma)
    for j, i in enumerate(out):
        if type(i) is not int or not 0 <= i < m or p[i][j] is None:
            raise ValueError("unavailable or invalid assignment")
    return out


def _task_loads(p, sigma):
    out = [Fraction(0)] * len(p)
    for j, i in enumerate(sigma):
        out[i] += p[i][j]
    return out


def construct_three_host_selector(p, S1, S2, T=1, a=0, b=1, c=2):
    """Validate the two YES witnesses and construct an actual bad profile.

    A blocked host has fixed, nonmigrating preload T.  S1 is checked with
    b,c blocked; S2 is checked with a blocked.  T=0 and empty job sets are
    accepted.  Invalid inputs or non-YES witnesses raise ValueError.

    Return sigma, free_host, loads (including the new profile), task_loads,
    preloads, W, colors, flip_order, YES task loads, T, and the exact bound.
    Every returned time or load is a Fraction.  The host IDs may be any
    three distinct machine IDs; eligibility may have arbitrary support.
    """
    p = _matrix(p)
    m, n = len(p), len(p[0])
    T = _rational(T)
    if any(type(i) is not int or not 0 <= i < m for i in (a, b, c)) \
            or len({a, b, c}) != 3:
        raise ValueError("three distinct valid integer host IDs required")
    S1 = _assignment(p, S1)
    S2 = _assignment(p, S2)
    load1, load2 = _task_loads(p, S1), _task_loads(p, S2)
    preload1 = [Fraction(0)] * m
    preload2 = [Fraction(0)] * m
    preload1[b] = preload1[c] = T
    preload2[a] = T
    if any(load1[i] + preload1[i] > T for i in range(m)):
        raise ValueError("S1 is not a YES schedule with only a free")
    if any(load2[i] + preload2[i] > T for i in range(m)):
        raise ValueError("S2 is not a YES schedule with only b,c free")

    # For j, use directed edge S1(j)->S2(j) of weight p[S1(j),j].
    # A reverse incidence list updates all row weights affected by a flip.
    reverse = [[] for _ in range(m)]
    toward_one = [Fraction(0)] * m
    for j in range(n):
        source, destination = S1[j], S2[j]
        weight = p[source][j]
        reverse[destination].append((source, weight))
        if destination == b:
            toward_one[source] += weight
    colors = [0] * m
    colors[b] = 1
    flip_order = []
    while True:
        chosen = None
        for i in range(m):
            if i in (b, c) or colors[i]:
                continue
            if 2 * toward_one[i] >= load1[i]:
                chosen = i
                break
        if chosen is None:
            break
        colors[chosen] = 1
        flip_order.append(chosen)
        for source, weight in reverse[chosen]:
            toward_one[source] += weight

    W = [i for i in range(m) if colors[i] == colors[a]]
    inside = set(W)
    free_host = b if b in inside else c
    sigma = [S2[j] if S1[j] in inside and S2[j] in inside else S1[j]
             for j in range(n)]
    task_loads = _task_loads(p, sigma)
    preloads = [Fraction(0)] * m
    preloads[a] = T
    preloads[c if free_host == b else b] = T
    loads = [task_loads[i] + preloads[i] for i in range(m)]
    bound = Fraction(3, 2) * T
    if max(loads) > bound:
        raise RuntimeError("majority splice violated its proved load bound")
    return {
        "sigma": sigma, "free_host": free_host, "loads": loads,
        "task_loads": task_loads, "preloads": preloads, "W": W,
        "colors": colors, "flip_order": flip_order,
        "yes1_task_loads": load1, "yes2_task_loads": load2,
        "T": T, "bound": bound,
    }


def solve_json_instance(data):
    """Read the documented exact JSON object without changing its instance."""
    if type(data) is not dict:
        raise ValueError("JSON instance must be an object")
    if not all(key in data for key in ("p", "S1", "S2")):
        raise ValueError("JSON instance requires p, S1, S2")
    hosts = data.get("hosts", {"a": 0, "b": 1, "c": 2})
    if type(hosts) is not dict or set(hosts) != {"a", "b", "c"}:
        raise ValueError("hosts must contain exactly a,b,c")
    return construct_three_host_selector(
        data["p"], data["S1"], data["S2"], data.get("T", 1), **hosts,
    )


def audit():
    """Reproducible finite tests; complete assignment oracles only here."""
    import hashlib
    import json
    from itertools import product
    from math import lcm
    from pathlib import Path
    from random import Random

    def oracle(p, T, a=0, b=1, c=2):
        # Enumerate every eligible full assignment using exact integer loads.
        # Clearing denominators is for speed, not a numerical approximation.
        p = _matrix(p)
        T = _rational(T)
        denominator = T.denominator
        for row in p:
            for value in row:
                if value is not None:
                    denominator = lcm(denominator, value.denominator)
        unit = int(T * denominator)
        choices = [[(i, int(p[i][j] * denominator))
                    for i in range(len(p)) if p[i][j] is not None]
                   for j in range(len(p[0]))]
        best = {b: None, c: None}
        witness = {b: None, c: None}
        assignments = 0
        for assignment in product(*choices):
            task = [0] * len(p)
            sigma = []
            for i, time in assignment:
                task[i] += time
                sigma.append(i)
            for free in (b, c):
                total = task[:]
                total[a] += unit
                total[c if free == b else b] += unit
                makespan = max(total)
                if best[free] is None or makespan < best[free]:
                    best[free] = makespan
                    witness[free] = sigma
            assignments += 1
        return {
            "best": {free: Fraction(value, denominator)
                     for free, value in best.items()},
            "witness": witness, "assignments": assignments,
        }

    def verify(p, S1, S2, T, a=0, b=1, c=2):
        clean = _matrix(p)
        T = _rational(T)
        answer = construct_three_host_selector(clean, S1, S2, T, a, b, c)
        m, n = len(clean), len(S1)
        # Recompute every original task assignment and its outside preload.
        actual = [Fraction(0)] * m
        for j, i in enumerate(answer["sigma"]):
            assert clean[i][j] is not None
            actual[i] += clean[i][j]
        assert actual == answer["task_loads"]
        preloads = [Fraction(0)] * m
        preloads[a] = T
        preloads[c if answer["free_host"] == b else b] = T
        actual = [actual[i] + preloads[i] for i in range(m)]
        assert actual == answer["loads"]
        assert max(actual) <= Fraction(3, 2) * T
        assert answer["free_host"] in (b, c)
        # Replay every flip against original task identities and row weights.
        colors = [0] * m
        colors[b] = 1
        old_load = [sum((clean[i][j] for j in range(n) if S1[j] == i), Fraction(0))
                    for i in range(m)]
        for i in answer["flip_order"]:
            assert i not in (b, c) and colors[i] == 0
            toward = sum((clean[i][j] for j in range(n)
                          if S1[j] == i and colors[S2[j]] == 1), Fraction(0))
            assert 2 * toward >= old_load[i]
            colors[i] = 1
        assert colors == answer["colors"]
        assert len(answer["flip_order"]) <= m - 2
        assert len(set(answer["flip_order"])) == len(answer["flip_order"])
        for i in range(m):
            if i in (b, c):
                continue
            cross = sum((clean[i][j] for j in range(n)
                         if S1[j] == i and colors[S2[j]] != colors[i]), Fraction(0))
            assert 2 * cross <= old_load[i]
        inside = set(answer["W"])
        assert inside == {i for i in range(m) if colors[i] == colors[a]}
        assert (b in inside) != (c in inside)
        for j, machine in enumerate(answer["sigma"]):
            expected = S2[j] if S1[j] in inside and S2[j] in inside else S1[j]
            assert machine == expected
        optimum = oracle(clean, T, a, b, c)
        assert optimum["best"][answer["free_host"]] <= max(actual)
        assert min(optimum["best"].values()) <= Fraction(3, 2) * T
        return answer, optimum

    rng = Random(202610171103)
    random_cases = assignments = total_flips = 0
    largest = Fraction(0)
    for _ in range(7000):
        internal_count = rng.randrange(0, 5)
        m = 3 + internal_count
        n = rng.randrange(1, 11)
        internal = list(range(3, m))
        S1 = [rng.choice([0] + internal) for _ in range(n)]
        S2 = [rng.choice([i for i in [1, 2] + internal if i != source])
              for source in S1]
        fixed = [Fraction(0)] * m
        for i in internal:
            fixed[i] = Fraction(rng.randrange(0, 5), 4)
        p = [[None] * n for _ in range(m)]
        for sigma in (S1, S2):
            for i in range(m):
                jobs = [j for j in range(n) if sigma[j] == i]
                if not jobs:
                    continue
                parts = [rng.randrange(1, 7) for _ in jobs]
                for j, part in zip(jobs, parts):
                    p[i][j] = (1 - fixed[i]) * Fraction(part, sum(parts))
        # Fixed internal work is a genuine forced original job.  In the
        # directed bootstrap it is a self-loop, not an external preload.
        for i in internal:
            for row in p:
                row.append(None)
            p[i][-1] = fixed[i]
            S1.append(i)
            S2.append(i)
        answer, optimum = verify(p, S1, S2, 1)
        random_cases += 1
        assignments += optimum["assignments"]
        total_flips += len(answer["flip_order"])
        largest = max(largest, max(answer["loads"]))

    sharp_p = [[Fraction(1, 2), Fraction(1, 2)], [1, None], [None, 1]]
    sharp, sharp_optimum = verify(sharp_p, [0, 0], [1, 2], 1)
    assignments += sharp_optimum["assignments"]
    assert sharp_optimum["best"] == {1: Fraction(3, 2), 2: Fraction(3, 2)}
    assert max(sharp["loads"]) == Fraction(3, 2)
    boundary_cases = [
        ([[], [], []], [], [], 1, 0, 1, 2),
        ([[], [], []], [], [], 0, 0, 1, 2),
        ([[0], [0], [0]], [1], [0], 1, 0, 1, 2),
        ([[0], [0], [0], [0]], [0], [3], 1, 3, 1, 2),
        (sharp_p + [[Fraction(1, 7), Fraction(1, 11)]],
         [0, 0], [1, 2], 1, 0, 1, 2),
        ([[0, 0], [0, None], [None, 0]], [0, 0], [1, 2], 0, 0, 1, 2),
    ]
    boundaries = []
    for p, S1, S2, T, a, b, c in boundary_cases:
        answer, optimum = verify(p, S1, S2, T, a, b, c)
        assignments += optimum["assignments"]
        boundaries.append({
            "hosts": {"a": a, "b": b, "c": c}, "T": T,
            "free_host": answer["free_host"], "loads": answer["loads"],
            "true_bad_profile_optima": optimum["best"],
            "eligible_full_assignments": optimum["assignments"],
        })
    # Tiny positive scales and huge denominators do not change iteration count.
    scale_records = []
    for T in (Fraction(7, 3), Fraction(1, 10**100 + 267)):
        p = [[None if time is None else Fraction(time) * T for time in row]
             for row in sharp_p]
        answer, optimum = verify(p, [0, 0], [1, 2], T)
        assert max(answer["loads"]) == Fraction(3, 2) * T
        assert all(value == Fraction(3, 2) * T for value in optimum["best"].values())
        assignments += optimum["assignments"]
        scale_records.append({"T": T, "loads": answer["loads"],
                              "flip_order": answer["flip_order"]})

    invalid = [
        ([], [], [], 1, 0, 1, 2),
        ([[0], []], [0], [0], 1, 0, 1, 2),
        ([[None], [None], [None]], [0], [0], 1, 0, 1, 2),
        ([[True], [0], [0]], [0], [0], 1, 0, 1, 2),
        ([[0.0], [0], [0]], [0], [0], 1, 0, 1, 2),
        ([[-1], [0], [0]], [0], [0], 1, 0, 1, 2),
        ([["1/0"], [0], [0]], [0], [0], 1, 0, 1, 2),
        ([[0], [0], [0]], [True], [0], 1, 0, 1, 2),
        ([[0], [0], [0]], [0], [0], True, 0, 1, 2),
        ([[0], [0], [0]], [0], [0], 1.0, 0, 1, 2),
        ([[0], [0], [0]], [0], [0], -1, 0, 1, 2),
        ([[0], [0], [0]], [0], [0], 1, 0, 0, 2),
        ([[0], [0], [0]], [0], [0], 1, 0, True, 2),
        ([[0], [0], [0]], [0], [0], 1, 0, 1, 3),
        (sharp_p, [1, 0], [1, 2], 1, 0, 1, 2),
        (sharp_p, [0, 0], [0, 2], 1, 0, 1, 2),
        (sharp_p, [0], [1, 2], 1, 0, 1, 2),
        (sharp_p, [0, 0], [2, 2], 1, 0, 1, 2),
    ]
    for case in invalid:
        try:
            construct_three_host_selector(*case)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid input or YES witness accepted")
    json_case = {"p": [["1/2", "1/2"], [1, None], [None, 1]],
                 "S1": [0, 0], "S2": [1, 2], "T": "1",
                 "hosts": {"a": 0, "b": 1, "c": 2}}
    assert solve_json_instance(json_case) == sharp
    sample_relative = "examples/unrelated_machines/three_host_selector_sharp_profiles.json"
    sample_path = Path(__file__).resolve().parents[3] / sample_relative
    sample_bytes = sample_path.read_bytes()
    sample = json.loads(sample_bytes)
    hosts = sample.get("hosts", {"a": 0, "b": 1, "c": 2})
    sample_answer = solve_json_instance(sample)
    sample_checked, sample_optimum = verify(
        sample["p"], sample["S1"], sample["S2"], sample.get("T", 1), **hosts,
    )
    assert sample_answer == sample_checked
    if "expected_bad_optima" in sample:
        assert sample_optimum["best"][hosts["b"]] == \
            _rational(sample["expected_bad_optima"]["only_b"])
        assert sample_optimum["best"][hosts["c"]] == \
            _rational(sample["expected_bad_optima"]["only_c"])
    assignments += sample_optimum["assignments"]
    proof_relative = "research/current/unrelated_machines/three_host_selector_sharp_three_halves.md"
    proof_path = Path(__file__).resolve().parents[3] / proof_relative
    return {
        "status": "passed", "precision": "exact Fraction / integers; no tolerance",
        "seed": 202610171103, "random_instances": random_cases,
        "full_assignments_enumerated": assignments,
        "random_bootstrap_flips": total_flips,
        "largest_random_unit_scale_makespan": largest,
        "sharp_example": {"p": sharp_p, "S1": [0, 0], "S2": [1, 2],
                          "constructed": sharp, "exact_bad_profile_optima": sharp_optimum["best"],
                          "eligible_full_assignments": sharp_optimum["assignments"]},
        "boundary_cases": boundaries, "scaled_sharp_cases": scale_records,
        "invalid_cases_rejected": len(invalid),
        "official_sample": {
            "path": sample_relative,
            "sha256": hashlib.sha256(sample_bytes).hexdigest(),
            "witness": sample_answer,
            "exact_bad_profile_optima": sample_optimum["best"],
            "eligible_full_assignments": sample_optimum["assignments"],
            "santa_sharp_section_checked": False,
        },
        "oracle": "every eligible full assignment, exact denominator-cleared loads",
        "source_proof": {
            "path": proof_relative,
            "sha256": hashlib.sha256(proof_path.read_bytes()).hexdigest(),
            "claim_id": "UM-THREE-HOST-SELECTOR-THREE-HALVES-v1",
            "scope": "finite three-host audit only; does not assign canonical status",
            "other_claims_checked": [],
        },
        "limits": [
            "does not find the two YES schedules",
            "does not prove hardness or an approximation for arbitrary scheduling inputs",
            "finite audits do not replace the general bootstrap proof",
            "no novelty or external-review certification",
        ],
    }


def main():
    import argparse
    import hashlib
    import json
    from pathlib import Path
    import platform
    import sys

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="read one documented JSON instance")
    parser.add_argument("--output", type=Path,
                        help="write a NEW JSON file, refusing existing files")
    args = parser.parse_args()
    if args.input is None:
        result = audit()
    else:
        input_bytes = args.input.read_bytes()
        result = {"status": "constructed", "input": str(args.input),
                  "input_sha256": hashlib.sha256(input_bytes).hexdigest(),
                  "witness": solve_json_instance(json.loads(input_bytes))}
    result["runtime"] = {"implementation": platform.python_implementation(),
                         "python_version": platform.python_version()}
    result["code_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result["commands"] = {"actual_argv": [sys.executable, *sys.argv],
                          "stdout_reproduction": ["python3", "tests/audits/unrelated_machines/three_host_majority_selector.py"]}

    def encode(value):
        if isinstance(value, Fraction):
            return str(value)
        raise TypeError(type(value).__name__)

    payload = json.dumps(result, default=encode, ensure_ascii=False, indent=2) + "\n"
    if args.output is None:
        print(payload, end="")
    else:
        with args.output.open("x", encoding="utf-8") as output:
            output.write(payload)
        print(json.dumps({"status": result["status"], "output": str(args.output)},
                         ensure_ascii=False))


if __name__ == "__main__":
    main()
