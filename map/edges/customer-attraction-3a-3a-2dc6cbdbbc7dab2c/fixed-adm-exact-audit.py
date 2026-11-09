import argparse
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from functools import lru_cache
import hashlib
import json
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[3])
parser.add_argument('--output', type=Path)
args = parser.parse_args()
source = args.repo.resolve()
evidence = source / 'archives/customer-attraction/tools/evidence/adm-seed-mutations-and-strict-cone-four-primary'
manifest = json.loads((evidence / 'dependency-manifest.json').read_text())
dependencies = {item['source']['path']: item for item in manifest['dependencies'][:5]}
for dependency in dependencies.values():
    original = source / dependency['existing_preserved_path']
    assert hashlib.sha256(original.read_bytes()).hexdigest() == dependency['source']['sha256']
sys.path.insert(0, str((source / dependencies['customer_attraction/model.py']['existing_preserved_path']).parent.parent))
from customer_attraction.model import Instance
from customer_attraction.exact import ExactSPESolver

seed_source = source / dependencies['examples/customer_attraction/root_tax_failure.json']['existing_preserved_path']
seed = Instance.from_dict(json.loads(seed_source.read_text()))
report = json.loads((evidence / 'original/strict_cone_discovery.json').read_text())
actual = tuple(report['path'])
acts = ExactSPESolver(seed).certificate(on_path=actual).actions
m, k = seed.players, seed.topic_count
labels = tuple(range(k))
assert set(acts) == {h for depth in range(m) for h in product(labels, repeat=depth)}

def finish(h):
    while len(h) < m:
        h += (acts[h],)
    return h

assert finish(()) == actual
stored = tuple(F(str(w)) for w in report['records'][0]['w'])
assert all(tuple(F(str(w)) for w in row['w']) == stored for row in report['records'])
weights = {mask: w for mask, w in enumerate(stored, 1) if w}
assert weights == {2:F(1,4), 61:F(1)}
assert set(labels) - {1} == {i for i in labels if 61 & 1<<i}

def current(topic, leaf):
    return sum((w / sum(bool(mask & 1<<other) for other in leaf) for mask, w in weights.items()
                if mask & 1<<topic), F(0))

slack = [current(acts[h], finish(h))-current(a, finish(h+(a,)))
         for h in acts for a in labels if a != acts[h]]
assert len(slack) == 1295 and min(slack) == 0
u = [current(a,actual) for a in actual]
assert u == [F(1,4)] * m

@lru_cache(None)
def outcomes(h):
    if len(h) == m:
        return {h}
    child = {a:outcomes(h+(a,)) for a in labels}
    cutoff = max(min(current(a,z) for z in child[a]) for a in labels)
    return {z for a in labels for z in child[a] if current(a,z)>=cutoff}

menu = {finish(actual[:i]+(a,)) for i in range(m) for a in labels}
cap = {z for i in range(m) for a in labels for z in outcomes(actual[:i]+(a,)) if current(a,z) <= u[i]}
assert menu <= cap
assert {z.count(1) for z in menu} == {z.count(1) for z in cap} == {0,1}

def insert(topic, leaf):
    return sum((w / (1 + sum(bool(mask & 1<<other) for other in leaf)) for mask, w in weights.items()
                if mask & 1<<topic), F(0))

payoffs = {z.count(1): (insert(0,z), insert(1,z)) for z in cap}
assert payoffs == {0:(F(1,5),F(1,4)),1:(F(1,4),F(1,8))}
p = F(5,7)
q = F(5,7)
primal = min(p*x+(1-p)*y for x,y in payoffs.values())
dual = max(q*payoffs[0][column] + (1-q)*payoffs[1][column] for column in (0,1))
assert primal == dual == F(3,14)

result = {
    'exact_scope': 'Archived CDAA reconstructed labeled policy at the single rationalized saved point; all cap-legal continuations independently enumerated. No strict LP claim.',
    'history_count': len(acts),
    'nonself_ic_count': len(slack),
    'minimum_slack': str(min(slack)),
    'actual': list(actual),
    'actual_payoffs': [str(x) for x in u],
    'distinct_actual_query_labeled_leaves': len(menu),
    'distinct_cap_legal_ordered_leaves': len(cap),
    'economic_B_counts': sorted(payoffs),
    'query_price_matrix': {i:[str(x) for x in payoffs[i]] for i in sorted(payoffs)},
    'query_broad_mass': str(p),
    'adversary_all_broad_mass': str(q),
    'exact_value': str(primal),
    'gap_from_W_over_m': str(primal - F(1,m)),
}
output = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
if args.output is not None:
    args.output.write_text(output, encoding='utf-8')
print(output, end='')
