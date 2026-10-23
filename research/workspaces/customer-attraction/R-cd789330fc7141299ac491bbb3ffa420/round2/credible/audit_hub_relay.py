"""Exact local algebra audit; no SPE, BI, author discovery code or optimizer."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def main():
    output=Path(__file__).with_name('hub_relay_audit.json')
    if output.exists():
        raise FileExistsError(output)
    topics=tuple(frozenset(x for x in range(3) if mask&(1<<x)) for mask in range(8))
    total=hub_hypotheses=unanimous=0
    for background in product(range(2),repeat=3):
        for root in topics:
            for length in (1,2,3):
                for future in product(topics,repeat=length):
                    tail=future[-1]
                    k=tuple(sum(x in t for t in future) for x in range(3))
                    denominator=tuple(background[x]+(x in root)+k[x] for x in range(3))
                    root_u=sum((F(1,denominator[x]) for x in root),F())
                    tail_u=sum((F(1,denominator[x]) for x in tail),F())
                    delta0=sum((F(1,background[x]+1) for x in root-tail),F())-sum(
                        (F(1,background[x]+1) for x in tail-root),F())
                    loss=sum((F(k[x],(background[x]+1)*(background[x]+1+k[x])) for x in root-tail),F())
                    gain=sum((F(k[x]-1,(background[x]+1)*(background[x]+k[x])) for x in tail-root),F())
                    assert root_u-tail_u == delta0-loss+gain
                    assert gain >= 0
                    total += 1
                    overlap=root & frozenset().union(*future)
                    if delta0 >= 0 and overlap <= tail:
                        assert root_u >= tail_u
                        hub_hypotheses += 1
                    if len(set(future)) == 1 and delta0 >= 0:
                        assert root_u >= tail_u
                        unanimous += 1
    report={'status':'exact_local_algebra_pass',
            'scope':'Three literal unit customers, all themes, backgrounds in {0,1}^3, one to three future actions.',
            'identity_checks':total,'hub_protection_checks':hub_hypotheses,
            'unanimous_tail_checks':unanimous,
            'limitations':'No general existence of a protected branch is claimed; no SPE counterexample was constructed.'}
    payload=json.dumps(report,indent=2)+'\n'
    with output.open('x') as f:
        f.write(payload)
    print(payload)


if __name__=='__main__':
    main()
