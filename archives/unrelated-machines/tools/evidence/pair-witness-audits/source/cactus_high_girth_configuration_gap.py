"""Exact cactus replacement of the VW two-tree configuration gap.

Self-contained finite configuration-gap generator; no hardness claim.  This is not a generic
configuration-LP solver.  Every certificate entry is checked using Fraction.
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as F
from itertools import product
import argparse
import hashlib
import json


def height(k):
    if type(k) is not int or k < 2:
        raise ValueError('k must be an integer at least two')
    a, h = F(1, k - 1), 1
    while a < F(1, 2):
        a *= F(k, k - 1)
        h += 1
    return h, a


def build(k, girth=3):
    if type(girth) is not int or girth < 3:
        raise ValueError('girth must be an integer at least three')
    h, alpha = height(k)
    machines, jobs, config = [], [], defaultdict(lambda: defaultdict(F))
    tree_nodes, path = [], []

    def machine(label):
        z = len(machines)
        machines.append(label)
        return z

    def job(label, u, a, v, b):
        z = len(jobs)
        jobs.append((label, ((u, F(a)), (v, F(b)))))
        return z

    roots = [machine(f"root_{side}") for side in range(2)]
    bridge = job("root_bridge", roots[0], 1, roots[1], 1)
    witness = {bridge: roots[0]}
    for side in range(2):
        def subtree(v, incoming, level, on_path):
            if level == h - 1:
                d = k - 1
                low = []
                for r in range(d):
                    inside = [machine(f"cycle_{side}_{v}_{r}_{t}") for t in range(girth-1)]
                    a = job(f"cycle_{side}_{v}_{r}_first", v, F(1,k), inside[0], 1)
                    chain = [job(f"cycle_{side}_{v}_{r}_path_{t}",inside[t],1,inside[t+1],1)
                             for t in range(girth-2)]
                    b = job(f"cycle_{side}_{v}_{r}_last", v, F(1,k), inside[-1], 1)
                    low.extend((a,b))
                    cycle_edges = [a]+chain+[b]
                    for t,u in enumerate(inside):
                        config[u][(cycle_edges[t],)] += F(1,2)
                        config[u][(cycle_edges[t+1],)] += F(1,2)
                    witness[a] = v
                    witness[b] = inside[-1]
                    for t,c in enumerate(chain):witness[c] = inside[t]
                a1 = F(1,d)
                for r in range(2*d):
                    config[v][tuple(sorted((incoming,low[r])))] += a1/F(2*d)
                    cyc = tuple(sorted(low[(r+t)%(2*d)] for t in range(k)))
                    config[v][cyc] += (1-a1)/F(2*d)
                return a1
            outgoing = []
            children = []
            for r in range(k):
                u = machine(f"tree_{side}_{v}_{r}")
                e = job(f"tree_{side}_{v}_{r}_edge", v, F(1,k), u, 1)
                outgoing.append(e)
                children.append((u,e))
                witness[e] = u if on_path and r == 0 else v
            child_alpha = None
            for r,(u,e) in enumerate(children):
                z = subtree(u,e,level+1,on_path and r == 0)
                assert child_alpha in (None,z)
                child_alpha = z
            for e in outgoing:
                config[v][tuple(sorted((incoming,e)))] += child_alpha/F(k-1)
            config[v][tuple(sorted(outgoing))] += 1-F(k)*child_alpha/F(k-1)
            return F(k)*child_alpha/F(k-1)
        z = subtree(roots[side],bridge,0,side == 0)
        assert z == alpha
    # Thin the root bridge independently without changing any other marginal.
    for r in roots:
        old = dict(config[r]); config[r].clear()
        thin = F(1,2)/alpha
        for C,w in old.items():
            if bridge in C:
                config[r][C] += w*thin
                config[r][tuple(j for j in C if j != bridge)] += w*(1-thin)
            else:
                config[r][C] += w
    clean = {i:{C:w for C,w in row.items() if w} for i,row in config.items()}
    return {"k":k,"girth":girth,"height":h,"machines":machines,"jobs":jobs,
            "certificate":clean,"witness":witness,
            "T":F(k+1,k),"theta":F(2*k-1,k)}


def check(data):
    k = data["k"]
    p = {(i,j):a for j,(_,opts) in enumerate(data["jobs"]) for i,a in opts}
    cover = [F(0)]*len(data["jobs"])
    count = 0
    for i in range(len(data["machines"])):
        row = data["certificate"][i]
        assert sum(row.values(),F(0)) == 1
        for C,w in row.items():
            assert w > 0 and len(C) == len(set(C))
            assert all((i,j) in p for j in C)
            assert sum((p[i,j] for j in C),F(0)) <= data["T"]
            for j in C: cover[j] += w
            count += 1
    assert set(cover) == {F(1)}
    assert set(data["witness"]) == set(range(len(cover)))
    loads = [F(0)]*len(data["machines"])
    for j,i in data["witness"].items():loads[i] += p[i,j]
    assert max(loads,default=F(0)) == data["theta"]
    return {"k":k,"girth":data["girth"],"height":data["height"],"machines":len(loads),
            "jobs":len(cover),"nonzero_configurations":count,
            "T":str(data["T"]),"witness_makespan":str(max(loads)),
            "claimed_lower_bound":str(data["theta"]),
            "ratio_to_certificate_T":str(data["theta"]/data["T"])}


def brute_opt(data):
    jobs, m = data["jobs"], len(data["machines"])
    best = None
    for bits in product((0,1),repeat=len(jobs)):
        loads = [F(0)]*m
        for (_,opts),b in zip(jobs,bits):
            i,p = opts[b];loads[i] += p
        C = max(loads,default=F(0))
        if best is None or C < best:best = C
    assert best == data["theta"]
    return str(best)


def encoded_certificate(data):
    return {"family":"cactus_high_girth_two_tree_configuration_gap","version":1,
      "k":data["k"],"girth":data["girth"],"height":data["height"],"T":str(data["T"]),
      "theta":str(data["theta"]),"machines":data["machines"],
      "jobs":[{"id":j,"name":name,"options":[[i,str(p)] for i,p in opts]}
              for j,(name,opts) in enumerate(data["jobs"])],
      "configurations":[{"machine":i,"jobs":list(C),"weight":str(w)}
                        for i,row in data["certificate"].items()
                        for C,w in sorted(row.items())],
      "schedule":[data["witness"][j] for j in range(len(data["jobs"]))]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output")
    ap.add_argument("--certificate-k",type=int)
    ap.add_argument("--girth",type=int,default=3)
    args = ap.parse_args()
    if args.certificate_k is not None:
        data=build(args.certificate_k,args.girth);check(data)
        result=encoded_certificate(data)
    else:
        result={"scope":"exact finite evidence, not the all-k proof","families":[]}
        for k,g in ((2,3),(3,3),(2,4),(2,7),(4,3),(4,7)):
            data=build(k,g);row=check(data)
            if k <= 3:row["exhaustive_optimum"]=brute_opt(data)
            result["families"].append(row)
        # Symbolically supplied recurrence and identities, checked exactly over
        # a finite parameter range without expanding exponentially large trees.
        for k in range(2,257):
            d=k-1;a=F(1,d)
            assert (a+(1-a)*k)/F(2*d) == F(1,2)
            h,z=height(k)
            assert z >= F(1,2)
            if h>1:assert z/F(k,k-1) < F(1,2)
            assert F(2*k-1,k)/F(k+1,k) == 2-F(3,k+1)
        result["finite_formula_parameters"]={"k_min":2,"k_max":256}
    text=json.dumps(result,ensure_ascii=False,indent=2)+"\n"
    if args.output:
        with open(args.output,"x") as f:f.write(text)
    else:print(text,end="")


if __name__ == "__main__":main()
