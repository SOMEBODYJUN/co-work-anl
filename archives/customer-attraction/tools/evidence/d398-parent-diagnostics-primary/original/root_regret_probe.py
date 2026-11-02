"""One exact fixed-tail-cone diagnostic of the NEW constant-three compiler.

Root IC is omitted, positive-depth IC is retained at every ordered history.
An extra nonnegative variable Delta dominates every true root regret. Optimize
(coverage of a comparison portfolio - 3*Delta)/actual W. A value >2 would yield
a compiler counterexample only after exact unit-customer and full-tree replay.
A <=2 result covers only the explicitly saved fixed policy cones.
"""
from pathlib import Path
import sys, json, hashlib
from fractions import Fraction as F
from itertools import combinations
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests/audits'))
from customer_attraction_strategy_lp import StrategyCone,payoff_row,coverage_row,dot,serializable
from customer_attraction.model import Instance
HERE=Path(__file__).resolve().parent

def optimize(name):
    ip=ROOT/'examples/customer_attraction'/f'{name}.json'
    cp=ROOT/'evidence/certificates/customer_attraction'/f'{name}.json'
    I=Instance.from_dict(json.loads(ip.read_text()))
    cert=json.loads(cp.read_text());cert=cert.get('strategy',cert)
    actions={tuple(x['history']):x['action'] for x in cert['actions']}
    p,m=I.topic_count,I.players;records=[]
    for actual in range(p):
        A=dict(actions);A[()]=actual;C=StrategyCone(p,m,A)
        rows=set()
        for h,a in A.items():
            if not h:continue
            own=payoff_row(p,C.terminals[h],a)
            for b in range(p):
                r=tuple(x-y for x,y in zip(own,payoff_row(p,C.terminals[h+(b,)],b)))+(F(0),)
                if any(r):rows.add(r)
        own=payoff_row(p,C.root,actual)
        for b in range(p):
            r=tuple(x-y for x,y in zip(own,payoff_row(p,C.terminals[(b,)],b)))+(F(1),)
            rows.add(r)
        C.rows=tuple(sorted(rows));C.welfare=C.welfare+(F(0),)
        C.matrix=np.array(C.rows,dtype=float)
        for J in combinations(range(p),min(m,p)):
            v=coverage_row(p,J)+(F(-3),)
            res=linprog(-np.array(v,dtype=float),A_ub=-C.matrix,b_ub=np.zeros(len(C.rows)),
                        A_eq=np.array([C.welfare],dtype=float),b_eq=[1],bounds=(0,None),method='highs')
            rec={'actual_root':actual,'portfolio':J,'status':res.message}
            if res.success:
                vals=tuple(F(float(x)).limit_denominator(10**7) for x in res.x)
                if not (C.verify(vals) and dot(C.welfare,vals)==1):vals=C.recover_vertex(res.x)
                assert vals is not None and C.verify(vals) and dot(C.welfare,vals)==1
                beta=F(float(-res.eqlin.marginals[0])).limit_denominator(10**7)
                dual=tuple(F(float(-x)).limit_denominator(10**7) for x in res.ineqlin.marginals)
                residual=tuple(beta*w-sum(mu*r[j] for mu,r in zip(dual,C.rows))-z for j,(w,z) in enumerate(zip(C.welfare,v)))
                exactdual=all(mu>=0 for mu in dual) and all(x>=0 for x in residual)
                value=dot(v,vals)
                dvals=[dot(payoff_row(p,C.terminals[(b,)],b),vals[:-1]) for b in range(p)]
                delta=max(dvals)-dvals[actual]
                assert vals[-1]>=delta>=0
                # Independently check each original positive-depth history.
                for h,a in A.items():
                    if h:assert dot(payoff_row(p,C.terminals[h],a),vals[:-1])>=max(dot(payoff_row(p,C.terminals[h+(b,)],b),vals[:-1]) for b in range(p))
                rec.update(value=value,dual_bound=beta if exactdual else None,exact_optimal=exactdual and beta==value,
                           sparse_primal=[(j,x) for j,x in enumerate(vals) if x],
                           sparse_dual=[(j,x) for j,x in enumerate(dual) if x] if exactdual else [],
                           root_regret=delta,actual_gap=dot(coverage_row(p,J),vals[:-1])-2)
                if value>2:
                    rec['candidate']='NEW_COMPILER_THRESHOLD_POSITIVE'
                    print('CANDIDATE',name,serializable(rec),flush=True)
            records.append(rec)
    result={'source_instance':str(ip.relative_to(ROOT)),'source_certificate':str(cp.relative_to(ROOT)),
            'source_certificate_sha256':hashlib.sha256(cp.read_bytes()).hexdigest(),
            'topics':p,'players':m,'scope':'Only this fixed positive-depth policy cone, all actual roots and all m-topic comparison supports. Not a general bound.',
            'records':records}
    print(name,'LPs',len(records),'max',max((r.get('value',F(-1000)) for r in records)), 'all_exact_duals',all(r.get('exact_optimal',False) for r in records),flush=True)
    return result

if __name__=='__main__':
    names=['root_tax_failure','eight_cce_welfare_gap','aggregate_theta_failure','fractional_actual_load_failure']
    output={'criterion':'OPT-2W>3Delta; failure of finite cones is not general evidence','inputs':[optimize(n) for n in names]}
    (HERE/'root_regret_probe.json').write_text(json.dumps(serializable(output),indent=2)+'\n')
