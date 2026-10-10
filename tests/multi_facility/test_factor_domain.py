"""A complete valid NE certificate must still report a factor >= 1."""
from copy import deepcopy
import unittest

from tests.multi_facility.definition_check import check_certificate


CERTIFICATE = {
    'instance': {'m': 2, 'k': 2, 'clients': [
        {'weight': 2, 'sites': [0]},
        {'weight': 3, 'sites': [0, 1]},
        {'weight': 5, 'sites': [1]}]},
    'on_path': {'layout': [0, 1], 'probabilities': [[1, 0], [1, 0], [0, 1]]},
    'deviations': [
        {'facility': 0, 'site': 1, 'pure_assignment': [-1, 0, 1]},
        {'facility': 1, 'site': 0, 'pure_assignment': [1, 0, -1]}],
    'factor': '1',
    'default_rule': 'least-index initial pure assignment, then strict pure best responses',
}


class FactorDomainTest(unittest.TestCase):
    def test_valid_equilibria_do_not_excuse_subunit_factor(self):
        for factor in ('-1', '0', '3/5', '999/1000'):
            with self.subTest(factor=factor):
                cert = deepcopy(CERTIFICATE)
                cert['factor'] = factor
                with self.assertRaisesRegex(AssertionError, 'at least 1'):
                    check_certificate(cert, all_layouts=True)

    def test_boundary_and_larger_factors_remain_valid(self):
        for factor in ('1', '2'):
            with self.subTest(factor=factor):
                cert = deepcopy(CERTIFICATE)
                cert['factor'] = factor
                result = check_certificate(cert, all_layouts=True)
                self.assertEqual(result['actual_certificate_factor'], '1')
                self.assertEqual(result['actual_deviations_checked'], 2)
                self.assertEqual(result['unlisted_labeled_layouts_checked'], 1)


if __name__ == '__main__':
    unittest.main()
