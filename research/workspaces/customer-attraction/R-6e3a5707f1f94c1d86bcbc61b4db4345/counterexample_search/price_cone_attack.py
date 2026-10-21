"""Finite full-history cone attack on B(min_i u_i) <= W.

An LP proposes a capped coverage portfolio z and another LP moves customer
counts within a specified complete-history SPE cone. Integer primal points
and portfolio objectives are checked exactly. No failure of this finite search
is a proof of the price bridge or of Q-CAG-HALF.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, random, sys, time
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'customer_attraction/__init__.py').is_file())
sys.path.insert(0, str(ROOT))
SOURCE = ROOT / 'research/workspaces/customer-attraction/R-18e993ca519949aba29e030d3d7b15b3/counterexample_search/cone_walk.py'
spec = importlib.util.spec_from_file_location('existing_complete_history_cone', SOURCE)
engine_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine_module)


def portfolio(eng, r, price):
    """Return a rational feasible capped portfolio; LP dual is not needed."""
    n, p = len(eng.masks), eng.p
    matrix = np.hstack((-eng.inc.T.astype(float), np.eye(n)))
    result = linprog(np.r_[np.repeat(float(price), p), -np.asarray(r, dtype=float)],
                     A_ub=matrix, b_ub=np.zeros(n), bounds=[(0, 1)] * (n + p), method='highs')
    if not result.success:
        raise RuntimeError(result.message)
    z = tuple(F(float(v)).limit_denominator(10**6) for v in result.x[:p])
    assert all(0 <= v <= 1 for v in z)
    coverage = tuple(min(F(1), sum((z[a] for a in range(p) if mask & (1 << a)), F()))
                     for mask in eng.masks)
    return z, coverage


def exact_score(eng, clones, target, topic, z, coverage):
    welfare = sum(int(v) * int(c) for v, c in zip(eng.cov[target], clones))
    price = F(sum(int(v) * int(c) for v, c in zip(eng.pay[target, topic], clones)), eng.L)
    value = sum((h * c for h, c in zip(coverage, clones)), F()) - price * sum(z, F())
    return value / welfare, price, welfare


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--players', type=int, default=5)
    ap.add_argument('--topics', type=int, default=7)
    ap.add_argument('--steps', type=int, default=50)
    ap.add_argument('--rounds', type=int, default=4)
    ap.add_argument('--seed', type=int, default=2026102137)
    ap.add_argument('--output', default='price_m5p7')
    args = ap.parse_args()
    rng = random.Random(args.seed)
    eng = engine_module.Engine(args.players, args.topics, rng)
    seeds = [engine_module.baseline(args.players, args.topics)]
    # Known non-PNE reply cycle embedded among arbitrary additional themes.
    known = {2: 1, 3: 2, 7: 2, 10: 3, 12: 3, 13: 5}
    for j in range(12):
        r = [0] * len(eng.masks)
        for mask, n in known.items():
            r[mask - 1] = n * rng.choice((1, 2, 3))
        for a in range(4, args.topics):
            r[(1 << a) - 1] = rng.randint(1, 8)
        for k in range(rng.randint(1, 7)):
            r[rng.randrange(len(r))] += rng.randint(1, 5)
        seeds.append(r)
    records, endpoints, seen = [], [], set()
    best, start = F(-10**6), time.monotonic()
    best_witness = None
    for step in range(args.steps):
        if seeds:
            r = seeds.pop(0)
        elif endpoints and rng.random() < .75:
            r = [float(v) * rng.choice((10, 30, 100)) for v in rng.choice(endpoints)]
            for k in range(rng.randint(1, 5)):
                r[rng.randrange(len(r))] += rng.random() * .1
        else:
            r = [0] * len(eng.masks)
            for k in range(rng.randint(8, 25)):
                mask = sum(1 << a for a in rng.sample(range(args.topics), rng.randint(1, min(4, args.topics))))
                r[mask - 1] += rng.randint(1, 25)
        eng.solve(r, diverse=True)
        # Search the exact all-outcome menus, choosing low actual occupied payoff.
        targets = sorted(eng.R[0][0], key=lambda q: min(eng.u[q, a] for a, n in enumerate(eng.terminal[q]) if n))
        target = int(rng.choice(targets[:max(1, len(targets) // 3)]))
        actions, G = eng.strategy(target)
        key = hashlib.sha256(repr(actions).encode()).hexdigest()
        if key in seen:
            continue
        seen.add(key)
        occupied = [a for a, n in enumerate(eng.terminal[target]) if n]
        topic = min(occupied, key=lambda a: eng.u[target, a])
        row = {'step': step, 'root_counts': eng.terminal[target].tolist(), 'topic': topic,
               'cone_sha256': key, 'rows': len(G), 'rounds': []}
        for iteration in range(args.rounds):
            price = float(np.dot(eng.pay[target, topic], r)) / eng.L
            z, coverage = portfolio(eng, r, price)
            objective = np.array([float(h) for h in coverage]) - float(sum(z, F())) * eng.pay[target, topic].astype(float) / eng.L
            result = linprog(-objective, A_ub=-G.astype(float), b_ub=np.zeros(len(G)),
                             A_eq=[eng.cov[target].astype(float)], b_eq=[1.],
                             bounds=(0, None), method='highs')
            if not result.success:
                row['rounds'].append({'status': result.message})
                break
            r = result.x.tolist()
            endpoints.append(r)
            clones = eng.exact_recover(G, target, result.x)
            rec = {'proposal_B_over_W': float(-result.fun)}
            if clones is not None:
                value, exact_price, welfare = exact_score(eng, clones, target, topic, z, coverage)
                rec['exact_feasible_portfolio_over_W'] = str(value)
                if value > best:
                    inst, cert = engine_module.verify_canonical(args.players, args.topics, clones, actions,
                                                                eng.terminal[target].tolist())
                    best = value
                    best_witness = {'scope': 'one full-history pure SPE and feasible price portfolio; no universal result',
                                    'parameters': vars(args), 'step': step, 'round': iteration,
                                    'B_lower_bound_over_W': str(value), 'price': str(exact_price), 'W': welfare,
                                    'OPT': inst.optimal_welfare(), 'topic': topic,
                                    'z': [str(v) for v in z], 'instance': inst.to_dict(),
                                    'strategy': cert.to_dict(), 'canonical_full_history_verified': True}
                    (HERE / (args.output + '_best.json')).write_text(json.dumps(best_witness, indent=2) + '\n')
                    print(json.dumps({'step': step, 'round': iteration, 'new_exact_B_lower_over_W': str(best),
                                      'elapsed': round(time.monotonic() - start, 3)}), flush=True)
            row['rounds'].append(rec)
        records.append(row)
        report = {'scope': 'finite complete-history SPE-cone attack; no universal proof', 'parameters': vars(args),
                  'best_exact_B_lower_over_W': str(best), 'cones': len(seen),
                  'elapsed': round(time.monotonic() - start, 3), 'records': records}
        (HERE / (args.output + '_run.json')).write_text(json.dumps(report, indent=2) + '\n')
        if best > 1:
            break
    print(json.dumps({k: v for k, v in report.items() if k != 'records'}), flush=True)


if __name__ == '__main__':
    main()
