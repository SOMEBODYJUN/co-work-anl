"""Exact ONE-GAP attack on one named existing m5/p10 instance only.

Checks all root SPE endpoints, all root-realizable first-three count prefixes,
and the exact two-tail potential maximum.  The security certificate is checked
against every four-rival topic multiset. No random instances or strategy cones.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT))
from customer_attraction.model import Instance
from customer_attraction.exact import ExactSPESolver
from customer_attraction.certificate import verify_certificate


def main():
    ip = ROOT / 'examples/customer_attraction/five_individual_security.json'
    cp = ROOT / 'evidence/certificates/customer_attraction/five_individual_security.json'
    inst = Instance.from_dict(json.loads(ip.read_text()))
    raw = json.loads(cp.read_text())
    p = tuple(map(F, raw['security']['primary']))
    v = F(raw['security']['value'])
    assert len(p) == inst.topic_count and sum(p) == 1 and min(p) >= 0
    zero = (0,) * inst.topic_count
    def inc(c, a):
        return c[:a] + (c[a] + 1,) + c[a+1:]
    def utility(a, c):
        return inst.topic_payoff(a, c)
    min_security = None
    backgrounds = 0
    for rivals in combinations_with_replacement(range(inst.topic_count), 4):
        c = inst.counts(rivals)
        value = sum((p[a] * utility(a, inc(c, a)) for a in range(inst.topic_count)), F())
        min_security = value if min_security is None else min(min_security, value)
        backgrounds += 1
    assert min_security == v
    # The frozen dual is checked too, so the named v is exact, not merely lower.
    against = [F() for _ in p]
    for row in raw['security']['dual']:
        c = inst.counts(row['rivals'])
        for a in range(inst.topic_count):
            against[a] += F(row['probability']) * utility(a, inc(c, a))
    assert max(against) == v
    assert sum(F(row['probability']) for row in raw['security']['dual']) == 1
    HH = [F()]
    for i in range(1, 6):
        HH.append(HH[-1] + F(1, i))
    def phi(c):
        return sum((client.multiplicity * HH[sum(c[a] for a in client.topics)]
                    for client in inst.customers), F())
    pair_list = list(combinations_with_replacement(range(inst.topic_count), 2))
    envelope = {}
    def max_tail(q):
        if q not in envelope:
            values = [(phi(inc(inc(q, a), b)), (a, b)) for a, b in pair_list]
            envelope[q] = max(values)
        return envelope[q]
    solver = ExactSPESolver(inst)
    outcomes = solver.outcomes()
    worst = None
    pairs_checked = 0
    for c in sorted(outcomes):
        u = inst.topic_payoffs(c)
        # Each stored prefix has an actual root-compatible order witnessing it.
        reachable = {zero: ()}
        for depth in range(3):
            nxt = {}
            for q, history in reachable.items():
                threshold = solver.threshold(q)
                for a in range(inst.topic_count):
                    if q[a] >= c[a]:
                        continue
                    child = inc(q, a)
                    if c in solver.outcomes(child) and u[a] >= threshold:
                        nxt.setdefault(child, history + (a,))
            reachable = nxt
        for q, history in reachable.items():
            U = sum((q[a] * u[a] for a in range(inst.topic_count)), F())
            P, maximizing_pair = max_tail(q)
            gamma = P - phi(c)
            assert gamma >= 0
            gap = U + gamma - 3 * v
            candidate = (gap, c, q, history, U, gamma, maximizing_pair)
            if worst is None or candidate < worst:
                worst = candidate
            pairs_checked += 1
    assert worst is not None
    gap, c, q, history, U, gamma, maximizing_pair = worst
    # Complete the root-compatible ordered path using the same exact endpoint.
    full = history
    qq = q
    while len(full) < 5:
        chosen = [a for a in range(inst.topic_count) if qq[a] < c[a]
                  and c in solver.outcomes(inc(qq, a))
                  and solver._utility(c, a) >= solver.threshold(qq)]
        assert chosen
        a = min(chosen)
        full += (a,)
        qq = inc(qq, a)
    cert = solver.certificate(c, on_path=full)
    checked = verify_certificate(inst, cert)
    checked.assert_valid()
    report = {
        'scope': __doc__, 'instance': str(ip.relative_to(ROOT)),
        'instance_sha256': hashlib.sha256(ip.read_bytes()).hexdigest(),
        'security_source_sha256': hashlib.sha256(cp.read_bytes()).hexdigest(),
        'true_integer_security_v5': str(v), 'security_primary': list(map(str,p)),
        'security_background_multisets_checked': backgrounds,
        'security_dual_topic_upper_bounds': list(map(str,against)),
        'all_SPE_endpoints': len(outcomes), 'legal_endpoint_prefix_pairs': pairs_checked,
        'distinct_tail_envelope_prefixes': len(envelope), 'tail_comparison_pairs': len(pair_list),
        'minimum_ONE_GAP_residual': str(gap),
        'is_counterexample': gap < 0,
        'worst_path': list(full), 'worst_terminal_counts': list(c),
        'worst_first_three_counts': list(q), 'actual_u': list(map(str,inst.player_payoffs(full))),
        'U123': str(U), 'Gamma2': str(gamma), 'tail_potential_maximizing_pair': maximizing_pair,
        'checked_complete_strategy_histories': checked.checked_histories,
        'checked_complete_strategy_deviations': checked.checked_deviations,
    }
    if gap < 0:
        report['counterexample_instance'] = inst.to_dict()
        report['counterexample_strategy'] = cert.to_dict()
    Path(__file__).with_name('one_gap_named_exact.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report if gap >= 0 else {k:w for k,w in report.items() if k not in ('counterexample_instance','counterexample_strategy')}, indent=2))


if __name__ == '__main__':
    main()
