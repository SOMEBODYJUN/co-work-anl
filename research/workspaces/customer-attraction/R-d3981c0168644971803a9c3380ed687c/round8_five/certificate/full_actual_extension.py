"""One common actual-HQR branch, all 747 rows at once, frozen old support.

This is an intermediate exact source for testing the other real history and
shared-catalog compatibility. No restricted optimum is a welfare theorem.
"""
from pathlib import Path
from fractions import Fraction as F
import json,sys,hashlib,time
import numpy as np
from scipy.optimize import linprog
from scipy.linalg import qr
import two_real_weighted_branches as two
cm=two.cm
sys.path.insert(0,str(cm.HERE.parent/'maxroot'))
import actual13_payment_pricing as payment
from exact_cross_primal import evaluator
from frozen_pair_reoptimization import fraction_solve


def run():
    start=time.time();pointpath=cm.HERE/'exact_current_source_actual13_v1.json';point=json.loads(pointpath.read_text());atoms=point['atoms'];N=len(atoms)
    all_source_rows=json.loads((cm.HERE.parent/'maxroot/actual13_payment_discovery.json').read_text())['row_names']
    # The projected A13 row follows from the same explicit HQR rows and is
    # redundant here. Removing it avoids a second independent hidden state.
    sourcerows=[n for n in all_source_rows if n!=payment.NAME]
    U=evaluator();U.__class__=payment.Universe;U.specs=cm.mp.menu_specs();U.proj_h=None
    old=[];fresh=[];w=[];o=[]
    for a in atoms:
        rr=U.atom_rows(a);assert set(rr)==set(all_source_rows);old.append([rr[n] for n in sourcerows])
        fresh.append([two.rows(a,s,'actual') for s in two.STATES]);w.append(int(any(map(int,a['bits'][:5]))));o.append(int(any(a['AB_hist'][4:])))
    newnames=list(fresh[0][0]);names=sourcerows+[f'actual-extension:{n}' for n in newnames]
    oldmat=np.repeat(np.array(old,dtype=float).T,8,axis=1)
    newmat=np.array([[float(fresh[j][s][n]) for j in range(N) for s in range(8)] for n in newnames])
    mat=np.vstack([oldmat,newmat]);ww=np.repeat(w,8);oo=np.repeat(o,8)
    lp=linprog(-oo.astype(float),A_ub=-mat,b_ub=np.zeros(len(names)),A_eq=[ww],b_eq=[1.],bounds=(0,None),method='highs');assert lp.success,lp.message
    beta=-float(lp.fun)
    report={'scope':'Frozen old support with the entire actual-third HQR extension. Only an intermediate necessary-row source, no full-type optimum, original game, or half claim.',
            'source_exact_point_sha256':hashlib.sha256(pointpath.read_bytes()).hexdigest(),'old_types':N,'hidden_states_per_type':8,
            'old_rows':len(sourcerows),'new_actual_rows':len(newnames),'restricted_beta_float':beta}
    print(json.dumps(report),flush=True)
    if beta<=2+1e-7:
        report['status']='Restricted support does not furnish an above-two extension point; full-type pricing would be needed for any bound.'
        (cm.HERE/'full_actual_extension_diagnostic_v2.json').write_text(json.dumps(report,indent=2)+'\n')
        clean_fields=('bits','AB_hist','AE_hist','second_hist','menus_lh','max_bits')
        discovered=[dict({k:a[k] for k in clean_fields},actual_HQR_bits=''.join(map(str,s))) for a in atoms for s in two.STATES]
        report.update({'row_names':names,'atoms':discovered,'primal_float':lp.x.tolist(),
                       'dual_beta_float':beta,'dual_multipliers_float':{n:float(-v) for n,v in zip(names,lp.ineqlin.marginals) if -v>1e-10},
                       'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()})
        (cm.HERE/'full_actual_extension_discovery.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps({'saved_discovery':'full_actual_extension_discovery.json','rows':len(names),'columns':len(discovered),'restricted_beta_float':beta}),flush=True)
        return
    support=list(np.where(lp.x>1e-8)[0]);active=list(np.where(abs(mat@lp.x)<1e-7)[0])
    def col(i,r):
        j,s=divmod(i,8)
        return old[j][r] if r<len(sourcerows) else fresh[j][s][newnames[r-len(sourcerows)]]
    eq=[[int(ww[i]) for i in support]]+[[col(i,r) for i in support] for r in active]
    _,r,piv=qr(np.array(eq,dtype=float).T,pivoting=True,mode='economic');rank=np.count_nonzero(abs(np.diag(r))>1e-8)
    assert rank==len(support),(rank,len(support));picks=list(piv[:len(support)])
    mass=fraction_solve([eq[j] for j in picks],[int(j==0) for j in picks]);assert min(mass)>0
    slacks={n:sum((m*col(i,r) for i,m in zip(support,mass)),F(0)) for r,n in enumerate(names)};assert min(slacks.values())>=0
    W=sum(m*int(ww[i]) for i,m in zip(support,mass));O=sum(m*int(oo[i]) for i,m in zip(support,mass));assert W==1 and O>2
    lifted=[];projected={}
    for i,m in zip(support,mass):
        j,s=divmod(i,8);a=atoms[j]
        lifted.append(dict(a,actual_HQR_bits=''.join(map(str,two.STATES[s])),exact_mass=str(m)))
        if j not in projected:projected[j]=[a,F(0)]
        projected[j][1]+=m
    source={'scope':'Exact above-two necessary-row source with an explicit feasible lift of all 747 actual-HQR rows. Not an original game/SPE or a full-type optimum.',
            'source_rows':len(names),'welfare':str(W),'comparison_cover':str(O),'gap_above_two':str(O-2),
            'positive_projected_atoms':len(projected),'positive_extended_atoms':len(lifted),
            'minimum_exact_slack':str(min(slacks.values())),'atoms':[dict(a,exact_mass=str(m)) for a,m in projected.values()],
            'actual_HQR_lift':lifted,'row_slacks':{n:str(v) for n,v in slacks.items()},
            'source_point_sha256':hashlib.sha256(pointpath.read_bytes()).hexdigest(),
            'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'seconds':time.time()-start}
    out=cm.HERE/'exact_full_actual_extension_source.json';out.write_text(json.dumps(source,indent=2)+'\n')
    print(json.dumps({k:v for k,v in source.items() if k not in ('atoms','actual_HQR_lift','row_slacks')},indent=2),flush=True)


if __name__=='__main__':run()
