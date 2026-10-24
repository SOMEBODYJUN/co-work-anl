"""Standalone exact audit of frozen source plans; no solver or LP imports."""
from fractions import Fraction as F
from itertools import combinations, product
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent


def audit(path):
    obj=json.loads(path.read_text())
    inst=obj["instance"]
    p=len(inst["topics"])
    m=inst["players"]
    clients=[(set(c["topics"]),c["multiplicity"]) for c in inst["customers"]]
    actions={tuple(h):a for h,a in obj["actions"]}
    expected={h for d in range(m) for h in product(range(p),repeat=d)}
    assert set(actions)==expected
    assert all(a in range(p) for a in actions.values())
    signatures=[frozenset(i for i,(topics,_) in enumerate(clients) if a in topics)
                for a in range(p)]
    assert len(set(signatures))==p

    def leaf(h):
        while len(h)<m:
            h=h+(actions[h],)
        return h

    def utility(a,z):
        return sum((F(w,sum(b in topics for b in z))
                    for topics,w in clients if a in topics),F(0))

    rows=0
    for h,a in actions.items():
        if not h:
            continue
        actual=utility(a,leaf(h))
        for b in range(p):
            assert actual>=utility(b,leaf(h+(b,))),(path,h,a,b)
            rows+=1
    actual=leaf(())
    assert list(actual)==obj["actual"]
    root_u=[utility(a,leaf((a,))) for a in range(p)]
    u=root_u[actions[()]]
    delta=max(root_u)-u
    assert list(map(str,root_u))==obj["root_deviation_payoffs"]
    assert str(u)==obj["actual_root_payoff"]
    assert str(delta)==obj["root_regret"]
    def coverage(support):
        return sum(w for topics,w in clients if topics.intersection(support))
    W=coverage(set(actual))
    opt=max(coverage(set(s)) for s in combinations(range(p),min(m,p)))
    assert W==obj["W"] and opt==obj["OPT_m"]
    return {"file":path.name,"players":m,"topics":p,
            "ordered_histories":len(actions),"positive_depth_IC_rows":rows,
            "W":W,"OPT_m":opt,"root_regret":str(delta),
            "exact_source_repair_margin":str(F(opt-2*W)-3*delta)}


if __name__=="__main__":
    report={"contract":"all ordered positive-depth IC and all root deviations checked with Fraction",
            "scope":"These are root-only source plans, not a claim that their root is optimal.",
            "sources":[audit(path) for path in sorted(HERE.glob("seed_source_*.json"))]}
    (HERE/"frozen_sources_exact_audit.json").write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))
