"""Independent definition-level check; expands all multiplicities to unit clients.

Imports no game package, search engine, optimizer, or SPE outcome recurrence.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import argparse, hashlib, json

def audit(path):
    raw=path.read_bytes();obj=json.loads(raw);inst=obj['instance'];m=inst['players'];p=len(inst['topics'])
    units=tuple(frozenset(row['topics']) for row in inst['customers'] for _ in range(row['multiplicity']))
    actions={tuple(row['history']):row['action'] for row in obj['strategy']['actions']}
    histories={h for d in range(m) for h in product(range(p),repeat=d)}
    assert len(actions)==len(obj['strategy']['actions']) and set(actions)==histories
    assert all(a in range(p) for a in actions.values())
    terminals={}
    def terminal(h):
        if h not in terminals:terminals[h]=h if len(h)==m else terminal(h+(actions[h],))
        return terminals[h]
    cache={}
    def utility(z,a):
        key=(z,a)
        if key not in cache:cache[key]=sum((F(1,sum(b in B for b in z)) for B in units if a in B),F(0))
        return cache[key]
    def welfare(z):return sum(any(a in B for a in z) for B in units)
    violations=[];strict=ties=0;minimum=None
    for h in sorted(histories,key=lambda h:(len(h),h)):
        a=actions[h];actual=utility(terminal(h),a)
        for b in range(p):
            if b==a:continue
            deviating=utility(terminal(h+(b,)),b);slack=actual-deviating
            strict+=slack>0;ties+=slack==0;minimum=slack if minimum is None else min(minimum,slack)
            if slack<0:violations.append({'history':h,'a':a,'b':b,'actual':str(actual),'deviating':str(deviating)})
    z=terminal(());W=welfare(z);O=max(welfare(J) for J in combinations(range(p),min(m,p)))
    u=utility(z,z[obj['attacked_position']]);q=tuple(z.count(a) for a in range(p))
    assert list(q)==obj['strategy']['terminal_counts'] and W==obj['W'] and O==obj['OPT']
    assert u==F(obj['u']) and F(O,u)==F(obj['ratio'])
    topics=[frozenset(i for i,B in enumerate(units) if a in B) for a in range(p)]
    distinct=set(topics);maximal=[A for A in distinct if not any(A<B for B in distinct)]
    assert not violations
    return {'source':str(path),'source_sha256':hashlib.sha256(raw).hexdigest(),
            'method':'standard-library Fraction; explicitly expanded unit clients; all ordered histories',
            'unit_customers':len(units),'players':m,'topics':p,'distinct_coverages':len(distinct),
            'maximal_coverages':len(maximal),'decision_histories':len(histories),
            'nonself_deviations':len(histories)*(p-1),'strict':strict,'ties':ties,
            'minimum_slack':str(minimum),'violations':violations,'full_history_SPE':True,
            'path':z,'payoffs':[str(utility(z,a)) for a in z],'W':W,'OPT':O,
            'individual_ratio':str(F(O,u)),'weak_floor_gap':str((2*m-1)*u-O),'half_gap':2*W-O}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('source',nargs='+',type=Path);ap.add_argument('--output',required=True,type=Path)
    args=ap.parse_args();report=[audit(p) for p in args.source]
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps([{k:v for k,v in r.items() if k not in ['source','source_sha256','violations']} for r in report],indent=2))
