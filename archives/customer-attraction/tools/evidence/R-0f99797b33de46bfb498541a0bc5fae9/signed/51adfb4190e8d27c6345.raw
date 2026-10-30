"""Attack exactly the signed optimal-tuple B/Q candidate in fixed full SPE cones.

No finite negative result is a universal theorem. Positive results are retained
only after exact full-history and all-optimum-tuple checks.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement
import sys,json
import numpy as np
from scipy.optimize import linprog

ROOT=next(p for p in Path(__file__).resolve().parents if (p/'customer_attraction/__init__.py').exists())
sys.path[:0]=[str(ROOT),str(ROOT/'tests/audits')]
from customer_attraction_strategy_lp import StrategyCone,coverage_row,dot,integer_clones,instance_from_clones,independently_verify
from customer_attraction import Instance,StrategyCertificate,verify_certificate
HERE=Path(__file__).resolve().parent

def rows(cone,z,kind):
    row=[]
    for mask in range(1,1<<cone.topics):
        c=sum(cone.root[a] for a in range(cone.topics) if mask>>a&1)
        d=sum(mask>>a&1 for a in z)
        fee=F(d,c+1) if kind=='Q' else sum((F(1,c+t) for t in range(1,d+1)),F())
        row.append(fee-int(c>0)-int(c>0 and d==0))
    return tuple(row)

def sources():
    seen=set()
    for ep in sorted((ROOT/'examples/customer_attraction').glob('*.json')):
        cp=ROOT/'evidence/certificates/customer_attraction'/ep.name
        if not cp.exists():continue
        try:
            I=Instance.from_dict(json.loads(ep.read_text()))
            raw=json.loads(cp.read_text());raw=raw.get('strategy',raw)
            acts={tuple(x['history']):x['action'] for x in raw['actions']}
            if I.players>4 or I.topic_count>6 or I.players>I.topic_count:continue
            cone=StrategyCone(I.topic_count,I.players,acts)
            sig=(cone.topics,cone.players,tuple(sorted(cone.actions.items())))
            if sig not in seen:seen.add(sig);yield ep.name,cone
        except (KeyError,ValueError):pass
    ext=ROOT/'research/workspaces/customer-attraction/R-5d61c5324e744dc0a66133207fcbd010/exchange'
    for name in ('thirteen','strict_forty'):
        raw=json.loads((ext/f'{name}_m3_certificate.json').read_text());raw=raw.get('strategy',raw)
        cone=StrategyCone(4,3,{tuple(x['history']):x['action'] for x in raw['actions']})
        sig=(cone.topics,cone.players,tuple(sorted(cone.actions.items())))
        if sig not in seen:seen.add(sig);yield name,cone

def main():
    records=[]
    for name,cone in sources():
        k,m=cone.topics,cone.players
        supports=[z for r in range(1,m+1) for z in combinations(range(k),r)]
        cov={z:coverage_row(k,z) for z in supports}
        for J in supports:
            optrows=[tuple(a-b for a,b in zip(cov[J],cov[z])) for z in supports if z!=J]
            G=cone.rows+tuple(optrows)
            completions=[tuple(J)+(a,)*(m-len(J)) for a in J] if len(J)<m else [tuple(J)]
            for kind in ('B','Q'):
                objectives=[rows(cone,z,kind) for z in completions]
                # Maximize the minimum signed excess over all extremal completions.
                # The concavity lemma then excludes an untested helpful completion
                # on this same support, before the all-optimal-support check below.
                Aub=np.vstack([np.c_[-np.array(G,float),np.zeros(len(G))],np.array([[-float(x) for x in row]+[1] for row in objectives])])
                objective=np.zeros((1<<k));objective[-1]=-1
                r=linprog(objective,A_ub=Aub,b_ub=np.zeros(len(Aub)),A_eq=np.array([list(cone.welfare)+[0]],float),b_eq=[1],bounds=[(0,None)]*((1<<k)-1)+[(None,None)],method='highs')
                if not r.success:continue
                rec={'source':name,'actual':cone.root,'comparison_support':J,'extreme_completions':completions,'kind':kind,'max_min_signed_excess':float(-r.fun)}
                records.append(rec)
                if -r.fun<=1e-8:continue
                w=tuple(F(float(x)).limit_denominator(10**7) for x in r.x[:-1])
                if not cone.verify(w) or any(dot(row,w)<0 for row in optrows):continue
                best=max(dot(cov[z],w) for z in supports)
                opts=[z for z in combinations_with_replacement(range(k),m) if dot(coverage_row(k,set(z)),w)==best]
                gap=min(dot(rows(cone,z,kind),w) for z in opts)
                rec.update({'exact_gap_tested_support':str(min(dot(row,w) for row in objectives)),'min_gap_all_optimal_tuples':str(gap),'all_optimal_tuples':opts})
                if gap>0:
                    clones=integer_clones(w);I=instance_from_clones(k,m,clones)
                    signatures=[tuple(mask for mask,count in enumerate(clones,1) if count and mask>>a&1) for a in range(k)]
                    if len(set(signatures))<k:
                        rec['rejected']='duplicated topic sets after zero-weight types removed; labels cannot silently serve as distinct signals'
                        continue
                    assert independently_verify(cone,clones)
                    verify_certificate(I,StrategyCertificate(cone.actions,cone.root)).assert_valid()
                    payload={'scope':f'Signed {kind} candidate only; not Q-CAG-HALF','record':rec,'instance':I.to_dict(),'strategy':StrategyCertificate(cone.actions,cone.root).to_dict()}
                    (HERE/f'signed_{kind}_counterexample.json').write_text(json.dumps(payload,indent=2)+'\n')
                    print(json.dumps({'FOUND':rec}),flush=True)
                    (HERE/'signed_budget_report.json').write_text(json.dumps(records,indent=2)+'\n')
                    return
        print(json.dumps({'source_done':name,'comparisons':len(records),'maximum':max((r['max_min_signed_excess'] for r in records),default=None)}),flush=True)
    (HERE/'signed_budget_report.json').write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps({'status':'finite_no_counterexample','comparisons':len(records)}))

if __name__=='__main__':main()
