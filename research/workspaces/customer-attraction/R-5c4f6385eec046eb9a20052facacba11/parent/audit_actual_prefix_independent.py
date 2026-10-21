"""Independent literal unit-client audit of a supplied full four-player tree.

No imports from the finder, Instance, ExactSPESolver, or canonical verifier.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib
import json


def main():
    base=Path(__file__).resolve().parents[1]
    source=base/'background/global_actual_prefix_complete_spe.json'
    raw=source.read_bytes(); obj=json.loads(raw)
    strategy={tuple(row['history']):row['action'] for row in obj['actions']}
    expected={h for length in range(4) for h in product(range(6),repeat=length)}
    assert set(strategy)==expected and len(strategy)==len(obj['actions'])==259
    assert all(type(v) is int and 0<=v<6 for v in strategy.values())
    groups=[({0},10),({1},12),({2},5),({3},5),({2,4},2),({3,4},2),
            ({2,5},2),({3,5},2),({0,4,5},6),({1,4,5},6)]
    clients=[membership for membership,n in groups for _ in range(n)]
    assert len(clients)==52
    def follow(h):
        while len(h)<4: h=h+(strategy[h],)
        return h
    def utility(a,path):
        return sum((Fraction(1,sum(t in member for t in path)) for member in clients if a in member),Fraction(0))
    checked=0;slacks=[]
    for h in sorted(expected,key=lambda t:(len(t),t)):
        chosen=strategy[h]; realized=follow(h+(chosen,)); u=utility(chosen,realized)
        for alternative in range(6):
            terminal=follow(h+(alternative,)); other=utility(alternative,terminal)
            assert u>=other,(h,chosen,alternative,u,other)
            slacks.append(u-other);checked+=1
    path=follow(());assert path==(0,1,0,1)
    profits=[utility(a,path) for a in path];assert profits==[8,9,8,9]
    covered=lambda p:{i for i,member in enumerate(clients) if any(a in member for a in p)}
    actual=covered(path);prefix=covered(path[:2]);fresh=set(range(52))-prefix
    delta=len(covered(path[2:])&fresh);assert delta==0
    opt4=max(len(covered(p)) for p in product(range(6),repeat=4))
    freshopt2=max(len(covered(p)&fresh) for p in product(range(6),repeat=2))
    assert len(actual)==34 and opt4==52 and freshopt2==18
    assert sum(profits[2:])+delta==17<freshopt2
    report={'certificate_sha256':hashlib.sha256(raw).hexdigest(),'nodes':len(expected),
            'comparisons_including_self':checked,'minimum_slack':str(min(slacks)),
            'actual_path':path,'actual_profits':[str(v) for v in profits],
            'root_W':len(actual),'root_OPT4':opt4,'tail_P':str(sum(profits[2:])),
            'tail_delta':delta,'tail_freshOPT2':freshopt2,'all_assertions_passed':True}
    out=Path(__file__).with_name('actual_prefix_independent_audit.json')
    out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))


if __name__=='__main__': main()
