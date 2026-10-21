"""Discovery: fixed full-policy cone attack on the uniform actual-deletion cap.
This is a proposed sufficient interface, not Q-CAG-HALF itself.
"""
from pathlib import Path
import importlib.util,json
import numpy as np
from scipy.optimize import linprog
ROOT=Path(__file__).resolve().parents[5]
source=ROOT/'research/workspaces/customer-attraction/R-d28e1c3c70cf4adfbb52398ac7cf4c7b/experiments/dual_cone_menu.py'
spec=importlib.util.spec_from_file_location('old_menu',source)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

def run(name):
 k,n,masks,bits,G,c,z,menu,deletions=module.policy_matrix(name)
 load=sum(bits[a] for a in z)
 f=np.where(load>0,(n+1)/(n*(load+1)),1)
 best=None
 for a in range(k):
  objective=bits[a]*f-c/(n-.5)
  r=linprog(-objective,A_ub=-G,b_ub=np.zeros(len(G)),A_eq=[c],b_eq=[1],bounds=(0,None),method='highs')
  if r.success and (best is None or -r.fun>best['gap']):
   best={'name':name,'n':n,'k':k,'z':z,'query':a,'gap':-r.fun,'weights':{int(T):float(w) for T,w in zip(masks,r.x) if w>1e-9}}
 return best
if __name__=='__main__':
 records=[]
 for name in ['aggregate_theta_failure','individual_security_failure','local_security_increment','root_tax_failure','global_decorrelation_failure','empirical_iid_kernel','root_stationary_kernel']:
  row=run(name);records.append(row);print(json.dumps(row),flush=True)
 Path(__file__).with_name('deletion_probe.json').write_text(json.dumps(records,indent=2))
