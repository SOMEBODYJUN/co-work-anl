"""Independent exact rank/finite-difference and game-table checks.

This file does not import the discovery audit or the canonical CAG package.
The general theorem is independently reconstructed in the accompanying review.
"""
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import argparse
import json


def rank(rows):
    basis={}
    for row in rows:
        r=list(row)
        for j,base in sorted(basis.items()):
            t=r[j]
            if t:r=[x-t*y for x,y in zip(r,base)]
        pivot=next((j for j,x in enumerate(r) if x),None)
        if pivot is not None:
            t=r[pivot]
            basis[pivot]=[x/t for x in r]
    return len(basis)


def comps(total,length):
    if length==1:
        yield (total,)
        return
    for first in range(total+1):
        for tail in comps(total-first,length-1):yield (first,)+tail


def payoff(q,a,B):
    return F(1,sum(q[j] for j in range(len(q)) if B>>j&1)) if B>>a&1 else F(0)


def moments(r,p,m):
    return {A:sum(v for B,v in r.items() if B&A==A)
            for A in range(1,1<<p) if A.bit_count()<=m}


def check_game(r,s,p,m):
    assert moments(r,p,m)==moments(s,p,m)
    checks=0
    for path in product(range(p),repeat=m):
        q=tuple(path.count(a) for a in range(p))
        for a in path:
            assert sum(v*payoff(q,a,B) for B,v in r.items())==sum(v*payoff(q,a,B) for B,v in s.items())
            checks+=1
        mask=sum(1<<a for a,c in enumerate(q) if c)
        assert sum(v for B,v in r.items() if B&mask)==sum(v for B,v in s.items() if B&mask)
    return checks


def run():
    ranks=[]
    for p in range(1,6):
        for m in range(1,5):
            # Independent full row-rank test, not rank of the proposed basis.
            rows=[]
            for q in comps(m,p):
                for a,c in enumerate(q):
                    if c:rows.append([payoff(q,a,B) for B in range(1,1<<p)])
            actual=rank(rows)
            expected=sum(comb(p,j) for j in range(1,min(p,m)+1))
            assert actual==expected
            ranks.append({'m':m,'p':p,'full_payoff_rows':len(rows),'rank':actual})
    differences=0
    for m in range(1,20):
        for s in range(1,m+1):
            coeff=sum((F((-1)**(s-1-j)*comb(s-1,j),m-s+1+j)
                       for j in range(s)),F(0))
            assert coeff==F((-1)**(s-1),s*comb(m,s))
            differences+=1
    parity=[]
    for m in range(1,5):
        p=m+1
        even={B:1 for B in range(1,1<<p) if B.bit_count()%2==0}
        odd={B:1 for B in range(1,1<<p) if B.bit_count()%2==1}
        checked=check_game(even,odd,p,m)
        assert sum(odd.values())-sum(even.values())==1
        parity.append({'m':m,'p':p,'ordered_payoff_checks':checked})
    # Explicit rational-cone elimination witness: all 15 types of four labels
    # reduce to eight odd types with multiplicity two for the two-player table.
    p,m=4,2
    original={B:1 for B in range(1,1<<p)}
    compressed={B:2 for B in range(1,1<<p) if B.bit_count()%2}
    checks=check_game(original,compressed,p,m)
    assert len(compressed)==8<=sum(comb(p,s) for s in range(1,m+1))
    for a,b in product(range(p),repeat=2):
        before=sum(v for B,v in original.items() if bool(B>>a&1)!=bool(B>>b&1))
        after=sum(v for B,v in compressed.items() if bool(B>>a&1)!=bool(B>>b&1))
        assert before==after
    return {'status':'independently checked; no fatal objection',
            'full_rank_cases':ranks,'finite_difference_identities':differences,
            'parity_checks':parity,'explicit_compression':{'before':15,'after':8,'ordered_payoff_checks':checks},
            'general_half':'OPEN; representation theorem only'}


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    r=run()
    if args.output:
        with args.output.open('x') as stream:
            json.dump(r,stream,ensure_ascii=False,indent=2)
            stream.write('\n')
    print(json.dumps(r,ensure_ascii=False))
