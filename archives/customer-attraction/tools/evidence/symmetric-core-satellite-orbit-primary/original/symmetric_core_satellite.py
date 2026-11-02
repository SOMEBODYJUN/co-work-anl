"""Exact all-SPE outcome quotient for symmetric disjoint satellite blocks.

Each satellite has an identical block: a customer is interested in that one
satellite and any chosen subset of k core topics. Additional customers may
like any nonempty subset of the cores. The solver takes an orbit of the
*set* of continuation outcomes, never a symmetric/Markov policy selector.
It is independently compared with the canonical unrestricted solver on
small instances. Large finite results are observations, not universal bounds.
"""
from __future__ import annotations
import argparse, json, math, random, sys, time
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'customer_attraction/__init__.py').is_file())
sys.path.insert(0, str(ROOT))
from customer_attraction import CustomerType, ExactSPESolver, Instance


class SymmetricSolver:
    def __init__(self, m, k, ell, satellite_weights, core_weights):
        self.m, self.k, self.ell = m, k, ell
        self.sw, self.cw = tuple(satellite_weights), tuple(core_weights)
        assert len(self.sw) == len(self.cw) == 1 << k
        assert self.cw[0] == 0
        self.L = math.lcm(*range(1, m + 1))
        self.cache, self.thresholds = {}, {}

    def instance(self):
        customers = [CustomerType(frozenset(a for a in range(self.k) if B & (1 << a)), w)
                     for B, w in enumerate(self.cw) if w]
        for j in range(self.ell):
            customers.extend(CustomerType(frozenset({self.k + j} | {a for a in range(self.k) if B & (1 << a)}), w)
                             for B, w in enumerate(self.sw) if w)
        return Instance(tuple(str(a) for a in range(self.k + self.ell)), tuple(customers), self.m)

    @lru_cache(None)
    def utilities(self, q):
        den = [sum(q[a] for a in range(self.k) if B & (1 << a)) for B in range(1 << self.k)]
        cores = []
        for a in range(self.k):
            value = sum(w * (self.L // den[B]) for B, w in enumerate(self.cw) if w and B & (1 << a) and den[B])
            value += sum(w * (self.L // (den[B] + v)) for v in q[self.k:]
                         for B, w in enumerate(self.sw) if w and B & (1 << a) and den[B] + v)
            cores.append(value)
        sats = [sum(w * (self.L // (den[B] + v)) for B, w in enumerate(self.sw) if w and den[B] + v)
                for v in q[self.k:]]
        return tuple(cores + sats)

    def welfare(self, q):
        den = [sum(q[a] for a in range(self.k) if B & (1 << a)) for B in range(1 << self.k)]
        return sum(w for B, w in enumerate(self.cw) if den[B]) + sum(w for v in q[self.k:]
                   for B, w in enumerate(self.sw) if den[B] + v)

    def canonical(self, state, terminal):
        result = list(terminal[:self.k])
        sats = state[self.k:]
        for v in sorted(set(sats)):
            result.extend(sorted(terminal[self.k + j] for j, c in enumerate(sats) if c == v))
        return tuple(result)

    def child_transitions(self, state, action):
        """All (parent outcome orbit, current mover payoff) pairs for an action.

        A moved satellite merges into its new occupancy class. A child orbit
        may assign it any of that class's final loads; all such assignments
        are needed. This is the critical distinction from count-policy tying.
        """
        k = self.k
        if action < k:
            child = state[:action] + (state[action] + 1,) + state[action + 1:]
            return [(q, self.utilities(q)[action]) for q in self.solve(child)]
        r = action - k  # satellite action indexed by its current load class
        sats = list(state[k:])
        sats.remove(r)
        sats.append(r + 1)
        sats.sort()
        child = state[:k] + tuple(sats)
        result = []
        for q in self.solve(child):
            groups = {v: [q[k + j] for j, c in enumerate(sats) if c == v] for v in set(sats)}
            for final_load in set(groups[r + 1]):
                parent_groups = {v: list(vals) for v, vals in groups.items()}
                parent_groups[r + 1].remove(final_load)
                parent_groups.setdefault(r, []).append(final_load)
                parent = list(q[:k])
                for v in sorted(set(state[k:])):
                    parent.extend(sorted(parent_groups[v]))
                den = [sum(q[a] for a in range(k) if B & (1 << a)) for B in range(1 << k)]
                value = sum(w * (self.L // (den[B] + final_load)) for B, w in enumerate(self.sw) if w)
                result.append((tuple(parent), value))
        return result

    def solve(self, state=None):
        state = (0,) * (self.k + self.ell) if state is None else state
        if state in self.cache:
            return self.cache[state]
        if sum(state) == self.m:
            result = frozenset({state})
        else:
            actions = list(range(self.k)) + [self.k + r for r in sorted(set(state[self.k:]))]
            branches = [self.child_transitions(state, a) for a in actions]
            floor = max(min(value for q, value in branch) for branch in branches)
            self.thresholds[state] = floor
            result = frozenset(q for branch in branches for q, value in branch if value >= floor)
        assert result
        self.cache[state] = result
        return result

    def price_portfolio(self, price):
        """Symmetric feasible portfolio; exact value, no numeric upper claim.

        Concavity of capped coverage permits averaging satellite z entries,
        hence this symmetry reduction also preserves the price optimum.
        """
        types = [(B, 0, w) for B, w in enumerate(self.cw) if w]
        types += [(B, 1, self.ell * w) for B, w in enumerate(self.sw) if w]
        p, n = self.k + 1, len(types)
        incidence = np.array([[int(bool(B & (1 << a))) for a in range(self.k)] + [sat]
                              for B, sat, w in types])
        matrix = np.hstack((-incidence, np.eye(n)))
        cost = [float(price)] * self.k + [self.ell * float(price)] + [-w for B, sat, w in types]
        result = linprog(cost, A_ub=matrix, b_ub=np.zeros(n), bounds=[(0, 1)] * (p + n), method='highs')
        assert result.success
        z = tuple(F(float(v)).limit_denominator(10**6) for v in result.x[:p])
        value = sum((w * min(F(1), sat * z[-1] + sum((z[a] for a in range(self.k) if B & (1 << a)), F()))
                     for B, sat, w in types), F())
        value -= price * (sum(z[:-1], F()) + self.ell * z[-1])
        return value, z


def self_test():
    rng = random.Random(24121)
    count = 0
    for m in (2, 3, 4):
        for k in (1, 2):
            for ell in (2, 3):
                for repetition in range(8):
                    sw = [rng.randrange(4) for B in range(1 << k)]
                    cw = [0] + [rng.randrange(4) for B in range(1, 1 << k)]
                    symmetry = SymmetricSolver(m, k, ell, sw, cw)
                    ordinary = ExactSPESolver(symmetry.instance())
                    for state in [(0,) * (k + ell), (1,) + (0,) * (k + ell - 1),
                                  (0,) * k + (0,) * (ell - 1) + (1,)]:
                        expected = {symmetry.canonical(state, q) for q in ordinary.outcomes(state)}
                        observed = set(symmetry.solve(state))
                        if expected != observed:
                            raise AssertionError((m, k, ell, sw, cw, state, expected, observed))
                        count += 1
    return {'comparisons': count, 'status': 'exact orbit sets equal canonical unrestricted outcome sets'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--self-test', action='store_true')
    ap.add_argument('--players', type=int, default=9)
    ap.add_argument('--cores', type=int, default=2)
    ap.add_argument('--satellites', type=int, default=9)
    ap.add_argument('--steps', type=int, default=30)
    ap.add_argument('--seed', type=int, default=202610218)
    ap.add_argument('--concentrated', action='store_true')
    args = ap.parse_args()
    if args.self_test:
        print(json.dumps(self_test()))
        return
    rng = random.Random(args.seed)
    best, best_price, records, start = F(0), F(0), [], time.monotonic()
    for step in range(args.steps):
        if args.concentrated:
            sw = [0] * (1 << args.cores)
            cw = [0] * (1 << args.cores)
            scale = 1 if step == 0 else rng.choice((1, 2, 5, 10))
            sw[0] = scale
            cw[1] = args.players * scale
            if step:
                for _ in range(rng.randint(1, 5)):
                    B = rng.randrange(1 << args.cores)
                    sw[B] += rng.randrange(1, 1 + scale)
                for _ in range(rng.randint(0, 4)):
                    B = rng.randrange(1, 1 << args.cores)
                    cw[B] += rng.randrange(1, 1 + args.players * scale)
        else:
            sw = [rng.randrange(0, 13) for B in range(1 << args.cores)]
            cw = [0] + [rng.randrange(0, 25) for B in range(1, 1 << args.cores)]
        solver = SymmetricSolver(args.players, args.cores, args.satellites, sw, cw)
        outcomes = solver.solve()
        worst = min(outcomes, key=solver.welfare)
        inst = solver.instance()
        optimum = inst.optimal_welfare()
        W = solver.welfare(worst)
        ratio = F(optimum, W) if W else F(1)
        min_price = min(F(v, solver.L) for a, v in enumerate(solver.utilities(worst)) if worst[a])
        price_candidates = []
        for q in outcomes:
            price = min(F(v, solver.L) for a, v in enumerate(solver.utilities(q)) if q[a])
            value, z = solver.price_portfolio(price)
            price_candidates.append((value / solver.welfare(q), q, price, z))
        price_score, price_q, price, z = max(price_candidates)
        best_price = max(best_price, price_score)
        records.append({'step': step, 'satellite_weights': sw, 'core_weights': cw,
                        'outcomes': len(outcomes), 'states': len(solver.cache), 'worst': worst,
                        'W': W, 'OPT': optimum, 'ratio': str(ratio), 'min_occupied_payoff': str(min_price),
                        'best_price_portfolio_over_W': str(price_score), 'price_counts': price_q,
                        'price': str(price), 'z_cores_and_common_satellite': [str(v) for v in z]})
        if ratio > best:
            best = ratio
            print(json.dumps(records[-1] | {'elapsed': round(time.monotonic() - start, 3)}), flush=True)
        report = {'scope': 'finite orbit-set all-SPE search in an explicitly restricted incidence class; no universal bound',
                  'parameters': vars(args), 'best_ratio': str(best), 'best_exact_price_lower_over_W': str(best_price),
                  'elapsed': round(time.monotonic() - start, 3),
                  'records': records}
        suffix = '_concentrated' if args.concentrated else ''
        (HERE / f'symmetric_m{args.players}_k{args.cores}_l{args.satellites}{suffix}.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'records'}), flush=True)


if __name__ == '__main__':
    main()
