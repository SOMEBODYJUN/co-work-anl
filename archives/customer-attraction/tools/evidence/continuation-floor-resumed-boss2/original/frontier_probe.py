"""Exact attacks on natural Pareto compression of credible continuation menus.

Exploratory finite computation, not a general theorem or a half-coverage test.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from functools import lru_cache
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction import CustomerType, ExactSPESolver, Instance


def profile(instance, prefix, terminal):
    """Current incumbent topic rents, followed by remaining players' profit."""
    utility = instance.topic_payoffs(terminal)
    rents = tuple(utility[a] for a, n in enumerate(prefix) if n)
    profit = sum((terminal[a] - prefix[a]) * utility[a]
                 for a in range(instance.topic_count))
    return rents + (profit,)


def compressed(instance, direction):
    """Prune at every nonroot node by one fixed Pareto orientation."""
    p = instance.topic_count

    @lru_cache(None)
    def solve(prefix):
        if sum(prefix) == instance.players:
            return frozenset({prefix})
        children = []
        for action in range(p):
            child = list(prefix)
            child[action] += 1
            children.append(solve(tuple(child)))
        threshold = max(min(instance.topic_payoffs(q)[a] for q in children[a])
                        for a in range(p))
        menu = frozenset(q for a in range(p) for q in children[a]
                         if instance.topic_payoffs(q)[a] >= threshold)
        if not sum(prefix):
            return menu
        vectors = {q: profile(instance, prefix, q) for q in menu}
        kept = set()
        for q, v in vectors.items():
            if not any(all(direction * x <= direction * y for x, y in zip(w, v))
                       and w != v for w in vectors.values()):
                kept.add(q)
        assert kept
        return frozenset(kept)

    return solve((0,) * p)


def encode(v):
    if isinstance(v, Fraction):
        return str(v)
    if isinstance(v, (tuple, list)):
        return [encode(x) for x in v]
    if isinstance(v, dict):
        return {k: encode(x) for k, x in v.items()}
    return v


def run(seed, trials, players, topics):
    rng = random.Random(seed)
    found = {}
    checked = 0
    for trial in range(trials):
        masks = rng.sample(range(1, 1 << topics),
                           rng.randint(topics, min((1 << topics) - 1, 2 * topics)))
        customers = tuple(CustomerType(frozenset(a for a in range(topics)
                                                if mask & (1 << a)),
                                       rng.randint(1, 5)) for mask in masks)
        instance = Instance(tuple(f"T{a}" for a in range(topics)), customers, players)
        solver = ExactSPESolver(instance)
        full = solver.outcomes()
        full_w = min(instance.welfare(q) for q in full)
        checked += 1
        for direction, label in [(1, "minimize_all"), (-1, "maximize_all")]:
            if label in found:
                continue
            reduced = compressed(instance, direction)
            reduced_w = min(instance.welfare(q) for q in reduced)
            if reduced_w != full_w:
                found[label] = encode({
                    "trial": trial, "instance": instance.to_dict(),
                    "full_minimum_welfare": full_w,
                    "compressed_minimum_welfare": reduced_w,
                    "full_root_outcomes": sorted(full),
                    "compressed_root_outcomes": sorted(reduced),
                })
        if len(found) == 2:
            break
    return {"status": "finite exact Pareto-compression attack", "seed": seed,
            "trials_requested": trials, "trials_checked": checked,
            "players": players, "topics": topics, "counterexamples": found}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=71021)
    parser.add_argument("--trials", type=int, default=2000)
    parser.add_argument("--players", type=int, default=4)
    parser.add_argument("--topics", type=int, default=4)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(args.seed, args.trials, args.players, args.topics)
    text = json.dumps(result, indent=2)
    if args.output:
        args.output.write_text(text + "\n")
    print(text)
