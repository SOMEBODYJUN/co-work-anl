from pathlib import Path
import sys, json
from fractions import Fraction
from itertools import combinations
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
sys.path[:0]=[str(ROOT),str(ROOT/'tests/audits')]
from customer_attraction_strategy_lp import StrategyCone,payoff_row,coverage_row,integer_clones,independently_verify,serializable

def group_policy(p,m):
 from itertools import product
 n=p//2;X=set(range(n));actions={}
 for depth in range(m):
  for h in product(range(p),repeat=depth):
   if not h:a=0
   elif depth==1:a=n if h[0]<n else 0
   else:
    start=0 if h[1]<n else n
    a=next(k for k in range(start,start+n) if k not in h)
   actions[h]=a
 return StrategyCone(p,m,actions)

cone=group_policy(6,3)
for player in range(cone.players):
 h=();path=[]
 for i in range(cone.players):a=cone.actions[h];path.append(a);h=h+(a,)
 own=payoff_row(cone.topics,cone.root,path[player])
 best=None
 for k in range(1,min(cone.topics,cone.players)+1):
  for supp in combinations(range(cone.topics),k):
   obj=coverage_row(cone.topics,supp)
   r=linprog(-np.array(obj,float),A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),A_eq=[np.array(own,float)],b_eq=[1],bounds=(0,None),method='highs')
   if r.success and (best is None or -r.fun>best[0]):best=(-r.fun,supp,r.x)
 print('player',player,'max O/u',best[0],'support',best[1],flush=True)
