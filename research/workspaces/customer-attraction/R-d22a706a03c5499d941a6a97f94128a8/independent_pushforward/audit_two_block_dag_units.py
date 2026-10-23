"""Definition-level unit-customer audit of the independent two-block DAG.

Does not import the builder, equilibrium solver, numpy, or outcome sets.
Every reachable DAG memory node explicitly supplies all eight transitions.
"""
from fractions import Fraction as F
from functools import lru_cache
import json
from pathlib import Path


def main():
    here=Path(__file__).resolve().parent
    raw=json.loads((here/'two_block_integer_bi_certificate.json').read_text())
    m,k=raw['players'],raw['topics']
    assert (m,k)==(8,8)
    expected_types=[(mask<<shift,w) for shift in (0,4)
                    for mask,w in [(1,2),(10,4),(5,6),(12,3),(15,1)]]
    assert raw['customer_types']==[list(z) for z in expected_types]
    customers=[]
    for mask,multiplicity in raw['customer_types']:
        assert isinstance(mask,int) and 0<mask<1<<k
        assert isinstance(multiplicity,int) and multiplicity>0
        customers.extend([tuple(a for a in range(k) if mask>>a&1)]*multiplicity)
    assert len(customers)==32
    nodes=raw['nodes'];terminals=[tuple(q) for q in raw['terminals']]
    seen={};decisions=0;comparisons=0

    @lru_cache(None)
    def utility(q,a):
        answer=F(0)
        for interest in customers:
            if a in interest:
                load=sum(q[z] for z in interest)
                assert load>0
                answer+=F(1,load)
        return answer

    @lru_cache(None)
    def insertion(q,a):
        return sum((F(1,1+sum(q[z] for z in interest))
                    for interest in customers if a in interest),F(0))

    def audit(node):
        nonlocal decisions,comparisons
        q=tuple(node['counts'])
        assert len(q)==k and all(isinstance(x,int) and x>=0 for x in q)
        assert sum(q)<=m
        if sum(q)==m:
            assert node['action'] is None and node['children']==[]
            assert terminals[node['target']]==q
            return q
        decisions+=1
        assert len(node['children'])==k
        leaves=[]
        for a,nid in enumerate(node['children']):
            assert isinstance(nid,int) and 0<=nid<len(nodes)
            child=nodes[nid];wanted=list(q);wanted[a]+=1
            assert child['counts']==wanted
            if nid not in seen:seen[nid]=audit(child)
            leaves.append(seen[nid])
        chosen=node['action']
        assert isinstance(chosen,int) and 0<=chosen<k
        actual=leaves[chosen]
        assert terminals[node['target']]==actual
        own=utility(actual,chosen)
        for a,alternative in enumerate(leaves):
            assert own>=utility(alternative,a)
            comparisons+=1
        return actual

    actual=audit(raw['root']);u=utility(actual,raw['root']['action'])
    assert len(seen)==len(nodes)
    rootmenu=[seen[nid] for nid in raw['root']['children']]
    K=[[insertion(rootmenu[b],a) for b in range(k)] for a in range(k)]
    maxima=[max(K[a][b] for a in range(k)) for b in range(k)]
    assert all(z>u for z in maxima)
    Q=[F(0),F(0),F(1,14),F(3,7)]*2
    assert sum(Q)==1
    caps=[sum((K[a][b]*Q[b] for b in range(k)),F(0)) for a in range(k)]
    assert caps==[F(577,210),F(67,35),F(851,280),F(851,280)]*2
    assert max(caps)<u
    p=[F(0),F(0),F(2,7),F(3,14)]*2
    assert sum(p)==1
    dual=[sum((p[a]*K[a][b] for a in range(k)),F(0)) for b in range(k)]
    assert dual==[F(443,140),F(443,140),F(851,280),F(851,280)]*2
    assert min(dual)==max(caps)
    assert all(not Q[a] or caps[a]==max(caps) for a in range(k))
    report={'valid_complete_DAG_SPE':True,'customers':len(customers),
            'DAG_nodes_including_root':len(nodes)+1,'DAG_decision_nodes':decisions,
            'DAG_action_comparisons_including_chosen':comparisons,
            'actual_counts':list(actual),'root_utility':str(u),
            'root_deviation_utilities':[str(utility(q,b)) for b,q in enumerate(rootmenu)],
            'pure_column_max_query':[str(z) for z in maxima],
            'mixed_cap_distribution':list(map(str,Q)),
            'mixed_cap_query_values':list(map(str,caps)),
            'mixed_cap_value':str(max(caps)),
            'mixed_cap_slack':str(u-max(caps)),
            'matching_query_dual':list(map(str,p)),
            'dual_column_values':list(map(str,dual)),
            'exact_M_full':str(max(caps)),
            'Q_is_symmetric_meta_Nash':True}
    (here/'two_block_dag_unit_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
