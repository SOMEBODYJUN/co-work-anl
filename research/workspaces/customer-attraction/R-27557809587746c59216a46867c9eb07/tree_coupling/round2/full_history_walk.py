"""Full-history moment-cone walk for the stronger submodular half question.

No moment vector is asserted to have nonnegative customer realization.
The canonical set-valued SPE recursion is reused with an explicit precomputed
abstract Shapley payoff table; the empty Instance supplies only count/history
validation. Every constructed policy and accepted LP vector is also checked
at every ordered history using Fraction. This searches adjacent strategy
cones, not just fixed Markov policies or budget-additive inputs.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product, combinations
from pathlib import Path
import argparse
import hashlib
import json
import random
import sys
import time
import numpy as np
from scipy.optimize import linprog

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction import Instance, ExactSPESolver


def counts(total, p):
    if p == 1:
        yield (total,)
    else:
        for x in range(total+1):
            for r in counts(total-x, p-1):
                yield (x,)+r


def subs(mask):
    r = mask
    while True:
        yield r
        if not r:
            return
        r = (r-1) & mask


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), F(0))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--players', type=int, default=5)
    ap.add_argument('--topics', type=int, default=7)
    ap.add_argument('--rounds', type=int, default=60)
    ap.add_argument('--seed', type=int, default=9201773)
    ap.add_argument('--output', default='full_history_walk.json')
    ap.add_argument('--restart-every', type=int, default=10)
    ap.add_argument('--continuations', choices=['minimal', 'nearest', 'highest'], default='nearest')
    ap.add_argument('--global-submodular', action='store_true')
    ap.add_argument('--root-selection', choices=['fewest', 'most', 'random'], default='fewest')
    args = ap.parse_args()
    n, p = args.players, args.topics
    moment_order = p if args.global_submodular else n
    masks = [s for s in range(1, 1 << p) if s.bit_count() <= moment_order]
    mi = {s: i for i, s in enumerate(masks)}
    d = len(masks)
    units = {s: tuple(F(i == mi[s]) for i in range(d)) for s in masks}
    units[0] = (F(0),)*d
    def sub(a, b):
        return tuple(x-y for x, y in zip(a, b))
    @lru_cache(None)
    def payoff(q, a):
        support = sum(1 << b for b in range(p) if q[b])
        def f(typ):
            return F(1, sum(q[b] for b in range(p) if typ >> b & 1)) if typ >> a & 1 else F(0)
        row = [F(0)]*d
        for s in subs(support):
            if s:
                row[mi[s]] = -sum(((-1)**(s.bit_count()-v.bit_count())*f(support & ~v) for v in subs(s)), F(0))
        return tuple(row)
    terminals = list(counts(n, p))
    supports = {q: sum(1 << a for a in range(p) if q[a]) for q in terminals}
    sparse = {(q, a): [(i, v) for i, v in enumerate(payoff(q, a)) if v]
              for q in terminals for a in range(p) if q[a]}
    base = []
    for s in [0]+masks:
        if s.bit_count() < moment_order:
            for a in range(p):
                if not s >> a & 1:
                    base.append(sub(units[s | (1 << a)], units[s]))
        if s.bit_count() <= moment_order-2:
            for a in range(p):
                if s >> a & 1:
                    continue
                for b in range(a+1, p):
                    if not s >> b & 1:
                        base.append(tuple(x+y-z-w for x, y, z, w in zip(units[s | (1 << a)], units[s | (1 << b)], units[s], units[s | (1 << a) | (1 << b)])))
    rng = random.Random(args.seed)
    targets = [sum(1 << a for a in chosen) for chosen in combinations(range(p), min(n, p))]
    template = Instance(tuple('T'+str(a) for a in range(p)), (), n)
    best = F(0)
    best_witness = None
    history = []
    seen_cones = set()
    c = None
    started = time.time()
    for step in range(args.rounds):
        if c is None or step % args.restart_every == 0:
            terms = []
            for _ in range(rng.randint(2, 12)):
                weights = [rng.choice([0, 0, 1, 2, 3, 5, 8]) for _ in range(p)]
                terms.append((weights, rng.randint(1, max(1, sum(weights)))))
            c = tuple(F(sum(min(cap, sum(w[a] for a in range(p) if s >> a & 1)) for w, cap in terms)) for s in masks)
            if step % (4*args.restart_every) == 0:
                c = tuple(F(n*bool(s & 1)+(s & ~1).bit_count()) for s in masks)
            if not any(c):
                continue
        assert all(dot(row, c) >= 0 for row in base)
        solver = ExactSPESolver(template)
        table = {q: tuple(sum((v*c[i] for i, v in sparse[(q, a)]), F(0)) if q[a] else F(0)
                          for a in range(p)) for q in terminals}
        solver._payoffs.update(table)
        outcomes = solver.outcomes()
        minimum = min(c[mi[supports[q]]] for q in outcomes)
        worst = [q for q in sorted(outcomes) if c[mi[supports[q]]] == minimum]
        if args.root_selection == 'fewest':
            root_target = min(worst, key=lambda q: (supports[q].bit_count(), q))
        elif args.root_selection == 'most':
            root_target = max(worst, key=lambda q: (supports[q].bit_count(), q))
        else:
            root_target = rng.choice(worst)
        if args.continuations == 'minimal':
            cert = solver.certificate(root_target)
            actions = dict(cert.actions)
        else:
            # Every offpath child may use ANY credible SPE terminal whose
            # deviator payoff is <= the chosen current payoff. This is wider
            # than the canonical certificate's minimum-payoff submenus.
            actions = {}
            def expand(h, prefix, desired):
                if len(h) == n:
                    assert prefix == desired
                    return
                floor = solver.threshold(prefix)
                admissible = [a for a in range(p)
                              if desired in solver.outcomes(tuple(prefix[b]+(a == b) for b in range(p)))
                              and table[desired][a] >= floor]
                a = min(admissible)
                actions[h] = a
                current = table[desired][a]
                for b in range(p):
                    child = tuple(prefix[t]+(b == t) for t in range(p))
                    if b == a:
                        target_child = desired
                    else:
                        allowed = [z for z in solver.outcomes(child) if table[z][b] <= current]
                        assert allowed
                        if args.continuations == 'nearest':
                            score = min(sum(abs(x-y) for x, y in zip(z, desired)) for z in allowed)
                            allowed = [z for z in allowed if sum(abs(x-y) for x, y in zip(z, desired)) == score]
                        else:
                            score = max(table[z][b] for z in allowed)
                            allowed = [z for z in allowed if table[z][b] == score]
                        target_child = min(allowed)
                    expand(h+(b,), child, target_child)
            expand((), (0,)*p, root_target)
        assert set(actions) == {h for k in range(n) for h in product(range(p), repeat=k)}
        z = {}
        for k in range(n, -1, -1):
            for h in product(range(p), repeat=k):
                z[h] = tuple(h.count(a) for a in range(p)) if k == n else z[h+(actions[h],)]
        assert z[()] == root_target
        gamma = set()
        checks = 0
        for h, a in actions.items():
            for b in range(p):
                assert table[z[h]][a] >= table[z[h+(b,)]][b]
                row = sub(payoff(z[h], a), payoff(z[h+(b,)], b))
                if any(row):
                    gamma.add(row)
                checks += 1
        gamma = sorted(gamma)
        cone_hash = hashlib.sha256(str(gamma).encode()).hexdigest()
        seen_cones.add(cone_hash)
        optimum = max(c[mi[t]] for t in targets)
        game_ratio = optimum/minimum
        record = {'round': step, 'root': root_target, 'SPE_outcomes': len(outcomes),
                  'ordered_comparisons': checks, 'unique_gamma': len(gamma),
                  'cone': cone_hash, 'input_true_abstract_ratio': str(game_ratio)}
        rows = base+gamma
        mat = -np.array(rows, dtype=float)
        rootmask = supports[root_target]
        target = rng.choice([t for t in targets if c[mi[t]] == optimum])
        res = linprog(-np.array(units[target], dtype=float), A_ub=mat, b_ub=np.zeros(len(rows)),
                      A_eq=np.array([units[rootmask]], dtype=float), b_eq=[1], bounds=(0, None), method='highs')
        candidate = None
        if res.success:
            q = tuple(F(float(x)).limit_denominator(10**8) for x in res.x)
            if all(x >= 0 for x in q) and q[mi[rootmask]] == 1 and all(dot(row, q) >= 0 for row in rows):
                candidate = q
                record['exact_LP_value'] = str(q[mi[target]])
        # Explore an optimal face by a second, randomly weighted objective.
        if candidate is not None:
            bound = candidate[mi[target]]
            direction = np.array([rng.randint(-4, 4) for _ in masks], dtype=float)
            extmat = np.vstack([mat, -np.array(units[target], dtype=float)])
            extres = linprog(-direction, A_ub=extmat, b_ub=np.r_[np.zeros(len(rows)), -float(bound)],
                             A_eq=np.array([units[rootmask]], dtype=float), b_eq=[1], bounds=(0, None), method='highs')
            if extres.success:
                q = tuple(F(float(x)).limit_denominator(10**8) for x in extres.x)
                if all(x >= 0 for x in q) and q[mi[rootmask]] == 1 and q[mi[target]] >= bound and all(dot(row, q) >= 0 for row in rows):
                    candidate = q
            c = candidate
            value = max(c[mi[t]] for t in targets)
            record['next_candidate_comparison'] = str(value)
            if value > best:
                best = value
                best_witness = {'round': step, 'root': root_target, 'target': max(targets, key=lambda t: c[mi[t]]),
                                'actions': [{'h': h, 'a': a} for h, a in actions.items()],
                                'moments': {str(s): str(c[i]) for i, s in enumerate(masks) if c[i]},
                                'exact_feasible_ratio': str(value), 'customer_realizability': 'not_claimed'}
                print(json.dumps({'new_exact_ratio': str(value), 'round': step, 'full_history': True}), flush=True)
        else:
            record['LP_exact_recovery'] = 'failed_or_not_solved'
            c = None
        history.append(record)
        out = {'n': n, 'p': p, 'seed': args.seed, 'rounds_requested': args.rounds,
               'continuation_policy': args.continuations,
               'global_submodular': args.global_submodular,
               'root_selection': args.root_selection,
               'rounds_completed': len(history), 'distinct_full_tree_cones': len(seen_cones),
               'scope': ('global' if args.global_submodular else 'truncated')+' monotone submodular common moments, complete arbitrary-history pure SPE; no customer positivity claim',
               'Q_CAG_HALF': 'OPEN', 'best_exact_feasible_ratio': str(best),
               'best_witness': best_witness, 'history': history, 'elapsed_seconds': time.time()-started}
        (BASE/args.output).write_text(json.dumps(out, indent=2)+'\n')
        if best > 2:
            break
    print(json.dumps({'completed': len(history), 'best_exact_ratio': str(best), 'elapsed': time.time()-started}), flush=True)


if __name__ == '__main__':
    main()
