from pathlib import Path
import sys,json
from fractions import Fraction
from itertools import combinations
import numpy as np
from scipy.optimize import linprog
R=Path(__file__).resolve().parents[5];sys.path[:0]=[str(R),str(R/'tests/audits')]
from customer_attraction import *
from customer_attraction_strategy_lp import *
p,m=6,3
o=json.loads((R/'evidence/certificates/customer_attraction/individual_security_failure.json').read_text())
cert=StrategyCertificate.from_dict(o['strategy']);cone=StrategyCone(p,m,dict(cert.actions))
for mult in (m-1,m):
 best=-100;bestrec=None
 for port in combinations(range(p),m):
  obj=tuple(v-w-mult*u for v,w,u in zip(coverage_row(p,port),cone.welfare,payoff_row(p,cone.root,cone.actions[()])))
  rr=linprog(-np.array(obj,float),A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),A_eq=np.array([cone.welfare],float),b_eq=[1],bounds=(0,None),method='highs')
  if not rr.success or -rr.fun<=best+1e-8:continue
  vs=tuple(Fraction(float(x)).limit_denominator(10**6) for x in rr.x)
  if not cone.verify(vs) or dot(cone.welfare,vs)!=1:vs=cone.recover_vertex(rr.x)
  if vs is None:continue
  best=dot(obj,vs);cs=integer_clones(vs);ins=instance_from_clones(p,m,cs);verify_certificate(ins,cert).assert_valid()
  bestrec={'p':p,'m':m,'mult':mult,'objective':str(best),'weights':cs,'path':(0,3,4),'utilities':list(map(str,ins.player_payoffs((0,3,4)))),'welfare':ins.welfare(cone.root),'optimum':ins.optimal_welfare(),'portfolio':port,'strategy':cert.to_dict()}
 print({k:v for k,v in bestrec.items() if k not in ('strategy','weights')},flush=True)
 (Path(__file__).parent/f'fixed_bridge_mult{mult}.json').write_text(json.dumps(bestrec))
