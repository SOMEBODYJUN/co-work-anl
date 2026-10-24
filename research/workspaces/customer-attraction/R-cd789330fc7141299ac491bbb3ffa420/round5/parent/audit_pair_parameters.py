"""Independent exact scalar checks for the stated PB background construction.

This does not enumerate its strategy tree or prove its Greedy/Punish lemmas.
"""
from fractions import Fraction as F
import json
import platform
import hashlib
from pathlib import Path

k,d,q,t,r,Q,H,M = 3,20,12,10,2475,2063,100000,10**9

def f(c):
    return F(q-1,M+c)+F(1,M+c+1)

def g(c):
    return F(H*q,H*M+c)

u = d*k*f(k)
s = d*(f(1+F(r*k,Q))+(k-1)*g(r+1))
checks = dict(G=g(r)-(2*f(1)-f(2)),
              P=f(t)+(d-1)*f(1)+d*(k-1)*g(r)-d*(f(2)+(k-1)*g(1)),
              Fill=k*f(k)-f(t)-(k-1)*g(1),
              safety_gap=s-u,
              singleton=F(d*q,M+r+1)-F(1,M+1))
assert all(value > 0 for value in checks.values())
free = Q-(3+k+d*(t-1))
assert r-1 < 2*free
assert r-(3+d*(t-1)) > Q+k
assert r-3 < 2*(Q-3)
for ell in range(1,k+1):
    assert ell*f(2)+(k-ell)*g(1) <= f(2)+(k-1)*g(1)
    assert f(t)+(ell-1)*f(1)+(k-ell)*g(1) <= f(t)+(k-1)*g(1)
out = dict(status='exact_scalar_checks_passed_not_a_strategy_tree_proof',
           python=platform.python_version(), arithmetic='fractions.Fraction',
           script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           parameters=dict(k=k,d=d,q=q,t=t,r=r,Q=Q,H=H,M=M),
           gaps={name:str(v) for name,v in checks.items()},
           current_profit=str(u), safety_lower_bound=str(s),
           free_blocks_lower_bound=free, punish_steps_upper_bound=d*(t-1),
           unit_customers=d*(Q*q+(k-1)*H*q))
print(json.dumps(out,indent=2))
