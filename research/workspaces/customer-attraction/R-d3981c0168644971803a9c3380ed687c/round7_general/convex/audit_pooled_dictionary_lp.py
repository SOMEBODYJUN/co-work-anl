"""Independent exact resource-menu audit for the finite dictionary LP example.

No author script, repository SPE solver, or numerical LP solver is imported.
All next-action/grandchild menus are reconstructed from the original three
provider equal-sharing definition. Finite line arrangements certify the H
formulas on their entire half-line, not only on a sample of prices.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

def payoff(z,who,value):
    return F(value,z.count(z[who]))

def menus(resources,value,role):
    old=() if role==0 else (0,)
    groups=[]
    for A in range(resources):
        by_next=[]
        for B in range(resources):
            if role==0:
                zs=[(A,B,C) for C in range(resources)]
                br=max(payoff(z,2,value) for z in zs)
                zs=[z for z in zs if payoff(z,2,value)==br]
            else:
                zs=[old+(A,B)]
            by_next.append([(payoff(z,role,value),payoff(z,role+1,value)) for z in zs])
        theta=max(min(v for d,v in leafs) for leafs in by_next)
        groups.append(tuple(sorted(set((d,theta-v) for leafs in by_next for d,v in leafs))))
    return tuple(groups)

def H(groups,tau):
    return max(min(intercept+slope*tau for intercept,slope in lines) for lines in groups)

def arrangement(groups):
    lines=sorted(set(line for lines in groups for line in lines))
    grid={F(0)}
    for a,b in product(lines,repeat=2):
        if a[1]!=b[1]:
            x=(b[0]-a[0])/(a[1]-b[1])
            if x>=0:grid.add(x)
    grid=sorted(grid)
    cells=[]
    for j,left in enumerate(grid):
        right=grid[j+1] if j+1<len(grid) else None
        sample=(left+right)/2 if right is not None else left+1
        candidate=next(line for line in lines if line[0]+line[1]*sample==H(groups,sample))
        # All affine line orders are fixed on this open cell. Checking an
        # interior point identifies the full max-min affine branch there.
        assert candidate[0]+candidate[1]*left==H(groups,left)
        if right is not None:assert candidate[0]+candidate[1]*right==H(groups,right)
        if cells and cells[-1]['line']==candidate:
            cells[-1]['right']=right
        else:cells.append(dict(left=left,right=right,line=candidate))
    return cells

def expected_H(label,role,tau):
    if label=='E':return min((1+tau)/2,F(1))
    return 1-tau if role==0 else F(1)

def C(g):
    P=sum(max(x,0) for x in g);N=sum(max(-x,0) for x in g)
    p=max([F(0)]+[max(x,0) for x in g]);v=max([F(0)]+[max(-x,0) for x in g])
    return 2*P-N+p+v

def audit():
    descriptions=[]
    for label,r,value in [('E',3,1),('J',2,2)]:
        for role in (0,1):
            groups=menus(r,value,role);cells=arrangement(groups)
            for cell in cells:
                left,right=cell['left'],cell['right']
                samples=[left,left+1] if right is None else [left,(left+right)/2,right]
                assert all(H(groups,t)==expected_H(label,role,t) for t in samples)
            descriptions.append(dict(component=label,role=role+1,
                    H_cells=[dict(left=str(c['left']),right=None if c['right'] is None else str(c['right']),
                                  intercept=str(c['line'][0]),slope=str(c['line'][1])) for c in cells]))
    # Exact objective pieces and their minima: the common H arrangement is {0,1}.
    pieces=[]
    for lo,hi in [(F(0),F(2,3)),(F(2,3),F(1))]:
        for x in (lo,(lo+hi)/2,hi):
            psi=(max(x,1-x/2),F(1));u=(1-x/2,1-x/2)
            g=tuple(a-b for a,b in zip(psi,u));B=4-3*x
            assert B+C(g)==3+F(3,2)*abs(x-F(2,3))
            oldg=(x/2,x/2)
            assert B+C(oldg)==4-x/2
        pieces.append(dict(left=str(lo),right=str(hi),minimum='3'))
    # Clear the normalized optimizer x=2/3 to E_count=2,J_count=1.
    psi=(F(2),F(3));target=(F(2),F(2),F(4));g=tuple(a-b for a,b in zip(psi,target))
    assert g==(F(0),F(1)) and C(g)==3
    B=6
    assert B+C(g)==9
    assert C(())==0
    return dict(scope='Exact independent finite resource-menu and dictionary-example arithmetic; not a half proof',
                menus=descriptions,common_price_grid=['0','1'],
                normalized_new_min='3',normalized_new_argmin='2/3',normalized_old_min='7/2',normalized_old_argmin='1',
                integer_components=dict(E=2,J=1),target_payoffs=[str(x) for x in target],
                Psi=[str(x) for x in psi],g=[str(x) for x in g],B=str(B),repair_cost=str(C(g)),total='9',
                zero_dimension_cost='0',all_exact_checks=True)

if __name__=='__main__':
    result=audit()
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
