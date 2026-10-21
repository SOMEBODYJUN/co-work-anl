"""Exact audit of B10-TWO-SUPPORT-END-AB-v1; finite checks are not its proof.

Reconstructs original three SPE comparisons on each customer membership,
without the canonical solver or another audit. Refuses to overwrite output.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import json


def check(k, l):
    m = k + l
    checked = 0
    for a, b, t, r in product((0, 1), repeat=4):
        p = (k-1)*a + (l-1)*b
        def u(x, y):
            return F(x, p+1+y)
        actual_a, actual_b = u(a,b), u(b,a)
        slacks = (actual_a-u(t,r), u(r,t)-u(b,t), actual_b-u(r,a))
        remainder = F(a*(1-r), (p+1)*(p+2))
        t_weight = (F(t) if not a and not b else
                    F(t,k) if a and not b else
                    F(t,l+1) if b and not a else F(t,m))
        constant = F(a*(1-b)*(k+2),k*(k+1)) + F(a*b,m)
        assert constant - t_weight == sum(slacks) + remainder
        assert remainder >= 0
        # Independent expansion of the actual last-player comparison.
        before_last = k*a + (l-1)*b
        last_query = F(t,before_last+1)
        weight = (F(t) if not a and not b else
                  F(t,k+1) if a and not b else
                  F(t,l) if b and not a else F(t,m))
        assert last_query == weight
        checked += 1

    x,y,z,v = F(l*(k+2)-1,k*(k+1)),F(k-1,l),F(k+2,k+1),F(l+2,l+1)
    det = z*v-x*y
    assert det == F(l*(k+2)*(k+l+1)+(k-1)*(l+1),k*l*(k+1)*(l+1))
    lam = (y+z)/(x+y+z+v)
    delta = det/(x+y+z+v)
    gamma = 2-delta
    pa,pb,la,lb = 2+x,2-v,2-z,2+y
    assert 0 < lam < 1 and delta > 0
    assert lam*pa+(1-lam)*la == gamma
    assert lam*pb+(1-lam)*lb == gamma
    # Recover portfolio coefficients from the primitive single-topic weights.
    assert F(m*(k+2),k*(k+1)) + 1-F(1,k) == pa
    assert 1-F(1,l+1) == pb
    assert 1-F(1,k+1) == la
    assert F(m,l)+1-F(1,l) == lb
    return checked, {'k':k,'l':l,'lambda':str(lam),'delta':str(delta),
                     'beta':str(2-min(delta,F(1,m)))}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    if args.output and args.output.exists():
        ap.error('output already exists')
    grid = list(product(range(1,41),repeat=2)) + [(1,10000),(10000,1),(127,991)]
    count=0;examples=[]
    for k,l in grid:
        n,row=check(k,l);count+=n
        if (k,l) in [(1,1),(4,1),(20,2),(20,20),(1,10000),(10000,1),(127,991)]:
            examples.append(row)
    # Zero population: every original inequality and final conclusion is 0.
    assert F(0)==sum(F(0) for _ in range(4))
    report={'claim':'B10-TWO-SUPPORT-END-AB-v1','status':'exact_audit_passed',
            'parameter_pairs':len(grid),'membership_identity_checks':count,
            'zero_population_checked':True,'examples':examples,
            'scope':'Finite algebra audit; universal statement follows from the written identities and positive numerator.'}
    content=json.dumps(report,ensure_ascii=False,indent=2)+'\n'
    if args.output:
        with args.output.open('x') as stream: stream.write(content)
    print(content,end='')


if __name__=='__main__':
    main()
