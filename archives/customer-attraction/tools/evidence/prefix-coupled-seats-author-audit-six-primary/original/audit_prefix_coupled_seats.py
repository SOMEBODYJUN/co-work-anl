"""Exact regression of the all-input coupled-seat formulas on the frozen witness.

The analytic theorem is in prefix_coupled_seat_budget.md. This audit neither
searches for a half counterexample nor purports to establish a general bound.
"""
import itertools
import json
import sys
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[5]))
from customer_attraction.model import Instance
from customer_attraction.exact import ExactSPESolver
from customer_attraction.certificate import verify_certificate

obj = json.loads((HERE / 'refined_spectrum_strict_example.json').read_text())
inst = Instance.from_dict(obj['instance'])
hist = tuple(obj['path'])
sol = ExactSPESolver(inst)
cert = sol.certificate(on_path=hist)
verified = verify_certificate(inst, cert)
verified.assert_valid()
assert verified.terminal_history == hist
cs = inst.customers
m, n = inst.players, inst.topic_count
sets = [frozenset(x for x, c in enumerate(cs) if a in c.topics) for a in range(n)]
maxima = [a for a in range(n) if not any(sets[a] < sets[b] for b in range(n))
          and sets[a] not in sets[:a]]
C = frozenset().union(*(sets[a] for a in hist))
private = {a: sets[a] - frozenset().union(*(sets[b] for b in maxima if b != a))
           for a in maxima}
Q = {a: private[a] - C for a in maxima}
a_size = {a: sum(cs[x].multiplicity for x in Q[a]) for a in maxima}
old_slots = sorted((F(a_size[a], k) + F(sum(cs[x].multiplicity for x in sets[a] - Q[a]), m)
                    for a in maxima for k in range(1, m + 1)), reverse=True)
b = [0] * len(cs)
rows = []
new_sum = robust_sum = old_sum = F(0)
for i, actual in enumerate(hist):
    r = m - i
    integer_slots, explicit_slots = [], []
    for a in maxima:
        for k in range(1, r + 1):
            e = sum((F(cs[x].multiplicity, b[x] + r) for x in sets[a] - Q[a]), F(0))
            explicit = F(a_size[a], k) + e
            feasible = []
            for others in itertools.combinations_with_replacement(range(n), r - 1):
                touches = sum(bool(sets[t] & Q[a]) for t in others)
                if touches <= k - 1:
                    value = sum((F(cs[x].multiplicity, b[x] + 1
                                         + sum(x in sets[t] for t in others))
                                 for x in sets[a]), F(0))
                    feasible.append(value)
            assert feasible
            robust = min(feasible)
            assert robust >= explicit
            integer_slots.append(robust)
            explicit_slots.append(explicit)
    lam_F = sorted(integer_slots, reverse=True)[r - 1]
    lam_G = sorted(explicit_slots, reverse=True)[r - 1]
    direct = max(sum((F(cs[x].multiplicity, b[x] + r) for x in sets[a]), F(0))
                 for a in maxima)
    old = max(old_slots[r - 1], direct)
    actual_payoff = inst.player_payoffs(hist)[i]
    assert actual_payoff >= lam_F >= lam_G >= old
    rows.append({'i': i + 1, 'remaining': r, 'actual': str(actual_payoff),
                 'F_spectrum': str(lam_F), 'G_spectrum': str(lam_G),
                 'old_spectrum': str(old_slots[r - 1]), 'direct': str(direct)})
    robust_sum += lam_F
    new_sum += lam_G
    old_sum += old
    for x in sets[actual]:
        b[x] += 1
assert new_sum == F(obj['new'])
assert old_sum == F(obj['old_combined'])
assert new_sum - old_sum == F(obj['gap']) > 0
out = {'status': 'all assertions passed', 'rows': rows,
       'welfare': inst.welfare(inst.counts(hist)), 'F_sum': str(robust_sum),
       'G_sum': str(new_sum), 'old_combined_sum': str(old_sum),
       'strict_gap': str(new_sum - old_sum),
       'complete_certificate_histories': verified.checked_histories,
       'complete_certificate_deviations': verified.checked_deviations}
(HERE / 'prefix_coupled_seat_audit.json').write_text(json.dumps(out, indent=2) + '\n')
(HERE / 'refined_spectrum_complete_strategy.json').write_text(json.dumps(cert.to_dict(), indent=2) + '\n')
print(json.dumps(out, indent=2))
