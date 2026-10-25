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
def run(iterations=3,universe_class=None,source_name='indexed_hinge_discovery.json',target_name='indexed_hinge_fullpricing.json',max_new_columns=100,per_state_batch=12,target_beta=None):
    U=(universe_class or ip.Universe)();target=HERE/target_name;source=target if target.exists() else HERE/source_name;src=json.loads(source.read_text());atoms=[];cols=[];keys=set();ws=[];os=[]
    def add(a):
        key=cm.mp.atom_key(a)+(a['max_bits'],)
        if key in keys:return 0
        rr=U.atom_rows(a);assert set(rr)==set(U.names);keys.add(key);atoms.append(a);cols.append([float(rr[n]) for n in U.names]);ws.append(int(any(map(int,a['bits'][:5]))));os.append(int(any(a['AB_hist'][4:])));return 1
    for a in src['atoms']:add(a)
    history=[]
    for iteration in range(iterations):
        mat=np.asarray(cols).T;lp=linprog(-np.array(os,float),A_ub=-mat,b_ub=np.zeros(len(U.names)),A_eq=[ws],b_eq=[1.],bounds=(0,None),method='highs');assert lp.success,lp.message
        beta=float(-lp.fun);lam=-lp.ineqlin.marginals;pricing_beta=beta
        if target_beta is not None and beta<=target_beta+1e-8:
            costs=np.maximum(1.,np.max(np.abs(mat),axis=1))
            dd=linprog(costs,A_ub=mat.T,b_ub=target_beta*np.array(ws)-np.array(os),bounds=(0,None),method='highs')
            assert dd.success,dd.message
            lam=dd.x;pricing_beta=float(target_beta)
        print(json.dumps({'iteration':iteration,'columns':len(atoms),'restricted_beta':beta,'certificate_target_beta':pricing_beta}),flush=True)
        states=[];new=[]
        if beta<=2+1e-7:
            modes=U.pricing_modes() if hasattr(U,'pricing_modes') else [None]
            for mode in modes:
                if hasattr(U,'set_pricing_mode'):U.set_pricing_mode(mode)
                for state in range(32):
                    begin=time.time();U.active_max=state
                    minimum,candidates,contexts=super(cm.Universe,U).price(lam,pricing_beta,batch=per_state_batch)
                    new.extend(candidates);rec={'projection_mode':mode,'maximum_state':state,'minimum_scaled_residual':float(minimum),'contexts':contexts,'seconds':time.time()-begin};states.append(rec);print(json.dumps(rec),flush=True)
            if hasattr(U,'set_pricing_mode'):U.set_pricing_mode(None)
        U.active_max=None;new.sort(key=lambda z:z[0]);count=sum(add(a) for _,a in new[:max_new_columns])
        rec={'iteration':iteration,'restricted_beta':beta,'certificate_target_beta':pricing_beta,'new_columns':count,'state_reports':states};history.append(rec)
        report={'scope':__doc__,'row_names':U.names,'atoms':atoms,'primal_float':lp.x.tolist()+[0.]*count,'primal_beta_float':beta,'dual_beta_float':pricing_beta,'dual_multipliers_float':{n:float(w) for n,w in zip(U.names,lam) if w>1e-10},'history':history,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()};target.write_text(json.dumps(report,indent=2)+'\n')
        if beta>2+1e-7 or not count:break
if __name__=='__main__':run()
