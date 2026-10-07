"""Fast exact regressions for equal-weight flow and its independent oracle.

Run: python3 -m tests.test_equal_light_flow
Larger fixed-grid evidence: tests/audits/kfac_equal_light_flow.py.
"""
from fractions import Fraction as F
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from multi_facility_spe.equal_light_flow import equal_weight_box_ne
from tests.audits.kfac_equal_light_flow import (
    _rational, audit_instance, enumerate_minimizers, invalid_cases,
    rerouting_fixture, seeded_cases, special_cases,
)


ROOT = Path(__file__).resolve().parents[1]


class EqualLightFlowTests(unittest.TestCase):
    def test_empty_customers_including_no_sites(self):
        for q, c in (([], []), ([1], ['1/2']), ([9, 2, 1], ['0', '1', '2/3'])):
            with self.subTest(q=q):
                oracle, result = audit_instance(dict(q=q, c=c, w=[], A=[]))
                self.assertEqual(result['assignment'], [])
                self.assertEqual(result['X'], c)
                self.assertEqual(result['objective'], '0')
                self.assertEqual(result['augmentations'], 0)
                self.assertEqual(result['reverse_assignment_traversals'], 0)
                self.assertEqual(result['max_assignment_reroutes_per_augmentation'], 0)
                self.assertEqual(oracle['assignment_count'], 1)

    def test_single_site_keeps_initial_slack_with_negative_base(self):
        obj = dict(q=[11], c=['1/7'], w=['2/3'] * 8, A=[[0]] * 8)
        oracle, result = audit_instance(obj)
        self.assertEqual(result['X'], ['1/7'])
        self.assertEqual(result['assignment'], [0] * 8)
        self.assertLess(oracle['minimum'], 0)

    def test_every_tied_global_minimum_is_checked(self):
        obj = dict(q=[1, 1], c=['1', '0'], w=['1/2'] * 2, A=[[0, 1]] * 2)
        oracle, _result = audit_instance(obj)
        self.assertEqual(set(oracle['minimizers']), {(0, 1), (1, 0)})
        self.assertEqual(oracle['assignment_count'], 4)
        self.assertEqual(oracle['original_options_checked'], 8)

    def test_unconstrained_oracle_includes_outside_box_assignments(self):
        obj = dict(q=[1, 1], c=['0', '0'], w=['2/3'] * 2, A=[[0, 1]] * 2)
        oracle, result = audit_instance(obj)
        self.assertEqual(oracle['assignment_count'], 4)
        self.assertEqual(oracle['outside_box_assignment_count'], 3)
        self.assertEqual(result['assignment'], [0, 0])

    def test_two_reverse_reroutes_in_one_augmentation(self):
        _oracle, result = audit_instance(rerouting_fixture())
        self.assertEqual(result['assignment'], [1, 2, 0])
        self.assertEqual(result['objective'], '0')
        self.assertEqual(result['augmentations'], 3)
        self.assertGreaterEqual(result['reverse_assignment_traversals'], 2)
        self.assertGreaterEqual(result['max_assignment_reroutes_per_augmentation'], 2)

    def test_special_exact_inputs(self):
        for name, obj in special_cases():
            with self.subTest(name=name):
                audit_instance(obj)

    def test_equivalent_exact_representations_and_duplicate_menus(self):
        obj = dict(q=(3, 1), c=(F(3, 4), 0), w=(F(1, 2), '0.5'),
                   A=((1, 0, 1), (0, 1, 0)))
        audit_instance(obj)

    def test_binary_multiplicity_beyond_decimal_conversion_limit(self):
        # More than 6,000 decimal digits: a direct str(Fraction) fails under
        # Python's default safety limit.  The constructor must not expand q
        # facilities or change that process-wide conversion setting.
        multiplicity = 1 << 20000
        before = sys.get_int_max_str_digits() if hasattr(sys, 'get_int_max_str_digits') else None
        result = equal_weight_box_ne([multiplicity], ['1/2'], ['1/3'], [[0]])
        self.assertEqual(result['assignment'], [0])
        self.assertEqual(result['X'], ['1/2'])
        self.assertGreater(len(result['objective']), 6000)
        self.assertEqual(_rational(result['objective']), F(1, 6 * multiplicity))
        self.assertEqual(result['augmentations'], 1)
        if before is not None:
            self.assertEqual(sys.get_int_max_str_digits(), before)

    def test_exact_rational_string_beyond_decimal_conversion_limit(self):
        weight = '1/' + '9' * 5000
        self.assertEqual(_rational(weight), F(1, 10 ** 5000 - 1))
        audit_instance(dict(q=[2, 1], c=['1/2', '0'], w=[weight] * 2,
                            A=[[0, 1], [0, 1]]))

    def test_invalid_and_unequal_inputs_rejected(self):
        for name, obj in invalid_cases():
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    equal_weight_box_ne(**obj)
                with self.assertRaises(ValueError):
                    enumerate_minimizers(**obj)

    def test_seeded_random_against_exhaustive_oracle(self):
        for case, obj in enumerate(seeded_cases(count=24)):
            with self.subTest(case=case):
                audit_instance(obj)

    def test_audit_cli_refuses_to_overwrite_existing_output(self):
        with tempfile.TemporaryDirectory(prefix='equal-light-flow-test-') as directory:
            output = Path(directory) / 'frozen.json'
            content = json.dumps({'preserve': 'exactly'})
            output.write_text(content, encoding='utf-8')
            process = subprocess.run(
                [sys.executable, 'tests/audits/kfac_equal_light_flow.py',
                 '--random-cases', '0', '--output', str(output)],
                cwd=ROOT, capture_output=True, text=True, check=False)
            self.assertNotEqual(process.returncode, 0)
            self.assertIn('Refusing to overwrite', process.stderr)
            self.assertEqual(output.read_text(encoding='utf-8'), content)


if __name__ == '__main__':
    unittest.main()
