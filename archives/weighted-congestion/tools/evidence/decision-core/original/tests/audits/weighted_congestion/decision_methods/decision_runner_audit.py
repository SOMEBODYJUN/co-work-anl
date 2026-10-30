#!/usr/bin/env python3
"""Independent literal-cost and full-certificate audit of decision_runner.

Standard library only. Author implementation checks, not external peer review.
No numerical tolerance. Does not infer an infinite-family result from tests.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import platform
import random
import subprocess
import sys
import tempfile

from decision_runner import CapacityError, Game, InputError, solve

HERE = Path(__file__).resolve().parent
FIXTURES = HERE.parents[3] / "examples/weighted_congestion/decision_methods"
RUNNER = HERE / "decision_runner.py"
SEED = 20261021


def literal_cost(raw, state, i, action=None):
    """Frozen-others single-player oracle; no import of runner load/fee logic."""
    players = raw["players"]
    chosen = players[i]["strategies"][state[i] if action is None else action]
    total = Q(0)
    for e in chosen:
        load = Q(players[i]["weight"])
        for j, player in enumerate(players):
            if j != i and e in player["strategies"][state[j]]:
                load += Q(player["weight"])
        total += sum((Q(a) * load ** k for k, a in enumerate(raw["resources"][e])), Q(0))
    return total


def independent_factor(current, alternatives):
    if current and any(x == 0 for x in alternatives):
        return "infinity"
    return str(max([Q(1), *(current / x for x in alternatives if x)]))


def verify(raw, report):
    states = list(product(*(range(len(p["strategies"])) for p in raw["players"])))
    rows = report["states"]
    assert len(rows) == len(states) == report["enumeration"]["states"]
    assert report["enumeration"]["complete"] is True
    cost_table = {s: tuple(literal_cost(raw, s, i) for i in range(len(raw["players"]))) for s in states}
    objectives = {s: (sum(cost_table[s], Q(0)), sum((Q(p["weight"]) * c for p, c in zip(raw["players"], cost_table[s])), Q(0))) for s in states}
    metrics = ("sum_cost", "weighted_sum_cost")
    factors = {}
    edges = 0
    for sid, state in enumerate(states):
        row = rows[sid]
        assert row["state_id"] == sid and tuple(row["state"]) == state
        assert tuple(map(Q, row["costs"])) == cost_table[state]
        for j, metric in enumerate(metrics):
            assert Q(row[metric]) == objectives[state][j]
        all_ratios = [Q(1)]
        expected_edges = {}
        infinite = False
        for i, p in enumerate(raw["players"]):
            alternatives = [literal_cost(raw, state, i, a) for a in range(len(p["strategies"]))]
            for action, new in enumerate(alternatives):
                if action == state[i]:
                    continue
                edges += 1
                target = state[:i] + (action,) + state[i + 1:]
                old = cost_table[state][i]
                q = independent_factor(old, [new])
                expected_edges[i, action] = (target, old, new, q)
                if q == "infinity":
                    infinite = True
                else:
                    all_ratios.append(Q(q))
        actual_edges = {(d["player"], d["to_action"]): d for d in row["deviations"]}
        assert len(actual_edges) == len(row["deviations"]) == len(expected_edges)
        for key, (target, old, new, q) in expected_edges.items():
            d = actual_edges[key]
            assert d["from_action"] == state[key[0]]
            assert d["to_state_id"] == states.index(target)
            assert Q(d["current_cost"]) == old and Q(d["deviation_cost"]) == new
            assert d["required_alpha"] == q
        factors[state] = "infinity" if infinite else str(max(all_ratios))
        assert factors[state] == row["alpha_min"]
        # Independently recompute loads and the integral, using powers rather than Horner.
        loads = {e: sum((Q(p["weight"]) for p, a in zip(raw["players"], state)
                         if e in p["strategies"][a]), Q(0)) for e in raw["resources"]}
        assert row["loads"] == {e: str(x) for e, x in loads.items()}
        potential = sum((Q(c) * loads[e] ** (k + 1) / (k + 1)
                         for e, coeffs in raw["resources"].items()
                         for k, c in enumerate(coeffs)), Q(0))
        assert Q(row["integral_potential"]) == potential
    assert edges == report["enumeration"]["nontrivial_deviations"]
    finite = [Q(q) for q in factors.values() if q != "infinity"]
    assert report["minimum_feasible_alpha"] == str(min(finite))

    def verify_decision(desc):
        state = tuple(desc["state"])
        assert desc["state_id"] == states.index(state)
        assert desc["alpha_min"] == factors[state]
        for j, metric in enumerate(metrics):
            assert Q(desc[metric]) == objectives[state][j]
            opt = min(v[j] for v in objectives.values())
            expected = "infinity" if not opt and objectives[state][j] else str(objectives[state][j] / opt if opt else Q(1))
            assert desc["ratios_to_social_optimum"][metric] == expected

    for query in report["queries"]:
        alpha = Q(query["alpha"])
        stable = [sid for sid, s in enumerate(states) if all(cost_table[s][i] <= alpha * literal_cost(raw, s, i, a)
                   for i, p in enumerate(raw["players"]) for a in range(len(p["strategies"])))]
        assert stable == query["stable_state_ids"] and len(stable) == query["stable_count"]
        assert query["status"] == ("feasible" if stable else "infeasible")
        if stable:
            for j, metric in enumerate(metrics):
                desc = query["optimal_decisions"][metric]
                verify_decision(desc)
                assert Q(desc[metric]) == min(objectives[states[sid]][j] for sid in stable)
        else:
            cert = query["nonexistence_certificate"]
            assert cert["covered_states"] == len(states)
            assert sorted(d["state_id"] for d in cert["witnesses"]) == list(range(len(states)))
            for d in cert["witnesses"]:
                s = states[d["state_id"]]
                i, a = d["player"], d["to_action"]
                old, new = cost_table[s][i], literal_cost(raw, s, i, a)
                assert old > alpha * new
                assert Q(d["current_cost"]) == old and Q(d["deviation_cost"]) == new
                assert Q(d["strict_margin"]) == old - alpha * new > 0

    for j, metric in enumerate(metrics):
        optimum = report["baselines"]["social_optima"][metric]
        verify_decision(optimum)
        assert Q(optimum[metric]) == min(v[j] for v in objectives.values())
        frontier = report["frontiers"][metric]
        previous = None
        for entry in frontier:
            alpha = Q(entry["alpha_from_inclusive"])
            verify_decision(entry["decision"])
            value = Q(entry["objective"])
            assert previous is None or value < previous
            assert value == min(objectives[s][j] for s in states if factors[s] != "infinity" and Q(factors[s]) <= alpha)
            assert Q(factors[tuple(entry["decision"]["state"])]) <= alpha
            previous = value
        # Check EVERY factor level, including ones omitted from the staircase.
        for alpha in sorted(set(finite)):
            active = [x for x in frontier if Q(x["alpha_from_inclusive"]) <= alpha]
            assert active
            assert Q(active[-1]["objective"]) == min(objectives[s][j] for s in states if factors[s] != "infinity" and Q(factors[s]) <= alpha)
    generic = report["baselines"]["generic_degree_threshold"]
    assert Q(generic["threshold"]) == max(1, report["degree"])
    for metric in metrics:
        verify_decision(generic["optimal_decisions_at_threshold"][metric])
        assert Q(generic["optimal_decisions_at_threshold"][metric]["alpha_min"]) <= Q(generic["threshold"])
    integ = report["baselines"]["integral_potential_degree_plus_one"]
    verify_decision(integ["integral_potential_minimizer"])
    assert Q(integ["integral_potential"]) == min(Q(r["integral_potential"]) for r in rows)
    assert Q(integ["integral_potential_minimizer"]["alpha_min"]) <= report["degree"] + 1

    br = report["baselines"]["fixed_order_best_response"]
    state = tuple(br["initial"])
    trace = br["trace"]
    phase_states = []
    no_moves = 0
    for turn, step in enumerate(trace):
        i = turn % len(raw["players"])
        phase_states.append((state, i))
        assert step["turn"] == turn and step["player"] == i and tuple(step["state"]) == state
        choices = [(literal_cost(raw, state, i, a), a) for a in range(len(raw["players"][i]["strategies"]))]
        new, action = min(choices)
        old = cost_table[state][i]
        moved = new < old
        assert step["best_action"] == action and Q(step["best_response_cost"]) == new
        assert Q(step["current_cost"]) == old and step["moved"] == moved
        state = state[:i] + (action,) + state[i + 1:] if moved else state
        no_moves = 0 if moved else no_moves + 1
        assert tuple(step["next_state"]) == state
    if br["status"] == "cycle":
        assert (state, len(trace) % len(raw["players"])) == phase_states[br["cycle_start_turn"]]
        assert br["cycle_length_turns"] == len(trace) - br["cycle_start_turn"]
        assert any(s["moved"] for s in trace[br["cycle_start_turn"]:])
    elif br["status"] == "equilibrium":
        assert no_moves == len(raw["players"]) and factors[state] == "1"
        verify_decision(br["decision"])
    else:
        assert br["status"] == "turn_limit"
    return {"states": len(states), "deviations": edges, "minimum_alpha": report["minimum_feasible_alpha"],
            "best_response_status": br["status"], "best_response_turns": br["turns"]}


def expect_error(fn, cls):
    try:
        fn()
    except cls:
        return
    raise AssertionError(f"expected {cls.__name__}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", type=Path, help="create NEW output; refuse overwrite")
    args = ap.parse_args()
    runs, summaries, fixture_hashes = {}, {}, {}
    for path in sorted(FIXTURES.glob("*.json")):
        raw = json.loads(path.read_text())
        queries = ["1", "9/8", "16/11", "2"]
        if path.stem == "quadratic_triad":
            queries = ["1", "21/20", "286/267", "963/898", "1507/1403", "2"]
        result = solve(raw, queries)
        summaries[path.stem] = verify(raw, result)
        runs[path.stem] = result
        fixture_hashes[path.name] = sha256(path.read_bytes()).hexdigest()
    assert len(runs) == 5
    assert runs["zero_cost"]["minimum_feasible_alpha"] == "1"
    assert all(r["alpha_min"] == "1" for r in runs["zero_cost"]["states"])
    assert runs["empty_strategy"]["states"][0]["alpha_min"] == "infinity"
    assert runs["empty_strategy"]["states"][1]["alpha_min"] == "1"
    assert runs["single_player"]["states"][0]["costs"] == ["11/2"]
    assert runs["single_player"]["states"][1]["alpha_min"] == "20/11"
    triad = runs["quadratic_triad"]
    assert triad["minimum_feasible_alpha"] == "286/267"
    assert triad["baselines"]["fixed_order_best_response"]["status"] == "cycle"
    assert triad["baselines"]["fixed_order_best_response"]["cycle_length_turns"] == 6
    assert triad["queries"][0]["nonexistence_certificate"]["covered_states"] == 8
    assert triad["queries"][2]["stable_state_ids"] == [2, 5]
    hetero = runs["heterogeneous_nonlinear"]
    assert hetero["baselines"]["social_optima"]["sum_cost"]["state"] != hetero["baselines"]["social_optima"]["weighted_sum_cost"]["state"]

    rng = random.Random(SEED)
    random_summaries = []
    for case in range(40):
        names = [f"r{j}" for j in range(4)]
        raw = {"id": f"audit-random-{case}", "resources": {e: [str(rng.randrange(3)) for _ in range(rng.randrange(1, 4))] for e in names}, "players": []}
        for i in range(rng.randrange(1, 4)):
            choices = []
            target = rng.randrange(1, 4)
            while len(choices) < target:
                action = sorted(rng.sample(names, rng.randrange(5)))
                if action not in choices:
                    choices.append(action)
            raw["players"].append({"id": str(i), "weight": str(Q(rng.randrange(1, 6), rng.randrange(1, 4))), "strategies": choices})
        result = solve(raw, ["1", "7/6", "3"])
        random_summaries.append(verify(raw, result))
        # Scaling every resource cost does not change stability or response choices.
        scaled = json.loads(json.dumps(raw))
        scaled["resources"] = {e: [str(7 * Q(x)) for x in c] for e, c in raw["resources"].items()}
        scale_result = solve(scaled, ["1", "7/6", "3"])
        verify(scaled, scale_result)
        assert [r["alpha_min"] for r in result["states"]] == [r["alpha_min"] for r in scale_result["states"]]
        assert all([7 * Q(x) for x in a["costs"]] == list(map(Q, b["costs"])) for a, b in zip(result["states"], scale_result["states"]))

    raw = json.loads((FIXTURES / "quadratic_triad.json").read_text())
    expect_error(lambda: solve(raw, ["1"], max_states=7), CapacityError)
    expect_error(lambda: solve(raw, ["1"], max_deviations=23), CapacityError)
    expect_error(lambda: solve(raw, ["999/1000"]), InputError)
    expect_error(lambda: solve(raw, [1.5]), InputError)
    expect_error(lambda: solve(raw, ["1"], initial=[2, 0, 0]), InputError)
    invalids = []
    for weight in ["0", "-1", 0.5, True]:
        bad = json.loads(json.dumps(raw)); bad["players"][0]["weight"] = weight; invalids.append(bad)
    bad = json.loads(json.dumps(raw));bad["resources"]["e0_0"] = ["-1"];invalids.append(bad)
    bad = json.loads(json.dumps(raw));bad["players"][0]["strategies"] = [];invalids.append(bad)
    bad = json.loads(json.dumps(raw));bad["players"][0]["strategies"] = [["missing"]];invalids.append(bad)
    bad = json.loads(json.dumps(raw));bad["players"][0]["strategies"] = [["e0_0", "e0_0"]];invalids.append(bad)
    bad = json.loads(json.dumps(raw));bad["players"][0]["strategies"] = [[], []];invalids.append(bad)
    bad = json.loads(json.dumps(raw));bad["players"][0]["id"] = "p1";invalids.append(bad)
    for bad in invalids:
        expect_error(lambda: Game(bad), InputError)
    truncated = solve(raw, ["1"], max_br_turns=1)
    assert truncated["baselines"]["fixed_order_best_response"]["status"] == "turn_limit"
    # CLI capacity failure is nonzero and explicitly says it is not nonexistence.
    cli = subprocess.run([sys.executable, str(RUNNER), str(FIXTURES / "quadratic_triad.json"), "--max-states", "7"], capture_output=True, text=True)
    assert cli.returncode == 2 and not cli.stdout
    cli_error = json.loads(cli.stderr)
    assert cli_error["status"] == "capacity_error" and cli_error["nonexistence_certified"] is False
    with tempfile.TemporaryDirectory() as temp:
        output = Path(temp) / "certificate.json"
        command = [sys.executable, str(RUNNER), str(FIXTURES / "quadratic_triad.json"), "--alpha", "286/267", "--output", str(output)]
        first = subprocess.run(command, capture_output=True, text=True)
        assert first.returncode == 0, first.stderr
        before = output.read_bytes()
        saved = json.loads(before)
        assert saved["queries"][0]["stable_count"] == 2
        second = subprocess.run(command, capture_output=True, text=True)
        assert second.returncode == 2 and output.read_bytes() == before

    report = {"status": "all exact assertions passed", "arithmetic": "standard-library fractions.Fraction, no floating-point decisions",
              "scope": "finite implementation and certificate audit; no general theorem or novelty inference; author audit, not independent external review",
              "python": platform.python_version(), "seed": SEED,
              "source_sha256": {"decision_runner.py": sha256(RUNNER.read_bytes()).hexdigest(),
                                "decision_runner_audit.py": sha256(Path(__file__).read_bytes()).hexdigest()},
              "fixture_sha256": fixture_hashes, "fixture_summaries": summaries,
              "random_games": len(random_summaries), "cost_scaled_games": len(random_summaries),
              "random_state_checks": sum(x["states"] for x in random_summaries),
              "random_deviation_checks": sum(x["deviations"] for x in random_summaries),
              "input_rejections_checked": len(invalids) + 5,
              "capacity_cli_error": cli_error, "overwrite_protection_checked": True,
              "fixture_runs": runs}
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        with args.output.open("x") as handle:
            handle.write(payload)
        print(json.dumps({k: v for k, v in report.items() if k in ("status", "fixture_summaries", "random_games", "random_state_checks", "random_deviation_checks")}))
    else:
        sys.stdout.write(payload)


if __name__ == "__main__":
    main()
