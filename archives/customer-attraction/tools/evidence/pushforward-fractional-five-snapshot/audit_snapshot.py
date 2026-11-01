"""Current exact reconstruction of one frozen floating snapshot; not its generator.

Standard library only. Reuses the frozen complete action function, checks every
ordered history against both literal decimal weights and an explicitly NEW
integer reconstruction, then evaluates stated fractional-load constructions.
No optimization, random search, or new SPE selection is performed.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, combinations_with_replacement
from pathlib import Path
import argparse
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
OLD = ROOT / 'archives/customer-attraction/tools/evidence/security-chain-boundary/original'
FILES = {
    'snapshot': (HERE / 'original.json', '207bb54c38056a422191ffdc2ef0a134626b6d3a601cc075f035e2104a623f89'),
    'game': (OLD / 'examples/customer_attraction/five_individual_security.json', '689cae34e0cbed60583710cd8e40a06b558cde59ddd566b2cb89e06ab5e8700f'),
    'policy': (OLD / 'evidence/certificates/customer_attraction/five_individual_security.json', '372bea6caf743792be542c411e9bcb961b6af6d31dc89d76e6a903e609be990f'),
}


def run():
    if sys.flags.optimize:
        raise RuntimeError('This audit requires enabled assertions; do not use Python -O.')
    evidence = {}
    for name, (path, sha) in FILES.items():
        raw = path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == sha
        evidence[name] = {'path': str(path.relative_to(ROOT)), 'bytes': len(raw), 'sha256': sha}
    s = json.loads(FILES['snapshot'][0].read_text(), parse_float=F)
    game = json.loads(FILES['game'][0].read_text())
    cert = json.loads(FILES['policy'][0].read_text())
    assert set(s) == {'p', 'weights', 'extra', 'name', 'masklist', 'gap'}
    assert game['players'] == 5 and len(game['topics']) == 10
    assert s['name'] == 'five_individual_security' and s['extra'] == 0
    masks = tuple(sum(1 << a for a in c['topics']) for c in game['customers'])
    assert list(masks) == s['masklist'] and len(masks) == len(s['weights']) == 29
    assert len(s['p']) == 10 and min(s['p']) >= 0 and min(s['weights']) >= 0
    expected_histories = tuple(h for d in range(5) for h in product(range(10), repeat=d))
    actions = cert['strategy']['actions']
    policy = {tuple(row['history']): row['action'] for row in actions}
    assert len(actions) == len(policy) == 11111 and set(policy) == set(expected_histories)
    assert all(type(a) is int and 0 <= a < 10 for a in policy.values())

    @lru_cache(None)
    def terminal(h):
        return h if len(h) == 5 else terminal(h + (policy[h],))

    def counts(z):
        return tuple(z.count(a) for a in range(10))

    # The new candidate is stated explicitly, never silently identified with floats.
    multiplicities = tuple(1 if b in (16, 512) else 20 if b == 495
                           else 0 if b in (511, 1007) else 15 for b in masks)
    assert sum(multiplicities) == 382
    rational = tuple(F(v, 73) for v in multiplicities)
    assert tuple(x.limit_denominator(1000) for x in s['weights']) == rational
    weight_sets = {'literal_decimal': tuple(s['weights']), 'reconstructed': rational}

    def ic_audit(weights):
        @lru_cache(None)
        def payoff(a, zcounts):
            return sum((w / sum(zcounts[i] for i in range(10) if b >> i & 1)
                        for b, w in zip(masks, weights) if b >> a & 1), F(0))
        minimum = None
        first_negative = None
        negative = strict = tied = 0
        for h in expected_histories:
            own = payoff(policy[h], counts(terminal(h)))
            for a in range(10):
                slack = own - payoff(a, counts(terminal(h + (a,))))
                if minimum is None or slack < minimum:
                    minimum = slack
                if slack < 0:
                    negative += 1
                    if first_negative is None:
                        first_negative = {'history': h, 'prescribed': policy[h], 'deviation': a,
                                          'slack': str(slack)}
                elif a != policy[h]:
                    strict += slack > 0
                    tied += slack == 0
        z = terminal(())
        return {
            'ordered_histories': len(expected_histories), 'comparisons_including_self': 111110,
            'negative_comparisons': negative, 'strict_nonself': strict, 'tied_nonself': tied,
            'minimum_slack': str(minimum), 'first_negative': first_negative,
            'actual_path': z, 'actual_utilities': [str(payoff(a, counts(z))) for a in z],
        }

    audits = {name: ic_audit(weights) for name, weights in weight_sets.items()}
    assert audits['reconstructed']['negative_comparisons'] == 0
    assert audits['reconstructed']['actual_utilities'] == ['1'] + ['77/73'] * 4
    full = tuple(terminal((a,)) for a in range(10))
    tails = tuple(z[1:] for z in full)
    assert tails == ((5, 6, 7, 8),) * 5 + ((0, 1, 2, 3),) * 5

    def prices(weights, load):
        return tuple(sum((w / (1 + sum(load[i] for i in range(10) if b >> i & 1))
                          for b, w in zip(masks, weights) if b >> a & 1), F(0))
                     for a in range(10))

    def push(weights, p, branches):
        load = tuple(sum((p[a] * branches[a].count(i) for a in range(10)), F(0)) for i in range(10))
        g = prices(weights, load)
        average = sum((p[a] * g[a] for a in range(10)), F(0))
        return {'load_mass': str(sum(load)), 'topic_loads': list(map(str, load)),
                'query_prices': list(map(str, g)), 'average': str(average), 'average_float': float(average)}

    # Reproduction of printed gap uses binary float arithmetic as in a discovery computation.
    pf = list(map(float, s['p'])); wf = list(map(float, s['weights']))
    def float_push(branches):
        load = [sum(pf[a] * branches[a].count(i) for a in range(10)) for i in range(10)]
        g = [sum(w / (1 + sum(load[i] for i in range(10) if b >> i & 1))
                 for b, w in zip(masks, wf) if b >> a & 1) for a in range(10)]
        return sum(pf[a] * g[a] for a in range(10))
    float_root = sum(w / sum(bool(b >> a & 1) for a in terminal(()))
                     for b, w in zip(masks, wf) if b >> policy[()] & 1)
    gap_recomputed = float_push(tails) - float_root
    assert abs(gap_recomputed - float(s['gap'])) < 1e-13
    p_normalized = tuple(p / sum(s['p']) for p in s['p'])
    rational_saved_p = push(rational, p_normalized, tails)
    assert F(rational_saved_p['average']) > 1

    # A simpler exact query witnesses the same restricted construction failure.
    p_simple = tuple(F(1, 2) if a in (4, 9) else F(0) for a in range(10))
    simple = push(rational, p_simple, tails)
    assert F(simple['average']) == F(223, 219)
    assert max(map(F, simple['query_prices'])) == F(223, 219)
    free_standard = prices(rational, (F(2, 5),) * 10)
    free_extra = prices(rational, (F(1, 2),) * 10)
    assert max(free_standard) == F(1525, 1533) < 1
    assert max(free_extra) == F(61, 73) < 1
    welfare = lambda z: sum(v for b, v in zip(masks, multiplicities) if any(b >> a & 1 for a in z))
    W = welfare(terminal(()))
    OPT = max(welfare(z) for z in combinations_with_replacement(range(10), 5))
    assert (W, OPT) == (381, 382)
    return {
        'status': 'PASS_CURRENT_EXACT_RECONSTRUCTION',
        'python_version': sys.version,
        'audit_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'assertions_enabled': True,
        'scope': 'One frozen floating snapshot; literal-decimal IC diagnostic, new 382-unit reconstruction with the frozen 11111-action policy, and stated fixed fractional backgrounds. No discovery-generator replay or free-background optimization.',
        'evidence': evidence,
        'snapshot_fields': list(s), 'literal_p_sum': str(sum(s['p'])),
        'literal_p_sum_minus_one': str(sum(s['p']) - 1),
        'saved_gap_token': str(s['gap']), 'float_root': float_root,
        'float_tail_gap_recomputed': gap_recomputed,
        'float_full_terminal_gap': float_push(full) - float_root,
        'multiplicities': multiplicities, 'normalization': 73,
        'maximum_weight_change': str(max(abs(x - y) for x, y in zip(s['weights'], rational))),
        'ic_audits': audits, 'forced_root_terminals': full,
        'normalized_saved_query_tail_push': rational_saved_p,
        'simple_exact_query': list(map(str, p_simple)), 'simple_exact_tail_push': simple,
        'simple_exact_gap': str(F(simple['average']) - 1),
        'uniform_free_standard_prices': list(map(str, free_standard)),
        'uniform_free_extra_prices': list(map(str, free_extra)),
        'unit_W': W, 'unit_OPT': OPT, 'unit_half_margin': 2 * W - OPT,
        'static_five_slot_multiset_profiles': 2002,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = json.dumps(run(), ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.write_text(result)
    else:
        print(result, end='')
