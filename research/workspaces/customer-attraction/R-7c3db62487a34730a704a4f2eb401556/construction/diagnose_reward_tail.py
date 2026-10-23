"""One targeted finite diagnosis of the arbitrary-r reward-tail candidate.

This solves only the three-responder subgame following C0,C1,C2,A3.
It does not certify a full seven-player SPE or scan parameter grids.
"""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import json

from customer_attraction.model import CustomerType, Instance
from customer_attraction.exact import ExactSPESolver


def run() -> dict:
    k, r, x, a, b, d = 4, 3, 2, 2, 6, 3
    names = tuple(z for i in range(k)
                  for z in (f"C{i}", f"A{i}", f"B{i}")) + ("D",)
    customers = []
    for i in range(k):
        customers.extend((
            CustomerType(frozenset((3*i, 3*i+1, 3*i+2)), x),
            CustomerType(frozenset((3*i+1,)), a),
        ))
    customers.extend((
        CustomerType(frozenset([3*i+2 for i in range(k)] + [3*k]), b),
        CustomerType(frozenset((3*k,)), d),
    ))
    instance = Instance(names, tuple(customers), k+r)
    solver = ExactSPESolver(instance)
    prefix = tuple(3*i for i in range(k-1)) + (3*(k-1)+1,)
    prefix_counts = instance.counts(prefix)
    anchor = 3*(k-1)+1
    outcomes = solver.outcomes(prefix_counts)
    minimum = min(instance.topic_payoff(anchor, q) for q in outcomes)
    target = min(q for q in outcomes if instance.topic_payoff(anchor, q) == minimum)
    strategy = {}

    def increment(counts, action):
        return tuple(v + (j == action) for j, v in enumerate(counts))

    def expand(history, counts, desired):
        if len(history) == instance.players:
            assert counts == desired
            return
        floor = solver.threshold(counts)
        candidates = [j for j in range(instance.topic_count)
                      if desired in solver.outcomes(increment(counts, j))
                      and instance.topic_payoff(j, desired) >= floor]
        chosen = candidates[0]
        strategy[history] = chosen
        for action in range(instance.topic_count):
            child_counts = increment(counts, action)
            child_outcomes = solver.outcomes(child_counts)
            child_target = desired if action == chosen else min(
                child_outcomes, key=lambda q: (instance.topic_payoff(action, q), q))
            expand(history + (action,), child_counts, child_target)

    expand(prefix, prefix_counts, target)

    # Rebuild actual, distinct unit clients. Verification below uses only these
    # sets and the complete ordered-history strategy, not compressed utilities.
    unit_topics = [set() for _ in names]
    client_id = 0
    for client_type in customers:
        for _ in range(client_type.multiplicity):
            for topic in client_type.topics:
                unit_topics[topic].add(client_id)
            client_id += 1

    def follow(history):
        while len(history) < instance.players:
            history += (strategy[history],)
        return history

    def unit_payoff(history, player):
        loads = [sum(c in unit_topics[j] for j in history)
                 for c in range(client_id)]
        return sum((Fraction(1, loads[c]) for c in unit_topics[history[player]]), Fraction())

    minimum_slack = None
    comparisons = 0
    for history, chosen in strategy.items():
        player = len(history)
        actual_utility = unit_payoff(follow(history), player)
        for alternative in range(instance.topic_count):
            alternative_utility = unit_payoff(follow(history + (alternative,)), player)
            slack = actual_utility - alternative_utility
            assert slack >= 0, (history, chosen, alternative, slack)
            minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)
            comparisons += 1
    actual = follow(prefix)
    assert unit_payoff(actual, len(prefix)-1) == minimum == Fraction(3)
    assert minimum > x
    assert len(strategy) == 1 + instance.topic_count + instance.topic_count**2
    return {
        "status": "finite subgame diagnostic; no full-game SPE asserted",
        "parameters": dict(k=k, r=r, x=x, a=a, b=b, d=d),
        "instance": instance.to_dict(),
        "fixed_ordered_prefix": [names[j] for j in prefix],
        "suffix_spe_outcome_count": len(outcomes),
        "anchor_payoff_minimum": str(minimum),
        "anchor_payoff_maximum": str(max(instance.topic_payoff(anchor, q) for q in outcomes)),
        "actual_C_payoff_in_candidate": str(x),
        "solver_stats": solver.stats.__dict__,
        "suffix_outcomes": [{"added_counts": {names[j]: q[j]-prefix_counts[j]
                                               for j in range(instance.topic_count)
                                               if q[j] > prefix_counts[j]},
                             "anchor_payoff": str(instance.topic_payoff(anchor, q))}
                            for q in sorted(outcomes)],
        "audited_full_suffix_strategy": [
            {"history": [names[j] for j in history], "action": names[action]}
            for history, action in sorted(strategy.items())],
        "independent_unit_replay": {
            "ordered_decision_nodes": len(strategy),
            "comparisons_including_self": comparisons,
            "proper_deviations": comparisons-len(strategy),
            "minimum_slack": str(minimum_slack),
            "realized_path": [names[j] for j in actual],
            "realized_player_payoffs": [str(unit_payoff(actual, i))
                                        for i in range(instance.players)],
        },
    }


if __name__ == "__main__":
    result = run()
    destination = Path(__file__).with_name("reward_tail_diagnostic.json")
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({k: result[k] for k in (
        "status", "parameters", "suffix_spe_outcome_count", "anchor_payoff_minimum",
        "solver_stats", "independent_unit_replay")}, ensure_ascii=False, indent=2))
