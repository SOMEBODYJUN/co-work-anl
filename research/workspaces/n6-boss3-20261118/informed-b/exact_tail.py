"""Exact full-history six-player SPE sets for a specified finite catalogue.

Mathematical recurrence is independently checked in q5-prefix-reduction.md,
following the local lemma at independent/full-history-recursion.md section 1.
Only set-valued reachability is cached by action counts; desired child leaves
may differ at copies of the same state. All utility comparisons use integers.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path
import time

class Solver:
    def __init__(self, data):
        self.labels = data['labels']
        self.cov = [frozenset(x['clients']) for x in self.labels]
        self.n = data['clients']
        self.A = len(self.cov)
        self.members = [tuple(a for a, c in enumerate(self.cov) if x in c)
                        for x in range(self.n)]
        self.branches = {}

    def child(self, q, a):
        v = list(q); v[a] += 1
        return tuple(v)

    @lru_cache(None)
    def terminal(self, y):
        payoff = [0] * self.A
        welfare = 0
        for membership in self.members:
            load = sum(y[a] for a in membership)
            if load:
                welfare += 1
                for a in membership:
                    payoff[a] += 60 // load
        return tuple(payoff), welfare

    @lru_cache(None)
    def E(self, q):
        if sum(q) == 6:
            self.terminal(q)
            return frozenset((q,))
        kids = [self.E(self.child(q, a)) for a in range(self.A)]
        lows = [min(self.terminal(y)[0][a] for y in kid)
                for a, kid in enumerate(kids)]
        threshold = max(lows)
        feasible = frozenset(y for a, kid in enumerate(kids) for y in kid
                             if self.terminal(y)[0][a] >= threshold)
        assert feasible
        self.branches[q] = (threshold, tuple(lows))
        return feasible

    def current_worst(self, q):
        self.E(q)
        threshold, _ = self.branches[q]
        choices = [(self.terminal(y)[0][a], a, y)
                   for a in range(self.A) for y in self.E(self.child(q, a))
                   if self.terminal(y)[0][a] >= threshold]
        return min(choices)

    def policy_certificate(self, prefix, desired, forced_action=None):
        """Export all action continuations as a finite DAG of (counts, leaf).

        Every node still has a child for every original label. Different ordered
        histories may enter distinct nodes carrying the same counts but different
        desired leaves, so this is not a restriction to count-based strategies.
        """
        nodes = []
        index = {}
        def visit(q, y, specified=None):
            key = (q, y, specified)
            if key in index:
                return index[key]
            node_id = len(nodes); index[key] = node_id
            node = {'counts': list(q), 'terminal': list(y)}
            nodes.append(node)
            if sum(q) == 6:
                assert q == y
                node['action'] = None; node['children'] = []
                return node_id
            threshold, _ = self.branches[q]
            actions = [a for a in range(self.A)
                       if y in self.E(self.child(q, a)) and
                       self.terminal(y)[0][a] >= threshold]
            a = specified if specified is not None else min(actions)
            assert a in actions
            node['action'] = a
            node['children'] = []
            for b in range(self.A):
                qb = self.child(q, b)
                z = y if b == a else min(self.E(qb),
                    key=lambda z: (self.terminal(z)[0][b], z))
                node['children'].append(visit(qb, z))
            return node_id
        root = visit(prefix, desired, forced_action)
        return {'root': root, 'nodes': nodes}


def verify_policy(data, cert):
    """Check complete exported DAG directly without using set recurrence."""
    sol = Solver(data)
    nodes = cert['nodes']
    visited = set()
    def check(i):
        if i in visited:
            return
        node = nodes[i]; q = tuple(node['counts']); y = tuple(node['terminal'])
        assert sum(y) == 6 and all(y[a] >= q[a] for a in range(sol.A))
        if sum(q) == 6:
            assert y == q and node['action'] is None and not node['children']
        else:
            a = node['action']; kids = node['children']
            assert len(kids) == sol.A and 0 <= a < sol.A
            assert tuple(nodes[kids[a]]['terminal']) == y
            own = sol.terminal(y)[0][a]
            for b, child in enumerate(kids):
                assert tuple(nodes[child]['counts']) == sol.child(q, b)
                check(child)
                assert own >= sol.terminal(tuple(nodes[child]['terminal']))[0][b]
        visited.add(i)
    check(cert['root'])
    assert len(visited) == len(nodes)
    return len(visited)


def run(data, do_root, certificate_path):
    started = time.perf_counter()
    sol = Solver(data)
    prefix = tuple(data['prefix_counts'])
    outcomes = sol.E(prefix)
    payoff, action, leaf = sol.current_worst(prefix)
    threshold, lows = sol.branches[prefix]
    result = {
        'scope': 'Specified finite original catalogue; all complete pure-SPE continuations at the specified ordered prefix; arbitrary ties.',
        'scale': 60, 'K': data['K'], 'OPT6': 6*data['K'],
        'prefix_labels': data['prefix_labels'],
        'prefix_counts': list(prefix),
        'prefix_outcome_count': len(outcomes),
        'minimum_current_payoff_times_60': payoff,
        'half_K_times_60': 30*data['K'],
        'current_threshold_times_60': threshold,
        'child_min_payoffs_times_60': list(lows),
        'min_current_action': sol.labels[action]['name'],
        'min_current_terminal_counts': list(leaf),
        'min_current_terminal_welfare': sol.terminal(leaf)[1],
        'prefix_min_terminal_welfare': min(sol.terminal(y)[1] for y in outcomes),
        'prefix_max_terminal_welfare': max(sol.terminal(y)[1] for y in outcomes),
    }
    cert = sol.policy_certificate(prefix, leaf, action)
    result['complete_subgame_policy_nodes'] = verify_policy(data, cert)
    Path(certificate_path).write_text(json.dumps({'input': data, 'policy': cert}, separators=(',', ':'))+'\n')
    if do_root:
        zero = (0,)*sol.A
        roots = sol.E(zero)
        worst = min(roots, key=lambda y: (sol.terminal(y)[1], y))
        result['root_outcome_count'] = len(roots)
        result['root_min_welfare'] = sol.terminal(worst)[1]
        result['root_worst_terminal_counts'] = list(worst)
        result['root_half_inequality_gap'] = 2*result['root_min_welfare']-6*data['K']
    result['count_states_evaluated'] = sol.E.cache_info().currsize
    result['terminal_profiles_evaluated'] = sol.terminal.cache_info().currsize
    result['elapsed_seconds'] = round(time.perf_counter()-started, 6)
    return result

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('input'); p.add_argument('--root', action='store_true')
    p.add_argument('--certificate', required=True)
    args = p.parse_args()
    data = json.loads(Path(args.input).read_text())
    print(json.dumps(run(data, args.root, args.certificate), indent=2))
