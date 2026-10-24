"""Independent unit-customer audit of the MIN-PI witness.

Only the instance bitmasks and complete strategy are read from the packet.
No optimizer, discovery code, exact SPE oracle, or canonical verifier is imported.
Integer scales 6 (utilities) and 12 (H_0 through H_4) keep all loops exact.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent / "parent/min_increment_counterexample.json"
packet = json.loads(PACKET.read_text())
actions = {tuple(v["history"]): v["action"] for v in packet["strategy"]["actions"]}
m = max(map(len, actions)) + 1
k = max(a for h, chosen in actions.items() for a in h + (chosen,)) + 1
assert (m, k) == (3, 6)
assert len(actions) == len(packet["strategy"]["actions"])
units = []
for mask_text, weight in packet["integer_weights"].items():
    mask = int(mask_text)
    assert 0 < mask < 1 << k and isinstance(weight, int) and weight > 0
    units.extend([mask] * weight)
units = tuple(units)  # Each position is a different unit customer.
expected_histories = {h for d in range(m) for h in product(range(k), repeat=d)}
assert set(actions) == expected_histories
assert all(0 <= a < k for a in actions.values())
topic_customers = [frozenset(x for x, mask in enumerate(units) if mask >> a & 1) for a in range(k)]
assert len(set(topic_customers)) == k

@lru_cache(None)
def completion(h):
    return h if len(h) == m else completion(h + (actions[h],))

def counts(z):
    return tuple(z.count(a) for a in range(k))

@lru_cache(None)
def unit_scores(q):
    # Individual copies are explicitly summed; mask arithmetic just supplies
    # each copy's interested topics and its terminal congestion.
    utility_six = [0] * k
    covered = 0
    h12 = (0, 12, 18, 22, 25)
    potential_twelve = 0
    loads = [sum(q[a] for a in range(k) if mask >> a & 1) for mask in range(1 << k)]
    for mask in units:
        c = loads[mask]
        if c:
            covered += 1
            potential_twelve += h12[c]
            if sum(q) == m:
                assert 6 % c == 0
                for a in range(k):
                    if mask >> a & 1:
                        utility_six[a] += 6 // c
    return tuple(utility_six), covered, potential_twelve

slacks = []
for h in sorted(expected_histories, key=lambda v: (len(v), v)):
    chosen = actions[h]
    current = unit_scores(counts(completion(h)))[0][chosen]
    for a in range(k):
        alternative = unit_scores(counts(completion(h + (a,))))[0][a]
        slacks.append(current - alternative)
assert min(slacks) >= 0
actual = completion(())
assert counts(actual) == tuple(packet["strategy"]["terminal_counts"])
actual_scores, actual_welfare, actual_potential_twelve = unit_scores(counts(actual))
payoffs = tuple(F(actual_scores[a], 6) for a in actual)
assert sum(payoffs) == actual_welfare

def compositions(n, d):
    if d == 1:
        yield (n,)
    else:
        for a in range(n + 1):
            for tail in compositions(n - a, d - 1):
                yield (a,) + tail

potentials, maximizers, profile_counts = {}, {}, {}
opt = 0
for n in range(m + 2):
    profiles = tuple(compositions(n, k))
    scored = [(F(unit_scores(q)[2], 12), q) for q in profiles]
    value = max(v for v, _ in scored)
    potentials[n] = value
    maximizers[n] = [q for v, q in scored if v == value]
    profile_counts[n] = len(profiles)
    if n == m:
        opt = max(unit_scores(q)[1] for q in profiles)
increments = tuple(potentials[n] - potentials[n - 1] for n in range(1, m + 2))
root = payoffs[0]
minimum_gap = min(increments) - root
assert minimum_gap > 0
assert all(increments[j] >= increments[j + 1] for j in range(len(increments) - 1))
assert len(units) == 15748
assert actual == (0, 3, 4)
assert payoffs == (F(3481), F(3709), F(3481))
assert actual_welfare == 10671 and opt == 12546
assert potentials == {0: F(0), 1: F(6013), 2: F(20275, 2), 3: F(27693, 2), 4: F(35111, 2)}
assert minimum_gap == 228

# A pure three-slot background already gives an upper bound below the root
# on genuine v_4, with no mixed optimization required for this scope check.
def query_score(a, q):
    loads = [sum(q[b] for b in range(k) if mask >> b & 1) for mask in range(1 << k)]
    return F(sum(12 // (1 + loads[mask]) for mask in units if mask >> a & 1), 12)
pure_caps = [(max(query_score(a, q) for a in range(k)), q) for q in compositions(m, k)]
theta, theta_background = min(pure_caps)

answer = {
    "status": "Independent exact unit audit passed; MIN-PI only.",
    "read_only_packet_fields": ["integer_weights", "strategy"],
    "imports_discovery_optimizer_or_SPE_oracle": False,
    "players": m, "topics": k, "unit_customers": len(units),
    "distinct_coverage_topics": len(set(topic_customers)) == k,
    "complete_ordered_histories": len(expected_histories),
    "comparisons_including_self": len(slacks), "minimum_IC_slack": str(F(min(slacks), 6)),
    "actual": actual, "actual_payoffs": list(map(str, payoffs)),
    "actual_welfare": actual_welfare, "OPT_m": opt,
    "actual_harmonic_potential": str(F(actual_potential_twelve, 12)),
    "potentials": {str(n): str(v) for n, v in potentials.items()},
    "potential_profile_counts": profile_counts,
    "all_potential_maximizers": maximizers,
    "increments": list(map(str, increments)),
    "increments_nonincreasing_through_r_plus_1": True,
    "minimum_increment_minus_root": str(minimum_gap),
    "two_W_minus_OPT": 2 * actual_welfare - opt,
    "pure_theta_r_plus_1": str(theta), "theta_background": theta_background,
    "theta_below_root": theta < root,
    "scope_caveat": "Concavity checked only for the required finite window P_0,...,P_(r+1); no infinite-population concavity claim.",
}
(HERE / "min_pi_independent_audit.json").write_text(json.dumps(answer, indent=2) + "\n")
print(json.dumps(answer, indent=2))
