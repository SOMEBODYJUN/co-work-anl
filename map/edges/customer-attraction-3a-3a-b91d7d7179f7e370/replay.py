"""Verify the frozen 427-column point and materialize its 33 specified last nodes."""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from math import gcd, lcm
from pathlib import Path
import runpy


REPO = Path(__file__).resolve().parents[3]
EVIDENCE = REPO / 'archives/customer-attraction/tools/evidence/joint-terminal-refinements-and-materialization-primary'
SOURCE = EVIDENCE / 'source-root'
WORKSPACES = SOURCE / 'research/workspaces/customer-attraction'
JOINT = WORKSPACES / 'R-ffea274483aa4105a317300038fe04ce/credible_counterexample'
INPUT = SOURCE / 'evidence/certificates/customer_attraction/five_player_indexed_bound.json'
OLD = SOURCE / 'tests/audits/customer_attraction_five_indexed.py'
OFF = WORKSPACES / 'R-c4732bee2f7b4e50a70568170e3334ae/continuation_completion/offdiagonal_closure.py'
EXPORTED = EVIDENCE / 'current-run-001/native-already-computed-unit-type-instance.json'
FIXED = tuple('ABCDEUVWXY')
GROUPS = ('T', 'L_actual', 'L_second', 'L_third', 'AB_R', 'AB_S', 'AE_R', 'AE_S',
          'second_H', 'second_I', 'second_J')
TRIPLES = tuple(product((0, 1), repeat=3))
QUADS = tuple(product((0, 1), repeat=4))


def read_json(path):
    return json.loads(path.read_bytes())


def expand(histogram, types):
    assert len(histogram) == len(types) and sum(histogram) == 5
    return tuple(ty for ty, count in zip(types, histogram, strict=True) for _ in range(count))


def align(histogram, types, slots):
    expanded = expand(histogram, types)
    partitions = [[ty for ty in expanded if ty[0] == t] for t in (0, 1)]
    for arrangement in product(*(sorted(set(permutations(part))) for part in partitions)):
        entries = tuple(map(iter, arrangement))
        yield tuple(next(entries[t]) for t in slots)


def assign(ell, h, slots):
    zeros = [i for i, t in enumerate(slots) if t == 0]
    ones = [i for i, t in enumerate(slots) if t == 1]
    for low, high in product(combinations(zeros, ell - h), combinations(ones, h)):
        yield tuple(int(i in low or i in high) for i in range(5))


def menus_for(ab, ae, second, last):
    return dict(zip(GROUPS, (tuple(row[0] for row in ab), *last,
                             tuple(row[1] for row in ab), tuple(row[2] for row in ab),
                             tuple(row[1] for row in ae), tuple(row[2] for row in ae),
                             tuple(row[1] for row in second), tuple(row[2] for row in second),
                             tuple(row[3] for row in second)), strict=True))


def exact_joint(bits, menus):
    a, b, c, _, e, u, _, _, _, _ = bits
    prefixes = {'L_actual': (a, b, c, menus['T']), 'L_second': (a, e, u, menus['T']),
                'L_third': (a, b, e, menus['T']), 'AB_S': (a, b, menus['T'], menus['AB_R']),
                'AE_S': (a, e, menus['T'], menus['AE_R']),
                'second_J': (a, menus['T'], menus['second_H'], menus['second_I'])}
    rows = {}
    for group, prefix in prefixes.items():
        def share_difference(i, member):
            load = sum(entry[i] if isinstance(entry, tuple) else entry for entry in prefix)
            return Fraction(menus[group][i] - member, 1 + load)

        for target, members in menus.items():
            rows[f'joint:{group}:vs:{target}:diag'] = sum(
                share_difference(i, members[i]) for i in range(5))
            rows[f'joint:{group}:vs:{target}:offdiag'] = sum(
                share_difference(i, members[j]) for i in range(5) for j in range(5) if i != j)
        for q, member in enumerate(bits):
            rows[f'joint:{group}:fixed:{q}'] = sum(share_difference(i, member) for i in range(5))
    assert len(rows) == 192
    return rows


def column_rows(bits, atom, evaluate, offdiag, coupling):
    histograms = [atom[name] for name in ('AB_hist', 'AE_hist', 'second_hist')]
    old = evaluate(bits, histograms, atom['menus_lh'], include_second_correlations=True)
    assert len(old) == 437
    off = offdiag(atom)
    assert len(off) == 10 and old.keys().isdisjoint(off)
    envelope = {'cross_envelope:' + key: value for key, value in coupling['rows'](atom).items()}
    assert len(envelope) == 46
    full = {}
    for group in ('AB', 'AE', 'second'):
        own, inverse = coupling['source_terms'](atom, group)
        for target, counts in coupling['target_counts'](atom).items():
            if not target.startswith(group + '_'):
                full[f'cross_full:{group}:{target}'] = 5 * own - sum(counts) * sum(inverse[0] + inverse[1])
    assert len(full) == 23
    rows = old | off | envelope | full
    assert len(rows) == 516
    return rows


def verify_point(atoms, report):
    audit_prefix, delimiter, _ = OLD.read_text().partition('\nfrom pathlib import Path\nfrom collections')
    assert delimiter
    namespace = {}
    exec(compile(audit_prefix, str(OLD), 'exec'), namespace)
    offdiag = runpy.run_path(str(OFF))['rows']
    coupling = runpy.run_path(str(JOINT / 'coupling_envelope_check.py'))
    refinements = iter(zip(report['refinements'], map(Fraction, report['exact_reweighting']), strict=True))
    slacks = {}
    positive = []
    covered = compared = Fraction(0)
    total = 0
    for parent, atom in enumerate(atoms):
        bits = tuple(map(int, atom['bits']))
        ab = expand(atom['AB_hist'], TRIPLES)
        slots = tuple(row[0] for row in ab)
        inherited = column_rows(bits, atom, namespace['evaluate'], offdiag, coupling)
        for ae, second, *last in product(align(atom['AE_hist'], TRIPLES, slots),
                                         align(atom['second_hist'], QUADS, slots),
                                         *(assign(ell, h, slots) for ell, h in atom['menus_lh'])):
            stored, weight = next(refinements)
            assert stored == json.loads(json.dumps({'parent_atom': parent, 'AE': ae, 'second': second, 'L': last}))
            assert weight >= 0
            menus = menus_for(ab, ae, second, last)
            coefficients = inherited | exact_joint(bits, menus)
            if slacks:
                assert slacks.keys() == coefficients.keys()
            for row, value in coefficients.items():
                slacks[row] = slacks.get(row, 0) + weight * value
            covered += weight * any(bits[:5])
            compared += weight * any(slots)
            if weight:
                positive.append((parent, bits, menus, weight))
            total += 1
    assert next(refinements, None) is None
    assert total == report['columns'] == 427 and len(slacks) == report['rows'] == 708
    assert len(positive) == report['positive_refinements'] == 44
    assert len({parent for parent, *_ in positive}) == report['positive_projected_atoms'] == 43
    assert covered == 1 and compared == Fraction(report['exact_primal_value']) > 2
    assert compared - 2 == Fraction(report['gap_above_two'])
    assert min(slacks.values()) == Fraction(report['minimum_slack']) == 0
    joint = {row: str(slack) for row, slack in slacks.items() if row.startswith('joint:')}
    assert joint == report['new_row_slacks'] and len(joint) == 192
    assert report['exact_optimality_claimed'] is False
    return positive, slacks


def create_catalog(positive):
    labels = FIXED + tuple(f'{group}{i}' for group in GROUPS for i in range(5))
    indices = {label: i for i, label in enumerate(labels)}
    scale = lcm(*(120 * weight.denominator for _, _, _, weight in positive))
    counts = Counter()
    for _, bits, menus, weight in positive:
        copies = weight * scale / 120
        assert copies.denominator == 1
        for perm in permutations(range(5)):
            mask = sum(bit << i for i, bit in enumerate(bits))
            for group in GROUPS:
                for i, slot in enumerate(perm):
                    mask |= menus[group][slot] << indices[f'{group}{i}']
            counts[mask] += copies.numerator
    common = gcd(*counts.values())
    counts = {mask: count // common for mask, count in counts.items()}
    signatures = {tuple(bool(mask & (1 << index)) for mask in counts) for index in range(len(labels))}
    assert len(signatures) == len(indices) == len(labels) == 65 and len(counts) == 1180
    assert scale % common == 0
    exported = read_json(EXPORTED)
    assert tuple(exported['labels']) == labels and exported['scaling'] == scale // common
    assert counts == {int(row['mask']): row['multiplicity'] for row in exported['customer_types']}
    return labels, indices, counts, scale // common


def specified_nodes():
    nodes = [(tuple('ABCD'), 'E'), (tuple('AEUV'), 'W'), (tuple('ABEX'), 'Y')]
    for i in range(5):
        t = f'T{i}'
        nodes.extend([(('A', 'B', 'C', t), f'L_actual{i}'), (('A', 'E', 'U', t), f'L_second{i}'),
                      (('A', 'B', 'E', t), f'L_third{i}'), (('A', 'B', t, f'AB_R{i}'), f'AB_S{i}'),
                      (('A', 'E', t, f'AE_R{i}'), f'AE_S{i}'),
                      (('A', t, f'second_H{i}', f'second_I{i}'), f'second_J{i}')])
    return nodes


def gains_and_last_nodes(labels, indices, counts, report):
    def utilities(prefix):
        known = [indices[label] for label in prefix]
        values = dict.fromkeys(labels, 0)
        for mask, count in counts.items():
            load = sum((mask >> index) & 1 for index in known)
            share = count * (60 // (1 + load))
            for label, index in indices.items():
                if mask & (1 << index):
                    values[label] += share
        return values

    def best(values):
        optimum = max(values.values())
        return [label for label, value in values.items() if value == optimum]

    nodes = specified_nodes()
    results = []
    for prefix, designated in nodes:
        values = utilities(prefix)
        assert designated in best(values)
        results.append({'history': list(prefix), 'action': designated,
                        'utility': str(Fraction(values[designated], 60)), 'best_replies': best(values)})
    assert results == report['node_results'] and len({prefix for prefix, _ in nodes}) == 33
    assert len(nodes) * len(labels) == report['deviation_comparisons_including_own'] == 2145
    witnesses = []
    tails = [('ABC', 'D', 'E', 'L_third0', 'W'), ('AEU', 'V', 'W', 'AE_S0', 'AE_R0'),
             ('ABE', 'X', 'Y', 'L_third0', 'second_J0')]
    for prefix, designated, reply, challenger, forced in tails:
        history = tuple(prefix)
        assert best(utilities((*history, challenger))) == [forced]
        actual = utilities((*history, reply))[designated]
        deviation = utilities((*history, forced))[challenger]
        gain = Fraction(deviation - actual, 60 * report['W'])
        assert gain > 0
        witnesses.append({'prefix': list(history), 'prescribed_tail': [designated, reply],
                          'forced_action': challenger, 'unique_last_br': forced, 'gain_over_W': str(gain)})
    return witnesses


def main():
    inputs = (INPUT, OLD, OFF, JOINT / 'coupling_envelope_check.py', JOINT / 'joint_terminal_lp.json',
              JOINT / 'audit_joint_terminal_materialization.json', EXPORTED)
    atoms = read_json(INPUT)['primal']['atoms']
    point = read_json(JOINT / 'joint_terminal_lp.json')
    audit = read_json(JOINT / 'audit_joint_terminal_materialization.json')
    assert len(atoms) == 64
    positive, slacks = verify_point(atoms, point)
    labels, indices, counts, scale = create_catalog(positive)
    welfare = sum(count for mask, count in counts.items() if mask & 31)
    tmask = sum(1 << indices[f'T{i}'] for i in range(5))
    compared = sum(count for mask, count in counts.items() if mask & tmask)
    assert welfare == scale == audit['W'] and compared == sum(counts.values()) == audit['customer_count']
    assert Fraction(compared, welfare) == Fraction(point['exact_primal_value'])
    witnesses = gains_and_last_nodes(labels, indices, counts, audit)
    print(json.dumps({
        'inputs': {str(path.relative_to(REPO)): sha256(path.read_bytes()).hexdigest() for path in inputs},
        'matrix': {'parents': len(atoms), 'columns': point['columns'], 'rows': point['rows'],
                   'zero_rows': sum(value == 0 for value in slacks.values()),
                   'zero_joint_rows': sum(value == 0 for row, value in slacks.items() if row.startswith('joint:')),
                   'positive_columns': len(positive), 'positive_parents': len({entry[0] for entry in positive}),
                   'ratio': point['exact_primal_value']},
        'materialized': {'labels': len(labels), 'types': len(counts), 'N': compared, 'W': welfare,
                         'all_exported_types_equal': True, 'verified_last_nodes': 33, 'utility_evaluations': 2145,
                         'all_reported_last_best_reply_lists_equal': True},
        'separate_three_penultimate_witnesses': witnesses,
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
