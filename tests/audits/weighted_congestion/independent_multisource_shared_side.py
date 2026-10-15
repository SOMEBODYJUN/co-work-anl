#!/usr/bin/env python3
"""Independent literal resource audit; uses no author code. Scratch-only finite evidence."""
from fractions import Fraction as Q
from itertools import product
import random, json, hashlib, sys
from pathlib import Path

SEED=706241
rng=random.Random(SEED)
def poly(p,x):
    z=Q(0)
    for c in reversed(p): z=z*x+c
    return z

def emitq(v):
    if isinstance(v,Q): return str(v)
    if isinstance(v,dict): return {str(k):emitq(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)): return [emitq(x) for x in v]
    return v

def build(case):
    n=case['hubs']; u=case['u']; lights=case['lights']; side=case['sides']; F=case['F']
    weights=[u]*n+[x['w'] for x in lights]
    res={}; acts=[]
    for v in range(n):
        for b in (0,1): res[('A',v,b)]=F[v]
    for j,s in enumerate(side):
        for b in (0,1): res[('B',j,b)]=s['G']
    for v in range(n): acts.append([{('A',v,b)}|{('B',j,b) for j,s in enumerate(side) if v in s['H']} for b in (0,1)])
    for l,x in enumerate(lights): acts.append([{('A',x['source'],b)}|{('B',j,1-b) for j,s in enumerate(side) if l in s['L']} for b in (0,1)])
    def loads(state):
        z={e:Q(0) for e in res}
        for p,b in enumerate(state):
            for e in acts[p][b]: z[e]+=weights[p]
        return z
    def cost(state,p):
        z=loads(state)
        return sum((poly(res[e],z[e]) for e in acts[p][state[p]]),Q(0))
    def E(state):
        z=loads(state); val=Q(0)
        for j,s in enumerate(side):
            for b in (0,1):
                e=('B',j,b)
                k=sum(e in acts[v][state[v]] for v in range(n))
                light_load=z[e]-k*u
                val+=sum((poly(s['G'],light_load+r*u) for r in range(1,k+1)),Q(0))
        return val
    return acts,res,cost,E,loads

def generated(d,alpha,index):
    n=rng.randint(1,4); u=Q(rng.randint(1,4),rng.randint(1,3))
    # Total source light weight <= u/(4d), guaranteeing positive monomial UF slack.
    counts=[rng.randint(0,2) for _ in range(n)]
    lights=[]
    for v,c in enumerate(counts):
        for z in range(c): lights.append({'source':v,'w':u*Q(rng.randint(1,4),16*d*max(1,c))})
    sides=[]
    for j in range(rng.randint(0,5)):
        typ=(index+j)%5
        if typ==0: G=[Q(0)]*(d+1)
        elif typ==1: G=[Q(rng.randint(1,3))]+[Q(0)]*d
        else: G=[Q(rng.randint(0,2),rng.randint(1,3)) if rng.random()<0.4 else Q(0) for _ in range(d+1)]
        sides.append({'H':[v for v in range(n) if rng.choice((0,1))], 'L':[l for l in range(len(lights)) if rng.choice((0,1))], 'G':G})
    F=[]
    for v in range(n):
        ll=[l for l,x in enumerate(lights) if x['source']==v]
        W=sum((lights[l]['w'] for l in ll),Q(0))
        if not ll:
            if index%3==0: F.append([Q(0)]*(d+1))
            elif index%3==1: F.append([Q(rng.randint(0,3))]+[Q(0)]*d)
            else: F.append([Q(rng.randint(0,2)) for _ in range(d+1)])
            continue
        a=Q(1)
        for l in ll:
            w=lights[l]['w']; rhs=Q(0)
            for s in sides:
                if l in s['L']:
                    T=sum((lights[k]['w'] for k in s['L']),Q(0))
                    rhs+=alpha*poly(s['G'],T+len(s['H'])*u)-poly(s['G'],w)
            den=(u+w)**d-alpha*W**d
            assert den>0
            a=max(a,rhs/den)
        F.append([Q(0)]*d+[a])
    return {'name':f'random-d{d}-a{alpha}-{index}','d':d,'alpha':Q(alpha),'hubs':n,'u':u,'lights':lights,'sides':sides,'F':F}

def audit(case):
    n=case['hubs']; u=case['u']; L=case['lights']; sides=case['sides']; F=case['F']; a=case['alpha']; d=case['d']
    for l,x in enumerate(L):
        v=x['source']; W=sum((y['w'] for y in L if y['source']==v),Q(0))
        lhs=poly(F[v],u+x['w']); rhs=poly(F[v],W)
        for s in sides:
            if l in s['L']:
                T=sum((L[k]['w'] for k in s['L']),Q(0))
                lhs+=poly(s['G'],x['w']); rhs+=poly(s['G'],T+len(s['H'])*u)
        assert lhs>=a*rhs, ('UF',case['name'],l)
    acts,res,cost,E,loads=build(case)
    def anti(h): return list(h)+[1-h[x['source']] for x in L]
    mincount=0; checks=0; resetchecks=0
    for h in product((0,1),repeat=n):
        state=anti(h); ev=E(state)
        local=True
        for v in range(n):
            hp=list(h); hp[v]^=1; reset=anti(hp)
            deviation=state.copy(); deviation[v]^=1
            # Exact fixed-light Rosenthal identity, using only actual resource costs.
            sidecur=cost(state,v)-poly(F[v],u)
            W=sum((x['w'] for x in L if x['source']==v),Q(0))
            sidenew=cost(deviation,v)-poly(F[v],u+W)
            assert ev-E(deviation)==sidecur-sidenew, ('identity',case['name'],h,v)
            # Reset is evaluated literally after the hub moved; may reduce potential.
            resetdelta=E(reset)-E(deviation)
            R=Q(0)
            for l,x in enumerate(L):
                if x['source']!=v: continue
                kappa=min(d*x['w']/u,x['w']/u+1)
                R+=kappa*sum((poly(s['G'],sum((L[k]['w'] for k in s['L']),Q(0))+len(s['H'])*u) for s in sides if l in s['L']),Q(0))
            assert resetdelta<=R, ('reset-bound',case['name'],h,v)
            M=a*poly(F[v],u+W)-poly(F[v],u)
            assert R<=M, ('source-budget',case['name'],h,v)
            resetchecks+=1
            if E(reset)<ev: local=False
        if local:
            mincount+=1
            for p in range(len(state)):
                dev=state.copy(); dev[p]^=1
                assert cost(state,p)<=a*cost(dev,p), ('PNE',case['name'],h,p)
                if p>=n: assert a*cost(state,p)<=cost(dev,p), ('strong-light',case['name'],h,p)
                checks+=1
    assert mincount>0
    return {'anti_states':2**n,'local_minima':mincount,'literal_player_checks':checks,'reset_checks':resetchecks}

cases=[]
for d,a in ((2,Q(121,50)),(3,Q(41,15)),(4,Q(3)),(6,Q(69,20)),(9,Q(4)),(10,Q(833,200)),(16,Q(5))):
    assert (a-1)**2>=d
    for i in range(12): cases.append(generated(d,a,i))
# All-zero and all-constant special cases with no lights, empty sides and empty H.
for name,F,sides in [
 ('zero-empty',[ [Q(0)] ],[]),
 ('constant-empty-light',[[Q(2)]],[{'H':[0], 'L':[], 'G':[Q(3)]},{'H':[],'L':[],'G':[Q(5)]}]),
]: cases.append({'name':name,'d':2,'alpha':Q(4),'hubs':1,'u':Q(1),'lights':[],'sides':sides,'F':F})
cases.append({'name':'zero-fees-large-multisource-lights','d':4,'alpha':Q(3),'hubs':3,'u':Q(1),'lights':[{'source':0,'w':Q(100)},{'source':1,'w':Q(1,2)},{'source':1,'w':Q(3)},{'source':2,'w':Q(2)}],'sides':[{'H':[0,2],'L':[0,1,2,3],'G':[Q(0)]},{'H':[],'L':[0,3],'G':[Q(0)]},{'H':[1],'L':[],'G':[Q(3)]}],'F':[[Q(0)],[Q(0)],[Q(0)]]})
records=[]
for case in cases:
    records.append({'parameters':emitq(case),'checks':audit(case)})
summary={k:sum(x['checks'][k] for x in records) for k in ('anti_states','local_minima','literal_player_checks','reset_checks')}
summary['games']=len(records)
result={'audit':'independent literal resource Fraction enumeration','scope':'finite evidence only; no author functions imported','command':'python3 tests/audits/weighted_congestion/independent_multisource_shared_side.py','python':sys.version,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'reviewed_freeze_sha256':{'original_weaker_candidate':'f69fba0b27e07068b44f9d8090f69078ac78e825ace8ade7b91ed420a840c336','sqrt_strengthening_candidate':'3f5c2025275b0f4dc186425427840c6100816307de58deba4bb530fb0a9f6711'},'seed':SEED,'generation':'complete parameters below; RNG random.Random; all costs exact fractions; d/alpha variants are rational at/just above alpha=1+sqrt(d), including exact d4 alpha3, d9 alpha4, d16 alpha5; arbitrary H/L independently selected; repeated lights across sides allowed; F monomial scaled from exact UF slack; no-light F zero/constant/general polynomial','summary':summary,'cases':records}
print(json.dumps(result,ensure_ascii=False,indent=2))
