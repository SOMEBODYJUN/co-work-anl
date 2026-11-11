"""Independent standard-library literal audit at the NEW exact point.

No constructor, sibling formula module, optimizer or third-party package is
imported.  All 32 candidate columns are independently evaluated at all 240
rows, including root source.  All old and root labelled vector margins use
explicit simultaneous S6 orbits.  Pair-index orbit counts are checked once
for all 36 named (i,j), avoiding millions of repeated rational evaluations.
The 36 new rows also keep separate source payoff, one source tax, query f,
and SAME-donor query overlap g, with every part checked exactly.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import permutations, product
from math import lcm
from pathlib import Path
import hashlib
import json
import sys
import time

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
PIN = 'b0ca65cfe61e5e3ef09537cba2a986c171aeaa7106f673077f803c80ee2b68e3'
PERMS = tuple(permutations(range(6)))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def q(n, d):
    return F(n, d) if n else F(0)


def bits(word, width):
    return tuple((word >> (width-1-k)) & 1 for k in range(width))


def families():
    single = ([('C-to-Y', k) for k in range(5)]+[('Y5-to-C',)]
              +[('B-to-Y', k) for k in range(5)]
              +[('Y-to-old', k, v) for k in range(4) for v in ('B', 'C')]
              +[('Y5-to-B',)])
    pair = ([('old-pair-to-Y', l, m) for l in range(5) for m in range(l, 5)]
            +[('new-pair-to-old', v, w) for v, w in (('B', 'B'), ('B', 'C'), ('C', 'C'))])
    assert len(single) == 20 and len(pair) == 18
    return single, pair


def true_pair_payoffs(background, first, last):
    # These positive-denominator expressions use the original two players'
    # separate literal payoffs, rather than the constructor's combined share.
    payoff = F(first, background+1+last)+F(last, background+1+first)
    tax = F(first, (background+1)*(background+2))
    return payoff, tax


def interface_literals(atom):
    """All 38 families times 36 named queries before symmetrization."""
    old = [bits(w, 3) for w in atom['old_words']]
    new = [bits(e, 5) for e in atom['new_words']]
    p3 = sum(int(c) for c in atom['actual'][:3])
    one, pair = families()
    values, pieces = {}, {}
    for i in range(6):
        t, b, c = old[i]
        p = p3+t
        opay, otax = true_pair_payoffs(p, b, c)
        for j in range(6):
            s, e = old[j][0], new[j]
            total = s+sum(e)
            for k in range(5):
                values[('C-to-Y', k), i, j] = F(c-e[k], p+b+1)
                values[('B-to-Y', k), i, j] = F(b, p+1+c)-F(e[k], p+2)
            values[('Y5-to-C',), i, j] = q(e[4], total)-F(c, s+sum(e[:4])+1)
            values[('Y5-to-B',), i, j] = q(e[4], total)-F(b, s+sum(e[:4])+1)
            for k in range(4):
                for v, member in (('B', b), ('C', c)):
                    values[('Y-to-old', k, v), i, j] = q(e[k], total)-F(member, s+sum(e[:k])+5-k)
            pref = s+sum(e[:3])
            npay, ntax = true_pair_payoffs(pref, e[3], e[4])
            for f in pair:
                if f[0] == 'old-pair-to-Y':
                    l, m = f[1:]
                    four = (opay, otax, F(e[l]+e[m], p+1), F(e[l]*e[m], (p+1)*(p+2)))
                else:
                    v = b if f[1] == 'B' else c
                    w = b if f[2] == 'B' else c
                    four = (npay, ntax, F(v+w, pref+1), F(v*w, (pref+1)*(pref+2)))
                pieces[f, i, j] = four
                values[f, i, j] = four[0]+four[1]-four[2]+four[3]
    assert len(values) == 38*36 and len(pieces) == 18*36
    averaged, wallets = {}, {}
    for f in one+pair:
        for rel in ('same', 'off'):
            indices = [(i, j) for i in range(6) for j in range(6) if (i == j) == (rel == 'same')]
            assert len(indices) == (6 if rel == 'same' else 30)
            averaged[f+(rel,)] = sum((values[f, i, j] for i, j in indices), F(0))/len(indices)
            if f in pair:
                wallets[f+(rel,)] = tuple(sum((pieces[f, i, j][k] for i, j in indices), F(0))/len(indices)
                                          for k in range(4))
    # Every row has exactly one mean source-payoff and one mean source-tax.
    for prefix in ('old-pair-to-Y', 'new-pair-to-old'):
        source_parts = {four[:2] for name, four in wallets.items() if name[0] == prefix}
        assert len(source_parts) == 1
    return averaged, wallets, values


def root_literals(atom, table):
    a = tuple(int(c) for c in atom['actual'])
    roots = [(w >> 2, bits(v, 5)) for w, v in zip(atom['old_words'], atom['new_words'])]
    d = sum(t for t, e in roots)
    out = defaultdict(F)
    root = F(0)
    for j, (t, e) in enumerate(roots):
        total = t+sum(e)
        root += q(t, total)/6
        out['gamma',] += (-2*q(sum(e), total)+table[t, atom['new_words'][j], d-t])/6
        for k in range(5):
            own = q(e[k], total)
            den = t+sum(e[:k])+5-k
            out['price', k] += F(e[k], 6*(sum(a[:5])+1))
            out['capacity', k] += F(e[k], 6)
            for i in range(6):
                out['floor-actual', k, i] += (F(a[i], den)-own)/6
            out['floor-other-opt', k] += (F(d-t, den)-5*own)/6
            out['floor-root', k] += (F(t, den)-own)/6
            for l in range(5):
                if l != k:
                    out['floor-own-tail', k, l] += (F(e[l], den)-own)/6
                for i, (s, donor) in enumerate(roots):
                    if i != j:
                        out['cross-floor', k, l] += (F(donor[l], den)-own)/6
            for i in range(5):
                out['actual-floor', i, k] += F(e[k], 6*(sum(a[:i])+6-i))
        pref = t+sum(e[:3])
        rpay, tax = true_pair_payoffs(pref, e[3], e[4])
        apref = sum(a[:4])
        own = (t,)+e
        for x in range(6):
            for y in range(x, 6):
                out['actual-pair', x, y] += (F(own[x]+own[y], apref+1)
                    -F(own[x]*own[y], (apref+1)*(apref+2)))/6
                for i, (s, donor) in enumerate(roots):
                    if i != j:
                        v = (s,)+donor
                        out['cross-pair', x, y] += (-rpay-tax+F(v[x]+v[y], pref+1)
                            -F(v[x]*v[y], (pref+1)*(pref+2)))/30
    assert len(out) == 163
    return root, dict(out)


def pair_identity_check():
    checked = 0
    for p in range(5):
        for b, c, x, y, r in product((0, 1), repeat=5):
            def U(v, w):
                return F(v, p+1+w)
            gden = (p+1)*(p+2)
            lhs = U(b, c)+U(c, b)+F(b, gden)-F(x+y, p+1)+F(x*y, gden)
            rhs = (U(b, c)-U(x, r))+(U(r, x)-U(y, x))+(U(c, b)-U(r, b))+F(b*(1-r), gden)
            assert lhs == rhs and F(b*(1-r), gden) >= 0
            checked += 1
    assert checked == 160
    return checked


def permutation_counts_check():
    """Every named query obtains the full same/off orbit with fixed weights."""
    assert len(PERMS) == 720
    for i in range(6):
        for j in range(6):
            counts = Counter((p[i], p[j]) for p in PERMS)
            target = {(a, b): (120 if i == j else 24)
                      for a in range(6) for b in range(6) if (a == b) == (i == j)}
            assert dict(counts) == target
    return 36*720


def main():
    started = time.monotonic()
    point = BASE/'union_augmented_lp/augmented_lp_exact.json'
    inputs_path, cert_path = HERE/'inputs_exact.json', HERE/'joint_completion_exact.json'
    inp, cert = json.loads(inputs_path.read_text()), json.loads(cert_path.read_text())
    assert sha(point) == inp['point_sha256'] == cert['point_sha256'] == PIN
    assert cert['input_snapshot_sha256'] == sha(inputs_path)
    for s in inp['sources']:
        assert sha(BASE/s['path']) == s['sha256']
    raw = json.loads(point.read_text())
    main_audit = json.loads((BASE/'main_19662_audit.json').read_text())
    assert raw['verified_rows'] == main_audit['rows'] == 19662
    assert len(raw['columns']) == main_audit['columns'] == 15593
    assert raw['W'] == main_audit['W'] and raw['O'] == main_audit['O'] == '1'
    hist = {i: {'original_column_index': i, **v} for i, v in enumerate(raw['columns']) if v['kind'] == 'hist'}
    assert len(hist) == 16 and list(hist.values()) == inp['original_hist_records']
    cap = next(F(v['weight']) for v in raw['columns'] if v['kind'] == 'K')
    pay = [sum((F(h['weight'])*q(int(h['actual_bits'][i]), sum(map(int, h['actual_bits'])))
                for h in hist.values()), F(0)) for i in range(6)]
    assert cap == F(inp['K']) and pay == list(map(F, inp['u']))
    assert sum(pay) == F(inp['W']) == F(raw['W'])
    contexts = defaultdict(F)
    for h in hist.values():
        contexts[h['actual_bits'], h['d']] += F(h['weight'])
    assert {k: v for k, v in contexts.items() if v} == {(r['actual'], r['d']): F(r['mass']) for r in inp['actual_margins']}
    table = {}
    for t in (0, 1):
        for row in json.loads((BASE/f'background_five_bridge/fixed53_b{t}_profit.json').read_text())['min_by_actual_and_d']:
            table[t, int(row['actual'], 2), row['d']] = F(row['min_rho'])
    assert len(table) == 384
    assert table == {(r['t'], r['word'], r['comparison_count']): F(r['value']) for r in inp['remainder_table']}
    candidates = inp['candidate_root_states']
    seed_original = json.loads((BASE/'cross_root_pricing/joint_completion_exact.json').read_text())['support']
    assert candidates == [{k: s[k] for k in ('actual', 'd', 'one_word', 'zero_words')} for s in seed_original]
    assert all('mass' not in r for r in candidates)
    # Rebuild the complete finite incidence set without relying on the constructor.
    expected = set()
    for hi, h in hist.items():
        if F(h['weight']) == 0:
            continue
        old = sorted([w for w, n in enumerate(h['hist']) for _ in range(n)], key=lambda w: (-int(w >= 4), w))
        assert sum(w >> 2 for w in old) == h['d'] == 1
        for ri, r in enumerate(candidates):
            if (r['actual'], r['d']) == (h['actual_bits'], h['d']):
                for tail in set(permutations(r['zero_words'])):
                    expected.add((hi, ri, tuple(sorted(zip(old, (r['one_word'],)+tail)))))
    columns = json.loads((HERE/'seed_columns.json').read_text())['columns']
    actual = {(c['hist'], c['seed_root_state'], tuple(sorted(zip(c['old_words'], c['new_words'])))) for c in columns}
    assert expected == actual and len(columns) == len(actual) == 32
    coefficient_path = HERE/'candidate_coefficients_exact.json'
    assert cert['coefficient_table_sha256'] == sha(coefficient_path)
    coefficient_input = json.loads(coefficient_path.read_text())
    assert coefficient_input['point_sha256'] == PIN
    row_order = [tuple(n) for n in coefficient_input['row_order']]
    assert len(row_order) == len(set(row_order)) == 240
    precomputed = {}
    all_wallets = {}
    literal_count = 0
    for j, column in enumerate(columns):
        stored = coefficient_input['columns'][j]
        assert column == {k: v for k, v in stored.items() if k != 'costs'}
        root, costs = root_literals(column, table)
        interface, wallet, literal = interface_literals(column)
        merged = {**costs, **{n: -v for n, v in interface.items()}, ('root-source',): root}
        assert set(merged) == set(row_order)
        assert [str(merged[n]) for n in row_order] == stored['costs']
        precomputed[j], all_wallets[j] = merged, wallet
        literal_count += len(literal)
    assert literal_count == 32*38*36
    identity_count = pair_identity_check()
    permutation_count = permutation_counts_check()
    old_margin, root_margin = defaultdict(F), defaultdict(F)
    old_law, root_law = defaultdict(F), defaultdict(F)
    cost_total = defaultdict(F)
    wallet_total = defaultdict(lambda: [F(0)]*4)
    denominator = 1
    for atom in cert['atoms']:
        mass = F(atom['mass'])
        assert mass > 0
        col = columns[atom['column']]
        assert col == {k: atom[k] for k in col}
        hi, ri = atom['hist'], atom['seed_root_state']
        h, r = hist[hi], candidates[ri]
        old, new = atom['old_words'], atom['new_words']
        assert atom['actual'] == h['actual_bits'] == r['actual']
        assert len(old) == len(new) == 6 and all(0 <= w < 8 for w in old) and all(0 <= w < 32 for w in new)
        assert [old.count(w) for w in range(8)] == h['hist']
        assert 4 <= old[0] < 8 and all(w < 4 for w in old[1:])
        assert sum(w >> 2 for w in old) == h['d'] == r['d'] == 1
        assert new[0] == r['one_word'] and sorted(new[1:]) == r['zero_words']
        old_margin[hi] += mass
        root_margin[ri] += mass
        for p in PERMS:
            old_law[hi, tuple(old[k] for k in p)] += mass/720
            root_law[ri, tuple(32*(old[k] >> 2)+new[k] for k in p)] += mass/720
        for name, value in precomputed[atom['column']].items():
            cost_total[name] += mass*value
        for name, four in all_wallets[atom['column']].items():
            wallet_total[name] = [x+mass*y for x, y in zip(wallet_total[name], four)]
        denominator = lcm(denominator, (mass/720).denominator)
    assert len(cert['atoms']) == cert['positive_atoms'] == 17
    assert sum(old_margin.values()) == F(cert['total_mass']) == 1
    assert denominator == int(cert['unit_customer_scale'])
    assert all((F(a['mass'])*denominator/720).denominator == 1 for a in cert['atoms'])
    old_law_count, own_count, root_law_count = 0, 0, 0
    own_report = []
    for hi, h in hist.items():
        mass = F(h['weight'])
        assert old_margin[hi] == mass
        words = set(permutations(w for w, n in enumerate(h['hist']) for _ in range(n)))
        for word in words:
            assert old_law[hi, word] == mass/len(words)
        old_law_count += len(words)
        for i in range(6):
            for w in range(8):
                own = sum((old_law[hi, v] for v in words if v[i] == w), F(0))
                assert own == mass*h['hist'][w]/6
                own_report.append({'hist': hi, 'index': i, 'old_word': w, 'mass': str(own)})
                own_count += 1
    saved_root_margins = {r['root_state']: F(r['mass']) for r in cert['new_root_state_margins']}
    for ri, r in enumerate(candidates):
        assert root_margin[ri] == saved_root_margins[ri]
        words = set(permutations((32+r['one_word'], *r['zero_words'])))
        for word in words:
            assert root_law[ri, word] == root_margin[ri]/len(words)
        root_law_count += len(words)
    true_actual_pair = sum((F(h['weight'])*sum(true_pair_payoffs(sum(map(int, h['actual_bits'][:4])),
                           int(h['actual_bits'][4]), int(h['actual_bits'][5]))) for h in hist.values()), F(0))
    assert true_actual_pair == pay[4]+pay[5]+sum((F(h['weight'])*F(int(h['actual_bits'][4]),
            (sum(map(int, h['actual_bits'][:4]))+1)*(sum(map(int, h['actual_bits'][:4]))+2)) for h in hist.values()), F(0))
    saved = {tuple(r['row']): r for r in cert['budget_slacks']}
    assert len(saved) == len(cert['budget_slacks']) == len(cost_total) == 240
    assert set(saved) == set(cost_total)
    audit_budgets = []
    for name, cost in cost_total.items():
        typ = name[0]
        if typ == 'gamma':
            budget = -F(226487, 10**21)*cap-F(5, 6)
        elif typ == 'price':
            budget = pay[5]
        elif typ == 'capacity':
            budget = cap
        elif typ == 'actual-floor':
            budget = pay[name[1]]
        elif typ == 'actual-pair':
            budget = true_actual_pair
        elif typ == 'root-source':
            budget = pay[0]
        else:
            budget = F(0)
        slack = budget-cost
        assert slack >= 0
        assert (budget, cost, slack) == tuple(F(saved[name][k]) for k in ('budget', 'cost', 'slack'))
        audit_budgets.append({'row': list(name), 'budget': str(budget), 'cost': str(cost), 'slack': str(slack)})
    assert cert['root_source_coefficient'] == 1
    rootgap = pay[0]-cost_total['root-source',]
    assert rootgap == F(cert['root_gap']) > 0
    assert cost_total['root-source',] == F(cert['root_cost']) and pay[0] == F(cert['root_budget'])
    previous = json.loads((HERE/'completion_203_exact.json').read_text())
    assert cert['unchanged_atoms_from_203_sha256'] == sha(HERE/'completion_203_exact.json')
    assert cert['atoms'] == previous['atoms'] and previous['nonroot_budgets'] == 203
    assert previous['point_sha256'] == PIN and previous['root_gap'] == cert['root_gap']
    assert len(previous['budget_slacks']) == 204
    for row in previous['budget_slacks']:
        assert row == saved[tuple(row['row'])]
    one, pair = families()
    labelled = []
    for f in one+pair:
        for i in range(6):
            for j in range(6):
                name = f+('same' if i == j else 'off',)
                value = -cost_total[name]
                assert value >= 0
                labelled.append({'family': list(f), 'old_index': i, 'root_index': j, 'slack': str(value)})
    pair_report, pair_slacks = [], []
    for name, (reward, tax, query, overlap) in wallet_total.items():
        slack = reward+tax-query+overlap
        assert slack == -cost_total[name] > 0
        pair_slacks.append(slack)
        pair_report.append({'row': list(name), 'source_payoff': str(reward), 'source_tax': str(tax),
                            'query_f_sum': str(query), 'query_overlap_g': str(overlap), 'slack': str(slack)})
    assert len(pair_report) == 36 and min(pair_slacks) == F(cert['new_pair_row_minimum'])
    for prefix in ('old-pair-to-Y', 'new-pair-to-old'):
        assert len({(r['source_payoff'], r['source_tax']) for r in pair_report if r['row'][0] == prefix}) == 1
    grouped = defaultdict(list)
    for row in audit_budgets:
        grouped[row['row'][0]].append(F(row['slack']))
    report = {
        'status': 'INDEPENDENT STANDARD-LIBRARY 239-BUDGET COMMON COMPLETION AUDIT PASSED',
        'scope': 'Exactly the declared 239 nonroot budgets and one root-source budget; no SPE or R/Z full-own claim.',
        'actual_argv': [sys.executable, *sys.argv], 'point_sha256': PIN,
        'certificate_sha256': sha(cert_path), 'verifier_sha256': sha(__file__),
        'input_snapshot_sha256': sha(inputs_path), 'coefficient_table_sha256': sha(coefficient_path),
        'original_hist_records': len(hist), 'positive_hist_records': sum(F(h['weight']) > 0 for h in hist.values()),
        'old_hist_margin_checks': len(hist), 'full_old_labelled_vector_margins': old_law_count,
        'own_eight_state_margins': own_count, 'full_new_root_labelled_vector_margins': root_law_count,
        'candidate_root_states': len(candidates), 'positive_root_states': sum(v > 0 for v in root_margin.values()),
        'complete_seed_incidence_columns': len(columns), 'positive_joint_atoms': len(cert['atoms']),
        'synchronous_permutations_per_atom': len(PERMS), 'unmerged_customer_type_records': len(PERMS)*len(cert['atoms']),
        'background_remainder_entries': len(table), 'candidate_literal_coefficient_checks': len(columns)*len(row_order),
        'canonical_named_interface_evaluations': literal_count,
        'synchronous_index_frequency_checks': permutation_count, 'strong_pair_identity_checks': identity_count,
        'root_original_budget_rows': 163, 'single_interface_orbit_rows': 40, 'pair_interface_orbit_rows': 36,
        'nonroot_budget_rows': 239, 'root_source_budget_rows': 1,
        'named_interface_queries': len(labelled), 'new_named_pair_queries': 18*36,
        'named_interface_queries_strict': sum(F(r['slack']) > 0 for r in labelled),
        'named_interface_queries_zero': sum(F(r['slack']) == 0 for r in labelled),
        'new_pair_rows_strict': len(pair_slacks), 'new_pair_minimum': str(min(pair_slacks)),
        'new_pair_minimum_float': float(min(pair_slacks)), 'root_cost': str(cost_total['root-source',]),
        'root_gap': str(rootgap), 'root_gap_float': float(rootgap), 'unit_customer_scale': str(denominator),
        'budget_summary': [{'family': k, 'rows': len(v), 'minimum': str(min(v)), 'minimum_float': float(min(v)),
                            'zero_rows': sum(s == 0 for s in v)} for k, v in grouped.items()],
        'all_budget_values': audit_budgets, 'new_pair_wallets': pair_report,
        'named_interface_values': labelled, 'full_own_eight_state_values': own_report,
        'elapsed_seconds': time.monotonic()-started,
    }
    (HERE/'independent_audit.json').write_text(json.dumps(report, indent=2)+'\n')
    omitted = {'all_budget_values', 'new_pair_wallets', 'named_interface_values', 'full_own_eight_state_values'}
    print(json.dumps({k: v for k, v in report.items() if k not in omitted}, indent=2))


if __name__ == '__main__':
    main()
