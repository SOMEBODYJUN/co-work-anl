#!/usr/bin/env python3
"""Portable exact evaluation of the displayed two-slope certificate formulas.

This is a transcription/reconciliation of the displayed mathematics, not a new
independent review. No Git objects, discovery code, NumPy or SciPy are needed.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

BASE=Path(__file__).resolve().parent

def div(n,d):return F(n,d) if n else F(0)

def rows(p,eta,e):
    a,b,c,d,q,r,s=eta
    labels=dict(zip('abcdqrs',eta));out={}
    for tag,y,start in [('actual',(a,b,c,d),0),('off',(d,q,r,s),1)]:
        u=[div(bit,p+sum(y)) for bit in y]
        for i in range(start,4):
            for name,bit in labels.items():
                out[f'{tag}:{i}:K:{name}']=u[i]-div(bit,p+sum(y[:i])+4-i)
        out[f'{tag}:3:sum-opt']=4*u[3]-div(e,p+sum(y[:3])+1)
        bg=p+y[0]+y[1]
        H=u[2]+u[3]+div(y[2],(bg+1)*(bg+2))
        out[f'{tag}:pair-opt']=6*H-div(e*(4-e),bg+1)-div(e*(e-1),bg+2)
    out['root-copy-d']=div(a,p+a+b+c+d)-div(d,p+d+q+r+s)
    return out

def main():
    reports={};minima={};all_res={}
    for name in ['binary_tail_exact','binary_tail_exact_1999']:
        cert=json.loads((BASE/'original'/(name+'.json')).read_text())
        weights={k:F(v) for k,v in cert['multipliers'].items()}
        beta=[F(cert['beta0']),F(cert['beta1'])]
        res={}
        for p,eta,e in product((0,1),product((0,1),repeat=7),range(5)):
            row=rows(p,eta,e);k=sum(eta[:4])
            value=beta[p]*div(k,p+k)-div(e,p+e)-sum(weights[j]*row[j] for j in weights)
            assert value>=0,(name,p,eta,e,value)
            res[p,eta,e]=value
        assert len(res)==1280 and sum(v==0 for v in res.values())==cert['zero_residuals']
        reports[name]={'states':len(res),'minimum':str(min(res.values())),
                       'zero_states':sum(v==0 for v in res.values())}
        minima[name]={}
        for actual in product((0,1),repeat=4):
            minima[name][''.join(map(str,actual))]=[str(min(res[p,(*actual,*aux),e] for aux in product((0,1),repeat=3) for e in range(5))) for p in (0,1)]
        all_res[name]=res
    reference=json.loads((BASE/'original/oct25_binary_tail_raw_audit.json').read_text())
    for entry in reference['retained_residuals_160']:
        p=entry['p'];actual=tuple(map(int,entry['abcd']));e=entry['comparison_count']
        values=[(all_res['binary_tail_exact_1999'][p,(*actual,*aux),e],aux) for aux in product((0,1),repeat=3)]
        value,aux=min(values)
        assert str(value)==entry['minimum_residual']
        assert ''.join(map(str,aux))==entry['attaining_qrs']
    result={'scope':'portable-transcription-of-displayed-mathematical-formulas',
            'new_independent_review_claimed':False,'certificates':reports,
            'complete_minimum_tables':minima,
            'strong_160_minima_and_attaining_auxiliary_bits_equal_original_raw_audit':True}
    (BASE/'replay').mkdir(parents=True,exist_ok=True)
    (BASE/'replay/coefficient_tables.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
