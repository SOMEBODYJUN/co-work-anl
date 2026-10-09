"""New-model exact SPE tests; independent full ordered-strategy tiny oracle.

The oracle enumerates complete ordered-history strategy maps directly and checks
each supplied continuation using individual unit customers. It neither imports
nor reimplements the solver's outcome-set recurrence.
"""

from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from customer_attraction import (
    CustomerType, ExactSPESolver, Instance, StrategyCertificate,
    big_theme_lower_bound, verify_certificate,
)


def direct_ordered_strategy_paths(topic_count, players, preferences, prefix=()):
    """Enumerate every complete pure strategy of this tiny ordered-history tree."""
    histories = [prefix + tail for depth in range(len(prefix), players)
                 for tail in product(range(topic_count), repeat=depth - len(prefix))]
    by_depth = {depth: [history for history in histories if len(history) == depth]
                for depth in range(len(prefix), players)}

    def unit_payoff(topic, path):
        return sum((Fraction(1, sum(chosen in liked for chosen in path))
                    for liked in preferences if topic in liked), Fraction(0))

    reachable = set()
    for choices in product(range(topic_count), repeat=len(histories)):
        strategy = dict(zip(histories, choices))
        continuation = {prefix + tail: prefix + tail
                        for tail in product(range(topic_count), repeat=players - len(prefix))}
        valid = True
        for depth in range(players - 1, len(prefix) - 1, -1):
            for history in by_depth[depth]:
                chosen = strategy[history]
                actual = continuation[history + (chosen,)]
                current_payoff = unit_payoff(chosen, actual)
                if any(unit_payoff(action, continuation[history + (action,)]) > current_payoff
                       for action in range(topic_count)):
                    valid = False
                    break
                continuation[history] = actual
            if not valid:
                break
        if valid:
            reachable.add(continuation[prefix])
    return reachable


def path_counts(path, topic_count):
    return tuple(path.count(topic) for topic in range(topic_count))


class CustomerAttractionTests(unittest.TestCase):
    def test_two_topic_independent_complete_strategy_enumeration(self):
        signatures = (frozenset({0}), frozenset({1}), frozenset({0, 1}))
        # All 27 compressed customer inputs, with multiplicities 0, 1, 2.
        # Each m=3 oracle exhausts all 2^(1+2+4)=128 complete strategy maps.
        for multiplicities in product(range(3), repeat=3):
            customers = tuple(CustomerType(liked, multiplicity)
                              for liked, multiplicity in zip(signatures, multiplicities)
                              if multiplicity)
            clones = tuple(liked for liked, multiplicity in zip(signatures, multiplicities)
                           for _ in range(multiplicity))
            for players in (1, 2, 3):
                with self.subTest(multiplicities=multiplicities, players=players):
                    instance = Instance(("A", "B"), customers, players)
                    solver = ExactSPESolver(instance)
                    direct = direct_ordered_strategy_paths(2, players, clones)
                    self.assertEqual(solver.outcomes(),
                                     {path_counts(path, 2) for path in direct})
                    self.assertEqual(set(solver.ordered_outcomes()), direct)
                    for terminal in solver.outcomes():
                        report = verify_certificate(instance, solver.certificate(terminal))
                        report.assert_valid()
                        self.assertEqual(report.terminal_counts, terminal)
                    for prefix in ((0,), (1,)):
                        subpaths = direct_ordered_strategy_paths(2, players, clones, prefix)
                        self.assertEqual(solver.outcomes(path_counts(prefix, 2)),
                                         {path_counts(path, 2) for path in subpaths})

    def test_three_topic_two_player_all_binary_type_inputs(self):
        signatures = tuple(frozenset(combination) for size in (1, 2, 3)
                           for combination in combinations(range(3), size))
        # 128 different inputs; each independent oracle exhausts all 3^4=81
        # complete strategy maps, including every off-path action.
        for present in product((False, True), repeat=len(signatures)):
            clones = tuple(liked for liked, included in zip(signatures, present) if included)
            instance = Instance(("A", "B", "C"), tuple(CustomerType(liked) for liked in clones), 2)
            solver = ExactSPESolver(instance)
            direct = direct_ordered_strategy_paths(3, 2, clones)
            with self.subTest(present=present):
                self.assertEqual(solver.outcomes(), {path_counts(path, 3) for path in direct})
                self.assertEqual(set(solver.ordered_outcomes()), direct)
                verify_certificate(instance, solver.worst_certificate()).assert_valid()

    def test_empty_single_and_duplicate_theme_boundaries(self):
        instance = Instance.from_topic_sets([{0, 1}, {0, 1}, set()], 2,
                                            labels=("A", "A-copy", "empty"))
        solver = ExactSPESolver(instance)
        self.assertEqual(solver.outcomes(), {(2, 0, 0), (1, 1, 0), (0, 2, 0)})
        self.assertEqual(solver.minimum_welfare(), 2)
        self.assertEqual(instance.optimal_welfare(), 2)
        single = Instance(("only",), (CustomerType(frozenset({0}), 5),
                                      CustomerType(frozenset(), 7)), 4)
        self.assertEqual(single.topic_payoffs((4,)), (Fraction(5, 4),))
        self.assertEqual(single.welfare((4,)), 5)
        verify_certificate(single, ExactSPESolver(single).certificate()).assert_valid()
        empty = Instance(("empty-0", "empty-1"), (), 3)
        self.assertEqual(ExactSPESolver(empty).outcomes(),
                         {(3, 0), (2, 1), (1, 2), (0, 3)})
        self.assertEqual(ExactSPESolver(empty).inefficiency_ratio(), 1)
        zero = Instance((), (), 0)
        self.assertEqual(ExactSPESolver(zero).outcomes(), {()})
        verify_certificate(zero, ExactSPESolver(zero).certificate()).assert_valid()
        with self.assertRaises(ValueError):
            Instance((), (), 1)

    def test_big_theme_lower_bound_family_and_exact_certificates(self):
        for players in range(1, 7):
            with self.subTest(players=players):
                instance = big_theme_lower_bound(players)
                solver = ExactSPESolver(instance)
                all_big = (players,) + (0,) * (players - 1)
                self.assertIn(all_big, solver.outcomes())
                self.assertEqual(solver.minimum_welfare(), players)
                self.assertEqual(instance.optimal_welfare(), 2 * players - 1)
                self.assertEqual(solver.inefficiency_ratio(), Fraction(2 * players - 1, players))
                report = verify_certificate(instance, solver.certificate(all_big))
                report.assert_valid()
                self.assertEqual(report.terminal_history, (0,) * players)
                self.assertEqual(instance.player_payoffs(report.terminal_history),
                                 (Fraction(1),) * players)

    def test_same_counts_different_ordered_histories_choose_different_continuations(self):
        instance = Instance(("A", "B"), (CustomerType(frozenset({0, 1}), 6),), 3)
        solver = ExactSPESolver(instance)

        def history_dependent_tie(history, candidates):
            return candidates[-1] if history == (1, 0) else candidates[0]

        certificate = solver.certificate((3, 0), continuation_selector=history_dependent_tie)
        self.assertEqual(instance.counts((0, 1)), instance.counts((1, 0)))
        self.assertEqual(certificate.actions[(0, 1)], 1)
        self.assertEqual(certificate.actions[(1, 0)], 0)
        report = verify_certificate(instance, certificate)
        report.assert_valid()
        self.assertEqual(report.checked_histories, 7)
        self.assertEqual(report.checked_deviations, 7)
        # Each of all 8 ordered paths is realizable; certificate reconstruction
        # can request its complete order and independently verifies every tree.
        self.assertEqual(set(solver.ordered_outcomes()), set(product(range(2), repeat=3)))
        for path in solver.ordered_outcomes():
            self.assertEqual(verify_certificate(instance, solver.certificate(on_path=path)).terminal_history,
                             path)
        # The same phenomenon also occurs with disjoint singleton customers,
        # where total player payoffs differ. The actual sequence is (1/2,1,1/2).
        singletons = Instance.from_topic_sets([{0}, {1}], 3, labels=("A", "B"))
        certificate = ExactSPESolver(singletons).certificate(on_path=(0, 1, 0))
        verify_certificate(singletons, certificate).assert_valid()
        self.assertEqual(certificate.actions[(0, 1)], 0)
        self.assertEqual(certificate.actions[(1, 0)], 1)
        self.assertEqual(singletons.player_payoffs((0, 1, 0)),
                         (Fraction(1, 2), Fraction(1), Fraction(1, 2)))

    def test_sequential_spe_outcome_need_not_be_a_simultaneous_ne(self):
        instance = Instance.from_topic_sets([{0}, {0, 1}, {1, 2}], 3,
                                            labels=("A", "B", "C"))
        solver = ExactSPESolver(instance)
        path = (2, 0, 2)
        certificate = solver.certificate(on_path=path)
        report = verify_certificate(instance, certificate)
        report.assert_valid()
        self.assertEqual(report.terminal_history, path)
        self.assertEqual(instance.player_payoffs(path), (Fraction(1),) * 3)
        self.assertEqual(instance.player_payoffs((2, 1, 2))[1], Fraction(4, 3))
        # In the sequential strategy the last player reacts to the B deviation.
        self.assertNotEqual(certificate.actions[(2, 1)], 2)

    def test_clone_compression_exact_shares_and_welfare_conservation(self):
        compressed = Instance(("A", "B", "C"), (
            CustomerType(frozenset({0, 1}), 5), CustomerType(frozenset({1, 2}), 7),
            CustomerType(frozenset({2}), 3)), 4)
        expanded = Instance(compressed.topics, tuple(
            CustomerType(customer.topics) for customer in compressed.customers
            for _ in range(customer.multiplicity)), compressed.players)
        self.assertEqual(ExactSPESolver(compressed).outcomes(), ExactSPESolver(expanded).outcomes())
        for path in product(range(3), repeat=4):
            counts = compressed.counts(path)
            self.assertEqual(compressed.player_payoffs(path), expanded.player_payoffs(path))
            self.assertEqual(sum(compressed.player_payoffs(path)), compressed.welfare(counts))
        huge = Instance(("A", "B"), (CustomerType(frozenset({0, 1}), 1 << 1000),), 3)
        self.assertEqual(huge.player_payoffs((0, 1, 0)), (Fraction(1 << 1000, 3),) * 3)

    def test_two_player_five_theme_residual_bound_counterexample(self):
        root = Path(__file__).resolve().parents[1]
        instance = Instance.from_dict(json.loads(
            (root / "examples/customer_attraction/residual_counterexample.json").read_text()))
        certificate = StrategyCertificate.from_dict(json.loads(
            (root / "evidence/certificates/customer_attraction/residual_counterexample.json").read_text()))
        report = verify_certificate(instance, certificate)
        report.assert_valid()
        self.assertEqual(report.checked_histories, 6)
        self.assertEqual(report.checked_deviations, 24)
        self.assertEqual(report.terminal_history, (0, 1))
        self.assertEqual(instance.player_payoffs(report.terminal_history), (Fraction(4), Fraction(5)))
        self.assertIn(report.terminal_counts, ExactSPESolver(instance).outcomes())
        counts = report.terminal_counts
        residual = max(sum(customer.multiplicity for customer in instance.customers
                           if topic in customer.topics
                           and not any(counts[accepted] for accepted in customer.topics))
                       for topic in range(instance.topic_count))
        self.assertEqual(residual, 5)
        self.assertLess(min(instance.player_payoffs(report.terminal_history)), residual)
        self.assertLess(instance.welfare(counts), instance.players * residual)
        self.assertEqual(instance.welfare(counts), 9)
        self.assertEqual(instance.optimal_welfare(), 10)
        self.assertGreaterEqual(2 * instance.welfare(counts), instance.optimal_welfare())

    def test_certificate_roundtrip_and_definition_level_rejection(self):
        instance = big_theme_lower_bound(3)
        certificate = ExactSPESolver(instance).worst_certificate()
        restored = StrategyCertificate.from_dict(json.loads(json.dumps(certificate.to_dict())))
        self.assertEqual(restored.actions, certificate.actions)
        verify_certificate(instance, restored).assert_valid()
        missing = dict(certificate.actions)
        del missing[(0, 1)]
        self.assertFalse(verify_certificate(instance, StrategyCertificate(missing, certificate.terminal_counts)).valid)
        extra = dict(certificate.actions)
        extra[(0, 0, 0)] = 0
        self.assertFalse(verify_certificate(instance, StrategyCertificate(extra, certificate.terminal_counts)).valid)
        report = verify_certificate(instance, StrategyCertificate(certificate.actions, (0, 0, 3)))
        self.assertFalse(report.valid)
        self.assertIn("declared terminal counts", report.errors[0])
        one = Instance(("A", "B"), (CustomerType(frozenset({0})),
                                     CustomerType(frozenset({1}), 3)), 1)
        wrong = verify_certificate(one, StrategyCertificate({(): 0}, (1, 0)))
        self.assertFalse(wrong.valid)
        self.assertEqual(len(wrong.violations), 1)
        self.assertEqual(wrong.violations[0].deviating_payoff, 3)
        with self.assertRaises(ValueError):
            wrong.assert_valid()

    def test_invalid_inputs_and_unrealizable_requested_order(self):
        for constructor in (
            lambda: CustomerType(frozenset({True})),
            lambda: CustomerType(frozenset({0}), 0),
            lambda: CustomerType(frozenset({0}), Fraction(1, 2)),
            lambda: Instance(("A", "A"), (), 2),
            lambda: Instance(("A",), (CustomerType(frozenset({1})),), 2),
            lambda: Instance(("A",), (), True),
        ):
            with self.assertRaises(ValueError):
                constructor()
        instance = Instance(("A", "B"), (CustomerType(frozenset({0}), 2),), 2)
        solver = ExactSPESolver(instance)
        for counts in ((0,), (3, 0), (-1, 2), (True, 0)):
            with self.assertRaises(ValueError):
                solver.outcomes(counts)
        with self.assertRaises(ValueError):
            solver.certificate((0, 2))
        with self.assertRaises(ValueError):
            solver.certificate((2, 0), on_path=(0, 1))
        with self.assertRaises(ValueError):
            solver.certificate(action_selector=lambda _history, _actions: 1)
        with self.assertRaises(ValueError):
            solver.threshold((2, 0))

    def test_cli_exact_report_certificate_verify_and_preserve_output(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(prefix="customer-attraction-test-") as directory:
            source = Path(directory) / "instance.json"
            target = Path(directory) / "result.json"
            source.write_text(json.dumps(big_theme_lower_bound(2).to_dict()))
            command = [sys.executable, "-m", "customer_attraction", str(source),
                       "--certificate", "--output", str(target)]
            completed = subprocess.run(command, cwd=root, text=True, capture_output=True)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            original = target.read_bytes()
            report = json.loads(original)
            self.assertEqual(report["inefficiency_ratio"], "3/2")
            verified = subprocess.run([sys.executable, "-m", "customer_attraction", str(source),
                                       "--verify", str(target)], cwd=root,
                                      text=True, capture_output=True)
            self.assertEqual(verified.returncode, 0, verified.stderr)
            self.assertTrue(json.loads(verified.stdout)["valid"])
            repeated = subprocess.run(command, cwd=root, text=True, capture_output=True)
            self.assertNotEqual(repeated.returncode, 0)
            self.assertIn("Refusing to overwrite", repeated.stderr)
            self.assertEqual(target.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
