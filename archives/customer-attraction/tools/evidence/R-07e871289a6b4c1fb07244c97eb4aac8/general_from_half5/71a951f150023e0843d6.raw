#!/usr/bin/env python3
"""Parameterized valid necessary-row relaxation; no claim of SPE sufficiency."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json
import math
import sys


def make_system(m, priced=False):
    types = [(a, d) for a in product(range(2), repeat=m) for d in range(m+1)]
    rows = []
    def add(name, fn, k=F(0)):
        rows.append((name, [fn(a,d) for a,d in types]+[F(k)]))
    def u(a,i):
        return F(a[i],sum(a)) if a[i] else F(0)
    def den(a,i):
        return sum(a[:i])+m-i
    for i in range(m):
        add(f'cap:A{i+1}', lambda a,d,i=i: -F(a[i]), 1)
        for j in range(m):
            add(f'safe:{i+1}:A{j+1}',lambda a,d,i=i,j=j:u(a,i)-F(a[j],den(a,i)))
        add(f'safe:{i+1}:Tavg',lambda a,d,i=i:u(a,i)-F(d,m*den(a,i)))
    add('cap:Tavg',lambda a,d:-F(d,m),1)
    add('root:K',lambda a,d:u(a,0),-F(1,m))
    def b(a): return sum(a[:-2])
    def gden(a): return (b(a)+1)*(b(a)+2)
    def h(a): return u(a,m-2)+u(a,m-1)+F(a[-2],gden(a))
    for i in range(m):
        for j in range(i,m):
            add(f'pair:A{i+1}:A{j+1}',lambda a,d,i=i,j=j:h(a)-F(a[i]+a[j],b(a)+1)+F(a[i]*a[j],gden(a)))
        add(f'pair:A{i+1}:Tavg',lambda a,d,i=i:h(a)-F(a[i],b(a)+1)-F(d,m*(b(a)+1))+F(a[i]*d,m*gden(a)))
    add('pair:Tdiag',lambda a,d:h(a)-F(2*d,m*(b(a)+1))+F(d,m*gden(a)))
    add('pair:Toffdiag',lambda a,d:h(a)-F(2*d,m*(b(a)+1))+F(d*(d-1),m*(m-1)*gden(a)))
    add('pair:O',lambda a,d:F(m,2)*h(a)+F(b(a),b(a)+1)-int(d>0))
    add('last:O',lambda a,d:m*u(a,m-1)+F(sum(a[:-1]),sum(a[:-1])+1)-int(d>0))
    if priced:
        # The old two-follower coefficients extend by pricing each additional
        # hidden follower at 1/8. Unlike the old table, psi is rebuilt at the
        # correct number of remaining players and background range.
        for source in range(m-1):
            ntail=m-source-1
            alpha=(F(1,8),)*(ntail-1)+(F(1,5),)
            beta=(F(0),)*(ntail-1)+(F(1,20),)
            gamma=F(1,4)
            def psi(a,t,q,source=source,alpha=alpha,beta=beta,gamma=gamma):
                return priced_projection(sum(a[:source]),sum(a[:-1]),t,q,alpha,beta,gamma)[0]
            def base(a,source=source,alpha=alpha): return u(a,source)+sum(alpha)*u(a,m-1)
            for ti in range(m):
                for qi in range(m):
                    add(f'priced:{source+1}:A{ti+1}:A{qi+1}',lambda a,d,ti=ti,qi=qi,psi=psi,base=base:base(a)-psi(a,a[ti],a[qi]),sum(beta))
                add(f'priced:{source+1}:A{ti+1}:Tavg',lambda a,d,ti=ti,psi=psi,base=base:base(a)-sum(F(d if q else m-d,m)*psi(a,a[ti],q) for q in range(2)),sum(beta))
                add(f'priced:{source+1}:Tavg:A{ti+1}',lambda a,d,ti=ti,psi=psi,base=base:base(a)-sum(F(d if t else m-d,m)*psi(a,t,a[ti]) for t in range(2)),sum(beta))
            add(f'priced:{source+1}:Tdiag',lambda a,d,psi=psi,base=base:base(a)-F(d,m)*psi(a,1,1)-F(m-d,m)*psi(a,0,0),sum(beta))
            def off(a,d,psi=psi,base=base):
                weights={(1,1):d*(d-1),(1,0):d*(m-d),(0,1):d*(m-d),(0,0):(m-d)*(m-d-1)}
                return base(a)-sum(F(v,m*(m-1))*psi(a,t,q) for (t,q),v in weights.items())
            add(f'priced:{source+1}:Toffdiag',off,sum(beta))
    return types,rows


def exact_solve(eqs,n):
    eqs=[list(eq) for eq in eqs]
    k=0
    for col in range(n):
        pivot=next((r for r in range(k,len(eqs)) if eqs[r][col]),None)
        if pivot is None:continue
        eqs[k],eqs[pivot]=eqs[pivot],eqs[k]
        q=eqs[k][col];eqs[k]=[x/q for x in eqs[k]]
        for r in range(len(eqs)):
            if r!=k and eqs[r][col]:
                q=eqs[r][col];eqs[r]=[x-q*y for x,y in zip(eqs[r],eqs[k])]
        k+=1
    assert k==n
    assert all(any(eq[:-1]) or not eq[-1] for eq in eqs)
    answer=[F(0)]*n
    for eq in eqs[:k]:
        col=next(j for j,x in enumerate(eq[:-1]) if x)
        answer[col]=eq[-1]
    return answer


def solve(m,priced=False):
    import numpy as np
    from scipy.optimize import linprog
    types,rows=make_system(m,priced=priced)
    w=[int(any(a)) for a,d in types]+[0]
    o=[int(d>0) for a,d in types]+[0]
    mat=np.array([[float(v) for v in row] for name,row in rows])
    sol=linprog(w,A_ub=-mat,b_ub=np.zeros(len(rows)),A_eq=[o],b_eq=[1],bounds=(0,None),method='highs')
    assert sol.success,sol.message
    rational=[F(float(x)).limit_denominator(100000000) for x in sol.x]
    supports=[(j,x) for j,x in enumerate(rational) if x]
    # Reconstruct a small exact vertex from its active float rows. Rounding alone
    # is insufficient: solve the identified support with exact Gaussian elimination.
    active=[row for name,row in rows if abs(sum(float(c)*sol.x[j] for j,c in enumerate(row)))<1e-8]
    eqs=[[row[j] for j,x in supports]+[F(0)] for row in active]
    eqs += [[F(o[j]) for j,x in supports]+[F(1)]]
    exact_support=exact_solve(eqs,len(supports))
    rational=[F(0)]*len(sol.x)
    for (j,_),v in zip(supports,exact_support):rational[j]=v
    assert all(x>=0 for x in rational)
    assert sum(F(o[j])*v for j,v in enumerate(rational))==1
    slacks={name:sum(c*x for c,x in zip(row,rational)) for name,row in rows}
    assert min(slacks.values())>=0
    value=sum(F(w[j])*v for j,v in enumerate(rational))
    # Exact sparse dual: w-nu*O-sum(lambda_j*S_j) has nonnegative
    # coefficients on every customer type and on K. Thus the reported value
    # is the precise optimum of this explicitly stated relaxation.
    dual_support=[i for i,x in enumerate(sol.ineqlin.marginals) if x< -1e-8]
    deqs=[[rows[i][1][j] for i in dual_support]+[F(o[j]),F(w[j])] for j,v in enumerate(rational) if v]
    dual=exact_solve(deqs,len(dual_support)+1)
    assert all(v>=0 for v in dual[:-1])
    assert dual[-1]==value
    dual_residuals=[F(w[j])-dual[-1]*o[j]-sum(v*rows[i][1][j] for i,v in zip(dual_support,dual)) for j in range(len(rational))]
    assert min(dual_residuals)>=0
    witness=[{'actual_bits':''.join(map(str,types[j][0])),'d':types[j][1],'weight':str(x)} for j,x in enumerate(rational[:-1]) if x]
    result={'m':m,'priced':priced,'n_types':len(types),'n_rows':len(rows),'W':str(value),'O':'1','K':str(rational[-1]),'support':witness,'slacks':{name:str(x) for name,x in slacks.items()},'min_slack':str(min(slacks.values())),'dual':{rows[i][0]:str(v) for i,v in zip(dual_support,dual)},'dual_nu':str(dual[-1]),'dual_min_residual':str(min(dual_residuals))}
    result['static_realization']=static_realization(result)
    return result


def static_realization(result):
    """Catalog realization of a static witness, and explicit non-SPE diagnosis."""
    m=result['m']
    assert all(s['d']==1 for s in result['support'])
    # For each support a and optimum index j, create D*n_a/m customers.
    scale=math.lcm(*(m*F(s['weight']).denominator for s in result['support']))
    groups=[(tuple(map(int,s['actual_bits'])),j,F(s['weight'])/m) for s in result['support'] for j in range(m)]
    def mem(a,j,q):return a[q] if q<m else int(j==q-m)
    def utility(q,r):
        return sum(w*F(mem(a,j,q),sum(a[:-2])+mem(a,j,q)+mem(a,j,r)) for a,j,w in groups if mem(a,j,q))
    original=utility(m-2,m-1)
    # Penultimate player copies the original last topic. After this deviation,
    # every follower best reply gives a strictly profitable deviation.
    q=m-1
    vals=[utility(r,q) for r in range(2*m)]
    best=max(vals)
    replies=[r for r,v in enumerate(vals) if v==best]
    gain=min(utility(q,r) for r in replies)-original
    assert gain>0
    name=lambda j:f'A{j+1}' if j<m else f'T{j-m+1}'
    return {'integer_scale_D':str(scale),'N':str(scale),'K':str(scale//m),'W':str(F(result['W'])*scale),'group_counts_per_optimum_index':[{'actual_bits':s['actual_bits'],'count':str(scale*F(s['weight'])/m)} for s in result['support']],'non_SPE_obstruction':{'source_player':m-1,'deviation':name(q),'follower_best_replies':[name(r) for r in replies],'original_payoff_normalized':str(original),'minimum_gain_normalized':str(gain)}}


@lru_cache(None)
def priced_projection(p,ell,t,q,alpha,beta,gamma):
    """Exact valid tail projection, alpha,beta indexed by hidden followers."""
    vals=[]
    for tail in product(range(2),repeat=len(alpha)):
        z=p+t+sum(tail)
        share=F(t,z) if t else F(0)
        last=F(tail[-1],z) if tail[-1] else F(0)
        value=share+sum(b*x for b,x in zip(beta,tail))+sum(a*x for a,x in zip(alpha,tail))/F(ell+1)-gamma*(last-F(q,p+t+sum(tail[:-1])+1))
        vals.append((value,tail))
    return min(vals)


def singleton_checks():
    alpha=(F(1,8),F(1,5));beta=(F(0),F(1,20));gamma=F(1,4)
    old=priced_projection(2,5,1,1,alpha,beta,gamma)
    shifted=priced_projection(3,5,1,1,alpha,beta,gamma)
    extended=priced_projection(2,5,1,1,(F(0),)+alpha,(F(0),)+beta,gamma)
    lhs=F(1,6)+sum(alpha)*F(1,6)+sum(beta)
    maxroot_rhs=F(94866177440,2048362573)*F(1,6)-F(60732827017,8193450292)
    assert lhs-old[0]==-F(1,30)
    assert lhs>=shifted[0] and lhs>=extended[0]
    assert maxroot_rhs<1
    return {'m':6,'N':[1],'catalog':[[1]],'all_strategy_actions':[1],'each_payoff':'1/6','K':'1','source_player_3_lhs':str(lhs),'incorrect_two_follower_rhs':str(old[0]),'incorrect_gap':str(lhs-old[0]),'valid_shifted_player_4_rhs':str(shifted[0]),'valid_three_follower_player_3_rhs':str(extended[0]),'three_follower_argmin':list(extended[1]),'incorrect_five_person_maxroot_rhs':str(maxroot_rhs)}


if __name__=='__main__':
    target=Path(__file__).with_name('six_stress_results.json')
    if '--verify' in sys.argv:
        data=json.loads(target.read_text())
        assert data['singleton_catalog_complete_SPE']==singleton_checks()
        for result in data['relaxations']:
            types,rows=make_system(result['m'],result['priced'])
            lookup={(a,d):i for i,(a,d) in enumerate(types)}
            n=[F(0)]*(len(types)+1)
            for s in result['support']:n[lookup[(tuple(map(int,s['actual_bits'])),s['d'])]]=F(s['weight'])
            n[-1]=F(result['K'])
            w=[int(any(a)) for a,d in types]+[0]
            o=[int(d>0) for a,d in types]+[0]
            assert min(n)>=0
            assert sum(F(x)*y for x,y in zip(o,n))==1
            assert sum(F(x)*y for x,y in zip(w,n))==F(result['W'])
            for name,row in rows:
                slack=sum(x*y for x,y in zip(row,n))
                assert slack==F(result['slacks'][name]) and slack>=0
            nu=F(result['dual_nu']);dual={name:F(x) for name,x in result['dual'].items()}
            assert all(x>=0 for x in dual.values())
            assert nu==F(result['W'])
            for j in range(len(n)):
                assert F(w[j])-nu*o[j]-sum(dual.get(name,0)*row[j] for name,row in rows)>=0
            assert static_realization(result)==result['static_realization']
            print('EXACT VERIFIED',result['m'],result['priced'],result['W'],len(types),'types',len(rows),'rows')
        sys.exit(0)
    results=[solve(m,priced=priced) for priced in (False,True) for m in (5,6)]
    # Direct counterexample to keeping the five-person priced source at player 3.
    checks={'singleton_catalog_complete_SPE':singleton_checks()}
    target.write_text(json.dumps({'relaxations':results,**checks},indent=2)+'\n')
    for r in results: print({k:r[k] for k in ('m','n_types','n_rows','W','K','min_slack')})
    print(checks)
