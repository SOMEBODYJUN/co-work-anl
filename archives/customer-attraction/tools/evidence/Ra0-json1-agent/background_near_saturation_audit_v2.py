"""Exact finite audit of BNS on every ordered node of genuine full SPEs.

This audits implementation and proof intermediates on specified finite examples;
it does not prove the universal lemma or Q-CAG-HALF. No strategy is restricted to
count Markov form. Customer multiplicities are distinct unit clones.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import random
import sys

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'customer_attraction/__init__.py').is_file())
sys.path.insert(0,str(ROOT))
from customer_attraction import CustomerType, ExactSPESolver, Instance, StrategyCertificate, verify_certificate


def audit(inst,cert,name):
    verification=verify_certificate(inst,cert)
    verification.assert_valid()
    p,m=inst.topic_count,inst.players
    types=inst.customers
    path={}
    for depth in range(m,-1,-1):
        for h in product(range(p),repeat=depth):
            path[h]=h if depth==m else path[h+(cert.actions[h],)]
    total=0; pairs=0; sat=0; minslack=None; mincase=None; arbitrary_pairs=0
    nonmarkov=0; count_actions={}
    for h,a in cert.actions.items():
        key=inst.counts(h)
        count_actions.setdefault(key,set()).add(a)
    nonmarkov=sum(len(v)>1 for v in count_actions.values())
    for h,a in cert.actions.items():
        k=m-len(h)
        if k<2:continue
        total+=1
        b=[sum(z in ty.topics for z in h) for ty in types]
        M=k+max(b,default=0)
        w=[F(1,z+k) for z in b]
        sizes=[sum((ty.multiplicity*w[j] for j,ty in enumerate(types) if C in ty.topics),F(0)) for C in range(p)]
        K=max(sizes)
        u=inst.player_payoffs(path[h])[len(h)]
        delta=u-K
        assert delta>=0,(name,h,'delta',delta)
        for C in range(p):
            s=sizes[C]
            MC=k+max((b[j] for j,ty in enumerate(types) if C in ty.topics),default=0)
            coef=(k-1)*(MC-1)+F(k*k,2)
            for D in range(p):
                lhs=sum((ty.multiplicity*(w[j] if C in ty.topics else F(1,b[j]+1))
                         for j,ty in enumerate(types) if D in ty.topics),F(0))
                assert lhs<=s+coef*(u-s),(name,h,C,D,'arbitrary')
                arbitrary_pairs+=1
        for C in range(p):
            if sizes[C]!=K:continue
            M=k+max((b[j] for j,ty in enumerate(types) if C in ty.topics),default=0)
            # This is the actual continuation of the supplied full strategy.
            terminal=path[h+(C,)]
            suffix=terminal[len(h):]
            L=suffix[-1]
            q=[sum(z in ty.topics for z in suffix) for ty in types]
            v=sum((F(ty.multiplicity,b[j]+q[j]) for j,ty in enumerate(types) if C in ty.topics),F(0))
            t=inst.player_payoffs(terminal)[-1]
            d=sum((ty.multiplicity*(k-q[j])*w[j] for j,ty in enumerate(types) if C in ty.topics),F(0))
            dL=sum((ty.multiplicity*w[j] for j,ty in enumerate(types) if C in ty.topics and L not in ty.topics),F(0))
            assert K<=v<=u
            assert d<=(M-1)*delta
            assert t-v<=(k-F(M,M-1))*dL
            assert dL<=d
            if k==2:assert d==dL
            if not delta:
                sat+=1
                for B in suffix[1:]:
                    assert all((C in ty.topics)==(B in ty.topics) for ty in types)
            for D in range(p):
                pairs+=1
                lhs=sum((ty.multiplicity*(w[j] if C in ty.topics else F(1,b[j]+1))
                         for j,ty in enumerate(types) if D in ty.topics),F(0))
                # Direct last deviation at its observed terminal prefix.
                deviated=terminal[:-1]+(D,)
                deviation=inst.player_payoffs(deviated)[-1]
                assert deviation>=lhs-F(k,2)*(d-dL)
                assert t>=deviation
                assert lhs<=v+F(k,2)*d+(F(k,2)-F(M,M-1))*dL
                rhs=K+(k-1)*(M-1)*delta
                slack=rhs-lhs
                assert slack>=0,(name,h,C,D,slack)
                if minslack is None or slack<minslack:
                    minslack=slack;mincase={'h':h,'C':C,'D':D,'k':k,'M':M,'u':str(u),'K':str(K)}
    return {'name':name,'players':m,'topics':p,'customers':inst.customer_count,
            'definition_verified_histories':verification.checked_histories,
            'definition_verified_deviations':verification.checked_deviations,
            'eligible_ordered_histories':total,'maximizer_query_pairs':pairs,
            'arbitrary_topic_query_pairs':arbitrary_pairs,
            'saturated_maximizer_branches':sat,
            'count_classes_with_distinct_actions':nonmarkov,
            'minimum_BNS_slack':str(minslack),'minimum_case':mincase}


def generate():
    rng=random.Random(20261021031)
    examples=[('zero',Instance(('a','b','c'),(),4)),
              ('common_duplicate',Instance(('a','b','c'),(CustomerType(frozenset(range(3)),5),),4)),
              ('big_private_m5p7',Instance(tuple(map(str,range(7))),tuple(CustomerType(frozenset({a}),5 if a==0 else 1) for a in range(7)),5))]
    for m,p in [(3,4),(4,5),(5,7),(6,4)]:
        customers=[]
        for mask in range(1,1<<p):
            if rng.random()<.18:
                customers.append(CustomerType(frozenset(a for a in range(p) if mask>>a&1),rng.randint(1,9)))
        examples.append((f'sparse_m{m}p{p}',Instance(tuple(map(str,range(p))),tuple(customers),m)))
    for name,inst in examples:
        solver=ExactSPESolver(inst)
        target=min(solver.worst_outcomes())
        cert=solver.certificate(target,
            action_selector=lambda h,c:rng.choice(c),
            continuation_selector=lambda h,c:rng.choice(c))
        yield name,inst,cert
    other=ROOT/'research/workspaces/customer-attraction/R-84ce8a8709e34ea6af94f99991d3c2e3/counterexample_search/nonpne_best.json'
    data=json.loads(other.read_text())
    yield 'existing_nonpne_m5p7',Instance.from_dict(data['instance']),StrategyCertificate.from_dict(data['strategy'])


def main():
    rows=[]
    for name,inst,cert in generate():
        row=audit(inst,cert,name);rows.append(row);print(json.dumps(row),flush=True)
    result={'scope':'specified finite full SPE certificates only; no universal bound inferred',
            'lemma_status':'v2 using topic-specific M_C; analytical recheck after independent reviewer suggestion',
            'arithmetic':'Fraction throughout all inequalities','cases':rows}
    (HERE/'background_near_saturation_audit_v2.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':main()
