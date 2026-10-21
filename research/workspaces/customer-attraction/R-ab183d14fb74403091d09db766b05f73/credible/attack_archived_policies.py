"""Complete fractional-query attack on stored, mechanistically selected SPE cones.

No policy sampling or universal conclusion. New target: B(u_i) <= (m-1)u_i.
"""
from pathlib import Path
from fractions import Fraction as F
import json,sys,numpy as np
from scipy.optimize import linprog
BASE=Path(__file__).resolve().parent
ROOT=next(p for p in BASE.parents if (p/'customer_attraction/__init__.py').is_file())
sys.path[:0]=[str(BASE),str(ROOT),str(ROOT/'tests/audits')]
from fractional_query_vertices import enumerate_vertices
from price_arrangement_attack import exact_export
from customer_attraction import Instance,ExactSPESolver
from customer_attraction_strategy_lp import StrategyCone,payoff_row

files=['coverage_opportunity_failure.json','aggregate_theta_failure.json','root_tax_failure.json','worst_pne_welfare_failure.json','worst_cce_welfare_failure.json','portfolio_matching_failure.json','prefix_balance_failure.json','optimal_last_query_failure.json']
log=[];best=-1e100;selected=None;queries={}
for name in files:
    obj=json.loads((ROOT/'examples/customer_attraction'/name).read_text());game=Instance.from_dict(obj);p=game.topic_count;m=game.players
    if p>5 or m>5:continue
    if p not in queries:queries[p]=enumerate_vertices(p)[0]
    zs=queries[p];I=np.array([[int(mask>>a&1) for a in range(p)] for mask in range(1,1<<p)]);C=np.minimum(1,np.array(zs,float)@I.T);taus=np.array(zs,float).sum(axis=1)
    solver=ExactSPESolver(game)
    # Use each distinct terminal of this archived mechanism, independently rebuilt.
    for q in sorted(solver.outcomes()):
        cert=solver.certificate(q);cone=StrategyCone(p,m,dict(cert.actions));used=[a for a,c in enumerate(q) if c]
        local=None
        for a in used:
            row=np.array(payoff_row(p,q,a),float)
            for j,Z in enumerate(zs):
                gain=C[j]-(m-1+taus[j])*row
                out=linprog(-gain,A_ub=-cone.matrix,b_ub=np.zeros(len(cone.rows)),A_eq=[cone.welfare],b_eq=[1],bounds=(0,None),method='highs')
                if out.success and (local is None or out.fun<local[0].fun):local=(out,a,j)
        out,a,j=local;value=-out.fun
        record={'source':name,'root':q,'attacked_topic':a,'max_gap_per_W_float':value,'queries':len(zs),'rows':len(cone.rows)};log.append(record);print(json.dumps(record),flush=True)
        if value>best+1e-8:
            best=value;selected=exact_export(cone,out.x,a,zs[j])
            if selected is not None:
                gap=F(selected['Bz'])-(m-1)*F(selected['u']);selected['tstar_gap']=str(gap);selected['tstar_gap_per_W']=str(gap/selected['W']);selected['source']=name
        (BASE/'archived_tstar_attack.json').write_text(json.dumps({'scope':'all queries for listed complete archived-mechanism policy cones only','records':log,'best_float':best,'selected':selected,'universal_result':False},indent=2)+'\n')
        if selected and F(selected['tstar_gap'])>0:sys.exit()
