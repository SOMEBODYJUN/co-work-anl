"""Exact audit for CA-HARMONIC-BRANCH-DELETION-OBSTRUCTION-v1.

Verifies the uploaded full ordered-history SPE certificate independently via
customer_attraction.verify_certificate, then recomputes the two root branches,
unit payoffs, welfare, and harmonic-potential deletion gap using Fraction.
This is an obstruction to branchwise potential monotonicity, not a Q-CAG-HALF
counterexample.
"""
from fractions import Fraction as F
import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[5]))
from customer_attraction import Instance, StrategyCertificate, ExactSPESolver, verify_certificate

HERE = Path(__file__).resolve().parent
raw = json.loads((HERE / "potential_branch_obstruction.json").read_text())
inst = Instance.from_dict(raw["instance"])
cert = StrategyCertificate.from_dict(raw["certificate"])
ver = verify_certificate(inst, cert)
ver.assert_valid()
assert ver.checked_histories == 43 and ver.checked_deviations == 215

def H(k):
    return sum((F(1, j) for j in range(1, k + 1)), F(0))

def phi(counts):
    out = F(0)
    for customer in inst.customers:
        load = sum(counts[t] for t in customer.topics)
        out += customer.multiplicity * H(load)
    return out

def follow(history):
    if len(history) == inst.players:
        return history, inst.counts(history, terminal=True)
    action = cert.actions[history]
    return follow(tuple(history) + (action,))

def branch(first):
    return follow((first,))
actual_history, actual_counts = follow(())
forced_history, forced_counts = branch(0)
assert actual_history == (1, 3, 4)
assert forced_history == (0, 0, 4)
assert inst.topic_payoff(1, actual_counts) == inst.topic_payoff(0, forced_counts) == F(1)
assert inst.welfare(actual_counts) == inst.optimal_welfare() == 4
actual_delete = list(actual_counts); actual_delete[1] -= 1
forced_delete = list(forced_counts); forced_delete[0] -= 1
assert phi(actual_counts) == F(9, 2)
assert phi(forced_counts) == F(5)
assert phi(tuple(actual_delete)) == F(7, 2)
assert phi(tuple(forced_delete)) == F(4)
assert phi(actual_counts) - phi(forced_counts) == F(-1, 2)
assert phi(tuple(actual_delete)) - phi(tuple(forced_delete)) == F(-1, 2)
print(json.dumps({
    "status": "passed",
    "claim": "CA-HARMONIC-BRANCH-DELETION-OBSTRUCTION-v1",
    "histories": ver.checked_histories,
    "deviations": ver.checked_deviations,
    "actual_history": actual_history,
    "forced_root_history": forced_history,
    "welfare": inst.welfare(actual_counts),
    "optimum": inst.optimal_welfare(),
    "phi_actual": str(phi(actual_counts)),
    "phi_forced": str(phi(forced_counts)),
    "phi_deleted_actual": str(phi(tuple(actual_delete))),
    "phi_deleted_forced": str(phi(tuple(forced_delete))),
    "potential_gap": str(phi(actual_counts) - phi(forced_counts)),
    "deletion_gap": str(phi(tuple(actual_delete)) - phi(tuple(forced_delete))),
    "scope": "branchwise harmonic-potential monotonicity fails; no main-claim counterexample",
}, ensure_ascii=False, sort_keys=True))
