"""Independent Fraction audit of triangular class-order potentials."""
from fractions import Fraction as F
from itertools import product
from math import comb,expm1,log
from pathlib import Path
from random import Random
import hashlib
import json


SOURCE=Path(__file__).resolve().parents[4] / 'research/current/weighted_congestion/weight_bands/finite_weight_class_potentials.md'


def cost(coeff,x):
    return sum((a*x**j for j,a in enumerate(coeff)),F(0))


def shifted(coeff,background):
    return [sum((coeff[j]*comb(j,r)*background**(j-r)
                 for j in range(r,len(coeff))),F(0)) for r in range(len(coeff))]


def order(k,r):
    return list(range(k-1,r,-1))+list(range(r+1))


def ordered(counts,weights,coeff,permutation):
    total=F(0);load=F(0)
    for j in permutation:
        for _ in range(counts[j]):
            load+=weights[j]
            total+=weights[j]*cost(coeff,load)
    return total


def parameters(d,k,upper_a):
    t=F(d-1)/upper_a
    unnormalized=[t**r for r in range(k)]
    total=sum(unnormalized,F(0))
    assert total<=upper_a
    lam=[v/total for v in unnormalized]
    assert sum(lam)==1 and all(v>0 for v in lam)
    cumulative=[sum(lam[:i+1],F(0)) for i in range(k)]
    for i in range(k):
        assert 1+F(d-1)*sum(lam[:i],F(0))<=upper_a*cumulative[i]
    return lam,cumulative,total==upper_a


def mixed(counts,weights,coeff,lam):
    return sum((lam[r]*ordered(counts,weights,coeff,order(len(weights),r))
                for r in range(len(weights))),F(0))


def resource_checks(d,k,a,rng):
    lam,cumulative,is_exact=parameters(d,k,a)
    comparisons=0
    for trial in range(10):
        weights=[F(1,10**(3*i)) for i in range(k)] if trial==0 else [
            F((k-i)*rng.randrange(1,8),rng.randrange(1,10)) for i in range(k)]
        weights=sorted(set(weights),reverse=True)
        if len(weights)!=k:weights=[F(1,13**i) for i in range(k)]
        counts=[rng.randrange(0,5) for _ in range(k)]
        coeff=[F(0)]*(d+1)
        for degree in {0,1,d}:coeff[degree]=F(rng.randrange(0,5),rng.randrange(1,8))
        if trial==1:coeff=[F(0)]*(d+1)
        old=mixed(counts,weights,coeff,lam)
        for i,w in enumerate(weights):
            after=list(counts);after[i]+=1
            y=sum((after[j]*weights[j] for j in range(k)),F(0))
            fee=cost(coeff,y)
            for r in range(k):
                delta=ordered(after,weights,coeff,order(k,r))-ordered(counts,weights,coeff,order(k,r))
                if r<i:assert w*fee<=delta<=d*w*fee
                elif r==i:assert delta==w*fee
                else:assert 0<=delta<=w*fee
                comparisons+=1
            change=mixed(after,weights,coeff,lam)-old
            h=cumulative[i]*w
            assert h*fee<=change<=a*h*fee
    return comparisons,is_exact


def game_checks(d,k,a,rng,rounding):
    lam,cumulative,_=parameters(d,k,a)
    representatives=[F(1,7**i) for i in range(k)]
    mobile_types=list(range(k))
    if k<=2:mobile_types+=list(range(k))
    rr=F(101,100) if rounding else F(1)
    actual=[representatives[j]*(1+(rr-1)*F(rng.randrange(0,9),8)) for j in mobile_types]
    strategies=[]
    for i,j in enumerate(mobile_types):
        if i%2==0:strategies.append([frozenset({0}),frozenset({0,1+i%3})])
        else:strategies.append([frozenset(),frozenset({1+i%3})])
    # Three unique-strategy background players of arbitrary distinct weights;
    # their weights are not counted in k and need not lie in any mobile cluster.
    fixed=[(F(11,13),frozenset({0,2})),(F(17),frozenset({1})),
           (F(999,31),frozenset())] if rounding else []
    background=[sum((w for w,s in fixed if e in s),F(0)) for e in range(4)]
    coefficients=[]
    for e in range(4):
        coeff=[F(0)]*(d+1)
        if e!=2:
            coeff[0]=F(e,7);coeff[1]=F(1,e+1);coeff[d]=F(2,e+2)
        coefficients.append(coeff)
    rows={};load_checks=0
    for state in product([0,1],repeat=len(mobile_types)):
        cp=[F(0)]*len(mobile_types);co=[F(0)]*len(mobile_types);phi=F(0)
        for e,coeff in enumerate(coefficients):
            users=[i for i in range(len(mobile_types)) if e in strategies[i][state[i]]]
            counts=[sum(mobile_types[i]==j for i in users) for j in range(k)]
            xp=background[e]+sum((representatives[mobile_types[i]] for i in users),F(0))
            xo=background[e]+sum((actual[i] for i in users),F(0))
            assert xp<=xo<=rr*xp
            fee_p=cost(coeff,xp);fee_o=cost(coeff,xo)
            assert fee_p<=fee_o<=rr**d*fee_p
            coeff_shift=shifted(coeff,background[e])
            assert all(v>=0 for v in coeff_shift)
            load= xp-background[e]
            assert cost(coeff_shift,load)==fee_p
            phi+=mixed(counts,representatives,coeff_shift,lam)
            for i in users:cp[i]+=fee_p;co[i]+=fee_o
            load_checks+=1
        rows[state]=(phi,cp,co)
    edges=improvements=localmins=0
    for state,(phi,cp,co) in rows.items():
        is_min=True
        for i in range(len(mobile_types)):
            nxt=list(state);nxt[i]^=1;nxt=tuple(nxt)
            phip,cpp,cop=rows[nxt]
            h=cumulative[mobile_types[i]]*representatives[mobile_types[i]]
            assert phip-phi<=h*(a*cpp[i]-cp[i])
            if cp[i]>a*cpp[i]:
                assert phip<phi
                improvements+=1
            is_min &= phip>=phi
            edges+=1
        if is_min:
            localmins+=1
            for i in range(len(mobile_types)):
                nxt=list(state);nxt[i]^=1
                assert cp[i]<=a*rows[tuple(nxt)][1][i]
                assert co[i]<=rr**d*a*rows[tuple(nxt)][2][i]
    return len(rows),edges,improvements,localmins,load_checks


def affine_checks():
    count=0
    for x,w,ell,beta in product([F(0),F(1,7),F(9)],
                                [F(1,100),F(1),F(13)],
                                [F(0),F(2,5),F(11)],
                                [F(0),F(1,8),F(9)]):
        assert ell*((x+w)**2-x*x+w*w)/2+beta*w==w*(ell*(x+w)+beta)
        count+=1
    return count


def main():
    rng=Random(195011)
    exact=[]
    for k,t in [(1,1),(2,1),(2,2),(3,1),(3,2),(4,1),(4,2),(5,1)]:
        a=F(sum(t**j for j in range(k)))
        d=1+t*a
        assert d.denominator==1
        exact.append((int(d),k,a))
    upper=[(2,3,F(19,10)),(2,5,F(199,100)),(2,8,F(1999,1000))]
    total_comparisons=0;totals=[0]*5;exact_count=0
    for d,k,a in exact+upper:
        comparisons,is_exact=resource_checks(d,k,a,rng)
        total_comparisons+=comparisons;exact_count+=is_exact
        for rounding in [False,True]:
            totals=[x+y for x,y in zip(totals,game_checks(d,k,a,rng,rounding))]
    diagnostics=0
    for d in range(16,10001):
        for k in range(1,int(log(d)/log(log(d)))+1):
            b=(d-1)/expm1(log(d)/k)
            assert b<=2*d/log(d)*(1+1e-12)
            diagnostics+=1
    print(json.dumps({
        'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'seed':195011,'exact_rational_root_parameters':[[d,k,str(a)] for d,k,a in exact],
        'normalized_rational_upper_root_parameters':[[d,k,str(a)] for d,k,a in upper],
        'exact_root_parameter_count':exact_count,
        'individual_triangular_order_insertions':total_comparisons,
        'finite_game_states':totals[0],'finite_game_deviations':totals[1],
        'strict_potential_improvements':totals[2],'potential_local_minima':totals[3],
        'background_shift_rounding_resource_checks':totals[4],
        'affine_endpoint_checks':affine_checks(),
        'log_corollary_float_diagnostic_cases':diagnostics,
        'truth_scope':'finite implementation audit; general proof carries algebraic roots and all real inputs'
    },indent=2))


if __name__=='__main__':main()
