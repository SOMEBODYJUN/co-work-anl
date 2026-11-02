#!/usr/bin/env python3
"""Stdlib-only fixed-record audit: 180 legal-prefix policies and 13 integer points."""
import argparse
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
import hashlib,json
from itertools import combinations,product
from math import lcm
from pathlib import Path


def counts(k,n):
    if k==1:return [(n,)]
    return [(a,)+q for a in range(n+1) for q in counts(k-1,n-a)]


def add(q,a):return q[:a]+(q[a]+1,)+q[a+1:]


def cover(q,weights):
    return sum(w for mask,w in weights.items() if any(q[a] and mask>>a&1 for a in range(len(q))))


def policy_record(rec,gamma):
    k=len(rec['root']);bg=tuple(rec['background']);m=sum(rec['root']);r=m-sum(bg)
    weights={int(t):F(str(v)).limit_denominator(1000000) for t,v in rec['weights'].items()}
    assert weights and all(1<=t<1<<k and v>0 for t,v in weights.items()) and sum(weights.values())==1
    acts={tuple(row['counts']):row['action'] for row in rec['actions']}
    expected={tuple(b+d for b,d in zip(bg,delta)) for j in range(r) for delta in counts(k,j)}
    assert len(acts)==len(rec['actions']) and set(acts)==expected
    assert all(type(a) is int and 0<=a<k for a in acts.values())
    @lru_cache(None)
    def end(q):return q if sum(q)==m else end(add(q,acts[q]))
    @lru_cache(None)
    def u(q,a):return sum((w/F(sum(q[b] for b in range(k) if mask>>b&1)) for mask,w in weights.items() if mask>>a&1),F())
    node_rows=[];strict=ties=0
    for q,a in acts.items():
        vals=[u(end(add(q,b)),b) for b in range(k)];assert vals[a]==max(vals)
        for b,v in enumerate(vals):
            if b!=a:
                if vals[a]>v:strict+=1
                else:ties+=1
        node_rows.append({'counts':q,'action':a,'all_true_query_payoffs':list(map(str,vals))})
    root=end(bg);assert root==tuple(rec['root']) and acts[bg]==rec['target_action']
    z=[F(str(v)).limit_denominator(1000000) for v in rec['queries']]
    cov=sum(w*min(F(1),sum(z[a] for a in range(k) if mask>>a&1)) for mask,w in weights.items())
    W=cover(root,weights);v=u(root,rec['target_action']);gap=cov-W-(sum(z)-gamma)*v
    assert gap==0 and abs(float(gap)-rec['value'])<1e-10
    return {'trial':rec['trial'],'iteration':rec['iteration'],'background':bg,'root':root,
            'target_action':rec['target_action'],'rational_reconstructed_weights':{str(t):str(w) for t,w in weights.items()},
            'queries':list(map(str,z)),'W':str(W),'current_utility':str(v),'saved_query_coverage':str(cov),
            'saved_query_strong_gap':str(gap),'count_policy_states':len(acts),'comparisons_including_self':len(acts)*k,
            'strict_nonself':strict,'tie_nonself':ties,'all_node_payoffs':node_rows,
            'scope':'complete suffix count policy at a fixed legal prefix; no old-player incentive assertions; recovered rational point, not the exact decimal-float vector'}


class IntegerGame:
    def __init__(self,k,m,weights):
        self.k=k;self.m=m;self.L=lcm(*range(1,m+1));self.weights=weights;self.states_evaluated=0
        assert all(type(v) is int and v>=0 for v in weights.values())
        self.OPT=max(cover(tuple(int(a in J) for a in range(k)),weights) for J in combinations(range(k),min(k,m)))
    @lru_cache(None)
    def u(self,q,a):
        assert q[a]>0
        return sum(w*(self.L//sum(q[b] for b in range(self.k) if t>>b&1)) for t,w in self.weights.items() if t>>a&1)
    @lru_cache(None)
    def outcomes(self,q):
        self.states_evaluated+=1
        if sum(q)==self.m:return frozenset([q])
        child=[self.outcomes(add(q,a)) for a in range(self.k)]
        floor=max(min(self.u(z,a) for z in child[a]) for a in range(self.k))
        return frozenset(z for a in range(self.k) for z in child[a] if self.u(z,a)>=floor)
    def floor(self,q):return max(min(self.u(z,a) for z in self.outcomes(add(q,a))) for a in range(self.k))
    def minpay(self,q):return min(self.u(q,a) for a in range(self.k) if q[a])
    def construct_suffix(self,bg,target,first):
        r=self.m-sum(bg);policy={}
        def visit(h,q,goal):
            if len(h)==r:assert q==goal;return
            child=[self.outcomes(add(q,a)) for a in range(self.k)];floor=self.floor(q)
            legal=[a for a in range(self.k) if goal in child[a] and self.u(goal,a)>=floor]
            a=first if not h else legal[0];assert a in legal;policy[h]=a
            for b in range(self.k):
                wanted=goal if b==a else min(child[b],key=lambda z:(self.u(z,b),z))
                visit(h+(b,),add(q,b),wanted)
        visit((),bg,target)
        @lru_cache(None)
        def end(h):return h if len(h)==r else end(h+(policy[h],))
        def q_of(h):return tuple(bg[a]+h.count(a) for a in range(self.k))
        assert q_of(end(()))==target
        rows=[]
        for d in range(r):
            for h in product(range(self.k),repeat=d):
                vals=[self.u(q_of(end(h+(a,))),a) for a in range(self.k)]
                assert vals[policy[h]]==max(vals)
                rows.append({'suffix_history':h,'action':policy[h],'query_utilities_scaled':vals})
        return {'scope':'new complete ordered suffix policy at this fixed background, not a recovered source policy',
                'remaining_players':r,'ordered_nodes':len(rows),'comparisons_including_self':len(rows)*self.k,
                'actual_suffix':end(()),'all_nodes':rows}


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output',required=True,type=Path);args=ap.parse_args()
    assert not args.output.exists();args.output.mkdir(parents=True)
    package=Path(__file__).resolve().parent;original=package/'original'
    manifest=json.loads((package/'manifest.json').read_text())
    for row in manifest['sources']:
        b=(package/row['package_path']).read_bytes();assert len(b)==row['size'] and hashlib.sha256(b).hexdigest()==row['sha256']
    policies=[];policy_summaries=[]
    for name in ['bg_s2r2k6.json','bg_s6r2k7.json','bg_s2r3k6.json']:
        source=json.loads((original/'early_price'/name).read_text());gamma=F(str(source['parameters']['gamma']))
        records=[policy_record(rec,gamma) for rec in source['records']]
        report={'file':name,'records':records};policies.append(report)
        (args.output/(name.removesuffix('.json')+'-exact-policies.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        policy_summaries.append({'file':name,'records':len(records),'states':sum(r['count_policy_states'] for r in records),
                                 'comparisons_including_self':sum(r['comparisons_including_self'] for r in records),
                                 'maximum_saved_query_gap':max(F(r['saved_query_strong_gap']) for r in records).__str__(),
                                 'mixed_records':[r['trial'] for r in records if len(r['rational_reconstructed_weights'])>1]})
    full=json.loads((original/'early_price/fullset_m5k7.json').read_text());full_reports=[]
    for source in full['record_improvements']:
        game=IntegerGame(7,5,{int(t):v for t,v in source['weights'].items()});roots=sorted(game.outcomes((0,)*7))
        def weak(q):return F(game.OPT-cover(q,game.weights))-F(5*game.minpay(q),game.L)
        def strong(q):return F(game.OPT-cover(q,game.weights))-F(4*game.minpay(q),game.L)
        assert len(roots)==source['root_outcomes']
        assert tuple(source['weak_terminal']) in roots and tuple(source['strong_terminal']) in roots
        assert weak(tuple(source['weak_terminal']))==max(map(weak,roots))
        assert strong(tuple(source['strong_terminal']))==max(map(strong,roots))
        assert abs(float(max(map(weak,roots)))-source['weak'])<1e-10
        assert abs(float(max(map(strong,roots)))-source['strong'])<1e-10
        q=tuple(source['price_terminal']);assert q in roots;v=F(game.minpay(q),game.L)
        assert abs(float(v)-source['price'])<1e-10
        z=[F(str(x)) for x in source['queries']]
        C=sum(w*min(F(1),sum(z[a] for a in range(7) if t>>a&1)) for t,w in game.weights.items())
        gap=C-cover(q,game.weights)-(sum(z)-1)*v
        assert abs(float(gap)-source['price_strong_gap'])<1e-10
        full_reports.append({'trial':source['trial'],'all_root_counts':roots,'OPT':game.OPT,
              'weak_gap_exact':str(max(map(weak,roots))),'strong_integer_menu_gap_exact':str(max(map(strong,roots))),
              'price_terminal':q,'W':cover(q,game.weights),'price_exact':str(v),'saved_queries':list(map(str,z)),
              'saved_query_strong_gap_exact':str(gap),'source_price_gap_float':source['price_strong_gap'],
              'source_float_minus_exact':str(F(str(source['price_strong_gap']))-gap),
              'price_optimality_certified':False,'DP_states':game.states_evaluated})
    (args.output/'fullset-four-fixed-points.json').write_text(json.dumps(full_reports,ensure_ascii=False,indent=2)+'\n')
    allbg=json.loads((original/'early_price/allbg_m5k7.json').read_text());bg_reports=[]
    for source in allbg['record_improvements']:
        game=IntegerGame(7,5,{int(t):v for t,v in source['weights'].items()})
        q=tuple(source['background']);target=tuple(source['terminal']);a=source['target_action']
        assert target in game.outcomes(add(q,a)) and game.u(target,a)>=game.floor(q)
        U=game.u(target,a);W=cover(target,game.weights);value=F(game.OPT-W)-F(5*U,game.L)
        assert U==source['utility_scaled'] and game.L==source['utility_scale']
        assert W==source['welfare'] and game.OPT==source['optimum'] and abs(float(value)-source['value'])<1e-10
        policy=game.construct_suffix(q,target,a)
        bg_reports.append({'trial':source['trial'],'background':q,'target_action':a,'terminal':target,
                           'utility_scaled':U,'scale':game.L,'W':W,'OPT':game.OPT,'value_exact':str(value),
                           'new_suffix_policy':policy,'DP_states':game.states_evaluated})
    (args.output/'allbg-nine-fixed-points-and-new-suffixes.json').write_text(json.dumps(bg_reports,ensure_ascii=False,indent=2)+'\n')
    assert sum(len(r['rational_reconstructed_weights'])==1 for group in policies for r in group['records'])==177
    assert sum(len(r['rational_reconstructed_weights'])>1 for group in policies for r in group['records'])==3
    summary={'identity':'Boss3','scope':'180 saved rational-recovered legal-prefix count policies plus 4 fullset and 9 all-background integer saved records only',
             'policy_summaries':policy_summaries,'policy_records':180,'one_interest_records':177,'mixed_interest_records':3,
             'fullset_records':full_reports,'all_background_records':[{k:v for k,v in r.items() if k!='new_suffix_policy'} for r in bg_reports],
             'new_suffix_policies':9,'new_suffix_ordered_nodes':sum(r['new_suffix_policy']['ordered_nodes'] for r in bg_reports),
             'new_suffix_comparisons_including_self':sum(r['new_suffix_policy']['comparisons_including_self'] for r in bg_reports),
             'original_CLI_calls':0,'project_solver_or_verifier_calls':0,'LP_calls':0,'random_calls':0,
             'original_nine_canonical_checks_replayed':0,'original_five_generated_random_checks_replayed':0,
             'p4_twelve_client_game_rechecks':0,'template_audit_rechecks':0,'new_fixed_audit_processes':1,'all_checks_passed':True}
    (args.output/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
