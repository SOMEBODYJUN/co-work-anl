#!/usr/bin/env python3
"""Honest transfer of the stronger 21669/D A6 credit; no point separation."""
from fractions import Fraction as F
from itertools import product
import hashlib
import json
from pathlib import Path

import zero_capacity_rows_v1 as base

HERE=Path(__file__).resolve().parent
INPUT=HERE/'shared_rz_zero_capacity_v1.json'
EXPECTED='2bd7138c2d35c19100c7d12bde244d2d37695b4609fbbf51260b1574c4b64f34'


def hidden_map(p,D,n,r,h):
    b,c,j,v=h
    if b==0 or D>=p+2:return h,'same_state'
    if c==1 or j==0 or p>=2:return (0,c,j,v),'lower_b_first'
    assert b==1 and c==0 and j==1 and p in (0,1) and D==p+1
    if v==1:return (0,1,1,1),'exception_v1'
    if p==1:return (0,1,1,0),'exception_p1_v0'
    if n>=1:return (0,1,1,0),'exception_p0_positive_n'
    assert r==0
    return (0,0,0,0),'exception_zero_n'


def main():
    assert hashlib.sha256(INPUT.read_bytes()).hexdigest()==EXPECTED
    old=json.loads(INPUT.read_text())
    map_count=0;reasons={};minimum_gap=None
    for p,extra,r,m,h in product(range(4),range(3),range(3),range(5),product((0,1),repeat=4)):
        D=p+extra+1;n=r+m;h0,reason=hidden_map(p,D,n,r,h);assert h[3]==h0[3]
        gap=base.E13(p,D,0,*h,1,n,r)-base.E13(p,D,0,*h0,0,n,r)-F(2162,D)
        assert gap>=0,(p,D,n,r,h,h0,gap)
        minimum_gap=gap if minimum_gap is None else min(minimum_gap,gap)
        reasons[reason]=reasons.get(reason,0)+1;map_count+=1
    for r in old['A6_credit_type_table']:
        assert F(r['A0_with_A6'])-F(r['A0_without_A6'])>=F(1,r['D'])
        assert F(r['B0_with_A6'])-F(r['B0_without_A6'])>=F(2162,r['D'])
        assert F(r['increment_times_D'])>=21669
    table={(r['p'],r['D'],r['n'],r['Cnum']):F(r['base']) for r in old['conditional_common_C_count_table']}
    def value(p,a4,a5,a6,n,Cnum,joint):
        D=p+a4+a5+1;P=p+a4
        return table[p,D,n,Cnum]+F(17965*n,6*(P+(1 if joint else 2)))
    baselines=[]
    for p,a4,a5,a6 in product(range(4),(0,1),(0,1),(0,1)):
        D=p+a4+a5+1;v=table[p,D,0,0]
        baselines.append({'p':p,'A4':a4,'A5':a5,'A6':a6,'D':D,
                          'new_baseline':str(v),'negative':v<0})
    coverage={};obstructions={};gain_checks=0;complete_coverage_values=[]
    for joint in (False,True):
        key='joint' if joint else 'separate_same_weights'
        misses=[value(0,0,0,0,n,0,joint) for n in range(1,7)];A=min(misses)
        taxed=[]
        for p,a4,a5,a6,n in product(range(4),(0,1),(0,1),(0,1),range(7)):
            v=value(p,a4,a5,a6,n,0,joint)
            s={'p':p,'A4':a4,'A5':a5,'A6':a6,'n':n}
            if p+a4+a5+a6:taxed.append((A*int(n>0)-v,s,v))
            complete_coverage_values.append(dict(s,mode=key,value=str(v)))
        B=max(x[0] for x in taxed)
        witnesses=[dict(s,value=str(v)) for tax,s,v in taxed if tax==B]
        assert str(A)==old['coverage_contracts'][key]['OPT_credit']
        assert str(B)==old['coverage_contracts'][key]['W_tax']
        coverage[key]={'OPT_credit':str(A),'W_tax':str(B),'two_OPT_credit_minus_W_tax':str(2*A-B),
                       'uncovered_by_opt_multiplicity':list(map(str,misses)),
                       'all_worst_covered_signatures':witnesses}
        upper=value(0,0,0,0,1,0,joint);lower=F(148951)-value(0,1,0,0,1,0,joint)
        assert str(upper)==old['remaining_two_signature_obstruction'][key]['half_multiplier_upper_at_U']
        assert str(lower)==old['remaining_two_signature_obstruction'][key]['half_multiplier_lower_at_C']
        obstructions[key]={'upper_at_U':str(upper),'lower_at_C':str(lower),'incompatible':upper<lower}
    for p,a4,a5,a6,n,Cnum in product(range(4),(0,1),(0,1),(0,1),range(7),range(7)):
        delta=value(p,a4,a5,a6,n,Cnum,True)-value(p,a4,a5,a6,n,Cnum,False)
        P=p+a4
        assert delta==F(17965*n,6*(P+1)*(P+2));gain_checks+=1
    out={'scope':'stronger A6-income transfer on frozen 49:10 contract, finite type algebra only, no new necessary-point evaluation',
         'shared_rz_input_sha256':EXPECTED,
         'budget_before':{'u4':'148951','u6':'20391','K':'0'},
         'A6_income_credit':'21669','budget_after':{'u4':'148951','u6':'-1278','K':'0'},
         'hidden_map_cases':map_count,'hidden_map_reason_counts':reasons,'hidden_map_minimum_gap':str(minimum_gap),
         'frozen_A6_difference_types_rechecked':len(old['A6_credit_type_table']),
         'unchanged_shared_R_gain_checks':gain_checks,
         'new_actual_baselines':baselines,
         'negative_A6_one_patterns':[r for r in baselines if r['A6'] and r['negative']],
         'coverage_contracts':coverage,'coverage_type_table':complete_coverage_values,
         'unchanged_two_signature_obstruction':obstructions}
    (HERE/'strong_a6_transfer_v1.json').write_text(json.dumps(out,indent=2)+'\n')
    print({k:v for k,v in out.items() if k not in ('new_actual_baselines','coverage_type_table')})


if __name__=='__main__':main()
