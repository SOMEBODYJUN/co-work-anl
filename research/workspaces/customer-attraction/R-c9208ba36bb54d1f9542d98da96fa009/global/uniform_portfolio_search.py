"""Attack the strong uniform-portfolio bridge using complete true continuations.

Personal exploratory code; no claim of an arbitrary-instance proof.
"""
from fractions import Fraction
from itertools import combinations_with_replacement
from pathlib import Path
import json
import random
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction import Instance, CustomerType, ExactSPESolver
from customer_attraction.certificate import StrategyCertificate, verify_certificate


def attack(instance, cert):
    m = instance.players
    def run(h):
        while len(h) < m:
            h += (cert.actions[h],)
        return h
    actual = run(())
    w = instance.welfare(instance.counts(actual))
    costs = []
    v = []
    for t in range(instance.topic_count):
        row = []
        for i in range(m):
            h = run(actual[:i] + (t,))
            row.append(instance.topic_payoff(t, instance.counts(h)))
        costs.append(sum(row))
        v.append(row)
    best = None
    for query in combinations_with_replacement(range(instance.topic_count), m):
        o = instance.welfare(instance.counts(query))
        lhs = m*o - sum(costs[t] for t in query) - (m-1)*w
        if best is None or lhs > best[0]:
            best = (lhs, query, o)
    return dict(gap=best[0], query=best[1], optimum=best[2], actual=actual,
                welfare=w, deviation_costs=costs, deviation_values=v)


def main():
    base = ROOT/'examples/customer_attraction'
    certbase = ROOT/'evidence/certificates/customer_attraction'
    tested = 0
    maxgap = None
    for path in sorted(base.glob('*.json')):
        cp = certbase/path.name
        if not cp.exists():
            continue
        obj = json.loads(cp.read_text())
        if 'actions' not in obj:
            continue
        inst = Instance.from_dict(json.loads(path.read_text()))
        cert = StrategyCertificate.from_dict(obj)
        verify_certificate(inst, cert).assert_valid()
        res = attack(inst,cert)
        print(path.stem, res)
        tested += 1
        if maxgap is None or res['gap'] > maxgap:
            maxgap = res['gap']
    print('frozen complete certificates', tested, 'max bridge violation', maxgap)

    if '--random' not in sys.argv:
        return
    rng = random.Random(22291)
    for trial in range(1000):
        k = rng.choice([3,4,5])
        m = rng.choice([3,4,5])
        customers=[]
        for bits in range(1,1<<k):
            r = rng.choice([0,0,0,1,2,3])
            if r:
                customers.append(CustomerType(frozenset(t for t in range(k) if bits>>t&1),r))
        inst = Instance(tuple(map(str,range(k))),tuple(customers),m)
        solver=ExactSPESolver(inst)
        for target in solver.worst_outcomes():
            cert=solver.certificate(target_counts=target)
            res=attack(inst,cert)
            if res['gap']>0:
                verify_certificate(inst,cert).assert_valid()
                print('FOUND',trial,res,inst.to_dict(),cert.to_dict())
                return
        if trial%50==0:
            print('random',trial,flush=True)


if __name__ == '__main__':
    main()
