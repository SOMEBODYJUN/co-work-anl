"""Search exact-model candidates by complete count-policy cones.

A count policy is a legal, special full-history policy. For fixed policy all
one-step SPE comparisons are linear in unit-customer multiplicities. This
script optimizes inside that cone, then chooses another genuine BI policy.
Floating output is discovery evidence only; no general theorem is asserted.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path
import time

import numpy as np
from scipy.optimize import linprog


def compositions(total, parts):
    if parts == 1:
        yield (total,)
    else:
        for first in range(total + 1):
            for tail in compositions(total - first, parts - 1):
                yield (first,) + tail


class Search:
    def __init__(self, m, k, seed):
        self.m, self.k = m, k
        self.rng = np.random.default_rng(seed)
        self.types = np.arange(1, 1 << k)
        self.inc = ((self.types[:, None] >> np.arange(k)) & 1).astype(float)
        self.layers = [list(compositions(d, k)) for d in range(m + 1)]
        self.term = self.layers[-1]
        self.tindex = {q: i for i, q in enumerate(self.term)}
        loads = np.asarray(self.term) @ self.inc.T
        self.cover = (loads > 0).astype(float)
        reciprocals = np.divide(1.0, loads, out=np.zeros_like(loads), where=loads > 0)
        self.coeff = reciprocals[:, None, :] * self.inc.T[None, :, :]
        self.opt_supports = list(combinations(range(k), min(m, k)))
        self.opt_coeff = np.asarray([
            (np.sum(self.inc[:, support], axis=1) > 0).astype(float)
            for support in self.opt_supports
        ])
        self.children = {}
        for layer in self.layers[:-1]:
            for q in layer:
                self.children[q] = [q[:a] + (q[a] + 1,) + q[a+1:]
                                    for a in range(k)]

    def bi(self, weights, tie_mode="random"):
        payoffs = self.coeff @ weights
        welfare = self.cover @ weights
        terminal = dict(self.tindex)
        policy = {}
        for layer in self.layers[-2::-1]:
            for q in layer:
                leaves = [terminal[c] for c in self.children[q]]
                vals = np.asarray([payoffs[leaf, a] for a, leaf in enumerate(leaves)])
                best = np.flatnonzero(vals >= max(vals) - 1e-8 * max(1, max(vals)))
                if tie_mode == "poor":
                    best = best[np.flatnonzero(
                        welfare[np.asarray(leaves)[best]] <=
                        min(welfare[np.asarray(leaves)[best]]) + 1e-9)]
                chosen = int(self.rng.choice(best))
                policy[q] = chosen
                terminal[q] = leaves[chosen]
        return policy, terminal

    def optimize(self, policy, terminal, support_index):
        rows = []
        for layer in self.layers[:-1]:
            for q in layer:
                chosen = policy[q]
                actual = self.coeff[terminal[q], chosen]
                for a, child in enumerate(self.children[q]):
                    if a != chosen:
                        rows.append(self.coeff[terminal[child], a] - actual)
        root_leaf = terminal[(0,) * self.k]
        result = linprog(-self.opt_coeff[support_index], A_ub=np.asarray(rows),
                         b_ub=np.zeros(len(rows)),
                         A_eq=self.cover[root_leaf][None, :], b_eq=[1.0],
                         bounds=(0, None), method="highs")
        return result, root_leaf

    def run(self, restarts, steps, output):
        best = 0.0
        started = time.monotonic()
        for restart in range(restarts):
            weights = self.rng.lognormal(0, 1.4, len(self.types))
            weights *= self.rng.random(len(weights)) < self.rng.uniform(.1, .8)
            weights += self.rng.random(len(weights)) * 1e-5
            for step in range(steps):
                policy, terminal = self.bi(weights, "poor" if step % 2 else "random")
                support_index = (int(np.argmax(self.opt_coeff @ weights))
                                 if step % 4 else int(self.rng.integers(len(self.opt_supports))))
                result, root_leaf = self.optimize(policy, terminal, support_index)
                if not result.success:
                    print(json.dumps({"restart": restart, "step": step,
                                      "status": result.message}), flush=True)
                    break
                ratio = -float(result.fun)
                if ratio > best + 1e-7:
                    best = ratio
                    record = {"m": self.m, "k": self.k, "ratio": ratio,
                              "root_counts": self.term[root_leaf],
                              "support": self.opt_supports[support_index],
                              "weights": [[int(t), float(w)] for t, w in zip(self.types, result.x)
                                          if w > 1e-9],
                              "policy": [[list(q), a] for q, a in policy.items()],
                              "restart": restart, "step": step,
                              "seconds": time.monotonic() - started}
                    Path(output).write_text(json.dumps(record, indent=2) + "\n")
                    print(json.dumps({key: record[key] for key in
                                      ("m", "k", "ratio", "root_counts", "support", "restart", "step", "seconds")}),
                          flush=True)
                weights = np.maximum(result.x, 0)
                # Preserve a coherent BI instance while crossing zero-type and
                # indifferent-policy faces. No claim is made from the noise.
                if step % 3 == 2:
                    noise = self.rng.random(len(weights))
                    noise *= self.rng.random(len(weights)) < .1
                    weights += self.rng.uniform(.001, .03) * noise
        print(json.dumps({"done": True, "best": best,
                          "seconds": time.monotonic() - started}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--players", type=int, default=5)
    parser.add_argument("--topics", type=int, default=7)
    parser.add_argument("--seed", type=int, default=133)
    parser.add_argument("--restarts", type=int, default=30)
    parser.add_argument("--steps", type=int, default=10)
    parser.add_argument("--output", default="best_policy_cone.json")
    args = parser.parse_args()
    Search(args.players, args.topics, args.seed).run(args.restarts, args.steps, args.output)
