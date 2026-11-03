"""Definition-level replay of the frozen full strategy; standard library only."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
obj = json.loads((HERE / 'terminal_share_padding_exact.json').read_text())
inst = obj['instance']
m = inst['players']
p = len(inst['topics'])
customers = [frozenset(c['topics']) for c in inst['customers']
             for _ in range(c['multiplicity'])]
actions = {tuple(q['history']): q['action']
           for q in obj['certificate']['actions']}
assert len(actions) == len(obj['certificate']['actions'])
assert set(actions) == {h for d in range(m) for h in product(range(p), repeat=d)}
assert all(a in range(p) for a in actions.values())

@lru_cache(None)
def terminal(h):
    return h if len(h) == m else terminal(h + (actions[h],))

@lru_cache(None)
def utility(path, theme):
    return sum((F(1, sum(a in c for a in path))
                for c in customers if theme in c), F())

slacks = []
actual_rows = []
for h in sorted(actions, key=lambda h: (len(h), h)):
    a = actions[h]
    branches = [terminal(h + (b,)) for b in range(p)]
    utilities = [utility(z, b) for b, z in enumerate(branches)]
    current = utilities[a]
    slacks.extend(current - utilities[b] for b in range(p) if b != a)
    assert all(current >= d for d in utilities), (h, utilities)
    if h == tuple(obj['path'][:len(h)]):
        actual_rows.append({'history': list(h), 'chosen': a,
                            'deviation_payoffs': list(map(str, utilities)),
                            'deviation_terminals': [list(z) for z in branches]})
path = terminal(())
payoffs = [utility(path, a) for a in path]
covered = lambda z: sum(any(a in c for a in z) for c in customers)
W = covered(path)
OPT = max(covered(z) for z in product(range(p), repeat=m))
assert path == tuple(obj['path'])
assert W == obj['welfare'] and OPT == obj['optimum']
assert list(map(str, payoffs)) == obj['payoffs']
violation = 6 * payoffs[-1] - 2 * W
assert violation > 0 and violation == F(obj['candidate_violation'])
report = {
    'valid': True,
    'independence': 'No canonical game model, SPE solver, verifier, or cone imported.',
    'expanded_unit_customers': len(customers),
    'decision_histories': len(actions),
    'nonself_deviations': len(slacks),
    'minimum_slack': str(min(slacks)),
    'zero_slacks': sum(q == 0 for q in slacks),
    'path': list(path), 'payoffs': list(map(str, payoffs)),
    'welfare': W, 'optimum': OPT,
    'C2_violation': str(violation),
    'actual_history_rows': actual_rows,
}
(HERE / 'terminal_share_padding_independent_audit.json').write_text(
    json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
