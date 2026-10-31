#!/usr/bin/env python3
"""Finite exact-integer oracles for ordered EF1 on the two published key matroids.

This evaluates finite valuation profiles, never the universal existence question.
"""
from itertools import permutations, product
from pathlib import Path
import hashlib, json, platform, random, math
import numpy as np


def allocations(groups, n=4, capacity=None):
    if n < 1 or not groups or any(type(k) is not int or k < 1 or k > n for k in groups):
        raise ValueError("positive groups, each at most n")
    m = sum(groups)
    if capacity is None:
        if m % n:
            raise ValueError("balanced complete key requires m divisible by n")
        capacity = m // n
    if type(capacity) is not int or capacity < 1 or n * capacity != m:
        raise ValueError("complete key requires n*capacity == m")
    choices = [list(permutations(range(n), k)) for k in groups]
    rows = []
    for selected in product(*choices):
        a = tuple(x for row in selected for x in row)
        if all(a.count(i) == capacity for i in range(n)):
            rows.append(a)
    return np.asarray(rows, dtype=np.int64).reshape((-1, m))


def validate_values(values, n, m):
    if len(values) != n or any(len(row) != m for row in values):
        raise ValueError("wrong valuation shape")
    if any(type(x) is not int or x < 0 or x > 10**6 for row in values for x in row):
        raise ValueError("oracle contract: integers in [0,10**6]")
    return np.asarray(values, dtype=np.int64)


def check_profile(rows, values):
    if rows.ndim != 2 or not rows.size or np.any(rows < 0):
        raise ValueError("nonempty assignment matrix required")
    n = int(rows.max()) + 1; m = rows.shape[1]
    v = validate_values(values, n, m)
    masks = rows[:, None, :] == np.arange(n)[None, :, None]
    utilities = np.einsum("igm,jm->ijg", masks, v)  # allocation, evaluator, recipient
    own = utilities[:, np.arange(n), np.arange(n)]
    largest = np.where(masks[:, None, :, :], v[None, :, None, :], 0).max(axis=3)
    ef1 = (own[:, :, None] >= utilities - largest).all(axis=(1,2))
    upper = np.triu(np.ones((n,n),dtype=bool),1)
    ordered = ((own[:, :, None] >= utilities) | ~upper[None,:,:]).all(axis=(1,2))
    serial = np.arange(len(rows))
    for i in range(n):
        serial = serial[own[serial,i] == own[serial,i].max()]
    if not ordered[serial].all():
        raise AssertionError("serial dictatorship must have ordered no envy")
    good = np.flatnonzero(ef1 & ordered)
    return {"feasible_count":len(rows),"ordered_ef1_count":len(good),
            "witness":rows[good[0]].tolist() if len(good) else None,
            "serial_ties":len(serial), "serial_good_count":int(ef1[serial].sum()),
            "serial_witness":rows[serial[0]].tolist()}


def direct_check(assignment, values):
    n=len(values)
    bundles=[[g for g,who in enumerate(assignment) if who==i] for i in range(n)]
    for i in range(n):
        own=sum(values[i][g] for g in bundles[i])
        for j in range(n):
            if i<j and own<sum(values[i][g] for g in bundles[j]):
                return False
            if bundles[j] and not any(own>=sum(values[i][h] for h in bundles[j] if h!=g) for g in bundles[j]):
                return False
    return True


def run():
    seed=20261020; rng=random.Random(seed)
    a8=allocations((3,3,2)); a12=allocations((3,3,3,3))
    # Independent labelled enumeration checks feasibility without group injections.
    manual=[]
    for a in product(range(4),repeat=8):
        if all(a.count(i)==2 for i in range(4)) and all(len(set(a[s:t]))==t-s for s,t in ((0,3),(3,6),(6,8))):
            manual.append(a)
    assert set(manual)==set(map(tuple,a8))
    assert len(a8)==4*3*math.factorial(3)**2*math.factorial(2)
    assert len(a12)==math.factorial(4)*math.factorial(3)**4
    rejected=0
    for args in [((3,3,2),0,None), ((5,3),4,None), ((3,3,1),4,None), ((3,3,2),4,3)]:
        try: allocations(*args)
        except ValueError: rejected+=1
        else: raise AssertionError("invalid key accepted")
    results=[]; serial_failure=None
    for groups,rows,num in [((3,3,2),a8,80),((3,3,3,3),a12,12)]:
        m=sum(groups)
        profiles=[[[0]*m for _ in range(4)], [[1]*m for _ in range(4)],
                  [[int(g==i) for g in range(m)] for i in range(4)],
                  [[(g%3)+1 for g in range(m)] for _ in range(4)]]
        profiles += [[[rng.randrange(21) for _ in range(m)] for _ in range(4)] for __ in range(num)]
        good_counts=[]
        for k,v in enumerate(profiles):
            r=check_profile(rows,v); good_counts.append(r["ordered_ef1_count"])
            if r["witness"] is not None: assert direct_check(r["witness"],v)
            if groups==(3,3,2) and k<8:
                assert r["ordered_ef1_count"]==sum(direct_check(a,v) for a in rows)
            if serial_failure is None and r["serial_good_count"]==0 and r["witness"] is not None:
                serial_failure={"groups":groups,"values":v,**r}
                assert not direct_check(r["serial_witness"],v)
        results.append({"groups":groups,"allocations":len(rows),"profiles":len(profiles),
                        "minimum_good_count":min(good_counts),"zero_good_profiles":sum(x==0 for x in good_counts)})
    # Additional oracle rejection cases; no float coercion or overflow permitted.
    for bad in [[], [[0]*8 for _ in range(3)], [[-1]*8 for _ in range(4)], [[1.0]*8 for _ in range(4)], [[10**7]*8 for _ in range(4)]]:
        try: check_profile(a8,bad)
        except (ValueError,IndexError): rejected+=1
        else: raise AssertionError("invalid values accepted")
    return {"claim":"SEL-LAMINAR4-KEY-v1","status":"finite observation only", "seed":seed,
            "arithmetic":"exact int64; input bounded by 10**6; bundle size <=3", "python":platform.python_version(),
            "numpy":np.__version__,"source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "independent_checks":"all 8-item labelled feasible allocations; direct removal oracle on 8 profiles; all returned witnesses",
            "invalid_inputs_rejected":rejected,"results":results,"serial_failure":serial_failure}

if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser(); parser.add_argument("--output",type=Path,required=True); args=parser.parse_args()
    result=run()
    with args.output.open("x") as f: json.dump(result,f,ensure_ascii=False,indent=2); f.write("\n")
    print(json.dumps(result,ensure_ascii=False,indent=2))
