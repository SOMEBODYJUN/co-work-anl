"""Independent exact unit-client replay of the parent's priority diagnostics.

Non-blind review; no parent/model/verifier import. Not a half counterexample.
"""

from fractions import Fraction as F
from itertools import permutations, product
from pathlib import Path
import json


def utilities(actions, catalogue):
    values = [F(0) for _ in actions]
    universe = set().union(*catalogue)
    for client in universe:
        providers = [i for i, action in enumerate(actions)
                     if client in catalogue[action]]
        if providers:
            for i in providers:
                values[i] += F(1, len(providers))
    return tuple(values)


def allocation(actions, catalogue, order):
    values = [0 for _ in actions]
    for client in set().union(*catalogue):
        for i in order:
            if client in catalogue[actions[i]]:
                values[i] += 1
                break
    return tuple(values)


def verify(catalogue, population, policy):
    def complete(prefix):
        sequence = list(prefix)
        while len(sequence) < population:
            sequence.append(policy[tuple(sequence)])
        return tuple(sequence)

    rows = []
    for i in range(population):
        for prefix in product(range(len(catalogue)), repeat=i):
            obey = complete(prefix)
            obey_value = utilities(obey, catalogue)[i]
            for query in range(len(catalogue)):
                deviated = complete(prefix + (query,))
                difference = obey_value - utilities(deviated, catalogue)[i]
                assert difference >= 0
                rows.append({"history": prefix, "query": query,
                             "difference": str(difference)})
    orders = tuple(permutations(range(population)))
    for actions in product(range(len(catalogue)), repeat=population):
        means = tuple(sum((F(allocation(actions, catalogue, order)[i])
                           for order in orders), F(0)) / len(orders)
                      for i in range(population))
        assert means == utilities(actions, catalogue)
    return complete, rows


catalogue_one = (frozenset({"x"}), frozenset({"y", "z"}))
complete_one, rows_one = verify(catalogue_one, 2, {(): 0, (0,): 1, (1,): 1})
actual_one, deviation_one = complete_one(()), complete_one((1,))
gamma_one = utilities(actual_one, catalogue_one)[0] - utilities(deviation_one, catalogue_one)[0]
cases_one = []
for order in permutations(range(2)):
    lam = int(order[0] == 0)
    actual = allocation(actual_one, catalogue_one, order)[0]
    deviation = allocation(deviation_one, catalogue_one, order)[0]
    cases_one.append({"order": order, "lambda": lam,
                      "actual": actual, "deviation": deviation,
                      "difference": actual - deviation})
weighted_one = sum((F(v["lambda"] * v["difference"], 2) for v in cases_one), F(0))
weighted_deviation_one = sum((F(v["lambda"] * v["deviation"], 2) for v in cases_one), F(0))
assert gamma_one == 0 and weighted_one == F(-1, 2)
assert weighted_deviation_one == 1 == utilities(actual_one, catalogue_one)[0]


catalogue_two = (frozenset({"x", "y"}), frozenset({"z"}))
complete_two, rows_two = verify(catalogue_two, 2, {(): 0, (0,): 1, (1,): 0})
actual_two = complete_two(())
assert utilities(actual_two, catalogue_two) == (2, 1)
assert utilities((0, 0), catalogue_two)[1] == utilities((0, 1), catalogue_two)[1] == 1
cases_two = []
for order in permutations(range(2)):
    query = 0 if order[0] == 1 else 1
    coefficients = [int(query == a) for a in range(2)]
    assert sum(coefficients) == 1
    cases_two.append({"order": order, "query": query,
                      "coefficients": coefficients,
                      "selected_winner": allocation((0, query), catalogue_two, order)[1]})
selected_two = sum((F(v["selected_winner"], 2) for v in cases_two), F(0))
assert selected_two == F(3, 2)
envelopes_two = [max(v["coefficients"][a] for v in cases_two) for a in range(2)]
assert envelopes_two == [1, 1]


zero_catalogue = (frozenset(),)
zero_complete, zero_rows = verify(zero_catalogue, 2, {(): 0, (0,): 0})
assert utilities(zero_complete(()), zero_catalogue) == (0, 0)
one_catalogue = (frozenset(),) + catalogue_two
one_complete, one_rows = verify(one_catalogue, 1, {(): 1})
assert utilities(one_complete(()), one_catalogue) == (2,)
assert max(allocation((a,), one_catalogue, (0,))[0] for a in range(3)) == 2

report = {
    "status": "PASS",
    "scope": "full-history priority-selection diagnostics only; no fixed missed-source-flow or half counterexample",
    "root_conditioning": {
        "IC_rows": rows_one, "Gamma": str(gamma_one), "cases": cases_one,
        "weighted_difference": str(weighted_one),
        "full_wallet_deviation_payment": str(weighted_deviation_one),
        "W": 3, "OPT": 3,
    },
    "adaptive_last_query": {
        "IC_rows": rows_two, "cases": cases_two,
        "selected_expected_winner": str(selected_two),
        "actual_last_profit": "1", "minimal_deterministic_envelopes": envelopes_two,
        "W": 3, "OPT": 3,
    },
    "boundaries": {"zero_client_IC_count": len(zero_rows),
                   "one_player_IC_count": len(one_rows)},
}
Path(__file__).with_suffix(".json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
