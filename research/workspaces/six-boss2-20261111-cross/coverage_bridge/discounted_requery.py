#!/usr/bin/env python3
"""Exact two-state projection of a discounted true same-source requery orbit.

Reads a necessary-row point, never treats it as a complete SPE.  LPs only
discover nonnegative multipliers.  Every retained cut is rebuilt with Fraction
on the entire 64 actual-mask x 7 comparison-multiplicity domain.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

NAMES = ["source", "alpha_mid", "alpha_last", "beta_mid", "beta_last"]
NAMES += [f"mu_A{i+1}" for i in range(6)]
NAMES += ["mu_avg", "mu_seed", "mu_self"]
DIM = len(NAMES)


def share(a, b):
    return F(a, b) if a else F(0)


def features(bits, d, seedbit, source, t, c, s):
    p, ell = sum(bits[:source]), sum(bits[:5])
    z = p + t + s + c
    den = p + t + s + 1
    out = [share(t, z), F(s, ell + 1), F(c, ell + 1), F(s), F(c)]
    qs = list(map(F, bits)) + [F(d, 6), F(seedbit), F(t)]
    out.extend(q / den - share(c, z) for q in qs)
    assert len(out) == DIM
    return out


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def edge_costs(bits, d, seedbit, source, params):
    k = 6 - source
    return {(t, c): min(dot(features(bits, d, seedbit, source, t, c, s), params)
                         for s in range(k-1))
            for t in (0, 1) for c in (0, 1)}


def closed_values(e, theta):
    e00, e01, e10, e11 = (e[0,0], e[0,1], e[1,0], e[1,1])
    return (
        min(e00, (1-theta)*e01+theta*e11, (e01+theta*e10)/(1+theta)),
        min(e11, (1-theta)*e10+theta*e00, (e10+theta*e01)/(1+theta)),
    )


def projection(bits, d, seedbit, source, params, theta, verify=True):
    e = edge_costs(bits, d, seedbit, source, params)
    psi = closed_values(e, theta)
    if verify:
        v = tuple(z/(1-theta) for z in psi)
        for t in (0, 1):
            residuals = [e[t,c]+theta*v[c]-v[t] for c in (0,1)]
            assert min(residuals) == 0, (bits,d,seedbit,source,params,theta,e,psi,residuals)
    return psi[seedbit]


def seed_components(bits, d, seed):
    if seed == "avg":
        return [(0, F(6-d,6)), (1,F(d,6))]
    return [(bits[int(seed[1:])-1], F(1))]


def visible_projection(bits, d, seed, source, params, theta):
    return sum((w*projection(bits,d,t,source,params,theta)
                for t,w in seed_components(bits,d,seed) if w), F(0))


def read_point(path):
    data = json.loads(Path(path).read_text())
    cols = data["columns"]
    K = sum((F(c["weight"]) for c in cols if c.get("kind") == "K"), F(0))
    hist = {}
    for c in cols:
        if c.get("kind") != "hist":
            continue
        mass = F(c["weight"])
        if not mass:
            continue
        bits = tuple(map(int, c["actual_bits"]))
        key = (bits, c["d"])
        hist[key] = hist.get(key,F(0)) + mass
    u = [sum((w*share(bits[i],sum(bits)) for (bits,d),w in hist.items()),F(0))
         for i in range(6)]
    return data,K,hist,u


def budget_coefficients(source, K, u):
    k=6-source
    return [u[source],(k-2)*u[5],u[5],(k-2)*K,K] + [F(0)]*(DIM-5)


def solve_one(hist,K,u,source,seed,theta):
    states=[]
    for (bits,d),mass in sorted(hist.items()):
        for t0,freq in seed_components(bits,d,seed):
            if freq:
                states.append((bits,d,t0,mass*freq))
    nvar=DIM+2*len(states)
    objective=np.zeros(nvar)
    objective[:DIM]=list(map(float,budget_coefficients(source,K,u)))
    rows=[]
    rhs=[]
    k=6-source
    for q,(bits,d,t0,mass) in enumerate(states):
        objective[DIM+2*q+t0]=-(1-float(theta))*float(mass)
        for t,c,s in itertools.product((0,1),(0,1),range(k-1)):
            row=np.zeros(nvar)
            row[:DIM]=-np.array(list(map(float,features(bits,d,t0,source,t,c,s))))
            row[DIM+2*q+t]+=1
            row[DIM+2*q+c]-=float(theta)
            rows.append(row)
            rhs.append(0)
    eq=np.zeros((1,nvar));eq[0,:DIM]=1
    bounds=[(0,None)]*DIM+[(None,None)]*(nvar-DIM)
    if k==2:
        bounds[1]=bounds[3]=(0,0)
    res=linprog(objective,A_ub=np.array(rows),b_ub=np.array(rhs),
                A_eq=eq,b_eq=[1],bounds=bounds,method="highs")
    if not res.success:
        return {"source":source+1,"seed":seed,"theta":str(theta),"success":False,"message":res.message}
    params=[F(float(x)).limit_denominator(1000000) if x>1e-10 else F(0)
            for x in res.x[:DIM]]
    normal=sum(params,F(0));params=[x/normal for x in params]
    budget=dot(params,budget_coefficients(source,K,u))
    credit=sum((mass*visible_projection(bits,d,seed,source,params,theta)
                for (bits,d),mass in hist.items()),F(0))
    slack=budget-credit
    out={"source":source+1,"seed":seed,"theta":str(theta),"success":True,
         "float_objective":float(res.fun),"exact_slack":str(slack),
         "exact_slack_float":float(slack),
         "params":{name:str(v) for name,v in zip(NAMES,params) if v}}
    if slack<0:
        coeffs=[]
        for bits in itertools.product((0,1),repeat=6):
            c=sum(bits)
            for d in range(7):
                row= params[0]*share(bits[source],c)
                row+=((k-2)*params[1]+params[2])*share(bits[5],c)
                row-=visible_projection(bits,d,seed,source,params,theta)
                coeffs.append({"actual_bits":"".join(map(str,bits)),"d":d,"coefficient":str(row)})
        out["K_coefficient"]=str((k-2)*params[3]+params[4])
        out["visible_coefficients"]=coeffs
    return out


def local_audit():
    """Independent Bellman residual check on arbitrary rational edge costs."""
    counts=0
    for vals in itertools.product((F(-2),F(-1,3),F(0),F(1,2),F(3)),repeat=4):
        e=dict(zip(((0,0),(0,1),(1,0),(1,1)),vals))
        for theta in (F(0),F(1,4),F(1,2),F(3,4),F(9,10),F(99,100)):
            psi=closed_values(e,theta)
            v=tuple(x/(1-theta) for x in psi)
            for t in (0,1):
                assert v[t] == min(e[t,c]+theta*v[c] for c in (0,1))
            counts+=1
    return {"arbitrary_edge_bellman_cases":counts,"all_exact":True}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--thetas",default="0,1/4,1/2,3/4,9/10,99/100")
    ap.add_argument("--sources",default="1,2,3,4,5")
    ap.add_argument("--seeds",default="A1,A2,A3,A4,A5,A6,avg")
    args=ap.parse_args()
    _,K,hist,u=read_point(args.input)
    audit=local_audit()
    results=[]
    for source in [int(x)-1 for x in args.sources.split(",")]:
        for seed in args.seeds.split(","):
            for theta in map(F,args.thetas.split(",")):
                assert 0<=theta<1
                r=solve_one(hist,K,u,source,seed,theta)
                results.append(r)
                if r.get("exact_slack_float",0)<-1e-10:
                    print("CUT",source+1,seed,theta,r["exact_slack_float"],flush=True)
        print("SOURCE",source+1,"complete",flush=True)
    negative=[x for x in results if F(x.get("exact_slack","0"))<0]
    report={"scope":"finite parameter-grid LP discovery; exact full-domain valid local rows; input not SPE",
            "input":args.input,"input_sha256":hashlib.sha256(Path(args.input).read_bytes()).hexdigest(),
            "K":str(K),"actual_u":list(map(str,u)),"positive_visible_types":len(hist),
            "audit":audit,"parameter_names":NAMES,"cases":len(results),"negative_cases":len(negative),
            "minimum_exact_slack":str(min(F(x.get("exact_slack","0")) for x in results)),
            "results":results}
    Path(args.output).write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({key:report[key] for key in ("cases","negative_cases","minimum_exact_slack")}),flush=True)


if __name__=="__main__":
    main()
