"""Independent standard-library literal six-root audit.

Certificate mode imports no discovery, recovery, compressed model or solver.
The optional small-domain test compares this literal implementation against the
compressed model. All 30 ordered different-root pairs are read literally.
"""
import argparse
from collections import defaultdict
from fractions import Fraction as F
import hashlib
from itertools import combinations_with_replacement
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUN = HERE.parent
PIN = 'd70c26065d42fd73dedc94183e4533dd6f8608d5841f7a6018ff180dc77e2f9f'


def q(a, b):
    return F(a, b) if a else F(0)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_data():
    p = RUN / 'peer_augmented_lp/augmented_lp_exact.json'
    assert digest(p) == PIN
    original = json.loads(p.read_text())
    hist = [x for x in original['columns'] if x['kind'] == 'hist']
    mu = defaultdict(F)
    for x in hist:
        mu[x['actual_bits'], x['d']] += F(x['weight'])
    mu = {k: v for k, v in sorted(mu.items()) if v}
    k = next(F(x['weight']) for x in original['columns'] if x['kind'] == 'K')
    u = [sum(v * q(int(a[i]), sum(map(int, a))) for (a, d), v in mu.items()) for i in range(6)]
    assert sum(u) == F(original['W'])
    table = {}
    for b in range(2):
        rows = json.loads((RUN / f'background_five_bridge/fixed53_b{b}_profit.json').read_text())
        for x in rows['min_by_actual_and_d']:
            table[b, x['actual'], x['d']] = F(x['min_rho'])
    return original, hist, mu, k, u, table


def literal(actual, d, records, table, extended=True):
    assert len(records) == 6 and sum(t for t, e in records) == d
    a = list(map(int, actual))
    coefficients = {}
    root = sum(q(t, t + sum(e)) for t, e in records) / 6
    coefficients['gamma',] = sum(-2 * q(sum(e), t + sum(e))
                                       + table[t, ''.join(map(str, e)), d - t] for t, e in records) / 6
    for k in range(5):
        coefficients['price', k] = sum(q(e[k], sum(a[:5]) + 1) for t, e in records) / 6
        coefficients['capacity', k] = sum(F(e[k]) for t, e in records) / 6
        for i in range(6):
            coefficients['floor-actual', k, i] = sum(q(a[i], t + sum(e[:k]) + 5 - k)
                                                     - q(e[k], t + sum(e)) for t, e in records) / 6
        coefficients['floor-other-opt', k] = sum(q(d - t, t + sum(e[:k]) + 5 - k)
                                                - 5 * q(e[k], t + sum(e)) for t, e in records) / 6
        coefficients['floor-root', k] = sum(q(t, t + sum(e[:k]) + 5 - k)
                                           - q(e[k], t + sum(e)) for t, e in records) / 6
        for l in range(5):
            if k != l:
                coefficients['floor-own-tail', k, l] = sum(q(e[l], t + sum(e[:k]) + 5 - k)
                                                           - q(e[k], t + sum(e)) for t, e in records) / 6
            value = F(0)
            for j, (t, e) in enumerate(records):
                for i, (s, f) in enumerate(records):
                    if i != j:
                        value += q(f[l], t + sum(e[:k]) + 5 - k) - q(e[k], t + sum(e))
            coefficients['cross-floor', k, l] = value / 6
    if extended:
        for l in range(6):
            for m in range(l, 6):
                value = F(0)
                for j, (t, e) in enumerate(records):
                    p = t + sum(e[:3])
                    h = q(e[3] + e[4], t + sum(e)) + q(e[3], (p + 1) * (p + 2))
                    for i, (s, f) in enumerate(records):
                        if i != j:
                            v = (s,) + tuple(f)
                            value += -h + q(v[l] + v[m], p + 1) - q(v[l] * v[m], (p + 1) * (p + 2))
                coefficients['cross-pair', l, m] = value / 30
                ap = sum(a[:4])
                coefficients['actual-pair', l, m] = sum(q(((t,) + tuple(e))[l] + ((t,) + tuple(e))[m], ap + 1)
                    - q(((t,) + tuple(e))[l] * ((t,) + tuple(e))[m], (ap + 1) * (ap + 2)) for t, e in records) / 6
        for i in range(5):
            for k in range(5):
                coefficients['actual-floor', i, k] = sum(q(e[k], sum(a[:i]) + 6 - i) for t, e in records) / 6
    assert len(coefficients) == (163 if extended else 96)
    return root, coefficients


def expected_budget(name, mu, cap, pay, o):
    typ = name[0]
    if typ == 'gamma':
        return -F(226487, 10**21) * cap - F(5, 6) * o
    if typ == 'price':
        return pay[5]
    if typ == 'capacity':
        return cap
    if typ == 'actual-floor':
        return pay[name[1]]
    if typ == 'actual-pair':
        return pay[4] + pay[5] + sum(m * q(int(a[4]), (sum(map(int, a[:4])) + 1)
                                          * (sum(map(int, a[:4])) + 2)) for (a, d), m in mu.items())
    return F(0)


def check_certificate(path):
    original, hist, mu, cap, pay, table = read_data()
    cert = json.loads(path.read_text())
    assert cert['point_sha256'] == PIN
    marginal = defaultdict(F)
    costs = defaultdict(F)
    root = F(0)
    for atom in cert['support']:
        mass = F(atom['mass'])
        assert mass >= 0
        a, d = atom['actual'], atom['d']
        assert d == 1 and len(atom['zero_words']) == 5
        assert atom['zero_words'] == sorted(atom['zero_words'])
        words = [atom['one_word']] + atom['zero_words']
        records = [(int(i == 0), tuple(map(int, f'{w:05b}'))) for i, w in enumerate(words)]
        r, b = literal(a, d, records, table, cert['extended'])
        marginal[a, d] += mass
        root += mass * r
        for name, val in b.items():
            costs[name] += mass * val
    assert dict(marginal) == mu
    slacks = {}
    saved = {tuple(x['row']): x for x in cert['budget_slacks']}
    for name, cost in costs.items():
        budget = expected_budget(name, mu, cap, pay, F(original['O']))
        slack = budget - cost
        assert slack >= 0, (name, slack)
        assert budget == F(saved[name]['budget']) and slack == F(saved[name]['slack'])
        slacks[name] = slack
    assert len(saved) == len(costs) == cert['budget_count']
    assert root == F(cert['root_cost']) and pay[0] == F(cert['root_budget'])
    gap = pay[0] - root
    assert gap > 0 and gap == F(cert['root_slack'])
    for source in cert['sources']:
        assert digest(RUN / source['path']) == source['sha256']
    # Exact product refinement preserves EACH original hist record, including
    # distinct old histograms with identical actual bits. It adds no identities.
    refined_path = HERE / 'original_hist_refinement_exact.json'
    refined = json.loads(refined_path.read_text())
    assert refined['point_sha256'] == PIN and refined['joint_completion_sha256'] == digest(path)
    refined_map = {(v['original_column_index'], v['joint_atom_index']): v for v in refined['atoms']}
    assert len(refined_map) == len(refined['atoms'])
    expected_original_hist = [{'original_column_index': i, **record} for i, record in enumerate(original['columns'])
                              if record['kind'] == 'hist']
    assert refined['original_hist_records'] == expected_original_hist
    lifted_atoms = 0
    joint_refined_marginal = defaultdict(F)
    for index, record in enumerate(original['columns']):
        if record['kind'] != 'hist':
            continue
        mass = F(record['weight'])
        if not mass:
            continue
        key = (record['actual_bits'], record['d'])
        total = F(0)
        for atom_index, atom in enumerate(cert['support']):
            if (atom['actual'], atom['d']) == key:
                value = mass * F(atom['mass']) / mu[key]
                assert value >= 0
                entry = refined_map[index, atom_index]
                assert F(entry['mass']) == value and entry['old_hist'] == record['hist']
                assert entry['one_word'] == atom['one_word'] and entry['zero_words'] == atom['zero_words']
                assert (entry['actual'], entry['d']) == key
                total += value
                joint_refined_marginal[atom_index] += value
                lifted_atoms += int(value > 0)
        assert total == mass
    assert lifted_atoms == len(refined['atoms']) == 25
    for i, atom in enumerate(cert['support']):
        assert joint_refined_marginal[i] == F(atom['mass'])
    frozen_input = json.loads((HERE / 'projection_inputs_exact.json').read_text())
    assert frozen_input['point_sha256'] == PIN and frozen_input['original_hist_records'] == expected_original_hist
    assert F(frozen_input['O']) == F(original['O']) and F(frozen_input['W']) == sum(pay)
    assert F(frozen_input['K']) == cap and list(map(F, frozen_input['u'])) == pay
    frozen_table = {(v['t'], f"{v['word']:05b}", v['comparison_count']): F(v['value'])
                    for v in frozen_input['remainder_table']}
    assert frozen_table == table
    report = {'status': 'INDEPENDENT STANDARD-LIBRARY SIX-ROOT JOINT AUDIT PASSED',
              'point_sha256': PIN, 'certificate_sha256': digest(path),
              'original_hist_refinement_sha256': digest(refined_path),
              'support_atoms': len(cert['support']), 'contexts': len(mu),
              'budget_rows': len(costs), 'root_source_rows': 1,
              'zero_budget_slacks': sum(v == 0 for v in slacks.values()),
              'root_slack': str(gap), 'root_slack_float': float(gap),
              'old_hist_product_refinement_atoms': lifted_atoms,
              'scope': 'Declared shared-customer projection only; no complete SPE, no general half conclusion.'}
    (HERE / 'joint_completion_audit.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


def check_small_domain():
    # Deliberately optional: the certificate verifier above never imports this.
    from contract import compressed_column, row_names, directed_pair_cost, single_root_local
    _, _, _, _, _, table = read_data()
    rem = {(t, int(e, 2), d): value for (t, e, d), value in table.items()}
    names = row_names(True)
    words = (0, 3, 17)
    count = 0
    per_d = {}
    for d in range(7):
        per_d[d] = 0
        for one in combinations_with_replacement(words, d):
            for zero in combinations_with_replacement(words, 6 - d):
                roots = [(1, w) for w in one] + [(0, w) for w in zero]
                records = [(t, tuple(map(int, f'{w:05b}'))) for t, w in roots]
                # Alternate actual contexts, preserving full coefficients.
                actual = ('000000', '100011', '111100')[count % 3]
                r, b = literal(actual, d, records, table, True)
                cr, cb = compressed_column(actual, d, roots, names, rem)
                assert r == cr and cb == [b[name] for name in names]
                # Check the local + 15 unordered-pair representation too.
                lr = F(0)
                lb = [F(0)] * len(names)
                for t, w in roots:
                    rr, bb = single_root_local(actual, d, t, w, names, rem)
                    lr += rr
                    lb = [x + y for x, y in zip(lb, bb)]
                for i in range(6):
                    for j in range(i + 1, 6):
                        x = directed_pair_cost(*roots[i], *roots[j], names)
                        y = directed_pair_cost(*roots[j], *roots[i], names)
                        lb = [a + b + c for a, b, c in zip(lb, x, y)]
                assert lr == r and lb == cb
                count += 1
                per_d[d] += 1
    assert count == 462
    report = {'status': 'SMALL COMPLETE ORBIT DOMAIN: LITERAL = COUNTS = PAIRWISE',
              'tail_word_domain': list(words), 'root_count': 6, 'd_values': list(range(7)),
              'columns': count, 'per_d_counts': per_d, 'rows_per_column': len(names),
              'exact_coefficient_checks': count * len(names),
              'scope': 'Complete 3-word orbit domain, not the full 32-word pricing domain.'}
    (HERE / 'small_domain_audit.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--small-domain', action='store_true')
    parser.add_argument('--certificate', default='joint_completion_exact.json')
    args = parser.parse_args()
    if args.small_domain:
        check_small_domain()
    else:
        check_certificate(HERE / args.certificate)
