import itertools,json,runpy
from pathlib import Path
import numpy as np
from scipy.optimize import linprog
D=runpy.run_path('research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/round3_boss/cone_opportunity_attack.py');policies=D['policies'];prepare=D['prepare']
out=Path('research/workspaces/customer-attraction/R-c9208ba36bb54d1f9542d98da96fa009/early_opportunity/canonical_strong.json');records=[]
for source in sorted(Path('evidence/certificates/customer_attraction').glob('*.json')):
 for label,cert in policies(json.loads(source.read_text()),str(source)):
  data=prepare(cert)
  if data is None:continue
  k,m,masks,member,actions,term,root,path,pay,rows,w=data;n=len(masks);rows=np.unique(rows,axis=0);best={'value':-1e99}
  for comp in itertools.combinations(range(k),min(k,m)):
   o=(member[list(comp)].sum(axis=0)>0).astype(float)
   for a in sorted(set(path)):
    target=o-w-(m-1)*pay(root,a)
    ans=linprog(-target,A_ub=rows,b_ub=np.zeros(len(rows)),A_eq=np.ones((1,n)),b_eq=[1],bounds=(0,None),method='highs')
    if ans.success and -ans.fun>best['value']+1e-10:best={'value':float(-ans.fun),'comparison':comp,'target_action':a,'root':root,'path':path,'weights':{str(mask):float(v) for mask,v in zip(masks,ans.x) if v>1e-9},'cert':cert}
  best['label']=label;records.append(best);print(json.dumps({a:b for a,b in best.items() if a not in ['weights','cert']}),flush=True);out.write_text(json.dumps({'scope':'numerical canonical complete strategy cones; stronger (m-1) coefficient','records':records},indent=2)+'\n')
