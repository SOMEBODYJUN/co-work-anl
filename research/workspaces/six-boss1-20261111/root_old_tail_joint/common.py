"""Old C / new-root-tail interface on a common six-index customer.

This module uses standard library only. The unique t=1 index is aligned before
any zero-index permutations. All rows are complete S6 orbit averages.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
PIN = 'd70c26065d42fd73dedc94183e4533dd6f8608d5841f7a6018ff180dc77e2f9f'


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def q(n, d):
    return F(n, d) if n else F(0)


def read_sources():
    source = BASE / 'cross_root_pricing'
    frozen = json.loads((source / 'projection_inputs_exact.json').read_text())
    root = json.loads((source / 'joint_completion_exact.json').read_text())
    product = json.loads((source / 'original_hist_refinement_exact.json').read_text())
    assert frozen['point_sha256'] == root['point_sha256'] == product['point_sha256'] == PIN
    assert digest(BASE / 'peer_augmented_lp/augmented_lp_exact.json') == PIN
    assert product['joint_completion_sha256'] == digest(source / 'joint_completion_exact.json')
    hist = {h['original_column_index']: h for h in frozen['original_hist_records']}
    return frozen, root, product, hist


def old_words(hist):
    words = [w for w, count in enumerate(hist) for _ in range(count)]
    assert len(words) == 6
    words.sort(key=lambda w: (-int(w >= 4), w))
    return words


def records(old, new):
    assert len(old) == len(new) == 6
    return [(tuple(map(int, f'{w:03b}')), tuple(map(int, f'{v:05b}')))
            for w, v in zip(old, new)]


def names():
    return [('C-to-Y', role, relation) for role in range(5) for relation in ('same', 'off')] + [
        ('Y5-to-C', relation) for relation in ('same', 'off')]


def literal_interface(actual, old, new):
    rec = records(old, new)
    p = sum(map(int, actual[:3]))
    out = {name: F(0) for name in names()}
    for i, ((t, b, c), ei) in enumerate(rec):
        for j, ((s, bj, cj), e) in enumerate(rec):
            relation = 'same' if i == j else 'off'
            norm = 6 if i == j else 30
            for role in range(5):
                out['C-to-Y', role, relation] += q(c - e[role], p + t + b + 1) / norm
            out['Y5-to-C', relation] += (
                q(e[4], s + sum(e)) - q(c, s + sum(e[:4]) + 1)) / norm
    return out


def aligned_assignments(hist, root):
    """All distinct joint incidence orbits for fixed hist/root multisets.

    D=1 only at this fixed input. A canonical old-word order is held fixed.
    Zero-root permutations that differ only inside an identical old-word block
    are equivalent under simultaneous S6 and are retained once.
    """
    old = old_words(hist['hist'])
    assert hist['d'] == root['d'] == sum(w >= 4 for w in old) == 1
    found = {}
    for p in sorted(set(permutations(root['zero_words']))):
        new = (root['one_word'],) + p
        key = tuple(sorted(zip(old, new)))
        if key not in found:
            found[key] = new
    return old, list(found.values())


def product_atoms(product, hist):
    """Uniform zero-index permutation, with old/root t=1 already aligned."""
    out = []
    for p in product['atoms']:
        h = hist[p['original_column_index']]
        old = old_words(h['hist'])
        assert old[0] >= 4 and all(w < 4 for w in old[1:])
        perms = sorted(set(permutations(p['zero_words'])))
        groups = defaultdict(int)
        reps = {}
        for e in perms:
            new = (p['one_word'],) + e
            key = tuple(sorted(zip(old, new)))
            groups[key] += 1
            reps[key] = new
        for key, count in sorted(groups.items()):
            out.append({'original_column_index': p['original_column_index'],
                        'joint_atom_index': p['joint_atom_index'],
                        'actual': p['actual'], 'old_words': old,
                        'new_words': list(reps[key]),
                        'mass': str(F(p['mass']) * count / len(perms))})
    return out


def eval_interface(atoms):
    result = {name: F(0) for name in names()}
    for atom in atoms:
        v = literal_interface(atom['actual'], atom['old_words'], atom['new_words'])
        for name, val in v.items():
            result[name] += F(atom['mass']) * val
    return result


def rows_json(values):
    return [{'row': list(name), 'value': str(value), 'float': float(value)}
            for name, value in values.items()]


def write_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
