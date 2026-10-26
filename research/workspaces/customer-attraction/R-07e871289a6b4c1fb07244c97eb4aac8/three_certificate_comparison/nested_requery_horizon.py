"""Independent arbitrary-horizon audit of the same-source requery motif.

No main agent formula implementation is imported. The finite games below reuse
only this researcher's earlier independently written exact history-game class.
"""
from fractions import Fraction as R
from itertools import product
from functools import lru_cache
from pathlib import Path
import json
from nested_requery import ExactGame,unit_topics

HERE=Path(__file__).resolve().parent

def unit(n,d):
    return R(n,d) if n else R(0)

def literal_cost(p,ell,t,q,first,second):
    """Use the two literal follower arrays, not count variables."""
    b,c=first[-2:];j,v=second[-2:]
    first_load=p+t+sum(first)
    second_load=p+c+sum(second)
    return (2*unit(t,first_load)-unit(c,first_load)
            +R(3,2)*unit(c,second_load)-R(1,2)*unit(v,second_load)
            +R(b,2*(p+c+sum(second[:-1])+1))
            +R(j,4*(ell+1))+R(5*v,12*(ell+1))+R(v,12)
            +R(q,p+t+sum(first[:-1])+1))

def count_cost(p,ell,t,q,b,c,j,v,s,sp):
    z=p+t+s+b+c;zp=p+c+sp+j+v
    return (2*unit(t,z)-unit(c,z)+R(3,2)*unit(c,zp)-R(1,2)*unit(v,zp)
            +R(b,2*(p+c+sp+j+1))+R(j,4*(ell+1))
            +R(5*v,12*(ell+1))+R(v,12)+R(q,p+t+s+b+1))

@lru_cache(None)
def compressed_phi(k,p,ell,t,q):
    return -min(count_cost(p,ell,t,q,b,c,j,v,s,sp)
                for b,c,j,v in product((0,1),repeat=4)
                for s,sp in product(range(k-2),repeat=2))

def literal_phi(k,p,ell,t,q):
    values=product((0,1),repeat=k-1)
    followers=list(values)
    return -min(literal_cost(p,ell,t,q,f,g) for f,g in product(followers,repeat=2))

def horizon_type_checks():
    checks=[]
    for k in range(3,8):
        count=0
        # Include large p/ell and zero states. These are implementation checks;
        # the all-k proof is exact quotienting by the two follower counts.
        for p,ell,t,q in product(range(3),range(4),(0,1),(0,1)):
            assert literal_phi(k,p,ell,t,q)==compressed_phi(k,p,ell,t,q)
            count+=1
        checks.append({'k':k,'visible_cases':count,
                       'literal_candidates_per_case':2**(2*(k-1)),
                       'compressed_candidates_per_case':16*(k-2)**2})
    return checks

def audit_game(game):
    m=game.m
    actual=game.finish(())
    last=game.payoffs(actual)[-1]
    K=max(map(len,game.topics))
    ell=[sum(x in game.topics[s] for s in actual[:-1]) for x in range(game.n)]
    records=[]
    for k in range(3,m+1):
        depth=m-k
        source_count=0;tests=0;smallest=None
        for h in product(range(len(game.topics)),repeat=depth):
            source_count+=1
            src=game.payoffs(game.finish(h))[depth]
            past=[sum(x in game.topics[s] for s in h) for x in range(game.n)]
            for T,Q in product(range(len(game.topics)),repeat=2):
                first=game.finish(h+(T,));ff=first[depth+1:];B,C=ff[-2:]
                second=game.finish(h+(C,));gg=second[depth+1:];J,V=gg[-2:]
                a=game.payoffs(first);a2=game.payoffs(second)
                slacks=[src-a[depth],src-a2[depth],
                        a2[-1]-game.topic_value(B,second[:-1]),
                        last-game.topic_value(J,actual[:-1]),
                        last-game.topic_value(V,actual[:-1]),
                        R(K-len(game.topics[V])),
                        a[-1]-game.topic_value(Q,first[:-1])]
                assert min(slacks)>=0
                total=sum(weight*slack for weight,slack in zip(
                    (R(2),R(3,2),R(1,2),R(1,4),R(5,12),R(1,12),R(1)),slacks))
                correction=R(0);phsum=R(0)
                for x in range(game.n):
                    t=int(x in game.topics[T]);q=int(x in game.topics[Q])
                    f=tuple(int(x in game.topics[s]) for s in ff)
                    g=tuple(int(x in game.topics[s]) for s in gg)
                    value=literal_cost(past[x],ell[x],t,q,f,g)
                    ph=compressed_phi(k,past[x],ell[x],t,q)
                    assert value+ph>=0
                    correction+=value+ph;phsum+=ph
                lhs=R(7,2)*src+R(2,3)*last+R(K,12)+phsum
                assert lhs==total+correction and lhs>=0
                smallest=lhs if smallest is None else min(smallest,lhs)
                tests+=1
        records.append({'k':k,'source_provider':depth+1,'source_histories':source_count,
                        'all_T_Q_inequalities_and_exact_identities':tests,'minimum_lhs':str(smallest)})
    return {'m':m,'topics':len(game.topics),'unit_customers':game.n,'tests_by_horizon':records}

def main():
    types=horizon_type_checks()
    cases=[([],1), ([(1,1),(2,1)],2),
           ([(1,2),(2,1),(3,2),(4,3),(5,1),(6,2),(7,1)],3),
           ([(1,1),(2,2),(3,1),(4,2),(5,1),(6,1),(7,2)],4)]
    games=[]
    for masks,topics_count in cases:
        topics,n=unit_topics(masks,topics_count)
        for salt in (0,7):games.append(audit_game(ExactGame(topics,n,salt=salt)))
    result={'scope':'all-k local seven-row motif and exact count quotient, not a global half certificate',
            'literal_compressed_checks':types,'six_player_games':games,
            'totals':{'games':len(games),
                      'source_histories_all_horizons':sum(r['source_histories'] for g in games for r in g['tests_by_horizon']),
                      'inequalities_and_exact_identities':sum(r['all_T_Q_inequalities_and_exact_identities'] for g in games for r in g['tests_by_horizon'])}}
    (HERE/'nested_requery_horizon.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='six_player_games'},indent=2))

if __name__=='__main__':
    main()
