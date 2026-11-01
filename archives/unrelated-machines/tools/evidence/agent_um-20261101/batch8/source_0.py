#!/usr/bin/env python3
"""One-stage exact bounded-arity normal form below threshold 2b.

All input finite times are nonnegative rationals <= b, with b>0. Every old
job is replaced by a private full binary selector tree. This file supplies
the actual transformed instance, actual forward schedule and actual decoder.
It supplies no approximation algorithm and no hardness theorem.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import sys

# Decimal representation limits must not exclude legal binary-sized rationals.
if hasattr(sys, 'set_int_max_str_digits'):
    sys.set_int_max_str_digits(0)


def rational(x):
    if isinstance(x, float):
        raise ValueError('provide exact rational strings, not floats')
    return Q(x)


def instance(m, options):
    """JSON-safe input: each job is a list of [machine, exact-time-string]."""
    return {'m':m, 'jobs':[[[i,str(rational(p))] for i,p in j] for j in options]}


def validate(P, b=None):
    if not isinstance(P['m'], int) or P['m'] < 1:
        raise ValueError('at least one machine is required')
    bound = None if b is None else rational(b)
    if bound is not None and bound <= 0:
        raise ValueError('b must be positive')
    for job in P['jobs']:
        if not job:
            raise ValueError('job without a finite endpoint')
        seen = set()
        for i,p in job:
            p = rational(p)
            if not isinstance(i,int) or not 0 <= i < P['m'] or i in seen:
                raise ValueError('invalid or repeated endpoint')
            if p < 0 or (bound is not None and p > bound):
                raise ValueError('processing time outside [0,b]')
            seen.add(i)
    return bound


def loads(P, sigma):
    if len(sigma) != len(P['jobs']):
        raise ValueError('assignment length')
    L = {}
    for job,i in zip(P['jobs'],sigma):
        choices = {a:rational(p) for a,p in job}
        if i not in choices:
            raise ValueError('unavailable endpoint in actual schedule')
        L[i] = L.get(i,Q(0)) + choices[i]
    return {i:v for i,v in L.items() if v}


def encoded_loads(P,sigma):
    return {str(i):str(v) for i,v in sorted(loads(P,sigma).items())}


def makespan(P, sigma):
    return max(loads(P,sigma).values(), default=Q(0))


def transform(P, b):
    b = validate(P,b)
    new = {'m':P['m'], 'jobs':[]}
    groups = []

    def add_job(opts):
        j = len(new['jobs'])
        new['jobs'].append([[i,str(p)] for i,p in opts])
        return j

    for old_j, old_options in enumerate(P['jobs']):
        options = sorted((i,rational(p)) for i,p in old_options)
        internal, leaves = [], []

        def tree(lo,hi):
            node = new['m']
            new['m'] += 1
            if hi-lo == 1:
                leaves.append((lo,node))
            else:
                middle = (lo+hi)//2
                left = tree(lo,middle)
                right = tree(middle,hi)
                internal.append((node,left,right))
            return node

        root = tree(0,len(options))
        root_pin = add_job([(root,b)])
        node_jobs = []
        for node,left,right in internal:
            j = add_job([(node,b),(left,b),(right,b)])
            node_jobs.append([j,node,left,right])
        ports = []
        for option,node in sorted(leaves):
            machine,p = options[option]
            j = add_job([(machine,p),(node,b)])
            ports.append([j,node,machine,str(p)])
        groups.append({'old_job':old_j,'root':root,'root_pin':root_pin,
                       'internal':node_jobs,'ports':ports})
        assert len(internal)==len(options)-1
        assert len(leaves)==len(options)
    record = {'b':str(b),'original_m':P['m'],'groups':groups}
    validate(new,b)
    for job in new['jobs']:
        assert len(job)<=3
        small = [(i,p) for i,p in job if rational(p)<b]
        assert len(small)<=1
        if small:
            assert len(job)==2 and any(rational(p)==b for i,p in job)
    return new,record


def forward(P,new,record,sigma):
    validate(P,record['b'])
    old_L = loads(P,sigma)
    b = rational(record['b'])
    out = [None]*len(new['jobs'])
    for group in record['groups']:
        out[group['root_pin']] = group['root']
        chosen_machine = sigma[group['old_job']]
        chosen_ports = [x for x in group['ports'] if x[2]==chosen_machine]
        if len(chosen_ports)!=1:
            raise ValueError('original assignment does not select one option')
        chosen_port,chosen_leaf,_,_ = chosen_ports[0]
        parent = {}
        for j,node,left,right in group['internal']:
            out[j] = node
            parent[left] = (node,j)
            parent[right] = (node,j)
        for j,node,machine,p in group['ports']:
            out[j] = node
        out[chosen_port] = chosen_machine
        node = chosen_leaf
        while node!=group['root']:
            previous,j = parent[node]
            out[j] = node
            node = previous
    L = loads(new,out)
    assert {i:v for i,v in L.items() if i<P['m']}==old_L
    assert all(v<=b for i,v in L.items() if i>=P['m'])
    assert max(L.values(),default=Q(0))<=max(b,max(old_L.values(),default=Q(0)))
    return out


def project(P,new,record,sigma_new):
    b = rational(record['b'])
    new_L = loads(new,sigma_new)
    if max(new_L.values(),default=Q(0))>=2*b:
        raise ValueError('projection contract requires actual C<2b')
    out = [None]*len(P['jobs'])
    chosen_new_ports = []
    for group in record['groups']:
        candidates = [(j,machine) for j,node,machine,p in group['ports']
                      if sigma_new[j]==machine]
        if not candidates:
            raise AssertionError('2d unit jobs cannot fit d-tree auxiliary slots')
        j,machine = candidates[0]
        chosen_new_ports.append(j)
        out[group['old_job']] = machine
    old_L = loads(P,out)
    assert all(v<=new_L.get(i,Q(0)) for i,v in old_L.items())
    return out,chosen_new_ports


def all_private(P,new,record):
    out = [None]*len(new['jobs'])
    for g in record['groups']:
        out[g['root_pin']]=g['root']
        for j,node,left,right in g['internal']: out[j]=node
        for j,node,machine,p in g['ports']: out[j]=node
    assert makespan(new,out)<=(2*rational(record['b']) if P['jobs'] else 0)
    return out


def schedules(P):
    return product(*[[i for i,p in j] for j in P['jobs']])


def enumerated_case(P,b):
    new,record=transform(P,b)
    n_old=n_new=n_projected=0
    original_opt=None
    transformed_opt=None
    for sigma in schedules(P):
        n_old+=1
        C=makespan(P,sigma)
        original_opt=C if original_opt is None else min(original_opt,C)
        sf=forward(P,new,record,sigma)
        assert makespan(new,sf)<=max(rational(b),C)
    for tau in schedules(new):
        n_new+=1
        C=makespan(new,tau)
        transformed_opt=C if transformed_opt is None else min(transformed_opt,C)
        if C<2*rational(b):
            sigma,chosen=project(P,new,record,tau)
            assert makespan(P,sigma)<=C
            n_projected+=1
    cap = min(2*rational(b),max(rational(b),original_opt)) if P['jobs'] else Q(0)
    assert transformed_opt==cap
    all_private(P,new,record)
    return {'b':str(b),'original_m':P['m'],'original_jobs':len(P['jobs']),
            'original_options':[len(j) for j in P['jobs']],
            'new_m':new['m'],'new_jobs':len(new['jobs']),
            'original_actual_schedules':n_old,'new_actual_schedules':n_new,
            'new_schedules_projected_below_2b':n_projected,
            'original_opt':str(original_opt),'transformed_opt':str(transformed_opt)}


def audit():
    cases=[
        (instance(1,[]),Q(1)),
        (instance(1<<80,[]),Q(1)),
        (instance(1<<80,[[(0,Q(1,5)),((1<<80)-1,Q(1,3))]]),Q(1)),
        (instance(1,[[(0,0)]]),Q(1)),
        (instance(2,[[(0,0),(1,Q(3,5))]]),Q(1)),
        (instance(3,[[(0,Q(1,7)),(1,Q(2,3)),(2,1)]]),Q(1)),
        (instance(1,[[(0,Q(3,4))],[(0,Q(3,4))]]),Q(1)),
        (instance(1,[[(0,1)],[(0,1)],[(0,1)]]),Q(1)),
        (instance(1,[[(0,Q(5,4))],[(0,Q(5,4))]]),Q(7,5))]
    summaries=[enumerated_case(P,b) for P,b in cases]
    # Explicit rich forward witness; all placements and load projections emitted.
    P=instance(3,[[(0,0),(1,Q(2,5)),(2,Q(3,4))],
                  [(0,Q(3,4)),(1,Q(1,3))]])
    b=Q(1)
    new,record=transform(P,b)
    sigma=[1,0]
    sf=forward(P,new,record,sigma)
    back,selected=project(P,new,record,sf)
    # 20001-bit k has >5000 decimal digits: parse and exact forward/project.
    k=(1<<20000)+3
    p=rational('1/'+str(k))
    huge=instance(2,[[(0,p),(1,1)]])
    hn,hr=transform(huge,1)
    hf=forward(huge,hn,hr,[0])
    assert project(huge,hn,hr,hf)[0]==[0]
    assert makespan(hn,hf)==1
    rejected=[]
    try: transform(instance(1,[[(0,2)]]),1)
    except ValueError: rejected.append('p>b')
    else: raise AssertionError('p>b accepted')
    try: transform(instance(1,[[(0,-1)]]),1)
    except ValueError: rejected.append('negative p')
    else: raise AssertionError('negative p accepted')
    try: transform(instance(1,[[(0,0)]]),0)
    except ValueError: rejected.append('nonpositive b')
    else: raise AssertionError('b0 accepted')
    try: project(P,new,record,all_private(P,new,record))
    except ValueError: rejected.append('actual C=2b')
    else: raise AssertionError('closed 2b boundary accepted')
    return {'status':'pass','scope':'finite exact audit, not general proof',
            'enumerated_cases':summaries,
            'total_original_schedules':sum(x['original_actual_schedules'] for x in summaries),
            'total_new_schedules':sum(x['new_actual_schedules'] for x in summaries),
            'total_actual_projections':sum(x['new_schedules_projected_below_2b'] for x in summaries),
            'full_forward_example':{'P':P,'b':str(b),'P_prime':new,'record':record,
                'original_sigma':sigma,'original_loads':encoded_loads(P,sigma),
                'forward_sigma':sf,'forward_loads':encoded_loads(new,sf),
                'projected_sigma':back,'projected_loads':encoded_loads(P,back),
                'selected_port_jobs':selected},
            'large_binary_parameter':{'k_bits':k.bit_length(),'k_decimal_digits':len(str(k)),
                                     'original_options':2,'new_jobs':len(hn['jobs']),
                                     'new_machines':hn['m'],'exact_roundtrip':True},
            'negative_controls':rejected,
            'load_encoding':'nonzero machine-index dictionary; all omitted machines have load0'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--audit',action='store_true',help='run finite exact key audit (default)')
    parser.parse_args()
    result=audit()
    result['code_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    print(json.dumps(result,indent=2,sort_keys=True))
