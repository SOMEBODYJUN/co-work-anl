"""Independent finite checks of seed acceptance and exact expanded policies.
This audits an implementation and does not prove general half-coverage.
"""
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
from types import SimpleNamespace
import numpy as np
import warm_dag_search as w


def check_seed(p,m,clones,q):
    seed,meta=w.initial_vector(p,q,clones)
    captured={}
    def only_check(c,*,integrality,bounds,constraints,options):
        act=constraints.A@seed
        low=np.asarray(constraints.lb);high=np.asarray(constraints.ub)
        lo=np.asarray(bounds.lb);hi=np.asarray(bounds.ub)
        residuals={'row_lower':float(np.maximum(low-act,0).max()),'row_upper':float(np.maximum(act-high,0).max()),'variable_lower':float(np.maximum(lo-seed,0).max()),'variable_upper':float(np.maximum(seed-hi,0).max()),'integrality':float(np.abs(seed[integrality>0]-np.rint(seed[integrality>0])).max())}
        assert max(residuals.values())<1e-12,residuals
        captured.update(residuals)
        return SimpleNamespace(x=seed,fun=float(c@seed),status=0,message='seed only; no optimization')
    w.dag.milp=only_check
    cone,info=w.dag.build(p,q,[0]*((1<<p)-1),fixed_clones=clones)
    assert cone and w.dag.independently_verify(cone,clones)
    return cone,captured


def main():
    records=[];checks=0
    for m in (1,2,3):
        for clones in product(range(2),repeat=3):
            inst=w.instance_from_clones(2,m,clones);solver=w.ExactSPESolver(inst)
            for q in solver.outcomes():
                if not inst.welfare(q):continue
                cone,residual=check_seed(2,m,clones,q)
                checks+=1
                records.append({'players':m,'clones':clones,'root':q,'residuals':residual})
    # An empty theme and identical nonempty themes remain legal labels here.
    for p,m,clones in [(3,2,(0,0,0,1,0,0,0)),(3,3,(0,0,0,0,0,0,1))]:
        inst=w.instance_from_clones(p,m,clones)
        for q in w.ExactSPESolver(inst).outcomes():
            cone,residual=check_seed(p,m,clones,q);checks+=1
            records.append({'players':m,'clones':clones,'root':q,'residuals':residual})
    # Known output unavailable to any count-Markov strategy: warm witness must
    # preserve target-dependent action selection when unfolded.
    source=w.ROOT/'research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/strategy_duality/markov_obstruction_report.json'
    clones=json.loads(source.read_text())['legal_types']
    cone,residual=check_seed(5,3,clones,(1,0,1,1,0))
    nonmarkov=any(len(h)==len(hh) and sorted(h)==sorted(hh) and a!=b for h,a in cone.actions.items() for hh,b in cone.actions.items())
    assert nonmarkov
    rejected=0
    for p,m,clones,q in [(2,2,(0,0,0),(2,0)),(2,2,(1,0,0),(0,2))]:
        try:w.initial_vector(p,q,clones)
        except ValueError:rejected+=1
        else:raise AssertionError('invalid seed accepted')
    result={'scope':'finite warm-seed encoding/whole-model residual/full-policy replay; no universal theorem','positive_finite_cases':checks,'boundary_rejections':rejected,'known_nonmarkov_root_023_full_seed_accepted':True,'same_count_different_action_observed':nonmarkov,'known_nonmarkov_model_residuals':residual,'cases':records}
    Path(__file__).with_name('warm_seed_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='cases'}))

if __name__=='__main__':main()
