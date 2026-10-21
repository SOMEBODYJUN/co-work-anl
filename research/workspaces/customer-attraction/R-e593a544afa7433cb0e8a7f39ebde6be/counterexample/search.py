"""Exploratory exact-payoff BI and full-strategy-cone LP; no universal claim.

Payoff coefficient rows are integral after multiplication by lcm(1,...,m).
For integer weights BI comparisons are exact. Floating LP is only a candidate
generator; any putative counterexample must go through canonical exact BI and
independent full-history verification before being reported as one.
"""
import argparse
from functools import lru_cache
from itertools import combinations
from math import lcm
import json
import random
import time
from pathlib import Path

import numpy as np
from scipy.optimize import linprog


def compositions(n, k):
    if k == 1:
        yield (n,)
    else:
        for a in range(n + 1):
            for tail in compositions(n - a, k - 1):
                yield (a,) + tail


class Search:
    def __init__(self, p, m, seed):
        self.p, self.m = p, m
        self.rng = random.Random(seed)
        self.types = np.arange(1, 1 << p)
        self.incidence = ((self.types[:, None] >> np.arange(p)) & 1).astype(np.int16)
        self.levels = [list(compositions(d, p)) for d in range(m + 1)]
        self.terminals = self.levels[m]
        self.tidx = {k: i for i, k in enumerate(self.terminals)}
        self.counts = sum(self.levels, [])
        self.idx = {k: i for i, k in enumerate(self.counts)}
        self.children = np.empty((len(self.counts) - len(self.terminals), p), dtype=int)
        for i, k in enumerate(self.counts[:len(self.children)]):
            for a in range(p):
                child = list(k)
                child[a] += 1
                self.children[i, a] = self.idx[tuple(child)]
        self.scale = lcm(*range(1, m + 1))
        denom = np.array(self.terminals) @ self.incidence.T
        self.f = np.zeros((len(self.terminals), p, len(self.types)), dtype=np.int16)
        for a in range(p):
            use = (denom > 0) & (self.incidence[:, a][None, :] > 0)
            self.f[:, a, :][use] = self.scale // denom[use]
        self.coverage = (denom > 0).astype(np.int16)
        self.J = tuple(combinations(range(p), min(m, p)))
        self.optrows = np.array([((self.types & sum(1 << a for a in j)) > 0)
                                 for j in self.J], dtype=np.int16)

    def bi(self, weights):
        """Integer weights give exact comparisons; float inputs use tolerance."""
        self.pay = self.f @ weights
        self.welfare = self.coverage @ weights
        self.optvalues = self.optrows @ weights
        self.R = [None] * len(self.counts)
        self.floor = np.zeros(len(self.children), dtype=self.pay.dtype)
        for t, k in enumerate(self.terminals):
            self.R[self.idx[k]] = np.array([t], dtype=int)
        tolerance = 0 if np.issubdtype(self.pay.dtype, np.integer) else 1e-8
        for i in reversed(range(len(self.children))):
            child = [self.R[j] for j in self.children[i]]
            floor = max(self.pay[c, a].min() for a, c in enumerate(child))
            self.floor[i] = floor
            self.R[i] = np.unique(np.concatenate([c[self.pay[c, a] >= floor - tolerance]
                                                 for a, c in enumerate(child)]))
        self.root = min(self.R[0], key=lambda t: self.welfare[t])
        self.ratio = max(self.optvalues) / max(self.welfare[self.root], 1e-20)
        return self.ratio

    def cone(self, mode="min", root=None):
        """All rows of one complete SPE, compressed by (counts, desired outcome).

        Every ordered history inherits its own desired outcome from its parent.
        Reusing identical (counts,desired) pairs only chooses a particular SPE;
        it does not collapse the full set-valued BI or claim every SPE Markov.
        """
        root = self.root if root is None else root
        rows = set()
        policy = {}
        tolerance = 1e-7
        @lru_cache(None)
        def visit(i, target):
            if i >= len(self.children):
                return
            allowed = [a for a, j in enumerate(self.children[i])
                       if target in self.R[j] and self.pay[target, a] >= self.floor[i] - tolerance]
            a = self.rng.choice(allowed)
            branch = []
            for b, j in enumerate(self.children[i]):
                if a == b:
                    desired = target
                else:
                    possible = self.R[j]
                    values = self.pay[possible, b]
                    if mode == "min":
                        possible = possible[values <= values.min() + tolerance]
                    else:
                        possible = possible[values <= self.pay[target, a] + tolerance]
                    desired = int(self.rng.choice(possible))
                    row = self.f[target, a].astype(np.int16) - self.f[desired, b]
                    if np.any(row):
                        rows.add(row.tobytes())
                branch.append(desired)
                visit(int(j), desired)
            policy[i, target] = (a, tuple(branch))
        visit(0, int(root))
        matrix = np.array([np.frombuffer(x, dtype=np.int16) for x in rows], dtype=float)
        return matrix, policy

    def optimize(self, matrix, root=None, all_j=False):
        root = self.root if root is None else root
        jlist = range(len(self.J)) if all_j else [int(np.argmax(self.optvalues))]
        best = None
        for j in jlist:
            res = linprog(-self.optrows[j].astype(float), A_ub=-matrix,
                          b_ub=np.zeros(len(matrix)), A_eq=self.coverage[root][None, :],
                          b_eq=[1], bounds=(0, None), method="highs")
            if res.success and (best is None or res.fun < best.fun):
                best = res
                best.j = j
        return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topics", type=int, default=7)
    ap.add_argument("--players", type=int, default=5)
    ap.add_argument("--seed", type=int, default=35193)
    ap.add_argument("--iterations", type=int, default=100)
    ap.add_argument("--all-j", action="store_true")
    ap.add_argument("--random-roots", action="store_true")
    ap.add_argument("--seeds", choices=("big", "random", "cycle", "mix"), default="big")
    ap.add_argument("--out", default="search_result.json")
    args = ap.parse_args()
    s = Search(args.topics, args.players, args.seed)
    weights = np.zeros(len(s.types), dtype=np.int64)
    weights[0] = args.players
    for a in range(1, args.topics):
        weights[(1 << a) - 1] = 1
    baseline = weights.copy()
    best = 0
    records = []
    started = time.time()
    for step in range(args.iterations):
        if step % 10 == 0:
            weights = baseline.copy()
            seedmode = s.rng.choice(("big", "random", "cycle")) if args.seeds == "mix" else args.seeds
            if seedmode == "random":
                weights[:] = 0
                for _ in range(s.rng.randrange(5, 16)):
                    mask = s.rng.randrange(1, 1 << args.topics)
                    weights[mask - 1] += s.rng.randrange(1, 21)
            elif seedmode == "cycle":
                weights[:] = 0
                cycle = {2: 3, 4: 3, 1 | 8: 2, 1 | 16: 2, 2 | 8 | 16: 2, 4 | 8 | 16: 2}
                for mask, count in cycle.items():
                    weights[mask - 1] = count
                for a in range(5, args.topics):
                    weights[(1 << a) - 1] = s.rng.randrange(1, 11)
        ratio = s.bi(weights)
        if args.random_roots and step % 3:
            ordered = sorted(s.R[0], key=lambda t: s.welfare[t])
            s.root = int(s.rng.choice(ordered[:max(1, len(ordered) // 2)]))
        matrix, policy = s.cone(mode="min" if step % 3 else "any")
        res = s.optimize(matrix, all_j=args.all_j)
        if res is None:
            print("LP failure", step, flush=True)
            continue
        candidate = -res.fun
        record = {"step": step, "ratio": float(ratio), "cone_value": candidate,
                  "rows": len(matrix), "root": s.terminals[s.root], "support": s.J[res.j],
                  "positive_types": int(np.count_nonzero(res.x > 1e-8))}
        records.append(record)
        if step % 50 == 49:
            print(json.dumps({"progress": step + 1, "current": record, "best": best,
                              "elapsed": time.time() - started}), flush=True)
        if candidate > best + 1e-8:
            best = candidate
            print(json.dumps(record) + f" time={time.time() - started:.1f}", flush=True)
            payload = {"args": vars(args), "best": record, "weights_float": res.x.tolist(),
                       "policy": [[i, t, a, list(branch)] for (i,t),(a,branch) in policy.items()],
                       "records": records}
            Path(args.out).write_text(json.dumps(payload, indent=2))
        if candidate > 2 + 1e-7:
            print("POTENTIAL ONLY; REQUIRES EXACT FULL-HISTORY VERIFICATION", flush=True)
            break
        # Stay on a boundary to preserve strategic ties, then occasionally move
        # into a nearby positive cone by mixing with the original SPE input.
        weights = res.x
        if step % 10 in (4, 8):
            weights = 0.999 * weights + 0.001 * baseline / args.players
    print(json.dumps({"best_float_candidate": best, "steps": len(records),
                      "elapsed": time.time() - started}), flush=True)
    result_path = Path(args.out)
    if result_path.exists():
        payload = json.loads(result_path.read_text())
        payload["records"] = records
        payload["elapsed"] = time.time() - started
        result_path.write_text(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
