"""Standard-library direct Fraction check of an exported complete DAG strategy."""
import argparse
from fractions import Fraction
import hashlib
from itertools import combinations,product
import json
from pathlib import Path


def audit(source):
    raw = source.read_bytes()
    report = json.loads(raw)
    if 'instance' in report and 'strategy' in report:
        inst = report['instance']
        m,p = inst['players'],len(inst['topics'])
        clones = [0]*((1<<p)-1)
        for row in inst['customers']:
            mask = sum(1<<a for a in row['topics'])
            if mask:clones[mask-1]+=row['multiplicity']
        point = {'certified':report['full_strategy_verified'],
                 'integer_clones':clones,'strategy':report['strategy'],
                 'welfare':report['W'],'optimal_welfare':report['OPT']}
        expected_counts = point['strategy']['terminal_counts']
    else:
        point = report['exact_candidate']
        m,p = report['milp']['players'],report['milp']['topics']
        expected_counts = report['milp']['root_counts']
    assert point and point['certified']
    clones = tuple(point['integer_clones'])
    assert len(clones)==(1<<p)-1 and all(isinstance(v,int) and v>=0 for v in clones)
    policy = {tuple(x['history']):x['action'] for x in point['strategy']['actions']}
    histories = tuple(h for d in range(m) for h in product(range(p),repeat=d))
    assert len(policy)==len(point['strategy']['actions']) and set(policy)==set(histories)
    assert all(a in range(p) for a in policy.values())
    types = tuple((frozenset(a for a in range(p) if mask&(1<<a)),c)
                  for mask,c in enumerate(clones,1) if c)
    terminals = {}
    def terminal(h):
        if h not in terminals:
            terminals[h] = h if len(h)==m else terminal(h+(policy[h],))
        return terminals[h]
    def utility(path,a):
        return sum((Fraction(c,sum(t in B for t in path)) for B,c in types if a in B),Fraction(0))
    def welfare(path):
        return sum(c for B,c in types if any(a in B for a in path))
    violations = []
    strict = ties = 0
    min_slack = None
    for h in histories:
        a = policy[h]
        actual = utility(terminal(h),a)
        for b in range(p):
            if b==a:continue
            deviation = utility(terminal(h+(b,)),b)
            slack = actual-deviation
            if min_slack is None or slack<min_slack:min_slack=slack
            strict += slack>0
            ties += slack==0
            if slack<0:violations.append((h,a,b,str(actual),str(deviation)))
    path = terminal(())
    q = tuple(path.count(a) for a in range(p))
    assert q == tuple(point['strategy']['terminal_counts']) == tuple(expected_counts)
    W = welfare(path)
    O = max(welfare(J) for J in combinations(range(p),min(p,m)))
    assert W==point['welfare'] and O==point['optimal_welfare']
    payoffs = tuple(utility(path,a) for a in path)
    assert sum(payoffs)==W
    out = {'source':str(source),'source_sha256':hashlib.sha256(raw).hexdigest(),
           'implementation':'independent standard-library Fraction; all complete ordered histories; direct type multiplicities',
           'topics':p,'players':m,'unit_customers':sum(clones),'decision_histories':len(histories),
           'proper_deviation_comparisons':len(histories)*(p-1),
           'strict_comparisons':strict,'tied_comparisons':ties,
           'full_history_SPE':not violations,'violations':violations,
           'minimum_slack':str(min_slack),'actual_path':path,
           'actual_payoffs':list(map(str,payoffs)),'welfare':W,'optimum':O,
           'half_gap':2*W-O,'minimum_weak_individual_gap':str((2*m-1)*min(payoffs)-O)}
    assert not violations
    return out


if __name__=='__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('source',type=Path,nargs='+')
    ap.add_argument('--output',type=Path,required=True)
    args = ap.parse_args()
    results = [audit(source) for source in args.source]
    args.output.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))
