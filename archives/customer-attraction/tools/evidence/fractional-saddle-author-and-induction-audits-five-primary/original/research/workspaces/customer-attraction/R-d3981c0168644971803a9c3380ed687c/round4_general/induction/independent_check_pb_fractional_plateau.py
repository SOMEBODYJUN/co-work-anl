"""Independent definition-level scalar audit of PB fractional saddle/plateau.
Does not import the author's audit or use floating point for certification.
The old PB full-history SPE is an explicit external mathematical dependency.
"""
from fractions import Fraction as Q
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
k,d,q,r,B,H,M=3,20,12,2475,2063,100000,10**9
f=lambda c:Q(q-1,M+c)+Q(1,M+c+1)
g=lambda c:Q(H*q,H*M+c)
L=Q(k*(r-1),B)
FR=f(1+L);FD=g(1)
HR=(Q(q-1,(M+1+L)**2)+Q(1,(M+2+L)**2))/B
HD=Q(H*q,(H*M+1)**2)
kappa=k*d*HR
Delta=d*(FR+(k-1)*FD)
u=k*d*f(k)
s=d*(f(1+Q(k*r,B))+(k-1)*g(r+1))
checks={
    'query_regular_one_real_strictly_best':FR<FD,
    'query_singleton_real_M_below_Delta':Q(1,M+1+L)<Delta,
    'query_singleton_real_Mplus1_below_Delta':Q(1,M+2+L)<Delta,
    'query_singleton_dummy_below_Delta':Q(1,H*M+1)<Delta,
    'gradient_three_real_strictly_best':HR>HD,
    'gradient_singleton_real_M_below_kappa':Q(1,B*(M+1+L)**2)<kappa,
    'gradient_singleton_real_Mplus1_below_kappa':Q(1,B*(M+2+L)**2)<kappa,
    'gradient_singleton_dummy_below_kappa':Q(1,(H*M+1)**2)<kappa,
    'strict_Delta_above_s':Delta>s,
    'strict_s_above_actual_u':s>u,
    'oldPB_greedy_scalar_G':g(r)>2*f(1)-f(2),
    'oldPB_punish_scalar_P':f(10)+(d-1)*f(1)+d*(k-1)*g(r)>d*(f(2)+(k-1)*g(1)),
    'oldPB_fill_scalar_F':k*f(k)>f(10)+(k-1)*g(1),
    'oldPB_singleton_strictly_dominated':Q(d*q,M+r+1)>Q(1,M+1),
    'oldPB_tail_no_hot_revisit':r-k<2*(B-k),
}
rows=[]
for j in (0,1,2,3):
    mass=r-j-1
    theta=Q(k)*(L-j)/mass
    hot=theta/k
    outside=(k-theta)/(B-k)
    row={'real_prefix_copies':j,'opponent_mass':mass,'theta':str(theta),
         'hot_marginal':str(hot),'outside_marginal':str(outside),
         'hot_total_load':str(j+mass*hot),'outside_total_load':str(mass*outside),
         'mixture_probability_legal':0<=theta<=1,
         'enough_distinct_outside_blocks':B-k>=k,
         'total_real_mass_exact':k*hot+(B-k)*outside==k,
         'all_real_loads_match_L':j+mass*hot==L and mass*outside==L}
    assert all(row[z] for z in ['mixture_probability_legal','enough_distinct_outside_blocks','total_real_mass_exact','all_real_loads_match_L'])
    rows.append(row)
assert all(checks.values()),checks
assert Delta-u==Q(253635774167992828702040109522630428194,231302667020810055653950767176470257283490990439844779)
assert s-u==Q(655518746053822970420433555247437051305,604541061548383275389777051408169916255944671102717364)
result={'status':'all exact scalar checks passed; conditional on cited oldPB complete-SPE theorem',
        'author_audit_imported':False,'parameters':{'k':k,'d':d,'q':q,'r':r,'Q':B,'H':H,'M':M},
        'customers':d*(B*q+(k-1)*H*q),'L':str(L),'Delta':str(Delta),'u':str(u),
        'Delta_minus_u':str(Delta-u),'s_minus_u':str(s-u),
        'F_D_minus_F_R':str(FD-FR),'H_R_minus_H_D':str(HR-HD),
        'checks':checks,'plateau_load_checks':rows,
        'scope':'one exact reused PB background and the existing three actual F decisions; not a root/aggregate/half counterexample'}
(HERE/'independent_pb_fractional_plateau_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'scalar_checks':len(checks),'plateau_rows':len(rows),'L':str(L),'Delta_minus_u':str(Delta-u),'theta_j1':rows[1]['theta']},indent=2))
