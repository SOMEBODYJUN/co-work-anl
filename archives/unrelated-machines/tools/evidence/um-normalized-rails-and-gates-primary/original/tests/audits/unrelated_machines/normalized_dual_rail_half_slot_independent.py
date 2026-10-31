#!/usr/bin/env python3
"""Statement-first normalized dual-rail solver and exact sharp audit.

No import of root/shared dual-rail code.  Every job contributes one
half-piece to each original endpoint.  A rail's selector half-piece is
first; two consecutive half-pieces form a capacity-one slot.  Each job
has two slot neighbors and each slot at most two jobs, so Hall holds.
An iterative alternating-path matcher covers all real jobs.
"""
from collections import Counter, deque
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import random

VERSION='normalized-dual-rail-independent-half-slots-v1.0'
SEED=558437


def construct(n,clauses):
    # clause=(positive integer A, tuple of (variable, sign)), sign1=positive.
    if not isinstance(n,int) or n<0:
        raise ValueError('invalid variable count')
    K=[0]*(2*n)
    for A,literals in clauses:
        if not isinstance(A,int) or A<1 or len(literals)>2*A-1:
            raise ValueError('invalid clause threshold/arity')
        for v,sign in literals:
            if not isinstance(v,int) or not 0<=v<n or sign not in (0,1):
                raise ValueError('invalid occurrence')
            K[2*v+(0 if sign else 1)]+=1
    machine_count=max(1,2*n+len(clauses))
    jobs=[]
    rails=[[] for _ in range(2*n)]
    clause_jobs=[[] for _ in clauses]
    for v in range(n):
        job=len(jobs)
        jobs.append({'id':f'selector_{v}','options':((2*v,F(1)),(2*v+1,F(1))),
                     'kind':'selector'})
        rails[2*v].append(job)
        rails[2*v+1].append(job)
    for c,(A,literals) in enumerate(clauses):
        for occurrence,(v,sign) in enumerate(literals):
            rail=2*v+(0 if sign else 1)
            assert K[rail]>=1
            job=len(jobs)
            jobs.append({'id':f'port_{c}_{occurrence}',
                         'options':((rail,F(1,K[rail])),(2*n+c,F(1,A))),
                         'kind':'port'})
            rails[rail].append(job)
            clause_jobs[c].append(job)
    slot_machine=[]
    slot_jobs=[]
    neighbors=[[] for _ in jobs]
    for machine,sequence in list(enumerate(rails))+[(2*n+c,row) for c,row in enumerate(clause_jobs)]:
        for start in range(0,len(sequence),2):
            slot=len(slot_machine)
            slot_machine.append(machine)
            slot_jobs.append(sequence[start:start+2])
            for job in sequence[start:start+2]:
                neighbors[job].append(slot)
    assert all(len(row)==2 and row[0]!=row[1] for row in neighbors)
    assert all(len(row)<=2 for row in slot_jobs)
    owner=[None]*len(slot_machine)
    chosen=[None]*len(jobs)
    for root in range(len(jobs)):
        assert chosen[root] is None
        queue=deque([root]);seen_jobs={root};parent={};free=None
        while queue and free is None:
            job=queue.popleft()
            for slot in neighbors[job]:
                if slot in parent:
                    continue
                parent[slot]=job
                previous=owner[slot]
                if previous is None:
                    free=slot
                    break
                if previous not in seen_jobs:
                    seen_jobs.add(previous)
                    queue.append(previous)
        assert free is not None
        while True:
            job=parent[free]
            previous_slot=chosen[job]
            chosen[job]=free
            owner[free]=job
            if previous_slot is None:
                break
            free=previous_slot
    sigma=[slot_machine[slot] for slot in chosen]
    assert len(set(chosen))==len(jobs)
    loads=[F(0)]*machine_count
    for job,machine in zip(jobs,sigma):
        assert machine in dict(job['options'])
        loads[machine]+=dict(job['options'])[machine]
    independent=[sum((dict(job['options'])[i] for job,machine in zip(jobs,sigma) if machine==i),F(0))
                 for i in range(machine_count)]
    assert loads==independent
    for rail in range(2*n):
        selector=sigma[rail//2]==rail
        ports=sum(job['kind']=='port' and dest==rail for job,dest in zip(jobs,sigma))
        if selector:
            assert ports<=K[rail]//2 and loads[rail]<=F(3,2)
        else:
            assert ports<=(K[rail]+2)//2 and ports<=K[rail] and loads[rail]<=1
    for c,(A,literals) in enumerate(clauses):
        count=sum(dest==2*n+c for dest in sigma)
        assert count<=(len(literals)+1)//2<=A
        assert loads[2*n+c]<=1
    assert max(loads)<=F(3,2)
    if n==0:
        assert not jobs and max(loads)==0
    return {'jobs':jobs,'sigma':sigma,'machine_loads':loads,'K':K,
            'slot_machine':slot_machine,'slots':slot_jobs,'job_to_slot':chosen,
            'actual_makespan':max(loads),'machine_count':machine_count}


def serial(result):
    return {**result,'actual_makespan':str(result['actual_makespan']),
            'machine_loads':[str(x) for x in result['machine_loads']],
            'jobs':[{**job,'options':[[i,str(p)] for i,p in job['options']]} for job in result['jobs']]}


def sharp_audit():
    clauses=((2,((0,1),(0,1),(1,1))),
             (2,((0,0),(0,0),(1,1))),
             (2,((1,0),(2,1),(2,1))),
             (2,((1,0),(2,0),(2,0))))
    result=construct(3,clauses)
    assert result['K']==[2]*6 and result['machine_count']==10 and len(result['jobs'])==15
    assert result['actual_makespan']==F(3,2)
    histogram=Counter();best=None;best_choices=None
    for choices in product((0,1),repeat=15):
        loads=[F(0)]*10
        for job,choice in zip(result['jobs'],choices):
            machine,p=job['options'][choice]
            loads[machine]+=p
        value=max(loads)
        histogram[str(value)]+=1
        if best is None or value<best:
            best=value;best_choices=choices
    assert sum(histogram.values())==1<<15
    assert best==F(3,2)
    assert histogram=={'3/2':13824,'2':18944}
    source_violations=[]
    for bits in product((0,1),repeat=3):
        true_counts=[sum(bits[v]==sign for v,sign in literals) for _,literals in clauses]
        assert max(true_counts)>=3
        source_violations.append({'assignment':list(bits),'clause_true_counts':true_counts})
    return {'clauses':[{'A':A,'occurrences':[list(x) for x in ls]} for A,ls in clauses],
            'complete_constructed_instance_and_sigma':serial(result),
            'exhaustive_assignment_count':1<<15,'all_sigma_makespan_histogram':dict(histogram),
            'exact_OPT':'3/2','one_exhaustive_optimal_option_vector':list(best_choices),
            'all_source_assignments':source_violations}


def main():
    rng=random.Random(SEED)
    trials=[]
    huge=2**257+5
    for _ in range(250):
        n=rng.randrange(7);clauses=[]
        for _ in range(rng.randrange(10)):
            A=rng.choice((1,2,3,4,huge))
            arity=0 if n==0 else rng.randrange(min(2*A-1,12)+1)
            literals=tuple((rng.randrange(n),rng.randrange(2)) for _ in range(arity))
            clauses.append((A,literals))
        result=construct(n,tuple(clauses))
        trials.append({'variables':n,'clauses':len(clauses),'jobs':len(result['jobs']),
                       'K_zero':sum(k==0 for k in result['K']),
                       'K_one':sum(k==1 for k in result['K']),
                       'actual_makespan':str(result['actual_makespan'])})
    empty=construct(0,())
    assert empty['machine_count']==1 and empty['actual_makespan']==0
    unused=construct(2,())
    assert unused['K']==[0]*4 and unused['actual_makespan']==1
    mixed=construct(3,((1,((0,1),)),(huge,((1,0),(1,1),(2,1))), (2,())))
    assert 0 in mixed['K'] and 1 in mixed['K']
    bad=((1,((0,1),(0,0))),)
    try:
        construct(1,bad)
    except ValueError:
        pass
    else:
        raise AssertionError('invalid arity not rejected')
    out={'version':VERSION,'code_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
         'seed':SEED,'arithmetic':'fractions.Fraction','status':'passed',
         'proof_contract':'independent half-slot Hall construction; no source assignment input',
         'random_trials':trials,'empty_variables_and_clauses':serial(empty),
         'unused_variables':serial(unused),'mixed_K0_K1_giant_A':serial(mixed),
         'giant_A':str(huge),'giant_A_bit_length':huge.bit_length(),
         'sharp':sharp_audit(),'scope':'finite implementation/exhaustive-sharp audit, separate from general proof'}
    print(json.dumps(out,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
