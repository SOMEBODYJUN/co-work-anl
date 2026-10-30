#!/usr/bin/env python3
"""有理拥塞博弈的整数单项式规范化与私有标记的 Fraction 审计。

The original oracle uses polynomial Horner evaluation.  The target oracle has
only an explicit list of monic resources, and sums their literal loaded costs;
it never consults the source coefficients.  The tests exhaust each finite
fixture's states and unilateral deviations, including the quotient action map.
This is a finite implementation audit, not a proof of a uniform existence bound.
Default output is JSON on stdout.  --output uses exclusive creation.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction as F
from functools import cache
import hashlib
from itertools import product
import json
from math import lcm
from pathlib import Path
import random
import sys


ROOT = Path(__file__).resolve().parents[4]
DEFAULT_INPUT = ROOT / "examples/weighted_congestion/template_certificates/exact_fixtures.json"
SEED = 73471


def require(condition, message):
    """Checks remain active if the interpreter is invoked with -O."""
    if not condition:
        raise AssertionError(message)


@dataclass(frozen=True)
class Game:
    weights: tuple
    fees: tuple
    actions: tuple


@dataclass(frozen=True)
class UnitGame:
    weights: tuple
    exponents: tuple
    actions: tuple


def parse_game(raw):
    weights = tuple(F(w) for w in raw["weights"])
    fees = tuple(tuple(F(a) for a in p) for p in raw["fees"])
    actions = tuple(tuple(frozenset(a) for a in family) for family in raw["strategies"])
    require(bool(weights) and bool(fees), "nonempty players and resources")
    require(len(weights) == len(actions), "one strategy family per player")
    require(all(w > 0 for w in weights), "positive weights")
    require(all(p and all(a >= 0 for a in p) for p in fees), "nonnegative polynomials")
    require(all(family and len(set(family)) == len(family) for family in actions),
            "source strategy families are nonempty sets of resource subsets")
    require(all(isinstance(e, int) and 0 <= e < len(fees)
                for family in actions for action in family for e in action), "resource indices")
    return Game(weights, fees, actions)


def states(g):
    return tuple(product(*(range(len(family)) for family in g.actions)))


def deviation(s, i, b):
    return tuple(b if j == i else a for j, a in enumerate(s))


@cache
def original_costs(g, s):
    """Original-resource oracle; recompute all loads at the actual state s."""
    loads = tuple(sum((w for j, w in enumerate(g.weights) if e in g.actions[j][s[j]]), F(0))
                  for e in range(len(g.fees)))
    values = []
    for e, polynomial in enumerate(g.fees):
        value = F(0)
        for a in reversed(polynomial):
            value = value * loads[e] + a
        values.append(value)
    return tuple(sum((values[e] for e in g.actions[i][b]), F(0)) for i, b in enumerate(s))


@cache
def literal_unit_costs(g, s):
    """Independent oracle: every resource exists as one actual monic resource.

    There is no grouped coefficient or source-resource lookup in this oracle.
    In particular constant resources charge load**0 == 1, including at load 0;
    only a player's selected resources enter that player's cost.
    """
    loads = tuple(sum(w for j, w in enumerate(g.weights) if e in g.actions[j][s[j]])
                  for e in range(len(g.exponents)))
    values = tuple(load ** exponent for load, exponent in zip(loads, g.exponents))
    return tuple(sum(values[e] for e in g.actions[i][b]) for i, b in enumerate(s))


def integer_normal_form(g):
    """Expand L*a[e,k]/Q**k actual resources, then quotient equal actions."""
    Q = lcm(*(w.denominator for w in g.weights))
    scaled = tuple(tuple(a / Q ** k for k, a in enumerate(p)) for p in g.fees)
    L = lcm(*(a.denominator for p in scaled for a in p))
    weights = tuple(int(Q * w) for w in g.weights)
    require(all(F(w) == Q * old for w, old in zip(weights, g.weights)), "integer weights")
    exponents = []
    expansion = [[] for _ in g.fees]
    counts = []
    for e, polynomial in enumerate(scaled):
        row = []
        for k, a in enumerate(polynomial):
            multiplicity = L * a
            require(multiplicity.denominator == 1 and multiplicity >= 0, "integer multiplicity")
            m = int(multiplicity)
            row.append(m)
            for _ in range(m):
                expansion[e].append(len(exponents))
                exponents.append(k)
        counts.append(tuple(row))
    dummy = not exponents
    if dummy:
        # MODEL requires E nonempty; this resource is in no player's strategy.
        exponents.append(0)
    maps, actions = [], []
    for family in g.actions:
        new_family, action_map = [], []
        for old_action in family:
            new_action = frozenset(r for e in old_action for r in expansion[e])
            if new_action not in new_family:
                new_family.append(new_action)
            action_map.append(new_family.index(new_action))
        actions.append(tuple(new_family))
        maps.append(tuple(action_map))
    unit = UnitGame(weights, tuple(exponents), tuple(actions))
    require(all(len(set(f)) == len(f) and f for f in unit.actions), "quotient strategy families")
    require(all(isinstance(w, int) and w > 0 for w in unit.weights), "positive integer weights")
    require(bool(unit.exponents) and all(isinstance(k, int) and k >= 0 for k in unit.exponents),
            "nonempty list of monic resources")
    return unit, tuple(maps), Q, L, tuple(counts), dummy


def mapped_state(s, maps):
    return tuple(maps[i][b] for i, b in enumerate(s))


def is_pne(g, s, alpha, oracle):
    """Use the defining weak inequalities, including all zero-cost cases."""
    return all(oracle(g, s)[i] <= alpha * oracle(g, deviation(s, i, b))[i]
               for i, family in enumerate(g.actions) for b in range(len(family)))


def exact_threshold(g, oracle):
    """Finite fixture beta; None means a state has a positive-to-zero edge.

    No division is ever performed with zero denominator.  The return value is
    independently checked with weak PNE inequalities at and below the endpoint.
    """
    state_factors = []
    for s in states(g):
        factor = F(1)
        for i, family in enumerate(g.actions):
            current = oracle(g, s)[i]
            for b in range(len(family)):
                target = oracle(g, deviation(s, i, b))[i]
                if target == 0:
                    if current > 0:
                        factor = None
                        break
                else:
                    factor = max(factor, F(current) / target)
            if factor is None:
                break
        state_factors.append(factor)
    finite = [v for v in state_factors if v is not None]
    require(bool(finite), "these finite fixtures have a finite equilibrium threshold")
    beta = min(finite)
    endpoint_states = tuple(s for s in states(g) if is_pne(g, s, beta, oracle))
    require(bool(endpoint_states), "the weak beta endpoint is attained")
    require(all(is_pne(g, s, beta, oracle) == (v == beta)
                for s, v in zip(states(g), state_factors)), "beta characterizes endpoint states")
    if beta > 1:
        below = (beta + 1) / 2
        require(not any(is_pne(g, s, below, oracle) for s in states(g)), "strictly below beta")
    else:
        below = None
    return beta, endpoint_states, below


def raw_game(g):
    return {"weights": list(map(str, g.weights)), "fees": [list(map(str, p)) for p in g.fees],
            "strategies": [[sorted(a) for a in f] for f in g.actions]}


def audit_normal_form(name, g):
    unit, maps, Q, L, counts, dummy = integer_normal_form(g)
    ss, new_ss = states(g), states(unit)
    require({mapped_state(s, maps) for s in ss} == set(new_ss), "surjective state quotient")
    require(max(unit.exponents) <= max(len(p) - 1 for p in g.fees), "degree bound preserved")
    cost_checks = deviation_checks = positive_to_zero = zero_to_zero = constant_uses = 0
    for s in ss:
        image = mapped_state(s, maps)
        for i, family in enumerate(g.actions):
            require(literal_unit_costs(unit, image)[i] == L * original_costs(g, s)[i],
                    "mapped state cost identity")
            cost_checks += 1
            constant_uses += sum(k == 0 for e in family[s[i]] for k, a in enumerate(g.fees[e]) if a)
            for b in range(len(family)):
                t = deviation(s, i, b)
                target_image = deviation(image, i, maps[i][b])
                require(target_image == mapped_state(t, maps), "unilateral deviations commute")
                old_target = original_costs(g, t)[i]
                require(literal_unit_costs(unit, target_image)[i] == L * old_target,
                        "true-load deviation cost identity")
                positive_to_zero += old_target == 0 and original_costs(g, s)[i] > 0
                zero_to_zero += old_target == 0 and original_costs(g, s)[i] == 0
                deviation_checks += 1
    beta, endpoint, below = exact_threshold(g, original_costs)
    unit_beta, unit_endpoint, _ = exact_threshold(unit, literal_unit_costs)
    require(beta == unit_beta, "quotient preserves exact equilibrium threshold")
    require({mapped_state(s, maps) for s in endpoint} == set(unit_endpoint),
            "quotient preserves all endpoint equilibrium states")
    alphas = sorted({F(1), F(53, 50), F(3, 2), beta} | ({below} if below is not None else set()))
    inequality_checks = 0
    for alpha in alphas:
        for s in ss:
            require(is_pne(g, s, alpha, original_costs) ==
                    is_pne(unit, mapped_state(s, maps), alpha, literal_unit_costs),
                    "weak equilibrium inequalities preserved")
            inequality_checks += 1
    if dummy:
        require(unit.exponents == (0,), "one constant dummy in all-zero source")
        require(all(not a for family in unit.actions for a in family), "dummy remains unreferenced")
    return {"name": name, "source_game": raw_game(g), "Q": Q, "L": L,
            "resource_multiplicities_by_source_degree": counts,
            "unit_weights": unit.weights, "unit_resource_count": len(unit.exponents),
            "unit_exponents": unit.exponents,
            "unit_strategies": [[sorted(a) for a in f] for f in unit.actions],
            "original_action_index_to_quotient_index": maps,
            "source_states": len(ss), "quotient_states": len(new_ss),
            "source_actions": sum(map(len, g.actions)), "quotient_actions": sum(map(len, unit.actions)),
            "unreferenced_dummy": dummy, "state_player_cost_checks": cost_checks,
            "literal_deviation_cost_checks": deviation_checks,
            "positive_to_zero_deviations": positive_to_zero, "zero_to_zero_deviations": zero_to_zero,
            "nonzero_constant_term_player_state_uses": constant_uses,
            "weak_pne_equivalence_checks": inequality_checks, "checked_alphas": list(map(str, alphas)),
            "beta": str(beta), "beta_pne_states": endpoint,
            "below_beta_with_no_pne": str(below) if below is not None else None}, unit


def private_marker(unit, K):
    """K literal copies of every resource, plus one constant private marker/i."""
    require(isinstance(K, int) and K >= 1, "positive integer replication factor")
    old_e = len(unit.exponents)
    n = len(unit.weights)
    exponents = unit.exponents * K + (0,) * n
    actions = tuple(tuple(frozenset({e + copy * old_e for e in a for copy in range(K)}
                                   | {K * old_e + i}) for a in family)
                    for i, family in enumerate(unit.actions))
    result = UnitGame(unit.weights, exponents, actions)
    require(all(a for family in result.actions for a in family), "marker makes all actions nonempty")
    return result


def audit_marker_cost_identity(unit, K=2):
    """Test markers on zero, empty-action and degree-zero fixtures as well."""
    marked = private_marker(unit, K)
    checks = deviations = source_zero_costs = 0
    for i, family in enumerate(marked.actions):
        marker = K * len(unit.exponents) + i
        require(all(marker in a for a in family), "own marker occurs in every own action")
        require(all(marker not in a for j, other in enumerate(marked.actions) if j != i for a in other),
                "private marker never occurs in another player's action")
    for s in states(unit):
        for i, family in enumerate(unit.actions):
            old = literal_unit_costs(unit, s)[i]
            require(literal_unit_costs(marked, s)[i] == K * old + 1, "all-fixture marker state cost")
            source_zero_costs += old == 0
            checks += 1
            for b in range(len(family)):
                t = deviation(s, i, b)
                require(literal_unit_costs(marked, t)[i] == K * literal_unit_costs(unit, t)[i] + 1,
                        "all-fixture marker deviation cost")
                deviations += 1
    return {"K": K, "state_player_cost_checks": checks,
            "literal_deviation_cost_checks": deviations,
            "source_zero_costs_mapped_to_one": source_zero_costs}


def audit_marker(unit):
    beta, _, _ = exact_threshold(unit, literal_unit_costs)
    require(beta > 1, "actual no-PNE fixture needed for strict-margin preservation")
    # A close rational threshold forces nontrivial replication for this fixture.
    alpha = beta - (beta - 1) / 10000
    selector, margins = [], []
    for s in states(unit):
        candidates = [(F(literal_unit_costs(unit, s)[i]) -
                       alpha * literal_unit_costs(unit, deviation(s, i, b))[i], i, b)
                      for i, family in enumerate(unit.actions) for b in range(len(family))]
        margin, i, b = max(candidates)
        require(margin > 0, "a strict selected improvement at every source state")
        selector.append((i, b))
        margins.append(margin)
    delta = min(margins)
    K = int((alpha - 1) // delta) + 1
    require(K * delta > alpha - 1, "strict replication condition")
    marked = private_marker(unit, K)
    checks = deviations = 0
    selected = []
    for s, (i, b), margin in zip(states(unit), selector, margins):
        for j, family in enumerate(unit.actions):
            require(literal_unit_costs(marked, s)[j] == K * literal_unit_costs(unit, s)[j] + 1,
                    "literal marker state cost identity")
            checks += 1
            for a in range(len(family)):
                t = deviation(s, j, a)
                require(literal_unit_costs(marked, t)[j] == K * literal_unit_costs(unit, t)[j] + 1,
                        "literal marker deviation cost identity")
                deviations += 1
        t = deviation(s, i, b)
        actual = literal_unit_costs(marked, s)[i] - alpha * literal_unit_costs(marked, t)[i]
        require(actual == K * margin - (alpha - 1) and actual > 0,
                "strict selected margin survives private markers")
        selected.append({"state": s, "player": i, "target_action": b,
                         "source_margin": str(margin), "marked_margin": str(actual)})
    require(not any(is_pne(marked, s, alpha, literal_unit_costs) for s in states(marked)),
            "every marked state has a strict alpha-improvement")
    marked_beta, endpoint, _ = exact_threshold(marked, literal_unit_costs)
    require(alpha < marked_beta < beta, "marker threshold is finite and has its weak endpoint")
    # At equality the selected margin is zero, so the sufficient condition must
    # be strict; this algebra check does not claim nonexistence fails at equality.
    equality_margin = (alpha - 1) / K
    require(K * equality_margin - (alpha - 1) == 0, "strict-condition boundary")
    return {"source_beta": str(beta), "alpha": str(alpha), "K": K,
            "minimum_selected_source_margin": str(delta),
            "K_times_minimum_margin_minus_alpha_minus_one": str(K * delta - (alpha - 1)),
            "states": len(states(unit)), "marked_resource_count": len(marked.exponents),
            "state_player_cost_checks": checks, "literal_deviation_cost_checks": deviations,
            "selected_strict_allstate_witnesses": selected,
            "marked_beta": str(marked_beta), "marked_beta_pne_states": endpoint,
            "strict_condition_equality_margin": str(equality_margin),
            "strict_condition_equality_transformed_margin": "0"}


def generated_games():
    rng = random.Random(SEED)
    for case in range(16):
        n, e = rng.randint(1, 3), rng.randint(1, 4)
        weights = tuple(F(rng.randint(1, 7), rng.choice((1, 2, 3))) for _ in range(n))
        Q = lcm(*(w.denominator for w in weights))
        D, d = rng.choice((1, 2, 3)), rng.randint(0, 3)
        # Choosing a[e,k] = m*Q**k/D bounds the literal expansion size.
        fees = tuple(tuple(F(rng.randint(0, 3) * Q ** k, D) for k in range(d + 1))
                     for _ in range(e))
        subsets = tuple(frozenset(j for j in range(e) if mask >> j & 1) for mask in range(1 << e))
        actions = tuple(tuple(rng.sample(subsets, rng.randint(1, min(3, len(subsets)))))
                        for _ in range(n))
        yield "seeded_bounded_expansion_%02d" % case, Game(weights, fees, actions)


def audit(path):
    raw = json.loads(path.read_text())
    fixtures = [(item["name"], parse_game(item)) for item in raw["games"]]
    triad_name, triad = next((name, g) for name, g in fixtures
                            if name == "integer_triad_strict_allstate_primal")
    # Replacing w by w/2 and a[e,k] by 2**k*a[e,k]/3 divides
    # every old cost by 3, producing genuinely rational weights/coefficients.
    rational_triad = Game(tuple(w / 2 for w in triad.weights),
                          tuple(tuple(a * 2 ** k / 3 for k, a in enumerate(p)) for p in triad.fees),
                          triad.actions)
    scale_checks = 0
    for s in states(triad):
        for i in range(len(triad.weights)):
            require(3 * original_costs(rational_triad, s)[i] == original_costs(triad, s)[i],
                    "rational fixture is an exact cost-scaled real non-PNE fixture")
            scale_checks += 1
    require(not any(is_pne(rational_triad, s, F(53, 50), original_costs)
                    for s in states(rational_triad)), "actual rational no-53/50-PNE fixture")
    fixtures.append(("rational_cost_scaled_" + triad_name, rational_triad))
    # Distinct source actions collapse solely because zero resources disappear.
    fixtures.append(("zero_resource_action_quotient_and_constants", parse_game({
        "weights": ["2/3", "5/2"], "fees": [[0], ["1/3"], [0, "2/3"], [0]],
        "strategies": [[[], [0], [3], [0, 3], [1], [0, 1]], [[2], [0, 2], []]]})))
    # A degree-zero nonzero game tests multiple literal copies of constants.
    fixtures.append(("degree_zero_nonzero_constants", parse_game({
        "weights": ["1/7"], "fees": [["2/5"], ["3/10"], [0]],
        "strategies": [[[0], [1], [0, 1], [2], []]]})))
    fixtures.extend(generated_games())
    reports, rational_unit = [], None
    for name, g in fixtures:
        report, unit = audit_normal_form(name, g)
        report["marker_cost_identity"] = audit_marker_cost_identity(unit)
        reports.append(report)
        if name.startswith("rational_cost_scaled_"):
            rational_unit = unit
    require(rational_unit is not None, "rational non-PNE fixture retained")
    marker = audit_marker(rational_unit)
    totals = {key: sum(r[key] for r in reports) for key in (
        "source_states", "quotient_states", "state_player_cost_checks", "literal_deviation_cost_checks",
        "positive_to_zero_deviations", "zero_to_zero_deviations",
        "nonzero_constant_term_player_state_uses", "weak_pne_equivalence_checks")}
    totals["collapsed_actions"] = sum(r["source_actions"] - r["quotient_actions"] for r in reports)
    totals["all_zero_dummy_games"] = sum(r["unreferenced_dummy"] for r in reports)
    totals["marker_state_player_cost_checks"] = sum(
        r["marker_cost_identity"]["state_player_cost_checks"] for r in reports)
    totals["marker_literal_deviation_cost_checks"] = sum(
        r["marker_cost_identity"]["literal_deviation_cost_checks"] for r in reports)
    totals["marker_source_zero_costs_mapped_to_one"] = sum(
        r["marker_cost_identity"]["source_zero_costs_mapped_to_one"] for r in reports)
    require(totals["collapsed_actions"] > 0 and totals["all_zero_dummy_games"] > 0 and
            totals["positive_to_zero_deviations"] > 0 and totals["zero_to_zero_deviations"] > 0 and
            totals["nonzero_constant_term_player_state_uses"] > 0, "required boundary coverage is nonvacuous")
    return {"schema_version": 1, "status": "PASS", "arithmetic": "fractions.Fraction; exact integers; no tolerance",
            "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "python_version": sys.version.split()[0], "seed": SEED,
            "input": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
            "input_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "input_recipe": {
                "external": "all games in input JSON; triad identified by its existing name",
                "rational_triad": "w -> w/2; a[e,k] -> 2**k*a[e,k]/3; costs -> costs/3",
                "boundary": "explicit zero-resource quotient and degree-zero constant fixtures in source",
                "random": "16 games; Random(seed); n=1..3, E=1..4, d=0..3; "
                          "w=p/q, p=1..7, q in {1,2,3}; a[e,k]=m*Q**k/D, "
                          "m=0..3, D in {1,2,3}; 1..3 distinct subset actions/player",
                "marker": "alpha=beta-(beta-1)/10000; delta=min_s max_(i,b)(C_i-alpha*C_i_after); "
                          "K=floor((alpha-1)/delta)+1; K resource copies and private constant-1 markers"},
            "game_count": len(reports), "totals": totals,
            "rational_fixture_scaling_player_state_checks": scale_checks,
            "games": reports, "private_marker_audit": marker,
            "limitations": "Finite exhaustive implementation checks on the recorded rational fixtures only; "
                           "not a proof for arbitrary games or real parameters, and no uniform d/ln(d) conclusion. "
                           "The private-marker strict-margin criterion is checked with a real all-state non-PNE "
                           "fixture; the equality calculation alone makes no nonexistence claim."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = audit(args.input.resolve())
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        with args.output.open("x", encoding="utf-8") as stream:
            stream.write(payload)
    print(payload, end="")


if __name__ == "__main__":
    main()
