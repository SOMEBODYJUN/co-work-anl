"""Exact scalar checks for the single explicit arbitrary-background PB candidate.
No solver, strategy enumeration, parameter search, or inference of full-history SPE.
The latter is the analytical obligation in pair_attack.md Sections 3--5.
"""
from fractions import Fraction as F
from pathlib import Path
import json
k,d,q,t,r,Q,H,M=3,20,12,10,2475,2063,100000,10**9
f=lambda c:F(q-1,M+c)+F(1,M+c+1)
g=lambda c:F(H*q,H*M+c)
u=d*k*f(k)
s=d*(f(F(1)+F(r*k,Q))+(k-1)*g(r+1))
gaps={
'G_greedy_padding':g(r)-2*f(1)+f(2),
'F_fill_per_segment':k*f(k)-f(t)-(k-1)*g(1),
'P_punisher':f(t)+(d-1)*f(1)+d*(k-1)*g(r)-d*(f(2)+(k-1)*g(1)),
'singleton_strict_inferiority':F(d*q,M+r+1)-F(1,M+1),
'S_security_lower_minus_actual_one_player':s-u,
}
assert all(v>0 for v in gaps.values())
max_punish=d*(t-1)
min_free=Q-2*k-max_punish
max_greedy_after_punish=r-1
min_future_after_punisher_deviation=r-(k+max_punish)
assert max_greedy_after_punish<2*min_free
assert min_future_after_punisher_deviation>Q+k
assert r-k>Q-k and r-k<2*(Q-k)
result={
'candidate':'For every legal background b and complete pure SPE with r>=2 remaining, u1+u2 >= 2*v_(r+1)(b)',
'status':'Strict scalar separation and exact construction checks; analytical full-history proof awaiting independent review',
'parameters':dict(k=k,d=d,q=q,t=t,r=r,Q=Q,H=H,M=M),
'customer_count':d*Q*q+d*(k-1)*H*q,
'actual_one_player':str(u),'security_lower':str(s),
'pair_gap_2u_minus_2security_lower':str(2*(u-s)),
'exact_positive_gaps':{a:str(v) for a,v in gaps.items()},
'count_checks':dict(max_punish=max_punish,min_free=min_free,max_greedy_after_punish=max_greedy_after_punish,min_future_after_punisher_deviation=min_future_after_punisher_deviation),
'scope':'Attacks arbitrary-background PB only. Prefix already covers every customer; no root half counterexample.'}
out=Path(__file__).with_suffix('.json');out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
