"""Exact checks of four fixed historical games; no random search or optimizer.

Use --original-dir for the nine frozen source files and --out for a new report.
All ordered-history policies are checked, including every off-path action.
The outcome-set recursion caches count states, not a common Markov policy.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import comb
from pathlib import Path


def counts(history, k):
    return tuple(history.count(a) for a in range(k))


def compositions(total, length):
    if length == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for tail in compositions(total - first, length - 1):
                yield (first,) + tail


class Game:
    def __init__(self, instance, players=None):
        self.k = len(instance['topics'])
        self.m = instance['players'] if players is None else players
        self.cells = tuple((tuple(c['topics']), c['multiplicity']) for c in instance['customers'])
        assert self.k > 0 and self.m > 0
        assert all(isinstance(w, int) and w > 0 and len(set(t)) == len(t)
                   and all(0 <= a < self.k for a in t) for t, w in self.cells)
        self.total = sum(w for _, w in self.cells)
        # Distinct column signatures show these fixed examples use a set catalog.
        self.signatures = [tuple(i for i, (t, _) in enumerate(self.cells) if a in t)
                           for a in range(self.k)]
        assert len(set(self.signatures)) == self.k

    @lru_cache(None)
    def welfare(self, q):
        return sum(w for t, w in self.cells if sum(q[a] for a in t) > 0)

    @lru_cache(None)
    def payoff(self, a, q):
        assert q[a] > 0
        return sum((F(w, sum(q[b] for b in t)) for t, w in self.cells if a in t), F(0))

    def policy(self, certificate):
        actions = certificate['actions']
        assert all(set(x) == {'history', 'action'} for x in actions)
        sigma = {tuple(x['history']): x['action'] for x in actions}
        expected = {h for depth in range(self.m) for h in product(range(self.k), repeat=depth)}
        assert len(sigma) == len(actions) and set(sigma) == expected
        assert all(a in range(self.k) for a in sigma.values())

        @lru_cache(None)
        def terminal(h):
            if len(h) == self.m:
                return h
            return terminal(h + (sigma[h],))

        rows = []
        comparisons = zeros = 0
        for h in sorted(sigma, key=lambda x: (len(x), x)):
            a = sigma[h]
            q = counts(terminal(h), self.k)
            u = self.payoff(a, q)
            alternatives = []
            for b in range(self.k):
                qb = counts(terminal(h + (b,)), self.k)
                v = self.payoff(b, qb)
                slack = u - v
                assert slack >= 0, (h, a, b, slack)
                comparisons += 1
                zeros += slack == 0
                alternatives.append({'action': b, 'terminal_counts': qb,
                                     'payoff': str(v), 'slack': str(slack)})
            rows.append({'history': h, 'action': a, 'payoff': str(u),
                         'alternatives': alternatives})
        actual = terminal(())
        q = counts(actual, self.k)
        assert list(q) == certificate['terminal_counts']
        return {'histories': len(expected), 'comparisons_including_prescribed': comparisons,
                'zero_comparisons_including_prescribed': zeros, 'negative_comparisons': 0,
                'actual_history': actual, 'terminal_counts': q,
                'welfare': self.welfare(q),
                'player_payoffs': [str(self.payoff(a, q)) for a in actual],
                'all_history_checks': rows}

    def equilibria(self):
        terminals = list(compositions(self.m, self.k))
        assert len(terminals) == comb(self.m + self.k - 1, self.k - 1)
        pnes = []
        failures = []
        for q in terminals:
            witness = None
            for a in range(self.k):
                if not q[a]:
                    continue
                for b in range(self.k):
                    if a == b:
                        continue
                    z = list(q)
                    z[a] -= 1
                    z[b] += 1
                    gain = self.payoff(b, tuple(z)) - self.payoff(a, q)
                    if gain > 0:
                        witness = {'counts': q, 'from': a, 'to': b, 'gain': str(gain)}
                        break
                if witness:
                    break
            if witness:
                failures.append(witness)
            else:
                pnes.append(q)
        assert pnes
        states = {}

        @lru_cache(None)
        def outcomes(n):
            if sum(n) == self.m:
                ans = frozenset([n])
            else:
                children = []
                for a in range(self.k):
                    z = list(n)
                    z[a] += 1
                    children.append(outcomes(tuple(z)))
                threshold = max(min(self.payoff(a, q) for q in child)
                                for a, child in enumerate(children))
                ans = frozenset(q for a, child in enumerate(children) for q in child
                                if self.payoff(a, q) >= threshold)
            assert ans
            states[n] = sorted(ans)
            return ans

        root = sorted(outcomes((0,) * self.k))
        assert len(states) == comb(self.m + self.k, self.k)
        spe_min = min(map(self.welfare, root))
        return {'players': self.m, 'unit_customers': self.total,
                'terminal_count_vectors': len(terminals), 'count_states': len(states),
                'optimal_welfare': max(map(self.welfare, terminals)),
                'pne_counts': pnes, 'pne_welfares': [self.welfare(q) for q in pnes],
                'worst_pne': min(map(self.welfare, pnes)),
                'non_pne_first_strict_deviation': failures,
                'root_spe_outcomes': root, 'root_spe_welfares': [self.welfare(q) for q in root],
                'worst_spe': spe_min,
                'worst_spe_counts': [q for q in root if self.welfare(q) == spe_min],
                'all_count_state_outcome_sets': [{'prefix_counts': n, 'outcomes': states[n]}
                                               for n in sorted(states, key=lambda x: (sum(x), x))]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--original-dir', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    root = args.original_dir
    manifest = []
    for p in sorted(root.iterdir()):
        if p.is_file():
            raw = p.read_bytes()
            manifest.append({'name': p.name, 'size': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
    assert len(manifest) == 9
    result = {'method': 'definition-level Fraction; fixed inputs only; no canonical solver import',
              'source_files': manifest, 'bridges': {}}
    for name in ['last_reply_bridge_counterexample.json', 'last_reply_bridge_four_topics.json']:
        d = json.loads((root / name).read_text())
        g = Game(d['instance'])
        p = g.policy(d['certificate'])
        q = tuple(p['terminal_counts'])
        last = p['actual_history'][-1]
        u = g.payoff(last, q)
        D = sum((F(w, sum(q[a] for a in t) + 1) for t, w in g.cells
                 if last not in t and sum(q[a] for a in t) > 0), F(0))
        W = g.welfare(q)
        opt = max(g.welfare(z) for z in compositions(g.m, g.k))
        result['bridges'][name] = {'policy': p, 'optimal_welfare': opt, 'last_payoff': str(u),
                                  'D': str(D), 'tau': str(W-u-D),
                                  'false_bridge_left': str((g.m-1)*u),
                                  'false_bridge_right': str(W+D),
                                  'false_bridge_excess': str((g.m-1)*u-W-D),
                                  'valid_last_reply_upper': str(W+(g.m-1)*u-D)}
        assert (g.m-1)*u-W-D == F(1, 4)
    sparse = json.loads((root/'static_dominance_sparse_result.json').read_text())
    minimized = json.loads((root/'static_dominance_minimized.json').read_text())
    certificate = json.loads((root/'static_dominance_certificate.json').read_text())
    g = Game(minimized['instance'])
    result['minimized_policy'] = g.policy(certificate)
    result['minimized_equilibria'] = g.equilibria()
    result['sparse_equilibria'] = Game(sparse['instance']).equilibria()
    for saved, key in [(minimized, 'minimized_equilibria'), (sparse, 'sparse_equilibria')]:
        checked = result[key]
        assert saved['worst_spe'] == checked['worst_spe']
        assert saved['worst_pne'] == checked['worst_pne']
        assert sorted(map(tuple, saved['pne_counts'])) == checked['pne_counts']
        wanted = saved['worst_spe_counts']
        if wanted and isinstance(wanted[0], int):
            wanted = [wanted]
        assert sorted(map(tuple, wanted)) == checked['worst_spe_counts']
    assert minimized['spe_count'] == len(result['minimized_equilibria']['root_spe_outcomes'])
    assert minimized['opt'] == result['minimized_equilibria']['optimal_welfare']
    result['same_55_customer_instance_other_player_counts'] = {}
    for m, expected in [(2, 46), (3, 46), (4, 50), (6, 55)]:
        row = Game(minimized['instance'], players=m).equilibria()
        assert row['worst_spe'] == row['worst_pne'] == expected
        result['same_55_customer_instance_other_player_counts'][m] = row
    result['execution_scope'] = {'successful_fixed_entry_invocations': 1,
                                 'policy_checks': 3, 'equilibrium_fixed_games': 6,
                                 'random_search_runs': 0, 'greedy_minimization_runs': 0,
                                 'original_program_runs': 0, 'optimizer_runs': 0,
                                 'canonical_solver_imports': 0}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'status': 'all_fixed_checks_passed',
                      'policy_histories': [15, 85, 781],
                      'minimized_outcomes': result['minimized_equilibria']['root_spe_outcomes'],
                      'sparse_outcomes': result['sparse_equilibria']['root_spe_outcomes'],
                      'output': str(args.out)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
