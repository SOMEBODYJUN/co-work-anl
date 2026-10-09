"""Optimize customer multiplicities inside a fixed full-history SPE cone.

Floating LP is a candidate generator only. All accepted primal/dual certificates
are checked over Fraction; integer clones and every ordered-history deviation
are then checked without invoking the canonical equilibrium verifier. A fixed
strategy cone is not the union of every SPE cone, so this audit proves no
universal efficiency bound. scipy is an optional audit dependency.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
import hashlib
from itertools import combinations, product
import json
from math import gcd, lcm
from pathlib import Path
import random
import subprocess
import sys
import time

import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from customer_attraction import CustomerType, ExactSPESolver, Instance, StrategyCertificate


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), Fraction(0))


@lru_cache(None)
def payoff_row(topics: int, counts: tuple[int, ...], action: int):
    result = []
    for mask in range(1, 1 << topics):
        denominator = sum(counts[a] for a in range(topics) if mask & (1 << a))
        result.append(Fraction(1, denominator) if mask & (1 << action) else Fraction(0))
    return tuple(result)


def coverage_row(topics: int, support):
    mask = sum(1 << a for a in support)
    return tuple(Fraction(bool(mask & customer)) for customer in range(1, 1 << topics))


@dataclass
class StrategyCone:
    """Exactly the multiplicities making a specified full strategy a pure SPE."""

    topics: int
    players: int
    actions: dict[tuple[int, ...], int]

    def __post_init__(self):
        required = {h for depth in range(self.players)
                    for h in product(range(self.topics), repeat=depth)}
        if set(self.actions) != required:
            raise ValueError("strategy must specify every ordered decision history")
        if any(a not in range(self.topics) for a in self.actions.values()):
            raise ValueError("invalid action")
        self.terminals = {}
        for depth in range(self.players, -1, -1):
            for h in product(range(self.topics), repeat=depth):
                if depth == self.players:
                    self.terminals[h] = tuple(h.count(a) for a in range(self.topics))
                else:
                    self.terminals[h] = self.terminals[h + (self.actions[h],)]
        self.root = self.terminals[()]
        self.welfare = coverage_row(self.topics, (a for a, c in enumerate(self.root) if c))
        constraints = set()
        for h, action in self.actions.items():
            actual = payoff_row(self.topics, self.terminals[h], action)
            for alternative in range(self.topics):
                if alternative == action:
                    continue
                deviation = payoff_row(self.topics, self.terminals[h + (alternative,)], alternative)
                row = tuple(x - y for x, y in zip(actual, deviation))
                if any(row):
                    constraints.add(row)
        self.rows = tuple(sorted(constraints))
        self.matrix = np.array(self.rows, dtype=float)
        if not self.rows:
            self.matrix = np.zeros((0, (1 << self.topics) - 1))

    def verify(self, multiplicities):
        if any(x < 0 for x in multiplicities):
            return False
        return all(dot(row, multiplicities) >= 0 for row in self.rows)

    def optimize(self, support):
        """Return an exact feasible vector and, when recovered, exact dual bound.

        max v.r subject to G.r >= 0, w.r = 1, r >= 0.
        The exact upper certificate is beta*w - G^T*mu >= v, mu >= 0.
        """
        objective = coverage_row(self.topics, support)
        res = linprog(-np.array(objective, dtype=float),
                      A_ub=-self.matrix, b_ub=np.zeros(len(self.rows)),
                      A_eq=np.array([self.welfare], dtype=float), b_eq=[1],
                      bounds=(0, None), method="highs")
        if not res.success:
            return {"status": res.message, "certified": False}
        values = tuple(Fraction(float(x)).limit_denominator(10**7) for x in res.x)
        primal_ok = self.verify(values) and dot(self.welfare, values) == 1
        # Exact rational recovery, rather than accepting a solver tolerance.
        if not primal_ok:
            values = self.recover_vertex(res.x)
            primal_ok = values is not None and self.verify(values) and dot(self.welfare, values) == 1
        if not primal_ok:
            return {"status": "floating_vertex_failed_exact_recovery", "certified": False}
        beta = Fraction(float(-res.eqlin.marginals[0])).limit_denominator(10**7)
        dual = tuple(Fraction(float(-x)).limit_denominator(10**7) for x in res.ineqlin.marginals)
        residual = tuple(beta * w - sum(mu * row[j] for mu, row in zip(dual, self.rows)) - v
                         for j, (w, v) in enumerate(zip(self.welfare, objective)))
        dual_ok = beta >= 0 and all(mu >= 0 for mu in dual) and all(x >= 0 for x in residual)
        value = dot(objective, values)
        if dual_ok and value > beta:
            raise AssertionError("exact primal exceeds exact dual")
        return {"status": "exact_primal", "certified": True,
                "values": values, "value": value,
                "dual_bound": beta if dual_ok else None,
                "dual_optimal": dual_ok and beta == value,
                "dual_support": tuple((i, mu) for i, mu in enumerate(dual) if mu) if dual_ok else (),
                "support": tuple(support)}

    def recover_vertex(self, floating):
        """Solve independent active rows on the floating positive support exactly."""
        support = [i for i, x in enumerate(floating) if x > 1e-8]
        candidates = [self.welfare] + [row for row in self.rows
                                      if abs(sum(float(row[j]) * floating[j] for j in range(len(row)))) < 1e-7]
        basis = {}
        for index, row in enumerate(candidates):
            reduced = [row[j] for j in support] + [Fraction(index == 0)]
            for pivot in sorted(basis):
                coefficient = reduced[pivot]
                if coefficient:
                    reduced = [x - coefficient * y for x, y in zip(reduced, basis[pivot])]
            pivot = next((j for j, x in enumerate(reduced[:-1]) if x), None)
            if pivot is not None:
                coefficient = reduced[pivot]
                basis[pivot] = [x / coefficient for x in reduced]
            elif reduced[-1]:
                return None
            if len(basis) == len(support):
                break
        if len(basis) != len(support):
            return None
        solution = [Fraction(0)] * len(support)
        for pivot in sorted(basis, reverse=True):
            row = basis[pivot]
            solution[pivot] = row[-1] - sum(row[j] * solution[j] for j in range(pivot + 1, len(support)))
        result = [Fraction(0)] * len(floating)
        for index, x in zip(support, solution):
            result[index] = x
        return tuple(result)


def integer_clones(values):
    scale = lcm(*(x.denominator for x in values))
    clones = tuple(int(x * scale) for x in values)
    common = gcd(*clones)
    return tuple(x // common for x in clones)


def instance_from_clones(topics, players, clones):
    return Instance(tuple(f"T{a}" for a in range(topics)),
                    tuple(CustomerType(frozenset(a for a in range(topics) if mask & (1 << a)), count)
                          for mask, count in enumerate(clones, 1) if count), players)


def independently_verify(cone, clones):
    """Directly compare all history-node terminal branch payoffs, using Fraction."""
    for h, action in cone.actions.items():
        def utility(branch, selected):
            total = Fraction(0)
            q = cone.terminals[branch]
            for mask, count in enumerate(clones, 1):
                if mask & (1 << selected):
                    total += Fraction(count, sum(q[a] for a in range(cone.topics) if mask & (1 << a)))
            return total
        actual = utility(h, action)
        for alternative in range(cone.topics):
            if utility(h + (alternative,), alternative) > actual:
                return False
    return True


def structural_seeds(topics, players):
    """Private big/small plus two reply-cycle variants; no random instance sweep."""
    n = (1 << topics) - 1
    base = [0] * n
    base[0] = players
    for a in range(1, topics):
        base[(1 << a) - 1] = 1
    yield tuple(base)
    # Embed the known 2-player residual reply cycle in every player count.
    if topics >= 5:
        residual = {2: 3, 4: 3, 1 | 8: 2, 1 | 16: 2, 2 | 8 | 16: 2, 4 | 8 | 16: 2}
        yield tuple(residual.get(mask, 0) for mask in range(1, 1 << topics))
        # Attach disjoint options and amplify shared-reply populations in turn.
        for factor in (players - 1, players, 2 * players):
            cycle = dict(residual)
            cycle[2 | 8 | 16] *= factor
            cycle[4 | 8 | 16] *= factor
            for a in range(5, topics):
                cycle[1 << a] = 3
            yield tuple(cycle.get(mask, 0) for mask in range(1, 1 << topics))


def cone_from_solver(solver, target, rng, random_ties=False):
    cert = solver.certificate(target,
        action_selector=(lambda h, candidates: rng.choice(candidates)) if random_ties else None,
        continuation_selector=(lambda h, candidates: rng.choice(candidates)) if random_ties else None)
    return StrategyCone(solver.instance.topic_count, solver.instance.players, dict(cert.actions))


def serializable(result):
    if isinstance(result, Fraction):
        return str(result)
    if isinstance(result, dict):
        return {str(k): serializable(v) for k, v in result.items()}
    if isinstance(result, (list, tuple)):
        return [serializable(v) for v in result]
    return result


def self_test():
    """Exhaust every two-topic complete tree at m=2,3, with arbitrary weights.

    When both topics occur the outcome is optimal. When only A occurs, the
    last mover's comparison gives |B\\A| <= |A\\B|/m, hence OPT/W <= 1+1/m.
    This simple independently proved fact checks the LP implementation on the
    entire full-history policy class, rather than reproducing its internals.
    """
    summaries = []
    for players in (2, 3):
        histories = tuple(h for d in range(players) for h in product(range(2), repeat=d))
        count = feasible = duals = 0
        maximum = Fraction(0)
        for choices in product(range(2), repeat=len(histories)):
            count += 1
            cone = StrategyCone(2, players, dict(zip(histories, choices)))
            result = cone.optimize((0, 1))
            if not result["certified"]:
                if "infeasible" not in result["status"].lower():
                    raise AssertionError(result)
                continue
            feasible += 1
            duals += int(result["dual_optimal"])
            if not result["dual_optimal"]:
                raise AssertionError("small exhaustive cone missing an exact optimal dual")
            clones = integer_clones(result["values"])
            if not independently_verify(cone, clones):
                raise AssertionError("independent clone validation failed")
            maximum = max(maximum, result["value"])
        if maximum != Fraction(players + 1, players):
            raise AssertionError((players, maximum))
        summaries.append({"players": players, "complete_full_history_trees": count,
                          "nonzero_feasible_cones": feasible, "exact_optimal_duals": duals,
                          "maximum_ratio": maximum})
    print(json.dumps(serializable({"self_test": summaries})))


def verify_export(path):
    """Check saved LP certificates using only exact ordered-history arithmetic."""
    report = json.loads(path.read_text())
    topics, players = report["parameters"]["topics"], report["parameters"]["players"]
    primals = duals = 0
    for record in report["cone_proofs"]:
        actions = {tuple(item["history"]): item["action"] for item in record["actions"]}
        cone = StrategyCone(topics, players, actions)
        for proof in record["portfolio_proofs"]:
            clones = tuple(proof["integer_clones"])
            if not independently_verify(cone, clones):
                raise AssertionError("exported primal is not a complete SPE")
            welfare = dot(cone.welfare, clones)
            objective = coverage_row(topics, proof["portfolio"])
            value = dot(objective, clones) / welfare
            if value != Fraction(proof["objective_value"]):
                raise AssertionError("exported primal objective mismatch")
            primals += 1
            if proof["dual_bound"] is None:
                continue
            beta = Fraction(proof["dual_bound"])
            dual = [Fraction(0)] * len(cone.rows)
            for index, multiplier in proof["dual_support"]:
                if index not in range(len(dual)) or dual[index]:
                    raise AssertionError("invalid or repeated dual index")
                dual[index] = Fraction(multiplier)
            if any(mu < 0 for mu in dual):
                raise AssertionError("negative dual multiplier")
            for j, (w, v) in enumerate(zip(cone.welfare, objective)):
                if beta * w - sum(mu * row[j] for mu, row in zip(dual, cone.rows)) < v:
                    raise AssertionError("exported dual coefficient inequality failed")
            if beta != value:
                raise AssertionError("exported dual is not exactly optimal")
            duals += 1
    print(json.dumps({"verified_exported_primals": primals, "verified_exported_optimal_duals": duals}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--topics", type=int, default=5)
    parser.add_argument("--players", type=int, default=3)
    parser.add_argument("--cones", type=int, default=60)
    parser.add_argument("--seed", type=int, default=6102026)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--export-duals", action="store_true")
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    if args.verify:
        verify_export(args.verify)
        return
    if args.self_test:
        self_test()
        return
    if args.output and args.output.exists():
        raise FileExistsError("refusing to overwrite a frozen audit")
    rng = random.Random(args.seed)
    queue = list(structural_seeds(args.topics, args.players))
    seen_instances, seen_cones = set(), set()
    processed = exact_primals = exact_duals = 0
    best = None
    results = []
    cone_proofs = []
    started = time.monotonic()
    while queue and processed < args.cones:
        clones = queue.pop(0)
        if clones in seen_instances:
            continue
        seen_instances.add(clones)
        instance = instance_from_clones(args.topics, args.players, clones)
        solver = ExactSPESolver(instance)
        targets = sorted(solver.worst_outcomes())
        # Include all worst terminal supports, with one full-history tie variant.
        for target in targets[:8]:
            for variant in range(2):
                cone = cone_from_solver(solver, target, rng, random_ties=bool(variant))
                key = tuple(sorted(cone.actions.items()))
                if key in seen_cones:
                    continue
                seen_cones.add(key)
                processed += 1
                portfolio_proofs = []
                portfolios = combinations(range(args.topics), min(args.topics, args.players))
                for portfolio in portfolios:
                    result = cone.optimize(portfolio)
                    if not result["certified"]:
                        continue
                    exact_primals += 1
                    exact_duals += int(result["dual_optimal"])
                    endpoint = integer_clones(result["values"])
                    if not independently_verify(cone, endpoint):
                        raise AssertionError("independent full-history primal check failed")
                    candidate = instance_from_clones(args.topics, args.players, endpoint)
                    welfare = candidate.welfare(cone.root)
                    optimum = candidate.optimal_welfare()
                    ratio = Fraction(optimum, welfare)
                    if best is None or ratio > best["ratio"]:
                        best = {"ratio": ratio, "clones": endpoint, "root_counts": cone.root,
                                "optimum": optimum, "welfare": welfare,
                                "strategy": StrategyCertificate(cone.actions, cone.root).to_dict(),
                                "optimized_portfolio": result["support"],
                                "cone_objective": result["value"],
                                "dual_bound": result["dual_bound"]}
                        print(json.dumps(serializable({"cone": processed, "new_best": best["ratio"],
                                                       "clones": endpoint})), flush=True)
                    if endpoint not in seen_instances:
                        queue.append(endpoint)
                    if args.export_duals:
                        portfolio_proofs.append({"portfolio": result["support"], "integer_clones": endpoint,
                                                 "objective_value": result["value"],
                                                 "dual_bound": result["dual_bound"] if result["dual_optimal"] else None,
                                                 "dual_support": result["dual_support"] if result["dual_optimal"] else ()})
                    # A sparse deterministic perturbation can cross a face. The
                    # next strategy is independently reconstructed from the new
                    # integer input, never presumed unchanged after perturbing.
                    if rng.random() < .18:
                        perturbed = list(endpoint)
                        scale = rng.choice((2, 3, 5))
                        perturbed = [scale * x for x in perturbed]
                        mask = rng.randrange(1, 1 << args.topics)
                        perturbed[mask - 1] += rng.choice((1, 2))
                        queue.append(tuple(perturbed))
                results.append({"root_counts": cone.root, "constraint_rows": len(cone.rows)})
                if args.export_duals:
                    cone_proofs.append({"actions": StrategyCertificate(cone.actions, cone.root).to_dict()["actions"],
                                        "portfolio_proofs": portfolio_proofs})
                if processed >= args.cones:
                    break
            if processed >= args.cones:
                break
    report = {"scope": "fixed complete ordered-history SPE cones, targeted multiplicity LP and face crossings",
              "universal_bound_proved": False, "parameters": vars(args) | {"output": str(args.output) if args.output else None},
              "cones": processed, "distinct_inputs": len(seen_instances), "exact_primal_candidates": exact_primals,
              "exact_optimal_dual_certificates": exact_duals, "best": best,
              "stronger_bound": str(Fraction(2 * args.players - 1, args.players)),
              "beats_stronger_bound": bool(best and best["ratio"] > Fraction(2 * args.players - 1, args.players)),
              "refutes_half_coverage": bool(best and best["ratio"] > 2),
              "unrecovered_optimal_duals": exact_primals - exact_duals,
              "base_git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
              "audit_script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "elapsed_seconds": round(time.monotonic() - started, 3), "cone_metadata": results}
    if args.export_duals:
        report["cone_proofs"] = cone_proofs
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(serializable(report), indent=2) + "\n")
    print(json.dumps(serializable({k: v for k, v in report.items() if k not in ("best", "cone_metadata", "cone_proofs")})))


if __name__ == "__main__":
    main()
