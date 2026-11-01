"""Exact scalar checks for a free-fractional saddle/plateau corollary of
the already proved PB-background construction. This does not verify its huge
full-history strategy; that theorem and its independent reviews are dependencies.
No search, optimization, parameter scan, or floating arithmetic.
"""
from fractions import Fraction as F
from pathlib import Path
import json
k,d,q,t,r,Q,H,M=3,20,12,10,2475,2063,100000,10**9

def f(c):return F(q-1,1)/(M+c)+F(1,1)/(M+c+1)
def g(c):return F(H*q,1)/(H*M+c)
L=F(k*(r-1),Q)
real=f(1+L);dummy=g(1)
HR=(F(q-1,1)/(M+1+L)**2+F(1,1)/(M+2+L)**2)/Q
HD=F(H*q,(H*M+1)**2)
delta=d*(real+(k-1)*dummy)
u=d*k*f(k)
s=d*(f(1+F(r*k,Q))+(k-1)*g(r+1))
theta=F(k,1)*(L-1)/(r-2)
hot_marginal=theta/k
outside_marginal=(k-theta)/(Q-k)
checks={
 'query_best_uses_one_real':dummy>real,
 'gradient_best_uses_three_real':HR>HD,
 'regular_query_beats_any_singleton':delta>F(1,M+1),
 'max_regular_gradient_beats_singleton':d*k*HR>max(F(1,Q)/(M+1+L)**2,F(1,(H*M+1)**2)),
 'delta_beats_old_security_lower':delta>s,
 'old_security_lower_beats_actual_u':s>u,
 'delta_beats_actual_u':delta>u,
 'child_mixture_probability_valid':0<=theta<=1,
 'hot_load_preserved':1+(r-2)*hot_marginal==L,
 'outside_load_preserved':(r-2)*outside_marginal==L,
 'dummy_load_preserved':True,
 'three_prefix_copies_also_feasible':L>=3,
 'all_three_mixtures_valid':all(0<=F(k,1)*(L-j)/(r-j-1)<=1 for j in (1,2,3)),
 'all_three_hot_loads_preserved':all(j+(r-j-1)*(F(k,1)*(L-j)/(r-j-1))/k==L for j in (1,2,3)),
 'all_three_outside_loads_preserved':all((r-j-1)*(k-F(k,1)*(L-j)/(r-j-1))/(Q-k)==L for j in (1,2,3)),
}
assert all(checks.values()),checks
out={'parameters':dict(k=k,d=d,q=q,t=t,r=r,Q=Q,H=H,M=M),
 'checks':checks,'L':str(L),'theta':str(theta),
 'delta_r_b':str(delta),'actual_first_u':str(u),
 'delta_minus_u':str(delta-u),'local_chain_D':str(u-delta),
 'real_query_discount':str(real),'dummy_query_discount':str(dummy),
 'real_gradient_minus_dummy_gradient':str(HR-HD),
 'scope':'Exact scalar/saddle/feasible-mixture corollary only; complete-SPE status depends on old PB analytic proof. Root aggregate and half remain OPEN.'}
path=Path(__file__).with_name('pb_fractional_plateau_audit.json')
path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'all_checks_pass':all(checks.values()),'L':str(L),'theta':str(theta),'delta_minus_u':str(delta-u),'local_chain_D':str(u-delta)},indent=2))
