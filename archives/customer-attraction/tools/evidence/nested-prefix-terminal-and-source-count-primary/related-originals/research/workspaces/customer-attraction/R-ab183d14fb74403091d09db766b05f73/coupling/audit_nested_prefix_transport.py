"""Independent arithmetic and true-tree audit for NP-TRANSPORT."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import random
import sys

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[4]
sys.path.insert(0, str(ROOT))
from customer_attraction import CustomerType, Instance, ExactSPESolver


def main():
    identities = 0
    for h in range(30):
        for r in range(1, 31):
            for a,b,z in product((0,1), repeat=3):
                union = int(a or b)
                both = a*b
                # Direct f(b)+U_a definition; no use of displayed kernel formula.
                old = F(b,h+1)+(F(1,h+1+r*b) if a else 0)
                newh = h+z
                new = F(b,newh+1)+(F(1,newh+1+(r-1)*b) if a else 0)
                assert old == F(union,h+1)+F(both,h+r+1)
                drift = F(z*union,(h+1)*(h+2))-F((1-z)*both,(h+r)*(h+r+1))
                assert old-new == drift
                residual = F(z*(1-union),(h+1)*(h+2))+F((1-z)*both,(h+r)*(h+r+1))
                assert new+F(newh,newh+1)-old-F(h,h+1) == residual >= 0
                identities += 1
    rng = random.Random(661093)
    true_comparisons = 0
    paths = 0
    for n,p in [(2,4),(3,4),(4,4)]:
        for sample in range(8):
            customers = tuple(CustomerType(frozenset(a for a in range(p) if b>>a&1),rng.randint(1,8)) for b in range(1,1<<p) if rng.random()<.4)
            ins = Instance(tuple('T'+str(a) for a in range(p)),customers,n)
            sol = ExactSPESolver(ins)
            cert = sol.certificate(min(sol.worst_outcomes()))
            acts = dict(cert.actions)
            def count(h):
                return tuple(h.count(a) for a in range(p))
            def payoff(a, h):
                return ins.topic_payoffs(count(h))[a]
            def f(h,a):
                return sum((F(c.multiplicity,1+sum(count(h)[b] for b in c.topics)) for c in customers if a in c.topics),F(0))
            def kernel(h,a,b):
                r = n-len(h)-1
                return f(h,b)+payoff(a,h+(a,)+(b,)*r)
            def tax(h):
                return sum((F(c.multiplicity*ell,ell+1) for c in customers if (ell:=sum(count(h)[b] for b in c.topics))),F(0))
            for k in range(n):
                for h in product(range(p),repeat=k):
                    r = n-k-1
                    for a,b in product(range(p),repeat=2):
                        reply = acts[h+(b,)*r]
                        assert kernel(h,b,reply) >= kernel(h,a,b)
                        assert kernel(h,b,reply)-kernel(h,a,b) == payoff(reply,h+(b,)*r+(reply,))-payoff(a,h+(b,)*r+(a,))
                        true_comparisons += 1
            # Complete arbitrary history chains, not just root policy path.
            for samplepath in range(20):
                history = tuple(rng.randrange(p) for _ in range(n-1))
                a,b = rng.randrange(p),rng.randrange(p)
                initial = kernel((),a,b)
                slack = F(0)
                for k in range(n):
                    h = history[:k]
                    r = n-k-1
                    for _ in range(rng.randrange(4)):
                        reply = acts[h+(b,)*r]
                        delta = kernel(h,b,reply)-kernel(h,a,b)
                        assert delta >= 0
                        slack += delta
                        a,b = b,reply
                    if k<n-1:
                        nxt = history[:k+1]
                        delta = kernel(nxt,a,b)+tax(nxt)-kernel(h,a,b)-tax(h)
                        assert delta >= 0
                        slack += delta
                final = kernel(history,a,b)+tax(history)
                assert final-initial == slack >= 0
                paths += 1
    report = {'claim':'NP-TRANSPORT','status':'formula and finite true-tree audit; general Q-CAG-HALF OPEN',
              'membership_identities':identities,'true_last_comparisons':true_comparisons,
              'alternating_paths':paths,'seed':661093}
    print(json.dumps(report,indent=2))
    (BASE/'nested_prefix_transport_audit.json').write_text(json.dumps(report,indent=2)+'\n')


if __name__ == '__main__':
    main()
