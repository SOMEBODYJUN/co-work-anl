"""Independent exact arithmetic for stated PB-extra candidate constants.
No author implementation, game enumeration, parameter search, or proof import.
"""
from fractions import Fraction as F
from pathlib import Path
import json
k,d,q,t,r,Q,H,M = 3,20,12,10,2475,2063,100000,10**9
f = lambda c: F(q-1)/(M+c) + F(1)/(M+c+1)
g = lambda c: F(H*q)/(H*M+c)
L = d*(t-1)
Z = Q-(k+k+L)
u = d*k*f(k)
s = d*(f(F(1)+F(r*k,Q))+(k-1)*g(r+1))
checks = {
 'G': g(r)-(2*f(1)-f(2)),
 'P': f(t)+(d-1)*f(1)+d*(k-1)*g(r)-d*(f(2)+(k-1)*g(1)),
 'F': k*f(k)-(f(t)+(k-1)*g(1)),
 'singleton': F(d*q,M+r+1)-F(1,M+1),
 'g1_minus_f1': g(1)-f(1),
 'g1_minus_f2': g(1)-f(2),
 'S_minus_U': s-u,
}
assert all(v>0 for v in checks.values())
assert r-(k+L)>=Q
assert r<2*Z
assert r-k<2*(Q-k)
assert t>2
out = dict(scope='stated constants only; independent exact scalar checks, not all-history proof',
 constants=dict(k=k,d=d,q=q,t=t,r=r,Q=Q,H=H,M=M),
 customers=d*(Q*q+(k-1)*H*q),
 max_punish_steps=L, max_punish_index=k+L,
 min_future_after_punish_deviation=r-(k+L),
 Q_bound=Q, min_zero_blocks_at_greedy_start=Z,
 r_less_than_twice_min_zeros=2*Z-r,
 actual_greedy_steps=r-k, actual_initial_zero_blocks=Q-k,
 margins={key:dict(exact=str(value),decimal=float(value)) for key,value in checks.items()},
 u=str(u), s=str(s), all_required_scalar_margins_strictly_positive=True,
 proves_all_histories=False, proves_half=False)
p=Path(__file__).with_name('pair_scalar_independent.json')
with p.open('x',encoding='utf-8') as h:json.dump(out,h,ensure_ascii=False,indent=2);h.write('\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
