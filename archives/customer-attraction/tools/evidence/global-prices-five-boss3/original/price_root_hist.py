"""Exhaustive full root-histogram pricing for the frozen 38-atom completion LP.

Every histogram with five indices and the required T count is enumerated.
Pricing uses floating duals, so negative/positive margins are proposals only.
The chosen histogram coefficients are replayed using Fraction definitions.
"""
from pathlib import Path
from itertools import product
from fractions import Fraction as F
import numpy as np,json,time,argparse,sys

HERE=Path(__file__).resolve().parent;SIB=HERE.parent/'next_credible';sys.path.insert(0,str(SIB))
CELL=np.array(list(product((0,1),repeat=5)),int);T=CELL[:,0];V=CELL[:,1:]
LOAD=CELL.sum(axis=1);PAY=V/np.maximum(LOAD[:,None],1)
DEN=np.array([1/(T+V[:,:j].sum(axis=1)+4-j) for j in range(4)]).T

def compositions(n,k):
 if k==1:yield(n,);return
 for x in range(n+1):
  for tail in compositions(n-x,k-1):yield(x,)+tail

def histograms(d):
 a=np.array(list(compositions(5-d,16)),np.int8);b=np.array(list(compositions(d,16)),np.int8)
 return np.c_[np.repeat(a,len(b),axis=0),np.tile(b,(len(a),1))]

def compact(h):
 return [(int(T[i]),tuple(map(int,V[i])),int(n)) for i,n in enumerate(h) if n]

def direct_off(h,j,k):
 count=sum(n*v[k] for t,v,n in h);out=F()
 for t,v,n in h:
  load=t+sum(v);den=t+sum(v[:j])+4-j
  u=F(v[j],load) if v[j] else F()
  out+=F(n,5)*(4*u-F(count-v[k],den))
 return out

def run(path):
 start=time.time();data=json.loads(path.read_text())
 env={'__file__':str(SIB/'root_menu_completion.py')};src=(SIB/'root_menu_completion.py').read_text()
 exec(compile(src.split('# Maximize a common margin')[0],'<root primitive definitions>','exec'),env)
 base=env['A'];var=env['variables'];old=env['old'];ds=list(map(int,env['d']))
 lam=np.array(data['dual_rows']);nu=np.array(data['dual_equalities']);assert len(lam)==len(base)+16 and len(nu)==len(old)
 assert np.min(lam)>-1e-8
 primitive=lam[:len(base)]@base;offlambda=lam[len(base):].reshape(4,4)
 offlin=4*PAY@offlambda.sum(axis=1)+np.einsum('ij,jk,ik->i',DEN,offlambda,V)
 cid={(a,t,tuple(v)):i for i,(a,t,v) in enumerate(var)}
 results=[];checked=0;gmax=-np.inf
 for d in sorted(set(ds)):
  H=histograms(d);counts=H@V;denoms=H@DEN
  quad=np.einsum('ij,jk,ik->i',denoms,offlambda,counts)
  for a in [i for i,x in enumerate(ds) if x==d]:
   coeff=np.array([primitive[cid[a,int(t),tuple(map(int,v))]] if (a,int(t),tuple(map(int,v))) in cid else 0. for t,v in zip(T,V)])
   scores=(H@(coeff+offlin)-quad)/5+nu[a]
   idx=int(np.argmax(scores));h=compact(H[idx]);score=float(scores[idx]);gmax=max(gmax,score)
   # Independently recompute the selected 16 off-row entries, with no vector
   # expression and no use of the sibling off(h,j,k) implementation.
   primitive_col=sum((n/5*base[:,cid[a,t,tuple(v)]] for t,v,n in h),np.zeros(len(base)))
   off_col=np.array([float(direct_off(h,j,k)) for j in range(4) for k in range(4)])
   replay=float(np.dot(lam,np.r_[primitive_col,off_col])+nu[a]);assert abs(replay-score)<1e-8,(a,replay,score)
   checked+=len(H);results.append({'atom':a,'d':d,'histogram_count':len(H),'maximum_dual_violation':score,'histogram':h})
  print(json.dumps({'d':d,'histograms_per_atom':len(H),'maximum_violation_so_far':gmax,'elapsed':time.time()-start}),flush=True)
 return {'scope':'full-domain floating pricing of the specified root-histogram necessary completion LP; no SPE claim','source':str(path),'columns_in_source':data['columns'],'rows':len(lam),'atoms':len(old),'enumerated_atom_histograms':checked,'maximum_dual_violation':gmax,'positive_columns':[x for x in results if x['maximum_dual_violation']>1e-8],'best_by_atom':results,'elapsed_seconds':time.time()-start}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--input',default=str(SIB/'root_full_hist_completion.json'));p.add_argument('--output',default=str(Path(__file__).with_suffix('.json')));args=p.parse_args()
 report=run(Path(args.input));Path(args.output).write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k not in ('positive_columns','best_by_atom')},indent=2))
