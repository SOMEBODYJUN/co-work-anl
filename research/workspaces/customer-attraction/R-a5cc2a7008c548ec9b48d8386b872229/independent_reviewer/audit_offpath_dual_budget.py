"""Definition-level DAG SPE audit and exact offpath-static-dual diagnostics.

Reads an existing full-strategy packet, writes only this research workspace.
No canonical SPE solver, verifier, discovery code, or floating LP is imported.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
from math import lcm
import gzip,json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
SOURCE=ROOT/'research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_k10_packet.json.gz'

def main():
    packet=json.loads(gzip.decompress(SOURCE.read_bytes()))
    ins=packet['instance'];m=ins['players'];p=len(ins['topics'])
    customers=[frozenset(t['topics']) for t in ins['customers'] for _ in range(t['multiplicity'])]
    assert all(isinstance(t['multiplicity'],int) and t['multiplicity']>0 for t in ins['customers'])
    scale=lcm(*range(1,m+1))
    @lru_cache(None)
    def utility(q):
        answer=[0]*p
        for likes in customers:
            c=sum(q[a] for a in likes)
            if c:
                for a in likes:answer[a]+=scale//c
        return tuple(answer)
    nodes=packet['nodes'];root=packet['root'];seen=set();stack=[root]
    depths={}
    while stack:
        v=stack.pop()
        if v in seen:continue
        seen.add(v);node=nodes[v];q=node['counts'];d=sum(q);depths[v]=d
        assert len(q)==p and all(isinstance(n,int) and n>=0 for n in q) and d<=m
        if d==m:
            assert node.get('terminal') is True and 'children' not in node
        else:
            assert len(node['children'])==p and 0<=node['action']<p
            for a,w in enumerate(node['children']):
                child=list(q);child[a]+=1
                assert nodes[w]['counts']==child
                stack.append(w)
    assert seen==set(range(len(nodes))) and nodes[root]['counts']==[0]*p
    terminal={};comparison_count=0;min_slack=None
    for v in sorted(seen,key=lambda v:depths[v],reverse=True):
        n=nodes[v]
        if depths[v]==m:terminal[v]=tuple(n['counts']);continue
        a=n['action'];terminal[v]=terminal[n['children'][a]]
        current=utility(terminal[v])[a]
        for b,w in enumerate(n['children']):
            difference=current-utility(terminal[w])[b]
            assert difference>=0,(v,b,difference)
            min_slack=difference if min_slack is None else min(min_slack,difference)
            comparison_count+=1
    q=terminal[root];path=[];v=root
    while depths[v]<m:
        a=nodes[v]['action'];path.append(a);v=nodes[v]['children'][a]
    actual_support={a for a,n in enumerate(q) if n}
    C=[bool(sum(q[a] for a in t)) for t in customers]
    W=sum(C)
    all_topics=set(range(p))
    assert all(t & {0,1,2,5} for t in customers)
    OPT=len(customers)
    query=2 # T
    missing=[t for t,c in zip(customers,C) if not c and query in t]
    K=len(missing);beta=F(2*W,2*m-1)
    def value(a,opponent):
        return sum((F(1,1+sum(opponent[b] for b in t)) for t in customers if a in t),F(0))
    deletion=[]
    for a in sorted(actual_support):
        opp=list(q);opp[a]-=1
        vals=[value(t,opp) for t in range(p)]
        assert vals[query]==K
        deletion.append({'deleted_topic':ins['topics'][a], 'opponent_counts':opp,
                         'query_values':[str(x) for x in vals], 'cap':str(max(vals))})
    exact_deletion_cap=min(F(d['cap']) for d in deletion)
    assert exact_deletion_cap==K==3 and beta==F(66,25)
    bounds=[F(2*j+2)-(j+1)*(j+2)*beta/K for j in range(m-1)]
    J_lower=max(F(0),max(bounds))
    assert J_lower==F(6,25)
    # Independent integer support-line identity, not an SPE sample claim.
    harmonic_checks=0
    for r in range(1,65):
        for j in range(r):
            for J in range(r+1):
                lhs=F(1,1+J)-F(2*j+2-J,(j+1)*(j+2))
                rhs=F((J-j)*(J-j-1),(J+1)*(j+1)*(j+2))
                assert lhs==rhs and rhs>=0
                harmonic_checks+=1
    # Query-only sharpness: J=0/1 with probability 19/25,6/25.
    query_only_value=F(19,25)*K+F(6,25)*F(K,2)
    assert query_only_value==beta
    # This witness establishes only sharpness of the T cut, not full dual feasibility.
    return {
        'source':str(SOURCE.relative_to(ROOT)),
        'scope':'Existing complete SPE; new consequences for actual-support static-dual restrictions only',
        'players':m,'customers':len(customers),'automaton_nodes':len(nodes),
        'all_nodes_reachable':True,'true_action_comparisons':comparison_count,
        'minimum_SPE_slack':str(F(min_slack,scale)),
        'actual_path':[ins['topics'][a] for a in path],
        'actual_counts':q,'W':W,'OPT':OPT,'half_slack':2*W-OPT,
        'missing_query':ins['topics'][query],'missing_query_size':K,
        'actual_support':[ins['topics'][a] for a in sorted(actual_support)],
        'all_actual_support_backgrounds_query_value':str(K),
        'weak_half_security_cap_threshold':str(beta),
        'actual_support_cap_gap':str(K-beta),
        'deletion_columns':deletion,'exact_deletion_minimax_cap':str(exact_deletion_cap),
        'minimum_expected_missing_hitting_slots':str(J_lower),
        'minimum_expected_nonactual_slots':str(J_lower),
        'harmonic_integer_identity_checks':harmonic_checks,
        'query_only_sharpness_mixture':{'zero_T_slots':'19/25','one_T_slot':'6/25','value':str(query_only_value)},
        'limitations':'No claim that the sharp query-only mixture is a full security dual; no new SPE instance; no half counterexample.'
    }

if __name__=='__main__':
    report=main()
    path=HERE/'offpath_dual_budget_audit.json'
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False,indent=2))
