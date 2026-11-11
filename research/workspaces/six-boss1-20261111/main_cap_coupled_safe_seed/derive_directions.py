"""Main directly pays CAP-coupled internal SAFE increments, no optimization."""
from pathlib import Path
from itertools import product
from fractions import Fraction as F
import hashlib
import json

P=Path(__file__).resolve().parent;W=P.parent
theta=(F(12425,31104),F(175,432),F(5,12))
atoms=list(product((0,1),repeat=9))
rows=[];directions=[];state_records=[]
base_data=json.loads((W/'source2_joint_internal_safe/sixteen_reweighted_vertex_family.json').read_text())
for s in [F(0),F(9)]:
    a0=25+sum(theta)-s
    for j in range(3,6):
        gamma=tuple(F(1) if k==j else F(1,6*(7-j)*(8-j)) if k<j else F(0) for k in range(3,6))
        states=[]
        for p,c,o in product((0,1),repeat=3):
            anchor=F(5*c,2)+F(24*c,p+5)-s*c/5+F(o,6*(p+4*c+1))
            anchor+=sum(theta[k-3]*F(o,6*(p+(k-2)*c+7-k)) for k in range(3,6))
            for tail in product((0,1),repeat=4):
                load=p+c+sum(tail)
                cost=(a0*c-tail[-1]-sum(theta[k]*tail[k] for k in range(3)))/load if load else F(0)
                cost+=F(sum(tail[:3]),2)+tail[-1]+F(o,6*(p+c+sum(tail[:3])+1))
                cost+=sum(theta[k-3]*F(o,6*(p+c+sum(tail[:k-3])+7-k)) for k in range(3,6))
                rho=cost-anchor;assert rho>=0
                gain=F(c-tail[j-3],load) if load else F(0)
                gain+=sum(gamma[k]*tail[k] for k in range(3))
                gain+=F(o,6*(p+c+sum(tail[:j-3])+7-j))
                gain-=c*sum(gamma)+F(o,6*(p+(j-2)*c+7-j))
                assert rho or gain>=0,(s,j,p,c,o,tail)
                states.append((p,c,o,tail,rho,gain))
        bound=min(rho/(-gain) for p,c,o,t,rho,gain in states if gain<0)
        assert bound>0
        attainers=[]
        for p,c,o,t,rho,gain in states:
            residual=rho+bound*gain;assert residual>=0
            if gain<0 and residual==0:attainers.append({'pco':[p,c,o],'tail':list(t),'base_residual':str(rho),'increment_residual':str(gain)})
            state_records.append({'s':str(s),'internal_source':j,'pco':[p,c,o],'tail':list(t),'rho':str(rho),'derivative':str(gain),'endpoint_residual':str(residual)})
        expected=min(F(3,8)+theta[j-3]/4, (F(14,5)+theta[j-3]-s/5)/3)
        assert bound==expected
        directions.append({'s':str(s),'internal_source':j,'endpoint':str(bound),'cap_increment_per_unit':list(map(str,gamma)),'critical_states':attainers})
        base=next(r for r in base_data if r['name']==f'SOURCE2_MAXIMUM_C_REWEIGHTED_INTERNAL_SAFE_V111_S{int(s)}')
        vec={}
        for h,bits in enumerate(atoms):
            actual=bits[:6];p=actual[0];c=bits[8];o=bits[7]
            u2=F(actual[1],sum(actual)) if sum(actual) else F(0)
            nj=F(o,6*(p+(j-2)*c+7-j))
            value=F(base['a'].get(str(h),'0'))+bound*(u2-nj)
            vec[str(h)]=str(value)
        vec['512']=base['a']['512']
        rows.append({'name':f'MAIN_CAP_COUPLED_SOURCE{j}_S{int(s)}','source':2,'T':'C_maximum',
                     'base_theta':list(map(str,theta)),'s':str(s),'increment_source':j,'increment':str(bound),
                     'raw_source_IC_weight':str(a0+bound),'middle_cap_weights':[str(F(1,2)+bound*g) for g in gamma],
                     'internal_SAFE_weights':[str(theta[k]+(bound if k==j-3 else 0)) for k in range(3)],
                     'a':vec,'rhs':'0','numerical_divisor':'25'})
assert len(state_records)==768 and len(rows)==6
for name,value in [('exact_directions.json',directions),('complete_residuals.json',state_records),('exact_rows.json',rows)]:
    (P/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
r={'owner':'Boss1/Main','status':'DIRECT_REAL_BUDGET_ENDPOINTS_PASS','optimizer_calls':0,
   'independent_direction_checks':6,'complete_hidden_states':768,'full_row_coefficients':3078,
   'endpoints_by_s_and_internal_source':{f"s{r['s']}_j{r['internal_source']}":r['endpoint'] for r in directions},
   'base_family_sha256':hashlib.sha256((W/'source2_joint_internal_safe/sixteen_reweighted_vertex_family.json').read_bytes()).hexdigest(),
   'boundary':'Only six one-coordinate endpoints directly checked. Simultaneous increment polytope is a separate ongoing obligation.'}
(P/'check_result.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(r,ensure_ascii=False))
