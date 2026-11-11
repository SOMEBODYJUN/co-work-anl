"""Attach the 28 exact positive rows to the unchanged 17-atom measure.

No LP or pricing is called: the previous common measure already passes every
new row. The separate verifier derives all literal queries and budgets afresh.
"""
from fractions import Fraction as F
import json
import sys

from interface import HERE, BASE, PIN, sha, names, coefficients


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')


def main():
    prevpath = BASE/'root_old_tail_joint/joint_completion_exact.json'
    previous = json.loads(prevpath.read_text())
    priorinput = json.loads((BASE/'root_old_tail_joint/input_snapshot_exact.json').read_text())
    assert previous['point_sha256'] == PIN == sha(BASE/'peer_augmented_lp/augmented_lp_exact.json')
    sourcepaths = ['peer_augmented_lp/augmented_lp_exact.json',
                   'background_five_bridge/fixed53_b0_profit.json',
                   'background_five_bridge/fixed53_b1_profit.json',
                   'root_old_tail_joint/joint_completion_exact.json',
                   'root_old_tail_joint/input_snapshot_exact.json',
                   'cross_root_pricing/joint_completion_exact.json']
    snapshot = {'point_sha256': PIN,
                'sources': [{'path': p, 'sha256': sha(BASE/p)} for p in sourcepaths],
                'projection_inputs': priorinput['projection_inputs'],
                'candidate_root_states': priorinput['new_root_certificate']['support'],
                'previous_root_state_margins': previous['new_root_state_margins'],
                'previous_atom_count': previous['support_atoms'],
                'construction': 'No new mass solve: preserve every previous atom and its mass exactly.'}
    write(HERE/'inputs_exact.json', snapshot)
    totals = {n: F(0) for n in names()}
    for a in previous['atoms']:
        for n, v in coefficients(a['actual'], a['old_words'], a['new_words']).items():
            totals[n] += F(a['mass'])*v
    assert len(totals) == 28 and min(totals.values()) > 0
    out = {k: v for k, v in previous.items() if k not in
           ('status', 'scope', 'input_snapshot_sha256', 'discovery_sha256',
            'normalization', 'old_budget_count', 'new_interface_orbits',
            'new_literal_queries', 'budget_slacks', 'active_recovery_rows')}
    out.update({
        'status': 'EXACT 203-BUDGET OLD-B/C AND SIX-ROOT-TAIL COMMON COMPLETION',
        'scope': 'Finite necessary membership projection only; no complete SPE and no half conclusion.',
        'input_snapshot_sha256': sha(HERE/'inputs_exact.json'),
        'previous_certificate_sha256': sha(prevpath),
        'construction_script_sha256': sha(__file__),
        'new_coefficient_script_sha256': sha(HERE/'interface.py'),
        'actual_argv': [sys.executable, *sys.argv],
        'normalization': 'Six-root source IC average coefficient exactly 1; all 203 other budget multipliers are arbitrary fixed nonnegative numbers.',
        'construction': 'The same 17 exact old-C completion atoms, with unchanged positive masses.',
        'root_budget_count': 163,
        'previous_interface_orbits': 12,
        'added_interface_orbits': 28,
        'total_interface_orbits': 40,
        'previous_literal_queries': 216,
        'added_literal_queries': 504,
        'total_literal_queries': 720,
        'nonroot_budget_count': 203,
        'total_budget_count_including_source': 204,
        'new_row_minimum': str(min(totals.values())),
        'new_row_minimum_float': float(min(totals.values())),
        'budget_slacks': previous['budget_slacks'] +
            [{'row': list(n), 'budget': '0', 'slack': str(v), 'float': float(v)}
             for n, v in totals.items()],
    })
    assert len(out['budget_slacks']) == 204
    write(HERE/'joint_completion_exact.json', out)
    print(json.dumps({k: out[k] for k in ('status', 'support_atoms', 'root_slack',
                     'root_slack_float', 'new_row_minimum', 'new_row_minimum_float',
                     'nonroot_budget_count', 'total_literal_queries')}, indent=2))


if __name__ == '__main__':
    main()
