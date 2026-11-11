#!/usr/bin/env python3
"""Same real R^C/Z^C edge: 49*cut2_C + 10*cut13 + one terminal IC.

Only exact finite type algebra is used. The row coefficients are fixed.
The same C_i/C_j labels are retained through four (T,C) count classes.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import json
from pathlib import Path

import zero_capacity_rows_v1 as base
from zero_capacity_ic_bridge_v1 import possible_a4

HERE=Path(__file__).resolve().parent
WR,WZ,LAMBDA=F(49),F(10),F(17965)
SOURCE=WR*999+WZ*10000
LAST=WR*139+WZ*1358
LAST_CREDIT=F(10859)


@lru_cache(None)
def common_C_base(p,D,n,Cnum):
    candidates=[]
    for c1 in range(max(0,Cnum-(6-n)),min(n,Cnum)+1):
        c0=Cnum-c1
        classes=[(0,0,6-n-c0),(0,1,c0),(1,0,n-c1),(1,1,c1)]
        total=F(0)
        for ti,ci,ni in classes:
            for tj,cj,nj in classes:
                count=ni*(nj-int((ti,ci)==(tj,cj)))
                if not count:continue
                A0=base.L2(p,D,0,ti,tj,ci,cj,0,n)
                B0=base.L13(p,D,0,0,n,ti+tj)
                total+=F(count,30)*(WR*A0+WZ*B0)
        candidates.append((total,c1))
    val=min(x[0] for x in candidates)
    return val,tuple(c1 for x,c1 in candidates if x==val)


def value(p,a4,a5,a6,n,Cnum,joint):
    D=p+a4+a5+1;P=p+a4
    old,_=common_C_base(p,D,n,Cnum)
    residue=LAST_CREDIT*F(a6*(p+2*a4+2*a5),D*(p+2))
    return old+LAMBDA*F(n,6*(P+(1 if joint else 2)))+residue


def main():
    prior=json.loads((HERE/'mainline_zero_capacity_v1.json').read_text())
    checks=0;Rmargin=None;Zmargin=None;ratios=[];last_credit_exact_min=None
    four_state_table=[];last_credit_table=[];last_credit_witness=None
    for r in prior['cut2_complete_visible_table']:
        p,D,x,y,ci,cj,a6,n=(r[k] for k in ('p','d','x','y','Ci','Bj','A6','n'))
        A=tuple(map(F,r['L']));B=tuple(base.L13(p,D,t,a6,n,x+y) for t in (0,1));q=F(n,6)
        assert A[0]==base.L2(p,D,0,x,y,ci,cj,a6,n)
        assert A[1]>A[0]
        if a6==0:
            increment=(WR*(base.L2(p,D,0,x,y,ci,cj,1,n)-A[0])
                       +WZ*(base.L13(p,D,0,1,n,x+y)-B[0]))
            assert increment>=F(21718,p+2)
            candidate=increment*D
            credit_record={'p':p,'D':D,'Ti':x,'Tj':y,'Ci':ci,'Cj':cj,'n':n,
                           'A0_without_A6':str(A[0]),'A0_with_A6':str(base.L2(p,D,0,x,y,ci,cj,1,n)),
                           'B0_without_A6':str(B[0]),'B0_with_A6':str(base.L13(p,D,0,1,n,x+y)),
                           'weighted_increment':str(increment),'increment_times_D':str(candidate)}
            last_credit_table.append(credit_record)
            if last_credit_exact_min is None or candidate<last_credit_exact_min:
                last_credit_exact_min=candidate;last_credit_witness=credit_record
        for a4 in possible_a4(p,D):
            P=p+a4
            rm=WR*(A[1]-A[0])-LAMBDA*q/((P+1)*(P+2))
            zm=WZ*(B[1]-B[0])-LAMBDA/(P+1)
            assert rm>=0 and zm>=0
            Rmargin=rm if Rmargin is None else min(Rmargin,rm)
            Zmargin=zm if Zmargin is None else min(Zmargin,zm)
            ratio=F(3593,2)*q/((P+1)*(P+2)*(A[1]-A[0]))
            ratios.append((ratio,dict(r,A4=a4)))
            joint=min(WR*A[R]+WZ*B[Z]+LAMBDA*(q-Z)/(P+R+1) for R,Z in product((0,1),repeat=2))
            separate=min(WR*a for a in A)+min(WZ*B[Z]+LAMBDA*(q-Z)/(P+R+1) for R,Z in product((0,1),repeat=2))
            target=WR*A[0]+WZ*B[0]+LAMBDA*q/(P+1)
            target_sep=WR*A[0]+WZ*B[0]+LAMBDA*q/(P+2)
            assert joint==target and separate==target_sep
            assert joint-separate==LAMBDA*q/((P+1)*(P+2))
            four_state_table.append({'p':p,'D':D,'A4':a4,'A5':D-1-p-a4,'A6':a6,
                                     'Ti':x,'Tj':y,'Ci':ci,'Cj':cj,'n':n,'P':P,
                                     'A_values':list(map(str,A)),'B_values':list(map(str,B)),
                                     'R_margin':str(rm),'Z_margin':str(zm),
                                     'joint_four_state_min':str(joint),'separate_min':str(separate),
                                     'exact_shared_R_gain':str(joint-separate)})
            checks+=1
    maximum_ratio,ratio_witness=max(ratios,key=lambda x:x[0])
    actual_baselines=[]
    for p,a4,a5,a6 in product(range(4),(0,1),(0,1),(0,1)):
        D=p+a4+a5+1
        raw=WR*base.L2(p,D,0,0,0,0,0,0,0)+WZ*base.L13(p,D,0,0,0,0)
        residue=LAST_CREDIT*F(a6*(p+2*a4+2*a5),D*(p+2))
        total=raw+residue
        if a6:assert total>=0
        actual_baselines.append({'p':p,'A4':a4,'A5':a5,'A6':a6,'D':D,
                                 'raw':str(raw),'last_overlap_credit':str(residue),'net':str(total)})
    conditional=[];C_checks=0
    for p in range(4):
        for extra in range(3):
            D=p+extra+1
            for n,Cnum in product(range(7),range(7)):
                v,arg=common_C_base(p,D,n,Cnum);zero,_=common_C_base(p,D,n,0)
                assert v>=zero+F(9065*Cnum,6*(p+2))
                conditional.append({'p':p,'D':D,'n':n,'Cnum':Cnum,'base':str(v),'min_T_and_C_overlap_counts':list(arg)})
                C_checks+=1
    coverage={};obstruction={}
    for joint in (False,True):
        key='joint' if joint else 'separate_same_weights'
        miss=[value(0,0,0,0,n,0,joint) for n in range(1,7)];A=min(miss)
        taxes=[]
        for p,a4,a5,a6,n in product(range(4),(0,1),(0,1),(0,1),range(7)):
            if p+a4+a5+a6==0:continue
            v=value(p,a4,a5,a6,n,0,joint)
            taxes.append((A*int(n>0)-v,{'p':p,'A4':a4,'A5':a5,'A6':a6,'n':n},v))
        B,witness,worstval=max(taxes,key=lambda x:x[0])
        coverage[key]={'uncovered_by_opt_multiplicity':list(map(str,miss)),
                       'OPT_credit':str(A),'W_tax':str(B),'two_OPT_credit_minus_W_tax':str(2*A-B),
                       'worst_covered_signature':witness,'worst_covered_value':str(worstval)}
        upper=value(0,0,0,0,1,0,joint)
        lower=SOURCE-value(0,1,0,0,1,0,joint)
        obstruction[key]={'half_multiplier_upper_at_U':str(upper),'half_multiplier_lower_at_C':str(lower),
                          'incompatible':upper<lower}
    out={'scope':'universal fixed-coefficient same-real-edge R^C/Z^C algebra, not a new SPE counterexample or full half proof',
         'frozen_package_sha256':prior['frozen_package_sha256'],'weights':{'cut2_C':str(WR),'cut13':str(WZ),'Z_optimal_average_IC':str(LAMBDA)},
         'source_budget':str(SOURCE),'last_budget_before_cancellation':str(LAST),
         'universal_last_income_credit':str(LAST_CREDIT),'last_budget_after_cancellation':str(LAST-LAST_CREDIT),
         'four_state_cases':checks,'max_required_cut2_to_cut13_scale':str(maximum_ratio),
         'limiting_scale_signature':ratio_witness,'minimum_R_margin':str(Rmargin),'minimum_Z_margin':str(Zmargin),
         'observed_full_type_last_credit_minimum':str(last_credit_exact_min),
         'observed_full_type_last_credit_limiting_signature':last_credit_witness,
         'joint_gain_formula':'17965*n/[6*(P+1)*(P+2)], P=p+A4',
         'C_count_checks':C_checks,'actual_baselines':actual_baselines,
         'four_state_type_table':four_state_table,'A6_credit_type_table':last_credit_table,
         'conditional_common_C_count_table':conditional,'coverage_contracts':coverage,
         'remaining_two_signature_obstruction':obstruction}
    (HERE/'shared_rz_zero_capacity_v1.json').write_text(json.dumps(out,indent=2)+'\n')
    print({k:v for k,v in out.items() if k not in ('actual_baselines','conditional_common_C_count_table','four_state_type_table','A6_credit_type_table')})


if __name__=='__main__':main()
