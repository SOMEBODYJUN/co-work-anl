"""Independent literal Fraction audit of the whole 164 x 164 tail.

This program never imports build.py or an older verifier.  It independently
constructs labels, uses FORWARD permutations, evaluates original shares via
the (1,0), (0,1), (1,1) joint membership counts, and checks every literal pair.
An additional per-atom Fraction sum checks each group-orbit representative.
"""
from collections import Counter
from fractions import Fraction as Q
from hashlib import sha256
from itertools import permutations, product
from math import lcm
from pathlib import Path
import json
import time

import numpy as np

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'fifth_reply_common/common_atoms_with_D.json'
EXPECTED_SHA = '91599404ee03184bbb072767d7d55761b95bcc89e1d55e748aebf2ee60f19c54'


def sha(path):
    return sha256(path.read_bytes()).hexdigest()


def encode(x):
    if isinstance(x, Q):
        return str(x)
    if isinstance(x, dict):
        return {str(k): encode(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [encode(v) for v in x]
    if isinstance(x, np.integer):
        return int(x)
    return x


def main():
    start = time.perf_counter()
    assert sha(SOURCE) == EXPECTED_SHA
    data = json.loads(SOURCE.read_bytes())
    mapping = json.loads((HERE / 'labels_and_orbits.json').read_bytes())
    counts = json.loads((HERE / 'integer_orbit_counts.json').read_bytes())
    matrix = json.loads((HERE / 'matrix_certificate.json').read_bytes())
    answer = json.loads((HERE / 'tail_solution.json').read_bytes())
    assert all(d['input_sha256'] == EXPECTED_SHA for d in (mapping, counts, matrix, answer))
    assert matrix['labels_and_orbits_sha256'] == sha(HERE / 'labels_and_orbits.json')
    assert matrix['integer_orbit_counts_sha256'] == sha(HERE / 'integer_orbit_counts.json')
    assert answer['matrix_certificate_sha256'] == sha(HERE / 'matrix_certificate.json')

    node_order = [(f, i, j) for f in (0, 1) for i in range(6) for j in range(6) if f != 0 or i != j]
    assert data['literal_node_order'] == [list(n) for n in node_order]
    names = [f'A{k}' for k in range(1, 7)]
    names += [f'{kind}{k}' for kind in ('T', 'B', 'C') for k in range(1, 7)]
    names += [f'{kind}{f}_{i+1}_{j+1}' for kind in ('R', 'Z') for f, i, j in node_order]
    names += ['H1', 'H2'] + [f'D{k}' for k in range(1, 7)]
    assert len(names) == 164 and len(set(names)) == 164
    assert [d['name'] for d in mapping['labels']] == names
    assert [d['id'] for d in mapping['labels']] == list(range(164))
    assert sum(n.startswith('R') for n in names) == 66
    assert sum(n.startswith('Z') for n in names) == 66
    label_id = {name: i for i, name in enumerate(names)}
    permutation_list = list(permutations(range(6)))

    # Independent forward action: an old named membership bit moves to its
    # new named label; no inverse-slot or inverse-node arrays are reused.
    forward = np.empty((720, 164), dtype=np.int64)
    for row, permutation in enumerate(permutation_list):
        for i, name in enumerate(names):
            kind = name[0]
            if kind in ('A', 'H'):
                destination = name
            elif kind in ('T', 'B', 'C', 'D'):
                destination = kind + str(permutation[int(name[1:]) - 1] + 1)
            else:
                head, left, right = name.split('_')
                destination = f'{head}_{permutation[int(left)-1]+1}_{permutation[int(right)-1]+1}'
            forward[row, i] = label_id[destination]
        assert sorted(forward[row].tolist()) == list(range(164))

    single_map = np.asarray(mapping['single_orbit_index'], dtype=np.int64)
    pair_map = np.asarray(mapping['ordered_pair_orbit_index'], dtype=np.int64)
    assert single_map.shape == (164,) and pair_map.shape == (164, 164)
    single_reps = [o['representative'] for o in mapping['single_orbits']]
    pair_reps = [o['representative'] for o in mapping['ordered_pair_orbits']]
    for orbit in mapping['single_orbits']:
        images = set(forward[:, orbit['representative']].tolist())
        assert images == set(orbit['members'])
        assert all(single_map[i] == orbit['id'] for i in images)
    for orbit in mapping['ordered_pair_orbits']:
        i, j = orbit['representative']
        images = set(zip(forward[:, i].tolist(), forward[:, j].tolist()))
        assert len(images) == orbit['size']
        assert all(pair_map[q, r] == orbit['id'] for q, r in images)
        assert np.count_nonzero(pair_map == orbit['id']) == orbit['size']

    all_atoms = []
    scale = 1
    total = Q()
    for block in data['blocks']:
        for atom in block['atoms']:
            mass = Q(atom['mass'])
            assert mass > 0
            scale = lcm(scale, (mass / 720).denominator)
            total += mass
            all_atoms.append((block, atom))
    assert len(all_atoms) == 100 and total == 1
    assert str(scale) == matrix['unit_customer_scale'] and len(str(scale)) == 595

    fifth_scaled = np.zeros((164, 164), dtype=object)
    sixth_scaled = np.zeros((164, 164), dtype=object)
    B_scaled = np.zeros(164, dtype=object)
    direct_fraction5 = [Q() for _ in pair_reps]
    direct_fraction6 = [Q() for _ in pair_reps]
    prefix_loads = Counter()
    independent_same = np.ones((164, 164), dtype=bool)
    replication_total = 0
    integer_count_checks = 0

    for atom_number, (block, atom) in enumerate(all_atoms):
        actual = [int(c) for c in block['actual_bits']]
        prefix_load = sum(actual[:4])
        prefix_loads[prefix_load] += 1
        words = []
        for code, number in enumerate(block['hist']):
            words.extend([((code >> 2) & 1, (code >> 1) & 1, code & 1)] * number)
        assert len(words) == 6
        base = actual.copy()
        base.extend(words[i][slot] for slot in range(3) for i in range(6))
        base.extend(int(state >= 2) for state in atom['states'])
        base.extend(int(state in (1, 3)) for state in atom['states'])
        base.extend(atom['B4_state'][0:2])
        base.extend(atom['D_bits'])
        assert len(base) == 164 and all(v in (0, 1) for v in base)
        members = np.empty((720, 164), dtype=np.int64)
        members[np.arange(720)[:, None], forward] = np.asarray(base, dtype=np.int64)[None, :]
        n11 = members.T @ members
        n10 = members.T @ (1 - members)
        n01 = n10.T
        single = members.sum(axis=0, dtype=np.int64)
        assert np.array_equal(n11, n11.T)
        assert np.array_equal(np.diag(n11), single)
        assert np.all(n10 + n11 == single[:, None])
        assert np.all(n01 + n11 == single[None, :])
        assert np.all(n11 >= 0) and np.all(n11 <= 720)
        independent_same &= (n10 + n01 == 0)

        record = counts['atoms'][atom_number]
        assert record['atom_id'] == atom_number
        assert record['hist_column'] == block['hist_column']
        assert record['mass'] == atom['mass']
        assert record['prefix_load'] == prefix_load
        assert record['single_counts'] == single[single_reps].tolist()
        assert record['ordered_pair_counts'] == [int(n11[i, j]) for i, j in pair_reps]
        assert np.array_equal(single, np.asarray(record['single_counts'], dtype=np.int64)[single_map])
        assert np.array_equal(n11, np.asarray(record['ordered_pair_counts'], dtype=np.int64)[pair_map])
        integer_count_checks += 164 + 164 * 164

        mass = Q(atom['mass'])
        count_per_permutation = mass * scale / 720
        assert count_per_permutation.denominator == 1 and count_per_permutation > 0
        number_units = count_per_permutation.numerator
        replication_total += 720 * number_units
        # These are the original payoff formulas: q=1,r=0 pays 1/(p+1)
        # and q=r=1 pays 1/(p+2).  60 is a common multiple of 1,...,6.
        coef5 = n10 * (60 // (prefix_load + 1)) + n11 * (60 // (prefix_load + 2))
        coef6 = n01 * (60 // (prefix_load + 1)) + n11 * (60 // (prefix_load + 2))
        fifth_scaled += coef5.astype(object) * number_units
        sixth_scaled += coef6.astype(object) * number_units
        B_scaled += (single * (60 // (prefix_load + 1))).astype(object) * number_units
        for oi, (q, r) in enumerate(pair_reps):
            direct_fraction5[oi] += (mass / 720) * (Q(int(n10[q, r]), prefix_load + 1) + Q(int(n11[q, r]), prefix_load + 2))
            direct_fraction6[oi] += (mass / 720) * (Q(int(n01[q, r]), prefix_load + 1) + Q(int(n11[q, r]), prefix_load + 2))
        if (atom_number + 1) % 10 == 0:
            print(json.dumps(dict(stage='independent_forward_literal_payoffs', atoms=atom_number+1,
                                  elapsed_seconds=time.perf_counter() - start)), flush=True)
    assert replication_total == scale

    saved_B = [Q(matrix['B_by_single_orbit'][int(o)]) for o in single_map]
    saved_J = [Q(v) for v in matrix['J_by_ordered_pair_orbit']]
    B = [Q(int(n), 60 * scale) for n in B_scaled]
    assert B == saved_B
    fifth = []
    sixth = []
    literal_fraction_checks = 0
    matrix_hash = sha256()
    for q in range(164):
        fiverow = []
        sixrow = []
        for r in range(164):
            u5 = Q(int(fifth_scaled[q, r]), 60 * scale)
            u6 = Q(int(sixth_scaled[q, r]), 60 * scale)
            j = saved_J[int(pair_map[q, r])]
            assert u5 == B[q] - j and u6 == B[r] - j
            assert u5 == direct_fraction5[int(pair_map[q, r])]
            assert u6 == direct_fraction6[int(pair_map[q, r])]
            assert u5 - u6 == B[q] - B[r]
            fiverow.append(u5)
            sixrow.append(u6)
            matrix_hash.update(f'{q},{r},{u5},{u6}\n'.encode())
            literal_fraction_checks += 1
        fifth.append(fiverow)
        sixth.append(sixrow)
    assert np.array_equal(fifth_scaled.T, sixth_scaled)
    actual_share5 = Q()
    actual_share6 = Q()
    for block, atom in all_atoms:
        bits = [int(c) for c in block['actual_bits']]
        if bits[4]:
            actual_share5 += Q(atom['mass']) / sum(bits)
        if bits[5]:
            actual_share6 += Q(atom['mass']) / sum(bits)
    assert fifth[4][5] == actual_share5 == Q(answer['actual']['U5'])
    assert sixth[4][5] == actual_share6 == Q(answer['actual']['U6'])

    rows = []
    all_m = []
    all_br = []
    strategy = []
    for q in range(164):
        value = max(sixth[q])
        best = [r for r in range(164) if sixth[q][r] == value]
        minimum = min(fifth[q][r] for r in best)
        punish = [r for r in best if fifth[q][r] == minimum]
        stored = answer['rows'][q]
        assert stored['Q'] == q and stored['Q_name'] == names[q]
        assert best == stored['BR'] and [names[r] for r in best] == stored['BR_names']
        assert punish == stored['punishment_replies']
        assert minimum == Q(stored['m']) and value == Q(stored['terminal_max'])
        all_m.append(minimum)
        all_br.append(best)
        strategy.append(punish[0])
        rows.append(dict(Q=q, name=names[q], BR=best, BR_names=[names[r] for r in best],
                         original_payoff_terminal_max=value, m=minimum,
                         all_BR_fifth_payoffs=[fifth[q][r] for r in best]))
    M = max(all_m)
    sources = [q for q in range(164) if all_m[q] == M]
    assert M == Q(answer['M']) and sources == answer['M_sources']
    pairs = [[q, r] for q in range(164) for r in all_br[q] if fifth[q][r] >= M]
    assert pairs == answer['all_realizable_pairs'] and len(pairs) == answer['all_realizable_pair_count']
    supported = 5 in all_br[4] and actual_share5 >= M
    assert supported == answer['actual']['actual_two_tail_is_supported']
    assert strategy == answer['complete_minimum_value_SPE']['sixth_strategy_by_fifth_action']
    assert fifth[sources[0]][strategy[sources[0]]] == M
    assert all(fifth[q][strategy[q]] <= M for q in range(164))

    # Check every saved forced deviation, plus all omitted labels, against
    # the independently evaluated original utilities and complete BR sets.
    forcing = [q for q in range(164) if all_m[q] > actual_share5]
    obstruction = answer['forcing_deviation_certificate']
    if forcing:
        assert obstruction is not None and obstruction['all_forcing_Q'] == forcing
        q = obstruction['Q']
        assert q in forcing
        assert [d['R'] for d in obstruction['all_best_replies']] == all_br[q]
        assert Q(obstruction['fifth_payoff_lower_bound']) == min(fifth[q][r] for r in all_br[q])
        assert Q(obstruction['lower_bound_minus_actual']) == all_m[q] - actual_share5 > 0
        for record in obstruction['all_best_replies']:
            r = record['R']
            assert Q(record['U5']) == fifth[q][r]
            assert Q(record['U6']) == sixth[q][r]
            assert Q(record['U5_minus_actual']) == fifth[q][r] - actual_share5 > 0
    else:
        assert obstruction is None
    for r, record in enumerate(answer['actual']['all_last_reply_margins']):
        assert record['R'] == r
        assert Q(record['actual_last_minus_reply']) == actual_share6 - sixth[4][r]

    equal_classes = []
    consumed = set()
    for q in range(164):
        if q in consumed:
            continue
        group = [r for r in range(164) if independent_same[q, r]]
        consumed.update(group)
        if len(group) > 1:
            equal_classes.append(dict(ids=group, labels=[names[r] for r in group]))
    assert equal_classes == mapping['same_coverage_label_classes']
    assert sha(SOURCE) == EXPECTED_SHA

    report = dict(
        status='PASS', input_sha256=EXPECTED_SHA, verifier_sha256=sha(Path(__file__)),
        proof_audit_scope='The iff criterion is valid for the two-player subgame after the fixed ordered length-four prefix.',
        arithmetic='Independent forward permutation; original-share n10/(p+1)+n11/(p+2); all literal cells converted to Fraction; extra direct per-atom Fraction sums for every pair orbit.',
        labels=164, canonical_atoms=100, expanded_atoms=72000, positive_unit_replication=True,
        unit_customer_scale=str(scale), unit_customer_scale_digits=len(str(scale)),
        single_orbits=len(single_reps), ordered_pair_orbits=len(pair_reps),
        group_orbits_independently_verified=True, prefix_load_atom_counts=dict(prefix_loads),
        literal_integer_count_checks=integer_count_checks, literal_fraction_matrix_checks=literal_fraction_checks,
        direct_per_atom_pair_orbit_fraction_checks=2 * len(pair_reps) * 100,
        row_major_original_payoff_matrix_sha256=matrix_hash.hexdigest(),
        actual_U5=actual_share5, actual_U6=actual_share6, actual_A6_in_BR=(5 in all_br[4]),
        actual_supported=supported, M=M, M_minus_actual_U5=M-actual_share5,
        M_sources=sources, M_source_names=[names[q] for q in sources],
        forcing_labels=[names[q] for q in forcing], all_realizable_pair_count=len(pairs),
        exact_literal_BR_and_m=rows,
        direct_fraction_by_pair_orbit=[dict(orbit=o, representative=pair_reps[o], U5=direct_fraction5[o], U6=direct_fraction6[o]) for o in range(len(pair_reps))],
        same_coverage_classes_retained=equal_classes,
        scope='Only the frozen customer law and complete specified 164-label directory at prefix A1,A2,A3,A4. Extra labels or other couplings may repair the failed actual tail. No SPE counterexample or resolution of six-player 2W>=OPT6.',
        elapsed_seconds=time.perf_counter() - start)
    (HERE / 'independent_verification.json').write_text(json.dumps(encode(report), ensure_ascii=False, indent=2) + '\n')
    concise = {k: v for k, v in report.items() if k not in ('unit_customer_scale', 'exact_literal_BR_and_m', 'direct_fraction_by_pair_orbit')}
    print(json.dumps(encode(concise), ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
