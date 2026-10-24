"""Exact definition-level audit; no SPE search or new game certificate.

Checks all local U,V,K counts up to four future roles, zero/fresh domains,
SAFE credit algebra, and one nonzero two-level fresh DAG identity.
"""
from fractions import Fraction as F
from pathlib import Path
import json


def sets(n):
    return [frozenset(i for i in range(n) if mask & (1 << i))
            for mask in range(1 << n)]


local_checks = subset_checks = safe_checks = 0
for n in range(5):
    ss = sets(n)
    for u in ss:
        for v in ss:
            for background in range(4):
                ca, cb = 1 + len(u), 1 + len(v) + background
                nu, df = F(1, cb), F(1, ca)
                p = F(len(u - v), ca * cb)
                neg = F(background + len(v - u), ca * cb)
                diag = F(1, ca * cb)
                common = F(len(u & v), ca * cb)
                assert nu - df == p - neg
                assert nu - p == df - neg == diag + common > 0
                for k in ss:
                    selected = F(len(k & (u - v)), ca * cb)
                    assert selected / nu <= F(len(k), len(k) + 1)
                    subset_checks += 1
                for y in (F(0), F(1, 3), F(2)):
                    for e in (F(0), F(1, 7)):
                        actual = df + y + e
                        refund = y + neg + e
                        assert 0 <= refund <= actual
                        assert actual - refund == diag + common
                        safe_checks += 1
                local_checks += 1

# A positive fresh edge: B has old background one, no future coverer;
# A has background zero and one new future coverer.  The child prescribed
# leaf is A; its actual reset has no old fresh coverage or future coverer.
# These are local completion counts, not a claimed game/SPE certificate.
nu1, p1, n1 = F(1, 2), F(1, 4), F(1, 4)
nu2, p2, n2 = F(1, 2), F(0), F(1, 2)
b1, b2 = F(1), F(0)
beta1 = b1 / nu1
h2 = b2 + beta1 * p1
beta2 = h2 / nu2
y1, e1, actual1 = F(1, 4), F(1, 8), F(7, 8)
y2, e2, actual2 = F(1, 2), F(1, 4), F(7, 4)
mass = beta1 * (nu1 - p1) + beta2 * (nu2 - p2)
ledger = beta1 * (actual1 - y1 - n1 - e1)
ledger += beta2 * (actual2 - y2 - n2 - e2)
assert mass == ledger == b1 + b2 == 1
assert beta1 > 1  # Explicitly records that the lemma does not give beta<=1.

report = {
    "status": "passed",
    "scope": "definition-level local count audit plus one positive fresh DAG; not a game or SPE scan",
    "local_identity_checks": local_checks,
    "all_subset_checks": subset_checks,
    "safe_refund_checks": safe_checks,
    "positive_fresh_dag": {
        "beta": [str(beta1), str(beta2)],
        "edge_profit": str(beta1 * p1),
        "input_mass": "1", "remaining_mass": str(mass),
        "signed_ledger": str(ledger),
        "claim_beta_cap": False,
    },
    "certifies_global_fee_bound": False,
}
out = Path(__file__).with_name("fresh_profit_normalization_audit.json")
with out.open("x", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
    f.write("\n")
print(json.dumps(report, ensure_ascii=False))
