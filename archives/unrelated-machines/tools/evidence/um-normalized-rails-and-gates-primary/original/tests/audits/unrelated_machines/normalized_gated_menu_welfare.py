"""Exact finite audits only; scipy proposes LP certificates, Fraction checks them.

No production LP solver or general-purpose UM solver is claimed. This file reads
no shared repository state and writes only its explicitly requested JSON output.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
from fractions import Fraction as F
from pathlib import Path


ZERO = F(0)
ONE = F(1)


def norm(weights):
    total = sum(weights, ZERO)
    assert total > 0
    return [F(w, total) for w in weights]


def check_menu(menu):
    assert menu and menu[0] and menu[0][0]
    m = len(menu[0][0])
    for states in menu:
        assert states
        for state in states:
            assert len(state) == m and min(state) >= 0
            assert sum(state, ZERO) == 1


def check_lp(menu, z, x, support=False):
    n, m = len(menu), len(menu[0][0])
    for g, states in enumerate(menu):
        assert len(z[g]) == len(states) == len(x[g])
        assert min(z[g]) >= 0 and sum(z[g], ZERO) == 1
        for s, state in enumerate(states):
            for u, p in enumerate(state):
                assert 0 <= x[g][s][u] <= z[g][s]
                if not p:
                    assert x[g][s][u] == 0
                if support and p:
                    assert x[g][s][u] == z[g][s]
    for u in range(m):
        assert sum((x[g][s][u] for g in range(n)
                    for s in range(len(menu[g]))), ZERO) <= 1


def objective(menu, x):
    return sum((p * x[g][s][u] for g, states in enumerate(menu)
                for s, state in enumerate(states)
                for u, p in enumerate(state)), ZERO)


def welfare_lp_certificate(menu):
    """Float proposal accepted only after exact primal/dual optimality checks."""
    from scipy.optimize import linprog

    n, m = len(menu), len(menu[0][0])
    variables = []
    for g, states in enumerate(menu):
        for s in range(len(states)):
            variables.append(("z", g, s, -1))
    for g, states in enumerate(menu):
        for s, state in enumerate(states):
            for u, p in enumerate(state):
                if p:
                    variables.append(("x", g, s, u))
    idx = {key: k for k, key in enumerate(variables)}
    d = len(variables)
    c = [ZERO] * d
    eq, eq_rhs, ub, ub_rhs = [], [], [], []
    for g, states in enumerate(menu):
        row = [ZERO] * d
        for s in range(len(states)):
            row[idx[("z", g, s, -1)]] = ONE
        eq.append(row)
        eq_rhs.append(ONE)
    for key, k in idx.items():
        kind, g, s, u = key
        if kind == "x":
            c[k] = -menu[g][s][u]
            row = [ZERO] * d
            row[k] = ONE
            row[idx[("z", g, s, -1)]] = -ONE
            ub.append(row)
            ub_rhs.append(ZERO)
    for u in range(m):
        row = [ZERO] * d
        for key, k in idx.items():
            if key[0] == "x" and key[3] == u:
                row[k] = ONE
        ub.append(row)
        ub_rhs.append(ONE)
    result = linprog([float(v) for v in c],
                     A_ub=[[float(v) for v in r] for r in ub],
                     b_ub=[float(v) for v in ub_rhs],
                     A_eq=[[float(v) for v in r] for r in eq],
                     b_eq=[float(v) for v in eq_rhs], method="highs")
    assert result.success, result.message
    rationalize = lambda a: [F(float(v)).limit_denominator(10**8) for v in a]
    primal = rationalize(result.x)
    dual_ub = rationalize(result.ineqlin.marginals)
    dual_eq = rationalize(result.eqlin.marginals)
    dot = lambda a, b: sum((aa * bb for aa, bb in zip(a, b)), ZERO)
    assert min(primal) >= 0
    assert all(dot(r, primal) <= rhs for r, rhs in zip(ub, ub_rhs))
    assert all(dot(r, primal) == rhs for r, rhs in zip(eq, eq_rhs))
    assert max(dual_ub) <= 0
    for k in range(d):
        reduced = c[k] - sum((r[k] * y for r, y in zip(ub, dual_ub)), ZERO)
        reduced -= sum((r[k] * y for r, y in zip(eq, dual_eq)), ZERO)
        assert reduced >= 0
    dual_value = dot(ub_rhs, dual_ub) + dot(eq_rhs, dual_eq)
    assert dot(c, primal) == dual_value
    z = [[ZERO] * len(states) for states in menu]
    x = [[[ZERO] * m for state in states] for states in menu]
    for key, k in idx.items():
        kind, g, s, u = key
        if kind == "z":
            z[g][s] = primal[k]
        else:
            x[g][s][u] = primal[k]
    check_lp(menu, z, x)
    assert objective(menu, x) == -dual_value
    return z, x, {"variables": d, "ub_rows": len(ub), "eq_rows": n,
                  "objective": -dual_value,
                  "exact_primal": primal, "exact_dual_ub": dual_ub,
                  "exact_dual_eq": dual_eq,
                  "positive_z": sum(v > 0 for row in z for v in row),
                  "fractional_z": sum(0 < v < 1 for row in z for v in row),
                  "fractional_incidence_coins": sum(
                      0 < x[g][s][u] < z[g][s]
                      for g, states in enumerate(menu)
                      for s, state in enumerate(states)
                      for u, p in enumerate(state) if p)}


def distribution(menu, z, x, fixed_states, fixed_bits, g, u):
    result = {}
    if fixed_states[g] is None:
        for s, state in enumerate(menu[g]):
            p, mass = state[u], x[g][s][u]
            if p and mass:
                result[p] = result.get(p, ZERO) + mass
    else:
        s = fixed_states[g]
        p = menu[g][s][u]
        if p:
            bit = fixed_bits.get((g, u))
            mass = x[g][s][u] / z[g][s] if bit is None else F(bit)
            if mass:
                result[p] = mass
    assert sum(result.values(), ZERO) <= 1
    return result


def expected_max_sum(menu, z, x, fixed_states, fixed_bits):
    n, m = len(menu), len(menu[0][0])
    total = ZERO
    for u in range(m):
        distributions = [distribution(menu, z, x, fixed_states, fixed_bits, g, u)
                         for g in range(n)]
        levels = sorted({p for dist in distributions for p in dist})
        previous = ZERO
        for p in levels:
            no_claim = ONE
            for dist in distributions:
                no_claim *= 1 - sum((q for v, q in dist.items() if v >= p), ZERO)
            total += (p - previous) * (1 - no_claim)
            previous = p
    return total


def brute_expected_max_support(menu, z):
    n, m = len(menu), len(menu[0][0])
    total = ZERO
    for states in itertools.product(*(range(len(row)) for row in menu)):
        prob = ONE
        for g, s in enumerate(states):
            prob *= z[g][s]
        value = sum((max(menu[g][states[g]][u] for g in range(n))
                     for u in range(m)), ZERO)
        total += prob * value
    return total


def round_welfare(menu, z, x, support=False):
    check_lp(menu, z, x, support)
    n, m = len(menu), len(menu[0][0])
    states = [None] * n
    bits = {}
    initial = expected_max_sum(menu, z, x, states, bits)
    if support:
        assert initial == brute_expected_max_support(menu, z)
    steps = []
    current = initial
    for g in range(n):
        candidates = []
        for s, prob in enumerate(z[g]):
            if prob:
                states[g] = s
                value = expected_max_sum(menu, z, x, states, bits)
                candidates.append((value, s, prob))
        assert sum((v * p for v, s, p in candidates), ZERO) == current
        value, state, prob = max(candidates, key=lambda item: (item[0], -item[1]))
        states[g] = state
        assert value >= current
        steps.append(("state", value - current))
        current = value
    for g, s in enumerate(states):
        for u, p in enumerate(menu[g][s]):
            if not p:
                continue
            coin = x[g][s][u] / z[g][s]
            if not coin or coin == 1:
                bits[g, u] = int(coin)
                assert expected_max_sum(menu, z, x, states, bits) == current
                continue
            values = []
            for bit in (0, 1):
                bits[g, u] = bit
                values.append(expected_max_sum(menu, z, x, states, bits))
            assert (1 - coin) * values[0] + coin * values[1] == current
            bit = 0 if values[0] >= values[1] else 1
            bits[g, u] = bit
            assert values[bit] >= current
            steps.append(("coin", values[bit] - current))
            current = values[bit]
    bundles = [set() for g in range(n)]
    for u in range(m):
        offers = [(menu[g][s][u], -g, g)
                  for g, s in enumerate(states) if bits.get((g, u))]
        if offers:
            p, _, g = max(offers)
            assert p > 0
            bundles[g].add(u)
    direct = sum((sum((menu[g][states[g]][u] for u in bundles[g]), ZERO)
                  for g in range(n)), ZERO)
    assert direct == current
    values, attaining = actual_values(menu, bundles)
    welfare = sum(values, ZERO)
    lp_value = objective(menu, x)
    assert welfare >= direct >= initial
    if lp_value:
        assert initial > F(5, 8) * lp_value
    return {"bundles": bundles, "values": values, "states": attaining,
            "welfare": welfare, "initial_expectation": initial,
            "lp_welfare": lp_value, "state_steps": n,
            "nontrivial_coin_steps": sum(tag == "coin" for tag, gain in steps),
            "positive_gain_steps": sum(gain > 0 for tag, gain in steps)}


def actual_values(menu, bundles):
    values, states = [], []
    for g, alternatives in enumerate(menu):
        val = [(sum((state[u] for u in bundles[g]), ZERO), -s, s)
               for s, state in enumerate(alternatives)]
        value, _, state = max(val)
        values.append(value)
        states.append(state)
    return values, states


def balanced(values):
    n = len(values)
    order = sorted(range(n), key=lambda g: (-values[g], g))
    candidates = [(min(F(k, n), values[order[k - 1]]), -k, k)
                  for k in range(1, n + 1)]
    beta, _, k = max(candidates)
    return beta, order[:k] if beta else []


def exhaustive_values(menu):
    n, m = len(menu), len(menu[0][0])
    best_welfare, best_beta = ZERO, ZERO
    count = 0
    for recipients in itertools.product(range(n + 1), repeat=m):
        bundles = [set() for g in range(n)]
        for u, g in enumerate(recipients):
            if g < n:
                bundles[g].add(u)
        values, states = actual_values(menu, bundles)
        best_welfare = max(best_welfare, sum(values, ZERO))
        best_beta = max(best_beta, balanced(values)[0])
        count += 1
    assert best_welfare >= n * best_beta**2
    return best_welfare, best_beta, count


def build_gate(menu):
    n, m = len(menu), len(menu[0][0])
    machines = [("R",)]
    machines += [("X", g) for g in range(n)]
    machines += [("M", g, s) for g, row in enumerate(menu) for s in range(len(row))]
    machines += [("Q", u) for u in range(m)]
    jobs = {("pin",): {("R",): ONE}}
    for g, states in enumerate(menu):
        jobs["connector", g] = {("R",): F(1, n), ("X", g): ONE}
        jobs["selector", g] = {("X", g): ONE}
        for s, state in enumerate(states):
            jobs["selector", g]["M", g, s] = ONE
            for u, p in enumerate(state):
                # The audit deliberately includes every explicit zero job.
                jobs["incidence", g, s, u] = {("M", g, s): p, ("Q", u): ONE}
    S = sum(len(row) for row in menu)
    I = S * m
    assert len(machines) == 1 + n + S + m
    assert len(jobs) == 1 + 2 * n + I
    assert sum(map(len, jobs.values())) == 1 + 3 * n + S + 2 * I
    return machines, jobs


def gate_schedule(menu, result, chosen=None):
    n = len(menu)
    machines, jobs = build_gate(menu)
    beta, H = balanced(result["values"]) if chosen is None else chosen
    H = set(H)
    assignment = {("pin",): ("R",)}
    for g, states in enumerate(menu):
        active = g in H
        selected = result["states"][g]
        assignment["connector", g] = ("X", g) if active else ("R",)
        assignment["selector", g] = ("M", g, selected) if active else ("X", g)
        for s, state in enumerate(states):
            for u, p in enumerate(state):
                out = active and s == selected and p and u in result["bundles"][g]
                assignment["incidence", g, s, u] = ("Q", u) if out else ("M", g, s)
    assert set(assignment) == set(jobs)
    loads = {machine: ZERO for machine in machines}
    for job, machine in assignment.items():
        assert machine in jobs[job]
        loads[machine] += jobs[job][machine]
    peak = max(loads.values())
    assert peak <= 2 - beta
    if peak < 2:
        decoded = [g for g in range(n) if assignment["connector", g] == ("X", g)]
        assert F(len(decoded), n) >= 2 - peak
        used = set()
        for g in decoded:
            _, gg, ss = assignment["selector", g]
            assert gg == g
            bundle = {u for u, p in enumerate(menu[g][ss])
                      if assignment["incidence", g, ss, u] == ("Q", u)}
            assert not used.intersection(bundle)
            used.update(bundle)
            assert sum((menu[g][ss][u] for u in bundle), ZERO) >= 2 - peak
    return peak, {"machines": len(machines), "jobs": len(jobs),
                  "finite_edges": sum(map(len, jobs.values())),
                  "zero_incidence_jobs": sum(not p for row in menu for state in row for p in state),
                  "beta_hat": beta, "active_groups": len(H)}


def brute_gate_opt(menu):
    machines, jobs = build_gate(menu)
    entries = list(jobs.items())
    # Compare every legal completion except pruning once its partial peak is
    # already no smaller than an actually feasible incumbent.
    loads = {machine: ZERO for machine in machines}
    best = F(2)
    leaves, nodes = 0, 0

    def search(k):
        nonlocal best, leaves, nodes
        nodes += 1
        if k == len(entries):
            leaves += 1
            best = min(best, max(loads.values()))
            return
        job, options = entries[k]
        for machine, p in options.items():
            loads[machine] += p
            if max(loads.values()) < best:
                search(k + 1)
            loads[machine] -= p
    search(0)
    return best, nodes, leaves


def feasible_support_example(rng, n, m, K):
    assert m >= n
    mixture = norm([rng.randint(1, 7) for _ in range(K)])
    menu = [[] for _ in range(n)]
    for _ in range(K):
        resources = list(range(m))
        rng.shuffle(resources)
        parts = [[resources[g]] for g in range(n)]
        for u in resources[n:]:
            parts[rng.randrange(n)].append(u)
        for g in range(n):
            weights = norm([rng.randint(1, 11) for u in parts[g]])
            state = [ZERO] * m
            for u, p in zip(parts[g], weights):
                state[u] = p
            menu[g].append(state)
    z = [list(mixture) for g in range(n)]
    x = [[[z[g][s] if p else ZERO for p in state]
          for s, state in enumerate(row)] for g, row in enumerate(menu)]
    return menu, z, x


def random_menu(rng, n, m, K):
    menu = []
    for g in range(n):
        states = []
        for s in range(K):
            weights = [rng.choice([0, 0, 1, 2, 3, 5, 8]) for u in range(m)]
            if not any(weights):
                weights[rng.randrange(m)] = 1
            states.append(norm(weights))
        menu.append(states)
    return menu


def encode(obj):
    if isinstance(obj, F):
        return f"{obj.numerator}/{obj.denominator}"
    if isinstance(obj, set):
        return sorted(obj)
    if isinstance(obj, dict):
        return {str(k): encode(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [encode(v) for v in obj]
    return obj


def main(output):
    rng = random.Random(20261018)
    report = {"seed": 20261018, "scope": "finite exact arithmetic only",
              "production_lp_solver": False, "source_hardness": False,
              "support_cases": [], "general_cases": [], "coin_cases": [],
              "brute_um_cases": []}
    for k in range(36):
        n = 1 + k % 4
        m = n + k % 3
        K = 1 + k % 3
        menu, z, x = feasible_support_example(rng, n, m, K)
        check_menu(menu)
        result = round_welfare(menu, z, x, support=True)
        assert result["welfare"] > F(5, 8) * n
        high = [g for g, value in enumerate(result["values"]) if value >= F(3, 8)]
        high_strict = [g for g, value in enumerate(result["values"]) if value > F(3, 8)]
        assert F(len(high), n) > F(2, 5)
        assert F(len(high_strict), n) > F(2, 5)
        peak, counts = gate_schedule(menu, result, (F(3, 8), high))
        assert peak <= F(13, 8)
        report["support_cases"].append({"n": n, "m": m, "K": K,
                                        "menu": menu, "lambda": z,
                                        "welfare": result["welfare"],
                                        "initial_expectation": result["initial_expectation"],
                                        "peak": peak, **counts})
    for k in range(72):
        n = 1 + k % 3
        m = 1 + (k // 3) % 5
        K = 1 + (k // 15) % 3
        menu = random_menu(rng, n, m, K)
        check_menu(menu)
        z, x, certificate = welfare_lp_certificate(menu)
        result = round_welfare(menu, z, x)
        wstar, bstar, allocations = exhaustive_values(menu)
        assert certificate["objective"] >= wstar >= n * bstar**2
        bhat, H = balanced(result["values"])
        w = result["welfare"] / n
        assert w <= 2 * bhat - bhat**2
        peak, counts = gate_schedule(menu, result)
        assert peak <= F(13, 8) * (2 - bstar)
        report["general_cases"].append({"n": n, "m": m, "K": K,
                                        "menu": menu, "z": z, "x": x,
                                        "lp_certificate": certificate,
                                        "welfare_opt": wstar, "beta_opt": bstar,
                                        "allocations_enumerated": allocations,
                                        "output_welfare": result["welfare"],
                                        "initial_expectation": result["initial_expectation"],
                                        "coin_steps": result["nontrivial_coin_steps"],
                                        "peak": peak, "ratio": peak / (2 - bstar),
                                        **counts})
    # Deliberate nonbasic optimal LP witnesses exercise the incidence-coin
    # phase, which the 72 basic LP optima above need not exercise.
    for n, weights in [(2, [ONE]), (3, [F(1, 3), F(2, 3)]),
                       (4, [F(1, 6), F(1, 3), F(1, 2)])]:
        m = len(weights)
        menu = [[list(weights)] for g in range(n)]
        z = [[ONE] for g in range(n)]
        x = [[[F(1, n)] * m] for g in range(n)]
        _, _, cert = welfare_lp_certificate(menu)
        assert objective(menu, x) == cert["objective"] == 1
        result = round_welfare(menu, z, x)
        assert result["nontrivial_coin_steps"] > 0
        wstar, bstar, allocations = exhaustive_values(menu)
        peak, counts = gate_schedule(menu, result)
        assert peak <= F(13, 8) * (2 - bstar)
        report["coin_cases"].append({"n": n, "m": m, "K": 1,
                                     "menu": menu, "z": z, "x": x,
                                     "optimal_lp_certificate": cert,
                                     "initial_expectation": result["initial_expectation"],
                                     "output_welfare": result["welfare"],
                                     "welfare_opt": wstar, "beta_opt": bstar,
                                     "coin_steps": result["nontrivial_coin_steps"],
                                     "peak": peak, **counts})
    for k in range(12):
        n = 1 + k % 2
        m = 1 + (k // 2) % 2
        K = 1 + (k // 4) % 2
        menu = random_menu(rng, n, m, K)
        wstar, bstar, allocs = exhaustive_values(menu)
        actual_opt, nodes, leaves = brute_gate_opt(menu)
        assert actual_opt == 2 - bstar
        report["brute_um_cases"].append({"n": n, "m": m, "K": K,
                                         "beta_opt": bstar, "um_opt": actual_opt,
                                         "search_nodes": nodes,
                                         "completed_better_schedules": leaves,
                                         "resource_allocations": allocs})
    # Out-of-contract negative control: gates change the original flat problem.
    control = [[[ONE]], [[ONE]]]
    gated_control, control_nodes, _ = brute_gate_opt(control)
    flat_jobs = [{0: ONE}, {1: ONE}, {0: ONE, 2: ONE}, {1: ONE, 2: ONE}]
    flat_best = None
    for choices in itertools.product(*(list(row) for row in flat_jobs)):
        load = [ZERO] * 3
        for row, destination in zip(flat_jobs, choices):
            load[destination] += row[destination]
        flat_best = max(load) if flat_best is None else min(flat_best, max(load))
    assert flat_best == 2 and gated_control == F(3, 2)
    report["flat_negative_control"] = {"n": 2, "states_each": 1, "resources": 1,
                                        "all_private_times": ONE,
                                        "flat_opt": flat_best, "gated_opt": gated_control,
                                        "flat_original_assignments": 4,
                                        "gated_search_nodes": control_nodes}
    tiny = F(1, 2**200 + 1)
    edge_fixtures = [
        ([[[tiny, 1 - tiny, ZERO], [1 - tiny, tiny, ZERO]]],
         [[F(1, 2), F(1, 2)]],
         [[[F(1, 2), F(1, 2), ZERO], [F(1, 2), F(1, 2), ZERO]]]),
        ([[[ONE]], [[ONE]]], [[ONE], [ONE]], [[[tiny]], [[1 - tiny]]]),
    ]
    report["large_denominator_cases"] = []
    for menu, z, x in edge_fixtures:
        check_menu(menu)
        check_lp(menu, z, x)
        result = round_welfare(menu, z, x)
        peak, counts = gate_schedule(menu, result)
        wstar, bstar, allocations = exhaustive_values(menu)
        assert result["welfare"] == wstar == objective(menu, x)
        assert peak <= F(13, 8) * (2 - bstar)
        report["large_denominator_cases"].append({"menu": menu, "z": z, "x": x,
            "welfare": result["welfare"], "peak": peak, "beta_opt": bstar,
            "nontrivial_coin_steps": result["nontrivial_coin_steps"], **counts})
    # Exact ratio square polynomial is decreasing on [0,1] and >= 1/64.
    margins = [(209 * F(k, 1024)**2 - 468 * F(k, 1024) + 260) / 64
               for k in range(1025)]
    assert min(margins) == F(1, 64)
    report["ratio_grid"] = {"points": 1025, "minimum_square_slack": min(margins),
                             "scope": "grid check; full monotonic proof is separate"}
    report["summary"] = {"support_cases": len(report["support_cases"]),
                           "certified_optimal_welfare_lp_cases": len(report["general_cases"]),
                           "general_fractional_state_cases": sum(
                               row["lp_certificate"]["fractional_z"] > 0
                               for row in report["general_cases"]),
                           "general_nontrivial_incidence_cases": sum(
                               row["lp_certificate"]["fractional_incidence_coins"] > 0
                               for row in report["general_cases"]),
                           "deliberate_optimal_nonbasic_coin_cases": len(report["coin_cases"]),
                           "nontrivial_coin_decisions": sum(
                               row["coin_steps"] for row in report["general_cases"] + report["coin_cases"]),
                           "brute_um_cases": len(report["brute_um_cases"]),
                           "max_observed_ratio": max(row["ratio"] for row in report["general_cases"])}
    report["code_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    with Path(output).open("x") as stream:
        stream.write(json.dumps(encode(report), ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(encode(report["summary"]), ensure_ascii=False, indent=2))
    print("saved", output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    if Path(args.output).exists():
        parser.error('refusing to overwrite frozen output')
    main(args.output)
