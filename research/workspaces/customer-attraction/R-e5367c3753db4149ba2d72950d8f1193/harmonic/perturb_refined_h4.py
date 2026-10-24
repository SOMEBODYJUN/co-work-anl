"""Targeted perturbation of one authenticated endpoint obstruction.

The original eight customer types and all 27,243 strategy-automaton states are
fixed. This tests the inferred H4 bridge, with all optimal A,B,T,P-containing
orders, against the full SPE cone of that single strategy. No new player count,
catalog family, or strategy is sampled. A cutting-plane LP proposes values;
exact row checks are required for any positive candidate.
"""
from pathlib import Path
from fractions import Fraction as F
import gzip
import json
import numpy as np
from scipy.optimize import linprog

ROOT=Path(__file__).resolve().parents[5]
SOURCE=ROOT/"research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_k10_packet.json.gz"

def main():
    data=json.loads(gzip.decompress(SOURCE.read_bytes()));inst=data["instance"]
    nodes=data["nodes"];m=inst["players"];p=len(inst["topics"])
    types=[frozenset(row["topics"]) for row in inst["customers"]];k=len(types)
    terminal={}
    for v in sorted(range(len(nodes)),key=lambda j:sum(nodes[j]["counts"]),reverse=True):
        n=nodes[v]
        terminal[v]=tuple(n["counts"]) if n.get("terminal") else terminal[n["children"][n["action"]]]
    def urow(a,q):return tuple(F(1,sum(q[b] for b in t)) if a in t else F(0) for t in types)
    rows=set()
    for v,n in enumerate(nodes):
        if n.get("terminal"):continue
        actual=urow(n["action"],terminal[v])
        for a,w in enumerate(n["children"]):
            dev=urow(a,terminal[w]);row=tuple(x-y for x,y in zip(actual,dev))
            if any(row):rows.add(row)
    rows=sorted(rows)
    v=data["root"];pathnodes=[]
    while not nodes[v].get("terminal"):
        pathnodes.append(v);v=nodes[v]["children"][nodes[v]["action"]]
    q=terminal[data["root"]];load=[sum(q[b] for b in t) for t in types]
    W=tuple(F(c>0) for c in load)
    e=[tuple(F(1,1+c) if a in t else F(0) for t,c in zip(types,load)) for a in range(p)]
    G=tuple(F(1,1+c) if c else F(0) for c in load)
    ds=[[urow(a,terminal[nodes[v]["children"][a]]) for a in range(p)] for v in pathnodes]
    costs=[[tuple(e[a][j]-ds[i][a][j] for j in range(k)) for a in range(p)] for i in range(m)]
    bit={0:1,1:2,2:4,5:8}
    def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
    def minimize(weights):
        states={0:(F(0),())}
        for crow in costs:
            new={}
            for mask,(value,order) in states.items():
                for a in range(p):
                    item=(value+dot(crow[a],weights),order+(a,));key=mask|bit.get(a,0)
                    if key not in new or item<new[key]:new[key]=item
            states=new
        return states[15]
    original=tuple(F(row["multiplicity"]) for row in inst["customers"])
    _,first=minimize(original)
    cuts=[];orders=[]
    def add(order):
        coeff=tuple(sum((costs[i][a][j] for i,a in enumerate(order)),F(0))-G[j] for j in range(k))
        cuts.append(tuple(-c for c in coeff)+(F(1),));orders.append(order)
    add(first)
    records=[];final=None
    for iteration in range(40):
        constraints=[tuple(-c for c in row)+(F(0),) for row in rows]+cuts
        res=linprog([0.]*k+[-1.],A_ub=np.array(constraints,float),b_ub=np.zeros(len(constraints)),
                    A_eq=np.array([W+(F(0),)],float),b_eq=[1.],bounds=[(0,None)]*k+[(None,None)],method="highs")
        if not res.success:
            records.append({"iteration":iteration,"status":res.message});break
        point=tuple(F(float(x)).limit_denominator(10**7) for x in res.x)
        exact=dot(W,point[:-1])==1 and all(dot(row,point)>=0 for row in [r+(F(0),) for r in rows])
        value,order=minimize(point[:-1]);true=value-dot(G,point[:-1])
        records.append({"iteration":iteration,"lp_bound_float":float(res.x[-1]),"exact_candidate_feasible":exact,
                        "exact_min_h4_debt":str(true),"new_order":list(order)})
        if true>=point[-1]-F(1,10**7) or order in orders:
            final={"values":list(map(str,point[:-1])),"minimum_debt_minus_G":str(true),
                   "candidate_exact_spe_feasible":exact,"positive_h4_failure":exact and true>0,
                   "best_order":list(order)}
            break
        add(order)
    result={"status":"candidate-specific finite LP diagnostic; no universal theorem",
            "endpoint_definition":"inferred harmonic q=c", "fixed_automaton_nodes":len(nodes),
            "distinct_exact_spe_rows":len(rows),"iterations":records,"final":final}
    out=Path(__file__).with_name("perturb_refined_h4.json");out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__=="__main__":main()
