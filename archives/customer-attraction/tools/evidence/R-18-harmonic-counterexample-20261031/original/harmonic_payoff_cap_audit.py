"""Exact audit of the elementary harmonic cap; finite checks are not a proof."""
import json
import random
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT))
from customer_attraction import CustomerType, ExactSPESolver, Instance, verify_certificate


def algebra(max_players=11):
    checks = 0
    for m in range(1, max_players + 1):
        harmonic = sum((F(1, r) for r in range(1, m + 1)), F())
        for j in range(m):
            coefficient = F(1)
            coefficient += sum((F(1, m-i) for i in range(j)), F())
            coefficient += sum((F(1, m-i+1) for i in range(j+1, m)), F())
            assert coefficient == harmonic
        for mask in range(1, 1 << m):
            load = mask.bit_count()
            for j in range(m):
                if not (mask >> j & 1):
                    continue
                for i in range(m):
                    if i == j:
                        continue
                    past = (mask & ((1 << i)-1)).bit_count()
                    remaining = m-i
                    q = remaining + (j < i)
                    assert F(1, past+remaining) >= F(1, q*load)
                    checks += 1
    return checks


def true_spe_checks():
    rng = random.Random(107131)
    paths = certificates = nodes = 0
    for p, m in [(2, 2), (3, 4), (4, 5), (7, 5)]:
        for sample in range(3):
            rows = []
            for mask in range(1, 1 << p):
                if rng.random() < .3:
                    rows.append(CustomerType(frozenset(a for a in range(p) if mask >> a & 1),
                                             rng.randint(1, 8)))
            if not rows:
                rows = [CustomerType(frozenset({0}), 1)]
            instance = Instance(tuple(map(str, range(p))), tuple(rows), m)
            solver = ExactSPESolver(instance)
            harmonic = sum((F(1, r) for r in range(1, m+1)), F())
            first = None
            for path in solver.ordered_outcomes():
                first = path if first is None else first
                q = instance.counts(path, terminal=True)
                values = instance.topic_payoffs(q)
                welfare = instance.welfare(q)
                actual = tuple(values[a] for a in path)
                for j, payoff in enumerate(actual):
                    assert welfare >= harmonic * payoff
                    for i, other in enumerate(actual):
                        if i != j:
                            assert other >= payoff / (m-i+(j<i))
                paths += 1
            certificate = solver.certificate(on_path=first)
            verify_certificate(instance, certificate).assert_valid()
            nodes += len(certificate.actions)
            certificates += 1
    return {'ordered_paths': paths, 'complete_certificates': certificates,
            'complete_ordered_decision_nodes': nodes}


if __name__ == '__main__':
    report = {'status': 'exact finite corroboration; universal proof is in companion markdown',
              'per_customer_checks': algebra(), 'true_spe': true_spe_checks()}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    Path(__file__).with_suffix('.json').write_text(json.dumps(report, ensure_ascii=False, indent=2))
