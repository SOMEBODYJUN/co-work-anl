#!/usr/bin/env python3
"""One fixed 49:10 same R^C/Z^C contract on the complete-ZZ projection point.

No discovery and no parameter change. Rebuild the complete joint-state row,
the four-state eliminated row, and the weaker A6-income-transfer row.
"""
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import json
from pathlib import Path

import joint_discounted_requery as data_api
import zero_capacity_rows_v1 as base

HERE=Path(__file__).resolve().parent
INPUT=HERE.parent/'master_cuts'/'complete_zz_5799_v1_original4849_exact.json'
EXPECTED='1af6fd35f9cf1a51220072e627df042b450a52a7c6ecac388a98247ecac043d2'
ORBIT=(1,0)


@lru_cache(None)
def cost(kind,actual,qs):
    p=sum(actual[:3]);D=sum(actual[:5])+1;P=sum(actual[:4])
    x,y,ci,cj=map(int,(qs[6],qs[9],qs[8],qs[11]));R,Z=map(int,(qs[12],qs[13]))
    n=qs[6]+qs[9]+4*qs[14];assert n.denominator==1;n=int(n)
    a6=actual[5];q=F(n,6)
    if kind=='full_joint_state':
        A=base.L2(p,D,R,x,y,ci,cj,a6,n)
        B=base.L13(p,D,Z,a6,n,x+y)
        return 49*A+10*B+17965*(q-Z)/(P+R+1)
    if kind=='eliminated_four_state':
        return 49*base.L2(p,D,0,x,y,ci,cj,a6,n)+10*base.L13(p,D,0,a6,n,x+y)+17965*q/(P+1)
    assert kind=='after_A6_income_transfer'
    residue=F(10859*a6*(p+2*actual[3]+2*actual[4]),D*(p+2))
    return 49*base.L2(p,D,0,x,y,ci,cj,0,n)+10*base.L13(p,D,0,0,n,x+y)+17965*q/(P+1)+residue


def make_row(cols,hs,kind):
    u4=F(148951);u6=F(9532 if kind=='after_A6_income_transfer' else 20391)
    row=[F(0)]*len(cols);hi=None
    def value(h,g,st):
        actual=tuple(map(int,h['column']['actual_bits']))
        qs=data_api.query_vector(actual,h['column']['hist'],g,st)
        return cost(kind,actual,qs)
    for index,col in enumerate(cols):
        if col['kind']=='K':continue
        if col['kind']=='hist':
            hi=index;h=hs[index];a=tuple(map(int,col['actual_bits']));den=sum(a)
            row[index]=u4*data_api.share(a[3],den)+u6*data_api.share(a[5],den)
            row[index]-=sum((F(n,30)*value(h,g,(0,0)) for g,n in h['groups'].items() if g[:2]==ORBIT),F(0))
        elif col['kind']=='joint-reply':
            f,diag,wi,wj=col['group'];g=f,diag,tuple(wi),tuple(wj)
            if g[:2]!=ORBIT:continue
            h=hs[hi]
            row[index]=-F(h['groups'][g],30)*(value(h,g,tuple(col['state']))-value(h,g,(0,0)))
    return row,(u4,u6)


def main():
    assert hashlib.sha256(INPUT.read_bytes()).hexdigest()==EXPECTED
    data,cols,hs,K,u=data_api.read_input(INPUT);records=[]
    states=data_api.state_measure(hs,3,0,ORBIT)
    for kind in ('full_joint_state','eliminated_four_state','after_A6_income_transfer'):
        row,(u4,u6)=make_row(cols,hs,kind)
        value=sum((v*F(c['weight']) for v,c in zip(row,cols)),F(0))
        direct=u4*u[3]+u6*u[5]
        for (p,ell,t,qs),mass in states.items():
            actual=tuple(map(int,qs[:6]));direct-=mass*cost(kind,actual,qs)
        assert value==direct
        if kind!='full_joint_state':assert all(v==0 for v,c in zip(row,cols) if c['kind']=='joint-reply')
        rec={'kind':kind,'budget':{'u4':str(u4),'u6':str(u6),'K':'0'},
             'exact_slack':str(value),'exact_slack_float':float(value),'negative':value<0,
             'column_count':len(cols),'row_nonzero':[[j,str(v)] for j,v in enumerate(row) if v],
             'row_sha256':hashlib.sha256(json.dumps(list(map(str,row)),separators=(',',':')).encode()).hexdigest()}
        records.append(rec);print(kind,float(value),'nonzero',len(rec['row_nonzero']),flush=True)
    vals=[F(r['exact_slack']) for r in records]
    assert vals[0]<=vals[1]<=vals[2]
    out={'scope':'single fixed-contract evaluation only; no reoptimization, no change to frozen 49:10 evidence',
         'input':str(INPUT),'input_sha256':EXPECTED,'input_W':data['W'],'orbit':[1,0],
         'fixed_weights':{'cut2_C':'49','cut13':'10','true_Z_optimal_average_IC':'17965'},
         'static_query_substitution':'only old Bj query slot of cut2 becomes old Cj; hidden b stays hidden',
         'full_columns':len(cols),'positive_visible_states':len(states),'rows':records,
         'loss_from_eliminating_RZ':str(vals[1]-vals[0]),
         'loss_from_analytic_A6_bound':str(vals[2]-vals[1]),'any_negative':any(v<0 for v in vals)}
    (HERE/'fixed_shared_rz_completezz5799_v1.json').write_text(json.dumps(out,indent=2)+'\n')
    print({'any_negative':out['any_negative'],'slacks_float':list(map(float,vals))},flush=True)


if __name__=='__main__':main()
