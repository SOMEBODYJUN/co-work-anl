"""Recover a small integer point from a frozen floating policy-cone candidate.

This script only discovers a candidate; the independent full-definition audit
is required before asserting a bridge counterexample. Existing outputs are
never overwritten. Integer row reconstruction uses lcm(1,...,m), because
every payoff coefficient is a sum of unit shares with those denominators.
"""
from pathlib import Path
import argparse
import json
import math
import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
import cone_attack as cone
from customer_attraction import Instance
from customer_attraction.certificate import StrategyCertificate


def main():
    ap=argparse.ArgumentParser();ap.add_argument('input',type=Path)
    ap.add_argument('--output',required=True,type=Path)
    ap.add_argument('--seconds',type=float,default=45)
    a=ap.parse_args()
    data=json.loads(a.input.read_text());obj=data['candidate'];ins=Instance.from_dict(obj['instance'])
    captured={};original=cone.linprog
    def capture(*args,**kwargs):
        captured.update(kwargs)
        return original(*args,**kwargs)
    cone.linprog=capture
    result,actual=cone.probe(ins,StrategyCertificate.from_dict(obj['certificate']),
                             tuple(obj['target']))
    support=[j for j,v in enumerate(result.x[:-1]) if v>1e-9]
    A=np.asarray(captured['A_ub']);D=math.lcm(*range(1,ins.players+1))
    assert np.max(np.abs(A*D-np.rint(A*D)))<1e-7
    rows=np.rint(A[:,:-1]*D);upper=-np.rint(A[:,-1]*D)
    r=milp(np.ones(len(support)),integrality=np.ones(len(support)),
           bounds=Bounds(0,np.inf),constraints=LinearConstraint(rows[:,support],-np.inf,upper),
           options={'time_limit':a.seconds})
    if r.x is None:raise RuntimeError(r.message)
    w=np.rint(r.x).astype(int)
    assert np.max(rows[:,support]@w-upper)<1e-8
    out=dict(status='integer_candidate_requires_definition_audit',target=obj['target'],
             actual=actual,weights={str(j+1):int(x) for j,x in zip(support,w) if x},
             certificate=obj['certificate'],unit_customers=int(w.sum()),
             milp_status=int(r.status),milp_message=r.message)
    with a.output.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['weights','certificate']}))


if __name__=='__main__':main()
