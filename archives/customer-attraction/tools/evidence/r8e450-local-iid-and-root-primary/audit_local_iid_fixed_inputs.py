"""One fixed-input exact reading audit; no original optimizer or SPE search."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal
from itertools import product
from math import comb
import json

ROOT = Path(__file__).resolve().parent
candidate = json.loads((ROOT / 'original/88de1467b66d9908f554/iid_drift_candidate.json').read_text(), parse_float=Decimal)
sigma = {(): 0, (0,): 1, (1,): 0, (0, 0): 1, (0, 1): 0, (1, 0): 1, (1, 1): 0}

def complete(h):
    while len(h) < 3:
        h = h + (sigma[h],)
    return h

def payoff(a, z):
    return F(1, z.count(a))

history_rows = []
strict = ties = 0
for depth in range(3):
    for h in product(range(2), repeat=depth):
        a = sigma[h]
        z = complete(h)
        incumbent = payoff(a, z)
        values = [payoff(t, complete(h + (t,))) for t in range(2)]
        assert all(incumbent >= v for v in values)
        for t, value in enumerate(values):
            if t != a:
                strict += incumbent > value
                ties += incumbent == value
        history_rows.append({'history': list(h), 'prescribed_action': a, 'terminal': list(z),
                             'all_true_query_payoffs': [str(v) for v in values]})

def iid_values(r, prefix, q):
    alpha = []
    for a in range(2):
        b = prefix.count(a)
        t = q[a]
        alpha.append(sum((F(comb(r-1, j)) * t**j * (1-t)**(r-1-j) / (b+1+j) for j in range(r)), F(0)))
    z = r * sum((q[a]*alpha[a] for a in range(2)), F(0))
    assert all(alpha[a] <= z/r for a in range(2))
    assert all(q[a] == 0 or alpha[a] == z/r for a in range(2))
    return {'r': r, 'prefix': list(prefix), 'q': [str(x) for x in q], 'all_pure_query_values': [str(x) for x in alpha], 'Z': str(z)}

root = iid_values(3, (), (F(1,2), F(1,2)))
after_a = iid_values(2, (0,), (F(0), F(1)))
after_ab = iid_values(1, (0,1), (F(1), F(0)))
path = complete(())
profits = [payoff(a,path) for a in path]
zs = [F(root['Z']), F(after_a['Z']), F(after_ab['Z']), F(0)]
debts = [zs[i]-zs[i+1]-profits[i] for i in range(3)]
assert strict == 4 and ties == 3 and path == (0,1,0)
assert debts == [F(1,4), F(-1,2), F(0)] and sum(debts) == F(-1,4)

ins = candidate['instance']
counts = candidate['counts']
types = [(set(c['topics']), c['multiplicity']) for c in ins['customers']]
total = sum(w for t,w in types)
assert ins['players'] == sum(counts) == 5 and len(ins['topics']) == len(counts) == 6
assert len(types) == 16 and all(isinstance(w,int) and w>0 for t,w in types)
assert all(0 in t or 1 in t for t,w in types)
covered = sum(w for t,w in types if any(counts[a] for a in t))
per_topic = [sum((F(w, sum(counts[a] for a in t)) for t,w in types if j in t), F(0)) for j in range(6)]
assert candidate['action'] == 0 and per_topic[0] == F(candidate['u']) == F(211,10)
assert covered == total == 98 and per_topic[1] == F(93,5)
assert sum(counts[a]*per_topic[a] for a in range(6)) == covered
numeric_difference = Decimal(211)/Decimal(10) + candidate['Znext'] - candidate['Z']
out = {
    'scope': 'new fixed-input standard-library audit; not the native probe, SLSQP, randomized search or exact outcome-set solver',
    'singleton_complete_policy': {'actions': history_rows, 'histories': len(history_rows), 'all_comparisons_including_self': 14,
                                  'changed_action_comparisons': 7, 'strict_changed_actions': strict, 'ties_changed_actions': ties,
                                  'actual': list(path), 'profits': [str(v) for v in profits], 'W':2, 'OPT_3':2},
    'singleton_static_KKT_at_specified_distributions': [root, after_a, after_ab],
    'singleton_local_drift': str(profits[0]+zs[1]-zs[0]),
    'singleton_weak_local_slack_using_original_n3': str(profits[0]-F(5,6)*(zs[0]-zs[1])),
    'singleton_actual_path_debts': [str(v) for v in debts],
    'singleton_total_debt': str(sum(debts)),
    'singleton_static_distribution_uniqueness': 'proved analytically in accompanying formal text, not by finite sample checks',
    'saved_six_label_candidate': {'all_top_level_keys': list(candidate), 'trial_recorded': candidate['trial'], 'players':5,'topics':ins['topics'],
        'all_interest_types': [{'topics':sorted(t),'multiplicity':w} for t,w in types], 'customers':total,'counts':counts,
        'action':candidate['action'],'selected_topic_actual_profit':str(per_topic[0]),'other_occupied_topic_actual_profit':str(per_topic[1]),
        'W':covered,'OPT_5':total,'OPT_proof':'Topics 0 and 1 already cover every customer; repetitions fill five slots.',
        'Z_recorded':str(candidate['Z']),'Znext_recorded':str(candidate['Znext']),
        'q_recorded':[str(v) for v in candidate['q']],'qnext_recorded':[str(v) for v in candidate['qnext']],
        'q_sum_from_stored_decimals':str(sum(candidate['q'],Decimal(0))),
        'qnext_sum_from_stored_decimals':str(sum(candidate['qnext'],Decimal(0))),
        'drift_from_stored_decimals_only':str(numeric_difference),
        'certified_as_static_Nash':False,'full_policy_supplied':False,'new_SPE_realizability_check':False,
        'boundary':'Exact actual counts arithmetic only. Float q/Z are preserved discovery data, not exact optimum, interval bounds or a full SPE certificate.'},
    'status':'PASS'
}
print(json.dumps(out,ensure_ascii=False,indent=2))
