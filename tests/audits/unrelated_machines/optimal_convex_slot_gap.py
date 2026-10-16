#!/usr/bin/env python3
"""Exact audit: fixed ordered ST slots can lose nearly 2 at the true OPT.

All finite processing times are positive. No LP solver is used. Output goes
only to stdout. Exhaustive oracles are deliberately capped at three machines.
When installed beside rounding_and_gap.py the default baseline path is local.
"""
from fractions import Fraction as F
from itertools import product, permutations
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import math
import platform
import random


def family(m):
    if type(m) is not int or m < 1:
        raise ValueError('m must be a positive integer')
    n = m*m
    p = [[F(1)] + [F(1,m+1)]*(n-1) for _ in range(m)]
    base = [0] + [1+(j-1)//(m+1) for j in range(1,n)]
    schedules = [[(i+r)%m for i in base] for r in range(m)]
    x = [[F(1,m)]*n for _ in range(m)]
    return p, schedules, x


def direct_loads(p, s):
    out = [F(0) for _ in p]
    for j,i in enumerate(s):
        if not 0 <= i < len(p):
            raise AssertionError('illegal machine')
        out[i] += p[i][j]
    return out


def slot_graph_from_atoms(m, small_orders=None):
    """Independent of round_slots: m atoms of size 1/m fill each slot.

    Every job is one atom on every machine, so its slot is position//m.
    Caller-supplied orders are permutations of the equal-sized small jobs.
    """
    n = m*m
    if small_orders is None:
        small_orders = [list(range(1,n)) for _ in range(m)]
    assert len(small_orders) == m
    slots_for_job = [[None]*m for _ in range(n)]
    for i,small in enumerate(small_orders):
        assert sorted(small) == list(range(1,n))
        for pos,j in enumerate([0]+small):
            slots_for_job[j][i] = (i,pos//m)
    return slots_for_job


def enumerate_assignments_and_slot_membership(m, p, graph):
    """Enumerates all m^(m*m) concrete schedules; separate slot injection."""
    if not 1 <= m <= 3:
        raise ValueError('exhaustive oracle capped at m=3')
    raw_opt = None
    slot_values = set()
    schedules_checked = 0
    slot_schedules = 0
    for s in product(range(m), repeat=m*m):
        schedules_checked += 1
        # Integer units m+1 avoid using the formula under audit.
        units = [0]*m
        for j,i in enumerate(s):
            units[i] += m+1 if j == 0 else 1
        val = F(max(units),m+1)
        raw_opt = val if raw_opt is None else min(raw_opt,val)
        chosen = [graph[j][s[j]] for j in range(m*m)]
        if len(set(chosen)) != m*m:
            continue
        slot_schedules += 1
        assert set(chosen) == {(i,r) for i in range(m) for r in range(m)}
        assert all(s.count(i) == m for i in range(m))
        slot_values.add(val)
    return {'assignments_checked': schedules_checked,
            'slot_schedules_checked': slot_schedules,
            'raw_optimum': str(raw_opt),
            'slot_makespan_values': sorted(map(str,slot_values))}


def enumerate_canonical_matchings(m, graph, p):
    """Different oracle: enumerate slot matchings blockwise, never m^n schedules."""
    if not 1 <= m <= 3:
        raise ValueError('matching oracle capped at m=3')
    count = 0
    values = set()
    for block_permutations in product(tuple(permutations(range(m))), repeat=m):
        s = [None]*(m*m)
        used = set()
        for r,perm in enumerate(block_permutations):
            for a,i in enumerate(perm):
                j = r*m+a
                slot = graph[j][i]
                assert slot == (i,r) and slot not in used
                used.add(slot)
                s[j] = i
        assert len(used) == m*m
        values.add(max(direct_loads(p,s)))
        count += 1
    return {'matchings_checked': count,
            'independent_count_formula': math.factorial(m)**m,
            'makespan_values': sorted(map(str,values))}


def one_case(m, round_slots, rng, tie_samples):
    p,ss,x = family(m)
    n=m*m
    # Constructed schedules are checked before their mean is used.
    assert all(direct_loads(p,s)==[F(1)]*m for s in ss)
    for j in range(n):
        assert sorted(s[j] for s in ss)==list(range(m))
        assert all(sum(F(1,m) for s in ss if s[j]==i)==x[i][j] for i in range(m))
    assert all(sum(p[i][j]*x[i][j] for j in range(n))==1 for i in range(m))
    assert all(v>0 for row in p for v in row)
    graph=slot_graph_from_atoms(m)
    assert len({sl for row in graph for sl in row})==n
    result,actual=round_slots(p,x,F(1))
    assert actual==direct_loads(p,result)
    assert all(result.count(i)==m for i in range(m))
    expected=F(2*m,m+1)
    assert max(actual)==expected
    # A deliberate cross-slot repair: send each co-located small job to a different other machine.
    big_machine=result[0]
    moved=[j for j in range(1,n) if result[j]==big_machine]
    others=[i for i in range(m) if i!=big_machine]
    assert len(moved)==len(others)==m-1
    repaired=list(result)
    for j,i in zip(moved,others):repaired[j]=i
    assert direct_loads(p,repaired)==[F(1)]*m
    assert sum(a!=b for a,b in zip(result,repaired))==m-1
    assert len({graph[j][result[j]] for j in range(n)})==n
    # Reconstruct all m convex schedules and both sides of the ratio.
    assert expected/F(1)==F(2)-F(2,m+1)
    out={'machines':m,'jobs':n,'optimum':'1','mean_schedule_count':m,
         'fractional_loads':['1']*m,'ordered_slots':n,
         'rounded_loads':list(map(str,actual)),
         'rounded_makespan':str(max(actual)),
         'fixed_slot_optimum':str(expected),'cross_slot_repaired_makespan':'1','changed_jobs':m-1,
         'ratio_to_actual_optimum':str(expected)}
    if m<=3:
        e=enumerate_assignments_and_slot_membership(m,p,graph)
        f=enumerate_canonical_matchings(m,graph,p)
        assert e['raw_optimum']=='1'
        assert e['slot_makespan_values']==[str(expected)]
        assert f['makespan_values']==[str(expected)]
        assert e['slot_schedules_checked']==f['matchings_checked']==f['independent_count_formula']
        out['all_assignment_oracle']=e
        out['all_canonical_matching_oracle']=f
        tie_records=[]
        for _ in range(tie_samples if m>=2 else 0):
            orders=[]
            for i in range(m):
                a=list(range(1,n));rng.shuffle(a);orders.append(a)
            g=slot_graph_from_atoms(m,orders)
            e2=enumerate_assignments_and_slot_membership(m,p,g)
            assert e2['raw_optimum']=='1' and e2['slot_makespan_values']==[str(expected)]
            tie_records.append({'small_orders':orders,**e2})
        out['sampled_distinct_tie_profiles']=tie_records
    return out


def contract_controls(round_slots):
    controls=[
        ('empty_jobs',[[]],[[]],F(0)),
        ('zero_optimum',[[F(0),F(1)],[F(1),F(0)]],[[F(1),F(0)],[F(0),F(1)]],F(0)),
        ('single_available_machine',[[F(3,7),F(4,7)]],[[F(1),F(1)]],F(1)),
        ('large_binary_denominator',[[F(1,2**127+1)]],[[F(1)]],F(1,2**127+1)),
    ]
    out=[]
    for name,p,x,t in controls:
        s,ls=round_slots(p,x,t)
        assert direct_loads(p,s)==ls and max(ls)<=t
        out.append({'name':name,'makespan':str(max(ls)),'target':str(t)})
    rejected=[]
    for val in [0,-1,True,F(1,2),1.0]:
        try:family(val)
        except ValueError:rejected.append(repr(val))
        else:raise AssertionError('invalid family parameter accepted')
    return {'actual_round_slots_controls':out,'invalid_family_parameters_rejected':rejected}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--baseline',type=Path,default=Path(__file__).with_name('rounding_and_gap.py'))
    parser.add_argument('--max-machines',type=int,default=40)
    parser.add_argument('--tie-samples',type=int,default=6)
    a=parser.parse_args()
    if a.max_machines<3 or a.tie_samples<0:parser.error('need max-machines>=3, tie-samples>=0')
    spec=importlib.util.spec_from_file_location('classical_st_baseline',a.baseline)
    baseline=importlib.util.module_from_spec(spec);spec.loader.exec_module(baseline)
    rng=random.Random(20261016)
    result={'scope':'finite audit, not proof or approximation algorithm',
            'python':platform.python_version(),'arithmetic':'fractions.Fraction and exact integer units',
            'seed':20261016,'precision':'exact','numerical_error':'none',
            'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'baseline_sha256':hashlib.sha256(a.baseline.read_bytes()).hexdigest(),
            'parameters':{'machines_inclusive':[1,a.max_machines],
                          'all_assignment_and_matching_enumeration':[1,2,3],
                          'tie_samples_each_m_2_3':a.tie_samples},
            'not_checked':['No all-assignment or all-matching enumeration for m>=4.',
                           'No exhaustive tie-profile enumeration; general tie independence is proved separately.',
                           'No general scheduling approximation construction or global novelty certification.'],
            'controls':contract_controls(baseline.round_slots),
            'records':[one_case(m,baseline.round_slots,rng,a.tie_samples) for m in range(1,a.max_machines+1)]}
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__=='__main__':main()
