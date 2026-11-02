"""Exploratory attacks on free-fractional security in legal background subgames.

Every sampled policy is a complete remaining-game SPE. All LP/SLSQP results
remain numerical until an independently rationalized certificate is supplied.
"""
from pathlib import Path
import sys, json, argparse, random, time
from math import lcm
from itertools import combinations_with_replacement
import numpy as np
from scipy.optimize import linprog

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE / 'security'))
from fractional_minmax_probe import value


class Game:
    def __init__(self, r, k, prefix):
        self.n, self.k = r, k
        self.prefix = tuple(prefix)
        self.M = np.array([[bool(mask & (1 << j)) for j in range(k)]
                           for mask in range(1, 1 << k)], dtype=float)
        self.bg = self.M @ np.array(prefix)
        self.levels = []
        for d in range(r+1):
            self.levels.append([tuple(seq.count(j) for j in range(k))
                 for seq in combinations_with_replacement(range(k), d)])
        self.final = self.levels[-1]
        self.children = {q: [tuple(v + (j == a) for j, v in enumerate(q))
                            for a in range(k)]
                         for level in self.levels[:-1] for q in level}
        self.scale = lcm(*range(1, r + sum(prefix) + 1))
        coeff, profits = [], []
        for q in self.final:
            load = self.bg + self.M @ q
            coeff.append(np.rint(self.M.T * (self.scale / np.maximum(1, load))).astype(np.int64))
            profits.append((self.M @ q) / np.maximum(1, load))
        self.coeff = np.array(coeff)
        self.profit = np.array(profits)

    def evaluate(self, w):
        U = self.coeff @ w
        O = {q: np.array([j]) for j, q in enumerate(self.final)}
        for level in self.levels[-2::-1]:
            for q in level:
                ch = [O[c] for c in self.children[q]]
                floor = max(np.min(U[ts, a]) for a, ts in enumerate(ch))
                O[q] = np.unique(np.concatenate([ts[U[ts, a] >= floor - 1e-8]
                                                 for a, ts in enumerate(ch)]))
        return O, U

    def select(self, w):
        O, U = self.evaluate(w)
        zero = (0,) * self.k
        ch = [O[c] for c in self.children[zero]]
        floor = max(np.min(U[ts, a]) for a, ts in enumerate(ch))
        best = None
        for a, ts in enumerate(ch):
            use = ts[U[ts, a] >= floor - 1e-8]
            if len(use):
                t = min(use, key=lambda z: U[z, a])
                if best is None or U[t, a] < best[0]:
                    best = (float(U[t, a]), a, int(t))
        return best[1], best[2], O, U

    def cone(self, w):
        first, t, O, U = self.select(w)
        rows, policy = set(), []
        stack = [((0,) * self.k, t)]
        seen = set()
        while stack:
            q, target = stack.pop()
            if (q, target) in seen or sum(q) == self.n:
                continue
            seen.add((q, target))
            ch = [O[c] for c in self.children[q]]
            floor = max(np.min(U[ts, a]) for a, ts in enumerate(ch))
            acts = [a for a, ts in enumerate(ch) if target in ts and U[target, a] >= floor - 1e-8]
            a = first if not sum(q) else acts[0]
            policy.append([q, target, a])
            for b, ts in enumerate(ch):
                dev = target if b == a else min(ts, key=lambda z: U[z, b])
                stack.append((self.children[q][b], int(dev)))
                row = tuple((self.coeff[target, a] - self.coeff[dev, b]).tolist())
                if any(row): rows.add(row)
        return np.array(sorted(rows), dtype=float) / self.scale, policy, first, t


def saddle(g, w, r=None, bg=None):
    r = g.n if r is None else r
    bg = g.bg if bg is None else bg
    val, q, pay = value(g.M, w, r, bg)
    z = 1 / (1 + bg + (r-1) * (g.M @ q))
    H = g.M.T @ (g.M * (w * z*z)[:, None])
    eq = [np.r_[np.ones(g.k), 0]]
    for j in np.flatnonzero(q > 1e-7): eq.append(np.r_[H[j], -1])
    active = pay >= val - 1e-6
    lp = linprog(np.zeros(g.k+1), A_ub=np.c_[H, -np.ones(g.k)],
        b_ub=np.zeros(g.k), A_eq=eq, b_eq=[1] + [0] * (len(eq)-1),
        bounds=[(0, None) if yes else (0, 0) for yes in active] + [(None, None)], method='highs')
    p = lp.x[:-1] if lp.success else active / sum(active)
    rho = g.M @ p
    aa = rho * (2*z - (1+bg)*z*z)
    DD = g.M.T * (rho*z*z)
    return val, q, p, aa, DD


def optimize(g, seed, kind, rounds=15):
    G, policy, action, target = g.cone(seed)
    ui = g.coeff[target, action] / g.scale
    norm = g.profit[target]
    w = seed / (norm @ seed)
    trace = []
    for iteration in range(rounds):
        val, q, p, aa, DD = saddle(g, w)
        rootmul = g.n if kind == 'local' else 1
        A = [np.r_[-row, 0, 0] for row in G]
        b = [0.] * len(A)
        A += [np.r_[row, -1, 0] for row in DD]
        b += [0.] * len(DD)
        obj = np.r_[ui-rootmul*aa, rootmul*(g.n-1), 0.]
        if kind == 'local':
            nv, nq, np_, na, nD = saddle(g, w, g.n-1, g.bg+g.M[:, action])
            den = 1+g.bg+g.M[:, action]+(g.n-2)*(g.M@nq)
            A += [np.r_[row, 0, -1] for row in g.M.T/den]
            b += [0.] * g.k
            obj[-1] = g.n-1
        lp = linprog(obj, A_ub=A, b_ub=b, A_eq=[np.r_[norm, 0, 0]], b_eq=[1],
                     bounds=[(0, None)] * len(w) + [(None, None), (None, None)], method='highs')
        if not lp.success:
            return dict(status=lp.message, trace=trace)
        w = lp.x[:-2]
        rv, rq, rp, ra, rD = saddle(g, w)
        debt = ui @ w - rv
        if kind == 'local':
            nv, nq, np_, na, nD = saddle(g, w, g.n-1, g.bg+g.M[:, action])
            debt = ui @ w + (g.n-1)*nv - g.n*rv
        trace.append(dict(iteration=iteration, debt=float(debt), leader=float(ui@w),
                          value=rv, min_spe_margin=float(np.min(G@w))))
        if debt < -1e-7 or len(trace)>1 and abs(trace[-2]['debt']-debt)<1e-11:
            break
    return dict(status='NUMERICAL_EXPLORATION', kind=kind, r=g.n, k=g.k,
                prefix=g.prefix, root_action=action, terminal=g.final[target],
                weights=w.tolist(), trace=trace, policy=policy, rows=G.tolist(),
                query=rp.tolist(), fractional_q=rq.tolist())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--r', type=int, default=3)
    ap.add_argument('--k', type=int, default=5)
    ap.add_argument('--prefix', default='1,0,0,0,0')
    ap.add_argument('--kind', choices=['floor','local'], default='floor')
    ap.add_argument('--seconds', type=int, default=45)
    ap.add_argument('--seed', type=int, default=6241)
    ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    prefix = tuple(map(int,a.prefix.split(',')))
    assert len(prefix) == a.k
    g = Game(a.r,a.k,prefix)
    rng = random.Random(a.seed)
    best, bank, trials, failures = None, [], 0, 0
    start = time.monotonic()
    while time.monotonic() - start < a.seconds:
        if bank and rng.random() < .7:
            seed = np.array(rng.choice(bank)['weights']) * 100
            for j in rng.sample(range(len(seed)), min(8,len(seed))):
                seed[j] = max(0, seed[j] + rng.randrange(-5,6))
        else:
            seed = np.array([rng.randrange(16) if rng.random()<.4 else 0 for _ in range(len(g.M))],dtype=float)
        if not sum(seed):continue
        try: out = optimize(g,seed,a.kind)
        except (RuntimeError, ValueError): failures += 1; continue
        trials += 1
        if not out.get('trace'): continue
        if best is None or out['trace'][-1]['debt'] < best['trace'][-1]['debt'] - 1e-10:
            best=out
            print(json.dumps(dict(trial=trials, prefix=prefix, best=out['trace'][-1])),flush=True)
        bank.append(out)
        bank.sort(key=lambda x:x['trace'][-1]['debt'])
        bank=bank[:10]
        a.output.write_text(json.dumps(dict(status='NUMERICAL_EXPLORATION_ONLY', trials=trials,
             elapsed=time.monotonic()-start, failures=failures, best=best, bank=bank),indent=2)+'\n')
        if best['trace'][-1]['debt'] < -1e-7:break

if __name__ == '__main__':main()
