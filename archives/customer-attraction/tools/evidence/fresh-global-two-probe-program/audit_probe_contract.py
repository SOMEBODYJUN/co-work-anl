"""Independent Fraction model; no original import, helper, LP or policy search.

Checks the 4 observed cones and 84 objectives; connects the already proved
four-multiplier H certificate to these exact source incentive rows.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations_with_replacement
import collections, hashlib, json

BASE = Path(__file__).resolve().parent
records = json.loads((BASE/'lp-capture.json').read_text())
assert len(records) == 84
q = 6; masks = list(range(1, 1 << q)); pairs = list(combinations_with_replacement(range(q), 2))
max_float_error = 0.; matrix_count = objective_count = identity_count = 0
policies = []; audits = []

def near(original, exact):
    global max_float_error
    delta = abs(original-float(exact)); max_float_error=max(max_float_error,delta)
    assert delta <= 1e-15, (original, str(exact), delta)

for case in range(4):
    block = records[case*21:(case+1)*21]; first=block[0]
    L=first['L']; A=first['actual']; reply=first['response']; B=reply[A]
    assert L==case+1 and len(reply)==q and all(0<=b<q for b in reply)
    bit=lambda m,a: (m>>a)&1
    def u(m,a,b):
        x,y=bit(m,a),bit(m,b); p=L*bit(m,0)
        return F(x,p+x+y) if x+y else F(0)
    labels=[('last',a,b) for a in range(q) for b in range(q) if b!=reply[a]]
    labels += [('root',a) for a in range(q) if a!=A]
    rows=[]
    for label in labels:
        if label[0]=='last':
            _,a,b=label; rows.append([u(m,b,a)-u(m,reply[a],a) for m in masks])
        else:
            _,a=label; rows.append([u(m,a,reply[a])-u(m,A,B) for m in masks])
    assert len(rows)==q*q-1==35
    for original,exact in zip(first['A_ub'],rows,strict=True):
        for f,r in zip(original,exact,strict=True): near(f,r); matrix_count+=1
    policies.append(dict(case=case,L=L,actual=A,reply=reply,row_labels=labels))
    for rec,pair in zip(block,pairs,strict=True):
        assert (rec['case'],rec['L'],rec['actual'],rec['response'],rec['compare'])==(case,L,A,reply,list(pair))
        assert rec['A_ub']==first['A_ub'] and rec['b_ub']==[0.]*35
        assert rec['A_eq']==[[1.]*63] and rec['b_eq']==[1]
        assert rec['bounds']==[0,None] and rec['method']=='highs'
        T,S=pair; cost=[]; multiplier=[F(0)]*35
        for topic,coefficient in [(B,F(1,2)),(0,F(1))]:
            if topic!=A: multiplier[labels.index(('root',topic))]+=coefficient
        for topic in pair:
            if topic!=B: multiplier[labels.index(('last',A,topic))]+=1
        remainders=[]
        for j,m in enumerate(masks):
            a,b,t,s,h=[bit(m,x) for x in (A,B,T,S,0)]
            p=L*h; D=(p+1)*(p+2)
            fresh=1-h
            target=u(m,A,B)+u(m,B,A)+fresh*(max(a,b)-max(t,s))
            cost.append(target); near(rec['c'][j],target); objective_count+=1
            rho=(a*((1-t)*(1-s)+t*s)+(1-a)*(F(b,2)+2*t*s)) if not h else ((1-b)*(2-F(3*a,2))+(t+s)*(3-a)+(p-1)*(1-F(a+b,2)+t+s))
            safety_B=u(m,B,reply[B])-F(b,p+2)
            safety_H=u(m,0,reply[0])-F(h,p+2)
            assert rho>=0 and safety_B>=0 and safety_H>=0
            remainder=F(rho,D)+F(1,2)*safety_B+safety_H
            assert remainder>=0
            assert target == -sum(lam*row[j] for lam,row in zip(multiplier,rows))+remainder
            remainders.append(remainder); identity_count+=1
        out=rec['result']; assert out['success'] and out['status']==0
        weights=[F(x).limit_denominator(10**9) for x in out['x']]
        assert len(weights)==63 and min(weights)>=0 and sum(weights)==1
        slacks=[-sum(c*w for c,w in zip(row,weights)) for row in rows]
        assert min(slacks)>=0
        value=sum(c*w for c,w in zip(cost,weights)); assert value>=0
        combined=sum(lam*s for lam,s in zip(multiplier,slacks))
        residual=sum(r*w for r,w in zip(remainders,weights))
        assert value==combined+residual
        near(out['fun'],value)
        audits.append(dict(case=case,L=L,compare=list(pair),floating_fun=out['fun'],exact_feasible_value=str(value),
                           nonzero_weights={str(m):str(w) for m,w in zip(masks,weights) if w},
                           exact_ic_slacks=[str(s) for s in slacks],
                           certificate_multipliers={str(i):str(x) for i,x in enumerate(multiplier) if x},
                           ic_contribution=str(combined),nonnegative_remainder=str(residual)))

summary=dict(status='PASS',original_imports=0,original_helpers=0,original_main=0,lp_calls=0,
             policies=policies,successful_observed_lp_calls=84,exact_feasible_reconstructions=84,
             unique_matrix_coefficients=matrix_count,objective_coefficients=objective_count,
             certificate_link_identities=identity_count,exact_ic_evaluations=84*35,
             max_absolute_float_coefficient_or_value_error=max_float_error,
             exact_values=dict(collections.Counter(x['exact_feasible_value'] for x in audits)),
             floating_min=min(r['result']['fun'] for r in records),floating_max=max(r['result']['fun'] for r in records),
             claim='Finite source/model integration audit plus reuse of an existing symbolic H certificate; positive reconstructed objectives are feasible values, not exact optimum certificates.',
             capture_sha256=hashlib.sha256((BASE/'lp-capture.json').read_bytes()).hexdigest(),records=audits)
assert matrix_count==8820 and objective_count==identity_count==5292
(BASE/'contract-audit.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k not in ('policies','records')},indent=2))
