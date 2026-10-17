#!/usr/bin/env python3
"""宏任务退出及有界畸变接收池的原任务枚举核验。"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import random
import sys

ROOT = Path(__file__).resolve().parents[3]
source = Path(__file__).with_name('private_group_exit_pool.py')
spec = importlib.util.spec_from_file_location('exit_pool', source)
algorithm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(algorithm)


def matrix(case):
    H, macros, jobs, rates, T, eta, beta, rho, pool = case
    rows = [row[:H]+([None]*len(rates) if ext is None else ext)
            for row, ext in zip(macros, pool[:len(macros)])]
    for (home, p, c), ext in zip(jobs, pool[len(macros):]):
        row = [None]*H + ([None]*len(rates) if ext is None else ext)
        row[home] = p
        rows.append(row)
    return rows


def original_oracle(rows, T):
    choices = [[i for i, p in enumerate(row) if p is not None] for row in rows]
    tested = 0
    for assignment in product(*choices):
        tested += 1
        loads = [F(0)]*len(rows[0]) if rows else [F(0)]
        for row, i in zip(rows, assignment):
            loads[i] += row[i]
        if max(loads) <= T:
            return assignment, tested
    return None, tested


def verify(case, result):
    H, macros, jobs, rates, T, eta, beta, rho, pool = case
    rows = matrix(case)
    if result['status'] != 'SCHEDULE':
        return False
    assignment = result['assignment']
    assert len(assignment) == len(rows)
    loads = [F(0)]*(H+len(rates))
    for row, i in zip(rows, assignment):
        assert type(i) is int and 0 <= i < len(loads) and row[i] is not None
        loads[i] += row[i]
    assert loads == result['loads']
    assert all(p <= T for p in loads[:H])
    assert all(p <= (rho*(1+eta)+beta)*T for p in loads[H:])
    if all(any(p == 0 for p in row) for row in rows):
        assert max(loads) == 0
    return True


def fixtures():
    H, rates, T, eta, beta, rho = 2, [F(1), F(2)], F(1), F(1,8), F(1,8), F(9,8)
    macros = [[F(1), F(3,4), F(1,32)], [F(1), None, F(1,32)],
              [None, F(1), F(1,32)]]
    jobs = [(0, F(1,2), F(1,32))]*2 + [(1, F(1,2), F(1,32))]*2
    works = [row[-1] for row in macros]+[c for h,a,c in jobs]
    pool = [[c, 2*c*(F(1) if j%2 else rho)] for j,c in enumerate(works)]
    nonrank = (H, macros, jobs, rates, T, eta, beta, rho, pool)
    one = (0, [[F(1,32)]]*5, [], [F(1),F(2)], F(1), eta, beta, F(1),
           [[F(1,32),F(1,16)]]*5)
    zero = (1, [[F(1),F(0)]]*3, [(0,F(0),F(0))], [F(1),F(10)],
            F(0),eta,F(0),F(3),[[F(0),F(0)]]*4)
    output = [nonrank, one, zero, (0, [], [], [F(1)], F(0),eta,beta,F(1),[])]
    for scale in [F(1,10**40), F(10**40)]:
        h,b,s,a,t,e,d,r,p = nonrank
        output.append((h, [[None if q is None else q*scale for q in row] for row in b],
                       [(v, None if q is None else q*scale, None if c is None else c*scale)
                        for v,q,c in s], a,t*scale,e,d,r,
                       [[q*scale for q in row] for row in p]))
    return output


def random_case(rng):
    H, count = rng.randrange(4), rng.randrange(1,4)
    rates = [rng.choice([F(1,2),F(1),F(2),F(4)]) for _ in range(count)]
    T, eta, beta = rng.choice([F(0), F(1), F(1,17)]), F(1,8), F(1,8)
    rho = rng.choice([F(1),F(9,8),F(3,2)])
    unit = beta*T/(rho*max(rates))
    macros = []
    for _ in range(rng.randrange(5)):
        row = [rng.choice([None, F(1) if T == 0 else T*F(3,4),
                           F(1) if T == 0 else T, F(1) if T == 0 else T*F(5,4)])
               for _ in range(H)]
        row.append(rng.choice([None,F(0),unit/2,unit]))
        if all(p is None for p in row):
            row[-1] = F(0)
        macros.append(row)
    jobs = []
    for _ in range(rng.randrange(5) if H else 0):
        a = rng.choice([None,F(0),T/3,T,F(1) if T==0 else T*F(5,4)])
        c = rng.choice([None,F(0),unit/2,unit])
        if a is None and c is None:
            a = F(0)
        jobs.append((rng.randrange(H),a,c))
    works = [row[-1] for row in macros]+[c for h,a,c in jobs]
    pool = [None if c is None else [a*c*rng.choice([F(1),(1+rho)/2,rho]) for a in rates]
            for c in works]
    return H,macros,jobs,rates,T,eta,beta,rho,pool


def encode(value):
    if isinstance(value,F):
        return str(value)
    if isinstance(value,dict):
        return {k:encode(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):
        return [encode(v) for v in value]
    return value


def run(export=None):
    rng = random.Random(2026101606)
    selected = fixtures()
    cases = selected+[random_case(rng) for _ in range(900)]
    count = dict(cases=0,promise_cases=0,successful_outputs=0,
                 original_assignments_enumerated=0,nonrank_cases=0,zero_targets=0)
    witnesses=[]
    for index, case in enumerate(cases):
        H,b,s,a,T,eta,beta,rho,p = case
        result = algorithm.solve_exit_pool(H,b,s,a,T,eta,beta,rho,p)
        actual, examined = original_oracle(matrix(case),T)
        count['cases']+=1
        count['original_assignments_enumerated']+=examined
        count['nonrank_cases']+=rho>1
        count['zero_targets']+=T==0
        if actual is not None:
            count['promise_cases']+=1
            assert result['status']=='SCHEDULE'
        count['successful_outputs']+=verify(case,result)
        if index<len(selected):
            witnesses.append(result)
    # The arbitrary-cost single-sink helper must also allow more macros than homes.
    single = algorithm.solve_shared_sink_with_exits(1,[[F(1),F(1,16)]]*3,
                                                   [(0,F(1),None)],F(1),F(1,8))
    assert single['status']=='SCHEDULE' and single['loads']==[F(1),F(3,16)]
    h,b,s,a,T,e,d,r,p = selected[0]
    illegal=[(h,b,s,[],T,e,d,r,p), (h,b,s,[F(0)],T,e,d,r,p),
             (h,b,s,a,T,e,d,F(1,2),p), (h,b,s,a,T,e,F(0),r,p),
             (h,b,s,a,T,e,d,r,[None]*len(p)),
             (h,b,s,a,T,0.125,d,r,p)]
    for args in illegal:
        try:algorithm.solve_exit_pool(*args)
        except ValueError:pass
        else:raise AssertionError('invalid pool contract accepted')
    if export:
        export=Path(export);export.mkdir(parents=True,exist_ok=True)
        for name,data in [('private_group_exit_pool_cases.json',dict(cases=selected,
                                layout=['H','macros','private','rates','T','eta','beta','rho','pool_times'])),
                          ('private_group_exit_pool_witness.json',dict(outputs=witnesses))]:
            dest=export/name;assert not dest.exists();dest.write_text(json.dumps(encode(data),indent=2)+'\n')
    return dict(arithmetic='fractions.Fraction',python=sys.version.split()[0],seed=2026101606,
                algorithm_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                audit_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                parameters=dict(eta='1/8',beta='1/8',rho=['1','9/8','3/2']),
                counts=count,illegal_contracts=len(illegal),single_sink_exit_control=True,
                limits='Finite exact oracle checks for the stated pool class; no general approximation or exhaustive parameter claim.')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--export-dir');args=parser.parse_args()
    print(json.dumps(run(args.export_dir),indent=2))
