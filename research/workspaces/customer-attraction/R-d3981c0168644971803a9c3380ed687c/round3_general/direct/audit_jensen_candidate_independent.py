"""Unit-customer audit of one supplied all-p Jensen candidate.

No author module, repository game model, verifier, SPE enumerator, NumPy or LP
solver is imported.  Only the raw finite input, full ordered-history policy and
query distribution are read.  This script does not search for another instance.
"""

from fractions import Fraction
from functools import lru_cache
from itertools import product
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
RAW = HERE.parent / "equilibrium" / "fractional_global_raw.json"
OUT = HERE / "jensen_candidate_independent_audit.json"


def show(q):
    return str(q)


data = json.loads(RAW.read_text())
m = data["players"]
k = len(data["topics"])
assert m == 3 and k == 6
entries = data["policy"]
policy = {tuple(e["history"]): e["action"] for e in entries}
assert len(policy) == len(entries)
expected_histories = {
    h for depth in range(m) for h in product(range(k), repeat=depth)
}
assert set(policy) == expected_histories
assert all(0 <= a < k for a in policy.values())

# Expand integer multiplicities to different unit customers.  All subsequent
# welfare, utility, IC, load and Jensen computations iterate over these units.
clients = []
for mask_text, count in data["customer_mask_multiplicities"].items():
    mask = int(mask_text)
    assert 0 < mask < 1 << k
    assert isinstance(count, int) and count >= 0
    interest = frozenset(a for a in range(k) if mask & (1 << a))
    for copy_number in range(count):
        clients.append(interest)
assert len(clients) == 817
topics = [frozenset(x for x, likes in enumerate(clients) if a in likes)
          for a in range(k)]
assert len(set(topics)) == k

p = tuple(Fraction(q) for q in data["p"])
assert len(p) == k and all(q >= 0 for q in p) and sum(p) == 1
support = [a for a in range(k) if p[a]]
px = [sum((p[a] for a in likes), Fraction()) for likes in clients]
assert all(0 <= q <= 1 for q in px)


@lru_cache(None)
def finish(history):
    history = tuple(history)
    while len(history) < m:
        history += (policy[history],)
    return history


@lru_cache(None)
def loads(sequence):
    return tuple(sum(a in likes for a in sequence) for likes in clients)


@lru_cache(None)
def utility(terminal, actor):
    a = terminal[actor]
    customer_load = loads(terminal)
    assert all(0 <= c <= m for c in customer_load)
    return sum((Fraction(1, customer_load[x]) for x in topics[a]), Fraction())


strict = ties = 0
minimum_slack = None
ic_rows = []
for h in sorted(expected_histories, key=lambda t: (len(t), t)):
    i = len(h)
    prescribed = finish(h)
    value = utility(prescribed, i)
    for a in range(k):
        deviated = finish(h + (a,))
        other_value = utility(deviated, i)
        slack = value - other_value
        assert slack >= 0, (h, a, value, other_value)
        strict += slack > 0
        ties += slack == 0
        minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)
        ic_rows.append({"history": h, "query": a,
                        "prescribed_terminal": prescribed,
                        "deviated_terminal": deviated,
                        "slack": show(slack)})

z = finish(())
actual_loads = loads(z)
W = sum(c > 0 for c in actual_loads)
actual_utilities = [utility(z, i) for i in range(m)]
assert sum(actual_utilities) == W
assert z == tuple(data["claimed_path"])
assert Fraction(W) == Fraction(data["claimed_welfare"])

# Directly enumerate only the finite comparison tuples for this supplied input;
# this is an exact OPT check, not an equilibrium enumeration or input search.
opt = 0
optimal_examples = []
for terminal in product(range(k), repeat=m):
    welfare = sum(c > 0 for c in loads(terminal))
    if welfare > opt:
        opt, optimal_examples = welfare, [terminal]
    elif welfare == opt:
        optimal_examples.append(terminal)

positions = []
F_values = []
C_values = []
for i in range(m):
    forced = {a: finish(z[:i] + (a,)) for a in support}
    # Remove the queried actor, retaining both the fixed earlier actors and all
    # true original-policy followers.  The remaining sequence always has m-1
    # elements, even when the same theme appears more than once.
    competitors = {a: y[:i] + y[i + 1:] for a, y in forced.items()}
    assert all(len(y) == m - 1 for y in competitors.values())
    mus = [sum((p[a] * loads(competitors[a])[x] for a in support), Fraction())
           for x in range(len(clients))]
    assert all(0 <= mu <= m - 1 for mu in mus)
    denoms = [1 + mu for mu in mus]
    assert all(1 <= d <= m for d in denoms)
    F = sum((px[x] / denoms[x] for x in range(len(clients))), Fraction())
    C = sum((p[a] * sum((px[x] / (1 + loads(competitors[a])[x])
                        for x in range(len(clients))), Fraction())
             for a in support), Fraction())
    D = sum((p[a] * utility(forced[a], i) for a in support), Fraction())
    assert F <= C
    assert D <= actual_utilities[i]
    F_values.append(F)
    C_values.append(C)
    # Store one row per original type only to keep the exact audit readable;
    # the calculations above used every different unit customer.
    type_rows = []
    offset = 0
    for mask_text, count in data["customer_mask_multiplicities"].items():
        if not count:
            continue
        x = offset
        type_rows.append({"mask": int(mask_text), "multiplicity": count,
                          "p_x": show(px[x]), "mu": show(mus[x]),
                          "denominator": show(denoms[x]),
                          "F_per_unit": show(px[x] / denoms[x])})
        offset += count
    assert offset == len(clients)
    positions.append({"position_zero_based": i,
                      "actual_prefix": z[:i],
                      "forced_terminals": {str(a): forced[a] for a in support},
                      "competitor_sequences": {str(a): competitors[a] for a in support},
                      "F": show(F), "C": show(C), "D": show(D),
                      "IC_slack_to_D": show(actual_utilities[i] - D),
                      "Jensen_gap_C_minus_F": show(C - F),
                      "mu_values": sorted(set(map(show, mus))),
                      "type_rows": type_rows})

excess = sum(F_values) - W
assert excess == Fraction(data["claimed_fractional_sum_minus_welfare"])
assert excess > 0

# Independently check one supplied simple static dual competitor.  A fixed
# two-theme competitor is a valid upper bound for the genuine static maximin
# security value; no claim that the bad p is an optimizer is needed.
static_competitor = (0, 2)
static_load = loads(static_competitor)
static_query_utilities = [sum((Fraction(1, 1 + static_load[x])
                               for x in topics[a]), Fraction()) for a in range(k)]
static_cap = max(static_query_utilities)
assert m * static_cap <= W

# q=(e_0+e_2)/2 induces exactly the same fractional load as this static
# competitor.  It supplies an upper bound for the bad p's fractional dual
# objective.  The universal coverage comparison gives delta_m>=OPT/(2m-1).
# Their strict separation certifies that this p is not a delta-dual optimizer.
bad_p_delta_dual_upper = sum((p[a] * static_query_utilities[a]
                              for a in range(k)), Fraction())
delta_lower = Fraction(opt, 2 * m - 1)
assert bad_p_delta_dual_upper < delta_lower

result = {
    "input": str(RAW), "method": "expanded different unit customers; stdlib Fraction only",
    "customers": len(clients), "distinct_topics": k, "players": m,
    "ordered_histories": len(policy), "IC_comparisons_including_self": len(ic_rows),
    "strict_IC": strict, "tie_IC": ties, "minimum_IC_slack": show(minimum_slack),
    "complete_SPE": True, "path": z, "topic_sizes": list(map(len, topics)),
    "actual_utilities": list(map(show, actual_utilities)), "welfare": W,
    "optimum": opt, "one_optimal_tuple": optimal_examples[0],
    "half_margin_2W_minus_OPT": 2 * W - opt,
    "query_distribution": list(map(show, p)), "positions": positions,
    "F_sum": show(sum(F_values)), "F_sum_minus_W": show(excess),
    "C_sum": show(sum(C_values)),
    "static_competitor": static_competitor,
    "static_query_utilities": list(map(show, static_query_utilities)),
    "static_security_cap": show(static_cap),
    "aggregate_security_margin_lower_bound_W_minus_m_cap": show(W - m * static_cap),
    "bad_p_delta_dual_upper_bound": show(bad_p_delta_dual_upper),
    "delta_lower_bound_OPT_over_2m_minus_1": show(delta_lower),
    "bad_p_is_not_delta_dual_optimizer": True,
    "strict_delta_optimality_gap_lower_bound": show(delta_lower - bad_p_delta_dual_upper),
    "claim_refuted": "For every input/SPE and every legal p, sum_i F_i(p) <= W",
    "not_established": ["Failure for an optimal p", "Failure of an existence-of-good-p statement",
                        "Failure of genuine static aggregate safety", "Failure of Q-CAG-HALF"],
    "all_IC_rows": ic_rows,
}
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({key: result[key] for key in (
    "customers", "ordered_histories", "IC_comparisons_including_self", "strict_IC", "tie_IC",
    "path", "actual_utilities", "welfare", "optimum", "half_margin_2W_minus_OPT",
    "F_sum", "F_sum_minus_W", "static_query_utilities", "static_security_cap")},
    ensure_ascii=False, indent=2))
