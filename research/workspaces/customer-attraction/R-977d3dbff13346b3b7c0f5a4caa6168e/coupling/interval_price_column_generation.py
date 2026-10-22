"""Terminal-labelled DAG pricing for the HI root-floor path LP.

Numerical column generation proposes prices and mixtures. Every reported lower
bound is recomputed by an exact Fraction shortest path over every terminal.
It never substitutes unlabelled edge-flow marginals for terminal correlation.
"""
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import argparse
import json
import sys
import time

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4]))
sys.path.insert(0, str(HERE.parent/'background'))
from customer_attraction import CustomerType, Instance
from interval_ceiling_dp import IntervalCeilingFloor


def compositions(total, p):
    if p == 1:
        yield (total,)
    else:
        for x in range(total+1):
            for tail in compositions(total-x, p-1):
                yield (x,)+tail


class Pricing:
    def __init__(self, ins):
        self.ins, self.p, self.m = ins, ins.topic_count, ins.players
        self.zero = (0,)*self.p
        self.hi = IntervalCeilingFloor(ins)
        self.hi.bounds(self.zero)
        self.reachable = {self.zero}
        for depth in range(self.m):
            for b in sorted(b for b in self.reachable if sum(b) == depth):
                for a in self.hi.allowed[b]:
                    self.reachable.add(self.hi.add(b, a))
        self.terminals = sorted((q for q in self.reachable if sum(q) == self.m),
                                key=lambda q: (ins.welfare(q), q))
        self.edges = sorted((b, a) for b in self.reachable if sum(b) < self.m
                            for a in self.hi.allowed[b])
        self.ei = {e: i for i, e in enumerate(self.edges)}
        self.floor_float = {b: float(self.hi.level[b]) for b in self.reachable if sum(b) < self.m}
        self.utility = {q: self.hi.pay(q) for q in self.terminals}
        self.utility_float = {q: tuple(map(float, self.utility[q])) for q in self.terminals}
        self.W = {q: ins.welfare(q) for q in self.terminals}

    def path(self, actions):
        b, es = self.zero, []
        for a in actions:
            assert a in self.hi.allowed[b]
            es.append((b, a)); b = self.hi.add(b, a)
        return b, tuple(es)

    def margin(self, actions):
        q, es = self.path(actions)
        return [(self.ei[(b, a)], self.utility[q][a]-self.hi.level[b]) for b, a in es]

    def pure_SPE_seed(self):
        """One complete Markov backward-induction selector; no equilibrium set pruning."""
        terminal, actions = {}, {}
        for depth in range(self.m, -1, -1):
            for b in compositions(depth, self.p):
                if depth == self.m:
                    terminal[b] = b
                    continue
                choices = [(self.hi.pay(terminal[self.hi.add(b, a)])[a], a,
                            terminal[self.hi.add(b, a)]) for a in range(self.p)]
                _, a, q = max(choices, key=lambda x: (x[0], -x[1]))
                actions[b], terminal[b] = a, q
        b, path = self.zero, []
        for _ in range(self.m):
            a = actions[b]; path.append(a); b = self.hi.add(b, a)
        assert all(value >= 0 for _, value in self.margin(tuple(path)))
        return tuple(path)

    def separate(self, lambdas, *, exact=False):
        """Return global min F_lambda and an attaining allowed ordered path."""
        infinity = None if exact else float('inf')
        best, best_path, visited = infinity, None, 0
        zero = F() if exact else 0.0
        for q in self.terminals:
            uq = self.utility[q] if exact else self.utility_float[q]
            chosen = {}
            @lru_cache(None)
            def shortest(b):
                if b == q:
                    return zero
                value, selected = infinity, None
                for a in self.hi.allowed[b]:
                    if b[a] >= q[a]:
                        continue
                    tail = shortest(self.hi.add(b, a))
                    if tail is None or (not exact and tail == float('inf')):
                        continue
                    lam = lambdas[self.ei[(b, a)]]
                    floor = self.hi.level[b] if exact else self.floor_float[b]
                    candidate = tail+lam*(floor-uq[a])
                    if value is None or candidate < value:
                        value, selected = candidate, a
                if selected is not None:
                    chosen[b] = selected
                return value
            val = shortest(self.zero)
            visited += shortest.cache_info().currsize
            if val is None or (not exact and val == float('inf')):
                continue
            val += self.W[q]
            if best is None or val < best:
                best = val
                b, path = self.zero, []
                while b != q:
                    a = chosen[b]; path.append(a); b = self.hi.add(b, a)
                best_path = tuple(path)
        assert best_path is not None
        return best, best_path, visited


def generate(ins, iterations):
    started = time.time()
    pricing = Pricing(ins)
    columns = [pricing.pure_SPE_seed()]
    minimum_W, low_path, _ = pricing.separate([0.0]*len(pricing.edges))
    if low_path not in columns:
        columns.append(low_path)
    log = []
    result, prices = None, None
    for iteration in range(iterations):
        ri, ci, va, costs = [], [], [], []
        for j, path in enumerate(columns):
            q, _ = pricing.path(path)
            costs.append(pricing.W[q])
            for e, margin in pricing.margin(path):
                if margin:
                    ri.append(e); ci.append(j); va.append(-float(margin))
        matrix = coo_matrix((va, (ri, ci)), shape=(len(pricing.edges), len(columns))).tocsc()
        result = linprog(np.array(costs, dtype=float), A_ub=matrix,
                         b_ub=np.zeros(len(pricing.edges)),
                         A_eq=np.ones((1, len(columns))), b_eq=[1],
                         bounds=(0, None), method='highs')
        assert result.success, result.message
        prices = np.maximum(0.0, -result.ineqlin.marginals)
        lower, path, states = pricing.separate(prices)
        gap = result.fun-lower
        log.append({'iteration': iteration, 'columns': len(columns),
                    'restricted_primal_value': float(result.fun),
                    'DAG_lower_value': float(lower), 'gap': float(gap),
                    'terminal_state_pairs_visited': states})
        print(json.dumps(log[-1]), flush=True)
        if gap < 1e-7 or path in columns:
            break
        columns.append(path)
    assert result is not None
    exact_prices = [F(float(x)).limit_denominator(10**8) for x in prices]
    exact_lower, worst, exact_states = pricing.separate(exact_prices, exact=True)
    weights = [F(float(x)).limit_denominator(10**8) for x in result.x]
    margins = {e: F() for e in range(len(pricing.edges))}
    for path, weight in zip(columns[:len(weights)], weights):
        for e, value in pricing.margin(path):
            margins[e] += weight*value
    primal_ok = sum(weights) == 1 and all(x >= 0 for x in weights) and all(x >= 0 for x in margins.values())
    exact_upper = sum((weight*pricing.W[pricing.path(path)[0]]
                       for path, weight in zip(columns[:len(weights)], weights)), F()) if primal_ok else None
    return {'instance': ins.to_dict(), 'scope': 'one fixed instance, count-state action prices',
            'not_a_general_half_theorem': True, 'G_I': str(pricing.hi.root()),
            'OPT': ins.optimal_welfare(), 'minimum_HI_terminal_W': str(int(minimum_W)),
            'HI_terminals': len(pricing.terminals), 'reachable_edges': len(pricing.edges),
            'exact_DAG_lower_bound': str(exact_lower), 'worst_priced_path': worst,
            'exact_terminal_state_pairs_visited': exact_states,
            'exact_primal': primal_ok, 'exact_primal_upper_bound': str(exact_upper) if primal_ok else None,
            'exact_optimality': primal_ok and exact_upper == exact_lower,
            'dual_nonzero': [{'b': b, 'a': a, 'lambda': str(lam)}
                             for (b, a), lam in zip(pricing.edges, exact_prices) if lam],
            'primal_nonzero': [{'actions': path, 'weight': str(weight)}
                               for path, weight in zip(columns[:len(weights)], weights) if weight],
            'log': log, 'elapsed_seconds': time.time()-started}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default=str(HERE/'interval_price_strict_candidate.json'))
    parser.add_argument('--iterations', type=int, default=100)
    parser.add_argument('--output', default='interval_price_column_generation.json')
    args = parser.parse_args()
    raw = json.loads(Path(args.input).read_text())
    if 'instance' in raw and 'topics' in raw['instance']:
        ins = Instance.from_dict(raw['instance'])
    else:
        p, m = raw['q'], raw['m']
        ins = Instance(tuple(map(str, range(p))),
                       tuple(CustomerType(frozenset(a for a in range(p) if mask >> a & 1), weight)
                             for mask, weight in raw['rows']), m)
    out = generate(ins, args.iterations)
    (HERE/args.output).write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k: v for k, v in out.items() if k not in
                      ('instance', 'dual_nonzero', 'primal_nonzero', 'log')}, indent=2))


if __name__ == '__main__':
    main()
