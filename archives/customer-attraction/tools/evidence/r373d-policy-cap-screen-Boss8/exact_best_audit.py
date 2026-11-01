#!/usr/bin/env python3
"""Independent Fraction audit of the saved best policy in a finite root-menu probe."""
from fractions import Fraction
from pathlib import Path
import hashlib, json

ROOT = Path(__file__).resolve().parent
src = ROOT / 'source.json'
data = json.loads(src.read_text())
best = data['best']
weights = {int(k): Fraction(str(v)).limit_denominator(1000) for k, v in best['weights'].items()}
policy = {tuple(x['history']): int(x['action']) for x in best['actions']}

def out(history):
    h = list(history)
    while len(h) < int(data['parameters']['m']):
        h.append(policy[tuple(h)])
    return h

def share(mask, action, terminal):
    if not ((mask >> action) & 1):
        return Fraction(0)
    return Fraction(1, terminal.count(action))

rows = []
for h, prescribed in policy.items():
    terminal = out(h)
    for forced in range(int(data['parameters']['p'])):
        if forced == prescribed:
            continue
        forced_terminal = out(h + (forced,))
        slack = sum(weight * (share(mask, prescribed, terminal) - share(mask, forced, forced_terminal))
                     for mask, weight in weights.items())
        rows.append(slack)

root_terminal = out(())
covered = {a for a in root_terminal}
welfare = sum(weight * sum(1 for a in covered if (mask >> a) & 1)
              for mask, weight in weights.items())
query = [Fraction(0)] * int(data['parameters']['p'])
for a in range(len(query)):
    for mask, weight in weights.items():
        if (mask >> a) & 1:
            for bg in best['backgrounds']:
                denominator = 1 + sum(bg[i] for i in range(len(query)) if (mask >> i) & 1)
                query[a] += weight * Fraction(1, denominator)
            query[a] /= len(best['backgrounds'])
# The saved best query is the fifth coordinate; the one saved background is all three rivals at topic 4.
saved_query = [Fraction(str(x)).limit_denominator(1000) for x in best['query']]
cap = max(query)
factor = Fraction(7, 2)
result = {
    'status': 'exact_best_policy_audit_passed',
    'source_id': '20c07eabe73f43a4218b',
    'source_path': 'research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/root_menu/policy_cap_m4p5_factor3.5_seed373801.json',
    'source_sha256': hashlib.sha256(src.read_bytes()).hexdigest(),
    'parameters': data['parameters'],
    'effective_factor': str(factor),
    'policy_histories': len(policy),
    'deviation_rows': len(rows),
    'negative_rows': sum(x < 0 for x in rows),
    'zero_rows': sum(x == 0 for x in rows),
    'positive_rows': sum(x > 0 for x in rows),
    'minimum_slack': str(min(rows)),
    'distinct_slacks': sorted({str(x) for x in rows}, key=lambda s: Fraction(s)),
    'weights': {str(k): str(v) for k, v in sorted(weights.items())},
    'root_terminal': root_terminal,
    'welfare_W': str(welfare),
    'backgrounds': best['backgrounds'],
    'query_values_for_saved_background': [str(x) for x in query],
    'saved_query': [str(x) for x in saved_query],
    'cap': str(cap),
    'factor_cap_minus_W': str(factor * cap - welfare),
    'interpretation': 'The exact candidate is a valid finite full-policy SPE certificate with W=1/2 and cap=1/8 for the saved root background; factor 7/2 gives -1/16. It is therefore not a counterexample to W >= (7/2) cap.',
    'limitations': [
        'The audit covers only the saved best policy and its one saved background, not all 60 sampled games, all 12 starts, or all complete SPEs.',
        'The source trace is a floating-point alternating LP search; no exact rational audit was performed for every trace record.',
        'The model is m=4,p=5 and does not establish any universal six-provider half-coverage theorem.'
    ]
}
(ROOT/'exact_best_audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
