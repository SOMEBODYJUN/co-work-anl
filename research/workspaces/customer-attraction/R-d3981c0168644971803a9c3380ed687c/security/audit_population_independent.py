"""Independent exact all-SPE audit of population_deletion_boundary.md.
Reads no author's code or evidence. All continuation endpoints are retained.
The count-cache stores sets, not a common tie selector for equal histories.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json


def check(m,t,d,eps,s,ordered=False):
    assert m>=2 and t>=4 and t%2==0 and d>=1 and 0<eps<F(t,2)
    L=d+(m+1)*t//2+eps;K=m+1
    # Block labels 0..m-1; T=m. Explicit unit membership sets.
    units=[]
    for i in range(m):
        units += [frozenset([i]) for _ in range(L-t)]
        units += [frozenset([i,m]) for _ in range(t)]
    units += [frozenset([m]) for _ in range(d)]
    @lru_cache(None)
    def payoff(c):
        # Each occupied topic's actual per-player payoff, from separate units.
        val=[]
        for a in range(K):
            if not c[a]:val.append(F());continue
            val.append(sum((F(1,sum(c[b] for b in u)) for u in units if a in u),F()))
        return tuple(val)
    def plus(c,a):return c[:a]+(c[a]+1,)+c[a+1:]
    records={}
    @lru_cache(None)
    def BI(state):
        c=tuple(state.count(i) for i in range(K)) if ordered else state
        depth=sum(c)
        if depth==s:return frozenset([c])
        child=[]
        for a in range(K):
            nextstate=state+(a,) if ordered else plus(c,a)
            child.append(BI(nextstate))
        # Independent children at every ordered history can choose their own SPE.
        threshold=max(min(payoff(z)[a] for z in child[a]) for a in range(K))
        allowed=frozenset((a,z) for a in range(K) for z in child[a] if payoff(z)[a]>=threshold)
        assert allowed
        records[state]=(c,allowed)
        return frozenset(z for a,z in allowed)
    root=() if ordered else (0,)*K
    outcomes=BI(root)
    categories={'contains_T':0,'noT_distinct':0,'noT_repeated':0}
    for c,allowed in records.values():
        actual_actions={a for a,z in allowed}
        fresh={i for i in range(m) if c[i]==0}
        assert fresh # s<=m and nonterminal
        if c[m]:
            categories['contains_T']+=1
            assert actual_actions<=fresh,(m,s,c,actual_actions)
        elif max(c[:m])<=1:
            categories['noT_distinct']+=1
            if s==m:assert actual_actions<=fresh,(m,s,c,actual_actions)
            else:assert actual_actions=={m},(m,s,c,actual_actions)
        else:
            categories['noT_repeated']+=1
            if s<m:assert actual_actions=={m},(m,s,c,actual_actions)
    if s==m:
        assert outcomes==frozenset([(1,)*m+(0,)])
    else:
        # Stronger complete classification: root T, then distinct blocks.
        assert all(z[m]==1 and max(z[:m])<=1 for z in outcomes)
        assert len(outcomes)==__import__('math').comb(m,s-1)
    # All no-T last-prefix counts and exact strict deviations, independent of BI.
    gap_min=None;prefixes=0
    def countvec(n,k):
        if k==1:yield(n,);return
        for i in range(n+1):
            for rest in countvec(n-i,k-1):yield(i,)+rest
    if s<m:
        for old in countvec(s-1,m):
            q=old+(1,);uT=payoff(q)[m]
            blockmax=max(payoff(plus(old+(0,),a))[a] for a in range(m))
            gap=uT-blockmax
            assert gap>=F((m-s)*t,2)-eps>0
            prefixes+=1;gap_min=gap if gap_min is None else min(gap_min,gap)
    # Direct terminal coverage maximization across all m-slot profiles.
    opt=None
    if s==m:
        for c in countvec(m,K):
            w=sum(any(c[a] for a in u) for u in units)
            opt=w if opt is None else max(opt,w)
        assert opt==m*L
    return {'m':m,'t':t,'d':d,'eps':eps,'population':s,'L':L,'unit_clients':len(units),'representation':'ordered histories' if ordered else 'count-cache of outcome sets','decision_states':len(records),'terminal_outcomes':len(outcomes),'state_categories':categories,'all_original_population_outcomes_all_blocks_once':s==m,'all_smaller_population_outcomes_T_once_distinct_blocks':s<m,'smaller_noT_last_prefixes':prefixes,'minimum_true_last_deviation_gap':None if gap_min is None else str(gap_min),'OPT_original_population':opt,'root_outcomes':sorted(outcomes) if len(outcomes)<=20 else None}


def audit():
    result={'scope':'independent exact finite all-SPE recurrence; general-m proof reviewed separately','count_set_cases':[],'ordered_history_cases':[],'parameter_variants':[]}
    dest=Path(__file__).with_name('population_independent_audit.json')
    for m in range(2,7):
        for s in range(1,m+1):
            result['count_set_cases'].append(check(m,4,1,1,s))
        dest.write_text(json.dumps(result,indent=2)+'\n')
    for m in range(2,6):
        result['ordered_history_cases'].append(check(m,4,1,1,m,True))
        # Check an underpopulation's complete ordered history tree as well.
        result['ordered_history_cases'].append(check(m,4,1,1,m-1,True))
    for m in range(2,6):
        for t,d,eps in [(6,2,1),(6,1,2),(10,3,4)]:
            for s in [m-1,m]:
                result['parameter_variants'].append(check(m,t,d,eps,s))
    dest.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'count_set_cases':len(result['count_set_cases']),'ordered_history_cases':len(result['ordered_history_cases']),'parameter_variants':len(result['parameter_variants']),'ordered_decision_histories':sum(x['decision_states'] for x in result['ordered_history_cases']),'fatal_found':False},indent=2))
if __name__=='__main__':audit()

# A second, separate payoff implementation checks why the epsilon window is strict.
def boundary_outcomes(m,s,t,d,eps):
    L=d+(m+1)*t//2+eps;K=m+1
    @lru_cache(None)
    def U(c):
        q=c[m]
        return tuple(F(L-t,c[a])+F(t,c[a]+q) if c[a] else F() for a in range(m)) + (sum((F(t,q+c[a]) for a in range(m)),F(d,q)) if q else F(),)
    def inc(c,a):return c[:a]+(c[a]+1,)+c[a+1:]
    @lru_cache(None)
    def allends(c):
        if sum(c)==s:return frozenset([c])
        children=[allends(inc(c,a)) for a in range(K)]
        cutoff=max(min(U(z)[a] for z in children[a]) for a in range(K))
        return frozenset(z for a in range(K) for z in children[a] if U(z)[a]>=cutoff)
    return allends((0,)*K)

if __name__=='__main__':
    boundary=[]
    for m in range(2,7):
        low=boundary_outcomes(m,m,4,1,0)
        high=boundary_outcomes(m,m-1,4,1,2)
        assert any(z[m] for z in low)
        assert any(not z[m] for z in high)
        boundary.append({'m':m,'epsilon_zero_m_population_has_T_SPE':True,'epsilon_t_over_two_smaller_population_has_noT_SPE':True})
    dest=Path(__file__).with_name('population_independent_audit.json')
    result=json.loads(dest.read_text());result['epsilon_boundary_cases']=boundary
    dest.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'strict_epsilon_window_boundary_cases':len(boundary),'boundary_claims_verified':True},indent=2))
