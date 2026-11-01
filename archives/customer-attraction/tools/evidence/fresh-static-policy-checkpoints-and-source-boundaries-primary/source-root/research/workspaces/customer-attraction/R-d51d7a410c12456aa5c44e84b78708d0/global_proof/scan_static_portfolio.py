"""Explore the aggregate static deviation allowance, not the main conjecture.

The candidate D_T(q) <= (1+1/m) W(q) for every topic T is sufficient for
half coverage via the exact portfolio identity documented in notes.md.
Exact SPE outcomes use the canonical oracle; finite searches prove nothing
universal. A discovered failure is reconstructed as a full certificate.
"""
import json
import random
from fractions import Fraction
from pathlib import Path
from customer_attraction import Instance, CustomerType, ExactSPESolver, verify_certificate


def static_deviation_sum(ins, q, a):
    answer = Fraction(0)
    for b, count in enumerate(q):
        if count:
            qq = list(q)
            qq[b] -= 1
            qq[a] += 1
            answer += count * ins.topic_payoff(a, qq)
    return answer


def main():
    rng = random.Random(20261021)
    best = Fraction(0)
    tested = 0
    for m, k, runs in [(2, 5, 200), (3, 5, 300), (4, 6, 300), (5, 7, 150)]:
        for trial in range(runs):
            cs = []
            for mask in range(1, 1 << k):
                if rng.random() < .4:
                    v = rng.randrange(1, 10)
                    cs.append(CustomerType(frozenset(a for a in range(k) if mask >> a & 1), v))
            ins = Instance(tuple(map(str, range(k))), tuple(cs), m)
            solver = ExactSPESolver(ins)
            for q in solver.outcomes():
                welfare = ins.welfare(q)
                if not welfare:
                    continue
                for a in range(k):
                    d = static_deviation_sum(ins, q, a)
                    ratio = d / welfare
                    tested += 1
                    if ratio > best:
                        best = ratio
                        print(json.dumps({'m': m, 'k': k, 'trial': trial, 'q': q,
                                          'a': a, 'D/W': str(ratio), 'tested': tested}), flush=True)
                    if d > Fraction(m+1, m) * welfare:
                        cert = solver.certificate(target_counts=q)
                        report = verify_certificate(ins, cert)
                        report.assert_valid()
                        result = {'instance': ins.to_dict(), 'certificate': cert.to_dict(),
                                  'q': q, 'a': a, 'D': str(d), 'W': welfare,
                                  'allowance': str(Fraction(m+1, m)*welfare)}
                        path = Path(__file__).with_name('static_aggregate_candidate_failure.json')
                        path.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
                        print('FAILURE', path, flush=True)
                        return
    print('COMPLETE', tested, 'maximum', best, flush=True)


if __name__ == '__main__':
    main()
