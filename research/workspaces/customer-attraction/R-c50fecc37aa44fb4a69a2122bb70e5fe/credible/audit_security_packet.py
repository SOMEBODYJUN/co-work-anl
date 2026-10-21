"""Independent replay of security's full-history strategy automaton.

Never imports game solver, constructor, canonical verifier, numpy, or LP.
The packet's `desired` fields are ignored. Actual terminal outcomes are
computed backwards from actions and child arcs. Customer payoff uses the
expanded list of distinct unit customers and exact Fractions.
"""
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
import argparse
import gzip
import hashlib
import json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('packet',type=Path);ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    if args.output.exists():raise FileExistsError(args.output)
    raw=args.packet.read_bytes();packet=json.loads(gzip.decompress(raw))
    instance=packet['instance'];p=len(instance['topics']);m=instance['players']
    units=tuple(frozenset(c['topics']) for c in instance['customers'] for _ in range(c['multiplicity']))
    nodes=packet['nodes'];root=packet['root']
    assert nodes[root]['counts']==[0]*p
    bydepth=defaultdict(list)
    for idx,node in enumerate(nodes):
        q=tuple(node['counts'])
        assert len(q)==p and all(type(x) is int and x>=0 for x in q)
        assert 0<=sum(q)<=m
        bydepth[sum(q)].append(idx)
    @lru_cache(None)
    def payoff(q,a):
        return sum((F(1,sum(q[b] for b in interested)) for interested in units if a in interested),F(0))
    outcomes={};deviations=0;minimum=None
    for depth in range(m,-1,-1):
        for idx in bydepth[depth]:
            node=nodes[idx];q=tuple(node['counts'])
            if depth==m:
                assert node.get('terminal') is True
                assert 'children' not in node and 'action' not in node
                outcomes[idx]=q;continue
            assert not node.get('terminal')
            action=node['action'];children=node['children']
            assert type(action) is int and 0<=action<p and len(children)==p
            for a,child in enumerate(children):
                assert type(child) is int and 0<=child<len(nodes)
                expected=q[:a]+(q[a]+1,)+q[a+1:]
                assert tuple(nodes[child]['counts'])==expected
            actual=outcomes[children[action]];outcomes[idx]=actual
            u=payoff(actual,action)
            for a,child in enumerate(children):
                v=payoff(outcomes[child],a)
                assert u>=v,(idx,a,str(u),str(v))
                if a!=action:
                    deviations+=1;slack=u-v
                    minimum=slack if minimum is None else min(minimum,slack)
    # Inductively every ordered action history has exactly one automaton path.
    multiplicities={root:1};totals=[]
    for depth in range(m+1):
        total=sum(multiplicities.get(idx,0) for idx in bydepth[depth])
        assert total==p**depth
        totals.append(total)
        if depth<m:
            for idx in bydepth[depth]:
                for child in nodes[idx]['children']:
                    multiplicities[child]=multiplicities.get(child,0)+multiplicities.get(idx,0)
    assert len(multiplicities)==len(nodes),'packet contains unreachable padding nodes'
    idx=root;actualpath=[]
    for _ in range(m):
        action=nodes[idx]['action'];actualpath.append(action);idx=nodes[idx]['children'][action]
    assert actualpath==packet['expected_path']
    assert outcomes[root]==tuple(packet['expected_terminal_counts'])
    q=outcomes[root];w=sum(any(q[a] for a in interested) for interested in units)
    alpha=F(m-1,m)
    g=[sum((1/(1+alpha*sum(q[b] for b in interested)) for interested in units if a in interested),F(0)) for a in range(p)]
    credit=sum((1/(1+alpha*sum(q[b] for b in interested)) for interested in units if any(q[b] for b in interested)),F(0))
    gap=m*max(g)-w-credit
    assert (w,credit,gap)==(33,F(708669,123025),F(29481,123025))
    report={'source_packet':str(args.packet),'source_sha256':hashlib.sha256(raw).hexdigest(),'strategy_nodes':len(nodes),'decision_nodes':sum(len(bydepth[d]) for d in range(m)),'nontrivial_automaton_deviations_checked':deviations,'minimum_deviation_slack':str(minimum),'represented_ordered_histories_per_depth':totals,'represented_ordered_decision_histories':sum(totals[:-1]),'represented_ordered_nontrivial_deviations':(p-1)*sum(totals[:-1]),'actual_path':actualpath,'actual_counts':q,'welfare':w,'g':[str(x) for x in g],'G_C':str(credit),'refined_tax_bridge_gap':str(gap),'ignored_all_desired_fields':True,'all_reachable':True,'no_solver_or_constructor_imported':True}
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))

if __name__=='__main__':main()
