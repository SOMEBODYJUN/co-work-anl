#!/usr/bin/env python3
"""Independent finite audits of actual resource incidences; no theorem oracle.

The universal proofs are in the structural accounts.  This program verifies
finite phase identities, all anchored repair bit strings up to length ten,
and a complete finite stable-set/cost-transfer instance.  It never generates
the enormous asymptotic witness and does not infer nonexistence from samples.
"""
from fractions import Fraction as F
from itertools import product, combinations
import argparse
import hashlib
import json
from pathlib import Path


def front(n, x):
    x %= 2*n
    return tuple(int(j < x) if x < n else int(j >= x-n) for j in range(n))


def paired_resources(n, k, orient, q, degree):
    """Literal (22), two classes a=0,b=1, pos(j,a)=2j+a."""
    resources = []
    for j in range(n):
        for side in (0, 1):
            users = {(0,j): side}
            for t in range(k):
                u = (j+t) % n
                sigma = int(2*u+1 > 2*j) ^ int(orient == -1)
                users[(1,u)] = sigma ^ side
            resources.append((users, degree))
    return resources


def costs(resources, bits, q):
    out = {p:F(0) for p in bits}
    for users, degree in resources:
        active = [p for p, action in users.items() if bits[p] == action]
        load = sum((F(1) if p[0] == 0 else q for p in active),F(0))
        val = load**degree
        for p in active:
            out[p] += val
    return out


def phase_checks():
    count = 0
    for n in range(2,9):
        for k in range(1,n+1):
            for degree in (1,2,5):
                q=F(1,7)
                res=paired_resources(n,k,-1,q,degree)
                area=sum(((1+r*q)**degree for r in range(1,k+1)),F(0))
                for r in range(2*n):
                    bits={(a,j):front(n,0 if a==0 else r)[j]
                          for a in (0,1) for j in range(n)}
                    h=k-min(r,k) if r<=n else min(r-n,k)
                    old=costs(res,bits,q)[(0,0)]
                    bits[(0,0)]^=1
                    new=costs(res,bits,q)[(0,0)]
                    assert (old,new)==((1+h*q)**degree,(1+(k-h)*q)**degree)
                    # Light endpoints, with its own class normalized to phase zero.
                    for direction, j in ((1,0),(-1,n-1)):
                        bits={(a,z):front(n,r if a==0 else 0)[z]
                              for a in (0,1) for z in range(n)}
                        old=costs(res,bits,q)[(1,j)]
                        bits[(1,j)]^=1
                        new=costs(res,bits,q)[(1,j)]
                        assert old<=area and new<=area
                    count+=1
        for degree in (1,3):
            q=F(1,7*n)
            res=paired_resources(n,n,1,q,degree)
            for r in range(2*n):
                bits={(a,j):front(n,r if a==0 else 0)[j]
                      for a in (0,1) for j in range(n)}
                e=[int(front(n,r)[(-k)%n] == int(k==0)) for k in range(n)]
                expected_old=sum((((n-k)*q+e[k])**degree for k in range(n)),F(0))
                expected_new=sum((((k+1)*q+1-e[k])**degree for k in range(n)),F(0))
                old=costs(res,bits,q)[(1,0)]
                bits[(1,0)]^=1
                new=costs(res,bits,q)[(1,0)]
                assert (old,new)==(expected_old,expected_new)
                count+=1
    return count


def gate_cost(bits, degree=12, scale=F(100)):
    n=len(bits)
    out=[F(0)]*n
    for i,j in combinations(range(1,n),2):
        participants=(0,i,j)
        sides=(bits[0],bits[i]^1,bits[j])
        for pos,p in enumerate(participants):
            occupancy=sum(s==sides[pos] for s in sides)
            out[p]+=scale*F(occupancy,3)**degree
    return out


def is_front(bits):
    return sum(a!=b for a,b in zip(bits,bits[1:]))<=1


def repair_checks():
    count=0
    for n in range(1,11):
        fronts={front(n,x) for x in range(2*n)}
        assert len(fronts)==2*n
        for bits in product((0,1),repeat=n):
            triggered=[(i,j) for i,j in combinations(range(1,n),2)
                       if bits[0]==bits[j] and bits[i]!=bits[0]]
            assert (not triggered)==is_front(bits)==(bits in fronts)
            if triggered:
                i=next(i for i in range(1,n) if bits[i]!=bits[0])
                changed=list(bits);changed[i]=bits[0]
                for j,k in combinations(range(1,n),2):
                    if i in (j,k):
                        assert not (changed[0]==changed[k] and changed[j]!=changed[0])
            else:
                for i in range(n):
                    changed=list(bits);changed[i]^=1
                    if is_front(changed):
                        for j,k in combinations(range(1,n),2):
                            if i in (0,j,k):
                                for s in (bits,changed):
                                    sides=(s[0],s[j]^1,s[k])
                                    mover=(0,j,k).index(i)
                                    assert sum(x==sides[mover] for x in sides)==2
            count+=1
    return count


def stable_set_checks():
    checks=0
    for n in (3,4,5):
        ell=F((n-1)*(n-2),2)
        u=F(100)*F(2,3)**12
        z=F(100)*F(1,3)**12
        # Private constant resources realize these literal base costs.
        base=[(F(3),F(1)) if i%2==0 else (F(1),F(2)) for i in range(n)]
        for alpha in (F(1),F(3,2),F(2)):
            assert 100 > alpha*(3+ell*u)
            for bits in product((0,1),repeat=n):
                old=gate_cost(bits)
                actual=True
                predicted=is_front(bits)
                for i in range(n):
                    t=list(bits);t[i]^=1
                    new=gate_cost(t)
                    if base[i][bits[i]]+old[i] > alpha*(base[i][t[i]]+new[i]):
                        actual=False
                    if is_front(bits) and is_front(t):
                        participation=ell if i==0 else n-2
                        if base[i][bits[i]]-alpha*base[i][t[i]] > (alpha-1)*participation*u:
                            predicted=False
                assert actual==predicted
                if is_front(bits):
                    assert sum(old)==ell*(2*u+z)
                checks+=1
    return checks


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result={'status':'PASS','scope':'finite actual-resource identities only; not a universal proof',
            'phase_parameter_cases':phase_checks(),
            'repair_bit_strings':repair_checks(),
            'stable_set_instances':stable_set_checks(),
            'seed':None,'arithmetic':'fractions.Fraction, exact integers',
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    output=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if args.output:
        with args.output.open('x') as f:
            f.write(output)
    print(output,end='')


if __name__=='__main__':
    main()
