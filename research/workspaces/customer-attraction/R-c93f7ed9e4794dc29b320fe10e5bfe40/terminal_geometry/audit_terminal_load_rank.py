"""Exact finite audit of terminal_load_rank.md; not a general SPE proof."""

from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction.model import Instance, CustomerType
from customer_attraction.exact import ExactSPESolver
from customer_attraction.certificate import verify_certificate


def harmonic(n):
    return sum((Q(1, r) for r in range(1, n + 1)), Q())


def phi(m, c):
    return Q(c - 1, m) + harmonic(m) - harmonic(c - 1)


def tail(m, membership):
    return sum((Q(1, sum(membership[:i]) + m - i)
                for i in range(m)), Q())


def audit_customer_patterns():
    patterns = 0
    minima = []
    for m in range(1, 13):
        found = {}
        for prior in product((0, 1), repeat=m - 1):
            membership = prior + (1,)
            c = sum(membership)
            value = tail(m, membership)
            found[c] = min(found.get(c, value), value)
            assert value >= phi(m, c)
            assert phi(m, c) >= harmonic(m) / c
            assert Q(1) <= phi(m, c) <= Q(m, c)
            patterns += 1
        for c, value in found.items():
            early = (1,) * (c - 1) + (0,) * (m - c) + (1,)
            assert value == phi(m, c) == tail(m, early)
        minima.append({"m": m, "phi_by_load": {str(c): str(found[c]) for c in found}})
    return patterns, minima


def audit_credit():
    cases = 0
    for m in range(1, 13):
        for h in range(m):
            for b, o in product((0, 1), repeat=2):
                p = int(h > 0)
                u = Q(b, h + 1)
                original = Q(o * p, h + 1) + p * (1 - o) + b * (1 - p) - u
                expanded = (Q(p * (1 - b) * o, h + 1)
                            + p * (1 - o) * (1 - b)
                            + Q(p * b * (1 - o) * h, h + 1))
                assert original == expanded
                assert original >= Q(p * (1 - b), m)
                cases += 1
    return cases


def optimal_support(instance):
    optimum = instance.optimal_welfare()
    for k in range(1, min(instance.players, instance.topic_count) + 1):
        for support in combinations(range(instance.topic_count), k):
            if sum(t.multiplicity for t in instance.customers if t.topics.intersection(support)) == optimum:
                return support
    raise AssertionError("no optimal support")


def audit_spe():
    # Catalogs include disjoint themes, intersecting maximal themes, strict
    # subsets, an empty label and duplicate-coverage labels; unit multiplicities.
    signatures = [
        [{0}, {1}],
        [{0}, {1}, {2}],
        [{0, 1}, {0, 2}, {1, 2}],
        [{0, 1, 3}, {0, 2}, {1, 2}, {0}],
    ]
    games = paths = certs = histories = deviations = 0
    tight_examples = []
    for m in range(1, 6):
        for family_index, family in enumerate(signatures):
            topic_count = max(max(s) for s in family) + 2  # One empty action.
            for weight_seed in range(1, 4):
                types = tuple(CustomerType(frozenset(s), 1 + (j * weight_seed) % 4)
                              for j, s in enumerate(family))
                instance = Instance(tuple(f"T{j}" for j in range(topic_count)), types, m)
                solver = ExactSPESolver(instance)
                support = optimal_support(instance)
                k = len(support)
                optimum = instance.optimal_welfare()
                for history in solver.ordered_outcomes():
                    payoffs = instance.player_payoffs(history)
                    u = payoffs[-1]
                    welfare = instance.welfare(instance.counts(history))
                    target = history[-1]
                    phis = credit = bsize = 0
                    qtotal = Q()
                    for i in range(m):
                        raw = sum((Q(t.multiplicity,
                                     sum(a in t.topics for a in history[:i]) + m - i)
                                   for t in types if target in t.topics), Q())
                        assert payoffs[i] >= raw >= u / (m - i)
                        qtotal += raw
                    for t in types:
                        h = sum(a in t.topics for a in history[:-1])
                        b = int(target in t.topics)
                        o = int(bool(t.topics.intersection(support)))
                        p = int(h > 0)
                        if b:
                            bsize += t.multiplicity
                            phis += t.multiplicity * phi(m, h + 1)
                        credit += t.multiplicity * (
                            Q(p * (1 - b) * o, h + 1)
                            + p * (1 - o) * (1 - b)
                            + Q(p * b * (1 - o) * h, h + 1))
                    assert welfare >= qtotal >= phis >= harmonic(m) * u
                    assert optimum - welfare <= (k - 1) * u - credit
                    assert credit >= Q(welfare - bsize, m)
                    if k - 1 <= harmonic(m):
                        assert optimum <= 2 * welfare
                    if welfare == phis:
                        tight_examples.append([m, family_index, weight_seed, list(history), str(u)])
                    # Reconstruct complete trees on one path per count state;
                    # their verifier evaluates every off-path comparison.
                    if paths % 29 == 0:
                        checked = verify_certificate(instance, solver.certificate(on_path=history))
                        checked.assert_valid()
                        certs += 1
                        histories += checked.checked_histories
                        deviations += checked.checked_deviations
                    paths += 1
                games += 1
    return {"games": games, "ordered_spe_paths": paths,
            "full_certificates": certs, "all_history_checks": histories,
            "all_deviation_checks": deviations,
            "load_floor_tight_examples_first_12": tight_examples[:12]}


def main():
    patterns, minima = audit_customer_patterns()
    report = {"status": "passed", "scope": "finite exact audit, not general theorem proof",
              "customer_patterns": patterns, "per_load_minima": minima,
              "credit_type_checks": audit_credit(), "spe_checks": audit_spe()}
    path = Path(__file__).with_name("load_rank_audit.json")
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({key: value for key, value in report.items() if key != "per_load_minima"},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
