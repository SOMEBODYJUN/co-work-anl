#!/usr/bin/env python3
"""Read preserved bytes and evaluate N5 functionals on the 16 stored atoms.

This does not construct M, solve an LP, audit all primal rows/dual columns,
or construct/verify a full SPE. The exact LP certificate is existing evidence.
"""
from fractions import Fraction as F
from hashlib import sha256
from math import comb
from pathlib import Path
import json
import sys

import numpy as np

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
BASE = ROOT / 'archives/customer-attraction/tools/evidence'
NPZ = BASE / 'boss5-profiles/test_profiles.arrays.npz'
AUDIT = BASE / 'boss5-profiles/array-and-exact-lp-audit.json'
PREFIX = BASE / 'five-prefix-interface-and-root-D-primary/source-root/research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/n5'
R3 = PREFIX / 'induction/audit_two_prefix_interface.json'
R4 = PREFIX / 'parent/audit_root_share_polynomial.json'


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def share(n, d):
    return F(n, d) if n else F(0)


def run():
    old = json.loads(AUDIT.read_text())
    r3 = {k: F(v) for k, v in json.loads(R3.read_text())['r3_minima'].items()}
    r4 = {k: F(v) for k, v in json.loads(R4.read_text())['table'].items()}
    # Eagerly read all eight arrays; only their existing byte fingerprints are
    # compared. No matrix reconstruction, multiplication or LP audit follows.
    with np.load(NPZ, allow_pickle=False) as z:
        arrays = {k: z[k].copy() for k in z.files}
    array_read = {}
    for k, a in arrays.items():
        digest = sha256(a.tobytes(order='C')).hexdigest()
        assert digest == old['arrays'][k]['array_c_order_sha256']
        array_read[k] = {'shape': list(a.shape), 'dtype': str(a.dtype),
                         'nbytes': a.nbytes, 'array_c_order_sha256': digest,
                         'matches_existing_report': True}
    assert sha256(NPZ.read_bytes()).hexdigest() == old['input_sha256']
    assert len(r3) == 96 and len(r4) == 32
    names = list(map(str, arrays['names']))
    family_counts = {'safe': sum(':K' in n or (':opt' in n and ':tail' not in n) for n in names),
                     'tails': sum(':tail' in n for n in names), 'rootE': names.count('rootE')}
    assert family_counts == {'safe': 90, 'tails': 1416, 'rootE': 1}
    assert not any(n.startswith('1:0:') for n in names)
    dual_read = []
    for term in old['dual']:
        i = term['row']
        assert names[i] == term['name'] and F(term['multiplier']) > 0
        assert abs(float(F(term['multiplier'])) - arrays['dual'][i]) < 1e-12
        dual_read.append({'row': i, 'name': term['name'], 'multiplier': term['multiplier']})
    W = O = u1 = u2 = D3 = D4 = F(0)
    atoms = []
    for atom in old['primal']:
        i = atom['column']
        bits = tuple(map(int, atom['membership_ABCDEQRST']))
        j = atom['optimal_multiplicity']
        mass = F(atom['mass'])
        assert mass > 0
        assert tuple(map(int, arrays['x'][i])) == bits
        assert int(arrays['e'][i]) == j
        assert abs(float(mass) - arrays['primal'][i]) < 1e-12
        a, b, c, d, e = bits[:5]
        n = a + b + c + d + e
        o = int(j > 0)
        W += mass * int(n > 0)
        O += mass * o
        u1 += mass * share(a, n)
        u2 += mass * share(b, n)
        v4 = ''.join(map(str, (b, c, d, e)))
        f4 = sum(choose(j, h) * choose(5-j, 4-h) * share(h, a+h)
                 for h in range(5))
        delta = f4 / 4 - o + F(a * o, 2)
        eta = F(20233, 24000) / (1 + b+c+d+e) - F(1, 2) + F(5, 4) * r4['1:' + v4]
        d4 = F(a * (1-o), 2) + a*eta + F(5*(1-a), 4)*r4['0:' + v4] + delta
        p = a+b
        v3 = ''.join(map(str, (c, d, e)))
        H3 = sum(choose(j, h) * choose(5-j, 3-h)
                 * (share(h, p+h) + r3[f'{p}:{v3}:{h}']) for h in range(4))
        d3 = F(59,72)*share(p, n) - o + H3/6
        assert d3 >= 0 and d4 >= 0
        D3 += mass * d3
        D4 += mass * d4
        atoms.append({'column': i, 'membership_ABCDEQRST': atom['membership_ABCDEQRST'],
                      'j': j, 'mass': str(mass), 'D3_per_customer': str(d3),
                      'D4_per_customer': str(d4)})
    B3 = F(25,9)*W - F(47,24)*(u1+u2) - D3
    B4 = F(1499,600)*W - F(39727,24000)*u1 - D4
    assert W == 1 and O == F(old['exact_objective']) and B3 == O and B4 > O > 2
    result = {'W': W, 'O': O, 'u1': u1, 'u2': u2, 'D3': D3, 'D4': D4,
              'B3': B3, 'B4': B4, 'B3_minus_O': B3-O, 'B4_minus_O': B4-O,
              'B3_minus_twoW': B3-2*W, 'B4_minus_twoW': B4-2*W,
              'P3_payment': F(47,24)*(u1+u2)+D3,
              'P4_payment': F(39727,24000)*u1+D4}
    assert result['P3_payment'] < F(7,9)*W
    assert result['P4_payment'] < F(299,600)*W
    return {
        'scope': 'fresh byte reading and short 16-atom evaluation only; not a new LP certificate or SPE realization',
        'input_files': [{'path': str(p.relative_to(ROOT)), 'sha256': sha256(p.read_bytes()).hexdigest()}
                        for p in (NPZ, AUDIT, R3, R4)],
        'array_read': array_read,
        'stored_row_family_counts': family_counts,
        'forced_second_path_root_has_no_safe_rows': True,
        'stored_active_dual_terms_read': dual_read,
        'existing_exact_certificate_reused': {'primal_atoms': 16, 'dual_multipliers': 14,
            'historically_checked_primal_rows': 1507, 'historically_checked_dual_columns': 3072,
            'historical_audit_rerun': False},
        'exact_functional_evaluation': {k: str(v) for k, v in result.items()},
        'atom_evaluation': atoms,
        'conclusion': 'Both formal P3/P4 inequalities hold; neither half-payment condition holds. The point does not refute the interfaces or the current five-person half theorem.',
        'operations_not_performed': ['LP solve', 'original matrix construction', 'all-row primal audit',
            'all-column dual audit', 'game or full-SPE search', 'five-person half verifier'],
    }


if __name__ == '__main__':
    report = run()
    out = HERE / 'read-and-prefix-evaluation.json'
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report['exact_functional_evaluation'], ensure_ascii=False, indent=2))
