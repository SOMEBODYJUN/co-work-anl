#!/usr/bin/env python3
"""多输出单位预载接口的有权闭包与实际轮廓边界。

construct_weighted_fanout uses only two supplied actual YES schedules.  A
blocked host has fixed nonmigrating preload T.  S1 has only a free among
{a}+outputs; S2 has a blocked and every output free.  Other machines have
no preload.  Output is a full legal schedule, all actual preloads/loads,
and the selected bound (2-beta_chosen)*T, using original finite edges.

missing_subset denotes the CANDIDATE output subset K, of size >=2, rather
than a set all blocked in the returned state.  Exactly a and K minus the
chosen host are blocked; every original output outside K is free.  beta
is a simplex vector indexed by the ordered K (or a dict with precisely
those host keys); default is uniform on K.  No optimum oracle is used by
the constructor.  Finite exhaustive optima occur only inside audit().

JSON --input keys: p (machine-by-job, null=unavailable), S1, S2, T, a,
outputs, optional beta and missing_subset.  Exact numbers are nonnegative
int, Fraction or integer/fraction strings; bool/float are rejected.
Default command writes audit JSON to stdout.  --output creates a NEW file
with exclusive mode and never overwrites an existing result.
"""
from __future__ import annotations

from fractions import Fraction
import re

SOURCE_CLAIMS = (
    "UM-WEIGHTED-FANOUT-PROFILE-BOUNDARY-v1",
    "UM-FANOUT-MISSING-ONE-THREE-HALVES-v1",
)


def _rational(value):
    if type(value) in (int, Fraction):
        out = Fraction(value)
    elif type(value) is str and re.fullmatch(r"\+?\d+(?:/\d+)?", value):
        try:
            out = Fraction(value)
        except (ValueError, ZeroDivisionError) as error:
            raise ValueError("invalid exact rational") from error
    else:
        raise ValueError("expected exact rational, not bool or float")
    if out < 0:
        raise ValueError("nonnegative exact rational required")
    return out


def _matrix(p):
    if type(p) not in (list, tuple) or not p:
        raise ValueError("nonempty explicit machine matrix required")
    if any(type(row) not in (list, tuple) for row in p):
        raise ValueError("machine rows must be explicit lists or tuples")
    n = len(p[0])
    if any(len(row) != n for row in p):
        raise ValueError("rectangular machine matrix required")
    clean = [[None if value is None else _rational(value) for value in row]
             for row in p]
    if any(all(row[j] is None for row in clean) for j in range(n)):
        raise ValueError("each job needs a finite eligible edge")
    return clean


def _assignment(p, sigma):
    m, n = len(p), len(p[0])
    if type(sigma) not in (list, tuple) or len(sigma) != n:
        raise ValueError("one actual machine ID is required per job")
    sigma = list(sigma)
    if any(type(i) is not int or not 0 <= i < m or p[i][j] is None
           for j, i in enumerate(sigma)):
        raise ValueError("invalid or unavailable assignment edge")
    return sigma


def _task_loads(p, sigma):
    loads = [Fraction(0)] * len(p)
    for j, i in enumerate(sigma):
        loads[i] += p[i][j]
    return loads


def _hosts_and_weights(m, a, outputs, beta, missing_subset):
    if type(outputs) not in (list, tuple) or len(outputs) < 2:
        raise ValueError("at least two explicitly ordered output hosts required")
    outputs = list(outputs)
    if type(a) is not int or not 0 <= a < m \
            or any(type(v) is not int or not 0 <= v < m for v in outputs) \
            or len(set([a] + outputs)) != len(outputs) + 1:
        raise ValueError("a and outputs must be distinct valid machine IDs")
    if missing_subset is None:
        candidates = outputs[:]
    elif type(missing_subset) in (set, frozenset):
        if any(type(v) is not int for v in missing_subset):
            raise ValueError("candidate hosts must be integer IDs")
        candidates = [v for v in outputs if v in missing_subset]
        if len(candidates) != len(missing_subset):
            raise ValueError("candidate hosts must belong to outputs")
    elif type(missing_subset) in (list, tuple):
        candidates = list(missing_subset)
    else:
        raise ValueError("candidate subset must be an explicit host subset")
    if len(candidates) < 2 \
            or any(type(v) is not int or v not in outputs for v in candidates) \
            or len(set(candidates)) != len(candidates):
        raise ValueError("candidate subset K needs at least two distinct outputs")
    k = len(candidates)
    if beta is None:
        weights = [Fraction(1, k)] * k
    elif type(beta) is dict:
        if any(type(v) is not int for v in beta) or set(beta) != set(candidates):
            raise ValueError("beta dictionary must contain exactly candidate hosts")
        weights = [_rational(beta[v]) for v in candidates]
    elif type(beta) in (list, tuple) and len(beta) == k:
        weights = [_rational(value) for value in beta]
    else:
        raise ValueError("beta must have one exact weight per candidate host")
    if sum(weights, Fraction(0)) != 1:
        raise ValueError("beta weights must sum exactly to one")
    return outputs, candidates, weights


def construct_weighted_fanout(p, S1, S2, T, a, outputs, beta=None,
                             missing_subset=None):
    """Return a concrete actual profile with C <= (2-beta_chosen)*T.

    The input YES contexts always refer to the FULL original output set.
    Candidate K = missing_subset defaults to outputs; a list/tuple retains
    its order, while a set uses original-output order.  beta is local to K.
    The constructor accepts T=0, zero times, empty job sets, arbitrary host
    indices and arbitrary original eligibility support.  Invalid input or
    a supplied schedule failing its YES context raises ValueError.

    Classes are closed sequentially with the ORIGINAL row total L_v:
    toward_class[v] >= beta_i * L_v.  Earlier classes freeze.  No residual
    normalization or numerical approximation occurs.  All returned times,
    loads and weights are Fractions; colors are zero-based candidate IDs.
    """
    p = _matrix(p)
    m, n = len(p), len(p[0])
    T = _rational(T)
    outputs, candidates, weights = _hosts_and_weights(
        m, a, outputs, beta, missing_subset)
    S1, S2 = _assignment(p, S1), _assignment(p, S2)
    load1, load2 = _task_loads(p, S1), _task_loads(p, S2)
    preload1, preload2 = [Fraction(0)] * m, [Fraction(0)] * m
    for host in outputs:
        preload1[host] = T
    preload2[a] = T
    if any(load1[v] + preload1[v] > T for v in range(m)):
        raise ValueError("S1 fails the original only-a-free YES context")
    if any(load2[v] + preload2[v] > T for v in range(m)):
        raise ValueError("S2 fails the all-original-outputs-free YES context")

    # Row v contains edges v=S1(j) -> S2(j) weighted by SOURCE time p[v,j].
    reverse = [[] for _ in range(m)]
    for j, (source, destination) in enumerate(zip(S1, S2)):
        reverse[destination].append((source, p[source][j]))
    k = len(candidates)
    colors = [-1] * m
    for color, host in enumerate(candidates):
        colors[host] = color
    absorption_order = []
    for color in range(k - 1):
        toward = [Fraction(0)] * m
        for destination in range(m):
            if colors[destination] == color:
                for source, time in reverse[destination]:
                    toward[source] += time
        while True:
            chosen = next((v for v in range(m) if colors[v] == -1
                           and toward[v] >= weights[color] * load1[v]), None)
            if chosen is None:
                break
            absorption_order.append({
                "machine": chosen, "color": color,
                "toward_before": toward[chosen],
                "threshold": weights[color] * load1[chosen],
            })
            colors[chosen] = color
            for source, time in reverse[chosen]:
                toward[source] += time
        # A final-class machine stays uncolored throughout each earlier closure.
        if any(toward[v] >= weights[color] * load1[v]
               for v in range(m) if colors[v] == -1):
            raise RuntimeError("closure stopped before reaching its threshold")
    last_class_unfixed = [v for v in range(m) if colors[v] == -1]
    for v in last_class_unfixed:
        colors[v] = k - 1
    if len(absorption_order) > m - k:
        raise RuntimeError("a machine entered more than one class")

    row_to_own = [Fraction(0)] * m
    for j, (source, destination) in enumerate(zip(S1, S2)):
        if colors[source] == colors[destination]:
            row_to_own[source] += p[source][j]
    if any(row_to_own[v] < weights[colors[v]] * load1[v] for v in range(m)):
        raise RuntimeError("weighted row-class quota failed")
    selected_color = colors[a]
    chosen_host, chosen_weight = candidates[selected_color], weights[selected_color]
    inside = {v for v in range(m) if colors[v] == selected_color}
    sigma = [S2[j] if S1[j] in inside and S2[j] in inside else S1[j]
             for j in range(n)]
    task_loads = _task_loads(p, sigma)
    splice_outgoing, splice_incoming = [Fraction(0)] * m, [Fraction(0)] * m
    for j, (source, destination) in enumerate(zip(S1, S2)):
        if source in inside and destination in inside:
            splice_outgoing[source] += p[source][j]
            splice_incoming[destination] += p[destination][j]
    if any(task_loads[v] != load1[v] - splice_outgoing[v] + splice_incoming[v]
           for v in range(m)):
        raise RuntimeError("actual per-machine splice identity failed")
    preloads = [Fraction(0)] * m
    preloads[a] = T
    for host in candidates:
        if host != chosen_host:
            preloads[host] = T
    loads = [task_loads[v] + preloads[v] for v in range(m)]
    bound = (2 - chosen_weight) * T
    if max(loads) > bound:
        raise RuntimeError("actual all-machine selected bound failed")
    return {
        "sigma": sigma, "chosen": chosen_host,
        "chosen_index": selected_color, "beta_chosen": chosen_weight,
        "outputs": outputs, "candidate_outputs": candidates,
        "beta": weights, "beta_by_host": dict(zip(candidates, weights)),
        "a": a, "T": T, "bound": bound, "selected_bound": bound,
        "preloads": preloads, "task_loads": task_loads, "loads": loads,
        "blocked": [a] + [v for v in candidates if v != chosen_host],
        "free_original_outputs": [v for v in outputs
                                  if v not in candidates or v == chosen_host],
        "colors": colors, "W": sorted(inside),
        "color_classes": [[v for v in range(m) if colors[v] == color]
                          for color in range(k)],
        "absorption_order": absorption_order,
        "last_class_unfixed": last_class_unfixed,
        "yes1_task_loads": load1, "yes2_task_loads": load2,
        "yes1_preloads": preload1, "yes2_preloads": preload2,
        "row_weight_to_own_color": row_to_own,
        "splice_outgoing": splice_outgoing, "splice_incoming": splice_incoming,
    }


def solve_json_instance(data):
    if type(data) is not dict or not all(key in data for key in
                                       ("p", "S1", "S2", "T", "a", "outputs")):
        raise ValueError("JSON requires p,S1,S2,T,a,outputs")
    beta = data.get("beta")
    if type(beta) is dict:
        converted = {}
        for host, weight in beta.items():
            if type(host) is str and re.fullmatch(r"\d+", host):
                host = int(host)
            if type(host) is not int or host in converted:
                raise ValueError("beta JSON host keys must be distinct machine IDs")
            converted[host] = weight
        beta = converted
    return construct_weighted_fanout(
        data["p"], data["S1"], data["S2"], data["T"], data["a"], data["outputs"],
        beta=beta, missing_subset=data.get("missing_subset"))


def audit():
    """Exact finite checks; assignment enumeration occurs only in this function."""
    import hashlib
    from itertools import combinations, product
    from math import lcm
    from pathlib import Path
    from random import Random
    import platform
    import time

    started = time.perf_counter()
    rng = Random(110709)
    counts = {}
    def count(key, amount=1):
        counts[key] = counts.get(key, 0) + amount

    def optimum_profiles(p, T, a, outputs):
        p = _matrix(p)
        T = _rational(T)
        denominator = T.denominator
        for row in p:
            for value in row:
                if value is not None:
                    denominator = lcm(denominator, value.denominator)
        integer = [[None if x is None else int(x * denominator) for x in row]
                   for row in p]
        unit = int(T * denominator)
        m, n = len(p), len(p[0])
        eligible = [[i for i in range(m) if integer[i][j] is not None]
                    for j in range(n)]
        masks = [frozenset(S) for k in range(1, len(outputs))
                 for S in combinations(outputs, k)]
        best = {mask: None for mask in masks}
        states = 0
        for sigma in product(*eligible):
            payload = [0] * m
            for j, v in enumerate(sigma):
                payload[v] += integer[v][j]
            baseline = max(max(payload), payload[a] + unit)
            for mask in masks:
                value = max(baseline, *(payload[v] + unit for v in mask))
                if best[mask] is None or value < best[mask]:
                    best[mask] = value
            states += 1
        count("test_only_exact_assignment_states", states)
        return {mask: Fraction(value, denominator) for mask, value in best.items()}

    def check_result(p, result):
        clean = _matrix(p)
        sigma = _assignment(clean, result["sigma"])
        task = _task_loads(clean, sigma)
        actual = [x + y for x, y in zip(task, result["preloads"])]
        assert actual == result["loads"] and task == result["task_loads"]
        assert max(actual) <= result["selected_bound"]
        K = result["candidate_outputs"]
        assert set(result["blocked"]) == {result["a"]} | (set(K) - {result["chosen"]})
        assert all(result["preloads"][v] == 0 for v in result["outputs"] if v not in K)
        assert len(result["absorption_order"]) <= len(p) - len(K)
        assert set(result["free_original_outputs"]) == set(result["outputs"]) - (set(K) - {result["chosen"]})

    examples = []
    for q in range(2, 10):
        p = [[Fraction(1, q)] * q] + [
            [Fraction(1) if j == i else None for j in range(q)] for i in range(q)]
        outputs = list(range(1, q + 1))
        result = construct_weighted_fanout(p, [0] * q, outputs, 1, 0, outputs)
        check_result(p, result)
        best = optimum_profiles(p, 1, 0, outputs)
        assert all(best[frozenset(set(outputs) - {v})] == 2 - Fraction(1, q)
                   for v in outputs)
        count("uniform_star_exact_single_profiles", q)
        if q <= 3:
            examples.append(result)
    for k in range(2, 8):
        for raw in ([1] * k, [0] + list(range(1, k)), [k] + [0] * (k - 1)):
            total = sum(raw)
            beta = [Fraction(v, total) for v in raw]
            # Add two original outputs outside the candidate K.
            outputs = list(range(1, k + 3));K = outputs[:k]
            p = [beta[:]] + [
                [Fraction(1) if j == i else None for j in range(k)]
                for i in range(k)] + [[None] * k, [None] * k]
            result = construct_weighted_fanout(p, [0] * k, K, 1, 0, outputs,
                                             beta=beta, missing_subset=K)
            check_result(p, result)
            best = optimum_profiles(p, 1, 0, K)
            profile = [best[frozenset(set(K) - {v})] for v in K]
            assert profile == [2 - v for v in beta]
            assert sum(profile) == 2 * k - 1
            count("weighted_star_exact_facet_profiles", k)
            count("weighted_star_vectors")

    # All ordered full binary trees through q=5, exact missing-one optima.
    def shapes(q):
        if q == 1:
            return (None,)
        return tuple((left, right) for k in range(1, q)
                     for left in shapes(k) for right in shapes(q - k))
    def tree_matrix(shape):
        children, leaves = {}, []
        next_vertex = 0
        def build(s):
            nonlocal next_vertex
            v = next_vertex
            next_vertex += 1
            if s is None:
                leaves.append(v)
            else:
                children[v] = (build(s[0]), build(s[1]))
            return v
        a = build(shape)
        edges = [(u, v) for u, dest in sorted(children.items()) for v in dest]
        p = [[None] * len(edges) for _ in range(next_vertex)]
        for j, (u, v) in enumerate(edges):
            p[u][j], p[v][j] = Fraction(1, 2), Fraction(1)
        return p, a, leaves, [u for u, v in edges], [v for u, v in edges]
    for q in range(2, 6):
        for shape in shapes(q):
            p, a, outputs, S1, S2 = tree_matrix(shape)
            best = optimum_profiles(p, 1, a, outputs)
            assert all(best[frozenset({v})] == Fraction(3, 2) for v in outputs)
            count("binary_tree_exact_missing_profiles", q)
            count("full_binary_tree_shapes")
            for u, v in combinations(outputs, 2):
                result = construct_weighted_fanout(
                    p, S1, S2, 1, a, outputs, missing_subset=[u, v])
                check_result(p, result)
                assert max(result["loads"]) == Fraction(3, 2)
                count("binary_tree_pair_actual_witnesses")

    def source_weights(dest, m, capacity=4):
        result = [0] * len(dest)
        for v in range(m):
            jobs = [j for j, x in enumerate(dest) if x == v]
            if len(jobs) > capacity:
                return None
            values = [1] * len(jobs)
            for unused in range(capacity - len(jobs)):
                if not jobs:
                    break
                position = rng.randrange(len(jobs) + 1)
                if position < len(jobs):
                    values[position] += 1
            for j, value in zip(jobs, values):
                result[j] = value
        return result
    for unused in range(260):
        q, I = rng.randrange(2, 6), rng.randrange(4)
        m, a = I + q + 1, I
        outputs = list(range(I + 1, m))
        n = rng.randrange(min(8, 4 * (I + 1)) + 1)
        S1 = [rng.randrange(I + 1) for j in range(n)]
        S2 = [rng.choice(list(range(I)) + outputs) for j in range(n)]
        w1, w2 = source_weights(S1, m), source_weights(S2, m)
        if w1 is None or w2 is None:
            continue
        p = [[None] * n for _ in range(m)]
        for j, (u, v, s, t) in enumerate(zip(S1, S2, w1, w2)):
            if u == v:
                p[u][j] = Fraction(min(s, t), 4)
            else:
                p[u][j], p[v][j] = Fraction(s, 4), Fraction(t, 4)
        if n:
            extra = next((v for v in range(m) if p[v][0] is None), None)
            if extra is not None:
                p[extra][0] = Fraction(rng.choice((0, 7)), 3)
        permutation = rng.sample(range(m), m)
        old = p
        p = [None] * m
        for v in range(m):
            p[permutation[v]] = old[v]
        S1, S2 = [permutation[v] for v in S1], [permutation[v] for v in S2]
        a, outputs = permutation[a], [permutation[v] for v in outputs]
        best = optimum_profiles(p, 1, a, outputs)
        for size in range(2, q + 1):
            for K in combinations(outputs, size):
                values = [best[frozenset(set(K) - {v})] for v in K]
                assert sum(values) <= 2 * size - 1
                count("random_exact_subset_profile_sum_checks")
                raw = [rng.randrange(5) for v in K]
                if not any(raw):
                    raw[0] = 1
                vectors = (None, [Fraction(v, sum(raw)) for v in raw],
                           [Fraction(1)] + [Fraction(0)] * (size - 1))
                for beta in vectors:
                    result = construct_weighted_fanout(
                        p, S1, S2, 1, a, outputs, beta=beta, missing_subset=K)
                    check_result(p, result)
                    optimum = best[frozenset(set(K) - {result["chosen"]})]
                    assert optimum <= max(result["loads"]) <= result["bound"]
                    count("random_weighted_actual_constructions")
        for u, v in combinations(outputs, 2):
            assert best[frozenset({u})] + best[frozenset({v})] <= 3
            count("random_exact_missing_pair_sum_checks")
        count("random_actual_instances")

    # Exact user-model boundaries, including extra finite edges and one-edge jobs.
    base = {
        "p": [["1/2", "1/2", 0], [1, None, None], [None, 1, None],
              ["11/3", None, "1/4"]],
        "S1": [0, 0, 3], "S2": [1, 2, 3], "T": 1, "a": 0,
        "outputs": [1, 2], "beta": ["1/2", "1/2"],
    }
    for T in (Fraction(1), Fraction(1, 10**120 + 151), Fraction(10**120 + 151, 37)):
        p = [[None if value is None else _rational(value) * T for value in row]
             for row in base["p"]]
        result = construct_weighted_fanout(p, base["S1"], base["S2"], T, 0, [1, 2])
        check_result(p, result)
        count("fixed_positive_internal_huge_rational_boundaries")
    for p, S1, S2, T, a, outputs in (
        ([[], [], [], [], []], [], [], 1, 4, [2, 0, 3]),
        ([[0], [0], [7], [None]], [0], [1], 0, 0, [1, 2]),
        ([[0], [0], [7], [None]], [0], [1], 1, 0, [1, 2]),
    ):
        result = construct_weighted_fanout(p, S1, S2, T, a, outputs)
        check_result(p, result)
        count("zero_deadline_zero_time_empty_boundaries")
    mapping = construct_weighted_fanout(
        [[Fraction(1, 2)] * 2, [1, None], [None, 1]], [0, 0], [1, 2],
        1, 0, [1, 2], beta={1: "1/3", 2: "2/3"}, missing_subset={1, 2})
    assert mapping["beta"] == [Fraction(1, 3), Fraction(2, 3)]
    count("dictionary_beta_set_subset_boundary")
    json_result = solve_json_instance({**base, "beta": {"1": "1/3", "2": "2/3"}})
    check_result(base["p"], json_result)
    count("json_concrete_instance")

    valid = {"p": [[Fraction(1, 2)] * 2, [1, None], [None, 1]],
             "S1": [0, 0], "S2": [1, 2], "T": 1, "a": 0, "outputs": [1, 2]}
    invalid = (
        {"T": -1}, {"T": 1.0}, {"T": True}, {"p": []},
        {"p": [[1], []]}, {"p": [[None], [None], [None]]},
        {"p": [[0.5, 0.5], [1, None], [None, 1]]},
        {"S1": [0]}, {"S1": [True, 0]}, {"S2": [2, 2]},
        {"S1": [1, 2]}, {"outputs": [1]}, {"outputs": [1, 1]},
        {"outputs": [0, 1]}, {"a": 3}, {"missing_subset": [1]},
        {"missing_subset": [1, 3]}, {"missing_subset": [1, 1]},
        {"missing_subset": [[1], [2]]},
        {"beta": [1]}, {"beta": [1, 1]}, {"beta": [-1, 2]},
        {"beta": [0.5, 0.5]}, {"beta": {1: 1}},
    )
    for changes in invalid:
        try:
            construct_weighted_fanout(**{**valid, **changes})
        except ValueError:
            count("invalid_inputs_rejected")
        else:
            raise AssertionError("accepted invalid test: " + repr(changes))
    return {
        "status": "passed", "source_claims": list(SOURCE_CLAIMS),
        "scope": "actual schedules only; no general SC extension audited",
        "python": platform.python_version(), "seed": 110709,
        "precision": "Fraction exact; test optima use denominator-cleared integers",
        "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "counts": counts, "examples": examples,
        "runtime_seconds": round(time.perf_counter() - started, 3),
        "limits": "Finite audit is not the universal proof. Constructors use supplied YES witnesses and never compute mu or call the test-only oracle. No general UM hardness result.",
    }


def _jsonable(value):
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def main():
    import argparse
    import json
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", help="exact concrete JSON instance")
    parser.add_argument("--output", help="new output file; existing files are never overwritten")
    args = parser.parse_args()
    if args.input:
        with Path(args.input).open() as handle:
            result = solve_json_instance(json.load(handle))
        payload = {"source_claims": list(SOURCE_CLAIMS), "result": result}
    else:
        payload = audit()
    serialized = json.dumps(_jsonable(payload), ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.output:
        with Path(args.output).open("x") as handle:
            handle.write(serialized)
    else:
        print(serialized, end="")


if __name__ == "__main__":
    main()
