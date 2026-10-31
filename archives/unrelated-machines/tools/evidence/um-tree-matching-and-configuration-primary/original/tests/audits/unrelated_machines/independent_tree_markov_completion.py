#!/usr/bin/env python3
"""Independent exact audit of five-machine forest Markov completion obstruction."""
from fractions import Fraction as F
from itertools import product
import json


P={
    'a':{1:F(1),2:F(1,2)},'b':{2:F(1,2),3:F(1)},
    'd':{3:F(1),4:F(1,2)},'e':{4:F(1,2),5:F(1)},
    'c':{1:F(1),5:F(1)}}
A={1:frozenset('c'),2:frozenset('ab'),3:frozenset(),4:frozenset('d'),5:frozenset('e')}
B={1:frozenset('a'),2:frozenset('b'),3:frozenset(),4:frozenset('de'),5:frozenset('c')}
SOURCE=[(A,F(1,2)),(B,F(1,2))]
PATH=[(1,2,'a'),(2,3,'b'),(3,4,'d'),(4,5,'e')]


def loads(assignment):
    result={i:F(0) for i in range(1,6)}
    for j,i in assignment.items():
        result[i]+=P[j][i]
    return result


def gluing():
    singleton={i:{} for i in range(1,6)}
    pair={}
    for state,w in SOURCE:
        for i,s in state.items():
            singleton[i][s]=singleton[i].get(s,F(0))+w
        for u,v,j in PATH:
            pair.setdefault((u,v),{})
            key=(state[u],state[v])
            pair[u,v][key]=pair[u,v].get(key,F(0))+w
    states=[({1:s},w) for s,w in singleton[1].items()]
    for u,v,j in PATH:
        new=[]
        for current,w in states:
            for (su,sv),pw in pair[u,v].items():
                if su == current[u]:
                    new.append((current|{v:sv},w*pw/singleton[u][su]))
        states=new
    assert sum(w for _,w in states)==1
    for i,marginal in singleton.items():
        check={}
        for state,w in states:
            check[state[i]]=check.get(state[i],F(0))+w
        assert check==marginal
    for u,v,j in PATH:
        check={}
        for state,w in states:
            key=(state[u],state[v])
            check[key]=check.get(key,F(0))+w
        assert check==pair[u,v]
    return states


def audit():
    source=[]
    for state,w in SOURCE:
        assignment={j:i for i,s in state.items() for j in s}
        assert len(assignment)==len(P)
        assert sum(len(s) for s in state.values())==len(P)
        assert max(loads(assignment).values())==1
        source.append({'probability':str(w),'maximum_load':'1'})
    jobs=list(P)
    best=None
    count=0
    for locations in product(*(tuple(P[j]) for j in jobs)):
        count+=1
        value=max(loads(dict(zip(jobs,locations))).values())
        best=value if best is None else min(best,value)
    assert best==1
    records=[]
    bad_mass=F(0)
    for state,w in gluing():
        partial={}
        for u,v,j in PATH:
            assert (j in state[u])+(j in state[v])==1
            partial[j]=u if j in state[u] else v
        partial_loads=loads(partial)
        completions=[]
        for i in P['c']:
            value=max(loads(partial|{'c':i}).values())
            completions.append(value)
        optimum_completion=min(completions)
        if optimum_completion==2:
            bad_mass+=w
        records.append({'full_local_states':{str(i):''.join(sorted(s)) for i,s in state.items()},
                        'probability':str(w),'frozen_assignment':partial,
                        'frozen_loads':{str(i):str(x) for i,x in partial_loads.items()},
                        'best_completion':str(optimum_completion)})
    assert bad_mass==F(1,4)
    return {'source_global_schedules':source,'independent_complete_assignments_enumerated':count,
            'integer_optimum':str(best),'glued_support':records,
            'probability_of_best_completion_2':str(bad_mass),
            'numeric_policy':'exact Fraction arithmetic and full integer assignment enumeration'}


if __name__=='__main__':
    print(json.dumps(audit(),indent=2))
