"""Exploratory fixed complete-policy LP attack. Positive result requires exact replay."""
import itertools,json,random,time,math
from pathlib import Path
from fractions import Fraction
import numpy as np
from scipy.optimize import linprog
from customer_attraction.model import Instance, CustomerType, big_theme_lower_bound
from customer_attraction.exact import ExactSPESolver
from customer_attraction.certificate import StrategyCertificate,verify_certificate
OUT=Path(__file__).resolve().parent
rng=random.Random(40051)

def data(n,m,cert):
    masks=np.arange(1,1<<n)
    bits=np.array([[(mask>>j)&1 for j in range(n)] for mask in masks],dtype=float)
    rows=[]
    cache={}
    def vec(q,a):
        key=(q,a)
        if key not in cache:
            load=bits@np.array(q)
            cache[key]=np.divide(bits[:,a],load,out=np.zeros(len(masks)),where=load>0)
        return cache[key]
    def walk(h):
        if len(h)==m:
            return tuple(h.count(a) for a in range(n))
        branches=[walk(h+(a,)) for a in range(n)]
        a=cert.actions[h]
        own=vec(branches[a],a)
        for b in range(n):
            if b!=a: rows.append(vec(branches[b],b)-own)
        return branches[a]
    q=walk(())
    load=bits@np.array(q)
    w=(load>0).astype(float)
    f=w+load/(load+1)
    return np.array(rows),bits,q,w,f

def instfrom(n,m,weights):
    return Instance(tuple(map(str,range(n))),tuple(CustomerType(frozenset(j for j in range(n) if mask>>j&1),int(v)) for mask,v in enumerate(weights,1) if v),m)

best=1.0
records=[]
started=time.time()
for it in range(160):
    n,m=rng.choice(((5,4),(6,4),(7,3),(6,5)))
    if it%4==0:
        # one crowded hub, individually sparse peripheral topics, plus sparse overlaps.
        weights=[0]*((1<<n)-1)
        weights[0]=m*rng.randint(1,5)
        for a in range(1,n): weights[(1<<a)-1]=rng.randint(1,5)
        for _ in range(3):
            mask=rng.randrange(1,1<<n);weights[mask-1]+=rng.randrange(3)
    else:
        weights=[0]*((1<<n)-1)
        for _ in range(rng.randint(n,3*n)):
            size=rng.choice((1,1,2,2,3))
            mask=sum(1<<j for j in rng.sample(range(n),min(n,size)))
            weights[mask-1]+=rng.randint(1,8)
    inst=instfrom(n,m,weights)
    oracle=ExactSPESolver(inst)
    outcomes=oracle.outcomes()
    # preferably concentrate terminal loads or choose weakest tax terminal.
    def gap(q):
        w=inst.welfare(q)
        tax=sum(Fraction(c.multiplicity*load,load+1) for c in inst.customers if (load:=sum(q[j] for j in c.topics)))
        return inst.optimal_welfare()-w-tax
    q=max(outcomes,key=gap)
    cert=oracle.certificate(q)
    mat,bits,q,w,f=data(n,m,cert)
    objbest=None
    # For n>m every fixed optimal-support comparison is a valid attack objective.
    for support in itertools.combinations(range(n),min(n,m)):
        o=(bits[:,support].sum(axis=1)>0).astype(float)
        res=linprog(f-o,A_ub=mat,b_ub=np.zeros(mat.shape[0]),A_eq=w[None,:],b_eq=[1],bounds=(0,None),method='highs')
        if res.success and (objbest is None or res.fun<objbest[0]): objbest=(res.fun,res.x,support)
    fun,x,support=objbest
    records.append({'iteration':it,'n':n,'m':m,'q':q,'tax_minus_fixed_opt':float(fun)})
    if fun<best-1e-9:
        best=fun
        print(json.dumps({'it':it,'n':n,'m':m,'q':q,'minimum_slack':fun,'support':support}),flush=True)
        # preserve rationalized proposal even before verification.
        vals=[Fraction(float(v)).limit_denominator(1000000) for v in x]
        den=math.lcm(*(v.denominator for v in vals))
        ints=[int(v*den) for v in vals]
        gcd=math.gcd(*ints);ints=[v//gcd for v in ints]
        exact=instfrom(n,m,ints)
        ver=verify_certificate(exact,cert)
        exactW=exact.welfare(q)
        exactG=sum((Fraction(c.multiplicity*load,load+1) for c in exact.customers if (load:=sum(q[j] for j in c.topics))),Fraction())
        exactO=exact.optimal_welfare()
        proposal={'instance':exact.to_dict(),'certificate':cert.to_dict(),'verification_valid':ver.valid,'violations':len(ver.violations),'tax_minus_opt':str(Fraction(exactW)+exactG-exactO)}
        (OUT/'tax_cone_best.json').write_text(json.dumps(proposal,indent=2))
        if ver.valid and exactW+exactG<exactO:
            print('EXACT COUNTEREXAMPLE',flush=True)
            break
(OUT/'tax_cone_report.json').write_text(json.dumps({'seed':40051,'trials':len(records),'seconds':time.time()-started,'best_minimum_slack':best,'records':records},indent=2))
print('DONE',it+1,time.time()-started,flush=True)
