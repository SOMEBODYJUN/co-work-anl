#!/usr/bin/env python3
"""One fixed stdlib reconciliation; no games, discovery, original entrypoints or LP.

The mature 160-row rho table is an input, not re-derived by repeating its 1280-
state/4096-state audits. New checks cover the two 192-type duals and the saved
32-row insurance formula report. This is a dependent certificate check.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent
RHO_PATH = 'archives/customer-attraction/tools/evidence/binary-tail-two-slope/original/oct25_binary_tail_raw_audit.json'
NAMES = ['bare0', 'bare1', 'bare2', 'bare3', 'negative_retained_binary',
         'last_query', 'root_profit', 'T_size']


def q(n, d):
    return F(n, d) if n else F(0)


def read(path):
    raw = path.read_bytes()
    return json.loads(raw), {'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    reference, rho_identity = read(args.repo/RHO_PATH)
    cert, cert_identity = read(HERE/'original/retained_binary_capacity_certificate.json')
    saved, swing_identity = read(HERE/'original/audit_insurance_swing.json')
    assert reference['certificate_sha256'] == cert['binary_sha256'] == 'dc50440f598bad7c511e01bccd8cb14a0c8f84d61396df354cdff8631e292511'
    assert (reference['beta_out'], reference['beta_in']) == ('1999/1000', '5/3')
    rho = {}
    for row in reference['retained_residuals_160']:
        key = (row['p'], tuple(map(int, row['abcd'])), row['comparison_count'])
        assert key not in rho
        rho[key] = F(row['minimum_residual'])
    assert set(rho) == set(product(range(2), product(range(2), repeat=4), range(5)))
    assert min(rho.values()) >= 0
    assert cert['rho_types'] == len(rho) == 160
    assert cert['universe_size'] == 192

    states = list(product(range(2), product(range(2), repeat=4), range(6)))
    matrix = []
    for t, tail, j in states:
        n = sum(tail)
        v, z = q(n, t+n), q(t, t+n)
        target = sum((F(count, 5)*q(j-included, t+j-included)
                      for included, count in [(0, 5-j), (1, j)] if count), F(0))
        credit = sum((F(count, 5)*rho[t, tail, j-included]
                      for included, count in [(0, 5-j), (1, j)] if count), F(0))
        base = (F(5, 3) if t else F(1999, 1000))*v-target-credit
        last = q(j, t+sum(tail[:3])+1)-5*q(tail[3], t+n)
        matrix.append(list(map(F, tail))+[-base, last, z, F(t)])

    cuts = []
    for cut in cert['cuts']:
        assert set(cut['multipliers']) <= set(NAMES)
        dual = [F(cut['multipliers'].get(name, 0)) for name in NAMES]
        assert all(x >= 0 for x in dual[:7])  # T_size is an equality multiplier.
        residuals = [sum((a*b for a, b in zip(row, dual)), F(0))-int(s[2]>0)
                     for row, s in zip(matrix, states)]
        assert min(residuals) == F(cut['minimum_residual']) == 0
        assert sum(x == 0 for x in residuals) == cut['zero_residuals'] == 8
        assert F(cut['row']['root_u']) == dual[6]
        assert F(cut['row']['K']) == sum(dual[:4])+dual[7]
        assert cut['row']['O'] == 1
        selected = []
        for t, tail, j in cut['selected_types']:
            i = states.index((t, tuple(tail), j))
            assert residuals[i] == 0
            selected.append(i)
        assert len(selected) == len(set(selected)) == sum(x != 0 for x in dual)
        cuts.append({'ratio_for_basis': cut['ratio_for_basis'], 'types': len(states),
                     'minimum_residual': str(min(residuals)), 'zero_residuals': 8,
                     'selected_types_all_distinct_and_tight': True,
                     'row_coefficients_match': True,
                     'residuals': [{'t': t, 'tail': list(tail), 'j': j, 'slack': str(slack)}
                                   for (t, tail, j), slack in zip(states, residuals)]})
    assert len(cuts) == 2

    rows = []
    for p, k, ell, emm in product(range(4), range(2), range(2), range(2)):
        loss = q(k, p+k+ell)-q(k, p+k+emm)
        difference = q(ell, p+k+ell)-q(emm, p+k+emm)
        slack = F(p+k+ell > 0)-3*loss-difference
        assert slack >= 0
        rows.append({'p': p, 'K': k, 'L': ell, 'M': emm,
                     'current_loss': str(loss), 'last_difference': str(difference), 'slack': str(slack)})
    assert rows == saved['rows']
    assert saved['cases'] == len(rows) == 32 and saved['all_nonnegative'] is True
    assert saved['minimum_slack'] == str(min(F(row['slack']) for row in rows)) == '0'
    assert saved['sharp_swing_example'] == {'current_loss': '1', 'actual_insurance_welfare': 3,
                                          'last_reply_difference': '0', 'loss_over_welfare': '1/3'}
    assert 2*F(rows[5]['current_loss'])+F(rows[2]['current_loss']) == 1
    assert 2*F(rows[5]['last_difference'])+F(rows[2]['last_difference']) == 0
    assert saved['five_player_cartesian_full_insurance_budget'] == {
        'k2_minimum_B_over_a': str(3*(1-F(1, 4))),
        'k2_ratio_upper_bound': str((5+F(9, 4))/(2+F(9, 4))),
        'k_ge_3_ratio_upper_bound': '5/3'}
    result = {'status': 'PASS', 'scope': 'fixed saved formula/dual reconciliation; no SPE enumeration',
              'inputs': [rho_identity, cert_identity, swing_identity],
              'rho_input_rows': 160, 'rho_1280_or_4096_audit_replayed': False,
              'original_program_entrypoints_executed': 0, 'LP_calls': 0,
              'cuts': cuts, 'insurance_rows_equal_saved': 32,
              'insurance_rows': rows, 'all_saved_arithmetic_fields_reconciled': True}
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('cuts', 'insurance_rows')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
