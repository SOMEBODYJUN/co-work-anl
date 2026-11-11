#!/usr/bin/env python3
"""Literal seven-client separation of the old full local parameter family.

This is not an SPE and not a point of the current master system.  Universal
q/z/tau/eta statements are proved in full_parameter_audit_v2.md; this script
only audits finite primitive rows and the one frozen rational candidate.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json


ROOT = Path(__file__).resolve().parent
RUN = ROOT.parent
customers = tuple(range(7))
catalog = {'E': frozenset(), 'A': frozenset({0})}
catalog.update({f'T{i}': frozenset({i}) for i in range(1, 7)})
replies = {q: 'E' for q in catalog}
actual = ('E', 'E', 'E', 'E', 'A', 'E')
past = {x: sum(x in catalog[q] for q in actual[:4]) for x in customers}


def u(q, r):
    return sum((F(1, past[x] + 1 + (x in catalog[r])) for x in catalog[q]), F(0))


v, w = u('A', 'E'), u('E', 'A')
source = {q: v - u(q, replies[q]) for q in catalog}
price = {q: w - u(replies[q], 'A') for q in catalog}
image = {(q, r): u(replies[q], q) - u(replies[r], q) for q in catalog for r in catalog}
assert v == 1 and w == 0
assert source['E'] == 1 and all(source[q] == 0 for q in catalog if q != 'E')
assert all(value == 0 for value in price.values())
assert all(value == 0 for value in image.values())
assert all(value >= 0 for value in [*source.values(), *price.values(), *image.values()])

queries = tuple(f'T{i}' for i in range(1, 7))
new_rows = {(q, r): u(replies[q], q) - u(r, q) for q in queries for r in queries}
assert sum(new_rows.values()) == -33
assert all(new_rows[(q, q)] == F(-1, 2) for q in queries)
assert all(value == -1 for (q, r), value in new_rows.items() if q != r)

gamma, eta = F(1, 7), F(12, 7)
coefficients = []
pair_rhs = F(0)
for x in customers:
    p = past[x]
    a = int(x in catalog['A'])
    n = sum(x in catalog[q] for q in queries)
    delta = F(1, (p + 1) * (p + 2))
    psi = (1 + gamma) * n / (p + 1) - gamma * delta * n * n / 6 - max(
        F(0), (1 - gamma) * delta * n + 6 * gamma / (p + 1) - eta / (p + a + 1))
    assert psi == (F(0) if x == 0 else F(95, 84))
    pair_rhs += F(2 * n, p + 1) - delta * n * n / 6 - 6 * a * delta
    coefficients.append({'customer': x, 'P': p, 'a': a, 'n': n, 'psi': str(psi)})

budget = 6 * v + eta * w
rhs = sum(F(row['psi']) for row in coefficients)
slack = budget - rhs
raw_slack = sum(source[q] for q in queries) + eta / 6 * sum(price[q] for q in queries)
raw_slack += (1 - gamma) / 6 * sum(image[(q, r)] for q in queries for r in queries)
raw_slack += gamma / 6 * sum(new_rows.values())
assert budget == 6 and rhs == F(95, 14)
assert slack == raw_slack == F(-11, 14)
pair_slack = 6 * (v + w) - pair_rhs
assert pair_rhs == F(17, 2) and pair_slack == F(-5, 2)

frozen = {
    'direct_tail_budget.md': 'b579e529103c584dae201e375055398280aef837e04bff6a339c949dd066e642',
    'direct_tail_budget/verify_direct_tail_budget_v1.py': 'a7174c5306aedfc4f7df9248b55604bdbb78138fbdd0545a172af1a8ca61bd2a',
    'direct_tail_budget/verify_direct_tail_budget_v1.json': '9e83b66a593325d8a272b422e6802e2bdeafb1c924e97c22864ce98ab1ce6104',
}
observed = {name: hashlib.sha256((RUN / name).read_bytes()).hexdigest() for name in frozen}
assert observed == frozen

report = {
    'status': 'PASS',
    'scope': 'Noncontainment in the old fixed-source full-parameter envelope only; violates old strong PAIR and actual terminal IC; not an SPE or a full old price-plus-PAIR cone witness.',
    'customers': len(customers),
    'catalog': {q: sorted(catalog[q]) for q in catalog},
    'actual': actual,
    'replies_at_h': replies,
    'actual_u5': str(v),
    'actual_u6': str(w),
    'old_primitive_rows': len(source) + len(price) + len(image),
    'old_source_slacks': {q: str(value) for q, value in source.items()},
    'old_price_rows_all_zero': True,
    'old_reply_image_rows_all_zero': True,
    'universal_old_parameters': 'Analytic: S(z)=z_E, Z(z)=V(z)=0 for every z>=0; B_q(1)=sum(q_x-1)_+ <= sum(q_x-theta_eta)_+ for every q>=0, eta>=0.',
    'new_Y_rows': len(new_rows),
    'new_Y_sum': '-33',
    'gamma': str(gamma),
    'eta': str(eta),
    'candidate_coefficients': coefficients,
    'candidate_budget': str(budget),
    'candidate_rhs': str(rhs),
    'candidate_slack': str(slack),
    'candidate_raw_slack': str(raw_slack),
    'actual_terminal_T_query_slack': str(w - u('T1', 'A')),
    'actual_terminal_A_query_slack': str(w - u('A', 'A')),
    'old_strong_pair_endpoint_rhs': str(pair_rhs),
    'old_strong_pair_endpoint_slack': str(pair_slack),
    'solvers_run': 0,
    'parameter_grids_run': 0,
    'master_points_read': 0,
    'v1_frozen_sha256_unchanged': observed,
}
(ROOT / 'verify_full_parameter_audit_v2.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({key: report[key] for key in (
    'status', 'old_primitive_rows', 'new_Y_rows', 'candidate_budget', 'candidate_rhs',
    'candidate_slack', 'actual_terminal_T_query_slack')}, ensure_ascii=False, indent=2))
