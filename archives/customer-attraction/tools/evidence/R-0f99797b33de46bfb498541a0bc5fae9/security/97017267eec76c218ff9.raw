"""Exact finite audits, not a substitute for the universal stationary proof."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations_with_replacement
import sys,random,json
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from customer_attraction import Instance,ExactSPESolver
HERE=Path(__file__).parent

def scalar(r,b,I,K):
    return F((r-1)*I-K,(r-1)*(b+I+K)) if I or K else F(0)

def run():
    scalar_checks=0
    for r in range(2,10):
        for b in range(9):
            for n in range(r):
                for K in range(n+1):
                    assert scalar(r,b,0,K)>=-F(n,(r-1)*(b+1));scalar_checks+=1
                for K in range(r-n):
                    assert scalar(r,b,1,K)>=F(n,(r-1)*(b+r-1));scalar_checks+=1
            for K in range(r):
                assert scalar(r,b,1,K)>=0
                assert scalar(r,b,0,K)>=-F(1,b+r-1);scalar_checks+=2
    outside=[(1,2),(0,3),(0,3),(1,2)]
    R=[[F(outside[i].count(j),2) for i in range(4)] for j in range(4)]
    pi=[F(1,4)]*4
    assert all(sum(R[j][i]*pi[i] for i in range(4))==pi[j] for j in range(4))
    ds=[scalar(3,0,int(i<2),1) for i in range(4)]
    assert sum(pi[i]*ds[i] for i in range(4))==-F(1,8)
    rng=random.Random(80915)
    cases=[]
    for case in range(10):
        k=3 if case<4 else 4
        # Distinct private anchor in each maximum, plus singleton, missing-one,
        # or all memberships. Interior subthemes are arbitrary subsets.
        maxima=[{j} for j in range(k)]
        for x in range(k,k+7):
            typ=rng.randrange(3)
            J=({rng.randrange(k)} if typ==0 else
               set(range(k))-{rng.randrange(k)} if typ==1 else set(range(k)))
            for j in J:maxima[j].add(x)
        topics=maxima+[{x for x in maxima[rng.randrange(k)] if rng.randrange(2)} for _ in range(2)]
        maximal=[A for A in set(map(frozenset,topics)) if not any(A<B for B in map(frozenset,topics))]
        assert len(maximal)==k
        for x in set().union(*maximal):
            assert sum(x in A for A in maximal) in {1,k-1,k}
        prefix=[rng.randrange(len(topics)) for _ in range(case%3)]
        r=3+case%2
        I=Instance.from_topic_sets(topics,len(prefix)+r)
        E=ExactSPESolver(I)
        counts=I.counts(prefix)
        floor=E.threshold(counts)
        def query(a,B):
            return sum(F(customer.multiplicity,1+sum(counts[j] for j in customer.topics)+sum(b in customer.topics for b in B))
                       for customer in I.customers if a in customer.topics)
        theta=min(max(query(a,B) for a in range(I.topic_count)) for B in combinations_with_replacement(range(I.topic_count),r-1))
        assert floor>=theta
        cases.append(dict(case=case,maximal_topics=k,catalog_topics=I.topic_count,customers=I.customer_count,prefix=prefix,remaining=r,
                          all_spe_first_floor=str(floor),theta=str(theta),count_states=E.stats.count_states))
    report=dict(scope='Exact scalar inequalities plus finite all-SPE first-floor examples; universal result rests on written proof.',
                scalar_checks=scalar_checks,partial_membership_obstruction=dict(pi=list(map(str,pi)),delta=list(map(str,ds)),weighted_delta='-1/8'),cases=cases)
    (HERE/'structured_theta_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':run()
