"""Counterexample test for a general candidate, never an exhaustive proof.

L_i is the minimum equilibrium current-mover payoff at any prefix of length
 i-1, allowing all SPE continuations. Test OPT_m <= 2*sum_i L_i.
ExactSPESolver thresholds use every successor's true optimality and all ties.
"""
from pathlib import Path
import json
import sys
from fractions import Fraction
ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction import Instance, ExactSPESolver


def composition(total, width):
    if width == 1:
        yield (total,)
    else:
        for head in range(total+1):
            for tail in composition(total-head,width-1):
                yield (head,)+tail


def check(path):
    instance = Instance.from_dict(json.loads(path.read_text()))
    solver = ExactSPESolver(instance)
    # Every count vector is a legal prefix; count states represent all ordered
    # histories' possible continuation sets, never a single count-only strategy.
    floors=[]
    witnesses=[]
    for depth in range(instance.players):
        pairs=[(solver.threshold(c),c) for c in composition(depth,instance.topic_count)]
        v,c=min(pairs)
        floors.append(v)
        witnesses.append(c)
    opt=instance.optimal_welfare()
    return dict(input=str(path.relative_to(ROOT)),players=instance.players,topics=instance.topic_count,
                opt=opt,depth_floors=list(map(str,floors)),floor_sum=str(sum(floors)),
                candidate_gap=str(2*sum(floors)-opt),prefix_witnesses=witnesses)

if __name__=='__main__':
    paths=[Path(x) if Path(x).is_absolute() else ROOT/x for x in sys.argv[1:]]
    if not paths:
        paths=[]
        for p in sorted((ROOT/'examples/customer_attraction').glob('*.json')):
            try:
                d=json.loads(p.read_text())
                if isinstance(d,dict) and {'players','topics','customers'}<=d.keys() and 1<=d['players']<=5 and len(d['topics'])<=7:
                    paths.append(p)
            except (ValueError,TypeError):
                pass
    records=[]
    for p in paths:
        r=check(p)
        records.append(r)
        print(json.dumps(r),flush=True)
    out=Path(__file__).with_name('depth_floor_checks.json')
    out.write_text(json.dumps({'candidate':'OPT_m <= 2 sum_i L_i','scope':'selected existing instances; rational exact tests, not universal proof','records':records},indent=2)+'\n')
