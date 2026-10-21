"""Repair every terminal sharp dilution by a common linear potential shift.

Only a finite |q|<=3 monotone-DR abstract potential game is claimed. The
resulting payoff table is NOT a common signed-customer table, by explicit
same-support efficiency disagreement. No optimizer or discovery import.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from pathlib import Path
from math import ceil
import json

HERE=Path(__file__).resolve().parent


def main():
    data=json.loads((HERE.parent/'next_independent/candidate_potential_individual.json').read_text())
    p,n=data['topics'],data['players']
    phi={tuple(row['counts']):F(row['value']) for row in data['potential']}
    def cnt(h):return tuple(h.count(a) for a in range(p))
    def value(q,a):
        b=list(q);b[a]-=1
        return phi[q]-phi[tuple(b)]
    states=[cnt(h) for h in combinations_with_replacement(range(p),n)]
    vertices=[(q,a) for q in states for a in range(p) if q[a]]
    maximum=F(0);witness=None;constraints=[];unit_count=0
    for q,a in vertices:
        for r,b in vertices:
            if a!=b or q==r:continue
            ratios=[]
            for mask in range(1,1<<p):
                if mask&(1<<a):
                    qload=sum(q[c] for c in range(p) if mask&(1<<c))
                    rload=sum(r[c] for c in range(p) if mask&(1<<c))
                    ratios.append(F(rload,qload))
            gamma=max(ratios)
            assert gamma>=1
            if gamma==1:
                unit_count+=1
                assert value(q,a)<=value(r,a)
            else:
                needed=(value(q,a)-gamma*value(r,a))/(gamma-1)
                if needed>maximum:
                    maximum=needed;witness=(q,r,a,gamma)
            constraints.append((q,r,a,gamma))
    K=ceil(maximum)
    slacks=[gamma*(value(r,a)+K)-(value(q,a)+K) for q,r,a,gamma in constraints]
    assert min(slacks)>=0
    # Adding K*|q| raises every occupied player's payoff by K; every SPE row
    # and every self-congestion or DR row is exactly invariant.
    actual=tuple(data['actual_counts'])
    welfare=sum(actual[a]*(value(actual,a)+K) for a in range(p) if actual[a])
    guarantee=F(data['safety_lower_bound'])+K
    assert welfare-n*guarantee==-189
    by_support={};mismatches=[]
    for q in states:
        support=tuple(a for a in range(p) if q[a])
        total=sum(q[a]*(value(q,a)+K) for a in support)
        if support not in by_support:by_support[support]=(q,total)
        elif total!=by_support[support][1]:
            old,previous=by_support[support]
            mismatches.append({'support':support,'first_counts':old,'second_counts':q,
                               'first_total':str(previous),'second_total':str(total),
                               'difference':str(total-previous)})
    assert mismatches
    q,r,a,gamma=witness
    result={'status':'exact_abstract_counterexample_with_ALL_terminal_sharp_dilution_NOT_CAG',
            'domain':'all count vectors of total at most 3; no global extension claimed',
            'common_linear_shift_K':K,'exact_minimum_shift':str(maximum),
            'sharp_dilution_constraints':len(constraints),'unit_ratio_constraints':unit_count,
            'minimum_dilution_slack':str(min(slacks)),
            'tight_shift_witness':{'q':q,'r':r,'topic':a,'gamma':str(gamma)},
            'shifted_welfare':str(welfare),'fixed_query_guarantee':str(guarantee),
            'welfare_minus_n_guarantee':str(welfare-n*guarantee),
            'same_support_efficiency_mismatch_count':len(mismatches),
            'same_support_efficiency_first_mismatch':mismatches[0],
            'excluded_even_by_common_signed_customer_representation':True}
    (HERE/'shifted_potential_dilution_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
