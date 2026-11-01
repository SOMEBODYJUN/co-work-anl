#!/usr/bin/env python3
"""Definition-level exact audit of low-tail deletion, with no SPE solver.

Reads an existing finite full-history strategy automaton, independently checks
its closure and every real deviation, and then computes the new deletion data.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
from math import lcm
import gzip
import json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
SOURCE=ROOT/"research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_k10_packet.json.gz"
d=json.loads(gzip.decompress(SOURCE.read_bytes()))
nodes=d["nodes"]; root=d["root"]; ins=d["instance"]
p=len(ins["topics"]); m=ins["players"]
customers=tuple(frozenset(row["topics"]) for row in ins["customers"]
                for _ in range(row["multiplicity"]))
assert len(customers)==36 and m==13 and p==6
den=lcm(*range(1,m+1))

@lru_cache(None)
def scaled_payoff(counts,topic):
    return sum(den//sum(counts[t] for t in s) for s in customers if topic in s)

assert nodes[root]["counts"]==[0]*p
seen=set(); todo=[root]
while todo:
    i=todo.pop()
    if i in seen:
        continue
    seen.add(i); v=nodes[i]; c=tuple(v["counts"]); depth=sum(c)
    assert len(c)==p and all(isinstance(x,int) and x>=0 for x in c)
    assert depth<=m
    if depth==m:
        assert not v.get("children")
    else:
        assert len(v["children"])==p and 0<=v["action"]<p
        for t,j in enumerate(v["children"]):
            assert isinstance(j,int) and 0<=j<len(nodes)
            expected=tuple(x+int(k==t) for k,x in enumerate(c))
            assert tuple(nodes[j]["counts"])==expected
            todo.append(j)
assert len(seen)==len(nodes)

final={}; suffix={}; comparisons=0; least=None
for i in sorted(range(len(nodes)),key=lambda i:sum(nodes[i]["counts"]),reverse=True):
    v=nodes[i]; depth=sum(v["counts"])
    if depth==m:
        final[i]=tuple(v["counts"]); suffix[i]=()
        continue
    chosen=v["action"]; child=v["children"][chosen]
    final[i]=final[child]; suffix[i]=(chosen,)+suffix[child]
    actual=scaled_payoff(final[i],chosen)
    for t,j in enumerate(v["children"]):
        slack=actual-scaled_payoff(final[j],t)
        assert slack>=0,(i,t,slack)
        comparisons+=1
        least=slack if least is None else min(least,slack)

z=suffix[root]
assert z==(5,)*10+(0,0,1)
assert final[root]==(2,1,0,0,0,10)
branch_data=[]
for a,j in enumerate(nodes[root]["children"]):
    q=final[j]
    pay=tuple(F(scaled_payoff(q,t),den) for t in (a,)+suffix[j])
    assert pay[0]==F(5,2)
    assert sum(pay[1:])>=F(61,2)
    branch_data.append({"root_topic":ins["topics"][a],"path":[a,*suffix[j]],
                        "root_payoff":str(pay[0]),"tail_profit":str(sum(pay[1:])),
                        "tail_minimum":str(min(pay[1:]))})

def deletion(epsilon):
    t=F(5,2)+epsilon
    q=final[root]
    actual=tuple(F(scaled_payoff(q,a),den) for a in z)
    low=tuple(i for i in range(1,m) if actual[i]<t)
    kept=tuple(a for i,a in enumerate(z) if i not in low)
    cq=tuple(kept.count(a) for a in range(p))
    # The root remains, so every root customer denominator is positive.
    after=sum((F(1,sum(cq[t] for t in s)) for s in customers if z[0] in s),F())
    before=actual[0]
    gain=after-before
    deficit=sum((t-actual[i] for i in low),F())
    assert low==tuple(range(1,12))
    assert gain==F(45,2) and deficit==11*epsilon
    assert all(F(row["tail_profit"])>=(m-1)*t for row in branch_data)
    return {"epsilon":str(epsilon),"threshold":str(t),"low_tail_positions_zero_based":low,
            "deleted_topics":[ins["topics"][z[i]] for i in low],
            "root_before":str(before),"root_after":str(after),"root_deletion_gain":str(gain),
            "total_low_tail_deficit":str(deficit),"gain_over_deficit":str(gain/deficit)}

report={"identity":"low-tail deficit cannot bound actual root dilution",
        "source":str(SOURCE.relative_to(ROOT)),"method":"expanded 36 unit customers; closed full-history DAG; exact integer payoffs",
        "nodes":len(nodes),"checked_comparisons_including_self":comparisons,
        "minimum_SPE_slack":str(F(least,den)),"root_branches":branch_data,
        "deletion_cases":[deletion(F(1,24)),deletion(F(1,1000)),deletion(F(1,1000000))],
        "universal_argument":"for arbitrary fixed K>=0 choose 0<epsilon<=1/24 with 11*K*epsilon<45/2",
        "main_half_and_background_gap":"not refuted; at root F13-P=3 and 13*min_u=65/2"}
(HERE/"low_tail_deletion_exact.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2))
