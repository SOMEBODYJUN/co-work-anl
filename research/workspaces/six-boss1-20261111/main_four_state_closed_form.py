"""Main's independent exact 16-cell form of the 82*u2+3*K inequality.

No discovery code is imported.  This solves all 16 stationary policies by
Fraction Gaussian elimination, then checks every literal middle membership.
The resulting table is a universal necessary inequality, not an SPE witness.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from hashlib import sha256
import json

HERE = Path(__file__).resolve().parent
STATES = list(product((0, 1), repeat=2))
THETA = F(1, 4)


def solve(a, b):
    n = len(b)
    a = [list(row) + [rhs] for row, rhs in zip(a, b)]
    for j in range(n):
        pivot = next(i for i in range(j, n) if a[i][j])
        a[j], a[pivot] = a[pivot], a[j]
        scale = a[j][j]
        a[j] = [x / scale for x in a[j]]
        for i in range(n):
            if i != j and a[i][j]:
                scale = a[i][j]
                a[i] = [x - scale * y for x, y in zip(a[i], a[j])]
    return [row[-1] for row in a]


def cost(p, q, a, t, c, middle):
    s = sum(middle)
    denominator = p + t + s + c
    numerator = 82 * t - 6 * c
    assert denominator or not numerator
    return (F(numerator, denominator) if denominator else F(0)) + s + F(4*q + 2*a, p+t+s+1)


def table():
    entries = []
    policies = []
    checks = 0
    for p, q in product((0, 1), repeat=2):
        edge = {(a, t, c): min(cost(p, q, a, t, c, bits)
                              for bits in product((0, 1), repeat=3))
                for a, t, c in product((0, 1), repeat=3)}
        values = []
        for policy in product((0, 1), repeat=4):
            mat = [[F(i == j) for j in range(4)] for i in range(4)]
            rhs = []
            for i, (a, t) in enumerate(STATES):
                c = policy[i]
                mat[i][STATES.index((t, c))] -= THETA
                rhs.append(edge[a, t, c])
            val = solve(mat, rhs)
            values.append(val)
            policies.append({'p': p, 'q': q, 'policy': policy,
                             'V': list(map(str, val))})
        best = [min(v[i] for v in values) for i in range(4)]
        assert any(v == best for v in values)
        for i, (a, t) in enumerate(STATES):
            gaps = []
            for c in (0, 1):
                for bits in product((0, 1), repeat=3):
                    gap = cost(p, q, a, t, c, bits) - best[i] + THETA*best[STATES.index((t, c))]
                    assert gap >= 0
                    gaps.append(gap)
                    checks += 1
            assert min(gaps) == 0
            entries.append({'p': p, 'q': q, 'a': a, 't': t,
                            'Psi': str((1-THETA)*best[i]),
                            'optimal_actions': [c for c in (0, 1)
                                if best[i] == edge[a, t, c] + THETA*best[STATES.index((t, c))]]})
    return entries, policies, checks


def main():
    entries, policies, checks = table()
    lookup = {(e['p'], e['q'], e['a'], e['t']): F(e['Psi']) for e in entries}
    point_path = HERE/'zz_closure_lp/round2/augmented_lp_exact.json'
    point_hash = sha256(point_path.read_bytes()).hexdigest()
    assert point_hash == 'bf47390017e37f49f47a8f89126eb8e812982e16bd535adb555f042c178a2ca3'
    point = json.loads(point_path.read_bytes())
    pack_path = HERE/'shared_source_deepening/selected_all_named_19556.json'
    pack_hash = sha256(pack_path.read_bytes()).hexdigest()
    assert pack_hash == '3b373504be8593d6737433ea8341aac5eba67a153243392d173631e05f02e130'
    candidates = json.loads(pack_path.read_bytes())['selected_rows']
    selected = [r for r in candidates if r.get('parameters', {}).get('source') == '82/89']
    assert len(selected) == 1
    old = {int(i): F(v) for i, v in selected[0]['coefficients']}
    full = {}
    for i, col in enumerate(point['columns']):
        value = F(0)
        if col['kind'] == 'K':
            value = F(3, 89)
        if col['kind'] == 'maximum-root-family-state':
            act = list(map(int, point['columns'][col['hist_column']]['actual_bits']))
            payout = F(act[1], sum(act)) if sum(act) else F(0)
            psi = lookup[act[0], col['hidden'][4], act[5], col['hidden'][3]]
            value = (82*payout-psi)/89
        assert value == old.get(i, F(0)), (i, value, old.get(i, F(0)))
        if value:
            full[i] = value
    slack = sum((v*F(point['columns'][i]['weight']) for i, v in full.items()), F(0))
    assert slack == F(selected[0]['exact_slack']) < 0
    report = {
        'claim': 'For every six-player complete-history pure SPE and any three legal labels A,T,Q, 82*u2+3*K >= sum_x Psi(p=1_A1,q=1_Q,a=1_A,t=1_T).',
        'budget_reason': 'Source IC weight 82; three intermediate capacity rows weight 1 each; last-player queries Q weight 4 and previous theme weight 2, with zero external query budget.',
        'source_history': 'The actual one-label history (A1), before player 2.',
        'theta': '1/4',
        'state_transition': '(a,t) -> (t,c)',
        'initial_previous_label': 'Any legal A; it need not map to T under C.',
        'state_order': STATES,
        'entries': entries,
        'all_stationary_policies': policies,
        'literal_Bellman_checks': checks,
        'all_exact': True,
        'source_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'point_audit': {
            'point_sha256': point_hash, 'cut_pack_sha256': pack_hash,
            'all_columns_reconstructed': len(point['columns']),
            'all_columns_equal': True, 'normalization': 'divide integer inequality by 89',
            'selected_initial_labels': ['A6', 'M1:H3', 'M1:H4'],
            'normalized_slack': str(slack), 'normalized_slack_float': float(slack)
        },
        'scope': 'General necessary inequality. Its application to a relaxation point is a separation only, not an original-game counterexample.'
    }
    out = HERE/'main_four_state_closed_form.json'
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'entries': entries, 'literal_Bellman_checks': checks,
                      'output': str(out)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
