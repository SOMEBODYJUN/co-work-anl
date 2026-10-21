"""Candidate-only search for the specified root-stationary kernel's weak cap.

This is not a half-coverage prover. It samples complete strategy cones, fixes a
unique root-stationary distribution, then maximizes one static query over the
entire nonnegative customer multiplicity cone. Every returned point is checked
with Fraction; a found cap failure would concern only this prescribed kernel.
"""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import json
from pathlib import Path
import random
import sys

import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests/audits"))
from customer_attraction import ExactSPESolver
from customer_attraction_strategy_lp import (StrategyCone, payoff_row, dot,
    integer_clones, instance_from_clones)
from cone_attack_credible_variants import credible_cone


def unique_stationary(tails, p, m):
    """Exact RREF; returns None if the stationary simplex has positive dimension."""
    rows = [[F(tails[j][i], m-1) - (i == j) for j in range(p)] + [F(0)]
            for i in range(p)] + [[F(1)]*p + [F(1)]]
    rank = 0
    for col in range(p):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        divisor = rows[rank][col]
        rows[rank] = [v/divisor for v in rows[rank]]
        for i in range(len(rows)):
            if i != rank and rows[i][col]:
                coefficient = rows[i][col]
                rows[i] = [v-coefficient*w for v, w in zip(rows[i], rows[rank])]
        rank += 1
    if rank < p:
        return None
    pi = tuple(rows[i][-1] for i in range(p))
    assert all(v >= 0 for v in pi) and sum(pi) == 1
    assert all(sum(pi[a]*F(tails[a][b], m-1) for a in range(p)) == pi[b]
               for b in range(p))
    return pi


def probe(cone):
    p, m = cone.topics, cone.players
    tails = [tuple(cone.terminals[(a,)][b] - (a == b) for b in range(p))
             for a in range(p)]
    pi = unique_stationary(tails, p, m)
    if pi is None:
        return None
    best = None
    for t in range(p):
        objective = tuple(sum(pi[a]*payoff_row(p, tuple(v+(j == t)
                          for j, v in enumerate(tails[a])), t)[mask]
                          for a in range(p)) for mask in range((1 << p)-1))
        result = linprog(-np.array(objective, float), A_ub=-cone.matrix,
                         b_ub=np.zeros(len(cone.rows)),
                         A_eq=np.array([cone.welfare], float), b_eq=[1],
                         bounds=(0, None), method="highs")
        if not result.success:
            continue
        weights = tuple(F(float(v)).limit_denominator(10**7) for v in result.x)
        if not cone.verify(weights) or dot(cone.welfare, weights) != 1:
            weights = cone.recover_vertex(result.x)
        if weights is None:
            continue
        assert cone.verify(weights) and dot(cone.welfare, weights) == 1
        value = F(2*m-1, 2)*dot(objective, weights)
        candidate = {"value": value, "query": t, "pi": pi,
                     "weights": weights, "tails": tails, "cone": cone}
        if best is None or value > best["value"]:
            best = candidate
    return best


def export(candidate, path):
    cone = candidate["cone"]
    clones = integer_clones(candidate["weights"])
    assert cone.verify(tuple(map(F, clones)))
    instance = instance_from_clones(cone.topics, cone.players, clones)
    record = {"identity": "candidate failure only of specified root-stationary weak cap",
              "main_half_coverage_claim": "OPEN",
              "instance": instance.to_dict(),
              "actions": [{"history": list(h), "action": a}
                          for h, a in sorted(cone.actions.items(), key=lambda x: (len(x[0]), x[0]))],
              "root_counts": list(cone.root),
              "stationary_distribution": list(map(str, candidate["pi"])),
              "root_followers": candidate["tails"],
              "query": candidate["query"],
              "scaled_cap_to_welfare": str(candidate["value"])}
    path.write_text(json.dumps(record, indent=2) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--iterations", type=int, default=100)
    ap.add_argument("--seed", type=int, default=712108)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    source = json.loads((ROOT / "evidence/runs/2026-10-09/customer_attraction_strategy_lp_m4p5_certified.json").read_text())
    record = source["cone_proofs"][41]
    initial = StrategyCone(5, 4, {tuple(x["history"]): x["action"] for x in record["actions"]})
    first = probe(initial)
    assert first is not None
    beam = [first]
    seen = {tuple(sorted(initial.actions.items()))}
    best = first["value"]
    print("INITIAL", best, flush=True)
    for iteration in range(args.iterations):
        parent = rng.choice(beam[:min(8, len(beam))])
        cone = parent["cone"]
        instance = instance_from_clones(cone.topics, cone.players, integer_clones(parent["weights"]))
        solver = ExactSPESolver(instance)
        targets = sorted(solver.outcomes())
        target = cone.root if rng.random() < .8 else rng.choice(targets)
        mode = rng.choice(("max_credible_payoff", "max_credible_welfare", "min_credible_welfare", "uniform_credible"))
        child, _ = credible_cone(solver, target, rng, mode)
        key = tuple(sorted(child.actions.items()))
        if key in seen:
            continue
        seen.add(key)
        result = probe(child)
        if result is None:
            continue
        beam.append(result)
        beam.sort(key=lambda x: x["value"], reverse=True)
        beam = beam[:30]
        if result["value"] > best:
            best = result["value"]
            print("BEST", iteration, str(best), "query", result["query"], flush=True)
        if result["value"] > 1:
            path = Path(__file__).with_name("weak_stationary_kernel_candidate.json")
            export(result, path)
            print("CANDIDATE", str(path), flush=True)
            return
        if iteration % 10 == 0:
            print("PROGRESS", iteration, "unique_cones", len(seen), "best", str(best), flush=True)
    print("FINITE_SEARCH_NO_COUNTEREXAMPLE", args.iterations, len(seen), str(best), flush=True)


if __name__ == "__main__":
    main()
