"""Independent unit-set arithmetic for the collision-free K-bridge obstruction.

The arbitrary-m SPE claim rests on the analytic Q/B induction in the companion
review, not on exhaustive tree expansion. This file checks exact set arithmetic
and the local induction formulas across bounded structured states.
"""
from itertools import combinations,product
from pathlib import Path
from fractions import Fraction as F
import json,hashlib

BASE=Path(__file__).resolve().parent

def instance(k):
    X=[frozenset((3*i,3*i+1)) for i in range(k)]
    a=[3*i+2 for i in range(k)];b=3*k;d=b+1
    topics={('A',i):X[i]|{a[i]} for i in range(k)}
    topics.update({('B',i):X[i]|{b} for i in range(k)})
    topics.update({('C',i):X[i] for i in range(k)})
    topics[('D',-1)]=frozenset((b,d))
    return topics

def payoff(topics,path,who):
    return sum((F(1,sum(x in topics[a] for a in path)) for x in topics[path[who]]),F(0))

def Q_suffix(k,history,designated):
    touched={i for a,i in history};fresh=[i for i in range(k) if i not in touched]
    return tuple(('C',i) for i in fresh)+(('D',-1) if designated is None else ('B',designated),)

def B_suffix(k,history,initial):
    touched={i for a,i in history};fresh=[i for i in range(k) if i not in touched]
    return tuple(('A',i) for i in fresh)+(('A',initial),)

def main():
    family=[];price_checks=0
    for k in range(1,101):
        topics=instance(k);m=k+1
        assert len(topics)==3*m-2 and len(set(topics.values()))==len(topics)
        allclients=frozenset().union(*topics.values())
        root=tuple(('C',i) for i in range(k))+(('D',-1),)
        optimum=tuple(('A',i) for i in range(k))+(('D',-1),)
        W=len(frozenset().union(*(topics[a] for a in root)))
        O=len(frozenset().union(*(topics[a] for a in optimum)))
        K=max(map(len,topics.values()));u=[payoff(topics,root,j) for j in range(m)]
        assert O==len(allclients)==3*m-1 and W==2*m and K==3
        assert u==[F(2)]*m
        assert O-K-m*u[0]==O-K-W==m-4
        assert 2*W-O==m+1
        family.append({'m':m,'topics':len(topics),'unit_clients':len(allclients),
                       'K':K,'W':W,'OPT':O,'each_u':2,'K_bridge_gap':m-4,
                       'aggregate_K_gap':m-4,'half_margin':m+1})
        for v in map(F,[0,F(1,2),1,F(3,2),2,F(5,2),3,F(7,2)]):
            if v<=1:s,t,u,w=F(1),1-v,F(1),1-v
            elif v<=2:s,t,u,w=(3-v)/2,F(0),2-v,F(0)
            elif v<=3:s,t,u,w=(3-v)/2,F(0),F(0),F(0)
            else:s=t=u=w=F(0)
            prices={x:s for i in range(k) for x in (3*i,3*i+1)}
            prices.update({3*i+2:t for i in range(k)})
            prices[3*k]=u;prices[3*k+1]=w
            assert all(0<=y<=1 for y in prices.values())
            assert all(sum(prices[x] for x in T)>=len(T)-v for T in topics.values())
            expected=3*m-1-m*v if v<=2 else (m-1)*(3-v) if v<=3 else F(0)
            primal_topics=optimum if v<=2 else tuple(('A',i) for i in range(k)) if v<=3 else ()
            covered=frozenset().union(*(topics[a] for a in primal_topics))
            primal=F(len(covered))-v*len(primal_topics)
            assert sum(prices.values())==primal==expected
            price_checks+=1

    local={'Q_states':0,'Q_fresh_A_branches':0,'Q_fresh_B_branches':0,'Q_base_best_reply_checks':0,
           'B_states':0,'B_base_best_reply_checks':0}
    for k in range(1,8):
        topics=instance(k)
        for codes in product(range(3),repeat=k): # 0 untouched, 1 old A, 2 old C
            h=tuple(('A' if code==1 else 'C',i) for i,code in enumerate(codes) if code)
            fresh=[i for i,c in enumerate(codes) if not c]
            oldA=[i for i,c in enumerate(codes) if c==1]
            for t in oldA or [None]:
                suffix=Q_suffix(k,h,t);path=h+suffix;local['Q_states']+=1
                assert all(payoff(topics,path,j)==2 for j in range(len(h),len(path)))
                if not fresh:
                    actual=payoff(topics,path,len(h))
                    assert all(payoff(topics,h+(a,),len(h))<=actual for a in topics)
                    local['Q_base_best_reply_checks']+=len(topics)
                else:
                    for i in fresh:
                        branch=h+(('A',i),);term=branch+Q_suffix(k,branch,i)
                        assert payoff(topics,term,len(h))==2
                        local['Q_fresh_A_branches']+=1
                        branch=h+(('B',i),);term=branch+B_suffix(k,branch,i)
                        assert payoff(topics,term,len(h))==2
                        local['Q_fresh_B_branches']+=1
            for initial in fresh:
                bh=h+(('B',initial),);suffix=B_suffix(k,bh,initial);path=bh+suffix
                local['B_states']+=1
                assert all(payoff(topics,path,j)==3 for j in range(len(bh),len(path)-1))
                assert payoff(topics,path,len(path)-1)==2
                if len(suffix)==1:
                    actual=payoff(topics,path,len(bh))
                    assert all(payoff(topics,bh+(a,),len(bh))<=actual for a in topics)
                    local['B_base_best_reply_checks']+=len(topics)
    result={'scope':'independent set arithmetic plus bounded structured-state checks; arbitrary m relies on companion analytic induction',
            'family_checked_m':[2,101],'structured_state_checked_k':[1,7],
            'local_checks':local,'first_violating_member_within_family':family[3],
            'price_primal_dual_checks':price_checks,
            'price_grid':['0','1/2','1','3/2','2','5/2','3','7/2'],
            'price_closed_form':['3m-1-mv for 0<=v<=2','(m-1)(3-v) for 2<=v<=3','0 for v>=3'],
            'general_formulas':{'m':'integer m>=2','N':'3m-1','catalogue_size':'3m-2',
                                'K':'3','W':'2m','OPT_m':'3m-1','u_i':'2 for every actual player',
                                'OPT_minus_K_minus_m_u_i':'m-4','OPT_minus_K_minus_W':'m-4',
                                'two_W_minus_OPT':'m+1'},
            'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'family_arithmetic':family}
    (BASE/'independent_collision_family_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='family_arithmetic'},indent=2))

if __name__=='__main__':main()
