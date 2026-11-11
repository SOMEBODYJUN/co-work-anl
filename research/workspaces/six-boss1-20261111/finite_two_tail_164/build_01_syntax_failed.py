"""Exact two-player tail on the frozen 164-label finite customer law.

Only this directory is written.  There is no optimizer, six-player strategy
enumeration, or import of any old construction or verification program.
All 720 permutations enter integer dot products; Fraction decides every tie.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import permutations, product
from math import lcm
from pathlib import Path
import json
import time

import numpy as np

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
INPUT = WORK / 'fifth_reply_common/common_atoms_with_D.json'
INPUT_SHA = '91599404ee03184bbb072767d7d55761b95bcc89e1d55e748aebf2ee60f19c54'


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def serial(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): serial(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [serial(v) for v in x]
    if isinstance(x, np.integer):
        return int(x)
    return x


def save(name, x):
    (HERE / name).write_text(json.dumps(serial(x), ensure_ascii=False, indent=2) + '\n')


def main():
    start = time.perf_counter()
    assert digest(INPUT) == INPUT_SHA
    witness = json.loads(INPUT.read_bytes())
    nodes = [e for e in product(range(2), range(6), range(6)) if e[0] == 1 or e[1] != e[2]]
    assert witness['literal_node_order'] == [list(e) for e in nodes]
    assert len(nodes) == 66
    node_ids = {e: k for k, e in enumerate(nodes)}
    labels = []

    def add(name, kind, indices=(), **fields):
        labels.append(dict(id=len(labels), name=name, kind=kind,
                           movable_indices=list(indices), **fields))

    for i in range(6):
        add(f'A{i + 1}', f'A{i + 1}', actual_index=i, bit_source='block.actual_bits[actual_index]')
    for kind, slot in [('T', 0), ('B', 1), ('C', 2)]:
        for i in range(6):
            add(f'{kind}{i + 1}', kind, (i,), word_slot=slot, bit_source='permuted hist word[movable_indices[0]][word_slot]')
    for kind in ('R', 'Z'):
        for e, (family, i, j) in enumerate(nodes):
            add(f'{kind}{family}_{i + 1}_{j + 1}', f'{kind}{family}', (i, j), family=family,
                literal_node_index=e, state_bit=('floor(states[node]/2)' if kind == 'R' else 'states[node] mod 2'))
    for k in (1, 2):
        add(f'H{k}', f'H{k}', B4_index=k - 1, bit_source='atom.B4_state[B4_index]')
    for i in range(6):
        add(f'D{i + 1}', 'D', (i,), bit_source='permuted atom.D_bits[movable_indices[0]]')
    assert len(labels) == 164 and len({d['name'] for d in labels}) == 164
    assert [d['name'] for d in labels[:6]] == [f'A{i}' for i in range(1, 7)]
    counts_by_kind = Counter(d['kind'] for d in labels)

    def signature(*ids):
        renumber = {}
        parts = []
        for i in ids:
            d = labels[i]
            parts.append((d['kind'], tuple(renumber.setdefault(x, len(renumber)) for x in d['movable_indices'])))
        return tuple(parts)

    single_keys = {}
    single_orbits = []
    single_map = []
    for q in range(164):
        key = signature(q)
        if key not in single_keys:
            single_keys[key] = len(single_orbits)
            single_orbits.append(dict(id=len(single_orbits), signature=key, representative=q, members=[]))
        oid = single_keys[key]
        single_orbits[oid]['members'].append(q)
        single_map.append(oid)
    pair_keys = {}
    pair_orbits = []
    pair_map = np.empty((164, 164), dtype=np.int64)
    for q in range(164):
        for r in range(164):
            key = signature(q, r)
            if key not in pair_keys:
                pair_keys[key] = len(pair_orbits)
                pair_orbits.append(dict(id=len(pair_orbits), signature=key, representative=[q, r], size=0))
            oid = pair_keys[key]
            pair_orbits[oid]['size'] += 1
            pair_map[q, r] = oid
    single_reps = np.array([o['representative'] for o in single_orbits], dtype=np.int64)
    pair_reps = np.array([o['representative'] for o in pair_orbits], dtype=np.int64)

    perms = list(permutations(range(6)))
    inverse_slots = np.empty((720, 6), dtype=np.int64)
    inverse_nodes = np.empty((720, 66), dtype=np.int64)
    for row, perm in enumerate(perms):
        for old, new in enumerate(perm):
            inverse_slots[row, new] = old
        for old, (family, i, j) in enumerate(nodes):
            inverse_nodes[row, node_ids[family, perm[i], perm[j]]] = old
    assert len(perms) == 720

    B = [F() for _ in single_orbits]
    J = [F() for _ in pair_orbits]
    atom_records = []
    total = F()
    scale = 1
    literal_equal = np.ones((164, 164), dtype=bool)
    atom_id = 0
    actual_direct = [F(), F()]
    for block in witness['blocks']:
        actual = tuple(map(int, block['actual_bits']))
        assert len(actual) == 6 and set(actual) <= {0, 1}
        p = sum(actual[:4])
        words = [word for word, count in zip(product(range(2), repeat=3), block['hist']) for _ in range(count)]
        assert len(words) == 6
        word_bits = np.array(words, dtype=np.int64)[inverse_slots]
        for within, atom in enumerate(block['atoms']):
            mass = F(atom['mass'])
            assert mass > 0
            assert len(atom['states']) == 66 and set(atom['states']) <= {0, 1, 2, 3}
            assert len(atom['D_bits']) == 6 and set(atom['D_bits']) <= {0, 1}
            assert len(atom['B4_state']) == 3 and set(atom['B4_state']) <= {0, 1}
            ss = np.array(atom['states'], dtype=np.int64)[inverse_nodes]
            dd = np.array(atom['D_bits'], dtype=np.int64)[inverse_slots]
            X = np.empty((720, 164), dtype=np.int64)
            X[:, :6] = actual
            X[:, 6:12] = word_bits[:, :, 0]
            X[:, 12:18] = word_bits[:, :, 1]
            X[:, 18:24] = word_bits[:, :, 2]
            X[:, 24:90] = ss // 2
            X[:, 90:156] = ss % 2
            X[:, 156:158] = atom['B4_state'][:2]
            X[:, 158:164] = dd
            assert X.dtype == np.int64 and np.all((X == 0) | (X == 1))
            c = X.sum(axis=0, dtype=np.int64)
            cc = X.T @ X
            assert cc.dtype == np.int64
            assert np.array_equal(np.diag(cc), c) and np.array_equal(cc, cc.T)
            single_counts = c[single_reps]
            pair_counts = cc[pair_reps[:, 0], pair_reps[:, 1]]
            assert np.array_equal(c, single_counts[np.array(single_map, dtype=np.int64)])
            assert np.array_equal(cc, pair_counts[pair_map])
            literal_equal &= ((c[:, None] + c[None, :] - 2 * cc) == 0)
            for o, count in enumerate(single_counts):
                B[o] += mass * F(int(count), 720 * (p + 1))
            for o, count in enumerate(pair_counts):
                J[o] += mass * F(int(count), 720 * (p + 1) * (p + 2))
            atom_records.append(dict(atom_id=atom_id, hist_column=block['hist_column'], block_atom_index=within,
                                     source_atom_index=atom['source_atom_index'], actual_bits=block['actual_bits'],
                                     prefix_load=p, mass=mass, single_counts=single_counts.tolist(),
                                     ordered_pair_counts=pair_counts.tolist()))
            for i, k in enumerate((4, 5)):
                if actual[k]:
                    actual_direct[i] += mass * F(actual[k], sum(actual))
            total += mass
            scale = lcm(scale, (mass / 720).denominator)
            atom_id += 1
            if atom_id % 10 == 0:
                print(json.dumps(dict(stage='integer_counts_and_exact_orbits', atoms=atom_id,
                                      elapsed_seconds=time.perf_counter() - start)), flush=True)
    assert atom_id == witness['base_atoms'] == 100
    assert 720 * atom_id == witness['expanded_atoms'] == 72000 and total == 1
    assert len(str(scale)) == 595
    literal_B = [B[o] for o in single_map]
    literal_J = [[J[int(pair_map[q, r])] for r in range(164)] for q in range(164)]
    rows = []
    mvalues = []
    for q in range(164):
        terminal_payoffs = [literal_B[r] - literal_J[q][r] for r in range(164)]
        terminal_max = max(terminal_payoffs)
        br = [r for r, value in enumerate(terminal_payoffs) if value == terminal_max]
        maximal_overlap = max(literal_J[q][r] for r in br)
        m = literal_B[q] - maximal_overlap
        punishers = [r for r in br if literal_J[q][r] == maximal_overlap]
        mvalues.append(m)
        rows.append(dict(Q=q, Q_name=labels[q]['name'], B=literal_B[q], terminal_max=terminal_max,
                         BR=br, BR_names=[labels[r]['name'] for r in br],
                         punishment_replies=punishers, punishment_reply_names=[labels[r]['name'] for r in punishers],
                         m=m, m_approx=float(m)))
    M = max(mvalues)
    M_sources = [q for q, m in enumerate(mvalues) if m == M]
    actual_u5 = literal_B[4] - literal_J[4][5]
    actual_u6 = literal_B[5] - literal_J[4][5]
    assert [actual_u5, actual_u6] == actual_direct
    actual_last_is_BR = 5 in rows[4]['BR']
    actual_fifth_ge_M = actual_u5 >= M
    actual_supported = actual_last_is_BR and actual_fifth_ge_M
    possible_pairs = [[q, r] for q in range(164) for r in rows[q]['BR'] if literal_B[q] - literal_J[q][r] >= M]
    assert possible_pairs
    strategy_min = [row['punishment_replies'][0] for row in rows]
    min_source = M_sources[0]
    assert [min_source, strategy_min[min_source]] in possible_pairs
    actual_margins = []
    for r in range(164):
        actual_margins.append(dict(R=r, R_name=labels[r]['name'],
                                   actual_last_minus_reply=actual_u6 - (literal_B[r] - literal_J[4][r])))

    exclusions = []
    for q in range(164):
        if mvalues[q] > actual_u5:
            exclusions.append(q)
    obstruction = None
    if exclusions:
        q = M_sources[0]
        assert q in exclusions
        replies = []
        for r in rows[q]['BR']:
            u5 = literal_B[q] - literal_J[q][r]
            replies.append(dict(R=r, R_name=labels[r]['name'], U5=u5,
                                U6=literal_B[r] - literal_J[q][r],
                                U5_minus_actual= u5 - actual_u5))
        obstruction = dict(Q=q, Q_name=labels[q]['name'], all_best_replies=replies,
                           fifth_payoff_lower_bound=mvalues[q], lower_bound_minus_actual=mvalues[q] - actual_u5,
                           all_forcing_Q=exclusions, all_forcing_Q_names=[labels[q]['name'] for q in exclusions])
    terminal_obstruction = None
    if not actual_last_is_BR:
        terminal_obstruction = dict(all_best_replies=rows[4]['BR'], all_best_reply_names=rows[4]['BR_names'],
                                    gain=rows[4]['terminal_max'] - actual_u6)

    equivalent = []
    used = set()
    for q in range(164):
        if q in used:
            continue
        group = [r for r in range(164) if literal_equal[q, r]]
        used.update(group)
        if len(group) > 1:
            equivalent.append(dict(ids=group, labels=[labels[r]['name'] for r in group]))

    save('labels_and_orbits.json', dict(
        input_sha256=INPUT_SHA, label_count=164, labels=labels, literal_node_order=nodes,
        counts_by_kind=dict(counts_by_kind),
        permutation_convention='For pi in S6, old slot i moves to new slot pi(i); A and H are fixed. R/Z family is fixed.',
        B4_third_coordinate='Directory mean Y; not an action and excluded from the 164 labels.',
        single_orbits=single_orbits, single_orbit_index=single_map,
        ordered_pair_orbits=pair_orbits, ordered_pair_orbit_index=pair_map.tolist(),
        same_coverage_label_classes=equivalent, same_coverage_labels_retained=True,
        repeated_actions_allowed=True))
    save('integer_orbit_counts.json', dict(
        input_sha256=INPUT_SHA, single_orbit_count=len(single_orbits), ordered_pair_orbit_count=len(pair_orbits),
        canonical_atom_count=100, permutation_count=720, expanded_atom_count=72000,
        meaning_single='sum over all 720 pi of the representative label membership bit',
        meaning_pair='sum over all 720 pi of the product of the two representative membership bits',
        all_literal_counts_checked_against_orbit_representatives=True, atoms=atom_records))
    save('matrix_certificate.json', dict(
        input_sha256=INPUT_SHA, labels_and_orbits_sha256=digest(HERE / 'labels_and_orbits.json'),
        integer_orbit_counts_sha256=digest(HERE / 'integer_orbit_counts.json'),
        arithmetic='Exact Fraction; integer int64 720-row 0/1 dot products; no floating comparisons.',
        prefix=['A1', 'A2', 'A3', 'A4'], total_mass=total, unit_customer_scale=str(scale),
        unit_customer_scale_digits=len(str(scale)), unit_scale_rule='Each (canonical atom, permutation) has exactly scale*mass/720 unit customers.',
        B_by_single_orbit=B, J_by_ordered_pair_orbit=J,
        reconstruction=dict(B='B[Q]=B_by_single_orbit[single_orbit_index[Q]]',
                            J='J[Q,R]=J_by_ordered_pair_orbit[ordered_pair_orbit_index[Q][R]]',
                            U5='B[Q]-J[Q,R]', U6='B[R]-J[Q,R]',
                            normalized='All displayed values divide unit-customer payoffs by unit_customer_scale.'),
        direct_atom_reconstruction=dict(B='sum_a mass[a]*single_counts[a,o]/(720*(prefix_load[a]+1))',
                                       J='sum_a mass[a]*ordered_pair_counts[a,o]/(720*(prefix_load[a]+1)*(prefix_load[a]+2))')))
    save('tail_solution.json', dict(
        input_sha256=INPUT_SHA, matrix_certificate_sha256=digest(HERE / 'matrix_certificate.json'),
        comparison_policy='All exact maximizers retained; labels never merged; diagonal actions allowed.',
        rows=rows, M=M, M_approx=float(M), M_sources=M_sources,
        M_source_names=[labels[q]['name'] for q in M_sources],
        actual=dict(Q=4, R=5, Q_name='A5', R_name='A6', U5=actual_u5, U6=actual_u6,
                    U5_approx=float(actual_u5), U6_approx=float(actual_u6), A6_in_BR=actual_last_is_BR,
                    fifth_payoff_ge_M=actual_fifth_ge_M, U5_minus_M=actual_u5 - M,
                    actual_two_tail_is_supported=actual_supported, all_last_reply_margins=actual_margins),
        all_realizable_pairs=possible_pairs, all_realizable_pair_count=len(possible_pairs),
        complete_minimum_value_SPE=dict(fifth_action=min_source, sixth_strategy_by_fifth_action=strategy_min,
                                        fifth_value=M),
        forcing_deviation_certificate=obstruction, terminal_deviation_certificate=terminal_obstruction,
        only_excludes_fixed_instance='An unsupported actual tail excludes only the stated customer law and 164-label directory. Extra labels or other customer couplings may repair it; this is not an SPE counterexample.')))
    summary = dict(status='COMPLETE', input_sha256=INPUT_SHA, producer_sha256=digest(Path(__file__)),
                   canonical_atoms=100, expanded_atoms=72000, labels=164,
                   single_orbits=len(single_orbits), ordered_pair_orbits=len(pair_orbits),
                   literal_matrix_entries=164 * 164, retained_same_coverage_classes=equivalent,
                   actual_supported=actual_supported, actual_A6_in_BR=actual_last_is_BR,
                   actual_U5=actual_u5, actual_U6=actual_u6, M=M, M_minus_actual_U5=M - actual_u5,
                   M_sources=[labels[q]['name'] for q in M_sources],
                   forcing_Q_count=len(exclusions), actual_BR=rows[4]['BR_names'],
                   selected_forcing_Q=(obstruction['Q_name'] if obstruction else None),
                   selected_forcing_Q_BR=([x['R_name'] for x in obstruction['all_best_replies']] if obstruction else []),
                   all_realizable_pair_count=len(possible_pairs),
                   elapsed_seconds=time.perf_counter() - start)
    save('build_summary.json', summary)
    print(json.dumps(serial(summary), ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
