#!/usr/bin/env python3
"""Independent Fraction replay of the frozen root270 algebraic bridge.

Reads JSON and prose only.  Does not import or execute any builder, Main,
previous-audit program, optimizer, or numerical library.  Run check_exact.py
first: the root source theorem is audited there, while this file checks its
standard257 encoding, the true menu-size budget, and the complete bridge.
"""
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = WS.parents[2]
PINS = {
    'main_root270_global_bridge/manifest.json':
        'ffb88045d91522bb87fbadaedc9350ab688fd36b432b83b15f7a4bca72114b7f',
    'main_root270_global_bridge/proof.md':
        'c35bc63657a1ff0fe6c5525a38747bfa0c8b6fe130a6a468ca908b4796060c78',
    'main_root270_global_bridge/ROOT270_TRUE_BRANCH_P25.json':
        'd4ee988b28e897bcb836811c45e1c27a9728c64e352d2e30c79c93fded71a834',
    'main_root270_global_bridge/exact_certificate.json':
        '6bd8f1b47b89dd64f38dcd955273b60cbb7b29fc7c36d073ec30b558b8d43313',
    'universal_union_wallet_v6/exact_input.json':
        '49532be5fae2913f2ab56ae641452510d7b0f8f14ff7049de0dd62fa7b9a8936',
    'universal_union_wallet_v6/exact_certificate.json':
        '98fa318efae0c6fef36e87b1861d559ede340ab4aaf7ed390c426854e5711f1d',
    'maximal_root_tail_wallet_v3/exact_certificate.json':
        'b7d27bcddc6da34bed635bf7c36a607ffea130b56bcb0f62803b94b3c20dc925',
    'maximal_root_tail_wallet_v3_audit/audit_result.json':
        '29af83b968bdab27fd060c7dbde69e1324684de1c9befa3a6475fe2becb49199',
}
for rel, digest in PINS.items():
    assert sha256((WS / rel).read_bytes()).hexdigest() == digest, rel


def read(rel):
    return json.loads((WS / rel).read_text())


def vector(mapping):
    assert all(0 <= int(k) < 257 for k in mapping)
    return [F(mapping.get(str(j), '0')) for j in range(257)]


def dot_rows(weights, rows):
    return [sum((w * F(rows[name]['a'].get(str(j), '0'))
                 for name, w in weights.items()), F(0)) for j in range(257)]


primary = read('maximal_root_tail_wallet_v3_audit/audit_result.json')
assert primary['status'] == 'PASS_INDEPENDENT_LITERAL_ROOT270_PRIMAL_DUAL_AND_131_COLUMNS'
assert primary['homogeneous_identity_columns'] == 131
root_certificate = read('maximal_root_tail_wallet_v3/exact_certificate.json')
bridge = read('main_root270_global_bridge/exact_certificate.json')
exported_root = read('main_root270_global_bridge/ROOT270_TRUE_BRANCH_P25.json')
old_input = read('universal_union_wallet_v6/exact_input.json')
old_certificate = read('universal_union_wallet_v6/exact_certificate.json')
assert old_input['variables'] == 257 and old_input['K_column'] == 256
assert old_input['nonnegative_columns'] == list(range(257))
assert len(old_input['atom_columns']) == 256
assert old_input['equality']['rhs'] == '1'
assert old_input['inequality_convention'] == 'a dot z >= rhs'

a = F(1767904008200582, 16877573861922720)
b = F(337340181272013, 16877573861922720)
assert a == F(primary['slope']) == F(root_certificate['universal_root_line']['a'])
assert b == F(primary['intercept']) == F(root_certificate['universal_root_line']['b'])
assert F(root_certificate['branch_union_OPT_weight']) == 0
assert F(bridge['root_a']) == a and F(bridge['root_b']) == b

# Reconstruct actual-root shares and coverage directly, retaining X and o as
# independent membership bits.  X is unused in this root theorem, not fixed.
W, O, U = [F(0)] * 257, [F(0)] * 257, [F(0)] * 257
for j, bits in enumerate(product((0, 1), repeat=8)):
    aa, x, o = bits[:6], bits[6], bits[7]
    assert old_input['atom_columns'][j] == {
        'index': j, 'a': list(aa), 'x': x, 'o': o}
    load = sum(aa)
    W[j] = F(bool(load))
    O[j] = F(o)
    U[j] = F(aa[0], load) if load else F(0)
assert W == vector(old_input['objective'])
assert O == vector(old_input['equality']['a'])
K = [F(0)] * 256 + [F(1)]
new_root = [U[j] - a * K[j] - b * O[j] for j in range(257)]
assert exported_root['name'] == 'ROOT270_TRUE_BRANCH_P25'
assert exported_root['family'] == 'TRUE_MAXIMUM_ROOT270'
assert exported_root['rhs'] == '0' and exported_root['numerical_divisor'] == '1'
assert new_root == vector(exported_root['a'])
assert exported_root == bridge['new_root_row']

# Literal payment of K-|union Q|/6: average of six legal size caps plus
# the exact menu-overlap remainder.  All 64 indexed menu patterns retained.
menu_cases = 0
for menu in product((0, 1), repeat=6):
    d, o = sum(menu), int(any(menu))
    overlap = F(d - o, 6)
    assert overlap >= 0
    customer_coefficient_from_caps = -sum((F(q, 6) for q in menu), F(0))
    assert customer_coefficient_from_caps + overlap == -F(o, 6)
    assert sum((F(1, 6) for _ in menu), F(0)) == 1  # K coefficient
    menu_cases += 1
menu_row = [K[j] - O[j] / 6 for j in range(257)]
assert menu_row == vector(bridge['additional_K_minus_O_over6_row'])

old_rows = {r['name']: r for r in old_input['raw_rows']}
assert len(old_rows) == 867
weights = {name: F(w) for name, w in old_certificate['dual']['row_weights'].items()}
assert len(weights) == 12 and all(w > 0 for w in weights.values())
assert weights == {name: F(w) for name, w in bridge['global_row_weights'].items()}
for name in weights:
    assert F(old_rows[name]['rhs']) == 0
old_alpha = F(old_certificate['dual']['normalization_multiplier'])
assert old_alpha == F(old_certificate['objective']) == F(bridge['old_alpha6'])
old_paid = dot_rows(weights, old_rows)
old_residual = [W[j] - old_alpha * O[j] - old_paid[j] for j in range(257)]
assert old_residual == vector(old_certificate['dual']['nonnegative_column_residual'])
assert all(r >= 0 for r in old_residual) and old_residual[256] == 0

old_name = 'ROOT30_B2_CAPACITY_FEEDBACK'
assert bridge['global_row_replacement'] == {old_name: exported_root['name']}
a2 = F(16737205739803, 163703695393620)
b2 = F(384153998287, 19098764462589)
old_root = [U[j] - a2 * K[j] - b2 * O[j] for j in range(257)]
assert old_root == vector(old_rows[old_name]['a'])
da, db = a - a2, b - b2
epsilon = da / 6 + db
assert da > 0 and db < 0 and epsilon > 0
assert da == F(bridge['delta_a']) and db == F(bridge['delta_b'])
assert epsilon == F(bridge['epsilon_on_K_at_least_O_over_6'])
for j in range(257):
    assert old_root[j] == new_root[j] + da * menu_row[j] + epsilon * O[j]

lam = weights[old_name]
assert lam == F(21667805751695512966068982199018795000,
                32141494323534104473815525970700519881)
menu_weight = lam * da
gain = lam * epsilon
new_alpha = old_alpha + gain
assert menu_weight > 0 and gain > 0
assert menu_weight == F(bridge['additional_K_minus_O_over6_weight'])
assert gain == F(bridge['new_gain'])
assert new_alpha == F(bridge['new_alpha'])
assert new_alpha == F(688930071678645080978179164614013566510285979581569,
                      1564818589840432726302471545016752331710657348785374)
new_paid = [old_paid[j] - lam * old_root[j] + lam * new_root[j]
            + menu_weight * menu_row[j] for j in range(257)]
new_residual = [W[j] - new_alpha * O[j] - new_paid[j] for j in range(257)]
assert new_residual == old_residual
assert new_residual == vector(bridge['all257_global_residuals'])
identity = [W[j] - new_alpha * O[j] - new_paid[j] - old_residual[j]
            for j in range(257)]
assert identity == [F(0)] * 257

manifest = read('main_root270_global_bridge/manifest.json')
for item in manifest['files']:
    data = (WS / 'main_root270_global_bridge' / item['path']).read_bytes()
    assert sha256(data).hexdigest() == item['sha256']
    assert len(data) == item['bytes']

result = {
    'status': 'PASS_INDEPENDENT_MENU_PAYMENT_AND_GLOBAL257_IDENTITY',
    'root_source_audit': 'check_exact.py / audit_result.json',
    'standard257_new_root_columns_rebuilt': 257,
    'standard257_old_root_columns_rebuilt': 257,
    'literal_six_index_menu_patterns_checked': menu_cases,
    'old_v6_positive_payments_replayed': len(weights),
    'old_v6_dual_identity_columns': 257,
    'new_global_identity_columns': 257,
    'old_root_weight': str(lam), 'delta_a': str(da), 'delta_b': str(db),
    'epsilon': str(epsilon), 'additional_menu_budget_weight': str(menu_weight),
    'old_alpha': str(old_alpha), 'new_alpha': str(new_alpha),
    'exact_gain': str(gain),
    'new_alpha_decimal_display_only': float(new_alpha),
    'unchanged_atom_residuals': 256, 'K_residual': '0',
    'atom_residual_zero_indices': [j for j in range(256) if old_residual[j] == 0],
    'atom_residual_positive_count': sum(r > 0 for r in old_residual[:256]),
    'all257_identity_residuals': {str(j): str(r) for j, r in enumerate(identity)},
    'source_scope': ('Root theorem and true menu-size payment independently audited here; '
                     'the remaining eleven v6 budget source theorems are inherited, '
                     'their frozen coefficients and complete dual identity are replayed.'),
    'zero_OPT_handling': 'OPT6=0 gives W>=0 directly; no normalization division is used.',
    'optimizer_calls': 0,
    'Main_builder_or_prior_audit_code_executed_or_imported': False,
    'source_sha256': {'research/workspaces/six-boss1-20261111/' + p: h
                      for p, h in PINS.items()},
    'not_claimed': ['new global LP optimum', 'new matching primal',
                    'SPE realization', 'best-known bound or half theorem'],
    'outstanding_errors': [],
}
(HERE / 'bridge_audit_result.json').write_text(
    json.dumps(result, indent=2, ensure_ascii=False) + '\n')
print(json.dumps({k: result[k] for k in ['status', 'new_global_identity_columns',
    'literal_six_index_menu_patterns_checked', 'new_alpha', 'exact_gain',
    'unchanged_atom_residuals', 'K_residual', 'outstanding_errors']}, indent=2))
