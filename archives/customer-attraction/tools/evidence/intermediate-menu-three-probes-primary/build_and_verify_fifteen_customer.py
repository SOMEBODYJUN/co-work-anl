"""Independent full ordered-history construction and client-definition audit.

No import from any original probe, canonical solver, or optimization package.
The tagged outcome recursion is independently implemented with an explicit
one-player base case, then expanded separately at each ordered history.
"""
from pathlib import Path
from fractions import Fraction
from functools import lru_cache
from itertools import product
import argparse
import hashlib
import json
import platform
import time

HERE = Path(__file__).resolve().parent
ORIGINAL = HERE / 'original/research/workspaces/customer-attraction/R-a5cc2a7008c548ec9b48d8386b872229/intermediate_menus/last_menu_separation.json'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-json', type=Path, default=ORIGINAL)
    parser.add_argument('--output-dir', type=Path, default=HERE / 'independent-complete-strategy')
    args = parser.parse_args()
    start = time.perf_counter()
    data = json.loads(args.source_json.read_text())
    p, m = data['n'], data['m']
    assert (p, m, data['weights']) == (3, 5, [[1, 6], [2, 3], [3, 6]])
    # Each entry is one distinct unit customer, not one weighted customer.
    customers = [frozenset(a for a in range(p) if mask >> a & 1)
                 for mask, multiplicity in data['weights']
                 for _ in range(multiplicity)]
    assert len(customers) == 15

    def counts(history):
        return tuple(history.count(a) for a in range(p))

    def add(q, a):
        return tuple(q[b] + (b == a) for b in range(p))

    def type_pay(q, action):
        return sum((Fraction(multiplicity, sum(q[a] for a in range(p) if mask >> a & 1))
                    for mask, multiplicity in data['weights'] if mask >> action & 1), Fraction())

    @lru_cache(None)
    def tagged(q):
        remaining = m - sum(q)
        assert remaining >= 1
        if remaining == 1:
            candidates = [(add(q, action), action) for action in range(p)]
            best = max(type_pay(z, action) for z, action in candidates)
            return frozenset((z, action) for z, action in candidates
                             if type_pay(z, action) == best)
        child = [tagged(add(q, action)) for action in range(p)]
        threshold = max(min(type_pay(z, action) for z, last in child[action])
                        for action in range(p))
        return frozenset(target for action in range(p) for target in child[action]
                         if type_pay(target[0], action) >= threshold)

    policy = {}

    def build(history, target):
        q = counts(history)
        assert target in tagged(q)
        if len(history) == m - 1:
            action = target[1]
            assert add(q, action) == target[0]
            policy[history] = action
            return
        child = [tagged(add(q, action)) for action in range(p)]
        threshold = max(min(type_pay(z, action) for z, last in child[action])
                        for action in range(p))
        eligible = [action for action in range(p)
                    if target in child[action] and type_pay(target[0], action) >= threshold]
        action = min(eligible)
        policy[history] = action
        for alternative in range(p):
            next_target = target if alternative == action else min(
                child[alternative], key=lambda item: (type_pay(item[0], alternative), item))
            build(history + (alternative,), next_target)

    targets = [(tuple(row[2]), row[3]) for row in data['menu']]
    root_payoffs = []
    for action in range(p):
        assert targets[action] in tagged(add((0,) * p, action))
        build((action,), targets[action])
        root_payoffs.append(type_pay(targets[action][0], action))
    policy[()] = max(range(p), key=lambda action: (root_payoffs[action], -action))
    histories = [history for depth in range(m) for history in product(range(p), repeat=depth)]
    assert set(policy) == set(histories)
    assert len(histories) == 121

    # The verifier below uses literal completed ordered paths and unit clients.
    # It does not consult tagged(), type_pay(), or any construction threshold.
    def complete(prefix):
        history = tuple(prefix)
        while len(history) < m:
            history += (policy[history],)
        return history

    def client_pay(history, player):
        action = history[player]
        return sum((Fraction(1, sum(chosen in customer for chosen in history))
                    for customer in customers if action in customer), Fraction())

    def insertion(history, theme):
        return sum((Fraction(1, 1 + sum(chosen in customer for chosen in history))
                    for customer in customers if theme in customer), Fraction())

    def welfare(history):
        return sum(any(action in customer for action in history) for customer in customers)

    checks = []
    for history in histories:
        chosen = policy[history]
        prescribed = complete(history)
        own = client_pay(prescribed, len(history))
        for alternative in range(p):
            deviated = complete(history + (alternative,))
            other = client_pay(deviated, len(history))
            assert own >= other
            checks.append({'history': list(history), 'chosen': chosen,
                           'alternative': alternative, 'prescribed_path': list(prescribed),
                           'deviation_path': list(deviated), 'own': str(own),
                           'deviation': str(other), 'slack': str(own - other)})
    assert len(checks) == 363
    branches = []
    for action in range(p):
        history = complete((action,))
        d, last, z, last_action = data['menu'][action]
        assert counts(history) == tuple(z) and history[-1] == last_action
        assert client_pay(history, 0) == Fraction(d)
        assert client_pay(history, m - 1) == Fraction(last)
        branches.append({'forced_root': action, 'history': list(history), 'counts': list(counts(history)),
                         'root_profit': str(client_pay(history, 0)),
                         'last_profit': str(client_pay(history, m - 1)),
                         'insertion_by_theme': [str(insertion(history, a)) for a in range(p)],
                         'insertion_cap': str(max(insertion(history, a) for a in range(p))),
                         'welfare': welfare(history)})
    actual = complete(())
    u = client_pay(actual, 0)
    assert u == Fraction(data['u']) == max(root_payoffs)
    assert all(Fraction(b['last_profit']) > u for b in branches)
    optimum = max(welfare(history) for history in product(range(p), repeat=m))
    strict = sum(Fraction(check['slack']) > 0 for check in checks)
    report = {'model': '15 distinct unit clients; 3 common labels including empty label2; 5 unit providers; full ordered-history pure SPE',
              'source_json_sha256': hashlib.sha256(args.source_json.read_bytes()).hexdigest(),
              'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'python': platform.python_version(), 'assertions_enabled': __debug__,
              'elapsed_seconds': time.perf_counter() - start,
              'unit_customer_interests': [sorted(customer) for customer in customers],
              'policy': [{'history': list(history), 'action': policy[history]} for history in histories],
              'ordered_decision_nodes': len(histories), 'comparisons_including_self': len(checks),
              'self_comparisons': len(histories), 'proper_deviations': len(checks) - len(histories),
              'strict_comparisons': strict, 'zero_comparisons': len(checks) - strict,
              'all_IC': checks, 'root_branches': branches, 'actual_history': list(actual),
              'actual_utilities': [str(client_pay(actual, player)) for player in range(m)],
              'actual_welfare': welfare(actual), 'OPT5': optimum,
              'half_surplus': 2 * welfare(actual) - optimum,
              'root_profit': str(u), 'min_last_profit': str(min(Fraction(b['last_profit']) for b in branches)),
              'last_minus_root_minimum': str(min(Fraction(b['last_profit']) for b in branches) - u),
              'tagged_state_cache': tagged.cache_info()._asdict(),
              'original_probe_imports': 0, 'canonical_solver_imports': 0, 'LP_calls': 0,
              'scope': 'Certifies this single constructed full strategy and the stated last-profit separation, not every SPE or a half counterexample.'}
    args.output_dir.mkdir(parents=True, exist_ok=False)
    (args.output_dir / 'certificate-and-all-IC.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    summary = {k: report[k] for k in ['ordered_decision_nodes', 'comparisons_including_self', 'proper_deviations',
                                     'strict_comparisons', 'zero_comparisons', 'actual_history', 'actual_utilities',
                                     'actual_welfare', 'OPT5', 'half_surplus', 'root_profit', 'min_last_profit',
                                     'last_minus_root_minimum', 'root_branches', 'elapsed_seconds']}
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
