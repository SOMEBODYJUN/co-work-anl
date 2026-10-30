#!/usr/bin/env python3
"""Independent exact audit of the anchored, equal-class-weight front compiler.

This script imports no repository research code.  It constructs genuine fresh
congestion resources and each player's two resource-set actions, then recomputes
every load after each tested deviation.  Base-game quantities enter only through
their stated bounds: selected front edges have base margin >= eta, and every
base cost lies in [0, B].  Consequently the edge assertions are universal margin
checks, not a construction of a base game satisfying the front-cover premise.
All arithmetic, including the choice of degree, is rational/integer arithmetic.
"""

from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from math import comb
import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys


@dataclass(frozen=True)
class Resource:
    group: int
    triple: tuple
    pattern: tuple
    coefficient: F
    degree: int


def is_front(bits):
    return sum(x != y for x, y in zip(bits, bits[1:])) <= 1


def class_indices(sizes):
    out, start = [], 0
    for n in sizes:
        out.append(tuple(range(start, start + n)))
        start += n
    return tuple(out)


def is_product_front(state, groups):
    return all(is_front(tuple(state[i] for i in g)) for g in groups)


def degree_and_amplitude(sizes, alpha, B, eta, refined=False):
    assert alpha >= 1 and B > 0 and 0 < eta <= B
    L = max((comb(n - 1, 2) if n >= 3 else 0 for n in sizes), default=0)
    if L == 0:
        return L, 0, F(0)
    amplitude = 2 * alpha * B
    # Select the least positive integer satisfying the exact inequality.  This
    # equals the ceiling of the logarithmic formula, without floating error.
    if refined:
        target = F(1) / (4 * alpha * L)
        if alpha > 1:
            target = min(target, eta / (4 * alpha * (alpha - 1) * B * L))
    else:
        target = eta / (4 * alpha * alpha * B * L)
    degree, attenuation = 1, F(2, 3)
    while attenuation > target:
        degree += 1
        attenuation *= F(2, 3)
    assert attenuation <= target
    if degree > 1:
        assert F(2, 3) ** (degree - 1) > target
    return L, degree, amplitude


def build_clock(sizes, class_weights, alpha, B, eta, refined=False):
    groups = class_indices(sizes)
    weights = tuple(w for n, w in zip(sizes, class_weights) for _ in range(n))
    L, degree, amplitude = degree_and_amplitude(sizes, alpha, B, eta, refined)
    resources = []
    actions = [[set(), set()] for _ in weights]
    for a, g in enumerate(groups):
        if len(g) < 3:
            continue
        for j in range(1, len(g)):
            for k in range(j + 1, len(g)):
                triple = (g[0], g[j], g[k])
                for pattern in ((0, 1, 0), (1, 0, 1)):
                    r = len(resources)
                    coefficient = amplitude / (3 * class_weights[a]) ** degree
                    resources.append(Resource(a, triple, pattern, coefficient, degree))
                    for i, bit in zip(triple, pattern):
                        actions[i][bit].add(r)
    for i in range(len(weights)):
        assert len(actions[i][0]) == len(actions[i][1]) <= L
        assert actions[i][0].isdisjoint(actions[i][1])
    return groups, weights, tuple(resources), actions, L, degree, amplitude


def true_costs(state, weights, resources, actions):
    loads = [F(0) for _ in resources]
    for i, bit in enumerate(state):
        for r in actions[i][bit]:
            loads[r] += weights[i]
    values = [r.coefficient * x ** r.degree for r, x in zip(resources, loads)]
    costs = tuple(sum((values[r] for r in actions[i][bit]), F(0))
                  for i, bit in enumerate(state))
    return costs, tuple(loads)


def first_opposite_repair(state, g):
    """Return the first opposite-to-anchor player in this nonfront class."""
    assert not is_front(tuple(state[i] for i in g))
    anchor = state[g[0]]
    position = next(j for j in range(1, len(g)) if state[g[j]] != anchor)
    assert any(state[g[k]] == anchor for k in range(position + 1, len(g)))
    return g[position]


def run_case(name, sizes, class_weights, alpha, B, eta, refined=False):
    groups, weights, resources, actions, L, D, amplitude = build_clock(
        sizes, class_weights, alpha, B, eta, refined)
    n = sum(sizes)
    states = tuple(product((0, 1), repeat=n))
    cache = {s: true_costs(s, weights, resources, actions) for s in states}
    front_states = front_edges = illegal_repairs = 0
    min_front_margin = min_repair_margin = None
    for s in states:
        costs, loads = cache[s]
        front = is_product_front(s, groups)
        full_resources = []
        for r, (res, load) in enumerate(zip(resources, loads)):
            w = class_weights[res.group]
            assert load in (F(0), w, 2 * w, 3 * w)
            full = load == 3 * w
            assert full == all(s[i] == b for i, b in zip(res.triple, res.pattern))
            if full:
                full_resources.append(r)
        assert front == (len(full_resources) == 0)
        if front:
            front_states += 1
            for i in range(n):
                t = list(s)
                t[i] ^= 1
                t = tuple(t)
                if not is_product_front(t, groups):
                    continue
                # Each incident pair has mover load counts n -> 4-n.  Both
                # endpoints nonfull force n=2, including anchor flips.
                for before_r in actions[i][s[i]]:
                    w = class_weights[resources[before_r].group]
                    after_r = before_r ^ 1
                    assert after_r in actions[i][t[i]]
                    assert loads[before_r] == 2 * w
                    assert cache[t][1][after_r] == 2 * w
                assert costs[i] == cache[t][0][i]
                assert costs[i] == len(actions[i][s[i]]) * amplitude * F(2, 3) ** D
                # This is valid for EVERY front-preserving edge; in particular
                # it is valid for whichever edge has base margin >= eta.
                margin = eta + costs[i] - alpha * cache[t][0][i]
                assert margin >= eta / 2
                min_front_margin = margin if min_front_margin is None else min(min_front_margin, margin)
                front_edges += 1
            continue
        for g in groups:
            if is_front(tuple(s[i] for i in g)):
                continue
            i = first_opposite_repair(s, g)
            t = list(s)
            t[i] ^= 1
            t = tuple(t)
            after_costs, after_loads = cache[t]
            vanished_full = 0
            for before_r in actions[i][s[i]]:
                res = resources[before_r]
                w = class_weights[res.group]
                # Complementary pairs are adjacent, so ^1 finds its mate.
                after_r = before_r ^ 1
                assert after_r in actions[i][t[i]]
                before_count = loads[before_r] / w
                after_count = after_loads[after_r] / w
                assert (before_count, after_count) in ((3, 1), (2, 2))
                vanished_full += before_count == 3
            assert vanished_full >= 1
            # Worst possible base margin is -alpha B.  No synthetic base costs
            # are mistaken for a realizable congestion game here.
            margin = costs[i] - alpha * after_costs[i] - alpha * B
            assert margin >= eta / 2
            min_repair_margin = margin if min_repair_margin is None else min(min_repair_margin, margin)
            illegal_repairs += 1
    return {
        "name": name, "degree_mode": "refined" if refined else "uniform",
        "sizes": sizes, "class_weights": list(map(str, class_weights)),
        "alpha": str(alpha), "B": str(B), "eta": str(eta), "L": L,
        "D": D, "amplitude": str(amplitude), "resources": len(resources),
        "states": len(states), "front_states": front_states,
        "front_preserving_edges_checked": front_edges,
        "illegal_class_repairs_checked": illegal_repairs,
        "minimum_conditional_front_margin": str(min_front_margin),
        "minimum_worst_case_repair_margin": str(min_repair_margin),
    }


def check_degenerate_base_boundaries():
    # Zero base: every actual margin is zero, so eta>0 / front-cover fails.
    groups = class_indices((1, 2, 3))
    weights = (F(1),) * 6
    states = tuple(product((0, 1), repeat=6))
    front = tuple(s for s in states if is_product_front(s, groups))
    assert front
    zero_resource = (Resource(-1, (), (), F(0), 0),)
    zero_actions = [[set(), set()] for _ in weights]
    zero_costs = {s: true_costs(s, weights, zero_resource, zero_actions)[0]
                  for s in states}
    zero_has_front_cover = all(any(
        zero_costs[s][i] > zero_costs[tuple(b ^ (j == i) for j, b in enumerate(s))][i]
        for i in range(6)) for s in front)
    assert not zero_has_front_cover
    # Genuine constant-cost resources, one private resource per player/action.
    # State-independent costs give an exact potential on the finite front graph:
    # a minimum of sum(cost_i) cannot have a front-preserving strict alpha edge.
    tables = (
        tuple((F(0), F(0)) for _ in range(6)),
        tuple((F(i % 3), F((i + 1) % 3)) for i in range(6)),
        tuple((F(7, i + 1), F(i, 7)) for i in range(6)),
    )
    count = 0
    for alpha in (F(1), F(3, 2), F(7, 3)):
        for table in tables:
            resources, actions = [], [[set(), set()] for _ in weights]
            for i, row in enumerate(table):
                for bit, constant in enumerate(row):
                    actions[i][bit].add(len(resources))
                    resources.append(Resource(-1, (), (), constant, 0))
            costs = {s: true_costs(s, weights, resources, actions)[0] for s in states}
            for s in states:
                assert costs[s] == tuple(table[i][b] for i, b in enumerate(s))
            witness = min(front, key=lambda s: sum(costs[s]))
            for i in range(6):
                t = list(witness)
                t[i] ^= 1
                t = tuple(t)
                if is_product_front(t, groups):
                    assert costs[witness][i] <= alpha * costs[t][i]
            count += 1
    return {"zero_base_front_cover": False,
            "constant_private_resource_front_potential_cases": count,
            "conclusion": "These bases cannot satisfy the strict front-cover premise; no compiler claim is inferred for B=0."}


def build_literal_fixture(data):
    """Rebuild section-1 literal windows directly from the JSON input."""
    m, N, p = data["class_count"], data["class_size"], data["degree"]
    assert m >= 2 and N >= 1 and p >= 0
    class_weights = tuple(map(F, data["class_weights"]))
    assert len(class_weights) == m and all(w > 0 for w in class_weights)
    weights = tuple(w for w in class_weights for _ in range(N))
    resources, actions = [], [[set(), set()] for _ in weights]
    for term in data["terms"]:
        a, b, K, orientation = term["test"]
        assert a != b and 0 <= a < m and 0 <= b < m
        assert 1 <= K <= N and orientation in (-1, 1)
        coefficient = F(term["actual_coefficient"])
        theta = F(term["theta"])
        assert coefficient == theta / (class_weights[a] + K * class_weights[b]) ** p
        for j in range(N):
            h = a * N + j
            users, phases = [h], [0]
            for k in range(K):
                v = (j + int(a > b) + k) % N
                u = b * N + v
                phase = int(v * m + b > j * m + a) ^ int(orientation == -1)
                users.append(u)
                phases.append(phase)
            assert len(set(users)) == K + 1
            for side in (0, 1):
                r = len(resources)
                pattern = tuple(phase ^ side for phase in phases)
                resources.append(Resource(-1, tuple(users), pattern, coefficient, p))
                for u, bit in zip(users, pattern):
                    actions[u][bit].add(r)
    assert all(actions[i][0] and actions[i][1] for i in range(len(weights)))
    assert all(actions[i][0].isdisjoint(actions[i][1]) for i in range(len(weights)))
    return (N,) * m, class_weights, weights, tuple(resources), actions


def add_fresh_clock(base_resources, base_actions, clock_resources, clock_actions):
    offset = len(base_resources)
    resources = base_resources + clock_resources
    actions = [[base_actions[i][b] | {offset + r for r in clock_actions[i][b]}
                for b in (0, 1)] for i in range(len(base_actions))]
    return resources, actions


def verify_fixture(input_path):
    input_path = input_path.resolve()
    data = json.loads(input_path.read_text())
    sizes, class_weights, weights, resources, actions = build_literal_fixture(data)
    alpha = F(data["alpha"])
    assert alpha >= 1
    groups = class_indices(sizes)
    n = len(weights)
    states = tuple(product((0, 1), repeat=n))
    costs = {s: true_costs(s, weights, resources, actions)[0] for s in states}
    B = max(c for row in costs.values() for c in row)
    selected, eta = {}, None
    front_count = base_pne_count = 0
    for s in states:
        all_margins, front_margins = [], []
        for i in range(n):
            t = tuple(bit ^ (j == i) for j, bit in enumerate(s))
            margin = costs[s][i] - alpha * costs[t][i]
            all_margins.append(margin)
            if is_product_front(s, groups) and is_product_front(t, groups):
                front_margins.append((margin, i))
        base_pne_count += max(all_margins) <= 0
        if is_product_front(s, groups):
            front_count += 1
            margin, i = max(front_margins)
            assert margin > 0
            selected[s] = i
            eta = margin if eta is None else min(eta, margin)
    assert 0 < eta <= B
    # These are the independently recomputed values quoted in the frozen text.
    assert B == F(16553910168, 815730721)
    assert eta == F(1410469765084842635603, 1070401852096200000000)
    assert front_count == 216 and len(states) == 512 and len(resources) == 36
    modes = []
    for refined in (False, True):
        _, cw, clock_res, clock_actions, L, D, amplitude = build_clock(
            sizes, class_weights, alpha, B, eta, refined)
        assert cw == weights
        combined_res, combined_actions = add_fresh_clock(resources, actions, clock_res, clock_actions)
        combined_costs = {s: true_costs(s, weights, combined_res, combined_actions)[0]
                          for s in states}
        all_min_best = min_front = min_repair = None
        deviation_count = selected_count = repair_count = pne_count = 0
        for s in states:
            margins = []
            for i in range(n):
                t = tuple(bit ^ (j == i) for j, bit in enumerate(s))
                margins.append(combined_costs[s][i] - alpha * combined_costs[t][i])
                deviation_count += 1
            best = max(margins)
            assert best > 0
            pne_count += best <= 0
            all_min_best = best if all_min_best is None else min(all_min_best, best)
            if s in selected:
                margin = margins[selected[s]]
                assert margin >= eta / 2
                min_front = margin if min_front is None else min(min_front, margin)
                selected_count += 1
            else:
                for g in groups:
                    if not is_front(tuple(s[i] for i in g)):
                        margin = margins[first_opposite_repair(s, g)]
                        assert margin >= eta / 2
                        min_repair = margin if min_repair is None else min(min_repair, margin)
                        repair_count += 1
        assert D == (4 if refined else 11)
        assert len(clock_res) == 6 and pne_count == 0
        modes.append({
            "mode": "refined" if refined else "uniform", "D": D,
            "output_degree": max(data["degree"], D), "L": L,
            "amplitude": str(amplitude), "attenuation": str(F(2, 3) ** D),
            "clock_resources": len(clock_res), "total_resources": len(combined_res),
            "all_states": len(states), "all_real_deviations_checked": deviation_count,
            "selected_front_edges_checked": selected_count,
            "illegal_class_repairs_checked": repair_count, "alpha_PNE_count": pne_count,
            "min_all_state_best_margin": str(all_min_best),
            "min_selected_front_margin": str(min_front),
            "min_illegal_class_repair_margin": str(min_repair),
        })
    return {"input": str(input_path),
            "input_sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
            "base_resources": len(resources), "base_degree": data["degree"],
            "B": str(B), "eta": str(eta), "product_front_states": front_count,
            "base_alpha_PNE_count": base_pne_count, "modes": modes}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="Explicit literal-window rational fixture JSON.")
    parser.add_argument("--output", type=Path, help="New JSON path; existing files are never overwritten.")
    args = parser.parse_args()
    cases = [
        ("singleton_no_clock", (1,), (F(1),), F(1), F(1), F(1)),
        ("size_two_no_clock", (2, 1), (F(1, 10**24), F(10**24)), F(3, 2), F(2), F(2, 7)),
        ("minimal_illegal_alpha_one", (3,), (F(1),), F(1), F(1), F(1)),
        ("three_classes_extreme_weights", (1, 2, 3), (F(1, 10**24), F(10**24), F(7, 11)), F(3, 2), F(13, 7), F(13, 259)),
        ("two_illegal_classes_extreme_weights", (3, 4), (F(10**40), F(1, 10**40)), F(7, 3), F(5, 13), F(5, 1261)),
        ("longer_class_alpha_one", (5,), (F(7, 11),), F(1), F(2), F(1, 100)),
        ("mixed_small_classes", (2, 3, 3), (F(2), F(10**15), F(1, 10**15)), F(5, 4), F(11, 5), F(1, 31)),
        ("large_alpha", (3, 3), (F(1, 3), F(17)), F(10), F(2, 3), F(1, 1000)),
    ]
    result = {"status": "passed", "scope": __doc__,
              "python": platform.python_version(), "command": [sys.executable, *sys.argv],
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "cases": [run_case(*case, refined=mode) for mode in (False, True) for case in cases],
              "base_boundary_checks": check_degenerate_base_boundaries()}
    if args.input is not None:
        result["fixture"] = verify_fixture(args.input)
    serialized = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output is None:
        print(serialized, end="")
    else:
        with args.output.open("x") as out:
            out.write(serialized)
        print(json.dumps({"status": result["status"], "output": str(args.output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
