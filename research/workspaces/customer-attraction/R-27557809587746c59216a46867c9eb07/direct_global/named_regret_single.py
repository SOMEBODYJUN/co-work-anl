import itertools,pathlib,json,importlib.util,functools,numpy as np
from scipy.optimize import linprog
HERE=pathlib.Path(__file__).parent
spec=importlib.util.spec_from_file_location('scan',HERE/'floor_scan.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
paths=['fractional_actual_load_failure','individual_security_failure','root_tax_failure','coverage_opportunity_failure','residual_counterexample','prefix_balance_failure','worst_pne_welfare_failure','worst_cce_welfare_failure','local_security_increment','aggregate_theta_failure']
best=10
for name in paths:
 path=pathlib.Path('evidence/certificates/customer_attraction')/(name+'.json')
 try:
  obj=json.loads(path.read_text());obj=obj.get('strategy',obj);acts={tuple(x['history']):x['action'] for x in obj['actions']}
 except Exception as e:print('SKIP',name,str(e));continue
 p=max(max(acts.values()),max(max(h,default=-1) for h in acts))+1;n=max(map(len,acts))+1
 if p**(n-1)>100000:continue
 f=mod.Fast(p,n)
 @functools.lru_cache(None)
 def terminal(h):
  if len(h)==n:return f.ids[tuple(h.count(a) for a in range(p))]
  return terminal(h+(acts[h],))
 target=terminal(());gamma=np.array([f.coefs[terminal(h),a]-f.coefs[terminal(h+(b,)),b] for h,a in acts.items() for b in range(p) if a!=b]);loads=f.den[target];covered=(loads>0).astype(float)
 gc=covered/(1+(n-1)/n*loads);F=f.M.T*np.where(loads>0,(n+1)/(loads+1),n)
 vals=[]
 for incumbent,a in itertools.product(np.flatnonzero(f.C[target]),range(p)):
  objective=covered+f.coefs[target,incumbent]-F[a]
  out=linprog(objective,A_ub=-gamma,b_ub=np.zeros(len(gamma)),A_eq=covered[None,:],b_eq=[1],bounds=(0,None),method='highs')
  if out.success:vals.append(out.fun)
  if out.success and out.fun<best-1e-8:
   best=out.fun;print('BEST',name,p,n,a,out.fun,flush=True)
   (HERE/'named_regret_single_best.json').write_text(json.dumps(dict(name=name,p=p,n=n,weights=out.x.tolist(),target=f.C[target].tolist(),a=a,slack=best,policy=[dict(h=h,a=v) for h,v in acts.items()])))
  if best<-1e-7:print('BRIDGE FAIL');raise SystemExit
 print(name,p,n,'min',min(vals) if vals else None,flush=True)
