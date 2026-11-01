"""No-LP check of original arithmetic blocks against exact two-player formulas.

The one reply map uses an explicitly synthetic seed0, NOT the unrecorded seed
of the historical12000-case report. The original run/main are never invoked.
"""
from argparse import ArgumentParser
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import ast
import json
import random
import time
import numpy as np


def main():
    ap=ArgumentParser(); ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True); args=ap.parse_args()
    raw=args.source.read_bytes()
    assert sha256(raw).hexdigest()=='efdfe17ac4a1751fc784c2c833e59d6fb5443935d6fce4c19aca148a5f191a12'
    tree=ast.parse(raw); fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='run')
    loop=next(n for n in fn.body if isinstance(n,ast.For) and isinstance(n.target,ast.Name) and n.target.id=='i')
    prefix=fn.body[:fn.body.index(loop)]
    stop=next(i for i,n in enumerate(loop.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='res' for t in n.targets))
    fragment=ast.Module(body=prefix+loop.body[:stop],type_ignores=[])
    assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='linprog' for n in ast.walk(fragment))
    q,L,seed=7,1,0
    env={'np':np,'random':random,'time':time,'q':q,'L':L,'seed':seed,'cases':1}
    exec(compile(fragment,str(args.source),'exec'),env)
    masks=list(range(1,2**q)); reply=env['reply']; A,B,H,T,S=1,2,0,3,4
    def bit(mask,a):return (mask>>a)&1
    def u(a,b,mask):
        aa,bb=bit(mask,a),bit(mask,b)
        return F(aa,L*bit(mask,H)+aa+bb) if aa else F()
    exact_utils=[[[u(a,b,m) for m in masks] for b in range(q)] for a in range(q)]
    utility_errors=[abs(F(float(env['utils'][a,b,j]))-exact_utils[a][b][j]) for a,b in product(range(q),repeat=2) for j in range(len(masks))]
    rows=[]; labels=[]
    for a,b in product(range(q),repeat=2):
        if b!=reply[a]:
            rows.append([u(b,a,m)-u(reply[a],a,m) for m in masks]); labels.append(['last',a,b,reply[a]])
    for a in range(q):
        if a!=A:
            rows.append([u(a,reply[a],m)-u(A,B,m) for m in masks]); labels.append(['first',a,reply[a]])
    objective=[u(A,B,m)+u(B,A,m)+(1-bit(m,H))*(int(bool(bit(m,A) or bit(m,B)))-int(bool(bit(m,T) or bit(m,S)))) for m in masks]
    assert env['masks'].tolist()==masks and env['reply'][A]==B and len(rows)==q*q-1==48
    assert len(env['rows'])==48
    row_errors=[abs(F(float(x))-y) for floatrow,exactrow in zip(env['rows'],rows) for x,y in zip(floatrow,exactrow)]
    objective_errors=[abs(F(float(x))-y) for x,y in zip(env['obj'],objective)]
    assert max(utility_errors+row_errors+objective_errors)<=F(1,2**50)
    lam={labels.index(['first',B,reply[B]]):F(1,2),labels.index(['first',H,reply[H]]):F(1),
         labels.index(['last',A,T,B]):F(1),labels.index(['last',A,S,B]):F(1)}
    remainder=[]
    for j,m in enumerate(masks):
        a,b,t,s,h=[bit(m,x) for x in [A,B,T,S,H]]; p=L*h; D=(p+1)*(p+2)
        if not h:
            rho=a*((1-t)*(1-s)+t*s)+(1-a)*(F(b,2)+2*t*s)
        else:
            rho=(1-b)*(2-F(3*a,2))+(t+s)*(3-a)+(p-1)*(1-F(a+b,2)+t+s)
        safety_B=u(B,reply[B],m)-F(b,p+2)
        safety_H=u(H,reply[H],m)-F(h,p+2)
        eta=F(rho,D)+F(1,2)*safety_B+safety_H
        lhs=objective[j]+sum(w*rows[k][j] for k,w in lam.items())
        assert lhs==eta and rho>=0 and safety_B>=0 and safety_H>=0 and eta>=0
        remainder.append({'mask':m,'rho':str(rho),'safety_B':str(safety_B),'safety_H':str(safety_H),'objective_plus_IC_rows':str(eta)})
    # The all-topics type is a universal feasible witness for EVERY reply map.
    full=(1<<q)-1
    assert all(u(a,b,full)==F(1,L+2) for a,b in product(range(q),repeat=2))
    assert all(row[-1]==0 for row in rows) and objective[-1]==F(2,L+2)
    out={'status':'PASS_SYNTHETIC_CONE_ARITHMETIC_AND_EXACT_CERTIFICATE_MAPPING',
         'scope':'One synthetic q7/L1/seed0 reply map; original AST arithmetic only, not historical12000 samples or original run/main. General legal-H theorem is reused analytically.',
         'source_sha256':sha256(raw).hexdigest(),'auditor_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
         'synthetic_inputs':{'q':q,'L':L,'seed':seed,'reply':reply},'columns':127,'IC_rows':48,
         'utility_entries_checked':q*q*len(masks),'row_coefficients_checked':48*127,'objective_entries_checked':127,
         'maximum_float_utility_error':str(max(utility_errors)),'maximum_float_row_error':str(max(row_errors)),
         'maximum_float_objective_error':str(max(objective_errors)),
         'row_labels':labels,'exact_rows':[[str(x) for x in row] for row in rows],'exact_objective':[str(x) for x in objective],
         'four_multipliers':[{'row':k,'label':labels[k],'multiplier':str(w)} for k,w in lam.items()],
         'exact_nonnegative_remainders':remainder,'universal_feasible_type':{'mask':full,'weight':'1','all_IC_slacks':'0','objective':str(F(2,L+2))},
         'original_AST_arithmetic_executions':1,'original_function_calls':0,'original_main_calls':0,'LP_calls':0,
         'historical_sampling_reconstructed':False,'new_universal_certificate_discovery':False}
    args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['row_labels','exact_rows','exact_objective','exact_nonnegative_remainders']},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
