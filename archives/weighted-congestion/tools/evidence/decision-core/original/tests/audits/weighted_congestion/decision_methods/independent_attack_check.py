#!/usr/bin/env python3
"""Independent, exact finite checks for weighted-congestion method interfaces.

No floating point and no external packages. This checks the stated finite
examples; it is not evidence for a universal threshold bound.
"""

from dataclasses import dataclass
import argparse
from hashlib import sha256
from fractions import Fraction as Q
from itertools import combinations, product
import json
from pathlib import Path
from random import Random


@dataclass(frozen=True)
class Game:
    weights: tuple
    coefficients: tuple
    strategies: tuple

    def profiles(self):
        return tuple(product(*(range(len(s)) for s in self.strategies)))

    def loads(self, profile):
        return tuple(sum((self.weights[i] for i, a in enumerate(profile)
                          if e in self.strategies[i][a]), Q(0))
                     for e in range(len(self.coefficients)))

    def latency(self, e, x):
        return sum((a * x**k for k, a in enumerate(self.coefficients[e])), Q(0))

    def costs(self, profile):
        loads = self.loads(profile)
        return tuple(sum((self.latency(e, loads[e])
                          for e in self.strategies[i][a]), Q(0))
                     for i, a in enumerate(profile))

    def welfare_cost(self, profile):
        return sum((w * c for w, c in zip(self.weights, self.costs(profile))), Q(0))

    def deviations(self, profile):
        for i in range(len(self.weights)):
            for a in range(len(self.strategies[i])):
                if a != profile[i]:
                    target = list(profile)
                    target[i] = a
                    yield i, tuple(target)

    def improvement_graph(self, alpha=Q(1)):
        return {s: tuple((i, t) for i, t in self.deviations(s)
                         if self.costs(s)[i] > alpha * self.costs(t)[i])
                for s in self.profiles()}


def strategies(*rows):
    return tuple(tuple(frozenset(a) for a in row) for row in rows)


def topological_order(graph):
    indeg = {s: 0 for s in graph}
    for edges in graph.values():
        for _, t in edges:
            indeg[t] += 1
    ready = sorted(s for s, n in indeg.items() if n == 0)
    order = []
    while ready:
        s = ready.pop(0)
        order.append(s)
        for _, t in graph[s]:
            indeg[t] -= 1
            if indeg[t] == 0:
                ready.append(t)
                ready.sort()
    return tuple(order) if len(order) == len(graph) else None


def stable_states(game, alpha=Q(1)):
    return tuple(s for s, edges in game.improvement_graph(alpha).items() if not edges)


def all_coalitions(n):
    return tuple(frozenset(c) for k in range(n + 1)
                 for c in combinations(range(n), k))


def verify_margin_envelopes(game, local_potential, h, alpha, d):
    ratios = []
    for e in range(len(game.coefficients)):
        assert local_potential(e, frozenset()) == 0
        for coalition in all_coalitions(len(game.weights)):
            x = sum((game.weights[i] for i in coalition), Q(0))
            latency = game.latency(e, x)
            resource_w = x * latency
            f = local_potential(e, coalition)
            if resource_w:
                ratios.append(f / resource_w)
            else:
                assert f == 0
            for i in coalition:
                previous = coalition - {i}
                z = x - game.weights[i]
                marginal = f - local_potential(e, previous)
                assert h[i] * latency <= marginal <= alpha * h[i] * latency
                delta_w = resource_w - z * game.latency(e, z)
                assert game.weights[i] * latency <= delta_w
                assert delta_w <= (d + 1) * game.weights[i] * latency
    return min(ratios, default=Q(1)), max(ratios, default=Q(1))


def verify_decision_theorem(game, local_potential, h, alpha, d, etas):
    m, big_m = verify_margin_envelopes(game, local_potential, h, alpha, d)
    assert m > 0
    profiles = game.profiles()
    opt = min(game.welfare_cost(s) for s in profiles)

    def potential(s):
        return sum((local_potential(e, frozenset(i for i, a in enumerate(s)
                     if e in game.strategies[i][a]))
                    for e in range(len(game.coefficients))), Q(0))

    checks = []
    for eta in etas:
        beta = max((alpha * h[i] + eta * (d + 1) * game.weights[i]) /
                   (h[i] + eta * game.weights[i]) for i in range(len(h)))
        objective = {s: potential(s) + eta * game.welfare_cost(s) for s in profiles}
        minimum = min(objective.values())
        minimizers = tuple(s for s in profiles if objective[s] == minimum)
        for s in minimizers:
            assert s in stable_states(game, beta)
            assert (m + eta) * game.welfare_cost(s) <= (big_m + eta) * opt
        checks.append({"eta": eta, "beta": beta, "minimizers": minimizers,
                       "weighted_costs": [game.welfare_cost(s) for s in minimizers]})
    return {"m": m, "M": big_m, "OPT": opt, "checks": checks}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="create a NEW JSON file; default stdout")
    args = parser.parse_args()
    out = {}
    # Local exact weighted potentials do not share one player scale.
    subsets = ((), (0,), (1,), (0, 1))
    calibration = Game((Q(1), Q(2)), ((Q(0), Q(1)), (Q(0), Q(0), Q(1))),
                       strategies(subsets, subsets))
    graph = calibration.improvement_graph()
    order = topological_order(graph)
    assert order is not None
    assert stable_states(calibration) == ((0, 0),)
    # Exact full-state cost-difference calibration at alpha=1 forces
    # 2*h1=h2 on the affine square and 8*h1=5*h2 on the quadratic one.
    assert Q(1, 2) != Q(5, 8)
    out["acyclic_but_no_common_scale_calibration"] = {
        "profiles": len(graph), "strict_edges": sum(map(len, graph.values())),
        "topological_order": order, "PNE": stable_states(calibration),
        "required_h1_over_h2": {"affine": Q(1, 2), "quadratic": Q(5, 8)},
        "local_exact_potential_e": [0, 1, 4, 7],
        "local_exact_potential_f": [0, 5, 32, 77],
    }

    # An actual WC improvement cycle. Empty actions preserve the cycle and
    # introduce a unique PNE, distinguishing existence from acyclicity.
    coefficients = ((Q(0), Q(9, 2)), (Q(0), Q(0), Q(1)),
                    (Q(14),), (Q(19, 4),))
    cycle_game = Game((Q(1), Q(2)), coefficients,
                      strategies(((0, 1), (2,)), ((0,), (1, 3))))
    cycle = ((0, 0), (1, 0), (1, 1), (0, 1), (0, 0))
    cycle_edges = []
    for s, t in zip(cycle, cycle[1:]):
        i = next(i for i in range(2) if s[i] != t[i])
        before, after = cycle_game.costs(s)[i], cycle_game.costs(t)[i]
        assert before > after
        cycle_edges.append({"from": s, "to": t, "player": i + 1,
                            "before": before, "after": after,
                            "ratio": before / after})
    assert stable_states(cycle_game) == ()
    expanded = Game(cycle_game.weights, coefficients,
                    strategies(((0, 1), (2,), ()), ((0,), (1, 3), ())))
    assert stable_states(expanded) == ((2, 2),)
    assert topological_order(expanded.improvement_graph()) is None
    out["PNE_does_not_imply_acyclic"] = {
        "weights": cycle_game.weights, "coefficients": coefficients,
        "cycle_edges": cycle_edges,
        "base_best_factor": min(edge["ratio"] for edge in cycle_edges),
        "with_empty_actions_PNE": stable_states(expanded),
    }

    # Adding a constant private penalty creates a different game.
    k = Q(100)
    original = Game((Q(1),), ((Q(1),), (k,)), strategies(((0,), (1,))))
    compiled = Game((Q(1),), ((Q(1),), (k,), (k,)), strategies(((0, 2), (1,))))
    assert stable_states(compiled) == ((1,),)
    original_ratio = original.costs((1,))[0] / original.costs((0,))[0]
    assert original_ratio == k
    out["compiled_penalty_not_original_repair"] = {
        "penalty": k, "compiled_PNE": stable_states(compiled),
        "original_regret_factor_of_compiled_PNE": original_ratio,
    }

    # Exact stability does not imply weighted-social optimality.
    social = Game((Q(1), Q(1)), ((Q(0), Q(1)), (Q(2),)),
                  strategies(((0,), (1,)), ((0,), (1,))))
    assert (0, 0) in stable_states(social)
    opt = min(social.welfare_cost(s) for s in social.profiles())
    assert opt == 3 and social.welfare_cost((0, 0)) == 4
    out["stable_not_social_optimum"] = {"PNE_cost": Q(4), "OPT": opt}

    # The two common social-cost conventions need not have the same minimizer.
    conventions = Game((Q(1), Q(2)),
                       ((Q(0), Q(1)), (Q(2),), (Q(11, 4),)),
                       strategies(((0,), (1,)), ((0,), (2,))))
    profiles = conventions.profiles()
    unweighted = {s: sum(conventions.costs(s), Q(0)) for s in profiles}
    weighted = {s: conventions.welfare_cost(s) for s in profiles}
    assert min(unweighted, key=unweighted.get) == (0, 1)
    assert min(weighted, key=weighted.get) == (1, 0)
    out["social_conventions_differ"] = {
        "unweighted_minimizer": (0, 1), "unweighted_minimum": unweighted[(0, 1)],
        "weighted_minimizer": (1, 0), "weighted_minimum": weighted[(1, 0)],
    }

    # Nontrivial finite test of the Phi+eta*W interpolation theorem.
    quality = Game((Q(1), Q(2), Q(3)), ((Q(0), Q(1)), (Q(4),)),
                   strategies(*([((0,), (1,))] * 3)))

    def affine_potential(e, coalition):
        x = sum((quality.weights[i] for i in coalition), Q(0))
        a = quality.coefficients[e][1] if len(quality.coefficients[e]) > 1 else Q(0)
        b = quality.coefficients[e][0]
        own_squares = sum((quality.weights[i]**2 for i in coalition), Q(0))
        return a * (x*x + own_squares) / 2 + b * x

    out["decision_quality_affine"] = verify_decision_theorem(
        quality, affine_potential, quality.weights, Q(1), 1,
        (Q(0), Q(1, 2), Q(1), Q(4)))

    # d=0 endpoint, with exact weighted welfare as the potential.
    constant = Game((Q(1), Q(2)), ((Q(1),), (Q(2),)),
                    strategies(((0,), (1,)), ((0,), (1,))))
    def constant_potential(e, coalition):
        x = sum((constant.weights[i] for i in coalition), Q(0))
        return x * constant.latency(e, x)
    out["decision_quality_d0"] = verify_decision_theorem(
        constant, constant_potential, constant.weights, Q(1), 0, (Q(0), Q(3)))

    # Zero latencies, empty actions, and OPT=0; no divisions by zero.
    zero = Game((Q(1), Q(2)), ((Q(0),), (Q(0), Q(0), Q(1))),
                strategies(((0,), (1,), ()), ((0,), (1,), ())))
    def zero_potential(e, coalition):
        x = sum((zero.weights[i] for i in coalition), Q(0))
        return x * zero.latency(e, x)
    out["decision_quality_zero_OPT_empty"] = verify_decision_theorem(
        zero, zero_potential, zero.weights, Q(3), 2, (Q(0), Q(1), Q(10)))

    # Cross-check the method implementations against the independent game
    # evaluator above, rather than only rerunning their author audits.
    import calibration_audit as calibration_impl
    import decision_runner as runner_impl

    one_variable_counts = {"FEASIBLE": 0, "INFEASIBLE": 0}
    rng = Random(211021)
    for _ in range(1500):
        matrix = [[Q(rng.randint(-5, 5))] for _ in range(rng.randrange(8))]
        rhs = [Q(rng.randint(-8, 8)) for _ in matrix]
        lower, upper, impossible = Q(0), None, False
        for row, b in zip(matrix, rhs):
            a = row[0]
            if a > 0:
                upper = b / a if upper is None else min(upper, b / a)
            elif a < 0:
                lower = max(lower, b / a)
            elif b < 0:
                impossible = True
        feasible = not impossible and (upper is None or lower <= upper)
        answer = calibration_impl.solve_feasibility(matrix, rhs, nvars=1)
        expected = "FEASIBLE" if feasible else "INFEASIBLE"
        assert answer["status"] == expected and answer["verified"]
        one_variable_counts[expected] += 1

    def raw_game(game):
        return {"resources": {str(e): [str(a) for a in coefficients]
                              for e, coefficients in enumerate(game.coefficients)},
                "players": [{"id": str(i), "weight": str(w),
                             "strategies": [[str(e) for e in sorted(action)]
                                            for action in game.strategies[i]]}
                            for i, w in enumerate(game.weights)]}

    runner_checks = []
    examples = (calibration, cycle_game, expanded, original, compiled, social,
                conventions, quality, constant, zero)
    for game in examples:
        raw = raw_game(game)
        report = runner_impl.solve(raw, (Q(1), Q(55, 54), Q(2), Q(3)))
        profiles = game.profiles()
        index = {s: k for k, s in enumerate(profiles)}
        rows = report["states"]
        assert len(rows) == len(profiles)
        for s, row in zip(profiles, rows):
            assert tuple(row["state"]) == s
            assert tuple(map(Q, row["costs"])) == game.costs(s)
            expected = []
            for i, t in game.deviations(s):
                old, new = game.costs(s)[i], game.costs(t)[i]
                expected.append((i, index[t], old, new))
            actual = [(v["player"], v["to_state_id"], Q(v["current_cost"]),
                       Q(v["deviation_cost"])) for v in row["deviations"]]
            assert actual == expected
        for query in report["queries"]:
            alpha = Q(query["alpha"])
            stable = stable_states(game, alpha)
            assert query["stable_state_ids"] == [index[s] for s in stable]
            if stable:
                for metric, cost_fn in (("sum_cost", lambda s: sum(game.costs(s), Q(0))),
                                        ("weighted_sum_cost", game.welfare_cost)):
                    chosen = tuple(query["optimal_decisions"][metric]["state"])
                    assert chosen in stable
                    assert cost_fn(chosen) == min(cost_fn(s) for s in stable)
            else:
                witnesses = query["nonexistence_certificate"]["witnesses"]
                assert sorted(v["state_id"] for v in witnesses) == list(range(len(profiles)))
                for v in witnesses:
                    s, i = profiles[v["state_id"]], v["player"]
                    t = list(s)
                    t[i] = v["to_action"]
                    old, new = game.costs(s)[i], game.costs(tuple(t))[i]
                    assert old - alpha * new == Q(v["strict_margin"]) > 0
        finite_levels = sorted({Q(row["alpha_min"]) for row in rows
                                if row["alpha_min"] != "infinity"})
        for metric, cost_fn in (("sum_cost", lambda s: sum(game.costs(s), Q(0))),
                                ("weighted_sum_cost", game.welfare_cost)):
            for alpha in finite_levels:
                active = [v for v in report["frontiers"][metric]
                          if Q(v["alpha_from_inclusive"]) <= alpha]
                assert active
                assert Q(active[-1]["objective"]) == min(
                    cost_fn(s) for s in stable_states(game, alpha))
        runner_checks.append({"states": len(profiles), "deviations": sum(
            1 for s in profiles for _ in game.deviations(s)),
            "minimum_factor": report["minimum_feasible_alpha"]})

    # Feed both genuine WC distinctions through the full-state calibrator.
    cal_data = calibration_impl.enumerate_game(
        list(calibration.weights),
        [[[e for e in action] for action in menu] for menu in calibration.strategies],
        list(calibration.coefficients))
    cal_no = calibration_impl.state_graph_lp(cal_data["costs"], cal_data["edges"], Q(1))
    assert cal_no["status"] == "INFEASIBLE" and cal_no["verified"]
    cycle_data = calibration_impl.enumerate_game(
        list(expanded.weights),
        [[[e for e in action] for action in menu] for menu in expanded.strategies],
        list(expanded.coefficients))
    cycle_no = calibration_impl.state_graph_lp(cycle_data["costs"], cycle_data["edges"], Q(1))
    assert cycle_no["status"] == "INFEASIBLE" and cycle_no["verified"]
    mandatory = calibration_impl.enumerate_game([Q(1)], [[[0]]], [[0, 1]])
    assert mandatory["resources"][0]["table"] == [[Q(0)]]
    b = mandatory["resources"][0]["background"]
    restored = Q(1) * b * calibration_impl.polynomial([0, 1], b)
    assert restored == mandatory["costs"][0][0] == Q(1)
    out["independent_implementation_cross_checks"] = {
        "one_variable_LP_exact_cases": one_variable_counts,
        "runner_examples": runner_checks,
        "runner_total_states": sum(v["states"] for v in runner_checks),
        "runner_total_deviations": sum(v["deviations"] for v in runner_checks),
        "acyclic_game_calibration": cal_no["status"],
        "cycle_plus_PNE_calibration": cycle_no["status"],
        "both_Farkas_verified": True,
        "mandatory_only_unrestored_potential": Q(0),
        "mandatory_only_restored_potential": restored,
    }
    out["status"] = "PASS: all exact independent assertions passed"
    out["source_sha256"] = {
        Path(module_path).name: sha256(Path(module_path).read_bytes()).hexdigest()
        for module_path in (__file__, calibration_impl.__file__, runner_impl.__file__)
    }

    def encode(obj):
        if isinstance(obj, Q):
            return str(obj)
        raise TypeError(type(obj).__name__)
    payload = json.dumps(out, default=encode, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        with args.output.open("x", encoding="utf-8") as handle:
            handle.write(payload)
        print(f"PASS: exact finite checks; wrote {args.output.name}")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
