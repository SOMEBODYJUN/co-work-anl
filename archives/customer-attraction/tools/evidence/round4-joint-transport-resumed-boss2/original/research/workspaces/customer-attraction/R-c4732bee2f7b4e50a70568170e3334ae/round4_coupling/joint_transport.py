"""Exact shared-incidence rearrangement cuts for genuine final-player nodes.

The theorem is arbitrary q/background; the frozen-point evaluation is only
an illustration. No computation below is an unrestricted welfare bound.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement, permutations, product
from pathlib import Path
import hashlib
import json

ROOT = next(p for p in Path(__file__).resolve().parents
            if (p / 'customer_attraction/__init__.py').exists())
ACTOR = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'evidence/certificates/customer_attraction/five_player_indexed_bound.json'
AUGMENTED = ACTOR / 'continuation_completion/frozen_support_augmented.json'


def family(atom, label):
    arity = 4 if label == 'second' else 3
    return [bits for bits, n in zip(product((0, 1), repeat=arity), atom[label + '_hist'])
            for _ in range(n)]


def source_data(atom, label):
    a, b, c, d, e, *_ = map(int, atom['bits'])
    data = family(atom, label)
    own, inv = F(0), [[], []]
    for bits in data:
        prefix = a + (b if label == 'AB' else e) if label != 'second' else a
        den = prefix + sum(bits[:-1]) + 1
        own += F(bits[-1], den)
        inv[bits[0]].append(F(1, den))
    return own, inv


def transport_max(inv, target, components, brute=False):
    """components: (position, kind, positive weight), kind D or O.

    D is the diagonal comparison, O the offdiagonal comparison. The
    coupling-dependent sign is - for D and + for O.
    """
    out = F(0)
    for t in (0, 1):
        scores = [sum((weight * (-1 if kind == 'D' else 1) * bits[pos]
                       for pos, kind, weight in components), F(0))
                  for bits in target if bits[0] == t]
        assert len(scores) == len(inv[t])
        if brute:
            out += max((sum((d * s for d, s in zip(inv[t], perm)), F(0))
                        for perm in set(permutations(scores))), default=F(0))
        else:
            out += sum((d * s for d, s in zip(sorted(inv[t]), sorted(scores))), F(0))
    return out


def joint_row(atom, source, target_label, components, brute=False):
    own, inv = source_data(atom, source)
    target = family(atom, target_label)
    q = len(target)
    weight_own = sum((weight * (1 if kind == 'D' else q - 1)
                      for _, kind, weight in components), F(0))
    off_membership = sum((weight * sum(bits[pos] for bits in target)
                          for pos, kind, weight in components if kind == 'O'), F(0))
    return weight_own * own - off_membership * sum(inv[0] + inv[1], F(0)) \
        + transport_max(inv, target, components, brute)


def row_specs():
    for source, target in product(('AB', 'AE', 'second'), repeat=2):
        if source == target:
            continue
        positions = range(1, 4 if target == 'second' else 3)
        choices = list(product(positions, ('D', 'O')))
        for first, second in combinations_with_replacement(choices, 2):
            if first == second:
                continue
            for weight in (F(1), F(2), F(3)):
                components = ((first[0], first[1], F(1)), (second[0], second[1], weight))
                name = f'{source}:{target}:{first[0]}{first[1]}+{weight}*{second[0]}{second[1]}'
                yield name, source, target, components


def audit_rearrangement():
    checks = 0
    # Both conditioning groups and zero/one/two target overlaps occur.
    for q in (1, 2, 3, 4):
        for target in product(tuple(product((0, 1), repeat=2)), repeat=q):
            lifted = [(0, *bits) for bits in target]
            for pattern in ((1, 2), (2, 3), (1, 3, 5)):
                inv = [[F(1, pattern[i % len(pattern)]) for i in range(q)], []]
                for kinds in product(('D', 'O'), repeat=2):
                    for weight in (F(1), F(2)):
                        components = ((1, kinds[0], F(1)), (2, kinds[1], weight))
                        assert transport_max(inv, lifted, components) == \
                            transport_max(inv, lifted, components, brute=True)
                        checks += 1
    return checks


def strict_example():
    # All shared t bits are zero. Source denominators are 1,2 and last
    # action bits are 0,1, so own=1/2. Target menus partition the indices.
    atom = {'bits': '0000000000',
            'AB_hist': [1, 0, 0, 1, 0, 0, 0, 0],
            'AE_hist': [0, 1, 1, 0, 0, 0, 0, 0]}
    rows = {f'{pos}{kind}': joint_row(atom, 'AB', 'AE', ((pos, kind, F(1)),))
            for pos in (1, 2) for kind in ('D', 'O')}
    joint = joint_row(atom, 'AB', 'AE', ((1, 'O', F(1)), (2, 'O', F(1))))
    assert set(rows.values()) == {F(0)}
    assert joint == -F(1, 2)
    return {'scope': 'Strictly stronger than four separately optimized cross-family rows; '
                     'not a feasible point for the full preexisting SPE relaxation',
            'single_envelopes': {k: str(v) for k, v in rows.items()},
            'joint_two_offdiagonal': str(joint), 'atom': atom}


def frozen_report(atoms, masses):
    useful = {}
    negative = {}
    all_checks = 0
    max_gain = F(0)
    for name, source, target, components in row_specs():
        joint_total = F(0)
        separate_totals = [F(0), F(0)]
        for atom, mass in zip(atoms, masses):
            value = joint_row(atom, source, target, components)
            # Fixed target-state multiset: literal all-permutation maximum.
            assert value == joint_row(atom, source, target, components, brute=True)
            single = [joint_row(atom, source, target, (component,)) for component in components]
            assert value <= sum(single, F(0))
            joint_total += mass * value
            for j in range(2):
                separate_totals[j] += mass * single[j]
            all_checks += 1
        gain = sum(separate_totals, F(0)) - joint_total
        max_gain = max(max_gain, gain)
        if joint_total < 0:
            negative[name] = str(joint_total)
            if min(separate_totals) >= 0:
                useful[name] = {'joint_slack': str(joint_total),
                                'component_slacks': list(map(str, separate_totals)),
                                'independent_optimization_excess': str(gain)}
    return {'row_count': len(list(row_specs())), 'literal_matching_checks': all_checks,
            'negative_rows': negative,
            'negative_despite_both_component_envelopes_nonnegative': useful,
            'maximum_independent_optimization_excess': str(max_gain)}


def main():
    original = json.loads(SOURCE.read_text())['primal']
    augmented = json.loads(AUGMENTED.read_text())
    report = {'scope': 'General necessary shared-incidence inequalities, exact finite '
                        'verification and frozen-point illustration; Q-CAG-HALF remains OPEN',
              'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              'augmented_sha256': hashlib.sha256(AUGMENTED.read_bytes()).hexdigest(),
              'rearrangement_exact_checks': audit_rearrangement(),
              'strict_example': strict_example(), 'frozen': {}}
    for label, atoms, masses in [
        ('original_64', original['atoms'],
         [F(z['mass_numerator'], original['denominator']) for z in original['atoms']]),
        ('augmented_42', augmented['atoms'], [F(z['exact_mass']) for z in augmented['atoms']])]:
        report['frozen'][label] = frozen_report(atoms, masses)
    Path(__file__).with_suffix('.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({**report, 'frozen': {name: {key: val for key, val in data.items()
                                                if key != 'negative_rows'}
                                         for name, data in report['frozen'].items()}}, indent=2))


if __name__ == '__main__':
    main()
