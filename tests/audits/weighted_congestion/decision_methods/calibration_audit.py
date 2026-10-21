#!/usr/bin/env python3
"""Exact, small-instance common-scale calibration and independent audit.

No numeric optimizer is used. All primal and Farkas certificates are independently
checked with Fraction. The simplex implementation has a pivot cap and returns
UNKNOWN on failure; it is not a polynomial-runtime claim.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as Q
from itertools import permutations, product
from pathlib import Path
import hashlib
import json
import random


def q(x):
    if isinstance(x, float):
        raise TypeError("Use an integer, Fraction, or exact rational string, not float")
    return x if isinstance(x, Q) else Q(x)


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), Q(0))


def verify_primal(A, b, x):
    return (len(A) == len(b) and all(len(row) == len(x) for row in A)
            and all(v >= 0 for v in x)
            and all(dot(row, x) <= rhs for row, rhs in zip(A, b)))


def verify_farkas(A, b, y):
    """Ax<=b, x>=0 is impossible if y>=0, A^T y>=0, b^T y<0."""
    return (len(A) == len(b) == len(y) and all(v >= 0 for v in y)
            and all(sum((y[i]*A[i][j] for i in range(len(A))), Q(0)) >= 0
                    for j in range(len(A[0]) if A else 0))
            and dot(b, y) < 0)


def _simplex_zero_objective(A, b, nvars=None, pivot_cap=20000):
    """Phase-I rational tableau, Bland entering/leaving rules, x>=0."""
    m = len(b)
    n = len(A[0]) if A else (nvars or 0)
    assert len(A) == m and all(len(row) == n for row in A)
    A = [[q(v) for v in row] for row in A]
    b = list(map(q, b))
    if m == 0:
        return {"status": "FEASIBLE", "x": [Q(0)]*n, "pivots": 0}
    if n == 0:
        return {"status": "FEASIBLE" if all(v >= 0 for v in b) else "INFEASIBLE",
                "x": [], "pivots": 0}
    D = [[Q(0) for _ in range(n+2)] for _ in range(m+2)]
    B, N = list(range(n, n+m)), list(range(n))+[-1]
    for i in range(m):
        D[i][:n] = A[i]
        D[i][n], D[i][n+1] = Q(-1), b[i]
    D[m+1][n] = Q(1)
    pivots = 0

    def pivot(r, s):
        nonlocal pivots
        pivots += 1
        if pivots > pivot_cap:
            raise RuntimeError("pivot cap")
        inv = 1/D[r][s]
        for i in range(m+2):
            if i == r:
                continue
            for j in range(n+2):
                if j != s:
                    D[i][j] -= D[r][j]*D[i][s]*inv
        for j in range(n+2):
            if j != s:
                D[r][j] *= inv
        for i in range(m+2):
            if i != r:
                D[i][s] *= -inv
        D[r][s] = inv
        B[r], N[s] = N[s], B[r]

    def simplex(phase):
        objective = m+1 if phase == 1 else m
        while True:
            eligible = [j for j in range(n+1)
                        if D[objective][j] < 0 and (phase == 1 or N[j] != -1)]
            if not eligible:
                return True
            s = min(eligible, key=lambda j: N[j])
            candidates = [i for i in range(m) if D[i][s] > 0]
            if not candidates:
                return False
            r = min(candidates, key=lambda i: (D[i][n+1]/D[i][s], B[i]))
            pivot(r, s)

    try:
        r = min(range(m), key=lambda i: (D[i][n+1], B[i]))
        if D[r][n+1] < 0:
            pivot(r, n)
            if not simplex(1) or D[m+1][n+1] < 0:
                return {"status": "INFEASIBLE", "pivots": pivots}
            if D[m+1][n+1] != 0:
                return {"status": "UNKNOWN", "reason": "phase-I inconsistency"}
            for i in range(m):
                if B[i] == -1:
                    candidates = [j for j in range(n+1) if N[j] != -1 and D[i][j] != 0]
                    if candidates:
                        pivot(i, min(candidates, key=lambda j: N[j]))
        if not simplex(2):
            return {"status": "UNKNOWN", "reason": "zero-objective unboundedness"}
        x = [Q(0)]*n
        for i in range(m):
            if 0 <= B[i] < n:
                x[B[i]] = D[i][n+1]
        return {"status": "FEASIBLE", "x": x, "pivots": pivots}
    except (RuntimeError, ZeroDivisionError) as exc:
        return {"status": "UNKNOWN", "reason": str(exc), "pivots": pivots}


def solve_feasibility(A, b, nvars=None, pivot_cap=20000):
    """Return only exactly verified FEASIBLE/INFEASIBLE, otherwise UNKNOWN."""
    A = [[q(v) for v in row] for row in A]
    b = list(map(q, b))
    out = _simplex_zero_objective(A, b, nvars, pivot_cap)
    if out["status"] == "FEASIBLE":
        if not verify_primal(A, b, out["x"]):
            return {"status": "UNKNOWN", "reason": "primal verification failed"}
        out["verified"] = True
        return out
    if out["status"] != "INFEASIBLE":
        return out
    # Solve the Farkas alternative rather than trusting a tableau verdict.
    m = len(b)
    n = len(A[0]) if A else (nvars or 0)
    dual_A = [[-A[i][j] for i in range(m)] for j in range(n)]
    dual_b = [Q(0)]*n
    dual_A.append(b)
    dual_b.append(Q(-1))
    dual = _simplex_zero_objective(dual_A, dual_b, m, pivot_cap)
    if dual["status"] == "FEASIBLE" and verify_farkas(A, b, dual["x"]):
        return {"status": "INFEASIBLE", "farkas": dual["x"], "verified": True,
                "pivots": out.get("pivots", 0), "dual_pivots": dual.get("pivots", 0)}
    return {"status": "UNKNOWN", "reason": "no verified Farkas certificate"}


def polynomial(coeffs, load):
    ans = Q(0)
    for a in reversed(coeffs):
        ans = ans*load + q(a)
    return ans


def ordered_potential(mask, users, weights, coeffs, order, background=Q(0)):
    """Background is absorbed into c; it has no potential contribution."""
    load, ans = q(background), Q(0)
    for i in order:
        if mask >> users.index(i) & 1:
            load += weights[i]
            ans += weights[i]*polynomial(coeffs, load)
    return ans


def local_resource(users, weights, coeffs, orders=None, background=Q(0)):
    users = tuple(users)
    orders = list(orders) if orders is not None else list(permutations(users))
    table = [[ordered_potential(mask, users, weights, coeffs, order, background)
              for mask in range(1 << len(users))] for order in orders]
    rows = []
    for mask in range(1 << len(users)):
        for bit, i in enumerate(users):
            if mask >> bit & 1:
                continue
            plus = mask | (1 << bit)
            load = q(background)+sum((weights[j] for b, j in enumerate(users)
                                     if plus >> b & 1), Q(0))
            rows.append({"player": i, "cost": polynomial(coeffs, load),
                         "mask": mask, "plus": plus,
                         "marginals": [v[plus]-v[mask] for v in table]})
    return {"users": users, "orders": orders, "table": table, "rows": rows,
            "background": q(background), "coefficients": list(map(q, coeffs))}


def fixed_marginal_calibration(rows, nplayers):
    """Rows: (player, cost>=0, actual marginal); exact best h for fixed F."""
    rows = [(i, q(cost), q(marginal)) for i, cost, marginal in rows]
    ratios = [[] for _ in range(nplayers)]
    for i, cost, marginal in rows:
        cost, marginal = q(cost), q(marginal)
        if cost < 0:
            raise ValueError("negative cost")
        if cost == 0:
            if marginal != 0:
                return {"status": "INFEASIBLE", "reason": "nonzero zero-cost marginal"}
        elif marginal <= 0:
            return {"status": "INFEASIBLE", "reason": "nonpositive positive-cost marginal"}
        else:
            ratios[i].append(marginal/cost)
    h = [min(r) if r else Q(1) for r in ratios]
    alpha = max([Q(1)]+[max(r)/min(r) for r in ratios if r])
    assert all(h[i]*cost <= marginal <= alpha*h[i]*cost for i, cost, marginal in rows)
    return {"status": "FEASIBLE", "alpha": alpha, "h": h,
            "upper": [max(r) if r else Q(0) for r in ratios]}


def dictionary_lp(resources, nplayers, alpha):
    """Resource-specific nonnegative mixture, globally common h=1+g."""
    alpha = q(alpha)
    assert alpha >= 1
    offsets, cursor = [], 0
    for resource in resources:
        offsets.append(cursor)
        cursor += len(resource["table"])
    h_offset, nvars = cursor, cursor+nplayers
    A, b = [], []
    for e, resource in enumerate(resources):
        for data in resource["rows"]:
            i, cost = data["player"], data["cost"]
            low, high = [Q(0)]*nvars, [Q(0)]*nvars
            for r, marginal in enumerate(data["marginals"]):
                low[offsets[e]+r], high[offsets[e]+r] = -marginal, marginal
            low[h_offset+i], high[h_offset+i] = cost, -alpha*cost
            A += [low, high]
            b += [-cost, alpha*cost]
    result = solve_feasibility(A, b, nvars)
    result.update({"alpha": alpha, "matrix_rows": len(A), "matrix_columns": nvars})
    if result["status"] == "FEASIBLE":
        x = result["x"]
        result["h"] = [Q(1)+v for v in x[h_offset:]]
        result["theta"] = [x[off:off+len(r["table"])] for off, r in zip(offsets, resources)]
        assert verify_dictionary(resources, result["h"], result["theta"], alpha)
    return result


def verify_dictionary(resources, h, theta, alpha):
    alpha = q(alpha)
    if len(theta) != len(resources) or any(v <= 0 for v in h) or q(alpha) < 1:
        return False
    for resource, coeffs in zip(resources, theta):
        if len(coeffs) != len(resource["table"]) or any(v < 0 for v in coeffs):
            return False
        for data in resource["rows"]:
            marginal = dot(coeffs, data["marginals"])
            target = h[data["player"]]*data["cost"]
            if not target <= marginal <= alpha*target:
                return False
    return True


def full_local_lp(resources, nplayers, alpha):
    """Free F_e(mask)>=0, with F_e(0)=0; equivalent to unrestricted local F."""
    alpha = q(alpha)
    offsets, cursor = [], 0
    for resource in resources:
        offsets.append(cursor)
        cursor += (1 << len(resource["users"]))-1
    h_offset, nvars = cursor, cursor+nplayers
    A, b = [], []
    for e, resource in enumerate(resources):
        for data in resource["rows"]:
            i, cost = data["player"], data["cost"]
            low, high = [Q(0)]*nvars, [Q(0)]*nvars
            high[offsets[e]+data["plus"]-1] += 1
            if data["mask"]:
                high[offsets[e]+data["mask"]-1] -= 1
            low = [-v for v in high]
            low[h_offset+i], high[h_offset+i] = cost, -alpha*cost
            A += [low, high]
            b += [-cost, alpha*cost]
    result = solve_feasibility(A, b, nvars)
    result.update({"alpha": q(alpha), "matrix_rows": len(A), "matrix_columns": nvars})
    if result["status"] == "FEASIBLE":
        x = result["x"]
        result["h"] = [Q(1)+v for v in x[h_offset:]]
        result["potentials"] = [[Q(0)]+x[off:off+(1 << len(r["users"]))-1]
                                for off, r in zip(offsets, resources)]
        assert verify_local(resources, result["h"], result["potentials"], q(alpha))
    return result


def verify_local(resources, h, potentials, alpha):
    if len(resources) != len(potentials) or any(v <= 0 for v in h) or alpha < 1:
        return False
    for resource, values in zip(resources, potentials):
        if len(values) != 1 << len(resource["users"]):
            return False
        for data in resource["rows"]:
            marginal = values[data["plus"]]-values[data["mask"]]
            cost = h[data["player"]]*data["cost"]
            if not cost <= marginal <= alpha*cost:
                return False
    return True


def state_graph_lp(costs, edges, alpha):
    """costs[state][player]; edges=(source,target,mover), all true deviations."""
    alpha = q(alpha)
    nstates, nplayers = len(costs), len(costs[0])
    nvars, A, b = nstates+nplayers, [], []
    for source, target, i in edges:
        budget = alpha*costs[target][i]-costs[source][i]
        row = [Q(0)]*nvars
        row[target] += 1
        row[source] -= 1
        row[nstates+i] -= budget
        A.append(row)
        b.append(budget)
    result = solve_feasibility(A, b, nvars)
    result.update({"alpha": alpha, "matrix_rows": len(A), "matrix_columns": nvars})
    if result["status"] == "FEASIBLE":
        result["phi"] = result["x"][:nstates]
        result["h"] = [Q(1)+v for v in result["x"][nstates:]]
        assert verify_graph(costs, edges, result["phi"], result["h"], alpha)
    return result


def verify_graph(costs, edges, phi, h, alpha):
    alpha = q(alpha)
    return (len(phi) == len(costs) and len(h) == len(costs[0]) and alpha >= 1
            and all(v > 0 for v in h)
            and all(phi[t]-phi[s] <= h[i]*(alpha*costs[t][i]-costs[s][i])
                    for s, t, i in edges))


def fixed_h_difference_certificate(costs, edges, h, alpha):
    """Exact Bellman-Ford: potential or a negative-cycle budget certificate."""
    alpha = q(alpha)
    h = list(map(q, h))
    if alpha < 1 or any(v <= 0 for v in h):
        raise ValueError("alpha>=1 and h>0 required")
    n = len(costs)
    budgets = [h[i]*(alpha*costs[t][i]-costs[s][i]) for s, t, i in edges]
    distance, predecessor = [Q(0)]*n, [None]*n
    updated = None
    for _ in range(n):
        updated = None
        for edge_index, (s, t, _) in enumerate(edges):
            candidate = distance[s]+budgets[edge_index]
            if distance[t] > candidate:
                distance[t] = candidate
                predecessor[t] = (s, edge_index)
                updated = t
        if updated is None:
            phi = [v-min(distance) for v in distance]
            assert verify_graph(costs, edges, phi, h, alpha)
            return {"status": "FEASIBLE", "h": h, "phi": phi, "alpha": alpha,
                    "verified": True}
    vertex = updated
    for _ in range(n):
        vertex = predecessor[vertex][0]
    start, reverse_cycle = vertex, []
    while True:
        previous, edge_index = predecessor[vertex]
        reverse_cycle.append(edge_index)
        vertex = previous
        if vertex == start:
            break
    cycle = list(reversed(reverse_cycle))
    total = sum((budgets[j] for j in cycle), Q(0))
    assert total < 0
    assert all(edges[cycle[j]][1] == edges[cycle[(j+1) % len(cycle)]][0]
               for j in range(len(cycle)))
    return {"status": "INFEASIBLE", "h": h, "alpha": alpha, "cycle": cycle,
            "cycle_edges": [edges[j] for j in cycle], "cycle_budget": total, "verified": True}


def fixed_h_exact_threshold(costs, edges, h, cycle_cap=100000):
    """Enumerate simple cycles for an exact rational optimum with fixed h.

    Exponential in the explicit graph; a cap produces UNKNOWN, never a NO.
    """
    h = list(map(q, h))
    if any(v <= 0 for v in h):
        raise ValueError("h>0 required")
    outgoing = [[] for _ in costs]
    for edge_index, (s, t, i) in enumerate(edges):
        outgoing[s].append((t, i, edge_index))
    alpha, critical, cycles = Q(1), None, 0
    impossible = None

    def visit(start, state, seen, path, numerator, denominator):
        nonlocal alpha, critical, cycles, impossible
        for t, i, edge_index in outgoing[state]:
            if t < start:
                continue
            a = numerator+h[i]*costs[state][i]
            b = denominator+h[i]*costs[t][i]
            if t == start:
                cycles += 1
                if cycles > cycle_cap:
                    raise RuntimeError("cycle cap")
                cycle = path+[edge_index]
                if b == 0:
                    if a > 0:
                        impossible = cycle
                elif a/b > alpha:
                    alpha, critical = a/b, cycle
            elif t not in seen:
                visit(start, t, seen | {t}, path+[edge_index], a, b)
    try:
        for start in range(len(costs)):
            visit(start, start, {start}, [], Q(0), Q(0))
    except (RuntimeError, RecursionError) as exc:
        return {"status": "UNKNOWN", "reason": str(exc), "cycles": cycles}
    if impossible is not None:
        a = sum((h[edges[j][2]]*costs[edges[j][0]][edges[j][2]] for j in impossible), Q(0))
        b = sum((h[edges[j][2]]*costs[edges[j][1]][edges[j][2]] for j in impossible), Q(0))
        assert a > 0 and b == 0
        assert all(edges[impossible[j]][1] == edges[impossible[(j+1) % len(impossible)]][0]
                   for j in range(len(impossible)))
        return {"status": "NO_FINITE_FACTOR", "zero_denominator_cycle": impossible,
                "cycle_edges": [edges[j] for j in impossible], "numerator": a,
                "denominator": b, "verified": True, "cycles": cycles}
    cert = fixed_h_difference_certificate(costs, edges, h, alpha)
    assert cert["status"] == "FEASIBLE"
    return {"status": "FEASIBLE", "alpha": alpha, "critical_cycle": critical,
            "cycles": cycles, "certificate": cert}


def exact_profile_factor(costs, edges, state):
    factor = Q(1)
    for source, target, i in edges:
        if source != state:
            continue
        old, new = costs[source][i], costs[target][i]
        if new == 0:
            if old > 0:
                return None  # infinity
        else:
            factor = max(factor, old/new)
    return factor


def exact_stability_certificate(costs, edges, state, alpha):
    rows = [{"source": s, "target": t, "player": i,
             "old": costs[s][i], "new": costs[t][i],
             "slack": alpha*costs[t][i]-costs[s][i]}
            for s, t, i in edges if s == state]
    return {"state": state, "alpha": alpha, "verified": all(r["slack"] >= 0 for r in rows),
            "maximum_ratio": exact_profile_factor(costs, edges, state), "deviations": rows}


def calibrated_descent(costs, edges, phi, h, alpha, start=0):
    assert verify_graph(costs, edges, phi, h, alpha)
    outgoing = [[] for _ in costs]
    gaps = []
    for s, t, i in edges:
        outgoing[s].append((t, i))
        gap = h[i]*(costs[s][i]-alpha*costs[t][i])
        if gap > 0:
            gaps.append(gap)
    state, path, seen = start, [start], {start}
    while True:
        chosen = next(((t, i) for t, i in outgoing[state]
                       if costs[state][i] > alpha*costs[t][i]), None)
        if chosen is None:
            break
        target, _ = chosen
        assert phi[target] < phi[state] and target not in seen
        seen.add(target)
        path.append(target)
        state = target
    cert = exact_stability_certificate(costs, edges, state, alpha)
    assert cert["verified"]
    bound = len(costs)-1
    if gaps:
        bound = min(bound, int((phi[start]-min(phi))/min(gaps)))
    assert len(path)-1 <= bound
    return {"path": path, "steps": len(path)-1, "step_bound": bound,
            "minimum_strict_gap": min(gaps) if gaps else None, "stability": cert}


def exact_bisection(oracle, low, high, rounds=8):
    """Excluded low, feasible high; no claim that the infimum is attained."""
    low, high = q(low), q(high)
    upper = oracle(high)
    assert upper["status"] == "FEASIBLE"
    at_low = oracle(low)
    if at_low["status"] == "FEASIBLE":
        assert low == 1
        return {"lower": low, "upper": low, "exact_optimum": True, "certificate": at_low}
    if at_low["status"] != "INFEASIBLE":
        return {"lower": Q(1), "upper": high, "exact_optimum": False, "status": "UNKNOWN"}
    calls = [{"alpha": low, "status": "INFEASIBLE"}, {"alpha": high, "status": "FEASIBLE"}]
    for _ in range(rounds):
        middle = (low+high)/2
        result = oracle(middle)
        calls.append({"alpha": middle, "status": result["status"]})
        if result["status"] == "FEASIBLE":
            high, upper = middle, result
        elif result["status"] == "INFEASIBLE":
            low = middle
        else:
            break
    return {"lower_excluded": low, "upper_feasible": high, "width": high-low,
            "exact_optimum": False, "calls": calls, "certificate": upper}


def enumerate_game(weights, strategies, coefficients):
    """Pure data adapter: resources integer-indexed, coefficients low degree first."""
    weights = list(map(q, weights))
    strategies = [[frozenset(s) for s in menu] for menu in strategies]
    profiles = list(product(*[range(len(menu)) for menu in strategies]))
    index = {s: k for k, s in enumerate(profiles)}
    costs, edges = [], []
    for profile in profiles:
        sets = [strategies[i][a] for i, a in enumerate(profile)]
        loads = [sum((weights[i] for i, S in enumerate(sets) if e in S), Q(0))
                 for e in range(len(coefficients))]
        fees = [polynomial(c, x) for c, x in zip(coefficients, loads)]
        costs.append([sum((fees[e] for e in S), Q(0)) for S in sets])
    for source, profile in enumerate(profiles):
        for i, menu in enumerate(strategies):
            for action in range(len(menu)):
                if action != profile[i]:
                    target = list(profile)
                    target[i] = action
                    edges.append((source, index[tuple(target)], i))
    locals_ = []
    for e, coeffs in enumerate(coefficients):
        mandatory = [i for i, menu in enumerate(strategies) if all(e in S for S in menu)]
        optional = [i for i, menu in enumerate(strategies)
                    if any(e in S for S in menu) and not all(e in S for S in menu)]
        background = sum((weights[i] for i in mandatory), Q(0))
        ascending = tuple(sorted(optional, key=lambda i: (weights[i], i)))
        descending = tuple(reversed(ascending))
        orders = list(dict.fromkeys([ascending, descending]))
        locals_.append(local_resource(optional, weights, coeffs, orders, background))
    return {"profiles": profiles, "costs": costs, "edges": edges,
            "resources": locals_, "weights": weights, "strategies": strategies}


def from_runner_game(game):
    """Adapter for decision_runner.Game without importing or modifying that file."""
    names = list(game.resources)
    resource_index = {name: i for i, name in enumerate(names)}
    weights = [player.weight for player in game.players]
    menus = [[{resource_index[name] for name in strategy} for strategy in player.strategies]
             for player in game.players]
    out = enumerate_game(weights, menus, [game.resources[name] for name in names])
    # Independently compare the adapter's full cost table to the runner oracle.
    for profile, costs in zip(out["profiles"], out["costs"]):
        _, runner_costs = game.costs(profile)
        if tuple(costs) != tuple(runner_costs):
            raise ValueError("runner/calibration cost-table mismatch")
    out["resource_names"] = names
    out["player_names"] = [player.id for player in game.players]
    return out


def dictionary_graph_potential(game, theta):
    phi = []
    for profile in game["profiles"]:
        total = Q(0)
        for e, resource in enumerate(game["resources"]):
            mask = sum(1 << b for b, i in enumerate(resource["users"])
                       if e in game["strategies"][i][profile[i]])
            total += sum((a*table[mask] for a, table in zip(theta[e], resource["table"])), Q(0))
        phi.append(total)
    return phi


def _jsonable(x):
    if isinstance(x, Q):
        return str(x)
    if isinstance(x, dict):
        return {str(k): _jsonable(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [_jsonable(v) for v in x]
    return x


def audit():
    counts = {"lp_certificates": 0, "local_rows": 0, "games": 0,
              "states": 0, "deviations": 0, "descent_runs": 0}
    # Simplex boundary/regression examples, including exact Farkas rejection.
    lp_examples = [([[1], [-1]], [0, -1], "INFEASIBLE"),
                   ([[1], [-1]], [2, -1], "FEASIBLE"),
                   ([[0]], [-1], "INFEASIBLE"),
                   ([[0]], [0], "FEASIBLE"),
                   ([[1, -1], [-1, 1]], [-1, -1], "INFEASIBLE"),
                   ([], [], "FEASIBLE")]
    for A, b, status in lp_examples:
        out = solve_feasibility(A, b, nvars=2 if not A else None)
        assert out["status"] == status and out["verified"]
        counts["lp_certificates"] += 1
    # Exhaustive one-variable boxes, checked by a separate interval oracle.
    for a in product(range(-2, 3), repeat=2):
        for b in product(range(-2, 3), repeat=2):
            lower, upper, possible = Q(0), None, True
            for aa, bb in zip(a, b):
                if aa > 0:
                    v = Q(bb, aa)
                    upper = v if upper is None else min(upper, v)
                elif aa < 0:
                    lower = max(lower, Q(bb, aa))
                elif bb < 0:
                    possible = False
            possible = possible and (upper is None or lower <= upper)
            out = solve_feasibility([[a[0]], [a[1]]], list(b))
            assert out["status"] == ("FEASIBLE" if possible else "INFEASIBLE")
            assert out["verified"]
            counts["lp_certificates"] += 1
    fixed = fixed_marginal_calibration([(0, Q(1), Q(1)), (0, Q(1), Q(100))], 1)
    assert fixed["alpha"] == 100 and fixed["h"] == [Q(1)]
    assert fixed_marginal_calibration([(0, Q(0), Q(1))], 1)["status"] == "INFEASIBLE"
    assert fixed_marginal_calibration([(0, Q(1), Q(0))], 1)["status"] == "INFEASIBLE"
    assert fixed_marginal_calibration([(0, Q(0), Q(0))], 1)["alpha"] == 1

    # Exact calibration on differing polynomial resources, not sampled envelopes.
    weights = [Q(3), Q(1)]
    resources = [local_resource((0, 1), weights, c, [(0, 1), (1, 0)])
                 for c in [(0, 0, 1), (0, 0, 0, 1), (1,), (0,)]]
    intervals = {}
    for label, oracle in [("dictionary", lambda a: dictionary_lp(resources, 2, a)),
                           ("full_local", lambda a: full_local_lp(resources, 2, a))]:
        intervals[label] = exact_bisection(oracle, 1, 3, 9)
        upper = intervals[label].get("upper_feasible", intervals[label].get("upper"))
        assert upper < 3
    counts["local_rows"] += sum(len(r["rows"]) for r in resources)
    # Analytic two-player full-local optimum: positive root of this polynomial.
    # Checking rational signs corroborates, but does not prove, the analytic formula.
    optimum_polynomial = lambda a: 997*a*a-96*a-1015
    full_interval = intervals["full_local"]
    assert optimum_polynomial(full_interval["lower_excluded"]) < 0
    assert optimum_polynomial(full_interval["upper_feasible"]) > 0
    # Full permutations, missing categories, equal weights, nonintegral weights,
    # constant/zero fees, and nonzero mandatory background.
    grids = [([Q(4), Q(2), Q(1)], (0, 1, 2)),
             ([Q(3, 2), Q(3, 2), Q(1, 3)], (0, 1, 2)),
             ([Q(7), Q(1), Q(2, 5)], (0, 2)),
             ([Q(1)], (0,))]
    for weights_, users in grids:
        for coeffs in [(0,), (2,), (1, 3), (2, 0, 1), (0, 0, 0, 1)]:
            for background in [Q(0), Q(5, 3)]:
                orders = list(permutations(users))
                resource = local_resource(users, weights_, coeffs, orders, background)
                degree = len(coeffs)-1
                alpha = Q(max(1, degree))
                ascending = tuple(sorted(users, key=lambda i: (weights_[i], i)))
                theta = [Q(order == ascending) for order in orders]
                h = [w for w in weights_]
                assert verify_dictionary([resource], h, [theta], alpha)
                rows = [(data["player"], data["cost"], dot(theta, data["marginals"]))
                        for data in resource["rows"]]
                fixed_ = fixed_marginal_calibration(rows, len(weights_))
                assert fixed_["status"] == "FEASIBLE" and fixed_["alpha"] <= alpha
                counts["local_rows"] += len(rows)

    # Supplied independently by the attacking agent: exact PNE exists, while
    # alpha=1 common-scale graph calibration is impossible.
    obstruction = enumerate_game([1, 2], [[set(), {0}, {1}, {0, 1}]]*2,
                                 [(0, 1), (0, 0, 1)])
    obstruction_no = state_graph_lp(obstruction["costs"], obstruction["edges"], 1)
    assert obstruction_no["status"] == "INFEASIBLE" and obstruction_no["verified"]
    assert exact_profile_factor(obstruction["costs"], obstruction["edges"], 0) == 1
    fixed_no = fixed_h_difference_certificate(obstruction["costs"], obstruction["edges"], [1, 2], 1)
    assert fixed_no["status"] == "INFEASIBLE"
    assert fixed_h_difference_certificate(obstruction["costs"], obstruction["edges"], [1, 2], 2)["status"] == "FEASIBLE"
    threshold_costs = [[Q(3), Q(1)], [Q(1), Q(2)]]
    threshold_edges = [(0, 1, 0), (1, 0, 1)]
    threshold = fixed_h_exact_threshold(threshold_costs, threshold_edges, [1, 1])
    assert threshold["alpha"] == Q(5, 2)
    games = [enumerate_game([3, 1], [[{0, 2}, {1, 2}, set()],
                                    [{0, 2}, {1, 2}, {2}]],
                            [(0, 0, 1), (0, 0, 0, 1), (1, 1)]),
             enumerate_game([2, 1], [[set(), {0}], [{0}, {1}]], [(0,), (1,)]),
             enumerate_game([3, 2, 1], [[{0}, {0, 1}], [{0}, {0, 2}], [{1}, {2}]],
                            [(1, 0, 1), (0, 0, 0, 1), (2,)]), obstruction]
    rng = random.Random(20261021)
    all_sets = [set(), {0}, {1}, {2}, {0, 1}, {0, 2}, {1, 2}, {0, 1, 2}]
    for _ in range(8):
        weights_ = [Q(rng.randint(1, 4), rng.randint(1, 3)) for _ in range(3)]
        menus = [rng.sample(all_sets, 2) for _ in weights_]
        coefficients = [tuple(rng.randint(0, 2) for _ in range(4)) for _ in range(3)]
        games.append(enumerate_game(weights_, menus, coefficients))
    game_results = []
    for game in games:
        costs, edges = game["costs"], game["edges"]
        degree = max(len(r["coefficients"])-1 for r in game["resources"])
        baseline = Q(max(1, degree))
        local = dictionary_lp(game["resources"], len(game["weights"]), baseline)
        assert local["status"] == "FEASIBLE"
        phi = dictionary_graph_potential(game, local["theta"])
        assert verify_graph(costs, edges, phi, local["h"], baseline)
        alpha1 = state_graph_lp(costs, edges, Q(1))
        assert alpha1["status"] in ("FEASIBLE", "INFEASIBLE")
        chosen = alpha1 if alpha1["status"] == "FEASIBLE" else state_graph_lp(costs, edges, baseline)
        assert chosen["status"] == "FEASIBLE"
        descents = [calibrated_descent(costs, edges, chosen["phi"], chosen["h"], chosen["alpha"], s)
                    for s in range(len(costs))]
        factors = [exact_profile_factor(costs, edges, s) for s in range(len(costs))]
        optimum = min(v for v in factors if v is not None)
        assert optimum <= baseline
        counts["games"] += 1
        counts["states"] += len(costs)
        counts["deviations"] += len(edges)
        counts["descent_runs"] += len(descents)
        counts["local_rows"] += sum(len(r["rows"]) for r in game["resources"])
        game_results.append({"states": len(costs), "deviations": len(edges), "degree": degree,
                             "exact_game_factor": optimum, "graph_alpha1_status": alpha1["status"],
                             "selected_alpha": chosen["alpha"],
                             "h": chosen["h"], "phi": chosen["phi"],
                             "max_steps": max(d["steps"] for d in descents),
                             "sample_descent": max(descents, key=lambda d: d["steps"])})
    # Candidate perturbation must be rejected by independent row verifier.
    cert = dictionary_lp(resources, 2, 3)
    bad_h = cert["h"][:]
    bad_h[0] *= 10**6
    assert not verify_dictionary(resources, bad_h, cert["theta"], 3)
    # A deliberately synthetic graph tests a genuine exact NO certificate.
    synthetic_costs = [[Q(2), Q(1)], [Q(1), Q(2)]]
    synthetic_edges = [(0, 1, 0), (1, 0, 1)]
    synthetic_no = state_graph_lp(synthetic_costs, synthetic_edges, Q(1))
    assert synthetic_no["status"] == "INFEASIBLE" and synthetic_no["verified"]
    return {"claim_id": "WC-FINITE-COMMON-SCALE-CALIBRATION-v1", "status": "PASS",
            "arithmetic": "fractions.Fraction; exact rational simplex and primal/Farkas verification",
            "seed": 20261021, "counts": counts, "calibration_intervals": intervals,
            "analytic_full_local_optimum": {"polynomial": ["-1015", "-96", "997"],
                "root_selection": "unique positive root; exact derivation in calibration.md",
                "lower_sign": optimum_polynomial(full_interval["lower_excluded"]),
                "upper_sign": optimum_polynomial(full_interval["upper_feasible"])},
            "games": game_results, "synthetic_graph_no": synthetic_no,
            "real_game_calibration_no_despite_exact_pne": {"graph_lp": obstruction_no,
                "empty_profile_stability": exact_stability_certificate(obstruction["costs"], obstruction["edges"], 0, Q(1)),
                "fixed_h_negative_cycle": fixed_no,
                "source": "Independently supplied by independent_attack agent; reconstructed and rerun here"},
            "synthetic_fixed_h_exact_threshold": threshold,
            "scope": "Finite implementation audits only; general theorem is proved in calibration.md; "
                     "NO rejects the specified calibration LP, not existence of alpha-PNE."}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path(__file__).with_suffix(".json"))
    args = parser.parse_args()
    result = audit()
    result["source_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(_jsonable(result), stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps(_jsonable({"status": result["status"], "output": str(args.output),
                               "counts": result["counts"],
                               "intervals": {k: {kk: vv for kk, vv in v.items() if kk != "certificate"}
                                             for k, v in result["calibration_intervals"].items()}}),
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
