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


def _rational(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, str, Q)):
        raise ValueError(f'{name} must be an exact rational, not a bool or float')
    try:
        return Q(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError(f'{name} must be a finite exact rational') from exc


def _sequence(value, name):
    if not isinstance(value, (list, tuple)):
        raise ValueError(f'{name} must be an array')
    return value


def _indices(value, size, name):
    values = _sequence(value, name)
    if any(type(i) is not int or not 0 <= i < size for i in values):
        raise ValueError(f'{name} contains an invalid integer index')
    return values


def parse(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be an object')
    try:
        w = [_rational(x, 'weight') for x in
             _sequence(instance['weights'], 'weights')]
        if any(x <= 0 for x in w):
            raise ValueError('weights must be positive')
        sites = [set(_indices(x, len(w), 'location customers')) for x in
                 _sequence(instance['locations'], 'locations')]
        u1 = list(dict.fromkeys(_indices(instance['U1'], len(sites), 'U1')))
        u2 = list(dict.fromkeys(_indices(instance['U2'], len(sites), 'U2')))
    except KeyError as exc:
        raise ValueError(f'missing input field: {exc.args[0]}') from exc
    if not u1 or not u2:
        raise ValueError('nonempty catalogs are required')
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
    """Check a finite attainment certificate without support enumeration.

    Negative existence reports cannot be certified by this witness checker.
    Validation uses explicit exceptions and remains active under python -O.
    """
    w,sites,u1,u2 = parse(instance)

    def require(condition, message):
        if not condition:
            raise ValueError(message)

    def field(obj, key):
        require(isinstance(obj, dict), 'certificate records must be objects')
        require(key in obj, f'missing certificate field: {key}')
        return obj[key]

    require(field(result, 'finite_factor_exists') is True,
            'a finite attainment witness is required; negative reports are not verified')
    alpha = _rational(field(result, 'alpha'), 'alpha')
    require(alpha >= 1, 'alpha must be at least one')

    def check(rec):
        layout = _indices(field(rec, 'layout'), len(sites), 'layout')
        require(len(layout) == 2, 'layout must contain two locations')
        s,t = layout
        require(s in u1 and t in u2, 'layout is outside the permitted catalogs')
        common = sorted(sites[s]&sites[t])
        shared = _indices(field(rec, 'shared'), len(w), 'shared')
        require(common == list(shared), 'shared customer IDs do not match the layout')
        p = [_rational(z, 'probability') for z in
             _sequence(field(rec, 'prob_first'), 'prob_first')]
        require(len(common) == len(p), 'wrong probability vector length')
        require(all(0 <= z <= 1 for z in p), 'probabilities must lie in [0,1]')
        x = sum((w[i] for i in sites[s]-sites[t]),Q(0))
        y = sum((w[i] for i in sites[t]-sites[s]),Q(0))
        x += sum((w[i]*z for i,z in zip(common,p)),Q(0))
        y += sum((w[i]*(1-z) for i,z in zip(common,p)),Q(0))
        loads = [_rational(z, 'load') for z in
                 _sequence(field(rec, 'loads'), 'loads')]
        require([x,y] == loads, 'reported loads do not match probabilities')
        for i,z in zip(common,p):
            diff = x-y+w[i]*(1-2*z)
            require((z == 0 or diff <= 0) and (z == 1 or diff >= 0),
                    'customer continuation is not an exact Nash equilibrium')
        return x,y

    on_path = field(result, 'on_path')
    x,y = check(on_path)
    s,t = on_path['layout']
    expected = {(1,r,t) for r in u1 if r != s}|{(2,s,r) for r in u2 if r != t}
    seen = set()
    for rec in _sequence(field(result, 'deviations'), 'deviations'):
        deviator = field(rec, 'deviator')
        require(type(deviator) is int and deviator in (1,2), 'invalid deviator')
        witness_rec = field(rec, 'witness')
        a,b = check(witness_rec)
        ds,dt = witness_rec['layout']
        key = deviator,ds,dt
        require(key in expected, 'witness is not an actual unilateral deviation')
        require(key not in seen, 'duplicate deviation witness')
        seen.add(key)
        require((a if deviator == 1 else b) <= alpha*(x if deviator == 1 else y),
                'facility deviation exceeds the reported factor')
    require(seen == expected, 'missing deviation witnesses')


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
    with open(args.input) as f: instance = json.load(f, parse_float=str)
    text = json.dumps(serial(solve(instance)),ensure_ascii=False,indent=2)
    if args.output:
        with open(args.output,'w') as f:f.write(text+'\n')
    else:print(text)
