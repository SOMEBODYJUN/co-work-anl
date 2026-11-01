"""LP over every possible newly added last-reply topic, for a fixed old point.

The new topic may split old customer types arbitrarily; float discovery only.
"""
from pathlib import Path
import sys,json
from fractions import Fraction as F
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5];sys.path.insert(0,str(ROOT))
from customer_attraction import Instance,CustomerType
primal=json.loads((ROOT/'evidence/certificates/customer_attraction/five_player_indexed_bound.json').read_text())['primal']
D=primal['denominator'];atoms=primal['atoms'];rs=[F(a['mass_numerator'],D) for a in atoms];bs=[[int(x) for x in a['bits']] for a in atoms]
inst=Instance(tuple('ABCDEUVWXY'),tuple(CustomerType(frozenset(i for i,b in enumerate(a['bits']) if b=='1'),a['mass_numerator']) for a in atoms),5)
actual=inst.player_payoffs(tuple(range(5)));scale=lambda x:F(x,D)
epay=scale(actual[4]);dpay=scale(actual[3]);p=[sum(b[:3]) for b in bs]
result=[]
for a in range(10):
 baseline=sum((r*F(b[a],load+b[a]) for b,load,r in zip(bs,p,rs) if b[a]),F(0))
 penalty=[F(b[a],(load+b[a])*(load+b[a]+1)) if b[a] else F(0) for b,load in zip(bs,p)]
 newpay=[F(1,load+b[a]+1) for b,load in zip(bs,p)]
 oldactual=[F(1,load+b[3]+1) for b,load in zip(bs,p)]
 prefix=(0,1,2,a)
 br=max(scale(inst.player_payoffs(prefix+(last,))[-1]) for last in range(10))
 lp=linprog([-float(x) for x in penalty],A_ub=[[float(x) for x in oldactual],[-float(x) for x in newpay]],b_ub=[float(epay),-float(br)],bounds=[(0,float(r)) for r in rs],method='highs')
 out={'deviation':inst.topics[a],'status':lp.message,'actual_D_payoff':str(dpay),'min_deviation_if_one_arbitrary_new_topic_is_best_reply':None if lp.fun is None else float(baseline)+lp.fun,'base':str(baseline),'max_original_last_reply_payoff':str(br)}
 result.append(out);print(json.dumps(out),flush=True)
Path(__file__).with_suffix('.json').write_text(json.dumps({'scope':'float necessary feasibility probe only; omitted exact dual certification','results':result},indent=2)+'\n')
