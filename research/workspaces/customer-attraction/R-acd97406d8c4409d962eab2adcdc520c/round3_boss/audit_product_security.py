"""Independent exact audit of the disjoint-singleton product-security gap.

No customer-attraction solver, optimization package or sibling script is used.
Finite checks corroborate the symbolic proof; they do not prove its quantifiers.
"""
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
import json
from pathlib import Path
import random


def compositions(total, length):
    if length==1:
        yield (total,)
    else:
        for first in range(total+1):
            for tail in compositions(total-first,length-1):
                yield (first,*tail)


def payoffs(rows):
    n=len(rows[0]);values=[]
    for j in range(n):
        law=[F(1)]
        for row in rows:
            q=row[j];new=[F(0)]*(len(law)+1)
            for k,p in enumerate(law):
                new[k]+=p*(1-q);new[k+1]+=p*q
            law=new
        assert sum(law)==1
        values.append(sum((p/F(k+1) for k,p in enumerate(law)),F()))
    return values


def check(rows):
    n=len(rows[0]);r=n-1
    assert len(rows)==r and all(sum(row)==1 for row in rows)
    values=payoffs(rows);cap=max(values);v=F(n+1,2*n)
    gap=F(r*(n-2),2*n*n*(n*n+2*r*r))
    delta=cap-v
    assert delta>=gap
    lam=[sum(row[j] for row in rows) for j in range(n)]
    collision=sum((sum(rows[i][j]*rows[k][j] for j in range(n))
                   for i in range(r) for k in range(i+1,r)),F())
    assert collision==F(1,2)*(sum(x*x for x in lam)-sum(x*x for row in rows for x in row))
    assert delta>=collision/F(n*n)
    if delta<F(1,2*r*n):
        bound=F(r,n)+2*r*delta
        assert F(1,2)<=bound<1
        assert all(F(r,n)-2*delta<=x<=bound for x in lam)
        assert all(sum(x*x for x in row)<=bound*bound+(1-bound)**2 for row in rows)
        assert collision>=F(r,2)*(F(n-2,n*n)-4*r*delta)
    return delta


def main():
    exact_games=0;static_backgrounds=0;integer_rows=0
    # Static lower certificate: uniform query; equality iff all opponents differ.
    for n in range(1,11):
        r=n-1;v=F(n+1,2*n)
        if n<=7:
            for counts in compositions(r,n):
                avg=sum((F(1,k+1) for k in counts),F())/n
                assert avg>=v
                assert (avg==v)==all(k<=1 for k in counts)
                static_backgrounds+=1
        # Matching correlated dual: omit one uniform theme, all others once.
        dual=sum((F(1,1+int(j!=0)) for j in range(n)),F())/n
        assert dual==v
        # Pointwise collision remainder, including k=0 and all-equal opponents.
        for k in range(r+1):
            excess=F(1,k+1)-(1-F(k,2))
            assert excess==F(k*(k-1),2*(k+1))
            assert excess>=F(k*(k-1),2*n)
            integer_rows+=1
    for n,denominator in ((3,4),(4,2)):
        simplex=[tuple(F(x,denominator) for x in v) for v in compositions(denominator,n)]
        for rows in product(simplex,repeat=n-1):
            check(rows);exact_games+=1
    rng=random.Random(6222026)
    for n in range(3,15):
        r=n-1
        for _ in range(50):
            rows=[]
            for i in range(r):
                raw=[rng.randrange(0,11) for _ in range(n)]
                if not sum(raw):raw[0]=1
                rows.append(tuple(F(x,sum(raw)) for x in raw))
            check(rows);exact_games+=1
        b=F(r*(n-2),2*n*n*(n*n+2*r*r))
        assert 0<b<F(1,2*r*n)
    return {'status':'passed','arithmetic':'fractions.Fraction',
            'independence':'no solver, optimization or sibling import',
            'product_games':exact_games,'static_backgrounds':static_backgrounds,
            'pointwise_integer_rows':integer_rows,
            'seed':6222026,'general_gap':'(n-1)(n-2)/(2 n^2 (n^2+2(n-1)^2))',
            'n3_gap':str(F(1,153)),
            'scope':'finite implementation audit; the universal theorem uses its analytic proof'}


if __name__=='__main__':
    result=main();out=Path(__file__).with_name('product_security_audit.json')
    out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
