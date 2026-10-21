import argparse,json
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

def run(m,i):
 cols=[(mask,d) for mask in range(1<<m) for d in range(m+1) if mask or d]
 actual=np.array([[(mask>>j)&1 for mask,d in cols] for j in range(m)])
 c=actual.sum(axis=0);pays=np.divide(actual,c,out=np.zeros(actual.shape),where=c>0)
 d=np.array([d for mask,d in cols]);o=(d>0);w=(c>0);rows=[]
 for j in range(m):
  b=actual[:j].sum(axis=0);r=m-j
  for a in range(m):rows.append(actual[a]/(b+r)-pays[j])
  rows.append(d/m/(b+r)-pays[j])
 target=o.astype(float)-w
 ans=linprog(-target,A_ub=np.array(rows),b_ub=np.zeros(len(rows)),A_eq=pays[i].reshape((1,-1)),b_eq=[1],bounds=(0,None),method='highs')
 return {'m':m,'position':i+1,'success':ans.success,'message':ans.message,'max_gap_per_payoff':float(-ans.fun) if ans.success else None,'weights':{str(cols[n]):float(v) for n,v in enumerate(ans.x) if v>1e-8} if ans.success else {}}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--players',type=int,default=5);p.add_argument('--output',required=True);args=p.parse_args();data=[run(args.players,i) for i in range(args.players)];Path(args.output).write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data,indent=2))
