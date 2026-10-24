"""Attack the general arbitrary-root half candidate in four existing suffix cones.

Candidate AR-HALF: m>=2 and every positive-depth subgame is SPE, with no
condition on the prescribed root, implies OPT_m<=2W. Finite negative output is
not a proof. This is not an independent fixed-player research task.
"""
from pathlib import Path
import sys, json
from itertools import combinations
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[6]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'tests/audits'))
from customer_attraction_strategy_lp import StrategyCone,payoff_row,serializable
from customer_attraction.model import Instance
import numpy as np

def attack(name):
    ip=ROOT/'examples/customer_attraction'/f'{name}.json'
    cp=ROOT/'evidence/certificates/customer_attraction'/f'{name}.json'
    inst=Instance.from_dict(json.loads(ip.read_text()))
    cert=json.loads(cp.read_text());cert=cert.get('strategy',cert)
    acts={tuple(x['history']):x['action'] for x in cert['actions']}
    p,m=inst.topic_count,inst.players
    best=None;records=[]
    for a in range(p):
        actions=dict(acts);actions[()]=a
        cone=StrategyCone(p,m,actions)
        rows=set()
        for h,b in actions.items():
            if not h:continue
            own=payoff_row(p,cone.terminals[h],b)
            for c in range(p):
                row=tuple(x-y for x,y in zip(own,payoff_row(p,cone.terminals[h+(c,)],c)))
                if any(row):rows.add(row)
        cone.rows=tuple(sorted(rows));cone.matrix=np.array(cone.rows,dtype=float)
        for port in combinations(range(p),min(p,m)):
            r=cone.optimize(port);r['actual_root']=a
            records.append(r)
            if r.get('certified') and (best is None or r['value']>best['value']):best=r
            if r.get('certified') and r['value']>2:
                print('AR-HALF candidate counterexample',name,serializable(r),flush=True)
                return {'source':name,'topics':p,'players':m,'best':best,'records':records}
    print(name,'max',best['value'],'exact',all(r.get('dual_optimal',False) for r in records),flush=True)
    return {'source':name,'topics':p,'players':m,'best':best,'records':records}

if __name__=='__main__':
    out={'candidate':'AR-HALF, every positive-depth SPE plan obeys OPT_m<=2W (m>=2)',
         'scope':'Only four existing fixed suffix policy cones; no general conclusion.',
         'results':[attack(n) for n in ['root_tax_failure','eight_cce_welfare_gap','aggregate_theta_failure','fractional_actual_load_failure']]}
    Path(__file__).with_suffix('.json').write_text(json.dumps(serializable(out),indent=2)+'\n')
