"""Finite exact diagnosis of welfare-minimum tail threshold selections.

The complete-history solver is canonical. This script neither restricts policies
nor proves any assertion outside each enumerated finite instance.
"""
from fractions import Fraction
from pathlib import Path
from itertools import product
import argparse,json,random,sys,time
from customer_attraction import Instance,CustomerType,ExactSPESolver

ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).parent

def diagnose(inst):
    sol=ExactSPESolver(inst)
    worst=sol.worst_outcomes();w=sol.minimum_welfare();m=inst.players
    kappa=Fraction(1) if m==2 else Fraction(m+1,2*(m-1))
    last=[];pair=[];n=0
    for c in worst:
        vals=inst.topic_payoffs(c)
        for h in sol.ordered_outcomes(c):
            n+=1
            e=(m-1)*vals[h[-1]]
            p=min(e,(m-kappa)*vals[h[-2]])
            last.append((e,h));pair.append((p,h))
    le,lh=min(last);pe,ph=min(pair)
    return {'welfare':w,'opt':inst.optimal_welfare(),'worst_paths':n,
            'last_best_cost':str(le),'last_slack':str(w-le),'last_path':lh,
            'pair_best_cost':str(pe),'pair_slack':str(w-pe),'pair_path':ph,
            'worst_counts':[list(c) for c in sorted(worst)]}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--random',type=int,default=0)
    ap.add_argument('--seed',type=int,default=324912)
    ap.add_argument('--output',required=True)
    args=ap.parse_args();records=[];rng=random.Random(args.seed)
    candidates=[]
    for p in sorted((ROOT/'examples/customer_attraction').glob('*.json')):
        try:i=Instance.from_dict(json.loads(p.read_text()))
        except (ValueError,KeyError,TypeError):continue
        if 2<=i.players<=6 and i.topic_count<=8:candidates.append((str(p.relative_to(ROOT)),i))
    for trial in range(args.random):
        m=rng.choice([3,4,5,6]);k=rng.choice([4,5,6,7])
        types=tuple(CustomerType(frozenset(a for a in range(k) if b>>a&1),rng.randint(1,20))
                    for b in range(1,1<<k) if rng.random()<.18)
        candidates.append(('random_'+str(trial),Instance(tuple(map(str,range(k))),types,m)))
    for name,inst in candidates:
        r=diagnose(inst);r['name']=name;records.append(r)
        print(json.dumps(r),flush=True)
        if Fraction(r['last_slack'])<0:r['instance']=inst.to_dict()
        if Fraction(r['pair_slack'])<0:
            print('PAIR CANDIDATE FAILURE',flush=True)
            r['instance']=inst.to_dict();break
    Path(args.output).write_text(json.dumps({'scope':'specified finite instances only; pure complete-history SPE outcome sets','parameters':vars(args),'records':records},indent=2)+'\n')
if __name__=='__main__':main()
