"""Fraction checks of saved finite policies and canonical set-valued BI agreement."""
import json,math,random,runpy
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import numpy as np
from customer_attraction.model import Instance,CustomerType
from customer_attraction.exact import ExactSPESolver

BASE=Path(__file__).resolve().parent

def audit_policy(rec):
    k=len(rec['root']);m=sum(rec['root']);bg=tuple(rec['background']);acts={tuple(a['counts']):a['action'] for a in rec['actions']}
    weights={int(b):F(str(v)).limit_denominator(1000000) for b,v in rec['weights'].items()}
    assert len(acts)==math.comb(k+m-sum(bg)-1,k)
    @lru_cache(None)
    def terminal(q):
        if sum(q)==m:return q
        a=acts[q];return terminal(q[:a]+(q[a]+1,)+q[a+1:])
    def pay(q,a):
        return sum((v/F(sum(q[b] for b in range(k) if mask>>b&1)) for mask,v in weights.items() if mask>>a&1),F())
    low=F();comp=0
    for q,a in acts.items():
        u=pay(terminal(q),a)
        for b in range(k):
            child=q[:b]+(q[b]+1,)+q[b+1:];low=min(low,u-pay(terminal(child),b));comp+=1
    root=terminal(bg);assert root==tuple(rec['root']);u=pay(root,rec['target_action'])
    z=[F(str(v)).limit_denominator(1000000) for v in rec['queries']]
    cov=sum((v*min(F(1),sum(z[a] for a in range(k) if mask>>a&1)) for mask,v in weights.items()),F())
    w=sum(v for mask,v in weights.items() if any(root[a] and mask>>a&1 for a in range(k)))
    return {'policy_states':len(acts),'comparisons':comp,'min_slack':str(low),'valid':low>=0,'saved_query_strong_gap':str(cov-w-(sum(z)-1)*u)}

def instance(k,m,weights):
    return Instance(tuple('T'+str(a) for a in range(k)),tuple(CustomerType(frozenset(a for a in range(k) if int(mask)>>a&1),int(v)) for mask,v in weights.items() if int(v)),m)

def main():
    report={'status':'finite exact audits only; universal bridges remain OPEN','policy_files':[],'canonical_checks':[]}
    for name in ['bg_s2r2k6.json','bg_s6r2k7.json','bg_s2r3k6.json']:
        rs=[audit_policy(r) for r in json.loads((BASE/name).read_text())['records']]
        assert all(r['valid'] for r in rs)
        report['policy_files'].append({'file':name,'records':len(rs),'states':sum(r['policy_states'] for r in rs),'comparisons':sum(r['comparisons'] for r in rs),'all_valid':True,'maximum_exact_saved_query_gap':str(max(F(r['saved_query_strong_gap']) for r in rs))})
    D=runpy.run_path(str(BASE/'fullset_search.py'));Oracle=D['Oracle']
    saved=json.loads((BASE/'fullset_m5k7.json').read_text())['record_improvements']
    cases=[(7,5,r['weights']) for r in saved]
    rng=random.Random(2026102128)
    cases.extend((5,4,{str(b):rng.choice([0,0,1,2,5]) for b in range(1,32)}) for _ in range(5))
    for k,m,weights in cases:
        O=Oracle(k,m);mass=np.array([int(weights.get(str(b),0)) for b in O.masks],dtype=np.int64);O.solve(mass)
        exact=ExactSPESolver(instance(k,m,weights));exact.outcomes();checked=0
        for q,outs in O.out.items():
            assert {O.term[j] for j in outs}==set(exact.outcomes(q));checked+=1
            if sum(q)<m:assert F(int(O.floor[q]),O.L)==exact.threshold(q)
        for j,t in enumerate(O.term):
            for a in range(k):
                if t[a]:assert F(int(O.U[j,a]),O.L)==exact.instance.topic_payoff(a,t)
        report['canonical_checks'].append({'k':k,'m':m,'count_states_checked':checked,'root_outcomes':len(O.out[(0,)*k]),'all_outcomes_and_thresholds_agree':True})
    (BASE/'audit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
