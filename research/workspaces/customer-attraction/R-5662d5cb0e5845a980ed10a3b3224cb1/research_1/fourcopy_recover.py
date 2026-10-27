#!/usr/bin/env python3
"""Outward integer-grid recovery; outputs require verify.py acceptance."""
from fractions import Fraction as F
from pathlib import Path
import argparse,json,math
from fourcopy_verify import coefficients,geometry,verify

HERE=Path(__file__).resolve().parent

def recover(c):
    n,copies=c['n'],c['copies'];paths,d=geometry(n,copies)
    grid=10**8
    weights={k:round(float(F(v))*grid) for k,v in c['multipliers'].items()}
    for i in range(1,d):weights.setdefault(f'CAP:{i}',0)
    S=sum(v for k,v in weights.items() if k.startswith(('PAIR:','LAST:')))
    # Normalize OPT coefficients exactly. Correct rounding on T=0 using common
    # legal CAP credits; on T=1 the root share pays their extra cost.
    correction=0
    for mask in range(0,1<<d,2):
        b,L,v,rows=coefficients(mask,n,copies,weights)
        raw=sum(w*g for w,g in zip(weights.values(),rows))
        ones=sum(b)
        if raw>0:correction=max(correction,(raw+L*ones-1)//(L*ones))
    for i in range(1,d):weights[f'CAP:{i}']+=correction
    C=F(c['C']);B=F(0)
    for mask in range(1,1<<d,2):
        b,L,v,rows=coefficients(mask,n,copies,weights)
        raw=sum(w*g for w,g in zip(weights.values(),rows))
        required=(F(raw,S)-C*L)/v
        B=max(B,required)
    result=dict(n=n,copies=copies,paths=paths,bits=d,C=str(C),B=str(B),B_float=float(B),multipliers={k:str(F(v,S)) for k,v in weights.items() if v},recovery=dict(grid=grid,opt_sum=S,uniform_cap_integer_correction=correction))
    check=verify(result)
    print(n,copies,str(C),str(B),float(B),'types',check['types'],'zeros',check['zero_types'],flush=True)
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,default=HERE/'discovery_n6_c2.json');p.add_argument('--output',type=Path,default=HERE/'exact_cuts.json');a=p.parse_args()
    result=[recover(c) for c in json.loads(a.input.read_text())]
    a.output.write_text(json.dumps(result,indent=2))
