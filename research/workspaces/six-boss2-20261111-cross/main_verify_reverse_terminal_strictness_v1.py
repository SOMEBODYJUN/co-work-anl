"""Main independent audit: 624 full rows and an actual-linked 616 lift.

No discovery/recovery code is imported. All 616 inequalities, both new/old
separator vectors, and the deterministic padding construction are rationally
verified from the actual columns and explicit ordered-history formulas.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from collections import defaultdict
import hashlib, json, time
from main_cross_query_features_v1 import query_samples, literal_product, pay
from main_reverse_terminal_features_v1 import all_616, projection_624, reverse_value, moment_product

B = Path(__file__).resolve().parent
pp = B / 'master_cuts/dynamic_5799_exact.json'
cp = B / 'joint_requery/reverse_terminal_5799_one_v1.json'
lp = B / 'joint_requery/actual_padding_616_vs_624_strictness_5799_v1.json'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
point, pack, lift = (json.loads(p.read_text()) for p in (pp, cp, lp))
assert sha(cp) == '3b39262c153be351853f2625809da5679e634648d895c233b554868f1bd0077c'
assert sha(lp) == 'a06786cd8a5176754544d614034eeec78efc6a733f8ad0552f5ce760b48a14ce'
assert pack['source_sha256'] == lift['base_source_sha256'] == sha(pp)
assert lift['separator_package_sha256'] == sha(cp)
assert (pack['i'], pack['k'], pack['member'], pack['orb']) == (3, 3, 0, [0, 0])
started = time.time()
cols = point['columns']
blocks = []
for j, c in enumerate(cols):
    if c['kind'] == 'hist':
        blocks.append((j, c, []))
    elif c['kind'] == 'joint-reply':
        blocks[-1][2].append((j, c))

actual = [F(0)] * 6
for j, h, joint in blocks:
    a = tuple(map(int, h['actual_bits']))
    for i in range(6):
        actual[i] += F(h['weight']) * pay(a[i], sum(a))
K = F(cols[0]['weight'])
assert actual == list(map(F, pack['actual_utilities'])) == list(map(F, lift['original_actual_utilities']))
assert K == F(pack['K']) == F(lift['original_K'])

def visible_key(v):
    p, ell, t, qs, moments = v['state']
    return (p, ell, t, tuple(map(F, qs)), tuple(map(F, moments)))

rows_checked = []
original_visible = None
new_phi = None
for rec in (pack['old616_cut'], pack['cuts'][0]):
    assert (rec['i'], rec['k'], rec['member'], rec['orb']) == (3, 3, 0, [0, 0])
    weights = {n: F(w) for n, w in rec['weights'].items()}
    assert min(weights.values()) >= 0
    assert weights['sourceT'] + weights['sourceC'] == 1
    price = sum((w for n, w in weights.items() if n.startswith('price:')), F(0))
    cap = sum((w for n, w in weights.items() if n.startswith('cap:')), F(0))
    assert F(rec['u6_coefficient']) == price and F(rec['K_coefficient']) == cap
    phi = projection_624(weights)
    row = [F(0)] * 4849
    row[0] = cap
    visible = defaultdict(F)
    for hi, h, joint in blocks:
        a = tuple(map(int, h['actual_bits']))
        words = tuple(w for w, n in zip(product((0, 1), repeat=3), h['hist']) for _ in range(n))
        hm = F(h['weight'])
        mass_at = {(tuple(c['group'][:2]), tuple(c['group'][2]), tuple(c['group'][3]), tuple(c['state'])): F(c['weight']) for _, c in joint}
        base, increments = F(0), defaultdict(F)
        for i in range(6):
            for j in range(6):
                if i == j:
                    continue
                masses = {st: mass_at.get(((0, 0), words[i], words[j], st), F(0)) for st in ((0, 1), (1, 0), (1, 1))}
                masses[0, 0] = hm - sum(masses.values(), F(0))
                assert min(masses.values()) >= 0
                values = {}
                for state in product((0, 1), repeat=2):
                    samples, qs, moments = query_samples(a, words, i, j, state)
                    for name in weights:
                        if name.startswith('oldpair'):
                            assert moment_product(name, qs, moments) == literal_product(samples, name)
                    key = (sum(a[:3]), sum(a[:5]), state[0], qs, moments)
                    values[state] = phi(*key)
                    visible[key] += masses[state] / 30
                base += values[0, 0] / 30
                for state in ((0, 1), (1, 0), (1, 1)):
                    increments[words[i], words[j], state] += (values[state] - values[0, 0]) / 30
        row[hi] = pay(a[3], sum(a)) + price * pay(a[5], sum(a)) - base
        for ci, c in joint:
            family, diag, wi, wj = c['group']
            if (family, diag) == (0, 0):
                row[ci] = -increments[tuple(wi), tuple(wj), tuple(c['state'])]
    saved = [F(0)] * 4849
    for j, value in rec['sparse_row']:
        assert saved[j] == 0
        saved[j] = F(value)
    assert row == saved
    digest = hashlib.sha256(json.dumps(list(map(str, row)), separators=(',', ':')).encode()).hexdigest()
    assert digest == rec['row_sha256']
    slack = sum(v * F(c['weight']) for v, c in zip(row, cols))
    assert slack == F(rec['exact_slack']) < 0
    visible = {v: m for v, m in visible.items() if m}
    supplied = {visible_key(v): F(v['mass']) for v in rec['visible']}
    assert len(supplied) == len(rec['visible']) == 56 and supplied == visible
    for v in rec['visible']:
        assert phi(*visible_key(v)) == F(v['minimum'])
    if original_visible is None:
        original_visible = visible
    else:
        assert original_visible == visible
        new_phi = phi
    rows_checked.append({'has_reverse_weight': any(n.startswith('prior') for n in weights),
                         'all_4849_coefficients_equal': True, 'row_sha256': digest, 'exact_slack': str(slack)})

padding = lift['padding']
assert padding['actual_bits'] == [0, 0, 0, 1, 0, 1]
assert padding['six_old_words'] == [[1, 1, 1]] * 6 and padding['R'] == padding['Z'] == 1
assert padding['macro_hidden'] == [1, 1, 1, 1, 0, 0]
delta, mass = F(lift['source_gap_delta']), F(padding['mass'])
assert delta > 0 and mass == 6 * delta
recovered = F(lift['recovered_old616_feasible_source'])
assert recovered == actual[3] + delta
_, pad_qs, pad_moments = query_samples(tuple(padding['actual_bits']), ((1, 1, 1),) * 6, 0, 1, (1, 1))
pad_key = (0, 1, 1, pad_qs, pad_moments)
assert pad_key not in original_visible
expected_visible = dict(original_visible)
expected_visible[pad_key] = mass
states = [visible_key(v) for v in lift['visible']]
assert len(states) == len(set(states)) == 57
assert dict(zip(states, (F(v['mass']) for v in lift['visible']))) == expected_visible
newactual = [sum(m * pay(qs[i], sum(qs[:6])) for (p, ell, t, qs, mom), m in expected_visible.items()) for i in range(6)]
assert newactual == list(map(F, lift['actual_utilities']))
assert newactual == [value + mass * F(padding['actual_bits'][i], 2) for i, value in enumerate(actual)]
newK = F(lift['K'])
assert newK == K + mass
observed = [F(0)] * len(states)
sums = defaultdict(F)
base_sums = defaultdict(F)
for atom in lift['hidden_lift']:
    vi, hidden, w = atom['visible'], tuple(atom['hidden']), F(atom['mass'])
    assert 0 <= vi < len(states) and w > 0
    assert len(hidden) == 6 and all(x in (0, 1) for x in hidden[:4]) and hidden[4:] == (0, 0)
    observed[vi] += w
    values, budgets = all_616(*states[vi], hidden)
    for name, val in values.items():
        sums[name] += w * val
        if states[vi] != pad_key:
            base_sums[name] += w * val
    if states[vi] == pad_key:
        assert hidden == tuple(padding['macro_hidden']) and w == mass
assert len(lift['hidden_lift']) == 77
assert observed == [expected_visible[state] for state in states]
assert set(sums) == set(lift['all616_slacks_at_actual'])
slacks = {}
for name, (sr, su, sk) in budgets.items():
    slack = sr * newactual[3] + su * newactual[5] + sk * newK - sums[name]
    assert slack == F(lift['all616_slacks_at_actual'][name]) >= 0
    assert sr * recovered + su * actual[5] + sk * K - base_sums[name] >= 0
    slacks[name] = slack
assert len(slacks) == 616 and min(slacks.values()) == 0

# The padding lemma is checked for each old feature, not merely the selected
# separating combination. Source credit is exactly 1/6 per unit.
pad_values, pad_budgets = all_616(*pad_key, tuple(padding['macro_hidden']))
for name, value in pad_values.items():
    sr, su, sk = pad_budgets[name]
    credit = F(sr) / 2 + F(su) / 2 + F(sk) - value
    assert credit >= 0
    if name.startswith('source'):
        assert credit == F(1, 6)
for node in ('priorR', 'priorZ'):
    for label in ('b', 'c', 'j', 'v'):
        assert reverse_value(node + ':' + label, pad_qs, tuple(padding['macro_hidden'])) == 0

assert lift['new624_weights'] == pack['cuts'][0]['weights']
theta = {n: F(w) for n, w in lift['new624_weights'].items()}
au = sum(w for n, w in theta.items() if n.startswith('price:'))
ak = sum(w for n, w in theta.items() if n.startswith('cap:'))
pad_min = new_phi(*pad_key)
assert pad_min == F(33575891, 60000000)
assert F(1, 2) + au / 2 + ak - pad_min == F(1, 6)
for state, value in zip(states, lift['new624_visible_minima']):
    assert new_phi(*state) == F(value)
new_slack = newactual[3] + au * newactual[5] + ak * newK - sum(m * new_phi(*state) for state, m in expected_visible.items())
assert new_slack == F(lift['new624_exact_slack']) < 0
assert new_slack == F(pack['cuts'][0]['exact_slack']) + delta
menu_caps = [newK - sum(m * qs[i] for (p, ell, t, qs, mom), m in expected_visible.items()) for i in range(17)]
menu_prices = [newactual[5] - sum(m * qs[i] / (ell + 1) for (p, ell, t, qs, mom), m in expected_visible.items()) for i in range(17)]
assert menu_caps == list(map(F, lift['all17_menu_caps'])) and min(menu_caps) >= 0
assert menu_prices == list(map(F, lift['all17_actual_terminal_prices'])) and min(menu_prices) >= 0

result = {'status': 'PASS', 'point_sha256': sha(pp), 'separator_sha256': sha(cp), 'lift_sha256': sha(lp),
          'full_rows_checked': rows_checked, 'original_visible_types': 56, 'padded_visible_types': 57,
          'hidden_atoms': 77, 'old_inequalities_checked': len(slacks), 'minimum_old_slack': str(min(slacks.values())),
          'actual_utilities_reconstructed': True, 'all_hidden_mass_equalities': True,
          'padding_delta': str(delta), 'padding_mass': str(mass), 'padding_source_credit': '1/6',
          'padding_cut_credit': '1/6', 'new624_negative_slack': str(new_slack),
          'all_17_visible_terminal_prices_and_caps': True,
          'scope': 'Strict P624 subset P616 on the general actual-linked actual4/R/orb00 domain with the same 17 old queries. One additional histogram is used; no fixed-16hist strictness, whole-master feasibility, or complete SPE is claimed.',
          'seconds': time.time() - started, 'verifier_sha256': sha(Path(__file__))}
Path(__file__).with_suffix('.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
