"""Independent unit-customer audit; reads only the author's explicit policy JSON."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
POLICY_PATH = HERE.parent / "five_budget" / "actual_tail_surplus_policy.json"
ALPHABET = "ABCX"
N = frozenset(range(13))
TOPICS = {
    "A": frozenset((0, 1, 2, 6, 7, 8, 9, 10, 11)),
    "B": frozenset((0, 1, 2, 7, 8, 9, 10, 11)),
    "C": frozenset((3, 4, 5, 6, 7, 8, 9, 10, 11)),
    "X": frozenset((0, 1, 2, 3, 4, 5, 6, 12)),
}


def load(profile):
    return tuple(sum(x in TOPICS[a] for a in profile) for x in N)


def query_payoff(action, rivals):
    rival_load = load(rivals)
    return sum((F(1, 1 + rival_load[x]) for x in TOPICS[action]), F())


def payoff(profile, position):
    occupancies = load(profile)
    return sum((F(1, occupancies[x]) for x in TOPICS[profile[position]]), F())


def potential(profile):
    return sum((sum((F(1, j) for j in range(1, count + 1)), F())
                for count in load(profile)), F())


raw_bytes = POLICY_PATH.read_bytes()
raw = json.loads(raw_bytes)
assert raw["players"] == 5 and raw["topics"] == list(ALPHABET)
assert raw["multiplicities"] == [3, 3, 1, 5, 1]
assert raw["membership"] == [
    [1, 1, 0, 1], [0, 0, 1, 1], [1, 0, 1, 1],
    [1, 1, 1, 0], [0, 0, 0, 1],
]
policy = raw["policy"]
histories = ["".join(h) for depth in range(5)
             for h in product(ALPHABET, repeat=depth)]
assert len(histories) == 341 and set(policy) == set(histories)
assert all(action in TOPICS for action in policy.values())


def continuation(history):
    while len(history) < 5:
        history += policy[history]
    return history


comparisons = 0
min_slack = None
for history in histories:
    position = len(history)
    actual = continuation(history)
    prescribed_payoff = payoff(actual, position)
    for action in ALPHABET:
        deviation = continuation(history + action)
        slack = prescribed_payoff - payoff(deviation, position)
        comparisons += 1
        assert slack >= 0, (history, action, actual, deviation, str(slack))
        min_slack = slack if min_slack is None else min(min_slack, slack)
assert comparisons == 1364

actual = continuation("")
assert actual == "XXCBC"
actual_u = [payoff(actual, i) for i in range(5)]
assert actual_u == [F(5, 2), F(5, 2), F(8, 3), F(8, 3), F(8, 3)]
actual_union = set().union(*(TOPICS[a] for a in actual))
assert actual_union == N
optimum = max(len(set().union(*(TOPICS[a] for a in profile)))
              for profile in product(ALPHABET, repeat=5))
assert optimum == len(N) == 13

prefix = actual[:3]
tail_potential_increments = {
    a + b: potential(prefix + a + b) - potential(prefix)
    for a, b in product(ALPHABET, repeat=2)
}
max_increment = max(tail_potential_increments.values())
assert max_increment == F(191, 30)
assert tail_potential_increments[actual[3:]] == F(37, 6)
gamma = max_increment - tail_potential_increments[actual[3:]]
assert gamma == F(1, 5)

local_matrix = {
    a: {b: query_payoff(a, prefix + b) for b in ALPHABET}
    for a in ALPHABET
}
local_w = F(157, 60)
assert min(local_matrix["A"].values()) == local_w
assert max(local_matrix[a]["A"] for a in ALPHABET) == local_w
tail_surplus = actual_u[3] + actual_u[4] - 2 * local_w
assert tail_surplus == F(1, 10) < gamma

# Check the supplied root static saddle certificate directly, without an LP.
root_v = F(202, 85)
primal = dict(zip(ALPHABET, (F(5, 17), F(), F(5, 17), F(7, 17))))
dual = [("ACXX", F(3, 17)), ("ACCX", F(7, 17)), ("AACX", F(7, 17))]
assert sum(primal.values()) == sum(prob for _, prob in dual) == 1
primal_values = [sum((primal[a] * query_payoff(a, rivals) for a in ALPHABET), F())
                 for rivals in product(ALPHABET, repeat=4)]
dual_values = {a: sum((prob * query_payoff(a, rivals) for rivals, prob in dual), F())
               for a in ALPHABET}
assert min(primal_values) == root_v
assert max(dual_values.values()) == root_v
early = sum(actual_u[:3], F())
assert early + gamma > 3 * root_v
assert early + gamma > F(23, 72) * optimum

report = {
    "review_status": "PASS",
    "independence": "Explicit 13 unit customers; only policy JSON read; no author solver imports or calls.",
    "policy_sha256": hashlib.sha256(raw_bytes).hexdigest(),
    "ordered_histories": len(histories),
    "SPE_comparisons_including_prescribed": comparisons,
    "minimum_slack": str(min_slack),
    "actual_profile": actual,
    "actual_payoffs": list(map(str, actual_u)),
    "W": len(actual_union),
    "OPT5": optimum,
    "prefix": prefix,
    "tail_potential_increments": {k: str(v) for k, v in tail_potential_increments.items()},
    "tail_potential_maximizers": [k for k, v in tail_potential_increments.items()
                                  if v == max_increment],
    "Gamma2": str(gamma),
    "local_payoff_matrix": {a: {b: str(v) for b, v in row.items()}
                            for a, row in local_matrix.items()},
    "local_w": str(local_w),
    "local_primal": "pure A",
    "local_dual": "pure A",
    "tail_surplus": str(tail_surplus),
    "root_v5": str(root_v),
    "root_primal_background_comparisons": len(primal_values),
    "root_dual_query_values": {a: str(v) for a, v in dual_values.items()},
    "early_plus_Gamma": str(early + gamma),
    "ONE_GAP_margin": str(early + gamma - 3 * root_v),
    "weak_payment_margin": str(early + gamma - F(23, 72) * optimum),
    "scope": "Refutes only Gamma2 <= (u4+u5)-2 v2(prefix); satisfies ONE-GAP, weak payment and half.",
}
output_path = HERE / "actual_tail_surplus_independent_audit.json"
output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({k: report[k] for k in (
    "review_status", "ordered_histories", "SPE_comparisons_including_prescribed",
    "actual_profile", "Gamma2", "local_w", "tail_surplus", "root_v5",
    "ONE_GAP_margin")}, ensure_ascii=False))
