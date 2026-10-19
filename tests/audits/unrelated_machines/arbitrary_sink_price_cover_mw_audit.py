#!/usr/bin/env python3
"""Independent finite audit of the unique-home / arbitrary-sink cover-MW interface.

No repository implementation is imported. Exact Fraction arithmetic throughout.
The expensive matroid rounding stage is deliberately outside this audit.
"""

from __future__ import annotations

from dataclasses import dataclass
import argparse
from fractions import Fraction as F
from itertools import product
import hashlib
import json
import math
from pathlib import Path
import random
import sys

SEED = 2026101811
CASES_NAME = "price_cover_joint_independent_cases.json"
REPORT_NAME = "price_cover_joint_independent_report.json"


def fs(x):
    return str(x) if isinstance(x, F) else x


def ceilf(x):
    return (x.numerator + x.denominator - 1) // x.denominator


@dataclass(frozen=True)
class Private:
    home: int
    a: F
    sinks: tuple[tuple[int, F], ...]


@dataclass(frozen=True)
class Case:
    name: str
    homes: int
    sinks: int
    macros: tuple[tuple[tuple[int, F], ...], ...]
    private: tuple[Private, ...]
    T: F
    delta: F
    rho: F
    tau: F
    eta: F

    @property
    def B(self):
        return self.rho * (1 - self.tau + self.delta) * self.T


def check_case(c):
    assert c.homes + c.sinks >= 1 and c.T > 0
    assert 0 < c.eta <= 1 and F(1, 2) <= c.tau < 1
    assert c.delta >= 0 and c.rho >= 1
    assert c.B <= c.T
    for edges in c.macros:
        assert edges
        for h, p in edges:
            assert 0 <= h < c.homes and p > c.T / 2
    for h in range(c.homes):
        assert sum((j.a for j in c.private if j.home == h), F(0)) <= c.T
    for j in c.private:
        assert 0 <= j.home < c.homes and 0 <= j.a <= c.delta * c.T
        assert len(set(z for z, _ in j.sinks)) == len(j.sinks)
        for z, p in j.sinks:
            assert 0 <= z < c.sinks and 0 <= p <= c.rho * j.a


def cover_dp(items, need, eta):
    """items=(id, true home-volume, priced cost); true coverage, floor only cost.

    Each DP layer is a fresh dict; traces are immutable item-ID tuples.
    """
    if need <= 0:
        return (), F(0)
    free = tuple(k for k, a, cost in items if cost == 0)
    vol = {k: a for k, a, cost in items}
    costs = {k: cost for k, a, cost in items}
    free_vol = sum((vol[k] for k in free), F(0))
    if free_vol >= need:
        return free, F(0)
    paid = tuple((k, a, cost) for k, a, cost in items if cost > 0)
    residual = need - free_vol
    if sum((a for k, a, cost in paid), F(0)) < residual:
        return None
    q = len(paid)
    assert q > 0
    candidates = []
    for guess in sorted(set(cost for k, a, cost in paid)):
        scale = eta * guess / q
        allowed = tuple((k, a, int(cost // scale)) for k, a, cost in paid if cost <= guess)
        dp = {0: (F(0), ())}
        for k, a, weight in allowed:
            nxt = dict(dp)
            for budget, (coverage, trace) in dp.items():
                new_budget = budget + weight
                candidate = (coverage + a, trace + (k,))
                old = nxt.get(new_budget)
                if old is None or candidate[0] > old[0] or (candidate[0] == old[0] and candidate[1] < old[1]):
                    nxt[new_budget] = candidate
            dp = nxt
        possible = [b for b, (v, trace) in dp.items() if v >= residual]
        if possible:
            trace = free + dp[min(possible)][1]
            candidates.append((sum((costs[k] for k in trace), F(0)), tuple(sorted(trace))))
    if not candidates:
        return None
    cost, trace = min(candidates)
    return trace, cost


def exact_cover(items, need):
    """Separate exhaustive subset oracle; no scaled costs or DP."""
    if need <= 0:
        return (), F(0)
    best = None
    for bits in product((0, 1), repeat=len(items)):
        ids = tuple(k for bit, (k, a, cost) in zip(bits, items) if bit)
        vol = sum((a for bit, (k, a, cost) in zip(bits, items) if bit), F(0))
        if vol >= need:
            cost = sum((cost for bit, (k, a, cost) in zip(bits, items) if bit), F(0))
            candidate = cost, ids
            if best is None or candidate < best:
                best = candidate
    return None if best is None else (best[1], best[0])


def best_injection(c, home_cost):
    """Enumerate actual macro choices, enforcing home capacity one."""
    choices = [tuple(h for h, p in edges if p <= c.T and home_cost[h] is not None) for edges in c.macros]
    best = None
    for dest in product(*choices):
        if len(set(dest)) != len(dest):
            continue
        cost = sum((home_cost[h] for h in dest), F(0))
        candidate = cost, dest
        if best is None or candidate < best:
            best = candidate
    return best


COUNTERS = {
    "oracle_calls": 0, "local_cover_checks": 0, "nonempty_local_covers": 0,
    "positive_cost_covers": 0, "zero_cost_covers": 0, "infeasible_covers": 0,
    "pruned_items": 0, "matching_rejections": 0, "priced_rejections": 0,
    "actual_schedules_enumerated": 0,
}
MAXES = {"cover_approx_ratio": F(0), "mode_l1_over_B": F(0), "priced_load_over_T": F(0)}


def oracle(c, pi, check_optimality=True):
    COUNTERS["oracle_calls"] += 1
    assert len(pi) == c.sinks
    assert (sum(pi, F(0)) == 1 and min(pi) >= 0) if pi else c.sinks == 0
    by_id = dict(enumerate(c.private))
    modes, costs, exact_costs = [], [], []
    for h in range(c.homes):
        W = sum((j.a for j in c.private if j.home == h), F(0))
        need = max(W - c.tau * c.T, F(0))
        items, destination = [], {}
        for k, j in by_id.items():
            if j.home != h or not j.sinks:
                continue
            priced, z, actual = min((pi[z] * p, z, p) for z, p in j.sinks)
            destination[k] = (z, actual)
            items.append((k, j.a, priced))
        epsilon = c.eta / 4
        result = cover_dp(items, need, epsilon)
        if check_optimality:
            exact = exact_cover(items, need)
            COUNTERS["local_cover_checks"] += 1
            assert (result is None) == (exact is None)
        else:
            exact = None
        if result is None:
            COUNTERS["infeasible_covers"] += 1
            modes.append(None); costs.append(None); exact_costs.append(None)
            continue
        ids, returned_cost = result
        assert len(ids) == len(set(ids))
        assert sum((by_id[k].a for k in ids), F(0)) >= need
        assert returned_cost == sum((pi[destination[k][0]] * destination[k][1] for k in ids), F(0))
        if check_optimality:
            assert returned_cost <= (1 + epsilon) * exact[1]
            if exact[1]:
                MAXES["cover_approx_ratio"] = max(MAXES["cover_approx_ratio"], returned_cost / exact[1])
        ids = list(ids)
        # Actual-volume inclusion minimization. Destination and cost never get worse.
        for k in tuple(ids):
            if sum((by_id[t].a for t in ids if t != k), F(0)) >= need:
                ids.remove(k)
                COUNTERS["pruned_items"] += 1
        vol = sum((by_id[k].a for k in ids), F(0))
        load = [F(0)] * c.sinks
        for k in ids:
            z, actual = destination[k]
            load[z] += actual
        if need == 0:
            assert not ids
        else:
            assert ids and vol >= need
            assert all(vol - by_id[k].a < need for k in ids)
            assert vol < need + c.delta * c.T
            COUNTERS["nonempty_local_covers"] += 1
        assert sum(load, F(0)) <= c.rho * vol <= c.B
        if c.B:
            MAXES["mode_l1_over_B"] = max(MAXES["mode_l1_over_B"], sum(load, F(0)) / c.B)
        cost = sum((pi[z] * load[z] for z in range(c.sinks)), F(0))
        assert cost <= returned_cost
        if ids:
            COUNTERS["positive_cost_covers" if cost else "zero_cost_covers"] += 1
        modes.append({"ids": tuple(ids), "load": tuple(load), "volume": vol, "need": need})
        costs.append(cost)
        exact_costs.append(exact[1] if check_optimality else None)
    choice = best_injection(c, costs)
    if choice is None:
        COUNTERS["matching_rejections"] += 1
        return {"status": "NO_MATCHING"}
    cost, macro_dest = choice
    if check_optimality:
        optimum = best_injection(c, exact_costs)
        assert optimum is not None and cost <= (1 + c.eta / 4) * optimum[0]
    loads = tuple(sum((modes[h]["load"][z] for h in macro_dest), F(0)) for z in range(c.sinks))
    assert cost == sum((pi[z] * loads[z] for z in range(c.sinks)), F(0))
    assert sum(loads, F(0)) <= len(macro_dest) * c.B
    actual_dest = []
    for k, j in by_id.items():
        h = j.home
        if h in macro_dest and k in modes[h]["ids"]:
            actual_dest.append(c.homes + min((pi[z] * p, z, p) for z, p in j.sinks)[1])
        else:
            actual_dest.append(h)
    full_load = [F(0)] * (c.homes + c.sinks)
    for b, h in enumerate(macro_dest):
        full_load[h] += dict(c.macros[b])[h]
    for j, d in zip(c.private, actual_dest):
        full_load[d] += j.a if d < c.homes else dict(j.sinks)[d - c.homes]
    assert tuple(full_load[c.homes:]) == loads
    assert all(v <= (1 + c.tau) * c.T for v in full_load[:c.homes])
    MAXES["priced_load_over_T"] = max(MAXES["priced_load_over_T"], cost / c.T)
    if cost > (1 + c.eta / 4) * c.T:
        COUNTERS["priced_rejections"] += 1
        return {"status": "PRICED_FAIL", "cost": cost, "loads": loads, "macro_dest": macro_dest}
    return {"status": "OK", "cost": cost, "loads": loads, "macro_dest": macro_dest, "modes": modes,
            "private_dest": tuple(actual_dest), "actual_loads": tuple(full_load)}


def actual_optimum(c):
    """Enumerate original matrix schedules, without cover/matching assumptions."""
    choices = []
    for edges in c.macros:
        choices.append(tuple(edges))
    for j in c.private:
        choices.append(((j.home, j.a),) + tuple((c.homes + z, p) for z, p in j.sinks))
    total = math.prod(len(t) for t in choices)
    best = None
    best_dest = None
    for assignment in product(*choices):
        loads = [F(0)] * (c.homes + c.sinks)
        for machine, p in assignment:
            loads[machine] += p
        value = max(loads, default=F(0))
        if best is None or value < best:
            best, best_dest = value, tuple(machine for machine, p in assignment)
    COUNTERS["actual_schedules_enumerated"] += total
    assert best is not None
    return best, best_dest, total


def price_vectors(s, rng):
    if not s:
        return [()]
    result = [tuple(F(1, s) for _ in range(s))]
    result += [tuple(F(z == k) for z in range(s)) for k in range(s)]
    for _ in range(3):
        a = [rng.randrange(1, 10) for z in range(s)]
        result.append(tuple(F(v, sum(a)) for v in a))
    return list(dict.fromkeys(result))


def random_cases(rng, count=100):
    result = []
    for number in range(count):
        h = rng.randint(1, 3)
        s = rng.randint(0, 3)
        eta = rng.choice((F(1, 8), F(1, 4), F(1, 2)))
        delta = rng.choice((F(1, 4), F(1, 3), F(1, 2)))
        rho = rng.choice(tuple(v for v in (F(1), F(3, 2), F(2)) if v * delta < 1))
        tau = rng.choice(tuple(v for v in (F(1, 2), F(2, 3), F(3, 4), F(7, 8))
                               if rho * (1 - v + delta) <= 1))
        T = rng.choice((F(1), F(2, 3), F((1 << 81) + 1, (1 << 80) + 3)))
        private = []
        budget = 8
        for home in range(h):
            q = rng.randint(0, min(4, budget))
            budget -= q
            a_choices = (F(0), delta / 2, delta)
            W = F(0)
            for _ in range(q):
                a = rng.choice(a_choices)
                if W + a > 1:
                    a = max(F(0), 1 - W)
                W += a
                selected = [z for z in range(s) if rng.random() < 0.65]
                # Bound original schedule enumeration, while preserving noncommon eligibility.
                if len(selected) > 2:
                    selected = rng.sample(selected, 2)
                sinks = tuple((z, rho * a * rng.choice((F(0), F(1, 4), F(1, 2), F(1))) * T) for z in sorted(selected))
                private.append(Private(home, a * T, sinks))
        macros = []
        for b in range(rng.randint(0, h + 1)):
            homes = [home for home in range(h) if rng.random() < 0.7]
            if not homes:
                homes = [rng.randrange(h)]
            macros.append(tuple((home, rng.choice((F(3, 5), F(3, 4), F(1), F(5, 4))) * T) for home in homes))
        c = Case(f"random-{number}", h, s, tuple(macros), tuple(private), T, delta, rho, tau, eta)
        check_case(c)
        result.append(c)
    return result


def boundary_cases():
    result = []
    result.append(Case("no-home-empty", 0, 1, (), (), F(1), F(1, 4), F(1), F(1, 2), F(1, 4)))
    # Empty macros, zero a/p, private job without any external endpoint, all-zero price optima.
    result.append(Case("no-macro", 1, 2, (), (Private(0, F(1, 4), ((0, F(1, 4)),)),), F(1), F(1, 4), F(1), F(1, 2), F(1, 4)))
    result.append(Case("zero-work", 1, 2, (((0, F(1)),),), (Private(0, F(0), ((0, F(0)), (1, F(0)))),), F(1), F(0), F(2), F(1, 2), F(1, 4)))
    result.append(Case("no-sink-feasible", 1, 0, (((0, F(3, 4)),),), (Private(0, F(1, 4), ()),), F(1), F(1, 4), F(1), F(1, 2), F(1, 4)))
    result.append(Case("no-sink-infeasible", 1, 0, (((0, F(1)),),), tuple(Private(0, F(1, 4), ()) for _ in range(4)), F(1), F(1, 4), F(1), F(1, 2), F(1, 4)))
    result.append(Case("zero-price-and-prune", 1, 2, (((0, F(1)),),), tuple(Private(0, F(1, 4), ((0, F(1, 4)), (1, F(0)))) for _ in range(4)), F(1), F(1, 4), F(1), F(1, 2), F(1, 4)))
    # No common sink: every task has a different singleton endpoint.
    result.append(Case("disjoint-qualifications", 1, 2, (((0, F(1)),),), tuple(Private(0, F(1, 4), ((j % 2, F(1, 4)),)) for j in range(4)), F(1), F(1, 4), F(1), F(1, 2), F(1, 4)))
    # Some required volume is unexportable, but a cover remains feasible.
    result.append(Case("unexportable-forced-home", 1, 1, (((0, F(3, 5)),),), (Private(0, F(1, 4), ()),) + tuple(Private(0, F(1, 4), ((0, F(1, 4)),)) for _ in range(3)), F(1), F(1, 4), F(1), F(1, 2), F(1, 4)))
    # More macros than homes, and p>T pruning without using a large finite infinity sentinel.
    result.append(Case("too-many-macros", 1, 1, (((0, F(1)),), ((0, F(1)),)), (), F(1), F(1, 4), F(1), F(1, 2), F(1, 4)))
    result.append(Case("pruned-all-macro-edges", 1, 1, (((0, F(5, 4)),),), (), F(1), F(1, 4), F(1), F(1, 2), F(1, 4)))
    # The floor-cost DP is genuinely approximate here: the A singleton costs 2/5,
    # but the higher-coverage B+C state has the same scaled budget and costs 97/240.
    result.append(Case("genuine-cover-approximation", 1, 1, (((0, F(1)),),),
                       (Private(0, F(2, 5), ((0, F(2, 5)),)),
                        Private(0, F(3, 10), ((0, F(97, 480)),)),
                        Private(0, F(3, 10), ((0, F(97, 480)),))),
                       F(1), F(2, 5), F(1), F(3, 5), F(1, 4)))
    # W=1 and D=1/4+eps force a two-piece cover of volume 1/2; its l1/B
    # approaches one while retaining a real T=1 source schedule and sub2 parameters.
    eps = F(1, 1 << 40)
    result.append(Case("near-tight-mode-B", 1, 1, (((0, F(1)),),),
                       tuple(Private(0, F(1, 4), ((0, F(1, 4)),)) for _ in range(4)),
                       F(1), F(1, 4), F(1), F(3, 4) - eps, F(1, 8)))
    return result


def mw_case(name, h, s, parts, a, tau, eta, rho=F(1), skew=False):
    private = []
    for home in range(h):
        for j in range(parts):
            sinks = tuple((z, a * rho * (F(1, 2) if skew and (home + j + z) % 3 == 0 else F(1))) for z in range(s))
            private.append(Private(home, a, sinks))
    return Case(name, h, s, tuple(((home, F(1)),) for home in range(h)), tuple(private), F(1), a, rho, tau, eta)


def run_mw(c, full, prefix=32):
    check_case(c)
    assert c.sinks > 0
    R = max(F(1), c.homes * c.B / c.T)
    gamma = c.eta / 4
    N = ceilf(16 * R * c.sinks / (c.eta * c.eta))
    rounds = N if full else min(N, prefix)
    w = [F(1)] * c.sinks
    cum = [F(0)] * c.sinks
    upper = F(c.sinks)
    hist = []
    menu_counts = {}
    macro_counts = {}
    per_round_weight_bound = 1 + gamma * (1 + c.eta / 4) / R
    for t in range(rounds):
        W = sum(w, F(0))
        pi = tuple(v / W for v in w)
        out = oracle(c, pi)
        if out["status"] != "OK":
            return {"name": c.name, "status": out["status"], "rounds": t, "full_requested": full,
                    "R": str(R), "gamma": str(gamma), "N": N, "failed_cost": fs(out.get("cost"))}
        loads = out["loads"]
        for b, h in enumerate(out["macro_dest"]):
            macro_counts[b, h] = macro_counts.get((b, h), 0) + 1
            mode = out["modes"][h]
            sinks = tuple(out["private_dest"][k] - c.homes for k in mode["ids"])
            key = h, mode["ids"], sinks
            old = menu_counts.get(key)
            if old is None:
                menu_counts[key] = [1, mode]
            else:
                assert old[1] == mode
                old[0] += 1
        old_w = tuple(w)
        for z in range(c.sinks):
            u = loads[z] / (R * c.T)
            assert 0 <= u <= 1
            w[z] *= 1 + gamma * u
            cum[z] += loads[z]
        # Exact, log-free product-potential certificate, checked after every prefix.
        assert sum(w, F(0)) == W * (1 + gamma * out["cost"] / (R * c.T))
        upper *= per_round_weight_bound
        assert sum(w, F(0)) <= upper
        assert all(w[z] >= old_w[z] for z in range(c.sinks))
        if t < 5 or t + 1 == rounds:
            hist.append({"round": t + 1, "price": list(map(str, pi)), "loads": list(map(str, loads)),
                         "cost": str(out["cost"]), "macro_dest": list(out["macro_dest"])})
    average = tuple(v / rounds for v in cum)
    # Explicit occupied-menu copies and macro edge marginals describe the same
    # convex combination of actual matchings, rather than separate row witnesses.
    assert sum(value[0] for value in menu_counts.values()) == rounds * len(c.macros)
    for b in range(len(c.macros)):
        assert sum(v for (bb, h), v in macro_counts.items() if bb == b) == rounds
    for h in range(c.homes):
        menu_mass = sum(v[0] for (hh, ids, sinks), v in menu_counts.items() if hh == h)
        macro_mass = sum(v for (b, hh), v in macro_counts.items() if hh == h)
        assert menu_mass == macro_mass <= rounds
    for z in range(c.sinks):
        assert sum((v[0] * v[1]["load"][z] for v in menu_counts.values()), F(0)) == cum[z]
    # Parameters imply the standard analytical MW average bound with no log evaluation.
    assert R * c.sinks / (gamma * N) <= c.eta / 4
    theoretical_bound = (1 + c.eta / 4 + R * c.sinks / (gamma * N)) / (1 - gamma)
    assert theoretical_bound <= 1 + c.eta
    if full:
        assert all(v <= (1 + c.eta) * c.T for v in average)
    return {"name": c.name, "status": "OK", "rounds": rounds, "full_N_completed": full,
            "R": str(R), "gamma": str(gamma), "N": N, "average_loads": list(map(str, average)),
            "average_budget": str((1 + c.eta) * c.T),
            "parameter_upper_bound": str(theoretical_bound),
            "weight_max_bits": max(max(v.numerator.bit_length(), v.denominator.bit_length()) for v in w),
            "product_certificate_prefixes": rounds, "sample_rounds": hist,
            "distinct_occupied_menus": len(menu_counts),
            "occupied_menus": [{"home": h, "private_ids": list(ids), "sink_destinations": list(sinks),
                                "count": v[0], "weight": str(F(v[0], rounds)),
                                "load": list(map(str, v[1]["load"])), "volume": str(v[1]["volume"]),
                                "need": str(v[1]["need"])}
                               for (h, ids, sinks), v in sorted(menu_counts.items())],
            "macro_edge_marginals": [{"macro": b, "home": h, "weight": str(F(v, rounds))}
                                      for (b, h), v in sorted(macro_counts.items())]}


def case_json(c):
    return {"name": c.name, "H": c.homes, "Z": c.sinks, "T": str(c.T), "delta": str(c.delta),
            "rho": str(c.rho), "tau": str(c.tau), "eta": str(c.eta), "B": str(c.B),
            "macros": [[(h, str(p)) for h, p in edges] for edges in c.macros],
            "private": [{"home": j.home, "a": str(j.a), "sinks": [(z, str(p)) for z, p in j.sinks]} for j in c.private]}


def zero_threshold_cases():
    return [
        Case("T0-empty", 0, 1, (), (), F(0), F(1, 4), F(1), F(1, 2), F(1, 4)),
        Case("T0-all-jobs-have-zero-edge", 1, 1, (),
             (Private(0, F(0), ()), Private(0, F(0), ((0, F(0)),))),
             F(0), F(1, 4), F(2), F(3, 4), F(1, 4)),
        Case("T0-positive-macro-has-no-zero-edge", 1, 1, (((0, F(1)),),),
             (Private(0, F(0), ((0, F(0)),)),),
             F(0), F(1, 4), F(1), F(1, 2), F(1, 4)),
    ]


def audit_zero_threshold(c):
    """Run before any T-normalization, weights, prices, or size division."""
    assert c.T == 0
    choices = list(c.macros)
    choices += [((j.home, j.a),) + tuple((c.homes + z, p) for z, p in j.sinks) for j in c.private]
    zeros = [tuple(machine for machine, p in row if p == 0) for row in choices]
    if all(zeros):
        dest = tuple(min(row) for row in zeros)
        status = "ZERO_SCHEDULE"
        for d, row in zip(dest, choices):
            assert (d, F(0)) in row
    else:
        status, dest = "FAIL", None
    optimum, opt_dest, enumerated = actual_optimum(c)
    assert (status == "ZERO_SCHEDULE") == (optimum == 0)
    return {"name": c.name, "status": status, "assignment": dest,
            "OPT": str(optimum), "enumerated_original_schedules": enumerated,
            "division_by_T_performed": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path,
                        help="Create new fixture/report files here; refuse existing file paths. Without this option, print the report to stdout.")
    args = parser.parse_args()
    if args.output_dir is not None:
        for name in (CASES_NAME, REPORT_NAME):
            if (args.output_dir / name).exists():
                raise FileExistsError(f"Refusing to replace existing artifact: {args.output_dir / name}")
    rng = random.Random(SEED)
    cases = boundary_cases() + random_cases(rng)
    original_summary = []
    feasible = 0
    static_calls = 0
    for index, c in enumerate(cases):
        check_case(c)
        opt, opt_dest, enumerated = actual_optimum(c)
        feasible += opt <= c.T
        vectors = price_vectors(c.sinks, rng)
        outcomes = []
        for pi in vectors:
            out = oracle(c, pi)
            static_calls += 1
            if opt <= c.T:
                assert out["status"] == "OK", (c.name, opt, pi, out)
            outcomes.append({"price": list(map(str, pi)), "status": out["status"], "cost": fs(out.get("cost"))})
        original_summary.append({"name": c.name, "OPT": str(opt), "T_feasible": opt <= c.T,
                                 "opt_dest": opt_dest, "enumerated_schedules": enumerated, "oracle": outcomes})
        if index % 25 == 0:
            print(f"static {index + 1}/{len(cases)} schedules={COUNTERS['actual_schedules_enumerated']}", file=sys.stderr, flush=True)
    mw_cases = [
        mw_case("mw-single-sink-full", 1, 1, 4, F(1, 4), F(1, 2), F(1, 2)),
        mw_case("mw-two-sinks-full-sub2", 2, 2, 4, F(1, 4), F(3, 4), F(1, 4), skew=True),
        mw_case("mw-two-sinks-full-cycling", 3, 2, 2, F(1, 2), F(1, 2), F(1, 2)),
        mw_case("mw-priced-rejection", 4, 1, 2, F(1, 2), F(1, 2), F(1, 2)),
        mw_case("mw-small-eta-prefix", 2, 3, 4, F(1, 4), F(3, 4), F(1, 8), rho=F(3, 2), skew=True),
    ]
    mw_cases.append(Case("mw-joint-home-switch-full-sub2", 2, 2,
                         (((0, F(1)), (1, F(1))),),
                         tuple(Private(home, F(1, 4), ((home, F(1, 4)),))
                               for home in range(2) for _ in range(4)),
                         F(1), F(1, 4), F(1), F(3, 4), F(1, 4)))
    mw_results = []
    for c in mw_cases:
        opt, dest, num = actual_optimum(c)
        print(f"MW {c.name}: OPT={opt}, original schedules={num}", file=sys.stderr, flush=True)
        item = run_mw(c, full="prefix" not in c.name)
        item["OPT"] = str(opt)
        item["T_feasible"] = opt <= c.T
        item["enumerated_original_schedules"] = num
        if opt <= c.T:
            assert item["status"] == "OK"
        mw_results.append(item)
        print(f"MW completed {c.name}: {item['status']}, rounds={item['rounds']}", file=sys.stderr, flush=True)
    zero_cases = zero_threshold_cases()
    zero_results = [audit_zero_threshold(c) for c in zero_cases]
    fixture = {"static_cases": list(map(case_json, cases)), "mw_cases": list(map(case_json, mw_cases)),
               "zero_threshold_cases": list(map(case_json, zero_cases))}
    fixture_text = json.dumps(fixture, ensure_ascii=False, indent=2) + "\n"
    report = {
        "arithmetic": "fractions.Fraction; no floating-point decisions",
        "environment_not_for_exact_comparison": {"python": sys.version},
        "seed": SEED, "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "fixtures_sha256": hashlib.sha256(fixture_text.encode()).hexdigest(),
        "specification": {"cover_epsilon": "eta/4", "gamma": "eta/4", "N": "ceil(16 R K/eta^2)",
                          "mean_budget": "(1+eta)T", "R": "max(1,|H|B/T)", "required_B_over_T": "<=1"},
        "static_original_cases": len(cases), "static_T_feasible_cases": feasible,
        "static_oracle_price_calls": static_calls, "counters": COUNTERS,
        "maxima": {k: str(v) for k, v in MAXES.items()},
        "static_cases": original_summary, "mw_results": mw_results, "zero_threshold_results": zero_results,
        "scope": ["Independent min-priced eligible endpoint selection", "Independent cost-scaled covering DP and exhaustive subset optimum",
                  "Actual-volume inclusion minimization and per-mode l1 bound B", "Exhaustive macro injection matching and one-sided priced rejection",
                  "Original full processing matrix schedule enumeration", "Exact product-potential MW prefix checks and selected full-N averages",
                  "Pre-division T=0 per-job zero-edge branch"],
        "not_checked": ["No generic rational LP or matroid intersection/rounding backend", "No final matroid IR+B claim checked here",
                        "No arbitrary-instance structure extraction", "No external novelty or universal approximation claim",
                        "The small-eta three-sink case runs a strict prefix, not its complete theoretical N"],
    }
    report_text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output_dir is None:
        print(report_text, end="")
    else:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        with (args.output_dir / CASES_NAME).open("x") as f:
            f.write(fixture_text)
        with (args.output_dir / REPORT_NAME).open("x") as f:
            f.write(report_text)
        print(json.dumps({"result": "PASS", "report": str(args.output_dir / REPORT_NAME), "cases": len(cases),
                          "schedules": COUNTERS["actual_schedules_enumerated"], "oracle_calls": COUNTERS["oracle_calls"]},
                         ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
