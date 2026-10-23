"""Exact coefficient audit; finite replay supplements the symbolic proof.

No CAG equilibrium is asserted for the middle-incidence menu obstruction.
All zero-numerator uncovered terms are defined as zero before division.
"""
from fractions import Fraction as F
from pathlib import Path
import json


def delta(N, b, included, tail_load):
    if not included and not tail_load:
        return F(0)
    return F(N*included-tail_load, N*(b+included+tail_load))


def run():
    checks = 0
    for N in range(1, 11):
        for b in range(7):
            assert delta(N, b, 1, 0) == F(1, b+1)
            for K in range(N+1):
                assert delta(N,b,1,K) >= 0
                assert delta(N,b,0,K) >= -F(1,b+N)
                checks += 2
            for n in range(N+1):
                for K in range(n+1):
                    assert delta(N,b,0,K) >= -F(n,N*(b+1))
                    checks += 1
                for K in range(N-n+1):
                    assert delta(N,b,1,K) >= F(n,N*(b+N))
                    # Exact nonnegative numerator, using n integer.
                    h=N-n-K
                    lhs=(N-K)*(b+N)-n*(b+1+K)
                    rhs=n*(n-1)+h*(b+N+n)
                    assert lhs == rhs and rhs >= 0
                    checks += 2
    obstructions=[]
    for N in [2,3,5,11]:
        # Rows are destinations, columns forced root maximal themes.
        M=((0,N-1,1,0),(N-1,0,0,1),(1,0,0,N-1),(0,1,N-1,0))
        assert all(sum(M[j][i] for j in range(4)) == N for i in range(4))
        assert all(sum(M[j][i] for i in range(4)) == N for j in range(4))
        for b in [0,1,7]:
            loads=[sum(M[j][i] for j in [0,1]) for i in range(4)]
            ds=[delta(N,b,int(i in [0,1]),loads[i]) for i in range(4)]
            avg=sum(ds,F(0))/4
            formula=-F(N-1,2*N*(b+N)*(b+1))
            assert avg == formula < 0
            obstructions.append({'r':N+1,'background':b,'counts':M,
                                 'tail_loads':loads,'delta':list(map(str,ds)),
                                 'stationary_average':str(avg)})
    # Integer optimal loads are essential to the background profit bound.
    profit_checks=0
    for b in range(7):
        for c in range(1,11):
            for d in range(11):
                gap=F(c+d,b+d+1)-F(c,b+c)
                assert gap == F(c*(c-1)+b*d,(b+d+1)*(b+c)) >= 0
                profit_checks += 1
    return {'scope':'coefficient identities and schematic menus only; not an SPE search',
            'coefficient_checks':checks,'profit_checks':profit_checks,
            'middle_incidence_obstructions':obstructions}


if __name__ == '__main__':
    result=run()
    target=Path(__file__).with_suffix('.json')
    target.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='middle_incidence_obstructions'}))
    print('first_middle_gap='+result['middle_incidence_obstructions'][0]['stationary_average'])
