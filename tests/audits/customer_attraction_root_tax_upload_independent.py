#!/usr/bin/env python3
"""Independent exact audit of the uploaded four-player root-tax instance.

No uploaded program and no repository solver are imported.  The only input
transcribed from the manuscript is the customer membership/count table.
Every customer is represented as a separate 0/1 incidence row.  All terminal
profiles are evaluated first; a policy table is then constructed backwards.
At a deviation we use the child node's precomputed continuation under that
same policy, rather than retaining any action from the original branch.

Run from any directory: python /.../uploaded_rt_review/independent_verify.py
The CSV/JSON audit records are written beside this source file.
"""

from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product, combinations_with_replacement
from pathlib import Path
import csv
import argparse
import hashlib
import json


LABELS = tuple("ABCDEF")
# Each copy below is a different unit customer; these are not weighted agents.
CUSTOMER_GROUPS = (
    ("A", 12), ("B", 8), ("C", 4), ("D", 8),
    ("AE", 6), ("AF", 6), ("CE", 3), ("CF", 3),
    ("AEF", 6), ("BEF", 2), ("CEF", 1), ("DEF", 2),
)


@dataclass(frozen=True)
class Game:
    labels: tuple
    customer_rows: tuple
    players: int
    priority: tuple

    def __post_init__(self):
        assert self.players >= 1
        assert self.labels and len(set(self.labels)) == len(self.labels)
        assert set(self.priority) == set(self.labels)
        assert len(self.priority) == len(self.labels)
        assert all(len(row) == len(self.labels) for row in self.customer_rows)
        assert all(x in (0, 1) for row in self.customer_rows for x in row)

    @property
    def actions(self):
        return tuple(range(len(self.labels)))

    def show(self, history):
        return "".join(self.labels[a] for a in history)

    def terminal_values(self, profile):
        assert len(profile) == self.players
        loads = tuple(sum(row[a] for a in profile) for row in self.customer_rows)
        utilities = tuple(
            sum((Q(row[a], load) for row, load in zip(self.customer_rows, loads)
                 if load), Q(0))
            for a in profile
        )
        covered = sum(load > 0 for load in loads)
        assert sum(utilities) == covered
        return utilities, covered


def make_game(labels, groups, players, priority):
    rows = []
    for membership, count in groups:
        assert isinstance(count, int) and count >= 0
        assert set(membership) <= set(labels)
        row = tuple(int(label in membership) for label in labels)
        rows.extend([row] * count)
    return Game(tuple(labels), tuple(rows), players, tuple(priority))


def evaluate(game, early_label="A"):
    """Evaluate the stated policy and compare every immediate-action deviation."""
    early = game.labels.index(early_label)
    rank = tuple(game.labels.index(a) for a in game.priority)
    terminal = {p: game.terminal_values(p)
                for p in product(game.actions, repeat=game.players)}
    continuation = {p: p for p in terminal}
    policy = {}
    last_records = []

    for depth in reversed(range(game.players)):
        for history in product(game.actions, repeat=depth):
            if depth == game.players - 1:
                values = tuple(terminal[history + (a,)][0][depth]
                               for a in game.actions)
                maximum = max(values)
                selected = next(a for a in rank if values[a] == maximum)
                last_records.append({
                    "history": game.show(history),
                    "action": game.labels[selected],
                    "best_actions": "".join(game.labels[a] for a in rank
                                            if values[a] == maximum),
                    **{game.labels[a]: str(values[a]) for a in game.actions},
                })
            else:
                selected = early
            policy[history] = selected
            continuation[history] = continuation[history + (selected,)]

    node_records, deviation_records, failures = [], [], []
    for depth in range(game.players):
        for history in product(game.actions, repeat=depth):
            chosen = policy[history]
            actual_profile = continuation[history]
            utility = terminal[actual_profile][0][depth]
            alternatives = {}
            for action in game.actions:
                deviating_profile = continuation[history + (action,)]
                alternative = terminal[deviating_profile][0][depth]
                alternatives[action] = alternative
                if action != chosen:
                    record = {
                        "history": game.show(history), "player": depth + 1,
                        "chosen": game.labels[chosen],
                        "alternative": game.labels[action],
                        "actual_outcome": game.show(actual_profile),
                        "deviation_outcome": game.show(deviating_profile),
                        "actual_payoff": str(utility),
                        "deviation_payoff": str(alternative),
                        "margin": str(utility - alternative),
                        "passes": alternative <= utility,
                    }
                    deviation_records.append(record)
                    if alternative > utility:
                        failures.append(record)
            node_records.append({
                "history": game.show(history), "player": depth + 1,
                "chosen": game.labels[chosen],
                "outcome": game.show(actual_profile),
                "chosen_payoff": str(utility),
                **{game.labels[a]: str(alternatives[a]) for a in game.actions},
            })

    outcome = continuation[()]
    utilities, welfare = terminal[outcome]
    optimum = max(w for _, w in terminal.values())
    prefix_loads = tuple(sum(row[a] for a in outcome[:-1])
                        for row in game.customer_rows)
    tax = sum((Q(b, b + 1) for b in prefix_loads), Q(0))
    return {
        "terminal": terminal, "policy": policy,
        "continuation": continuation, "last_records": last_records,
        "nodes": node_records, "deviations": deviation_records,
        "failures": failures, "outcome": outcome, "utilities": utilities,
        "welfare": welfare, "optimum": optimum, "tax": tax,
        "prefix_loads": prefix_loads,
    }


def write_csv(path, records):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    destination = args.output_dir
    destination.mkdir(parents=True, exist_ok=False)
    game = make_game(LABELS, CUSTOMER_GROUPS, 4, tuple("FEDCBA"))
    result = evaluate(game)
    claims = []

    def claim(name, observed, expected):
        passed = observed == expected
        claims.append({"claim": name, "observed": str(observed),
                       "expected": str(expected), "passes": passed})
        assert passed, (name, observed, expected)

    claim("unit customers", len(game.customer_rows), 61)
    claim("number of themes", len(game.labels), 6)
    sizes = tuple(sum(row[a] for row in game.customer_rows) for a in game.actions)
    claim("topic sizes A,B,C,D,E,F", sizes, (30, 10, 11, 10, 20, 20))
    claim("A,B,C,D form a customer partition",
          all(sum(row[:4]) == 1 for row in game.customer_rows), True)
    claim("pure SPE profitable deviations", len(result["failures"]), 0)
    claim("ordered nonterminal histories", len(result["nodes"]), 259)
    claim("nontrivial action deviations", len(result["deviations"]), 1295)
    claim("all terminal action profiles", len(result["terminal"]), 1296)

    # Independently recompute all 21 manuscript rows, including all six V values.
    claimed_pairs = {
        "AA": (Q(9), Q(9)), "AB": (Q(13), Q(11)),
        "AC": (Q(13), Q(10)), "AD": (Q(13), Q(11)),
        "AE": (Q(23, 2), Q(9)), "AF": (Q(23, 2), Q(9)),
        "BB": (Q(15), Q(38, 3)), "BC": (Q(15), Q(11)),
        "BD": (Q(15), Q(12)), "BE": (Q(13), Q(61, 6)),
        "BF": (Q(13), Q(61, 6)), "CC": (Q(15), Q(34, 3)),
        "CD": (Q(15), Q(11)), "CE": (Q(13), Q(9)),
        "CF": (Q(13), Q(9)), "DD": (Q(15), Q(38, 3)),
        "DE": (Q(13), Q(61, 6)), "DF": (Q(13), Q(61, 6)),
        "EE": (Q(12), Q(55, 6)), "EF": (Q(23, 2), Q(26, 3)),
        "FF": (Q(12), Q(55, 6)),
    }
    pair_records = []
    for p, q in combinations_with_replacement(game.actions, 2):
        values, replies = [], []
        for t in game.actions:
            history = (p, q, t)
            final_profile = result["continuation"][history]
            values.append(result["terminal"][final_profile][0][2])
            replies.append(game.labels[result["policy"][history]])
            swapped = result["continuation"][(q, p, t)]
            assert result["terminal"][swapped][0][2] == values[-1]
            assert result["policy"][(q, p, t)] == result["policy"][history]
        name = game.show((p, q))
        observed = (values[0], max(values[1:]))
        claim("comparison pair " + name, observed, claimed_pairs[name])
        pair_records.append({"pair": name,
                             **{game.labels[a]: str(values[a]) for a in game.actions},
                             "max_other": str(max(values[1:])),
                             "margin": str(values[0] - max(values[1:])),
                             "last_replies_for_ABCDEF": "".join(replies)})
    claim("unordered pairs including repetitions", len(pair_records), 21)
    claim("AA all six action values", tuple(Q(pair_records[0][a]) for a in LABELS),
          (Q(9),) * 6)

    last = {row["history"]: row for row in result["last_records"]}
    simple_reply = lambda h: ("A" if h.count("A") <= 1 else
                              "E" if "F" in h else "F")
    claim("exact simplified last response for all 216 histories",
          all(r["action"] == simple_reply(r["history"]) for r in result["last_records"]), True)
    claim("last response counts A,E,F",
          tuple(sum(r["action"] == a for r in result["last_records"])
                for a in ("A", "E", "F")), (200, 3, 13))
    claim("last rewards after AAA", tuple(Q(last["AAA"][a]) for a in LABELS),
          (Q(15, 2), Q(10), Q(11), Q(10), Q(11), Q(11)))
    claim("last chosen after AAA", last["AAA"]["action"], "F")
    claim("actual outcome", game.show(result["outcome"]), "AAAF")
    claim("actual utilities", result["utilities"], (Q(9), Q(9), Q(9), Q(11)))
    intersection = sum(row[0] and row[5] for row in game.customer_rows)
    a_only = sum(row[0] and not row[5] for row in game.customer_rows)
    f_only = sum(row[5] and not row[0] for row in game.customer_rows)
    claim("A intersection F", intersection, 12)
    claim("A minus F", a_only, 18)
    claim("F minus A", f_only, 8)
    claim("W", result["welfare"], 38)
    claim("OPT4", result["optimum"], 61)
    claim("prefix loads are 3 on A and 0 elsewhere", result["prefix_loads"],
          tuple(3 * row[0] for row in game.customer_rows))
    claim("root tax", result["tax"], Q(45, 2))
    claim("W plus tax", result["welfare"] + result["tax"], Q(121, 2))
    claim("RT violation", result["optimum"] - result["welfare"] - result["tax"],
          Q(1, 2))
    claim("uncovered customers", result["optimum"] - result["welfare"], 23)

    first_f = result["continuation"][(game.labels.index("F"),)]
    claim("first player deviation F continuation", game.show(first_f), "FAAE")
    claim("FAAE utilities", result["terminal"][first_f][0],
          (Q(9), Q(23, 2), Q(23, 2), Q(9)))
    claim("last rewards after FAA", tuple(Q(last["FAA"][a]) for a in LABELS),
          (Q(9), Q(9), Q(9), Q(9), Q(9), Q(7)))
    claim("last chosen after FAA", last["FAA"]["action"], "E")
    claim("six terms in V(F;A,A)",
          Q(3) + Q(6, 3) + Q(6, 4) + Q(2, 2) + Q(1, 2) + Q(2, 2), Q(9))

    f_b = tuple(sum((Q(row[a], b + 1)
                          for row, b in zip(game.customer_rows, result["prefix_loads"])),
                         Q(0)) for a in game.actions)
    claim("f_b of optimum partition", f_b[:4], (Q(15, 2), Q(10), Q(11), Q(10)))
    claim("sum optimum partition f_b", sum(f_b[:4]), Q(77, 2))
    claim("sum optimum partition f_b minus W", sum(f_b[:4]) - result["welfare"],
          Q(1, 2))
    last_payoff = result["utilities"][-1]
    claim("sum last-response slack", sum(last_payoff - value for value in f_b[:4]),
          Q(11, 2))
    claim("4u4 minus W", 4 * last_payoff - result["welfare"], Q(6))
    claim("4u4 plus tax", 4 * last_payoff + result["tax"], Q(133, 2))
    claim("(2-1/n)W", (Q(2) - Q(1, 4)) * result["welfare"], Q(133, 2))
    claim("2W", 2 * result["welfare"], 76)
    claim("OPT < (2-1/n)W < 2W",
          result["optimum"] < Q(7, 4) * result["welfare"] < 2 * result["welfare"], True)

    # Additional static maximin certificate supplied by the parent reviewer.
    # This recomputes all 56 opponent multisets from the customer incidence
    # matrix and verifies exact primal/dual inequalities without using an LP.
    probabilities = (Q(13, 45), Q(11, 45), Q(2, 9), Q(11, 45), Q(0), Q(0))
    claim("static safety mixture sums to one", sum(probabilities), Q(1))
    assert all(p >= 0 for p in probabilities)
    safety_records = []
    for competitors in combinations_with_replacement(game.actions, 3):
        load = tuple(sum(row[a] for a in competitors) for row in game.customer_rows)
        static_values = tuple(sum((Q(row[a], 1 + b)
                                   for row, b in zip(game.customer_rows, load)), Q(0))
                              for a in game.actions)
        mixture_value = sum(p * u for p, u in zip(probabilities, static_values))
        assert mixture_value >= 9, (competitors, mixture_value)
        safety_records.append({"opponent_multiset": game.show(competitors),
                               **{game.labels[a]: str(static_values[a])
                                  for a in game.actions},
                               "mixture_value": str(mixture_value),
                               "primal_margin": str(mixture_value - 9)})
    claim("static competitor multisets", len(safety_records), 56)
    claim("static primal minimum", min(Q(r["mixture_value"]) for r in safety_records), Q(9))
    dual = next(row for row in safety_records if row["opponent_multiset"] == "AAF")
    claim("static pure dual column AAF", tuple(Q(dual[a]) for a in LABELS),
          (Q(9), Q(9), Q(9), Q(9), Q(9), Q(7)))
    claim("static dual upper bound", max(Q(dual[a]) for a in LABELS), Q(9))
    claim("all realized players satisfy u_i >= static v4",
          all(u >= 9 for u in result["utilities"]), True)
    claim("aggregate static safety allowance", 4 * Q(9), Q(36))
    claim("W minus aggregate static safety allowance", Q(result["welfare"]) - 4 * Q(9), Q(2))

    # Boundary checks use the same independent engine, with no external solver.
    boundaries = []
    boundary_inputs = (
        ("one player, empty A, nonempty B", 1, ("A", "B"), (("B", 1),),
         ("B", 1, 1, Q(0))),
        ("four players, sole empty topic", 4, ("A",), (),
         ("AAAA", 0, 0, Q(0))),
        ("three players, equal coverage different labels", 3, ("A", "B"),
         (("AB", 1),), ("AAB", 1, 1, Q(2, 3))),
        ("two players, disjoint singleton topics", 2, ("A", "B"),
         (("A", 1), ("B", 1)), ("AB", 2, 2, Q(1, 2))),
        ("one player, all empty labels", 1, ("A", "B"), (),
         ("B", 0, 0, Q(0))),
    )
    for name, n, labels, groups, expected in boundary_inputs:
        edge = make_game(labels, groups, n, tuple(reversed(labels)))
        checked = evaluate(edge)
        observed = (edge.show(checked["outcome"]), checked["welfare"],
                    checked["optimum"], checked["tax"])
        claim("boundary " + name, observed, expected)
        assert not checked["failures"]
        boundaries.append({"name": name, "outcome": observed[0],
                           "W": observed[1], "OPT": observed[2],
                           "tau": str(observed[3]), "pure_SPE": True})
    # A negative control: on four providers/two disjoint customers the same
    # early-A policy is not an SPE, so the checker must find actual profitable
    # deviations (it cannot simply certify every constant early-action policy).
    negative_game = make_game(("A", "B"), (("A", 1), ("B", 1)), 4, ("B", "A"))
    negative = evaluate(negative_game)
    assert negative["failures"]
    assert any(row["history"] == "" and row["alternative"] == "B"
               and row["actual_payoff"] == "1/3"
               and row["deviation_payoff"] == "1/2"
               for row in negative["failures"])

    write_csv(destination / "all_nodes.csv", result["nodes"])
    write_csv(destination / "all_deviations.csv", result["deviations"])
    write_csv(destination / "last_replies.csv", sorted(result["last_records"],
                                                       key=lambda row: row["history"]))
    write_csv(destination / "comparison_21_pairs.csv", pair_records)
    write_csv(destination / "numeric_claims.csv", claims)
    write_csv(destination / "static_safety_56_multisets.csv", safety_records)
    source = Path(__file__).resolve().parents[2] / "history/source/notes/customer_attraction/uploaded_pro_2026-10-10/root_tax_source.md"
    source_digest = hashlib.sha256(source.read_bytes()).hexdigest() if source.exists() else None
    # No uploaded source code is executed: reading the uploaded document here
    # only produces its audit identifier.
    summary = {
        "verdict": "PASS", "independent": True,
        "uploaded_document_sha256": source_digest,
        "audit_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "input_groups": dict(CUSTOMER_GROUPS),
        "customer_count": len(game.customer_rows), "topic_sizes": dict(zip(LABELS, sizes)),
        "policy": {"first_three": "A at every ordered history",
                   "last": "true best reply at every three-action ordered history",
                   "last_tie_priority": "F>E>D>C>B>A",
                   "equivalent_last_rule": "A if count(A)<=1; otherwise E if F present, else F",
                   "last_response_counts": {a: sum(r["action"] == a for r in result["last_records"])
                                            for a in ("A", "E", "F")}},
        "outcome": game.show(result["outcome"]),
        "utilities": [str(u) for u in result["utilities"]],
        "W": result["welfare"], "OPT4": result["optimum"],
        "tau": str(result["tax"]), "RT_gap": "1/2",
        "terminal_profiles": len(result["terminal"]),
        "nodes": len(result["nodes"]), "deviations": len(result["deviations"]),
        "profitable_deviations": len(result["failures"]),
        "nodes_by_player": [sum(r["player"] == i for r in result["nodes"])
                            for i in range(1, 5)],
        "deviations_by_player": [sum(r["player"] == i for r in result["deviations"])
                                 for i in range(1, 5)],
        "equal_payoff_deviations_by_player": [
            sum(r["player"] == i and Q(r["margin"]) == 0 for r in result["deviations"])
            for i in range(1, 5)],
        "min_margin_by_player": [str(min(Q(r["margin"]) for r in result["deviations"]
                                            if r["player"] == i)) for i in range(1, 5)],
        "numeric_claims_checked": len(claims), "all_numeric_claims_pass": True,
        "static_safety": {
            "v4": "9", "p": [str(p) for p in probabilities],
            "opponent_multisets_checked": len(safety_records),
            "dual_opponents": "AAF", "dual_column": [dual[a] for a in LABELS],
            "binding_primal_multisets": [r["opponent_multiset"] for r in safety_records
                                         if Q(r["primal_margin"]) == 0],
            "realized_u_i_ge_v4": True, "4v4": "36", "W_minus_4v4": "2",
            "scope": "Numerical compatibility for this instance; no claim of a universal bridge."
        },
        "boundaries": boundaries,
        "negative_control_profitable_deviations": negative["failures"],
        "note": "Strict RT violation; the SPE itself uses weak best responses.",
    }
    (destination / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False)
                                               + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
