"""Full type separation of the matched-indexed hinge candidate.

Reports every exact allowed maximum-path state; all histogram contexts are
maximized, not sampled. Floating discovery requires later rational recovery.
"""
from pathlib import Path
import json,time,hashlib
import numpy as np
from scipy.optimize import linprog
import indexed_hinge_pricing as ip
cm=ip.cm;HERE=Path(__file__).resolve().parent
def run(iterations=3,universe_class=None,source_name='indexed_hinge_discovery.json',target_name='indexed_hinge_fullpricing.json'):
    U=(universe_class or ip.Universe)();target=HERE/target_name;source=target if target.exists() else HERE/source_name;src=json.loads(source.read_text());atoms=[];cols=[];keys=set();ws=[];os=[]
    def add(a):
        key=cm.mp.atom_key(a)+(a['max_bits'],)
        if key in keys:return 0
        rr=U.atom_rows(a);assert set(rr)==set(U.names);keys.add(key);atoms.append(a);cols.append([float(rr[n]) for n in U.names]);ws.append(int(any(map(int,a['bits'][:5]))));os.append(int(any(a['AB_hist'][4:])));return 1
    for a in src['atoms']:add(a)
    history=[]
    for iteration in range(iterations):
        mat=np.asarray(cols).T;lp=linprog(-np.array(os,float),A_ub=-mat,b_ub=np.zeros(len(U.names)),A_eq=[ws],b_eq=[1.],bounds=(0,None),method='highs');assert lp.success,lp.message
        beta=float(-lp.fun);lam=-lp.ineqlin.marginals;print(json.dumps({'iteration':iteration,'columns':len(atoms),'restricted_beta':beta}),flush=True)
        states=[];new=[]
        if beta<=2+1e-7:
            for state in range(32):
                begin=time.time();U.active_max=state
                minimum,candidates,contexts=super(cm.Universe,U).price(lam,beta,batch=12)
                new.extend(candidates);rec={'maximum_state':state,'minimum_scaled_residual':float(minimum),'contexts':contexts,'seconds':time.time()-begin};states.append(rec);print(json.dumps(rec),flush=True)
        U.active_max=None;new.sort(key=lambda z:z[0]);count=sum(add(a) for _,a in new[:100])
        rec={'iteration':iteration,'restricted_beta':beta,'new_columns':count,'state_reports':states};history.append(rec)
        report={'scope':__doc__,'row_names':U.names,'atoms':atoms,'primal_float':lp.x.tolist()+[0.]*count,'dual_beta_float':beta,'dual_multipliers_float':{n:float(w) for n,w in zip(U.names,lam) if w>1e-10},'history':history,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()};target.write_text(json.dumps(report,indent=2)+'\n')
        if beta>2+1e-7 or not count:break
if __name__=='__main__':run()
