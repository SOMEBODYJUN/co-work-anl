"""Exact finite witness requested by root; independent full ordered-tree audit."""
from fractions import Fraction
from itertools import product
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT))
from customer_attraction import Instance,ExactSPESolver,verify_certificate,StrategyCertificate
COVERAGE=({0,1},{2,3},{0,2},{1,3})
PATH=(2,3,0,1)
OUT=Path(__file__).resolve().parent

def audit(actions):
    expected={h for n in range(4) for h in product(range(4),repeat=n)}
    assert set(actions)==expected
    comparisons=0;strict=0
    def pay(path,owner):
        return sum((Fraction(1,sum(x in COVERAGE[a] for a in path))
                    for x in COVERAGE[owner]),Fraction())
    def terminal(h):
        nonlocal comparisons,strict
        if len(h)==4:return h
        branches=[terminal(h+(a,)) for a in range(4)]
        a=actions[h];actual=pay(branches[a],a)
        for b in range(4):
            comparisons+=1
            alternative=pay(branches[b],b)
            assert actual>=alternative,(h,a,b,actual,alternative)
            strict+=int(actual>alternative)
        return branches[a]
    path=terminal(())
    return {"path":list(path),"histories":len(expected),"comparisons_including_own":comparisons,
            "strict_comparisons":strict,"unit_customer_payoffs":[str(pay(path,a)) for a in path]}

def main():
    instance=Instance.from_topic_sets(COVERAGE,players=4,labels=("A","B","C","D"))
    solver=ExactSPESolver(instance)
    certificate=solver.certificate(on_path=PATH)
    normative=verify_certificate(instance,certificate);normative.assert_valid()
    independent=audit(certificate.actions)
    assert tuple(independent['path'])==PATH
    prefix_load=[sum(x in COVERAGE[a] for a in PATH[:2]) for x in range(4)]
    assert prefix_load==[1,1,1,1]
    result={"identity":"finite nonempty-class witness; no new general bound",
            "instance":instance.to_dict(),"certificate":certificate.to_dict(),
            "independent_audit":independent,"prefix_customer_load":prefix_load,
            "alpha":1,"beta":1,"normative_deviations":normative.checked_deviations,
            "W":instance.welfare(certificate.terminal_counts),"OPT":instance.optimal_welfare(),
            "root_outcomes":[list(q) for q in sorted(solver.outcomes())]}
    (OUT/'load_dominance_witness.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('certificate','root_outcomes','instance')},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
