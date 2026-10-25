"""Expand the six core customers and check all original-game histories exactly."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
j = json.loads((HERE / 'generic_padding_failure_exact.json').read_text())
i = j['core_instance']
p, m = len(i['topics']), i['players']
cs = [frozenset(c['topics']) for c in i['customers'] for _ in range(c['multiplicity'])]
sigma = {tuple(q['history']): q['action'] for q in j['core_certificate']['actions']}
assert set(sigma) == {h for d in range(m) for h in product(range(p), repeat=d)}

@lru_cache(None)
def terminal(h):
    return h if len(h) == m else terminal(h + (sigma[h],))

def payoff(z, a):
    return sum((F(1, sum(b in c for b in z)) for c in cs if a in c), F())

slacks = []
for h, a in sigma.items():
    current = payoff(terminal(h), a)
    for b in range(p):
        if b != a:
            slacks.append(current - payoff(terminal(h + (b,)), b))
assert min(slacks) >= 0
path = terminal(())
assert path == tuple(j['core_path'])
u = [payoff(path, a) for a in path]
assert list(map(str, u)) == j['core_payoffs']
D = 2 * u[0]
assert D / 3 > u[-1]
# The integral five-player instance is 3 clones of every original client
# plus 14 new D-only clients.  At (D,D,1,3), prescribed 3 earns 4,
# whereas deviation D earns 14/3.
five_cs = [c for c in cs for _ in range(3)] + [frozenset({4})] * 14
def five_payoff(z, a):
    return sum((F(1, sum(b in c for b in z)) for c in five_cs if a in c), F())
prescribed = five_payoff((4, 4, 1, 3, 3), 3)
deviated = five_payoff((4, 4, 1, 3, 4), 4)
assert prescribed == 4 and deviated == F(14, 3)
report = {'valid_core_SPE': True,
          'independence': 'No canonical model, solver, verifier, or author builder imported.',
          'expanded_core_unit_customers': len(cs),
          'core_decision_histories': len(sigma),
          'core_nonself_deviations': len(slacks),
          'core_minimum_slack': str(min(slacks)),
          'integer_five_customers': len(five_cs),
          'five_last_prescribed_payoff': str(prescribed),
          'five_last_D_deviation_payoff': str(deviated),
          'five_strict_improvement': str(deviated - prescribed)}
(HERE / 'generic_padding_failure_independent_audit.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
