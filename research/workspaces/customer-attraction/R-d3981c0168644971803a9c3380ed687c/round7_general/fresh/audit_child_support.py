"""Independent finite Fraction QA, not an SPE or half proof.

Proofs and non-blind review scope: child_support_independent_review.md.
No author/solver/model imports. The old13 packet is read only for actual-path
arithmetic; its complete SPE identity is inherited from its existing audit.
"""

from fractions import Fraction as F
from pathlib import Path
from collections import Counter
import gzip
import hashlib
import json


def f(b, d):
    return F(d, b + d) if d else F(0)


def lam(b, c, k):
    p = F(1, b + c + 1)
    return max(f(b, d) - d * p for d in range(k + 1))


support_checks = 0
for b in range(9):
    for c in range(9):
        for k in range(1, 13):
            value = lam(b, c, k)
            assert 0 <= value <= F(c, b + c + 1)
            for d in range(k + 1):
                assert f(b, d) <= F(d, b + c + 1) + value
            if k >= c:
                assert value == lam(b, c, c)
            if c == 0:
                assert value == 0
            if b == 0:
                assert value == F(c, c + 1)
            support_checks += 1


cut_checks = 0
for r in range(8):
    for initial in range(5):
        for mask in range(1 << r):
            ell = mask.bit_count()
            total = initial + ell
            b, c = initial, ell
            start_lambda = lam(b, c, c)
            start_k = F(c, total + 1)
            start_b = start_k - start_lambda
            theta_sum = F(0)
            for i in range(r):
                hit = (mask >> i) & 1
                old_lambda = lam(b, c, c)
                old_k = F(c, total + 1)
                old_b = old_k - old_lambda
                b, c = b + hit, c - hit
                new_lambda = lam(b, c, c)
                new_k = F(c, total + 1)
                new_b = new_k - new_lambda
                theta = old_lambda - new_lambda
                assert theta >= 0
                assert theta == F(hit, total + 1) + new_b - old_b
                theta_sum += theta
            assert c == 0 and lam(b, c, c) == 0
            assert theta_sum == start_lambda == start_k - start_b
            assert theta_sum <= start_k <= f(initial, ell)
            if initial == 0:
                assert start_b == 0
            cut_checks += 1


background_endpoint = {
    "a": 1, "ell": 1,
    "lambda": str(lam(1, 1, 1)),
    "K": str(F(1, 3)),
    "B": str(F(1, 3) - lam(1, 1, 1)),
}
assert background_endpoint["lambda"] == background_endpoint["B"] == "1/6"

# Integer load is essential: c=0 need not truncate real comparator loads.
fractional_d_failure = f(1, F(1, 2)) - F(1, 2) / 2
assert fractional_d_failure == F(1, 12)

# Independent old13 actual-path arithmetic from the frozen original packet.
base = Path(__file__).resolve().parents[3]
packet_path = (base / "R-c50fecc37aa44fb4a69a2122bb70e5fe" /
               "security/refined_tax_k10_packet.json.gz")
blob = packet_path.read_bytes()
packet = json.loads(gzip.decompress(blob))
instance = packet["instance"]
m = instance["players"]
node_id = packet["root"]
path = []
for _ in range(m):
    node = packet["nodes"][node_id]
    action = node["action"]
    path.append(action)
    node_id = node["children"][action]
assert path == packet["expected_path"]
counts = Counter(path)
topics = instance["topics"]
g = [F(0) for _ in topics]
W = 0
K = F(0)
J_base = F(0)
histogram = Counter()
for customer in instance["customers"]:
    interested = customer["topics"]
    mult = customer["multiplicity"]
    load = sum(counts[a] for a in interested)
    histogram[load] += mult
    if load:
        W += mult
        K += F(mult * load, load + 1)
        J_base += F(mult, load + 1)
    for a in interested:
        g[a] += F(mult, load + 1)
M = max(g)
gap = m * M + K - 2 * W
assert W == 33 and M == 3 and J_base == F(359, 66)
assert K == F(1819, 66) and gap == F(37, 66)

result = {
    "status": "passed",
    "scope": "finite static QA only; no new SPE/half proof",
    "support_checks": support_checks,
    "single_customer_cut_chains": cut_checks,
    "nonempty_background_endpoint": background_endpoint,
    "fractional_comparator_breaks_integer_zero_cut": str(fractional_d_failure),
    "old13": {
        "source_packet_sha256": hashlib.sha256(blob).hexdigest(),
        "actual_path": [topics[a] for a in path],
        "load_histogram": dict(sorted(histogram.items())),
        "W": W, "M": str(M), "K": str(K), "J_base": str(J_base),
        "mM_plus_K_minus_2W": str(gap),
        "query_values": {a: str(g[j]) for j, a in enumerate(topics)},
        "all_history_SPE_status": "inherited from existing source audit; not re-audited here",
    },
}
target = Path(__file__).with_suffix(".json")
target.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
