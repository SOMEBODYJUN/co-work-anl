"""Attack credible-threshold path prices through independent SPE menu forests.

Each path node has p independent credible child strategies. No claim that
the arbitrary path is itself SPE is imposed or needed. LPs generate points;
only exact nonnegative integer recovery plus fresh BI can certify failure.
"""
from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import json
import sys
import numpy as np
from scipy.optimize import linprog

import credible_floor_path as cp
ROOT=cp.ROOT
sys.path.insert(0,str(ROOT/'tests/audits'))
from customer_attraction_strategy_lp import payoff_row, coverage_row, dot, integer_clones, instance_from_clones


class Forest:
    def __init__(self,instance,path):
        self.instance=instance
        self.solver=cp.ExactSPESolver(instance)
        self.p,self.m=instance.topic_count,instance.players
        self.path=tuple(path)
        self.rows=set()
        self.menu=[]
        self.seen=set()
        k=(0,)*self.p
        for i,a in enumerate(self.path):
            for b,d in cp.increments(k):
                q=min(self.solver.outcomes(d),key=lambda q:(self.solver._utility(q,b),q))
                self.menu.append((i,k,b,q))
                self.expand(d,q)
            k=k[:a]+(k[a]+1,)+k[a+1:]
        self.rows=tuple(sorted(self.rows))

    def expand(self,k,q):
        if sum(k)==self.m or (k,q) in self.seen:
            return
        self.seen.add((k,q))
        floor=self.solver.threshold(k)
        a=min(a for a,d in cp.increments(k)
              if q in self.solver.outcomes(d) and self.solver._utility(q,a)>=floor)
        actual=payoff_row(self.p,q,a)
        for b,d in cp.increments(k):
            child=q if a==b else min(self.solver.outcomes(d),key=lambda t:(self.solver._utility(t,b),t))
            row=tuple(x-y for x,y in zip(actual,payoff_row(self.p,child,b)))
            if any(row):self.rows.add(row)
            self.expand(d,child)

    def optimize(self,support):
        n=(1<<self.p)-1
        rows=[tuple(-x for x in row)+(Fraction(0),)*self.m for row in self.rows]
        for i,k,a,q in self.menu:
            tail=tuple(Fraction(-int(j==i)) for j in range(self.m))
            rows.append(payoff_row(self.p,q,a)+tail)
        eq=(Fraction(0),)*n+(Fraction(1),)*self.m
        objective=coverage_row(self.p,support)+(Fraction(0),)*self.m
        res=linprog(-np.array(objective,dtype=float),A_ub=np.array(rows,dtype=float),
                    b_ub=np.zeros(len(rows)),A_eq=np.array([eq],dtype=float),b_eq=[1],
                    bounds=(0,None),method='highs')
        if not res.success:
            return {'status':res.message}
        values=tuple(Fraction(float(v)).limit_denominator(10**6) for v in res.x)
        exact=(dot(eq,values)==1 and all(dot(row,values)<=0 for row in rows))
        # A failed recovery has no mathematical status. Decimal vertices are
        # only proposal points; no epsilon is accepted as an SPE comparison.
        return {'float':float(-res.fun),'exact':exact,
                'value':str(dot(objective,values)) if exact else None,
                'clones':integer_clones(values[:n]) if exact else None,
                'prices':[str(v) for v in values[n:]] if exact else None,
                'support':support,'forest_rows':len(self.rows)}


def min_path(instance):
    solver=cp.ExactSPESolver(instance)
    @lru_cache(None)
    def lower(k):
        if sum(k)==instance.players:return Fraction(0),()
        v,path=min((lower(d)[0],(a,)+lower(d)[1]) for a,d in cp.increments(k))
        return solver.threshold(k)+v,path
    return lower((0,)*instance.topic_count)


def seeds():
    for f in sorted((ROOT/'examples/customer_attraction').glob('*.json')):
        try:I=cp.Instance.from_dict(json.loads(f.read_text()))
        except (ValueError,KeyError,TypeError):continue
        if I.topic_count<=7 and I.players<=6:
            yield f.name,I
    I=cp.Instance(('A','B','C','D','E','F'),tuple(cp.CustomerType(frozenset(a for a in range(6) if mask>>a&1),n)
          for mask,n in [(1,30),(2,7),(4,5),(8,7),(20,2),(36,2),(50,6),(52,4),(56,6)]),4)
    yield '69-floor-counterexample',I


def main():
    records=[]
    for name,instance in seeds():
        value,path=min_path(instance)
        forest=Forest(instance,path)
        best=None
        for support in combinations(range(instance.topic_count),min(instance.topic_count,instance.players)):
            result=forest.optimize(support)
            if best is None or result.get('float',-1)>best.get('float',-1):best=result
        best.update({'name':name,'path':path,'seed_L':str(value)})
        records.append(best)
        print(json.dumps(best),flush=True)
        if best.get('exact') and Fraction(best['value'])>2:
            endpoint=instance_from_clones(instance.topic_count,instance.players,best['clones'])
            result=cp.diagnostic(endpoint)
            records[-1]['endpoint']=endpoint.to_dict()
            records[-1]['exact_fresh_BI']=result
            print(json.dumps({'COUNTEREXAMPLE':records[-1]}),flush=True)
            break
    (Path(__file__).parent/'credible_path_menu_cone_results.json').write_text(json.dumps(records,indent=2)+'\n')


if __name__=='__main__':main()
