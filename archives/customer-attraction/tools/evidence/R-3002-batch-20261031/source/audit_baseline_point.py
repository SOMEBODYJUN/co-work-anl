"""Exact scalar audit of an old-root-row separation point, no discovery import."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
raw = (HERE / 'research_4/baseline_exact_primal.json').read_bytes()
point = json.loads(raw)
cert = json.loads((HERE / 'research_4/root_requery_third_L_o4.2_exact.json').read_text())
paths = cert['paths'][:4]
first = cert['first_genuine'][:4]
edges = cert['copy_edges'][:3]
names = ''.join(dict.fromkeys(''.join(paths)))
assert paths == ['TABCDE', 'TEFGHI', 'TAEJKL', 'TABEMN']
assert first == [1, 2, 3, 4]
atoms = []
for code, weight in point['weights'].items():
    code, weight = int(code), F(weight)
    assert 0 <= code < 2**len(names) and weight >= 0
    atoms.append(({a: (code >> i) & 1 for i, a in enumerate(names)}, weight))

def aggregate(function):
    return sum((weight * function(bit) for bit, weight in atoms), F())

def load(bit, path):
    return sum(bit[a] for a in path)

def payoff(bit, path, i):
    return F(bit[path[i]], max(load(bit, path), 1))

K, O = F(1), F(21, 5)
assert aggregate(lambda b: b['T']) == K
rows = []
for a in names:
    if a != 'T':
        rows.append(K - aggregate(lambda b: b[a]))
for s, i, t in edges:
    assert paths[s][:i] == paths[t][:i] and i >= first[s] and first[t] == i + 1
    rows.append(aggregate(lambda b: payoff(b, paths[s], i) - payoff(b, paths[t], i)))
for j, path in enumerate(paths):
    for i in range(first[j], 6):
        for a in names:
            rows.append(aggregate(lambda b: payoff(b, path, i) - F(b[a], load(b, path[:i]) + 6 - i)))
    rows.append(aggregate(lambda b: 6 * payoff(b, path, 5) + F(load(b, path[:5]), load(b, path[:5]) + 1)) - O)
    rows.append(aggregate(lambda b: 3 * (payoff(b, path, 4) + payoff(b, path, 5)
                                        + F(b[path[4]], (load(b, path[:4]) + 1) * (load(b, path[:4]) + 2)))
                          + F(load(b, path[:4]), load(b, path[:4]) + 1)) - O)
assert len(rows) == 235 and min(rows) >= 0
nu, den = cert['multipliers_numerators'], cert['denominator']
alpha = F(sum(v for k, v in nu.items() if k.startswith(('LASTO:', 'PAIRO:'))), den)
beta = F(cert['equality_numerator'] - sum(v for k, v in nu.items() if k.startswith('CAP:')), den)
r = aggregate(lambda b: payoff(b, paths[0], 0))
margin = r - alpha * O - beta * K
assert margin < 0
result = dict(input_sha256=hashlib.sha256(raw).hexdigest(), types=len(atoms),
              old_rows=len(rows), min_old_slack=str(min(rows)), K=str(K), O=str(O), r=str(r),
              QL_margin=str(margin),
              status='exact separation of specified 235 old root rows; not a game or SPE')
(HERE / 'baseline_point_audit.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
