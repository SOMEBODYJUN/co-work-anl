#!/usr/bin/env python3
"""Independent exact audit; no project or witness-verifier imports.

Reads only the game and strategy/security certificate. Enumerates the whole
ordered strategy tree, every ordered rival profile, and every coverage support.
All numerical assertions use fractions.Fraction, never an LP tolerance.
"""
from __future__ import annotations

from fractions import Fraction as F
import argparse
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def qstr(x):
    return str(x)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    opts = parser.parse_args()
    source_paths = {
        "input": ROOT / "examples/customer_attraction/local_security_increment.json",
        "certificate": ROOT / "evidence/certificates/customer_attraction/local_security_increment.json",
    }
    source = {k: json.loads(p.read_text()) for k, p in source_paths.items()}
    game, cert = source["input"], source["certificate"]
    n, m = game["players"], len(game["topics"])
    assert n == 3 and m == 6
    customers = []
    expanded = []
    for row in game["customers"]:
        liked = frozenset(row["topics"])
        count = row["multiplicity"]
        assert type(count) is int and count > 0
        assert liked and all(type(a) is int and 0 <= a < m for a in liked)
        customers.append((liked, count))
        expanded.extend([liked] * count)
    assert len(expanded) == 113

    actions = {}
    for row in cert["strategy"]["actions"]:
        h, a = tuple(row["history"]), row["action"]
        assert h not in actions and type(a) is int and 0 <= a < m
        actions[h] = a
    histories = [h for depth in range(n) for h in product(range(m), repeat=depth)]
    assert set(actions) == set(histories)
    # Check the compact rule stated in the current mathematical page too.
    for h in histories:
        expected = (0 if not h else 3 if len(h) == 1 and h[0] < 3
                    else 0 if len(h) == 1 else
                    min(a for a in (range(3) if h[-1] < 3 else range(3, 6)) if a not in h))
        assert actions[h] == expected
    assert len({tuple(i for i, liked in enumerate(expanded) if a in liked)
                for a in range(m)}) == m

    # Fixed strategy continuation is rebuilt directly in ordered histories.
    def terminal(h):
        while len(h) < n:
            h = h + (actions[h],)
        return h

    def payoff(a, final):
        ans = F(0)
        for liked, count in customers:
            if a in liked:
                denominator = sum(t in liked for t in final)
                assert denominator > 0
                ans += F(count, denominator)
        return ans

    def unit_payoff(a, final):
        return sum((F(1, sum(t in liked for t in final))
                    for liked in expanded if a in liked), F(0))

    comparisons, ties, negative = [], 0, []
    for h in histories:
        a = actions[h]
        final = terminal(h)
        actual = payoff(a, final)
        assert actual == unit_payoff(a, final)
        for alternative in range(m):
            deviation_final = terminal(h + (alternative,))
            deviation = payoff(alternative, deviation_final)
            assert deviation == unit_payoff(alternative, deviation_final)
            slack = actual - deviation
            ties += slack == 0
            row = {"history": list(h), "prescribed": a,
                   "alternative": alternative, "actual_terminal": list(final),
                   "deviation_terminal": list(deviation_final),
                   "actual_payoff": qstr(actual), "deviation_payoff": qstr(deviation),
                   "slack": qstr(slack)}
            comparisons.append(row)
            if slack < 0:
                negative.append(row)
    assert not negative
    path = terminal(())
    utilities = [payoff(a, path) for a in path]
    welfare = sum(count for liked, count in customers if liked.intersection(path))
    assert sum(utilities, F(0)) == welfare
    optimum = -1
    optimum_supports = []
    for size in range(min(n, m) + 1):
        for support in combinations(range(m), size):
            w = sum(count for liked, count in customers if liked.intersection(support))
            if w > optimum:
                optimum, optimum_supports = w, [list(support)]
            elif w == optimum:
                optimum_supports.append(list(support))
    assert tuple(path.count(a) for a in range(m)) == tuple(cert["strategy"]["terminal_counts"])

    def static_payoff(prefix, a, rivals):
        # One focal player plus fixed background and r-1 oblivious rivals.
        return payoff(a, tuple(prefix) + (a,) + tuple(rivals))

    def saddle(label, prefix, r, claim):
        value = F(claim["value"])
        primal = tuple(F(x) for x in claim["primary"])
        dual = tuple((tuple(row["rivals"]), F(row["probability"]))
                     for row in claim["dual"])
        assert len(primal) == m and sum(primal, F(0)) == 1
        assert all(p >= 0 for p in primal)
        assert sum(q for _, q in dual) == 1 and all(q >= 0 for _, q in dual)
        assert len({c for c, _ in dual}) == len(dual)
        assert all(len(c) == r-1 and all(0 <= a < m for a in c) for c, _ in dual)
        all_rivals = list(product(range(m), repeat=r-1))
        columns = []
        for c in all_rivals:
            entries = [static_payoff(prefix, a, c) for a in range(m)]
            expected = sum((p*x for p, x in zip(primal, entries)), F(0))
            assert expected >= value
            columns.append({"rivals": list(c), "matrix_column": list(map(qstr, entries)),
                            "primal_expected_payoff": qstr(expected),
                            "primal_slack": qstr(expected-value)})
        row_expectations = [sum((q*static_payoff(prefix, a, c) for c, q in dual), F(0))
                            for a in range(m)]
        assert all(x <= value for x in row_expectations)
        primal_min = min(F(row["primal_expected_payoff"]) for row in columns)
        dual_max = max(row_expectations)
        assert primal_min == value == dual_max
        # Feasibility bounds prove the exact value independently of a solver.
        assert all(not p or row_expectations[a] == value for a, p in enumerate(primal))
        assert all(not q or sum((primal[a]*static_payoff(prefix, a, c)
                                for a in range(m)), F(0)) == value for c, q in dual)
        return {"label": label, "fixed_prefix": list(prefix), "remaining_players": r,
                "value": qstr(value), "primal": list(map(qstr, primal)),
                "dual": [{"rivals": list(c), "probability": qstr(q)} for c, q in dual],
                "all_ordered_columns": columns,
                "primal_minimum": qstr(primal_min), "dual_maximum": qstr(dual_max),
                "dual_row_payoffs": list(map(qstr, row_expectations)),
                "primal_tight_ordered_columns": sum(F(x["primal_slack"]) == 0 for x in columns),
                "dual_tight_rows": sum(x == value for x in row_expectations)}

    global_check = saddle("root", (), n, cert["security_global"])
    local_claim = cert["security_after_root"]
    assert local_claim["fixed_prefix"] == [path[0]] and local_claim["remaining_players"] == n-1
    local_check = saddle("after_root", (path[0],), n-1, local_claim)
    # Last-player security has no opponents, so its pure maximum is explicit.
    last_immediate = [static_payoff(path[:-1], a, ()) for a in range(m)]
    last_value = max(last_immediate)
    assert last_value == utilities[-1]
    V = [F(global_check["value"]), F(local_check["value"]), last_value]
    assert all(V[i+1] >= V[i] for i in range(n-1))

    # Definition-level monotonicity is also checked at every possible prefix
    # and possible next action for this game, independently of the strategy.
    embeddings = 0
    for depth in range(n-1):
        r = n-depth
        for prefix in product(range(m), repeat=depth):
            for next_action in range(m):
                for rivals in product(range(m), repeat=r-2):
                    for focal in range(m):
                        assert static_payoff(prefix+(next_action,), focal, rivals) == \
                               static_payoff(prefix, focal, (next_action,)+rivals)
                        embeddings += 1

    root_value = V[0]
    full_terms = [utilities[i] - V[i] + (n-i-1)*(V[i+1]-V[i])
                  for i in range(n-1)] + [utilities[-1]-V[-1]]
    weak_terms = [utilities[i] + F(2*(n-i)-3, 2)*V[i+1]
                  - F(2*(n-i)-1, 2)*V[i] for i in range(n-1)]
    weak_terminal_slack = utilities[-1]-F(1, 2)*V[-1]
    assert sum(full_terms, F(0)) == welfare - n*root_value
    assert sum(weak_terms, F(0)) + weak_terminal_slack == welfare-F(2*n-1, 2)*root_value
    assert full_terms[0] < 0 and weak_terms[0] < 0
    assert welfare >= n*root_value
    assert welfare >= F(2*n-1, 2)*root_value
    assert 2*welfare >= optimum

    simple_p = tuple(F(x, 8) for x in (1, 1, 2, 1, 1, 2))
    simple_q = (((1,), F(3, 5)), ((2,), F(2, 5)))
    lower_columns = [sum((simple_p[a]*static_payoff((), a, c)
                          for a in range(m)), F(0))
                     for c in product(range(m), repeat=2)]
    upper_rows = [sum((q*static_payoff((0,), a, c) for c, q in simple_q), F(0))
                  for a in range(m)]
    lower, upper = min(lower_columns), max(upper_rows)
    assert lower == F(385, 12) and upper == F(484, 15)
    assert lower <= V[0] and V[1] <= upper
    full_upper = utilities[0]+2*upper-3*lower
    weak_upper = utilities[0]+F(3, 2)*upper-F(5, 2)*lower
    assert full_upper == -F(1, 20) and weak_upper == -F(17, 120)
    simple_bounds = {"root_primal": list(map(qstr, simple_p)),
                     "root_primal_all_ordered_column_values": list(map(qstr, lower_columns)),
                     "root_security_lower_bound": qstr(lower),
                     "local_dual": [{"rivals": list(c), "probability": qstr(q)} for c, q in simple_q],
                     "local_dual_all_row_values": list(map(qstr, upper_rows)),
                     "local_security_upper_bound": qstr(upper),
                     "full_first_increment_upper_bound": qstr(full_upper),
                     "weak_first_increment_upper_bound": qstr(weak_upper)}

    audit = {
        "claim_ids": ["CA-SECURITY-CHAIN-INTERFACE", "CA-LOCAL-SECURITY-INDUCTION-NO"],
        "status": "PASS", "method": "Independent Fraction checks; no project/witness-verifier imports",
        "source_sha256": {k: sha256(p.read_bytes()).hexdigest() for k, p in source_paths.items()},
        "n": n, "m": m, "customer_types": len(customers), "distinct_unit_clients": len(expanded),
        "decision_histories": len(histories), "terminal_histories": m**n,
        "all_action_comparisons": len(comparisons), "tied_comparisons": ties,
        "negative_comparisons": len(negative), "spe_comparisons": comparisons,
        "path": list(path), "utilities": list(map(qstr, utilities)),
        "welfare": welfare, "optimum": optimum, "optimum_supports": optimum_supports,
        "global_saddle": global_check, "local_saddle": local_check,
        "last_player_immediate_action_values": list(map(qstr, last_immediate)),
        "on_path_security_values": list(map(qstr, V)),
        "background_matrix_embedding_identities_checked": embeddings,
        "full_telescoping_terms": list(map(qstr, full_terms)),
        "full_bridge_margin": qstr(welfare-n*root_value),
        "weak_one_step_terms": list(map(qstr, weak_terms)),
        "weak_terminal_slack": qstr(weak_terminal_slack),
        "weak_bridge_margin": qstr(welfare-F(2*n-1, 2)*root_value),
        "doubled_half_coverage_margin_2W_minus_OPT": 2*welfare-optimum,
        "scope": "Disproves two universal local one-step inequalities; disproves no aggregate bridge or half-coverage bound",
        "mathematical_errors_in_witness": [],
        "simple_security_bounds": simple_bounds,
        "notation_issue": "Path-indexed V_n is last security; telescoping uses root V_1, also written v_n(0), not last V_n.",
    }
    if opts.output:
        opts.output.parent.mkdir(parents=True, exist_ok=True)
        with opts.output.open("x") as stream:
            stream.write(json.dumps(audit, indent=2)+"\n")
    print(json.dumps({k: audit[k] for k in ["status", "decision_histories", "all_action_comparisons",
                  "tied_comparisons", "path", "utilities", "welfare", "optimum",
                  "on_path_security_values", "full_telescoping_terms", "full_bridge_margin",
                  "weak_one_step_terms", "weak_terminal_slack", "weak_bridge_margin",
                  "doubled_half_coverage_margin_2W_minus_OPT"]}, indent=2))


if __name__ == "__main__":
    main()
