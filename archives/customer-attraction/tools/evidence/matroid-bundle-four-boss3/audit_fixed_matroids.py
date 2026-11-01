#!/usr/bin/env python3
"""Audit only the three saved best bundle functions, not their random batches.

Reuse the source exact integer outcome recursion once per point. Independently
check occupied payoffs by the player-coalition Shapley formula, reconstruct a
full strategy for the saved target and verify every ordered-history deviation.
Three static LPs supply candidate duals, which are checked over Fraction.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, combinations
from math import comb, factorial
import hashlib
import json
import platform
import runpy
import time

P=Path(__file__).resolve().parent
ns=runpy.run_path(str(P/'original/matroid_bundle_probe.py'))
import numpy as np
import scipy
from scipy.optimize import linprog


def compositions(total,k):
    if k==1:
        yield (total,)
    else:
        for first in range(total+1):
            for tail in compositions(total-first,k-1):
                yield (first,)+tail


def audit(name):
    raw=(P/'original'/name).read_bytes();doc=json.loads(raw)
    args=doc['args'];best=doc['best'];k=args['topics'];m=args['players']
    bundles=best['bundles'];assert len(bundles)==k
    assert all(b==sorted(set(b)) and 1<=len(b)<=4 and all(0<v<1<<args['dimension'] for v in b) for b in bundles)
    C=ns['coverage'](bundles);weights=ns['signed_weights'](C,k)
    for mask in range(1<<k):
        assert C[mask]==sum(v for B,v in weights.items() if B&mask)
    genuine=all(v>=0 for v in weights.values())
    solver=ns['Solver'](C,k,m)
    root=solver.solve((0,)*k)
    target=min(root,key=lambda q:(C[sum(1<<a for a,v in enumerate(q) if v)],q))
    assert list(target)==best['target']
    W=C[sum(1<<a for a,v in enumerate(target) if v)]
    assert W==best['welfare']

    @lru_cache(None)
    def direct(q,a):
        assert q[a]>0
        others=[b for b,n in enumerate(q) for _ in range(n-int(b==a))]
        assert len(others)==m-1
        answer=F(0)
        for selector in range(1<<(m-1)):
            mask=0;size=selector.bit_count()
            for index,b in enumerate(others):
                if selector>>index&1:mask|=1<<b
            answer+=F(factorial(size)*factorial(m-size-1),factorial(m))*(C[mask|(1<<a)]-C[mask])
        return answer

    payoff_checks=0
    for q in compositions(m,k):
        total=F(0)
        for a,n in enumerate(q):
            if not n:continue
            value=direct(q,a);assert value>=0
            assert value==F(solver.pay(q)[a],solver.scale)
            total+=n*value;payoff_checks+=1
        assert total==C[sum(1<<a for a,n in enumerate(q) if n)]
    actions=solver.certificate(target)
    sigma={tuple(x['history']):x['action'] for x in actions}
    expected={h for t in range(m) for h in product(range(k),repeat=t)}
    assert len(actions)==len(sigma) and set(sigma)==expected
    @lru_cache(None)
    def terminal(h):
        if len(h)==m:return tuple(h.count(a) for a in range(k))
        return terminal(h+(sigma[h],))
    assert terminal(())==target
    comparisons=0;strict=0;minimum=None
    for h,a in sigma.items():
        own=direct(terminal(h),a)
        for b in range(k):
            slack=own-direct(terminal(h+(b,)),b)
            assert slack>=0,(name,h,a,b,slack)
            comparisons+=1;strict+=int(slack>0)
            minimum=slack if minimum is None else min(minimum,slack)

    backgrounds=list(compositions(m-1,k));AA=[]
    for b in backgrounds:
        row=[]
        for a in range(k):
            q=list(b);q[a]+=1;row.append(direct(tuple(q),a))
        AA.append(row)
    # Recover the stored floating query, not a replacement proposed by this LP.
    pp=[F(float(p)).limit_denominator(10**6) for p in best['query_float']]
    pp=[p/sum(pp) for p in pp]
    assert all(p>=0 for p in pp)
    lower=min(sum((p*u for p,u in zip(pp,row)),F(0)) for row in AA)
    start=time.perf_counter()
    lp=linprog([0.]*k+[-1.],A_ub=[[-float(u) for u in row]+[1.] for row in AA],
               b_ub=[0.]*len(AA),A_eq=[[1.]*k+[0.]],b_eq=[1.],
               bounds=[(0,None)]*k+[(None,None)],method='highs')
    lp_seconds=time.perf_counter()-start
    assert lp.success
    dual=[F(float(-v)).limit_denominator(10**6) for v in lp.ineqlin.marginals]
    assert all(v>=0 for v in dual) and sum(dual)>0
    dual=[v/sum(dual) for v in dual]
    upper_by_action=[sum((v*row[a] for v,row in zip(dual,AA)),F(0)) for a in range(k)]
    upper=max(upper_by_action)
    assert lower==upper,(name,lower,upper)
    assert abs(float(lower)-best['security_float'])<1e-8
    opt=max(C[sum(1<<a for a in J)] for J in combinations(range(k),min(m,k)))
    exact_gap=F(W)-m*lower
    assert all(key not in best for key in ('exact_gap','query','actions','coverage','signed_weights'))
    source_path=[];h=()
    while len(h)<m:
        a=sigma[h];source_path.append(a);h=h+(a,)
    result={'file':name,'source_sha256':hashlib.sha256(raw).hexdigest(),'k':k,'m':m,
            'dimension':args['dimension'],'historical_games_argument':args['games'],
            'historical_distinct_functions':doc['distinct_functions'],'historical_best_trial':best['trial'],
            'historical_elapsed_seconds':doc['elapsed_seconds'],
            'all_rank_values':C,'distinct_vectors':len({v for b in bundles for v in b}),
            'rank_all_vectors':C[-1],'coverage_realizable':genuine,
            'nonzero_signed_types':{str(B):v for B,v in weights.items()},
            'negative_type_count':sum(v<0 for v in weights.values()),
            'minimum_welfare':W,'saved_target_is_lex_worst':True,'root_outcomes':len(root),
            'DP_states':len(solver.th)+comb(m+k-1,k-1),'occupied_payoff_checks':payoff_checks,
            'new_certificate_histories':len(sigma),'full_action_comparisons':comparisons,
            'strict_comparisons':strict,'minimum_IC_slack':str(minimum),
            'new_certificate_actual_path':source_path,'point_OPT_m':opt,
            'exact_security':str(lower),'stored_query_rationalized':list(map(str,pp)),
            'exact_gap':str(exact_gap),'historical_gap_float':best['gap_float'],
            'static_backgrounds':len(backgrounds),'query_guarantees':[str(sum((p*u for p,u in zip(pp,row)),F(0))) for row in AA],
            'new_LP_proposal_seconds':lp_seconds,'new_LP_float_security':-float(lp.fun),
            'exact_dual_backgrounds':[{'counts':list(b),'probability':str(v)} for b,v in zip(backgrounds,dual) if v],
            'exact_dual_pure_query_values':list(map(str,upper_by_action)),
            'full_BI_and_exact_security_identity':'new fixed-input audit; not original batch replay'}
    stem=name.removesuffix('.json')
    (P/(stem+'-new-full-strategy.json')).write_text(json.dumps({'identity':'current reconstruction for saved target; absent from frozen report','actions':actions},indent=2)+'\n')
    return result


def main():
    start=time.perf_counter()
    results=[audit(name) for name in ('matroid_k6_m3_d7.json','matroid_k7_m4_d9.json','matroid_k7_m5_d10.json')]
    report={'kind':'one fixed-input audit; 3 original exact outcome solves, 3 new static LP proposals, all recovered bounds exact',
            'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
            'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'source_program_sha256':hashlib.sha256((P/'original/matroid_bundle_probe.py').read_bytes()).hexdigest(),
            'original_random_CLI_runs':0,'random_games_generated':0,'new_static_LP_calls':3,
            'internal_audit_seconds_before_serialization':time.perf_counter()-start,'results':results}
    (P/'fixed-best-exact-audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='results'}),flush=True)
    for r in results:
        print(json.dumps({k:r[k] for k in ('file','coverage_realizable','negative_type_count','minimum_welfare','point_OPT_m','exact_security','exact_gap','root_outcomes','DP_states','new_certificate_histories','full_action_comparisons')}),flush=True)


if __name__=='__main__':main()
