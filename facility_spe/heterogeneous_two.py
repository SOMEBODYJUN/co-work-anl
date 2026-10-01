#!/usr/bin/env python3
"""Exact-rational pure-client factor-2 SPE for arbitrary two-facility catalogs.

The default uses four guarded seeds: all-on-one and the largest shared customer
alone, in both orientations. --all-singletons retains the larger audit menu.
Input format is the same as cross_one.py; no local m oracle is called.
"""
from fractions import Fraction as Q
import argparse
import json


from facility_spe.local.pure import load_pair, is_ne, guarded_repair


def make_menu(weights,sites,s,t,maximum_only=True):
    common=sorted(sites[s]&sites[t])
    ws=[weights[i] for i in common]
    a=sum((weights[i] for i in sites[s]-sites[t]),Q(0))
    b=sum((weights[i] for i in sites[t]-sites[s]),Q(0))
    seeds=[]
    designated=(range(len(ws)) if not maximum_only else
                ([max(range(len(ws)),key=lambda i:(ws[i],-common[i]))] if ws else []))
    for side in (0,1):
        seeds.append((side,)*len(ws))
        for h in designated:
            p=[1-side]*len(ws)
            p[h]=side
            seeds.append(tuple(p))
    menu={}
    for seed in seeds:
        p=guarded_repair(a,b,ws,seed)
        if p is not None:
            menu.setdefault(p,load_pair(a,b,ws,p))
    assert menu
    return {"common":common,"A":a,"B":b,"weights":ws,
            "entries":[{"prob_first":list(p),"loads":list(loads)}
                       for p,loads in menu.items()]}


def make_witness(s,t,data,entry):
    return {"layout":[s,t],"common":data["common"],
            "prob_first":entry["prob_first"],"loads":entry["loads"]}


def solve(instance,maximum_only=True):
    if any(isinstance(v,float) for v in instance["weights"]):
        raise TypeError("use exact rational strings or integers for weights")
    weights=[Q(str(v)) for v in instance["weights"]]
    if any(v<=0 for v in weights):
        raise ValueError("weights must be positive")
    sites=[set(v) for v in instance["locations"]]
    u1=list(dict.fromkeys(instance["U1"]));u2=list(dict.fromkeys(instance["U2"]))
    if not u1 or not u2:
        raise ValueError("both catalogs must be nonempty")
    menus={(s,t):make_menu(weights,sites,s,t,maximum_only=maximum_only) for s in u1 for t in u2}
    p1={pair:min(rec["entries"],key=lambda x:x["loads"][0]) for pair,rec in menus.items()}
    p2={pair:min(rec["entries"],key=lambda x:x["loads"][1]) for pair,rec in menus.items()}
    b1={t:max(u1,key=lambda s:p1[s,t]["loads"][0]) for t in u2}
    b2={s:max(u2,key=lambda t:p2[s,t]["loads"][1]) for s in u1}
    d1={t:p1[b1[t],t]["loads"][0] for t in u2}
    d2={s:p2[s,b2[s]]["loads"][1] for s in u1}
    node=(1,u1[0]);seen={};path=[]
    while node not in seen:
        seen[node]=len(path);path.append(node)
        color,site=node
        node=(2,b2[site]) if color==1 else (1,b1[site])
    cycle=path[seen[node]:]
    core1=[s for c,s in cycle if c==1]
    core2=[t for c,t in cycle if c==2]
    assert len(core1)==len(core2)
    best=None
    for s in core1:
        for t in core2:
            for entry in menus[s,t]["entries"]:
                x,y=entry["loads"]
                if (not x and d1[t]) or (not y and d2[s]):
                    continue
                alpha=max(Q(1),d1[t]/x if x else Q(0),d2[s]/y if y else Q(0))
                if best is None or alpha<best[0]:
                    best=(alpha,s,t,entry)
    assert best is not None and best[0]<=2,"R-menu closed-cycle construction failed"
    alpha,s,t,entry=best
    deviations=[]
    for r in u1:
        if r!=s:
            deviations.append({"deviator":1,"witness":make_witness(r,t,menus[r,t],p1[r,t])})
    for r in u2:
        if r!=t:
            deviations.append({"deviator":2,"witness":make_witness(s,r,menus[s,r],p2[s,r])})
    result={"finite_factor_exists":True,"alpha":alpha,"guarantee":2,
            "seed_mode":"maximum_only" if maximum_only else "all_singletons",
            "on_path":make_witness(s,t,menus[s,t],entry),"deviations":deviations,
            "response_cycle":[list(v) for v in cycle],
            "pair_count":len(menus),"menu_entry_count":sum(len(x["entries"]) for x in menus.values()),
            "default_continuation":"guarded_repair of the all-first seed at the requested layout"}
    verify(instance,result)
    return result


def verify(instance,result):
    """Direct exact certificate checks; never reads a menu or D value."""
    if any(isinstance(v,float) for v in instance["weights"]):
        raise TypeError("use exact rational strings or integers for weights")
    weights=[Q(str(v)) for v in instance["weights"]]
    sites=[set(v) for v in instance["locations"]]
    u1=set(instance["U1"]);u2=set(instance["U2"])
    if (not u1 or not u2 or any(w<=0 for w in weights)
            or any(type(i) is not int or not 0<=i<len(weights)
                   for site in sites for i in site)
            or any(type(s) is not int or not 0<=s<len(sites)
                   for s in u1|u2)):
        raise ValueError("invalid input instance")
    alpha=Q(str(result["alpha"]))
    if not 1<=alpha<=2:
        raise ValueError("claimed factor outside [1,2]")
    def check(rec):
        s,t=rec["layout"]
        if type(s) is not int or type(t) is not int or s not in u1 or t not in u2:
            raise ValueError("witness layout is outside the legal catalogs")
        common=sorted(sites[s]&sites[t]);p=rec["prob_first"]
        if common!=rec["common"] or len(common)!=len(p):
            raise ValueError("incorrect common-customer list or assignment length")
        if any(type(v) is not int or v not in (0,1) for v in p):
            raise ValueError("customer assignment is not pure")
        x=sum((weights[i] for i in sites[s]-sites[t]),Q(0))
        y=sum((weights[i] for i in sites[t]-sites[s]),Q(0))
        for i,z in zip(common,p):
            x+=weights[i]*z;y+=weights[i]*(1-z)
        if [x,y]!=[Q(str(z)) for z in rec["loads"]]:
            raise ValueError("incorrect facility loads")
        for i,z in zip(common,p):
            conditional_difference=x-y+weights[i]*(1-2*z)
            if not ((z==0 or conditional_difference<=0)
                    and (z==1 or conditional_difference>=0)):
                raise ValueError("customer assignment is not a Nash equilibrium")
        return x,y
    x,y=check(result["on_path"]);s,t=result["on_path"]["layout"]
    expected={(1,r,t) for r in u1 if r!=s}
    expected|={(2,s,r) for r in u2 if r!=t}
    observed=set()
    for rec in result["deviations"]:
        a,b=check(rec["witness"]);ds,dt=rec["witness"]["layout"]
        who=rec["deviator"]
        if type(who) is not int or who not in (1,2):
            raise ValueError("invalid deviating facility")
        key=(who,ds,dt)
        if key in observed:
            raise ValueError("duplicate deviation witness")
        observed.add(key)
        if (a if who==1 else b)>alpha*(x if who==1 else y):
            raise ValueError("facility deviation exceeds claimed factor")
    if expected!=observed:
        raise ValueError("missing or unrelated deviation witness")
    return True


def serial(value):
    if isinstance(value,Q):
        return str(value)
    if isinstance(value,list):
        return [serial(v) for v in value]
    if isinstance(value,dict):
        return {k:serial(v) for k,v in value.items()}
    return value


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--output")
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument("--all-singletons",action="store_false",dest="maximum_only",
                      help="use every designated shared customer (larger audit menu)")
    mode.add_argument("--maximum-only",action="store_true",dest="maximum_only",
                      help="use the default four seeds (compatibility option)")
    parser.set_defaults(maximum_only=True)
    args=parser.parse_args()
    with open(args.input) as stream:
        instance=json.load(stream,parse_float=str)
    rendered=json.dumps(serial(solve(instance,maximum_only=args.maximum_only)),ensure_ascii=False,indent=2)+"\n"
    if args.output:
        with open(args.output,"w") as stream:
            stream.write(rendered)
    else:
        print(rendered,end="")
