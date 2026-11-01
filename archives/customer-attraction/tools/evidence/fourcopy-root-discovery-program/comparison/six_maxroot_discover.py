#!/usr/bin/env python3
"""Maximum-theme root envelopes from true final-theme copy branches.

Discovery only; verify.py reconstructs accepted rational certificates.
"""
import argparse
from fractions import Fraction as F
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog

HERE=Path(__file__).resolve().parent

def build(n, copies):
    base=list(range(n))
    paths=[base]
    next_bit=n
    for i in range(1,copies+1):
        path=base[:i]+[n-1]+list(range(next_bit,next_bit+n-i-1))
        paths.append(path)
        next_bit+=n-i-1
    bits=((np.arange(1<<next_bit)[:,None]>>np.arange(next_bit))&1).astype(float)
    root=bits[:,0]
    vals=[]
    prefixes=[]
    for path in paths:
        memb=bits[:,path]
        total=memb.sum(axis=1)
        vals.append(np.divide(memb,total[:,None],out=np.zeros_like(memb),where=total[:,None]!=0))
        prefixes.append(np.cumsum(memb,axis=1)-memb)
    names=[]; rows=[]; ocoef=[]
    def add(name,row,o=0):
        names.append(name); rows.append(row); ocoef.append(o)
    for j in range(1,next_bit):
        add(f'CAP:{j}',root-bits[:,j])
    for k in range(1,len(paths)):
        i=k
        add(f'COPY:{i}',vals[0][:,i]-vals[k][:,i])
    for k,path in enumerate(paths):
        first=1 if k==0 else k+1
        for i in range(first,n):
            for j in range(next_bit):
                if j==path[i]:continue
                floor=bits[:,j]/(prefixes[k][:,i]+n-i)
                add(f'FLOOR:{k}:{i}:{j}',vals[k][:,i]-floor)
        p=prefixes[k][:,n-2]
        tax=bits[:,path[n-2]]/((p+1)*(p+2))
        H=vals[k][:,n-2]+vals[k][:,n-1]+tax
        add(f'PAIR:{k}',n/2*H+p/(p+1),-1)
        p=prefixes[k][:,n-1]
        add(f'LAST:{k}',n*vals[k][:,n-1]+p/(p+1),-1)
    return bits,paths,names,np.array(rows).T,np.array(ocoef),vals[0][:,0]

def run(n,copies,cs):
    bits,paths,names,rows,ocoef,vT=build(n,copies)
    A=np.column_stack([-vT,rows])
    eq=np.r_[0,-ocoef][None,:]
    result=[]
    for C in cs:
        sol=linprog(np.r_[1.,np.zeros(len(names))],A_ub=A,b_ub=C*bits[:,0],A_eq=eq,b_eq=[1],bounds=[(0,None)]*(len(names)+1),method='highs')
        if not sol.success:
            print('FAILED',n,copies,C,sol.message,flush=True);continue
        active={key:str(F(float(x)).limit_denominator(10**8)) for key,x in zip(names,sol.x[1:]) if x>1e-8}
        rec=dict(n=n,copies=copies,paths=paths,bits=len(bits[0]),C=str(F(C)),B_float=float(sol.x[0]),B=str(F(float(sol.x[0])).limit_denominator(10**8)),multipliers=active,status=sol.message)
        result.append(rec)
        print(n,copies,C,sol.x[0],len(active),flush=True)
        (HERE/f'discovery_n{n}_c{copies}.json').write_text(json.dumps(result,indent=2))
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=6);p.add_argument('--copies',type=int,default=2);p.add_argument('--C',type=float,nargs='+',default=[-8,-4,0]);a=p.parse_args()
    run(a.n,a.copies,a.C)
