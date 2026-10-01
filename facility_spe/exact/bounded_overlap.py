#!/usr/bin/env python3
"""Exact optimal SPE approximation for two facilities with bounded cross overlap.

Input: {weights:[positive rational strings], locations:[[client ids],...],
        U1:[site ids], U2:[site ids]}.
Runtime: O(|U1||U2| (n + kappa 3**kappa)) rational operations.
"""
from fractions import Fraction as Q
from itertools import product
import argparse
import json


def parse(instance):
    w = [Q(str(x)) for x in instance['weights']]
    sites = [set(x) for x in instance['locations']]
    u1 = list(dict.fromkeys(instance['U1']))
    u2 = list(dict.fromkeys(instance['U2']))
    if not u1 or not u2 or any(x <= 0 for x in w):
        raise ValueError('positive weights and nonempty catalogs are required')
    if any(not 0 <= i < len(w) for s in sites for i in s):
        raise ValueError('bad client index')
    if any(not 0 <= s < len(sites) for s in u1+u2):
        raise ValueError('bad location index')
    return w, sites, u1, u2


def local(w, sites, s, t):
    shared = sorted(sites[s] & sites[t])
    a = sum((w[i] for i in sites[s]-sites[t]), Q(0))
    b = sum((w[i] for i in sites[t]-sites[s]), Q(0))
    v = [w[i] for i in shared]
    total = a+b+sum(v, Q(0))
    delta = a-b
    pieces = []
    for states in product((-1,0,1), repeat=len(v)):
        mixers = [i for i,z in enumerate(states) if z == 0]
        c = delta+sum((z*x for z,x in zip(states,v)), Q(0))
        m = len(mixers)
        if m == 0:
            lo = hi = c
        elif m == 1:
            if c:
                continue
            lo,hi = -v[mixers[0]],v[mixers[0]]
        else:
            lo = hi = -c/Q(m-1)
        # Closures of support cells: endpoints may turn designated mixers pure.
        for z,x in zip(states,v):
            if z == 1:
                hi = min(hi,x)
            elif z == -1:
                lo = max(lo,-x)
            else:
                lo,hi = max(lo,-x),min(hi,x)
        if lo <= hi:
            pieces.append({'states':states,'gap_lo':lo,'gap_hi':hi,
                           'lo':(total+lo)/2,'hi':(total+hi)/2})
    if not pieces:
        raise AssertionError('a pure client NE must exist')
    return {'shared':shared,'weights':v,'a':a,'b':b,'total':total,
            'pieces':pieces,
            'min_piece':min(pieces,key=lambda z:z['lo']),
            'max_piece':max(pieces,key=lambda z:z['hi'])}


def witness(s,t,rec,piece,x):
    gap = 2*x-rec['total']
    assert piece['gap_lo'] <= gap <= piece['gap_hi']
    p = [Q(z+1,2) if z else (1+gap/w)/2
         for z,w in zip(piece['states'],rec['weights'])]
    return {'layout':[s,t], 'shared':rec['shared'], 'prob_first':p,
            'loads':[x,rec['total']-x]}


def ratio(n,d):
    return Q(0) if n == 0 else n/d if d else None


def solve(instance):
    w,sites,u1,u2 = parse(instance)
    data = {(s,t):local(w,sites,s,t) for s in u1 for t in u2}
    d1 = {t:max(data[s,t]['min_piece']['lo'] for s in u1) for t in u2}
    d2 = {s:max(data[s,t]['total']-data[s,t]['max_piece']['hi'] for t in u2)
          for s in u1}
    best = None
    for (s,t),rec in data.items():
        for piece in rec['pieces']:
            den = d1[t]+d2[s]
            target = rec['total']*d1[t]/den if den else piece['lo']
            x = max(piece['lo'],min(piece['hi'],target))
            r1,r2 = ratio(d1[t],x),ratio(d2[s],rec['total']-x)
            if r1 is None or r2 is None:
                continue
            alpha = max(Q(1),r1,r2)
            if best is None or alpha < best[0]:
                best = alpha,s,t,piece,x
    if best is None:
        return {'finite_factor_exists':False}
    alpha,s,t,piece,x = best
    off = []
    for r in u1:
        if r != s:
            rec = data[r,t]; p = rec['min_piece']
            off.append({'deviator':1,'witness':witness(r,t,rec,p,p['lo'])})
    for r in u2:
        if r != t:
            rec = data[s,r]; p = rec['max_piece']
            off.append({'deviator':2,'witness':witness(s,r,rec,p,p['hi'])})
    result = {'finite_factor_exists':True,'alpha':alpha,
              'kappa':max(len(z['shared']) for z in data.values()),
              'on_path':witness(s,t,data[s,t],piece,x),
              'deviations':off,
              'default_continuation':'enumerate local() and choose its first piece lower endpoint'}
    verify(instance,result)
    return result


def verify(instance,result):
    """Checks attainment directly, without invoking the support enumerator."""
    if not result['finite_factor_exists']:
        return
    w,sites,u1,u2 = parse(instance)
    alpha = Q(result['alpha'])
    assert alpha >= 1
    def check(rec):
        s,t = rec['layout']
        assert s in u1 and t in u2
        common = sorted(sites[s]&sites[t])
        assert common == rec['shared']
        p = list(map(Q,rec['prob_first']))
        assert len(common) == len(p)
        assert all(0 <= z <= 1 for z in p)
        x = sum((w[i] for i in sites[s]-sites[t]),Q(0))
        y = sum((w[i] for i in sites[t]-sites[s]),Q(0))
        x += sum((w[i]*z for i,z in zip(common,p)),Q(0))
        y += sum((w[i]*(1-z) for i,z in zip(common,p)),Q(0))
        assert [x,y] == list(map(Q,rec['loads']))
        for i,z in zip(common,p):
            diff = x-y+w[i]*(1-2*z)
            assert (z == 0 or diff <= 0) and (z == 1 or diff >= 0)
        return x,y
    x,y = check(result['on_path'])
    s,t = result['on_path']['layout']
    expected = {(1,r,t) for r in u1 if r != s}|{(2,s,r) for r in u2 if r != t}
    seen = set()
    for rec in result['deviations']:
        a,b = check(rec['witness'])
        ds,dt = rec['witness']['layout']
        assert rec['deviator'] in (1,2)
        key = rec['deviator'],ds,dt
        assert key not in seen
        seen.add(key)
        assert (a if rec['deviator'] == 1 else b) <= alpha*(x if rec['deviator'] == 1 else y)
    assert seen == expected


def serial(value):
    if isinstance(value,Q):return str(value)
    if isinstance(value,(list,tuple)):return [serial(x) for x in value]
    if isinstance(value,dict):return {k:serial(v) for k,v in value.items()}
    return value


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('--output')
    args = parser.parse_args()
    with open(args.input) as f: instance = json.load(f)
    text = json.dumps(serial(solve(instance)),ensure_ascii=False,indent=2)
    if args.output:
        with open(args.output,'w') as f:f.write(text+'\n')
    else:print(text)
