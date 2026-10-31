"""Exact combinatorial/input checks only; no solver or candidate-generation call."""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import json,hashlib
H=Path(__file__).resolve().parent
def main():
    manifest=json.loads((H/'primary-manifest.json').read_text());rows=[]
    for r in manifest['sources']:
        if not r['path'].endswith('.json'):continue
        d=json.loads((H/'original'/r['path']).read_text())
        q=tuple(d['root']);p=len(q);m=sum(q);a=d['tested_topic'];J=tuple(d['portfolio'])
        assert all(x>=0 for x in q)and q[a]>0 and len(J)==m and len(set(J))==len(J)and all(0<=b<p for b in J)
        n=(1<<p)-1;Y=comb(m+2*p-1,2*p-1);Z=p*comb(m+2*p-2,2*p-1);T=comb(m+p-1,p);L=comb(m+p-1,p-1)
        binary=Y+2*Z;variables=n+T+binary;constraints=2+p+Y-L+4*Z+p*T
        meta=d['milp'];assert(meta['variables'],meta['binary'],meta['rows'])==(variables,binary,constraints)
        objective=[]
        for mask in range(1,1<<p):
            o=F(any(mask>>b&1 for b in J));w=F(any((mask>>b&1)and c for b,c in enumerate(q)))
            u=F(1,sum(c for b,c in enumerate(q)if mask>>b&1))if mask>>a&1 else F(0)
            objective.append(o-w-m*u)
        assert objective[-1]==-1
        assert d['exact_candidate']is None and d['universal_bound_proved']is False and meta['floating_bound_not_a_certificate']is True and meta['floating_value']is None
        rows.append(dict(id=r['id'],file=Path(r['path']).name,m=m,p=p,root=q,tested_topic=a,portfolio=J,nonempty_interest_types=n,y_variables=Y,z_variables=Z,x_variables=Z,threshold_variables=T,binary_variables=binary,total_variables=variables,total_constraints=constraints,frozen_status=meta['status'],frozen_milp_seconds=meta['seconds'],exact_objective_coefficients=list(map(str,objective)),all_interest_feasible_SPE_objective='-1',scope='Combinatorial model dimensions and exact coefficient construction; not a MILP infeasibility certificate.'))
    assert len(rows)==4 and sorted(x['frozen_status']for x in rows)==[1,1,2,2]
    out=dict(status='pass',original_main_executions=0,solver_calls=0,cases=rows,scope='Fixed valid distinct portfolios only; exact structural check does not certify floating infeasible/time-limit results or universal weak budget.')
    (H/'frozen-model-structure-check.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(dict(status='pass',cases=4,solver_calls=0,dimensions=[(x['m'],x['p'],x['total_variables'],x['binary_variables'],x['total_constraints'])for x in rows]),indent=2))
if __name__=='__main__':main()
