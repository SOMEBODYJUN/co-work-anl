"""Exact regression of history-aware duplicate-coverage quotienting.

Run from the repository root. The proof is in duplicate_coverage_quotient.md;
this script checks finite cases and never treats them as a universal proof.
"""
from __future__ import annotations

from itertools import product
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT))
from customer_attraction import (  # noqa: E402
    CustomerType, ExactSPESolver, Instance, StrategyCertificate, verify_certificate,
)


def quotient(instance):
    signatures = [tuple(i for i, c in enumerate(instance.customers) if a in c.topics)
                  for a in range(instance.topic_count)]
    unique = list(dict.fromkeys(signatures))
    classes = tuple(unique.index(s) for s in signatures)
    groups = tuple(tuple(a for a, c in enumerate(classes) if c == j)
                   for j in range(len(unique)))
    target = Instance(tuple(f"class-{j}" for j in range(len(groups))),
                      tuple(CustomerType(frozenset(classes[a] for a in c.topics),
                                         c.multiplicity) for c in instance.customers),
                      instance.players)
    return target, classes, groups


def collapse(instance, certificate):
    target, classes, groups = quotient(instance)
    actions, lifts = {}, {}

    def build(history, lift):
        lifts[history] = lift
        if len(history) == instance.players:
            return
        prescribed = certificate.actions[lift]
        chosen_class = classes[prescribed]
        actions[history] = chosen_class
        for c, group in enumerate(groups):
            representative = prescribed if c == chosen_class else group[0]
            build(history + (c,), lift + (representative,))

    build((), ())
    path = ()
    while len(path) < instance.players:
        path += (actions[path],)
    result = StrategyCertificate(actions, target.counts(path, terminal=True))
    return target, result, lifts


def expand(instance, certificate):
    target, classes, groups = quotient(instance)
    actions = {}
    for depth in range(instance.players):
        for history in product(range(instance.topic_count), repeat=depth):
            projected = tuple(classes[a] for a in history)
            actions[history] = groups[certificate.actions[projected]][0]
    path = ()
    while len(path) < instance.players:
        path += (actions[path],)
    return StrategyCertificate(actions, instance.counts(path, terminal=True))


def run():
    rng = random.Random(10021)
    cases = [([set(), set()], 0), ([set(), set(), set()], 4),
             ([{0, 1}, {0, 1}, set()], 1),
             ([{0}, {0}, {1}, {1}, set()], 3),
             ([{0, 1}, {0, 1}, {1, 2}, {1, 2}, {2, 3}], 3),
             ([{0, 1}, {2, 3}, {1, 2, 3}, {2, 3}], 4)]
    report = []
    for coverage, players in cases:
        instance = Instance.from_topic_sets(coverage, players)
        target, classes, _ = quotient(instance)
        solver, reduced_solver = ExactSPESolver(instance), ExactSPESolver(target)
        original_paths = set(solver.ordered_outcomes())
        reduced_paths = set(reduced_solver.ordered_outcomes())
        projected_paths = {tuple(classes[a] for a in path) for path in original_paths}
        assert projected_paths == reduced_paths
        assert instance.optimal_welfare() == target.optimal_welfare()
        checked_collapse, checked_expand = 0, 0
        for path in sorted(original_paths):
            cert = solver.certificate(on_path=path,
                                      continuation_selector=lambda h, cs: rng.choice(cs))
            source_report = verify_certificate(instance, cert)
            source_report.assert_valid()
            reduced, collapsed, lifts = collapse(instance, cert)
            collapsed_report = verify_certificate(reduced, collapsed)
            collapsed_report.assert_valid()
            projected = tuple(classes[a] for a in source_report.terminal_history)
            assert collapsed_report.terminal_history == projected
            assert instance.player_payoffs(path) == reduced.player_payoffs(projected)
            assert instance.welfare(cert.terminal_counts) == reduced.welfare(collapsed.terminal_counts)
            # Check the simulation at every quotient history, including deviations.
            for history, lift in lifts.items():
                original, quotient_path = lift, history
                while len(original) < players:
                    original += (cert.actions[original],)
                while len(quotient_path) < players:
                    quotient_path += (collapsed.actions[quotient_path],)
                assert tuple(classes[a] for a in original) == quotient_path
                assert instance.player_payoffs(original) == reduced.player_payoffs(quotient_path)
            checked_collapse += 1
        for path in sorted(reduced_paths):
            cert = reduced_solver.certificate(on_path=path)
            expanded = expand(instance, cert)
            expanded_report = verify_certificate(instance, expanded)
            expanded_report.assert_valid()
            assert tuple(classes[a] for a in expanded_report.terminal_history) == path
            checked_expand += 1
        report.append(dict(players=players, labels=instance.topic_count,
                           coverage_classes=target.topic_count,
                           original_paths=len(original_paths), reduced_paths=len(reduced_paths),
                           collapse_certificates=checked_collapse,
                           expand_certificates=checked_expand))
    return dict(status="passed", seed=10021, cases=report,
                scope="Finite regression only; universal claim is proved in the companion note.")


if __name__ == "__main__":
    result = run()
    if len(sys.argv) > 1:
        output = Path(sys.argv[1])
        with output.open("x") as stream:
            json.dump(result, stream, indent=2)
            stream.write("\n")
    print(json.dumps(result, indent=2))
