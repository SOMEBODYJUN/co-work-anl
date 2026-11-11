"""Independent standard-library audit of all 203 shared nonroot budgets.

No sibling module, optimizer, row generator or third-party package is imported.
All 720 labelled B/C-to-root-tail and reverse queries are evaluated under all
720 simultaneous permutations of every atom, using integer denominator counts.
Whole six-index old and new labelled marginal laws are checked, as well as all
16 hist masses and the full eight-state (t,b,c) marginal of each named index.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import permutations
from math import lcm
from pathlib import Path
import hashlib
import json
import sys
import time

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
PIN = 'd70c26065d42fd73dedc94183e4533dd6f8608d5841f7a6018ff180dc77e2f9f'
PERMS = tuple(permutations(range(6)))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def q(n, d):
    return F(n, d) if n else F(0)


def bits(word, width):
    return tuple(int(c) for c in format(word, '0'+str(width)+'b'))


def families():
    return ([('C-to-Y', k) for k in range(5)]
            + [('B-to-Y', k) for k in range(5)]
            + [('Y-to-old', k, v) for k in range(4) for v in ('B', 'C')]
            + [('Y5-to-C',), ('Y5-to-B',)])


def literal_coefficients(atom):
    """Return every indexed coefficient and both complete labelled margins."""
    old = [bits(w, 3) for w in atom['old_words']]
    new = [bits(w, 5) for w in atom['new_words']]
    p = sum(int(c) for c in atom['actual'][:3])
    counts = [[0]*7 for _ in range(720)]
    old_law, root_law = Counter(), Counter()
    for perm in PERMS:
        ow = [old[r] for r in perm]
        nw = [new[r] for r in perm]
        old_law[tuple(atom['old_words'][r] for r in perm)] += 1
        root_law[tuple((old[r][0]<<5)+atom['new_words'][r] for r in perm)] += 1
        for i, (t, b, c) in enumerate(ow):
            cd = p+t+b+1
            bd = p+t+b+c
            bsafe = p+t+2
            for j, e in enumerate(nw):
                s = ow[j][0]
                den = s+sum(e)
                ij = 6*i+j
                for k in range(5):
                    counts[36*k+ij][cd] += c-e[k]
                    if b:
                        counts[36*(5+k)+ij][bd] += b
                    counts[36*(5+k)+ij][bsafe] -= e[k]
                for k in range(4):
                    safety = s+sum(e[:k])+5-k
                    bline = counts[36*(10+2*k)+ij]
                    cline = counts[36*(11+2*k)+ij]
                    if e[k]:
                        bline[den] += 1
                        cline[den] += 1
                    bline[safety] -= b
                    cline[safety] -= c
                lastden = s+sum(e[:4])+1
                if e[4]:
                    counts[36*18+ij][den] += 1
                    counts[36*19+ij][den] += 1
                counts[36*18+ij][lastden] -= c
                counts[36*19+ij][lastden] -= b
    assert len(PERMS) == 720 and sum(old_law.values()) == sum(root_law.values()) == 720
    assert all(row[0] == 0 for row in counts)
    values = [sum((F(row[d], 720*d) for d in range(1, 7)), F(0)) for row in counts]
    # Uniform simultaneous permutations must reproduce same/off rows for each
    # literal pair. There are no independent old/new permutations here.
    for f in range(20):
        for i in range(6):
            for j in range(6):
                representative = 0 if i == j else 1
                assert values[36*f+6*i+j] == values[36*f+representative]
    return values, old_law, root_law


def root_costs(atom, remainder):
    """Literal six-root sums and all 30 ordered different-root pairs."""
    a = tuple(int(c) for c in atom['actual'])
    roots = [(w//4, bits(e, 5)) for w, e in zip(atom['old_words'], atom['new_words'])]
    d = sum(t for t, e in roots)
    costs = defaultdict(F)
    root = F(0)
    for j, (t, e) in enumerate(roots):
        total = t+sum(e)
        root += q(t, total)/6
        costs['gamma',] += (-2*q(sum(e), total)+remainder[t, atom['new_words'][j], d-t])/6
        for k in range(5):
            own = q(e[k], total)
            safe = t+sum(e[:k])+5-k
            costs['price', k] += F(e[k], 6*(sum(a[:5])+1))
            costs['capacity', k] += F(e[k], 6)
            for i in range(6):
                costs['floor-actual', k, i] += (F(a[i], safe)-own)/6
            costs['floor-other-opt', k] += (F(d-t, safe)-5*own)/6
            costs['floor-root', k] += (F(t, safe)-own)/6
            for l in range(5):
                if l != k:
                    costs['floor-own-tail', k, l] += (F(e[l], safe)-own)/6
                for i, (s, donor) in enumerate(roots):
                    if i != j:
                        costs['cross-floor', k, l] += (F(donor[l], safe)-own)/6
            for i in range(5):
                costs['actual-floor', i, k] += F(e[k], 6*(sum(a[:i])+6-i))
        pref = t+sum(e[:3])
        ownpair = q(e[3]+e[4], total)+F(e[3], (pref+1)*(pref+2))
        apref = sum(a[:4])
        roles = (t,)+e
        for x in range(6):
            for y in range(x, 6):
                costs['actual-pair', x, y] += (F(roles[x]+roles[y], apref+1)
                     - F(roles[x]*roles[y], (apref+1)*(apref+2)))/6
                for i, (s, donor) in enumerate(roots):
                    if i != j:
                        v = (s,)+donor
                        costs['cross-pair', x, y] += (-ownpair+F(v[x]+v[y], pref+1)
                             -F(v[x]*v[y], (pref+1)*(pref+2)))/30
    assert len(costs) == 163
    return root, dict(costs)


def main():
    started = time.monotonic()
    certpath = HERE/'joint_completion_exact.json'
    inputpath = HERE/'inputs_exact.json'
    cert = json.loads(certpath.read_text())
    inputs = json.loads(inputpath.read_text())
    rawpath = BASE/'peer_augmented_lp/augmented_lp_exact.json'
    assert cert['point_sha256'] == inputs['point_sha256'] == sha(rawpath) == PIN
    assert cert['input_snapshot_sha256'] == sha(inputpath)
    for source in inputs['sources']:
        assert sha(BASE/source['path']) == source['sha256']
    previous = json.loads((BASE/'root_old_tail_joint/joint_completion_exact.json').read_text())
    assert cert['previous_certificate_sha256'] == sha(BASE/'root_old_tail_joint/joint_completion_exact.json')
    assert cert['atoms'] == previous['atoms']
    raw = json.loads(rawpath.read_text())
    hist = {i: {'original_column_index': i, **r} for i, r in enumerate(raw['columns']) if r['kind'] == 'hist'}
    frozen = inputs['projection_inputs']
    assert list(hist.values()) == frozen['original_hist_records'] and len(hist) == 16
    for source in frozen['sources']:
        assert sha(BASE/source['path']) == source['sha256']
    table = {}
    for t in (0, 1):
        source = BASE/f'background_five_bridge/fixed53_b{t}_profit.json'
        for r in json.loads(source.read_text())['min_by_actual_and_d']:
            table[t, int(r['actual'], 2), r['d']] = F(r['min_rho'])
    assert len(table) == 384
    assert table == {(r['t'], r['word'], r['comparison_count']): F(r['value']) for r in frozen['remainder_table']}
    cap = next(F(c['weight']) for c in raw['columns'] if c['kind'] == 'K')
    pay = [sum((F(h['weight'])*q(int(h['actual_bits'][i]), sum(map(int, h['actual_bits'])))
                for h in hist.values()), F(0)) for i in range(6)]
    assert cap == F(frozen['K']) and pay == list(map(F, frozen['u']))
    assert sum(pay) == F(raw['W']) == F(frozen['W'])
    pair_budget = pay[4]+pay[5]+sum((F(h['weight'])*F(int(h['actual_bits'][4]),
                       (sum(map(int, h['actual_bits'][:4]))+1)*(sum(map(int, h['actual_bits'][:4]))+2))
                       for h in hist.values()), F(0))
    totals = [F(0)]*720
    budgetcost = defaultdict(F)
    oldmargin, rootmargin = defaultdict(F), defaultdict(F)
    fullold, fullroot = defaultdict(F), defaultdict(F)
    rootcost = F(0)
    denominator = 1
    candidates = inputs['candidate_root_states']
    for atom in cert['atoms']:
        mass = F(atom['mass'])
        assert mass > 0
        hindex, rindex = atom['original_column_index'], atom['joint_atom_index']
        h, r = hist[hindex], candidates[rindex]
        old, new = atom['old_words'], atom['new_words']
        assert len(old) == len(new) == 6 and all(0 <= w < 8 for w in old) and all(0 <= w < 32 for w in new)
        assert atom['actual'] == h['actual_bits'] == r['actual']
        assert [old.count(w) for w in range(8)] == h['hist']
        assert old[0] >= 4 and all(w < 4 for w in old[1:])
        assert sum(w//4 for w in old) == h['d'] == r['d'] == 1
        assert new[0] == r['one_word'] and sorted(new[1:]) == r['zero_words']
        oldmargin[hindex] += mass
        rootmargin[rindex] += mass
        vals, olaw, rlaw = literal_coefficients(atom)
        totals = [a+mass*b for a, b in zip(totals, vals)]
        for word, count in olaw.items():
            fullold[hindex, word] += mass*count/720
        for word, count in rlaw.items():
            fullroot[rindex, word] += mass*count/720
        rc, bc = root_costs(atom, table)
        rootcost += mass*rc
        for name, val in bc.items():
            budgetcost[name] += mass*val
        denominator = lcm(denominator, (mass/720).denominator)
    assert len(cert['atoms']) == cert['support_atoms'] == 17
    assert sum(oldmargin.values()) == F(cert['total_mass']) == 1
    assert denominator == int(cert['unit_customer_scale'])
    assert all((F(a['mass'])*denominator/720).denominator == 1 for a in cert['atoms'])
    # Whole old labelled-vector marginal: stronger than separate hist or bit
    # counts, and keeps every old B/C own state in the same common measure.
    own_report, oldlaw_report = [], []
    old_law_entries = 0
    for hi, h in hist.items():
        mass = F(h['weight'])
        assert oldmargin[hi] == mass
        multiset = tuple(w for w, n in enumerate(h['hist']) for _ in range(n))
        words = set(permutations(multiset))
        for word in words:
            assert fullold[hi, word] == mass/len(words)
        old_law_entries += len(words)
        oldlaw_report.append({'hist': hi, 'labelled_vectors': len(words),
                              'mass_each': str(mass/len(words))})
        for i in range(6):
            for w in range(8):
                value = sum((fullold[hi, v] for v in words if v[i] == w), F(0))
                expected = mass*h['hist'][w]/6
                assert value == expected
                own_report.append({'hist': hi, 'index': i, 'old_word': w, 'mass': str(value)})
    expected_root = {r['original_root_state']: F(r['mass']) for r in inputs['previous_root_state_margins']}
    assert cert['new_root_state_margins'] == inputs['previous_root_state_margins']
    root_law_entries = 0
    rootlaw_report = []
    for ri, r in enumerate(candidates):
        assert rootmargin[ri] == expected_root[ri]
        values = (32+r['one_word'], *r['zero_words'])
        words = set(permutations(values))
        for word in words:
            assert fullroot[ri, word] == expected_root[ri]/len(words)
        root_law_entries += len(words)
        rootlaw_report.append({'root_state': ri, 'labelled_vectors': len(words),
                               'mass_each': str(expected_root[ri]/len(words))})
    saved = {tuple(v['row']): v for v in cert['budget_slacks']}
    assert len(saved) == len(cert['budget_slacks']) == 204
    budget_report = []
    for name, cost in budgetcost.items():
        if name[0] == 'gamma':
            budget = -F(226487, 10**21)*cap-F(5, 6)*F(raw['O'])
        elif name[0] == 'price':
            budget = pay[5]
        elif name[0] == 'capacity':
            budget = cap
        elif name[0] == 'actual-floor':
            budget = pay[name[1]]
        elif name[0] == 'actual-pair':
            budget = pair_budget
        else:
            budget = F(0)
        slack = budget-cost
        assert slack >= 0 and slack == F(saved[name]['slack']) and budget == F(saved[name]['budget'])
        budget_report.append({'row': list(name), 'budget': str(budget), 'cost': str(cost), 'slack': str(slack)})
    assert len(budgetcost) == 163
    gap = pay[0]-rootcost
    assert gap > 0 and gap == F(cert['root_slack']) == F(previous['root_slack'])
    assert rootcost == F(cert['root_cost']) == F(previous['root_cost'])
    assert pay[0] == F(cert['root_budget']) == F(saved['root-source',]['budget'])
    assert gap == F(saved['root-source',]['slack'])
    literal_report, orbit_report = [], []
    new_values = []
    for f, family in enumerate(families()):
        for i in range(6):
            for j in range(6):
                relation = 'same' if i == j else 'off'
                key = family+(relation,)
                val = totals[36*f+6*i+j]
                assert val >= 0 and val == F(saved[key]['slack']) and F(saved[key]['budget']) == 0
                literal_report.append({'family': list(family), 'old_index': i, 'root_index': j,
                                       'value': str(val)})
                if family[0] not in ('C-to-Y', 'Y5-to-C'):
                    assert val > 0
                    new_values.append(val)
        for rel, k in [('same', 0), ('off', 1)]:
            orbit_report.append({'row': list(family+(rel,)), 'slack': str(totals[36*f+k])})
    assert len(orbit_report) == 40 and len(new_values) == 504
    assert min(new_values) == F(cert['new_row_minimum'])
    assert set(saved) == set(budgetcost) | {('root-source',)} | {tuple(v['row']) for v in orbit_report}
    report = {
        'status': 'INDEPENDENT STANDARD-LIBRARY 203-BUDGET COMMON COMPLETION AUDIT PASSED',
        'scope': 'Declared membership projection only; no full-history strategy or SPE certification.',
        'actual_argv': [sys.executable, *sys.argv],
        'point_sha256': PIN,
        'certificate_sha256': sha(certpath),
        'input_snapshot_sha256': sha(inputpath),
        'verifier_sha256': sha(__file__),
        'positive_atoms': 17, 'simultaneous_permutations_each': 720,
        'literal_atoms_before_duplicate_merging': 17*720,
        'literal_queries_checked': 720,
        'new_literal_queries_checked': 504,
        'coefficient_checks': 17*720,
        'raw_permuted_query_evaluations': 17*720*720,
        'old_hist_margins': 16, 'full_old_labelled_marginal_entries': old_law_entries,
        'own_eight_state_marginal_entries': len(own_report),
        'full_root_labelled_marginal_entries': root_law_entries,
        'root_states_checked': len(candidates),
        'root_budget_rows_checked': len(budgetcost), 'interface_orbit_rows_checked': 40,
        'nonroot_budget_rows_checked': 203,
        'literal_queries_strict': sum(v > 0 for v in totals),
        'literal_queries_zero': sum(v == 0 for v in totals),
        'literal_queries_negative': sum(v < 0 for v in totals),
        'new_literal_queries_strict': len(new_values),
        'new_minimum': str(min(new_values)), 'new_minimum_float': float(min(new_values)),
        'root_cost': str(rootcost), 'root_gap': str(gap), 'root_gap_float': float(gap),
        'unit_customer_scale': str(denominator),
        'elapsed_seconds': time.monotonic()-started,
        'root_budget_values': budget_report,
        'interface_orbit_values': orbit_report,
        'literal_query_values': literal_report,
        'full_old_labelled_marginal_checks': oldlaw_report,
        'full_root_labelled_marginal_checks': rootlaw_report,
        'full_own_marginals': own_report,
    }
    (HERE/'independent_audit.json').write_text(json.dumps(report, indent=2)+'\n')
    omitted = {'root_budget_values', 'interface_orbit_values', 'literal_query_values',
               'full_old_labelled_marginal_checks', 'full_root_labelled_marginal_checks', 'full_own_marginals'}
    print(json.dumps({k: v for k, v in report.items() if k not in omitted}, indent=2))


if __name__ == '__main__':
    main()
