"""Independent definition-level check of a saved K+m*u_i bridge witness.

Imports no game solver, cone generator, or prior auditor. Reads integer incidence
blocks and a complete ordered-history action map, follows each genuine branch,
and evaluates final equal shares with fractions.Fraction.
"""
from pathlib import Path
from itertools import product, combinations
from fractions import Fraction as F
from functools import lru_cache
from math import gcd
import hashlib,json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
SOURCE=ROOT/'research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/round4_independent/candidate_near_kplus_0_kplus_3.json'
OUTPUT=HERE/'independent_kplus_blind_audit.json'

def main():
    raw=SOURCE.read_bytes();obj=json.loads(raw)
    clones=obj['clones'];p=(len(clones)+1).bit_length()-1;m=len(obj['path'])
    assert len(clones)==(1<<p)-1
    assert all(type(n) is int and n>=0 for n in clones)
    blocks=tuple((mask,n) for mask,n in enumerate(clones,1) if n)
    actions={}
    for row in obj['actions']:
        h=tuple(row['history']);a=row['action']
        assert h not in actions,'duplicate prescribed history'
        assert type(a) is int and 0<=a<p
        assert all(type(b) is int and 0<=b<p for b in h)
        actions[h]=a
    required={h for depth in range(m) for h in product(range(p),repeat=depth)}
    assert set(actions)==required,'strategy fails complete ordered-history domain'

    @lru_cache(None)
    def finish(h):
        if len(h)==m:return h
        return finish(h+(actions[h],))

    @lru_cache(None)
    def utility(terminal,topic):
        total=F(0)
        for mask,n in blocks:
            if mask&(1<<topic):
                coverage_count=sum(bool(mask&(1<<b)) for b in terminal)
                assert coverage_count>0
                total+=F(n,coverage_count)
        return total

    def welfare(terminal):
        support=sum(1<<a for a in set(terminal))
        return sum(n for mask,n in blocks if mask&support)

    depth_stats=[];worst=[]
    for depth in range(m):
        ties=strict=0;smallest=None
        for h in product(range(p),repeat=depth):
            actual_terminal=finish(h);chosen=actions[h]
            actual=utility(actual_terminal,chosen)
            assert actual_terminal[:depth]==h
            assert actual_terminal[depth]==chosen
            for a in range(p):
                branch_terminal=finish(h+(a,))
                deviation=utility(branch_terminal,a)
                slack=actual-deviation
                if slack<0:worst.append({'history':h,'chosen':chosen,'deviation':a,'slack':str(slack)})
                smallest=slack if smallest is None else min(smallest,slack)
                if slack==0:ties+=1
                else:strict+=1
        depth_stats.append({'depth':depth,'histories':p**depth,'comparisons':p**(depth+1),
                            'min_slack':str(smallest),'ties':ties,'strict_positive':strict})
    assert not worst,repr(worst[:3])
    root=finish(());assert root==tuple(obj['path'])
    u=tuple(utility(root,a) for a in root);W=welfare(root)
    assert sum(u)==W
    sizes=tuple(sum(n for mask,n in blocks if mask&(1<<a)) for a in range(p))
    K=max(sizes)
    pair_witnesses=[]
    for a,b in combinations(range(p),2):
        mask=next((mask for mask,n in blocks if bool(mask&(1<<a))!=bool(mask&(1<<b))),None)
        assert mask is not None,'duplicate physical topic sets'
        pair_witnesses.append({'topics':[a,b],'distinguishing_positive_block':mask})
    # Exhaustively cover all ordered m-tuples, including every repetition.
    best=-1;optimal_sequences=[]
    for terminal in product(range(p),repeat=m):
        value=welfare(terminal)
        if value>best:best=value;optimal_sequences=[terminal]
        elif value==best:optimal_sequences.append(terminal)
    attacked=obj['a'];assert attacked in root
    attacked_utility=utility(root,attacked)
    gap=F(best-K)-m*attacked_utility
    assert gap>0,'the proposed K bridge is not separated'
    payload={
        'claim_checked':'OPT_m <= K + m*u_i with K=max_T |T|; witness refutes this auxiliary bridge',
        'scope':'complete ordered-history pure SPE in original finite unit-customer common-catalogue model',
        'source':str(SOURCE),'source_sha256':hashlib.sha256(raw).hexdigest(),
        'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'players':m,'topics':p,'positive_incidence_blocks':len(blocks),
        'total_unit_customers':sum(clones),'multiplicities_nonnegative_integers':True,
        'multiplicity_gcd':gcd(*clones),'topic_sizes':sizes,'K':K,
        'physical_topics_pairwise_distinct':True,'distinctness_witnesses':pair_witnesses,
        'ordered_histories_checked':len(required),'ordered_action_comparisons':sum(row['comparisons'] for row in depth_stats),
        'every_comparison_nonnegative':True,'history_depths':depth_stats,
        'root_path':root,'root_utilities':[str(t) for t in u],'W':W,
        'ordered_comparison_tuples_checked':p**m,'OPT_m':best,
        'optimal_supports':sorted({tuple(sorted(set(t))) for t in optimal_sequences}),
        'attacked_topic':attacked,'attacked_positions_1_based':[i+1 for i,a in enumerate(root) if a==attacked],
        'attacked_utility':str(attacked_utility),'OPT_minus_K_minus_m_u':str(gap),
        'OPT_minus_W_minus_m_u':str(F(best-W)-m*attacked_utility),
        'twice_W_minus_OPT':2*W-best,'OPT_over_W':str(F(best,W)),
        'payoffs_computed_from':'sum over positive integer incidence blocks n/(number of selected covering topics)',
        'does_not_refute':['OPT_m <= W + m*u_i','2W >= OPT_m']}
    OUTPUT.write_text(json.dumps(payload,indent=2)+'\n')
    print(json.dumps(payload,indent=2))

if __name__=='__main__':main()
