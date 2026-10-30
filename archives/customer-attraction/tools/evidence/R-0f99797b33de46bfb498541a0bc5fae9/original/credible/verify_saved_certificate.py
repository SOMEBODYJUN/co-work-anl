"""Replay saved insurance-repair witnesses directly from unit customers/actions."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,sys

def check(path):
    obj=json.loads(Path(path).read_text());m=obj['m'];p=len(obj['topics'])
    rows=obj['actions'];A={tuple(z['history']):z['action'] for z in rows}
    assert len(A)==len(rows)
    expected={h for d in range(m) for h in product(range(p),repeat=d)}
    assert set(A)==expected
    assert all(a in range(p) for a in A.values())
    customers=[frozenset(B) for B in obj['unit_customer_interest']]
    def end(h):
        while len(h)<m:h=h+(A[h],)
        return h
    def u(z,a):
        return sum((F(1,sum(b in B for b in z)) for B in customers if a in B),F(0))
    def W(z):return sum(bool(B.intersection(z)) for B in customers)
    slacks=[u(end(h),a)-u(end(h+(b,)),b) for h,a in A.items() for b in range(p)]
    assert min(slacks)>=0
    z=end(());opt=max(W(t) for t in product(range(p),repeat=m))
    assert list(z)==obj['root_path']
    assert W(z)==obj['W'] and opt==obj['OPT']
    assert u(z,A[()])==F(obj['root_payoff'])
    return dict(file=Path(path).name,m=m,ordered_histories=len(A),comparisons=len(slacks),
                minimum_slack=str(min(slacks)),W=W(z),OPT=opt,root_payoff=str(u(z,A[()])))
if __name__=='__main__':
    paths=sys.argv[1:] or sorted(Path(__file__).parent.glob('two_theme_repair_m*_certificate.json'))
    print(json.dumps([check(p) for p in paths],indent=2))
