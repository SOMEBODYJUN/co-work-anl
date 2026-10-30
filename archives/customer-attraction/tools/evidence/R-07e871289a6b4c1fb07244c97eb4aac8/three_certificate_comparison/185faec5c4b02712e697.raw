"""Exact independent audit of the supplied seven-line nested requery lemma.

This reads no new certificate: only the formula and seven rows in the prompt.
All output is confined to compare_new/.  Python's Fraction handles all signs.
"""
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent

def share(n,d):
    return F(n,d) if n else F(0)

def local_F(p,ell,t,q,b,c,j,v):
    z1=p+t+b+c
    z2=p+c+j+v
    return (2*share(t,z1)-share(c,z1)
            +F(3,2)*share(c,z2)-F(1,2)*share(v,z2)
            +F(b,2*(p+c+j+1))+F(j,4*(ell+1))
            +F(5*v,12*(ell+1))+F(v,12)
            +F(q,p+t+b+1))

def phi_with_argmin(p,ell,t,q):
    pairs=[(local_F(p,ell,t,q,*bits),bits)
           for bits in product((0,1),repeat=4)]
    best=min(value for value,_ in pairs)
    return -best,[bits for value,bits in pairs if value==best]

def rows_customer_constant(p,ell,t,q,b,c,j,v):
    """Constant part of the weighted seven slacks, leaving r/u_m/K symbolic."""
    z1=p+t+b+c
    z2=p+c+j+v
    return (-2*share(t,z1)-F(3,2)*share(c,z2)
            +F(1,2)*(share(v,z2)-F(b,p+c+j+1))
            -F(j,4*(ell+1))-F(5*v,12*(ell+1))-F(v,12)
            +share(c,z1)-F(q,p+t+b+1))

def exact_type_checks():
    tests=0
    for p,ell in product(range(13),range(15)):
        for t,q,b,c,j,v in product((0,1),repeat=6):
            assert rows_customer_constant(p,ell,t,q,b,c,j,v)==-local_F(p,ell,t,q,b,c,j,v)
            ph,_=phi_with_argmin(p,ell,t,q)
            assert local_F(p,ell,t,q,b,c,j,v)+ph>=0
            tests+=1
    return tests

def table(m):
    out=[]
    for p in range(m-2):
        for ell in range(p,p+3):
            row={'p':p,'ell':ell}
            row['phi_tq_00_01_10_11']=[str(phi_with_argmin(p,ell,t,q)[0])
                                        for t,q in ((0,0),(0,1),(1,0),(1,1))]
            row['argmin_bcjv']={f'{t}{q}':[''.join(map(str,bits)) for bits in phi_with_argmin(p,ell,t,q)[1]]
                               for t,q in ((0,0),(0,1),(1,0),(1,1))}
            out.append(row)
    return out

def high_background_polynomial_certificate():
    """Prove the actual-source p>=4 table for every p, without sampling p.

    For ell=p+delta, multiply F-F(0000) by D=p(p+1)(p+2)(p+3),
    substitute p=4+s, and check all numerator coefficients are nonnegative.
    D>0 for s>=0. This is an exact polynomial proof, not a cutoff experiment.
    """
    def multiply(a,b):
        out=[F(0)]*(len(a)+len(b)-1)
        for i,x in enumerate(a):
            for j,y in enumerate(b):out[i+j]+=x*y
        return out
    def polynomial(shifts):
        a=[F(1)]
        for shift in shifts:a=multiply(a,[F(4+shift),F(1)])
        return a
    denominator=polynomial(range(4))
    records=[]
    for delta,t,q,b,c,j,v in product(range(3),*(range(2) for _ in range(6))):
        w=[F(0)]*4
        w[t+b+c]+=2*t-c
        w[c+j+v]+=F(3*c-v,2)
        w[c+j+1]+=F(b,2)
        w[delta+1]+=F(j,4)+F(5*v,12)
        w[t+b+1]+=q
        w[t]-=2*t
        w[t+1]-=q
        numerator=[F(v,12)*x for x in denominator]
        for a,wa in enumerate(w):
            quotient=polynomial(k for k in range(4) if k!=a)
            for degree,x in enumerate(quotient):numerator[degree]+=wa*x
        assert min(numerator)>=0
        records.append({'delta':delta,'tq':f'{t}{q}','bcjv':f'{b}{c}{j}{v}',
                        'numerator_s_coefficients_ascending':list(map(str,numerator))})
    assert len(records)==192
    return {'claim':'For actual-source ell=p+delta, delta in {0,1,2}, p>=4, min F equals F(0000)',
            'phi_closed_form':'-2*t/(p+t)-q/(p+t+1)',
            'proof':'D(F-F0000) at p=4+s has nonnegative coefficients, D=p(p+1)(p+2)(p+3)>0',
            'denominator_s_coefficients_ascending':list(map(str,denominator)),
            'coefficient_certificates':records}

def unit_topics(mask_counts,topic_count):
    customers=[]
    for mask,count in mask_counts:
        customers.extend([mask]*count)
    return tuple(frozenset(i for i,mask in enumerate(customers) if mask&(1<<s))
                 for s in range(topic_count)),len(customers)

class ExactGame:
    def __init__(self,topics,n,m=6,salt=0):
        self.topics=topics;self.n=n;self.m=m;self.salt=salt
        self.policy={}

    @lru_cache(None)
    def payoffs(self,leaf):
        loads=[sum(x in self.topics[s] for s in leaf) for x in range(self.n)]
        return tuple(sum((F(1,loads[x]) for x in self.topics[s]),F(0)) for s in leaf)

    @lru_cache(None)
    def finish(self,h=()):
        if len(h)==self.m:
            return h
        leaves=[self.finish(h+(s,)) for s in range(len(self.topics))]
        pay=[self.payoffs(leaf)[len(h)] for leaf in leaves]
        candidates=[s for s,value in enumerate(pay) if value==max(pay)]
        # Deterministic dependence on the entire ordered history, including ties.
        word=self.salt
        for s in h:
            word=word*17+s+1
        chosen=candidates[word%len(candidates)]
        self.policy[h]=chosen
        return leaves[chosen]

    def topic_value(self,topic,prefix):
        return sum((F(1,1+sum(x in self.topics[s] for s in prefix))
                    for x in self.topics[topic]),F(0))

    def audit(self):
        actual=self.finish(())
        u=self.payoffs(actual)[-1]
        K=max(map(len,self.topics))
        ell=[sum(x in self.topics[s] for s in actual[:-1]) for x in range(self.n)]
        count=0;node_count=0;realized=set();minimum=None;all_ic=0
        for depth in range(self.m):
            for h in product(range(len(self.topics)),repeat=depth):
                leaf=self.finish(h)
                value=self.payoffs(leaf)[depth]
                for T in range(len(self.topics)):
                    assert value>=self.payoffs(self.finish(h+(T,)))[depth]
                    all_ic+=1
        for h in product(range(len(self.topics)),repeat=self.m-3):
            node_count+=1
            r=self.payoffs(self.finish(h))[self.m-3]
            p=[sum(x in self.topics[s] for s in h) for x in range(self.n)]
            for T,Q in product(range(len(self.topics)),repeat=2):
                first=self.finish(h+(T,));B,C=first[-2:]
                second=self.finish(h+(C,));J,V=second[-2:]
                first_pay=self.payoffs(first)
                second_pay=self.payoffs(second)
                slacks=[r-first_pay[-3],r-second_pay[-3],
                        second_pay[-1]-self.topic_value(B,second[:-1]),
                        u-self.topic_value(J,actual[:-1]),
                        u-self.topic_value(V,actual[:-1]),
                        F(K-len(self.topics[V])),
                        first_pay[-1]-self.topic_value(Q,first[:-1])]
                assert min(slacks)>=0
                lambdas=[F(2),F(3,2),F(1,2),F(1,4),F(5,12),F(1,12),F(1)]
                slack_total=sum(a*b for a,b in zip(lambdas,slacks))
                phis=F(0);rem=F(0)
                for x in range(self.n):
                    bits=[int(x in self.topics[s]) for s in (T,Q,B,C,J,V)]
                    ph,_=phi_with_argmin(p[x],ell[x],bits[0],bits[1])
                    ff=local_F(p[x],ell[x],*bits)
                    assert ff+ph>=0
                    phis+=ph;rem+=ff+ph
                    realized.add((p[x],ell[x]))
                lhs=F(7,2)*r+F(2,3)*u+F(K,12)+phis
                assert lhs==slack_total+rem and lhs>=0
                minimum=lhs if minimum is None else min(minimum,lhs)
                count+=1
        return {'m':self.m,'topics':len(self.topics),'unit_customers':self.n,
                'all_history_ICs':all_ic,'source_nodes_remaining_three':node_count,
                'nested_inequalities_and_exact_identities':count,'minimum_lhs':str(minimum),
                'realized_p_ell':sorted(realized)}

def main():
    types=exact_type_checks()
    games=[]
    cases=[([],1), ([(1,1),(2,1)],2),
           ([(1,2),(2,1),(3,2),(4,3),(5,1),(6,2),(7,1)],3),
           ([(1,1),(2,2),(3,1),(4,2),(5,1),(6,1),(7,2)],4)]
    for mask_counts,topic_count in cases:
        topics,n=unit_topics(mask_counts,topic_count)
        for salt in (0,7):
            games.append(ExactGame(topics,n,salt=salt).audit())
    result={'scope':'Supplied local seven-row formula only; no 44/60-row certificate bytes read or replayed',
            'arithmetic':'fractions.Fraction',
            'local_type_identities_and_remainders_checked':types,
            'five_actual_source_table':table(5),'six_actual_source_table':table(6),
            'six_arbitrary_source_pair_domain':[[p,ell] for p in range(4) for ell in range(6)],
            'six_games':games,
            'high_background_polynomial_certificate':high_background_polynomial_certificate()}
    (HERE/'nested_requery.json').write_text(json.dumps(result,indent=2)+'\n')
    summary={k:v for k,v in result.items() if k not in ('six_games','six_actual_source_table','six_arbitrary_source_pair_domain','high_background_polynomial_certificate')}
    summary['six_game_totals']={'games':len(games),
        'source_nodes':sum(g['source_nodes_remaining_three'] for g in games),
        'inequalities_and_identities':sum(g['nested_inequalities_and_exact_identities'] for g in games),
        'all_history_ICs':sum(g['all_history_ICs'] for g in games)}
    print(json.dumps(summary,indent=2))

if __name__=='__main__':
    main()
