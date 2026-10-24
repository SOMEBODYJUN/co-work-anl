"""Definition-level audit of inferred H4 on the old thirteen-player packet.

No solver, discovery code, desired-terminal field or cached expected path is
used. A 16-state dynamic program minimizes endpoint debt over every optimal
tuple and every order: an optimum here is exactly a sequence containing all of
A,B,T,P. This finite audit is not a universal H4 result.
"""
from pathlib import Path
from fractions import Fraction as F
from functools import lru_cache
from math import lcm
import gzip
import json

ROOT=Path(__file__).resolve().parents[5]
SOURCE=ROOT/"research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_k10_packet.json.gz"

def audit():
    data=json.loads(gzip.decompress(SOURCE.read_bytes()))
    inst=data["instance"];m=inst["players"];p=len(inst["topics"])
    nodes=data["nodes"];root=data["root"]
    units=[frozenset(row["topics"]) for row in inst["customers"]
           for _ in range(row["multiplicity"])]
    L=lcm(*range(1,m+1))
    reached=set();stack=[root]
    while stack:
        v=stack.pop()
        if v in reached:continue
        reached.add(v);node=nodes[v];q=tuple(node["counts"])
        assert len(q)==p and min(q)>=0 and sum(q)<=m
        if node.get("terminal"):
            assert sum(q)==m and "children" not in node
        else:
            assert len(node["children"])==p and sum(q)<m
            for a,w in enumerate(node["children"]):
                assert tuple(nodes[w]["counts"])==tuple(n+int(j==a) for j,n in enumerate(q))
                stack.append(w)
    assert reached==set(range(len(nodes))) and tuple(nodes[root]["counts"])==(0,)*p
    @lru_cache(None)
    def utility(a,q):
        return sum(L//sum(q[b] for b in u) for u in units if a in u)
    terminal={};comparisons=0;min_gap=None
    for v in sorted(reached,key=lambda j:sum(nodes[j]["counts"]),reverse=True):
        node=nodes[v]
        if node.get("terminal"):
            terminal[v]=tuple(node["counts"]);continue
        a=node["action"];terminal[v]=terminal[node["children"][a]]
        for b,w in enumerate(node["children"]):
            gap=utility(a,terminal[v])-utility(b,terminal[w])
            assert gap>=0
            min_gap=gap if min_gap is None else min(min_gap,gap)
            comparisons+=1
    path=[];pathnodes=[];v=root
    while not nodes[v].get("terminal"):
        pathnodes.append(v);a=nodes[v]["action"];path.append(a);v=nodes[v]["children"][a]
    q=terminal[root];loads=[sum(q[b] for b in u) for u in units]
    W=sum(c>0 for c in loads)
    d=[[F(utility(a,terminal[nodes[v]["children"][a]]),L) for a in range(p)] for v in pathnodes]
    # Singleton-private customer classes force all four labels in every optimum.
    mandatory=tuple(a for a in range(p) if any(u=={a} for u in units))
    assert mandatory==(0,1,2,5)
    assert all(any(a in u for a in mandatory) for u in units)
    bit={a:1<<j for j,a in enumerate(mandatory)};allbits=(1<<len(mandatory))-1
    results=[]
    for alpha in (F(1),F(m-1,m)):
        e=[sum((1/(1+alpha*c) for u,c in zip(units,loads) if a in u),F(0)) for a in range(p)]
        G=sum((1/(1+alpha*c) for c in loads if c),F(0))
        states={0:(F(0),())}
        for row in d:
            new={}
            for mask,(value,order) in states.items():
                for a in range(p):
                    key=mask|bit.get(a,0);item=(value+e[a]-row[a],order+(a,))
                    if key not in new or item<new[key]:new[key]=item
            states=new
        debt,order=states[allbits]
        ep=sum((e[a] for a in order),F(0));true=sum((d[i][a] for i,a in enumerate(order)),F(0))
        assert ep-true==debt and all(a in order for a in mandatory)
        results.append({"alpha":str(alpha),"e":list(map(str,e)),"G":str(G),
                        "optimal_order":list(order),"endpoint_sum":str(ep),"true_deviation_sum":str(true),
                        "min_total_delta":str(debt),"h4_slack_G_minus_delta":str(G-debt),
                        "H4_holds_for_some_optimum":debt<=G})
    return {"status":"PASS", "definition_status":"inferred H4; alpha=1 is harmonic endpoint, alpha=(m-1)/m is old fractional endpoint",
            "scope":"fixed old complete SPE packet, all optimal tuples and all orders via exact DP",
            "automaton_nodes":len(nodes),"full_spe_comparisons":comparisons,"minimum_spe_gap":str(F(min_gap,L)),
            "actual_path":path,"W":W,"OPT":len(units),"mandatory_optimal_labels":list(mandatory),
            "true_actual_prefix_deviation_rows":[list(map(str,row)) for row in d],"results":results}

if __name__=="__main__":
    result=audit();out=Path(__file__).with_name("audit_h4_refined_packet.json")
    out.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
