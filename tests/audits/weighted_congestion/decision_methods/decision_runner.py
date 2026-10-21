#!/usr/bin/env python3
"""Exact decision/optimization for SMALL EXPLICIT weighted congestion games.

Only Python's standard library is required. This enumerates the Cartesian
product of explicitly listed strategies; it is NOT a compact-input polynomial
algorithm or a proof of any universal equilibrium threshold. See runner.md.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sys


class InputError(ValueError):
    pass


class CapacityError(ValueError):
    """An incomplete search must never be reported as mathematical nonexistence."""


def rational(value, label="rational"):
    if isinstance(value, bool) or not isinstance(value, (int, str, F)):
        raise InputError(f"{label}: use an integer or rational string, never a JSON float")
    try:
        return F(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise InputError(f"{label}: invalid rational {value!r}") from exc


def qs(x):
    return "infinity" if x is None else str(x)


def factor(old, new):
    """Least admissible alpha >= 1 for one comparison; None means +infinity."""
    if not new:
        return None if old else F(1)
    return max(F(1), old / new)


def ratio(value, optimum):
    if not optimum:
        return F(1) if not value else None
    return value / optimum


def polynomial(coefficients, load):
    value = F(0)
    for coefficient in reversed(coefficients):
        value = value * load + coefficient
    return value


@dataclass(frozen=True)
class Player:
    id: str
    weight: F
    strategies: tuple[frozenset[str], ...]


class Game:
    def __init__(self, raw):
        if not isinstance(raw, dict):
            raise InputError("game must be an object")
        self.id = str(raw.get("id", "unnamed"))
        source_resources = raw.get("resources")
        source_players = raw.get("players")
        if not isinstance(source_resources, dict) or not source_resources:
            raise InputError("resources must be a nonempty object")
        self.resources = {}
        for name, values in source_resources.items():
            if not isinstance(name, str) or not name:
                raise InputError("resource names must be nonempty strings")
            if not isinstance(values, list) or not values:
                raise InputError(f"resource {name}: coefficients must be a nonempty list, low degree first")
            coefficients = tuple(rational(v, f"resource {name}") for v in values)
            if any(v < 0 for v in coefficients):
                raise InputError(f"resource {name}: negative coefficient")
            while len(coefficients) > 1 and coefficients[-1] == 0:
                coefficients = coefficients[:-1]
            self.resources[name] = coefficients
        if not isinstance(source_players, list) or not source_players:
            raise InputError("players must be a nonempty list")
        self.players = []
        for i, raw_player in enumerate(source_players):
            if not isinstance(raw_player, dict):
                raise InputError(f"player {i}: must be an object")
            name = raw_player.get("id", str(i))
            if not isinstance(name, str) or not name:
                raise InputError(f"player {i}: id must be a nonempty string")
            weight = rational(raw_player.get("weight"), f"player {name} weight")
            if weight <= 0:
                raise InputError(f"player {name}: weight must be positive")
            source_strategies = raw_player.get("strategies")
            if not isinstance(source_strategies, list) or not source_strategies:
                raise InputError(f"player {name}: strategy family must be nonempty")
            strategies = []
            for action in source_strategies:
                if not isinstance(action, list) or any(not isinstance(e, str) for e in action):
                    raise InputError(f"player {name}: strategies must be lists of resource names")
                if len(set(action)) != len(action):
                    raise InputError(f"player {name}: a resource occurs twice in one subset")
                if not set(action) <= self.resources.keys():
                    raise InputError(f"player {name}: unknown resource")
                strategy = frozenset(action)
                if strategy in strategies:
                    raise InputError(f"player {name}: duplicate strategies; list each subset once")
                strategies.append(strategy)
            self.players.append(Player(name, weight, tuple(strategies)))
        if len({p.id for p in self.players}) != len(self.players):
            raise InputError("player ids must be unique")
        self.players = tuple(self.players)
        self.degree = max(len(c) - 1 for c in self.resources.values())
        self.number_states = 1
        for p in self.players:
            self.number_states *= len(p.strategies)
        self.number_deviations = self.number_states * sum(len(p.strategies) - 1 for p in self.players)

    def normalized(self):
        return {"id": self.id,
                "resources": {e: [str(x) for x in c] for e, c in sorted(self.resources.items())},
                "players": [{"id": p.id, "weight": str(p.weight),
                             "strategies": [sorted(s) for s in p.strategies]} for p in self.players]}

    def states(self):
        return product(*(range(len(p.strategies)) for p in self.players))

    def costs(self, state):
        """Literal resource loads, including a deviator's new weight exactly once."""
        loads = {e: F(0) for e in self.resources}
        for p, action in zip(self.players, state):
            for e in p.strategies[action]:
                loads[e] += p.weight
        fees = {e: polynomial(c, loads[e]) for e, c in self.resources.items()}
        costs = tuple(sum((fees[e] for e in p.strategies[a]), F(0))
                      for p, a in zip(self.players, state))
        return loads, costs

    def integral_potential(self, loads):
        return sum((coefficient * loads[e] ** (k + 1) / (k + 1)
                    for e, coefficients in self.resources.items()
                    for k, coefficient in enumerate(coefficients)), F(0))


def fixed_order_best_response(game, table, initial, max_turns):
    """Round robin by player input order; earliest minimum action; strict moves.

    Cycle detection includes the NEXT player. Repeated profiles alone are not
    enough because skipped turns can revisit a profile with a different phase.
    """
    n = len(game.players)
    if len(initial) != n or any(type(a) is not int or a < 0 or a >= len(p.strategies)
                                for p, a in zip(game.players, initial)):
        raise InputError("initial must give one valid zero-based action index per player")
    state = tuple(initial)
    phase_seen, trace = {}, []
    no_moves = 0
    for turn in range(max_turns):
        i = turn % n
        key = (state, i)
        if key in phase_seen:
            start = phase_seen[key]
            return {"status": "cycle", "initial": list(initial), "turns": turn,
                    "cycle_start_turn": start, "cycle_length_turns": turn - start,
                    "repeated_state": list(state), "next_player": i, "trace": trace}
        phase_seen[key] = turn
        old = table[state]["costs"][i]
        options = []
        for a in range(len(game.players[i].strategies)):
            t = state[:i] + (a,) + state[i + 1:]
            options.append((table[t]["costs"][i], a, t))
        new, action, target = min(options)
        moved = new < old
        trace.append({"turn": turn, "player": i, "state": list(state),
                      "best_action": action, "current_cost": str(old),
                      "best_response_cost": str(new), "moved": moved,
                      "next_state": list(target if moved else state)})
        if moved:
            state, no_moves = target, 0
        else:
            no_moves += 1
            if no_moves == n:
                return {"status": "equilibrium", "initial": list(initial), "turns": turn + 1,
                        "terminal_state": list(state), "trace": trace}
    return {"status": "turn_limit", "initial": list(initial), "turns": max_turns,
            "last_state": list(state), "trace": trace,
            "meaning": "No convergence or nonexistence conclusion from this truncated trajectory."}


def solve(raw, alphas=(F(1),), max_states=100000, max_deviations=2000000,
          initial=None, max_br_turns=None):
    game = raw if isinstance(raw, Game) else Game(raw)
    if type(max_states) is not int or max_states < 1:
        raise InputError("max_states must be a positive integer")
    if type(max_deviations) is not int or max_deviations < 0:
        raise InputError("max_deviations must be a nonnegative integer")
    if game.number_states > max_states:
        raise CapacityError(f"state_limit: {game.number_states} states exceed max_states={max_states}; NOT a no-equilibrium certificate")
    if game.number_deviations > max_deviations:
        raise CapacityError(f"deviation_limit: {game.number_deviations} deviations exceed max_deviations={max_deviations}; NOT a no-equilibrium certificate")
    alphas = tuple(rational(a, "alpha") for a in alphas)
    if not alphas or any(a < 1 for a in alphas):
        raise InputError("supply at least one finite rational alpha >= 1")
    states = list(game.states())
    table = {}
    for sid, state in enumerate(states):
        loads, costs = game.costs(state)
        table[state] = {"id": sid, "state": state, "loads": loads, "costs": costs,
                        "sum_cost": sum(costs, F(0)),
                        "weighted_sum_cost": sum((p.weight * c for p, c in zip(game.players, costs)), F(0)),
                        "potential": game.integral_potential(loads)}
    for state in states:
        row = table[state]
        deviations, alpha_min = [], F(1)
        for i, p in enumerate(game.players):
            for action in range(len(p.strategies)):
                if action == state[i]:
                    continue
                target = state[:i] + (action,) + state[i + 1:]
                old, new = row["costs"][i], table[target]["costs"][i]
                q = factor(old, new)
                deviations.append({"player": i, "player_id": p.id, "from_action": state[i],
                                   "to_action": action, "to_state_id": table[target]["id"],
                                   "current_cost": str(old), "deviation_cost": str(new),
                                   "required_alpha": qs(q)})
                if q is None or (alpha_min is not None and q > alpha_min):
                    alpha_min = q
        row["alpha_min"], row["deviations"] = alpha_min, deviations

    metrics = ("sum_cost", "weighted_sum_cost")
    optima = {m: min(table.values(), key=lambda r: (r[m], r["state"])) for m in metrics}

    def describe(row):
        return {"state_id": row["id"], "state": list(row["state"]),
                "alpha_min": qs(row["alpha_min"]),
                "costs": [str(c) for c in row["costs"]],
                **{m: str(row[m]) for m in metrics},
                "ratios_to_social_optimum": {m: qs(ratio(row[m], optima[m][m])) for m in metrics}}

    def query(alpha):
        stable = [r for r in table.values() if r["alpha_min"] is not None and r["alpha_min"] <= alpha]
        result = {"alpha": str(alpha), "status": "feasible" if stable else "infeasible",
                  "stable_state_ids": [r["id"] for r in stable], "stable_count": len(stable)}
        if stable:
            result["optimal_decisions"] = {m: describe(min(stable, key=lambda r: (r[m], r["state"]))) for m in metrics}
            # All action comparisons, including equalities and zeros, are retained.
            result["decision_certificate_state_ids"] = sorted({v["state_id"] for v in result["optimal_decisions"].values()})
        else:
            witnesses = []
            for row in table.values():
                dev = next(d for d in row["deviations"]
                           if F(d["current_cost"]) > alpha * F(d["deviation_cost"]))
                witnesses.append({"state_id": row["id"], **dev,
                                  "strict_margin": str(F(dev["current_cost"]) - alpha * F(dev["deviation_cost"]))})
            result["nonexistence_certificate"] = {"type": "one strict actual unilateral deviation for EVERY enumerated state",
                                                   "covered_states": len(witnesses), "witnesses": witnesses}
        return result

    # Staircase of the best objective attainable as the permitted factor rises.
    # Equal-cost ties at an earlier alpha are omitted, and endpoints are inclusive.
    frontiers = {}
    by_factor = sorted((r for r in table.values() if r["alpha_min"] is not None),
                       key=lambda r: (r["alpha_min"], r["state"]))
    for metric in metrics:
        frontier, previous = [], None
        best, cursor = None, 0
        while cursor < len(by_factor):
            alpha = by_factor[cursor]["alpha_min"]
            while cursor < len(by_factor) and by_factor[cursor]["alpha_min"] == alpha:
                row = by_factor[cursor]
                if best is None or (row[metric], row["alpha_min"], row["state"]) < (best[metric], best["alpha_min"], best["state"]):
                    best = row
                cursor += 1
            if previous is None or best[metric] < previous:
                frontier.append({"alpha_from_inclusive": str(alpha), "objective": str(best[metric]),
                                 "decision": describe(best)})
                previous = best[metric]
        frontiers[metric] = frontier

    degree_alpha = F(max(1, game.degree))
    integral_alpha = F(game.degree + 1)
    potential_min = min(table.values(), key=lambda r: (r["potential"], r["state"]))
    assert potential_min["alpha_min"] is not None and potential_min["alpha_min"] <= integral_alpha
    degree_query = query(degree_alpha)
    assert degree_query["status"] == "feasible", "finite instance contradicts the cited degree-threshold baseline"
    initial = tuple(0 for _ in game.players) if initial is None else tuple(initial)
    if max_br_turns is None:
        max_br_turns = game.number_states * len(game.players) + 1
    if type(max_br_turns) is not int or max_br_turns < 1:
        raise InputError("max_br_turns must be a positive integer")
    br = fixed_order_best_response(game, table, initial, max_br_turns)
    if br["status"] == "equilibrium":
        br["decision"] = describe(table[tuple(br["terminal_state"])])
    normalized = game.normalized()
    output_rows = [{**describe(r), "loads": {e: str(x) for e, x in sorted(r["loads"].items())},
                    "integral_potential": str(r["potential"]), "deviations": r["deviations"]} for r in table.values()]
    finite_min = min((r["alpha_min"] for r in table.values() if r["alpha_min"] is not None), default=None)
    result = {"schema": "explicit-wcg-decision-v1", "game": normalized,
              "input_sha256": sha256(json.dumps(normalized, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
              "arithmetic": "exact fractions.Fraction; infinity is a string, never a float",
              "cost_convention": "C_i=sum c_e(actual total weight), WITHOUT multiplying by player weight",
              "scope": "complete finite explicit state enumeration, exponential in compact input; no universal-threshold or novelty claim",
              "enumeration": {"complete": True, "states": len(states), "nontrivial_deviations": game.number_deviations,
                              "max_states": max_states, "max_deviations": max_deviations},
              "degree": game.degree, "minimum_feasible_alpha": qs(finite_min),
              "queries": [query(a) for a in alphas], "frontiers": frontiers,
              "baselines": {"social_optima": {m: describe(r) for m, r in optima.items()},
                            "fixed_order_best_response": br,
                            "generic_degree_threshold": {"threshold": str(degree_alpha),
                                "identity": "known existence baseline max(1,d); enumerate its stable set, not a compact constructive d-potential algorithm",
                                "source": "Known degree-d existence baseline for d>=1, arXiv:1902.07173v5; see research/current/weighted_congestion/decision_methods/baselines.md for verified statement; d=0 is exact",
                                "source_url": "https://arxiv.org/abs/1902.07173",
                                "optimal_decisions_at_threshold": degree_query["optimal_decisions"]},
                            "integral_potential_degree_plus_one": {"threshold": str(integral_alpha),
                                "identity": "self-contained degree+1 bound via integral potential; conservative, not asserted sharp",
                                "integral_potential_minimizer": describe(potential_min),
                                "integral_potential": str(potential_min["potential"])}},
              "states": output_rows}
    return result


def human_summary(result):
    """Short report for a reviewer; the JSON remains the full certificate."""
    enumeration = result["enumeration"]
    lines = [f"Game: {result['game']['id']}",
             f"Complete explicit enumeration: {enumeration['states']} states, {enumeration['nontrivial_deviations']} deviations; degree {result['degree']}.",
             f"Minimum feasible stability factor: {result['minimum_feasible_alpha']} (inclusive)."]
    for query in result["queries"]:
        lines.append(f"alpha={query['alpha']}: {query['status']}; {query['stable_count']} stable states.")
        if query["status"] == "infeasible":
            lines.append(f"  Full nonexistence certificate covers all {query['nonexistence_certificate']['covered_states']} states with strict actual deviations.")
        else:
            for metric, desc in query["optimal_decisions"].items():
                lines.append(f"  Best {metric}={desc[metric]} at actions {desc['state']}; optimum ratio {desc['ratios_to_social_optimum'][metric]}.")
    br = result["baselines"]["fixed_order_best_response"]
    lines.append(f"Fixed-order best response: {br['status']}, {br['turns']} turns.")
    if br["status"] == "cycle":
        lines.append(f"  Phase-aware cycle length {br['cycle_length_turns']}; this trajectory alone is not a nonexistence proof.")
    lines.append(f"Known degree baseline: alpha={result['baselines']['generic_degree_threshold']['threshold']}.")
    for metric, entries in result["frontiers"].items():
        lines.append(f"{metric} frontier (inclusive alpha: cost): " + ", ".join(f"{e['alpha_from_inclusive']}: {e['objective']}" for e in entries))
    lines.append("Scope: finite explicit games; state space can be exponential; no universal-threshold or novelty claim.")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--alpha", action="append", help="exact rational >=1; repeat for several queries; default 1")
    parser.add_argument("--max-states", type=int, default=100000)
    parser.add_argument("--max-deviations", type=int, default=2000000)
    parser.add_argument("--initial", help="comma-separated zero-based actions; default all zero")
    parser.add_argument("--max-br-turns", type=int)
    parser.add_argument("--summary", action="store_true", help="also print a concise human report to stderr; JSON is unchanged")
    parser.add_argument("--output", type=Path, help="create a NEW JSON file; refuses to overwrite")
    args = parser.parse_args()
    try:
        raw = json.loads(args.input.read_text())
        initial = None if args.initial is None else [int(a) for a in args.initial.split(",")]
        result = solve(raw, args.alpha or ["1"], args.max_states, args.max_deviations, initial, args.max_br_turns)
        result["runner_sha256"] = sha256(Path(__file__).read_bytes()).hexdigest()
        payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            with args.output.open("x") as handle:
                handle.write(payload)
        else:
            sys.stdout.write(payload)
        if args.summary:
            print(human_summary(result), file=sys.stderr)
        return 0
    except (InputError, CapacityError, OSError, json.JSONDecodeError, ValueError) as exc:
        kind = "capacity_error" if isinstance(exc, CapacityError) else "input_or_output_error"
        print(json.dumps({"status": kind, "error": str(exc), "complete_enumeration": False,
                          "nonexistence_certified": False}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
