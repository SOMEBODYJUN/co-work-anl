"""Finite exact attacks for the sequential shared-catalog attraction model.

This is independent of customer_attraction's canonical Fraction solver. Integer
payoffs are scaled by lcm(1,...,m). All pure history-dependent SPE outcomes are
retained; no global tie selector is imposed. Multiplicities are unit clones,
not indivisible strategic customer weights. Successful searches prove no
universal theorem. Frozen output is never overwritten.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
from functools import lru_cache
import hashlib
from itertools import permutations, product
import json
from math import lcm
from pathlib import Path
import random
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


def compositions(total: int, size: int):
    if size == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for rest in compositions(total - first, size - 1):
            yield (first,) + rest


@lru_cache(None)
def geometry(k: int, m: int):
    levels = [tuple(compositions(j, k)) for j in range(m + 1)]
    leaves = levels[-1]
    leaf_ids = {q: i for i, q in enumerate(leaves)}
    mask_topics = [tuple(a for a in range(k) if mask & (1 << a))
                   for mask in range(1, 1 << k)]
    denoms = [[sum(q[a] for a in topics) for topics in mask_topics]
              for q in leaves]
    children = {c: tuple(tuple(x + (a == b) for b, x in enumerate(c))
                         for a in range(k))
                for level in levels[:-1] for c in level}
    return levels, leaves, leaf_ids, mask_topics, denoms, children


def exact_outcomes(k: int, m: int, weights: tuple[int, ...]):
    """Return all root outcomes and terminal payoff/welfare data in integers.

    A chosen branch's terminal payoff must beat every alternative branch's
    minimum achievable SPE payoff. Those minima can be prescribed independently
    at different ordered histories. Symmetry makes achievable outcome sets
    depend only on prefix counts, without restricting the full strategy.
    """
    assert len(weights) == (1 << k) - 1
    assert all(type(w) is int and w >= 0 for w in weights)
    levels, leaves, leaf_ids, mask_topics, denoms, children = geometry(k, m)
    scale = lcm(*range(1, m + 1))
    payoffs = [[0] * len(leaves) for _ in range(k)]
    welfare = [0] * len(leaves)
    residual = [0] * len(leaves)
    for j, ds in enumerate(denoms):
        marginal = [0] * k
        for w, topics, d in zip(weights, mask_topics, ds):
            if not w:
                continue
            if d:
                welfare[j] += w
                share = w * (scale // d)
                for a in topics:
                    payoffs[a][j] += share
            else:
                for a in topics:
                    marginal[a] += w
        residual[j] = max(marginal)
    possible = {q: frozenset((j,)) for q, j in leaf_ids.items()}
    for level in reversed(levels[:-1]):
        for c in level:
            branches = [possible[child] for child in children[c]]
            threshold = max(min(payoffs[a][j] for j in js)
                            for a, js in enumerate(branches))
            allowed = frozenset(j for a, js in enumerate(branches)
                                for j in js if payoffs[a][j] >= threshold)
            assert allowed
            possible[c] = allowed
    ids = possible[(0,) * k]
    optimum = max(welfare)
    worst = min(welfare[j] for j in ids)
    residual_bad = [(j, a) for j in ids for a, q_a in enumerate(leaves[j])
                    if q_a and payoffs[a][j] < scale * residual[j]]
    return {"outcome_ids": ids, "leaves": leaves, "payoffs": payoffs,
            "welfare": welfare, "residual": residual, "scale": scale,
            "optimum": optimum, "worst": worst,
            "residual_bad": residual_bad}


def instance_record(k: int, m: int, weights: tuple[int, ...], data: dict):
    worst_ids = sorted(j for j in data["outcome_ids"]
                       if data["welfare"][j] == data["worst"])
    record = {"catalog_size": k, "players": m,
              "type_multiplicities_by_mask_1_to_2k_minus_1": list(weights),
              "customer_count": sum(weights), "opt_m": data["optimum"],
              "minimum_spe_welfare": data["worst"],
              "minimum_ratio": str(Fraction(data["worst"], data["optimum"]))
                               if data["optimum"] else "1",
              "all_spe_terminal_counts": [list(data["leaves"][j])
                                          for j in sorted(data["outcome_ids"])],
              "worst_spe_terminal_counts": [list(data["leaves"][j])
                                            for j in worst_ids]}
    if data["residual_bad"]:
        j, a = min(data["residual_bad"],
                   key=lambda pair: (sum(weights), data["leaves"][pair[0]], pair[1]))
        record["residual_lemma_counterexample"] = {
            "terminal_counts": list(data["leaves"][j]), "occupied_action": a,
            "own_payoff": str(Fraction(data["payoffs"][a][j], data["scale"])),
            "maximum_uncovered_action_size": data["residual"][j]}
    return record


def orbit_representatives(k: int, alphabet: int):
    """Exactly one vector per action-permutation orbit; no model reduction."""
    maps = []
    for perm in permutations(range(k)):
        maps.append(tuple(sum(1 << perm[a] for a in range(k) if mask & (1 << a)) - 1
                          for mask in range(1, 1 << k)))
    seen = set()
    for weights in product(range(alphabet), repeat=(1 << k) - 1):
        if weights in seen:
            continue
        yield weights
        for mapping in maps:
            transformed = [0] * len(weights)
            for old, new in enumerate(mapping):
                transformed[new] = weights[old]
            seen.add(tuple(transformed))


def canonical_confirm(record: dict):
    """Cross-check against a separately implemented Fraction recurrence."""
    from customer_attraction import CustomerType, Instance, ExactSPESolver
    k, m = record["catalog_size"], record["players"]
    weights = record["type_multiplicities_by_mask_1_to_2k_minus_1"]
    customers = tuple(CustomerType(frozenset(a for a in range(k) if mask & (1 << a)), w)
                      for mask, w in enumerate(weights, 1) if w)
    instance = Instance(tuple(chr(65 + a) for a in range(k)), customers, m)
    solver = ExactSPESolver(instance)
    actual = solver.outcomes()
    expected = frozenset(tuple(q) for q in record["all_spe_terminal_counts"])
    assert actual == expected, (actual, expected, record)
    assert solver.minimum_welfare() == record["minimum_spe_welfare"]
    if "residual_lemma_counterexample" in record:
        bad = record["residual_lemma_counterexample"]
        counts, action = tuple(bad["terminal_counts"]), bad["occupied_action"]
        assert instance.topic_payoff(action, counts) == Fraction(bad["own_payoff"])
        assert instance.topic_payoff(action, counts) < bad["maximum_uncovered_action_size"]
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--seed", type=int, default=20261009)
    parser.add_argument("--random-per-size", type=int, default=600)
    parser.add_argument("--skip-tiny", action="store_true")
    parser.add_argument("--confirm", action="store_true")
    parser.add_argument("--extended", action="store_true")
    args = parser.parse_args()
    if args.output and args.output.exists():
        raise FileExistsError("frozen evidence must not be overwritten")
    started = time.monotonic()
    rng = random.Random(args.seed)
    best = None
    best_ratio = Fraction(1)
    residual_counterexamples = []
    stages = []
    confirmations = []
    digest = hashlib.sha256()

    def run_stage(name, cases, parameters):
        nonlocal best, best_ratio
        count = violations = residual_violations = 0
        stage_best = None
        stage_ratio = Fraction(1)
        stage_started = time.monotonic()
        for k, m, weights in cases:
            data = exact_outcomes(k, m, weights)
            count += 1
            ratio = Fraction(data["worst"], data["optimum"]) if data["optimum"] else Fraction(1)
            digest.update(json.dumps([k, m, weights, sorted(data["outcome_ids"])],
                                     separators=(",", ":")).encode())
            if stage_best is None or ratio < stage_ratio:
                stage_ratio = ratio
                stage_best = instance_record(k, m, weights, data)
            if best is None or ratio < best_ratio:
                best_ratio = ratio
                best = instance_record(k, m, weights, data)
                print(json.dumps({"new_minimum_ratio": str(ratio), "stage": name,
                                  "case": count, "record": best}), flush=True)
            if 2 * data["worst"] < data["optimum"]:
                violations += 1
            if data["residual_bad"]:
                residual_violations += 1
                candidate = instance_record(k, m, weights, data)
                if not residual_counterexamples or sum(weights) < residual_counterexamples[0]["customer_count"]:
                    residual_counterexamples.insert(0, candidate)
                    del residual_counterexamples[10:]
                    print(json.dumps({"residual_lemma_counterexample": candidate}), flush=True)
        stage = {"name": name, "parameters": parameters, "instance_count": count,
                 "welfare_half_violations": violations,
                 "residual_lemma_violating_instances": residual_violations,
                 "minimum_ratio": str(stage_ratio), "worst_instance": stage_best,
                 "elapsed_seconds": round(time.monotonic() - stage_started, 3)}
        stages.append(stage)
        if args.confirm and stage_best:
            canonical_confirm(stage_best)
            confirmations.append({"stage": name, "kind": "worst_instance",
                                  "status": "all_outcome_sets_equal"})
        print(json.dumps({"stage_completed": name, "count": count,
                          "minimum_ratio": str(stage_ratio),
                          "residual_violations": residual_violations}), flush=True)

    if not args.skip_tiny:
        for k, alphabet in ((3, 3), (4, 2)):
            cases = ((k, m, weights) for weights in orbit_representatives(k, alphabet)
                     for m in (3, 4, 5))
            run_stage(f"exhaustive_k{k}_multiplicity_0_to_{alphabet-1}", cases,
                      {"catalog_size": k, "players": [3, 4, 5],
                       "multiplicity_alphabet": list(range(alphabet)),
                       "quotient": "all action permutation orbits exactly once",
                       "covered_types": list(range(1, 1 << k))})

    def random_cases(k):
        for i in range(args.random_per_size):
            m = (3, 4, 5)[i % 3]
            mode = i % 4
            if mode == 0:
                weights = tuple(rng.randrange(21) if rng.random() < .30 else 0
                                for _ in range((1 << k) - 1))
            elif mode == 1:
                weights = tuple(rng.choice((0, 0, 0, 1, 2, 3, 5, 8, 13, 21, 34))
                                for _ in range((1 << k) - 1))
            elif mode == 2:
                weights = tuple(rng.randrange(1, 31) if mask.bit_count() <= 2 else 0
                                for mask in range(1, 1 << k))
            else:
                weights = tuple(rng.randrange(1, 51) if mask.bit_count() in (1, k - 1) else 0
                                for mask in range(1, 1 << k))
            yield k, m, weights

    for k in (4, 5, 6):
        run_stage(f"seeded_random_k{k}", random_cases(k),
                  {"seed": args.seed, "catalog_size": k,
                   "samples": args.random_per_size,
                   "players_cycle": [3, 4, 5],
                   "modes": ["independent 30% nonzero U{0..20}",
                             "U{0,0,0,1,2,3,5,8,13,21,34}",
                             "singleton/pair masks U{1..30}",
                             "singleton/(k-1)-masks U{1..50}"]})

    if args.extended:
        extended_rng = random.Random(args.seed * 10 + 1)
        for k, m, sample_count in ((3, 8, 4000), (4, 6, 4000), (4, 8, 4000),
                                    (5, 6, 3000), (6, 6, 1500), (7, 5, 1000), (7, 6, 300)):
            def extended_cases():
                for i in range(sample_count):
                    density = (.09, .2, .5)[i % 3]
                    weights = tuple(extended_rng.randrange(101)
                                    if extended_rng.random() < density else 0
                                    for _ in range((1 << k) - 1))
                    yield k, m, weights
            run_stage(f"extended_residual_k{k}_m{m}", extended_cases(),
                      {"seed": args.seed * 10 + 1, "catalog_size": k,
                       "players": m, "samples": sample_count,
                       "nonzero_densities_cycle": [.09, .2, .5],
                       "conditional_multiplicity_alphabet": [0, 100]})

    # A classic concentration family: one large private action, disjoint small
    # private actions. This is deliberately checked rather than presumed to
    # remain sequentially bad.
    structured = []
    for m in (3, 4, 5):
        for small in (1, 2, 3, 6, 12):
            k = m + 1
            for delta in (-2, -1, 0, 1, 2):
                large = max(1, m * small + delta)
                weights = tuple(large if mask == 1 else small if mask.bit_count() == 1 else 0
                                for mask in range(1, 1 << k))
                structured.append((k, m, weights))
    run_stage("large_vs_disjoint_small", structured,
              {"players": [3, 4, 5], "catalog_size": "m+1",
               "small_size": [1, 2, 3, 6, 12], "large_size": "max(1,m*small+delta)",
               "delta": [-2, -1, 0, 1, 2]})
    if args.confirm and residual_counterexamples:
        canonical_confirm(residual_counterexamples[0])
        confirmations.append({"kind": "smallest_retained_residual_counterexample",
                              "status": "all_outcome_sets_and_payoff_equal"})
    source_version = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    script_digest = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result = {"scope": "finite shared-catalog sequential customer-attraction search",
              "status": "completed", "universal_claim_proved": False,
              "equilibrium": "all pure history-dependent SPE terminal outcomes",
              "arithmetic": "integer payoffs scaled by lcm(1,...,m); rational ratios",
              "unit_customer_semantics": "nonnegative integer type multiplicity equals that many unit clones",
              "recurrence": "E(c)=union_a {q in E(c+e_a): U_a(q)>=max_b min_r_in_E(c+e_b) U_b(r)}",
              "parameters": vars(args) | {"output": str(args.output) if args.output else None},
              "seed": args.seed, "base_git_commit": source_version,
              "audit_script_sha256": script_digest,
              "ordered_instance_outcomes_sha256": digest.hexdigest(),
              "total_instance_count": sum(s["instance_count"] for s in stages),
              "minimum_ratio": str(best_ratio), "worst_instance": best,
              "residual_lemma_counterexamples": residual_counterexamples,
              "canonical_independent_crosschecks": confirmations,
              "stages": stages,
              "elapsed_seconds": round(time.monotonic() - started, 3)}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in
                      ("stages", "worst_instance", "residual_lemma_counterexamples")}))


if __name__ == "__main__":
    main()
