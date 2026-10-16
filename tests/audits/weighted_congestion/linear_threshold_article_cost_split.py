"""非负多项式拆项与私有一次常数资源的精确费用保真审计。

Deterministic finite identity checks for the manuscript upper-bound import;
not a proof of the cited general approximate-potential theorem.
"""
from fractions import Fraction as F
from itertools import product
import json
import argparse
import hashlib
import platform
from pathlib import Path
import shlex
import sys


def costs(weights, polys, actions, state):
    loads = {e: sum((weights[i] for i, a in enumerate(state) if e in actions[i][a]), F(0))
             for e in polys}
    return tuple(sum((sum((a * loads[e] ** k for k, a in polys[e].items()), F(0))
                      for e in actions[i][state[i]]), F(0))
                 for i in range(len(weights)))


def split(weights, polys, actions):
    newpolys = {}
    newactions = []
    images = []
    for i, aa in enumerate(actions):
        row = []
        mapping = []
        for old in aa:
            new = set()
            for e in old:
                for k, a in polys[e].items():
                    if not a:
                        continue
                    if k:
                        key = ('shared', e, k)
                        newpolys[key] = {k: a}
                    else:
                        key = ('private', e, i)
                        newpolys[key] = {1: a / weights[i]}
                    new.add(key)
            new = frozenset(new)
            if new not in row:
                row.append(new)
            mapping.append(row.index(new))
        newactions.append(row)
        images.append(mapping)
    return newpolys, newactions, images


def check(weights, polys, actions, degree):
    pp, aa, mapping = split(weights, polys, actions)
    assert all(0 < next(iter(v)) <= degree for v in pp.values())
    assert all(next(iter(v.values())) > 0 for v in pp.values())
    # Verify private resource can occur only in its owner's actions.
    for key in pp:
        if key[0] == 'private':
            owner = key[2]
            assert all(key not in a for j, row in enumerate(aa) if j != owner for a in row)
    checked = devs = 0
    for state in product(*(range(len(row)) for row in actions)):
        newstate = tuple(mapping[i][a] for i, a in enumerate(state))
        assert costs(weights, polys, actions, state) == costs(weights, pp, aa, newstate)
        checked += 1
        for i, row in enumerate(actions):
            for action in range(len(row)):
                dev = list(state)
                dev[i] = action
                newdev = list(newstate)
                newdev[i] = mapping[i][action]
                assert costs(weights, polys, actions, dev) == costs(weights, pp, aa, newdev)
                devs += 1
    return {'states': checked, 'deviations_including_self': devs,
            'original_actions': [len(a) for a in actions],
            'merged_actions': [len(a) for a in aa],
            'positive_resources': len(pp)}


weights = (F(2, 3), F(7, 5), F(11, 2))
cases = [
    ({'z': {0: F(0)}}, [[set(), {'z'}], [{'z'}], [set(), {'z'}]], 1),
    ({'c': {0: F(3, 7)}, 'z': {2: F(0)}},
     [[set(), {'c'}, {'c', 'z'}], [{'c'}, {'z'}], [{'c'}, set()]], 1),
    ({'x': {0: F(3, 7), 1: F(2, 9), 3: F(5, 11)},
      'y': {0: F(7, 13), 2: F(5, 17)}, 'z': {0: F(0)}},
     [[set(), {'x'}, {'x', 'z'}, {'x', 'y'}], [{'x'}, {'y'}], [{'y'}, {'x', 'y'}, {'z'}]], 3),
]
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.output is not None and args.output.exists():
        parser.error('refusing to overwrite frozen output')
    code = Path(__file__).resolve()
    repo = code.parents[3]
    article = repo / 'research/current/weighted_congestion/linear_threshold_article.tex'
    result = {
        'title': '非负多项式拆项与私有一次常数资源的费用保真审计',
        'status': 'all exact assertions passed',
        'code_path': str(code.relative_to(repo)),
        'code_sha256': hashlib.sha256(code.read_bytes()).hexdigest(),
        'article_sha256': hashlib.sha256(article.read_bytes()).hexdigest(),
        'python_version': platform.python_version(),
        'command': shlex.join([sys.executable, *sys.argv]),
        'arithmetic': 'fractions.Fraction, exact; zero tolerance',
        'seed': None,
        'input_weights': [str(w) for w in weights],
        'inputs': [
            {'polynomials': {e: {str(k): str(v) for k, v in terms.items()} for e, terms in p.items()},
             'actions': [[sorted(action) for action in row] for row in a], 'degree': d}
            for p, a, d in cases],
        'results': [check(weights, p, a, d) for p, a, d in cases],
        'scope': 'Finite cost-preservation identities including empty/zero/constant/mixed cases; no general existence theorem is proved by enumeration.'}
    payload = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x', encoding='utf-8') as stream:
            stream.write(payload)
    print(payload, end='')

if __name__ == '__main__':
    main()
