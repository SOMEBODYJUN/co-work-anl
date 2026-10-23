"""Diagnostic only: actual-profile deletion static security caps."""
from fractions import Fraction as F
from pathlib import Path
import json,sys
import numpy as np
from scipy.optimize import linprog
from customer_attraction import Instance, StrategyCertificate, verify_certificate

BASE=Path(__file__).resolve().parents[5]
OUT=Path(__file__).resolve().parent

def matrix(ins,counts):
    support=[a for a,n in enumerate(counts) if n]
    mat=[]
    for a in range(ins.topic_count):
        row=[]
        for b in support:
            q=list(counts);q[b]-=1
            row.append(sum((F(t.multiplicity,1+sum(q[j] for j in t.topics))
                            for t in ins.customers if a in t.topics),F(0)))
        mat.append(row)
    return support,mat

def rational_probs(values):
    vals=[max(F(0),F(float(x)).limit_denominator(1000000)) for x in values]
    total=sum(vals)
    return [x/total for x in vals]

def diagnose(ins,counts):
    support,mat=matrix(ins,counts)
    A=np.array([[float(x) for x in row] for row in mat])
    nc=len(support);nr=ins.topic_count
    primal=linprog([0]*nc+[1],A_ub=np.column_stack([A,-np.ones(nr)]),b_ub=np.zeros(nr),
                    A_eq=np.array([[1]*nc+[0]]),b_eq=[1],bounds=[(0,None)]*nc+[(None,None)],method='highs')
    dual=linprog([0]*nr+[-1],A_ub=np.column_stack([-A.T,np.ones(nc)]),b_ub=np.zeros(nc),
                  A_eq=np.array([[1]*nr+[0]]),b_eq=[1],bounds=[(0,None)]*nr+[(None,None)],method='highs')
    assert primal.success and dual.success
    lam=rational_probs(primal.x[:-1]);p=rational_probs(dual.x[:-1])
    upper=max(sum(lam[j]*row[j] for j in range(nc)) for row in mat)
    lower=min(sum(p[i]*mat[i][j] for i in range(nr)) for j in range(nc))
    W=ins.welfare(counts);m=ins.players;threshold=F(2*W,2*m-1)
    return dict(W=W,m=m,counts=counts,support=support,lower=str(lower),upper=str(upper),
                threshold=str(threshold),strict_failure=lower>threshold,
                query=[str(x) for x in p],deletion=[str(x) for x in lam],
                matrix=[[str(x) for x in row] for row in mat])

def read_cert(obj):
    if isinstance(obj,dict):
        if 'actions' in obj:
            return obj
        for key in ['strategy','certificate']:
            if key in obj:
                return read_cert(obj[key])
    return None

def main():
    reports=[]
    for ep in sorted((BASE/'examples/customer_attraction').glob('*.json')):
        cp=BASE/'evidence/certificates/customer_attraction'/ep.name
        if not cp.exists():continue
        ins=Instance.from_dict(json.loads(ep.read_text()))
        raw=read_cert(json.loads(cp.read_text()))
        if raw is None:continue
        actions={tuple(x['history']):x['action'] for x in raw['actions']}
        hist=()
        for _ in range(ins.players):hist+= (actions[hist],)
        counts=ins.counts(hist,terminal=True)
        cert=StrategyCertificate(actions,counts)
        report=verify_certificate(ins,cert)
        report.assert_valid()
        item=diagnose(ins,counts);item.update(example=ep.name,path=hist,verified=True)
        reports.append(item)
        print(ep.name,item['lower'],item['upper'],item['threshold'],item['strict_failure'],flush=True)
    (OUT/'leave_one_out_existing.json').write_text(json.dumps(reports,indent=2)+'\n')

if __name__=='__main__':main()
