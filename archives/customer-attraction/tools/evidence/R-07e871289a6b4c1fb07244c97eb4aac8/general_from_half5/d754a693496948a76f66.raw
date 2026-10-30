#!/usr/bin/env python3
"""Standard-library exact addendum; frozen refinement assets are read only."""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import json
import math
import sys

from six_copy_refine import bridge_system,decode,add_query_family


def early_cap_checks(result):
    m=result['m'];types,rows=bridge_system(m);n=decode(result,types)
    checks=[]
    for source in range(m-2):
        def psi(a,t,q,source=source):
            denominator=sum(a[:source])+m-source-1
            return F(t,denominator)+F(q,denominator+t)
        new=[]
        add_query_family(new,types,m,f'earlycapacity:{source+1}',source,psi,1)
        values=[(sum(x*y for x,y in zip(row,n)),name) for name,row in new]
        value,name=min(values)
        assert value>=0
        checks.append({'source':source+1,'n_rows':len(new),'min_slack':str(value),'min_row':name})
    return {'extension_rows':sum(r['n_rows'] for r in checks),'total_rows':result['n_rows']+sum(r['n_rows'] for r in checks),'exact_optimum_unchanged':result['W'],'per_source':checks}


def visible_tail_checks(result):
    m=result['m'];assert m==6
    assert all(s['d']==1 for s in result['support'])
    D=math.lcm(*(m*F(s['weight']).denominator for s in result['support']))
    groups=[]
    for s in result['support']:
        a=tuple(map(int,s['actual_bits']));weight=D*F(s['weight'])/m
        assert weight.denominator==1
        for j in range(m):groups.append((sum(x<<i for i,x in enumerate(a))|(1<<(m+j)),int(weight)))
    @lru_cache(None)
    def utility(profile):
        out=[0]*m
        for mask,weight in groups:
            covered=[bool(mask&(1<<q)) for q in profile];c=sum(covered)
            if c:
                for i,yes in enumerate(covered):
                    if yes:out[i]+=weight*(60//c)
        return tuple(out)
    @lru_cache(None)
    def spe_outcomes(prefix):
        i=len(prefix)
        if i==m:return (prefix,)
        branches=[spe_outcomes(prefix+(q,)) for q in range(2*m)]
        # Each off-action subgame may use any pure SPE to minimize this
        # mover's payoff. An on-action outcome is implementable exactly when
        # its payoff clears all these punishment minima.
        threshold=max(min(utility(p)[i] for p in branch) for branch in branches)
        return tuple(p for branch in branches for p in branch if utility(p)[i]>=threshold)
    actual=tuple(range(m));actual_u=utility(actual)
    name=lambda q:f'A{q+1}' if q<m else f'T{q-m+1}'
    sources=[]
    for i in [4,3,2]:
        prefix=tuple(range(i))+(m-1,)
        outcomes=spe_outcomes(prefix)
        low=min(utility(p)[i] for p in outcomes)
        high=max(utility(p)[i] for p in outcomes)
        arg=next(p for p in outcomes if utility(p)[i]==low)
        gain=F(low-actual_u[i],60*D)
        assert gain>0
        sources.append({'source':i+1,'forced_theme':'A6','tail_players':m-i-1,'full_leaf_count':(2*m)**(m-i-1),'number_of_SPE_outcomes':len(outcomes),'minimum_gain_normalized':str(gain),'maximum_gain_normalized':str(F(high-actual_u[i],60*D)),'minimum_gain_outcome':[name(q) for q in arg]})
    visible_sizes=[sum(F(s['weight']) for s in result['support'] if s['actual_bits'][j]=='1') for j in range(m)]+[F(1,m)]*m
    realK=max(visible_sizes)
    assert realK<F(result['K'])
    return {'integer_scale_D':str(D),'formal_relaxation_K':result['K'],'visible_catalog_true_K':str(realK),'actual_normalized_payoffs':[str(F(v,60*D)) for v in actual_u],'copy_A6_diagnosis':sources}


if __name__=='__main__':
    folder=Path(__file__).parent
    result=json.loads((folder/'six_copy_free_results.json').read_text())['final']
    data={'early_capacity':early_cap_checks(result),'visible_catalog_tail':visible_tail_checks(result)}
    target=folder/'six_copy_extra_checks.json'
    if '--verify' in sys.argv:
        assert json.loads(target.read_text())==data
    else:target.write_text(json.dumps(data,indent=2)+'\n')
    print('EXACT VERIFIED',data['early_capacity']['extension_rows'],'early capacity rows; 3 finite SPE tail diagnoses')
