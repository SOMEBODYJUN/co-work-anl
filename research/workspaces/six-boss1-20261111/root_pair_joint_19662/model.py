"""Finite common old-word / six-root projection at the 19662-row point.

The old 17 root STATES are a seed only.  No old masses, budgets or signs are
imported.  The unique t=1 position (a fact of this point) is aligned first;
zero-root words are assigned jointly to the complete old (t,b,c) words.
All 36 new strong-PAIR rows use one true two-player source and two query
labels from the SAME donor branch.  Every row pays its source tax once.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations_with_replacement, permutations
from pathlib import Path
import hashlib
import json
import types

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
REPO = BASE.parents[2]
POINT = BASE / 'union_augmented_lp/augmented_lp_exact.json'
PIN = 'b0ca65cfe61e5e3ef09537cba2a986c171aeaa7106f673077f803c80ee2b68e3'
ROOT_SEED = BASE / 'cross_root_pricing/joint_completion_exact.json'
ROOT_CONTRACT = BASE / 'cross_root_pricing/contract.py'
PAIR_ROLES = tuple(combinations_with_replacement(range(5), 2))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def q(n, d):
    return F(n, d) if n else F(0)


def bits(w, n):
    return tuple(map(int, format(w, '0'+str(n)+'b')))


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')


def root_contract():
    """Read-only import; never creates a sibling __pycache__."""
    module = types.ModuleType('root_contract_readonly')
    module.__file__ = str(ROOT_CONTRACT)
    exec(compile(ROOT_CONTRACT.read_text(), str(ROOT_CONTRACT), 'exec'), module.__dict__)
    return module


def load_inputs():
    assert sha(POINT) == PIN
    raw = json.loads(POINT.read_text())
    hist = {i: {'original_column_index': i, **row}
            for i, row in enumerate(raw['columns']) if row['kind'] == 'hist'}
    assert len(hist) == 16
    marginal = defaultdict(F)
    for h in hist.values():
        assert sum(h['hist']) == 6
        assert sum(h['hist'][4:]) == h['d'] == 1
        marginal[h['actual_bits'], h['d']] += F(h['weight'])
    marginal = {ctx: value for ctx, value in sorted(marginal.items()) if value}
    pay = [sum((F(h['weight'])*q(int(h['actual_bits'][i]), sum(map(int, h['actual_bits'])))
                for h in hist.values()), F(0)) for i in range(6)]
    cap = next(F(v['weight']) for v in raw['columns'] if v['kind'] == 'K')
    assert sum(pay) == F(raw['W'])
    assert sum(F(h['weight']) for h in hist.values()) == F(raw['O']) == 1
    table = {}
    sources = [POINT, ROOT_SEED, ROOT_CONTRACT, BASE/'main_19662_audit.json']
    for t in (0, 1):
        path = BASE/f'background_five_bridge/fixed53_b{t}_profit.json'
        sources.append(path)
        for r in json.loads(path.read_text())['min_by_actual_and_d']:
            table[t, int(r['actual'], 2), r['d']] = F(r['min_rho'])
    assert len(table) == 384
    original = json.loads(ROOT_SEED.read_text())
    # These records have no mass field: only the old support is carried over.
    seeds = [{k: r[k] for k in ('actual', 'd', 'one_word', 'zero_words')}
             for r in original['support']]
    assert len(seeds) == 17
    data = {'hist': hist, 'masses': marginal, 'u': pay, 'K': cap, 'O': F(raw['O']),
            'W': F(raw['W']), 'remainder': table, 'seeds': seeds,
            'sources': [{'path': str(p.relative_to(BASE)), 'sha256': sha(p)} for p in sources]}
    return data


def input_snapshot(data):
    return {'scope': 'Fresh 19662-point data; old root states are candidate support only.',
            'point_sha256': PIN, 'sources': data['sources'],
            'original_hist_records': list(data['hist'].values()),
            'actual_margins': [{'actual': a, 'd': d, 'mass': str(m)}
                               for (a, d), m in data['masses'].items()],
            'u': list(map(str, data['u'])), 'K': str(data['K']),
            'O': str(data['O']), 'W': str(data['W']),
            'candidate_root_states': data['seeds'],
            'remainder_table': [{'t': t, 'word': w, 'comparison_count': d, 'value': str(v)}
                                for (t, w, d), v in sorted(data['remainder'].items())]}


def single_names():
    return ([('C-to-Y', k, rel) for k in range(5) for rel in ('same', 'off')]
            + [('Y5-to-C', rel) for rel in ('same', 'off')]
            + [('B-to-Y', k, rel) for k in range(5) for rel in ('same', 'off')]
            + [('Y-to-old', k, old, rel) for k in range(4) for old in ('B', 'C')
               for rel in ('same', 'off')]
            + [('Y5-to-B', rel) for rel in ('same', 'off')])


def pair_names():
    return ([('old-pair-to-Y', l, m, rel) for l, m in PAIR_ROLES
             for rel in ('same', 'off')]
            + [('new-pair-to-old', v, w, rel) for v, w in (('B', 'B'), ('B', 'C'), ('C', 'C'))
               for rel in ('same', 'off')])


def interfaces(actual, old, new):
    """Return positive-IC coefficients, with exact orbit normalizers."""
    a = tuple(map(int, actual))
    p3 = sum(a[:3])
    ow = [bits(w, 3) for w in old]
    nw = [bits(w, 5) for w in new]
    result = {name: F(0) for name in single_names()+pair_names()}
    for i, (t, b, c) in enumerate(ow):
        p = p3+t
        oldpay = q(b, p+b+c)
        old_pair_wallet = q(b+c, p+b+c)+F(b, (p+1)*(p+2))
        for j, e in enumerate(nw):
            s = ow[j][0]
            z = sum(e)
            rel = 'same' if i == j else 'off'
            norm = 6 if i == j else 30
            for k in range(5):
                result['C-to-Y', k, rel] += F(c-e[k], norm*(p+b+1))
                result['B-to-Y', k, rel] += (oldpay-F(e[k], p+2))/norm
            for k in range(4):
                truepay = q(e[k], s+z)
                safe = s+sum(e[:k])+5-k
                result['Y-to-old', k, 'B', rel] += (truepay-F(b, safe))/norm
                result['Y-to-old', k, 'C', rel] += (truepay-F(c, safe))/norm
            lastden = s+sum(e[:4])+1
            result['Y5-to-C', rel] += (q(e[4], s+z)-F(c, lastden))/norm
            result['Y5-to-B', rel] += (q(e[4], s+z)-F(b, lastden))/norm
            for l, m in PAIR_ROLES:
                result['old-pair-to-Y', l, m, rel] += (old_pair_wallet
                    - F(e[l]+e[m], p+1)+F(e[l]*e[m], (p+1)*(p+2)))/norm
            pref = s+sum(e[:3])
            new_pair_wallet = q(e[3]+e[4], s+z)+F(e[3], (pref+1)*(pref+2))
            for v, w, x, y in (('B', 'B', b, b), ('B', 'C', b, c), ('C', 'C', c, c)):
                result['new-pair-to-old', v, w, rel] += (new_pair_wallet
                    - F(x+y, pref+1)+F(x*y, (pref+1)*(pref+2)))/norm
    assert len(result) == 76
    return result


def canonical_old(h):
    words = [w for w, count in enumerate(h['hist']) for _ in range(count)]
    words.sort(key=lambda w: (-int(w >= 4), w))
    assert len(words) == 6 and words[0] >= 4 and all(w < 4 for w in words[1:])
    return words


def seed_columns(data, rc):
    """Complete incidence coupling over the seventeen seeded root states."""
    names = rc.row_names(True)
    result = []
    for hi, h in data['hist'].items():
        if not F(h['weight']):
            continue
        old = canonical_old(h)
        for ri, root in enumerate(data['seeds']):
            if (h['actual_bits'], h['d']) != (root['actual'], root['d']):
                continue
            rpay, costs = rc.compressed_column(root['actual'], root['d'],
                rc.column_roots(root['one_word'], root['zero_words']), names, data['remainder'])
            found = set()
            for zero in sorted(set(permutations(root['zero_words']))):
                new = (root['one_word'],)+zero
                key = tuple(sorted(zip(old, new)))
                if key in found:
                    continue
                found.add(key)
                inter = interfaces(root['actual'], old, new)
                result.append({'hist': hi, 'seed_root_state': ri, 'actual': root['actual'],
                               'old_words': old, 'new_words': list(new), 'root': rpay,
                               'root_costs': costs, 'interface': inter})
    assert len(result) == 32
    return result


def system(data, columns, pairs):
    rc = root_contract()
    root_names = rc.row_names(True)
    if_names = single_names()+(pair_names() if pairs else [])
    ub_names = root_names+if_names+[('root-source',)]
    ub = [[c['root_costs'][k] for c in columns] for k in range(163)]
    ub += [[-c['interface'][name] for c in columns] for name in if_names]
    ub += [[c['root'] for c in columns]]
    bub = rc.budgets(data, root_names)+[F(0)]*len(if_names)+[data['u'][0]]
    eq_names = [hi for hi, h in data['hist'].items() if F(h['weight'])]
    eq = [[F(c['hist'] == hi) for c in columns] for hi in eq_names]
    beq = [F(data['hist'][hi]['weight']) for hi in eq_names]
    return eq_names, eq, beq, ub_names, ub, bub
