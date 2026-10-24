"""Attack a precise general candidate: fixed-owner CLIP permits role cap 2.

This is a finite candidate attack, never a proof of HALF or its negation.
All decisions use a full ordered-history certificate.  LP outputs only propose
a separation; a found candidate is subsequently independently rationalized.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations, permutations
from pathlib import Path
import argparse
import json
import random
import sys

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT))
from customer_attraction.model import Instance, CustomerType
from customer_attraction.exact import ExactSPESolver
from customer_attraction.certificate import verify_certificate
from scipy.optimize import linprog


def model(ins, cert, optimum):
    m = ins.players
    types = [(x.topics, x.multiplicity) for x in ins.customers]
    def finish(h):
        h = tuple(h)
        while len(h) < m:
            h += (cert.actions[h],)
        return h
    def counts(z):
        return tuple(sum(a in likes for a in z) for likes, _ in types)
    def pay(z, i):
        c = counts(z)
        return sum((F(w, c[x]) for x, (likes,w) in enumerate(types) if z[i] in likes), F())
    Z = finish(())
    u = ins.player_payoffs(Z)
    source = [F() for _ in range(m)]
    b = defaultdict(F)
    for x, (likes,w) in enumerate(types):
        owners = [i for i,a in enumerate(optimum) if a in likes]
        if not owners:
            continue
        i = owners[0]
        Y = finish(Z[:i] + (optimum[i],))
        amount = F(w, counts(Y)[x])
        for j,a in enumerate(Y):
            if a not in likes:
                continue
            if j <= i:
                source[j] += amount
            else:
                b[Y[:j]] += amount
    records = {}
    queue = list(b)
    while queue:
        g = queue.pop()
        if g in records:
            continue
        i = len(g)
        B = finish(g)
        a = B[i]
        A = finish(Z[:i] + (a,))
        ca, cb = counts(A), counts(B)
        v = pay(B,i)
        assert v > 0
        caps = defaultdict(F)
        neg = F()
        for x,(likes,w) in enumerate(types):
            if a not in likes:
                continue
            JA = {j for j in range(m) if j != i and A[j] in likes}
            JB = {j for j in range(m) if j != i and B[j] in likes}
            raw = F(w, ca[x]*cb[x])
            neg += raw*len(JB-JA)
            for j in JA-JB:
                target = ('role',j) if j < i else ('node',A[:j])
                caps[target] += raw/v
        delta = max(F(), 1-u[i]/v)
        assert sum(caps.values(),F()) >= delta
        records[g] = {'v':v,'i':i,'absorb':min(F(1),u[i]/v),'delta':delta,'caps':dict(caps)}
        if delta:
            queue.extend(t[1] for t in caps if t[0] == 'node')
    nodes = sorted(records, key=lambda h:(len(h),h))
    ix = {g:i for i,g in enumerate(nodes)}
    arcs = [(g,t,c) for g in nodes if records[g]['delta'] for t,c in records[g]['caps'].items()]
    n = len(nodes)
    nv = n+len(arcs)+1
    eq, rhs = [], []
    for g in nodes:
        row = [F()]*nv
        row[ix[g]] = 1
        for k,(s,t,c) in enumerate(arcs):
            if t == ('node',g): row[n+k] -= 1
        eq.append(row); rhs.append(b[g])
        row = [F()]*nv
        row[ix[g]] = -records[g]['delta']
        for k,(s,t,c) in enumerate(arcs):
            if s == g: row[n+k] += 1
        eq.append(row); rhs.append(F())
    ub, urhs = [], []
    for k,(g,t,c) in enumerate(arcs):
        row=[F()]*nv
        row[n+k]=1; row[ix[g]]=-c
        ub.append(row); urhs.append(F())
    for j in range(m):
        row=[F()]*nv
        for g in nodes:
            if records[g]['i']==j: row[ix[g]]=records[g]['absorb']
        for k,(g,t,c) in enumerate(arcs):
            if t==('role',j): row[n+k]+=1
        row[-1]=-u[j]
        ub.append(row); urhs.append(-source[j])
    obj=[0.]*(nv-1)+[1.]
    fit=linprog(obj,A_ub=[[float(x) for x in row] for row in ub],b_ub=list(map(float,urhs)),
                A_eq=[[float(x) for x in row] for row in eq] if eq else None,
                b_eq=list(map(float,rhs)) if eq else None,bounds=(0,None),method='highs')
    if not fit.success:
        raise RuntimeError(fit.message)
    return fit.fun, {'actual':Z,'u':list(map(str,u)),'source':list(map(str,source)),
                     'initial':{str(g):str(v) for g,v in b.items()},'nodes':n,'arcs':len(arcs)}


def attack(seed, trials, players, topics, output):
    rng=random.Random(seed)
    best=0.
    for trial in range(trials):
        customers=[]
        for mask in range(1,1<<topics):
            if rng.random()<.5:
                customers.append(CustomerType(frozenset(a for a in range(topics) if mask>>a&1),rng.randint(1,8)))
        ins=Instance(tuple(map(str,range(topics))),tuple(customers),players)
        solver=ExactSPESolver(ins)
        targets=sorted(solver.worst_outcomes())
        cert=solver.certificate(rng.choice(targets),
              action_selector=lambda h,opts:rng.choice(opts),
              continuation_selector=lambda h,opts:rng.choice(opts))
        opt=max((s for k in range(1,min(topics,players)+1) for s in combinations(range(topics),k)),
                key=lambda s:ins.welfare(tuple(int(a in s) for a in range(topics))))
        optimum=tuple(opt)+(opt[0],)*(players-len(opt))
        rngopt=list(optimum);rng.shuffle(rngopt)
        value, data=model(ins,cert,tuple(rngopt))
        if value>best+1e-7:
            best=value
            print(json.dumps({'trial':trial,'best_float':best,**data}),flush=True)
        if value>2+1e-7:
            ver=verify_certificate(ins,cert);ver.assert_valid()
            item={'candidate':'fixed assignment first-owner CLIP role-cap2',
                  'status':'FLOAT LP SEPARATION; exact dual pending',
                  'seed':seed,'trial':trial,'instance':ins.to_dict(),'certificate':cert.to_dict(),
                  'optimum':rngopt,'float_cap':value,'details':data,
                  'checked_histories':ver.checked_histories,'checked_deviations':ver.checked_deviations}
            Path(output).write_text(json.dumps(item,indent=2)+'\n')
            return
    Path(output).write_text(json.dumps({'status':'finite attack no separation','candidate':'fixed assignment first-owner CLIP role-cap2',
        'seed':seed,'trials':trials,'players':players,'topics':topics,'best_float':best},indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seed',type=int,default=9021)
    p.add_argument('--trials',type=int,default=100);p.add_argument('--players',type=int,default=4)
    p.add_argument('--topics',type=int,default=4);p.add_argument('--output',required=True)
    a=p.parse_args();attack(a.seed,a.trials,a.players,a.topics,a.output)
