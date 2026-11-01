"""Definition-level second r=2 endpoint enumeration from frozen payoff kernel.

This does not independently reconstruct the threshold customer's moments.
It checks all ties / all possible SPE tails, not one chosen best response.
"""
from pathlib import Path
from fractions import Fraction as F
import json
import hashlib

HERE = Path(__file__).resolve().parent


def main():
    kp = HERE/'research_5/full156_tail2_kernel_10344.json'
    wp = HERE/'research_5/full156_tail2_welfare_10344.json'
    k, w = json.loads(kp.read_text()), json.loads(wp.read_text())
    source = HERE/'research_5/combined_branch_master_exact.json'
    assert hashlib.sha256(source.read_bytes()).hexdigest() == k['source_sha256']
    original = json.loads(source.read_text())
    hist = [c for c in original['columns']
            if c['kind'] == 'hist' and F(c['weight']) > 0]
    # The six T labels cover every constructed atom: every positive old
    # histogram has exactly one T-member among its six indexed words.
    assert sum(F(c['weight']) for c in hist) == 1
    assert all(sum(v for j, v in enumerate(c['hist']) if (j >> 2) & 1) == 1
               for c in hist)
    assert w['kernel_sha256'] == hashlib.sha256(kp.read_bytes()).hexdigest()
    assert w['topics'] == k['topics']
    names = k['topics']
    n = len(names)
    assert n == 156 and len(set(names)) == n
    u = [[int(x) for x in row] for row in k['payoff_numerators']]
    ff = list(map(int, k['F_numerators']))
    gg = [[int(x) for x in row] for row in k['G_numerators']]
    den = int(k['payoff_denominator_for_normalized_point'])
    scale = int(k['unit_customer_scale'])
    ww = [[int(x) for x in row] for row in w['welfare_numerators']]
    br = []
    comparisons = 0
    for a in range(n):
        best = max(u[b][a] for b in range(n))
        br.append([b for b in range(n) if u[b][a] == best])
        for b in range(n):
            assert gg[a][b] == gg[b][a]
            assert u[a][b] == ff[a]-gg[a][b]
            comparisons += 1
    threshold = max(min(u[a][b] for b in br[a]) for a in range(n))
    tails = [(a, b) for a in range(n) for b in br[a]
             if u[a][b] >= threshold]
    welfare = min(F(ww[a][b], scale) for a, b in tails)
    aa, bb = k['actual_last_pair']
    deficit = max(F(0), F(threshold-u[aa][bb], den))
    assert len(tails) == 6
    assert {(names[a], names[b]) for a, b in tails} == {
        (f'C{i}', f'B{i}') for i in range(1, 7)}
    assert welfare == F(
        6245548492134933268269408059574569,
        10760672980915589666594608867865816)
    result = {
        'scope': 'Second definition-level r2 SPE endpoint enumeration from '
                 'author kernel; fixed actual first four topics only. '
                 'Not an independent customer-moment reconstruction.',
        'kernel_sha256': hashlib.sha256(kp.read_bytes()).hexdigest(),
        'welfare_sha256': hashlib.sha256(wp.read_bytes()).hexdigest(),
        'topics': n, 'ordered_pair_payoff_checks': comparisons,
        'SPE_tail_count': len(tails),
        'SPE_tails': [[names[a], names[b]] for a, b in tails],
        'minimum_normalized_welfare': str(welfare),
        'normalized_OPT6': '1; six T topics cover all mass',
        'minimum_strictly_above_half': welfare > F(1, 2),
        'old_actual_last_is_best_reply': bb in br[aa],
        'old_actual_penultimate_deficit': str(deficit),
        'three_times_deficit': str(3*deficit),
        'old_half_gap': str(1-2*F(k['source_W'])),
        'old_target_cannot_pass_known_repair_cost':
            3*deficit >= 1-2*F(k['source_W']),
        'main_target': 'OPEN; other first-four prefixes and other catalogues '
                       'are not excluded',
    }
    HERE.joinpath('audit_full156_reply_set.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
