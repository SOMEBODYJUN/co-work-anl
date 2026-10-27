"""Independent explicit-unit checker for the six-player ESM embedding.

All ordered histories are checked. Terminal payoff caching by counts only
caches arithmetic; the given policy remains fully ordered-history dependent.
Sixty-scaled utilities are exact integers since denominators are at most six.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent/'attack/potential_tax/six_esm_embedding.json'


def main():
    packet = json.loads(PACKET.read_text())
    instance = packet['instance']
    p, m = len(instance['topics']), instance['players']
    assert (p, m) == (6, 6)
    clients = [frozenset(t['topics']) for t in instance['customers']
               for _ in range(t['multiplicity'])]
    assert all(isinstance(t['multiplicity'], int) and t['multiplicity'] > 0
               for t in instance['customers'])
    policy = {tuple(item['history']): item['action'] for item in packet['strategy']}
    assert len(policy) == len(packet['strategy'])
    alphabet = tuple(range(p))
    histories = [h for depth in range(m) for h in product(alphabet, repeat=depth)]
    assert set(policy) == set(histories)
    assert all(action in alphabet for action in policy.values())
    scale = 60

    @lru_cache(None)
    def payoff_by_counts(counts):
        # Each entry in clients is one different unit customer, no weighted
        # customer evaluator or author's certificate code is used.
        payoff = [0]*p
        for likes in clients:
            count = sum(counts[a] for a in likes)
            if count:
                assert scale % count == 0
                share = scale//count
                for a in likes:
                    payoff[a] += share
        return tuple(payoff)

    def payoffs(leaf):
        counts = tuple(leaf.count(a) for a in alphabet)
        return payoff_by_counts(counts)

    finish = {leaf: leaf for leaf in product(alphabet, repeat=m)}
    comparisons = 0
    min_slack = None
    for depth in range(m-1, -1, -1):
        for h in product(alphabet, repeat=depth):
            own = finish[h+(policy[h],)]
            finish[h] = own
            actual_u = payoffs(own)[own[depth]]
            for a in alphabet:
                other = finish[h+(a,)]
                slack = actual_u-payoffs(other)[a]
                assert slack >= 0, (h, a, slack)
                min_slack = slack if min_slack is None else min(min_slack, slack)
                comparisons += 1
    actual = finish[()]
    u = [F(payoffs(actual)[a], scale) for a in actual]
    prefix = tuple(packet['examined_prefix'])
    assert prefix == actual[:len(prefix)]
    action = policy[prefix]
    r = m-len(prefix)
    old = [sum(a in likes for a in prefix) for likes in clients]
    H = [F()]
    for j in range(1, m+1):
        H.append(H[-1]+F(1, j))

    def phi(suffix):
        return sum((H[b+sum(a in likes for a in suffix)]-H[b]
                    for b, likes in zip(old, clients)), F())

    tails = list(product(alphabet, repeat=r))
    P = max(map(phi, tails))
    PA = max(phi(tail) for tail in tails if action in tail)
    safe = sum((F(1, b+r) for b, likes in zip(old, clients) if action in likes), F())
    surplus = u[len(prefix)]-safe
    loss = P-PA
    W = sum(any(a in likes for a in actual) for likes in clients)
    # Six legal themes and six players permit selecting all themes; this
    # covers every listed customer and reaches the obvious total-size bound.
    OPT = sum(bool(likes) for likes in clients)
    assert sum(u) == W and W == 1056 and OPT == 1131
    assert actual == (5, 5, 5, 0, 1, 2)
    assert u == list(map(F, (170, 170, 170, 166, 190, 190)))
    assert (P, PA, safe, surplus, loss-surplus) == (F(801), F(754), F(120), F(46), F(1))
    assert loss > surplus and 2*W >= OPT
    report = {
        'status': 'PASS',
        'scope': 'complete six-player SPE refuting ESM at an actual fourth-player prefix; not a half counterexample',
        'packet_sha256': hashlib.sha256(PACKET.read_bytes()).hexdigest(),
        'explicit_unit_customers': len(clients),
        'complete_ordered_histories': len(histories),
        'all_full_strategy_ic': comparisons,
        'minimum_scaled_ic_slack': min_slack,
        'utility_integer_scale': scale,
        'arithmetic_terminal_count_cache_entries': payoff_by_counts.cache_info().currsize,
        'actual_path': list(actual), 'actual_payoffs': list(map(str, u)),
        'actual_examined_prefix': list(prefix),
        'all_ordered_suffix_comparisons': len(tails),
        'P3_background': str(P), 'P3_background_containing_A': str(PA),
        'forcing_loss': str(loss), 'actual_surplus': str(surplus),
        'ESM_violation': str(loss-surplus), 'W': W, 'OPT6': OPT,
    }
    HERE.joinpath('six_esm_units_audit.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
