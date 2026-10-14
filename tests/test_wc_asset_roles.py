"""Ensure WC asset routing does not relax the older research tracks."""
import unittest
from research.check_assets import valid_asset_role

class AssetRoleTests(unittest.TestCase):
    def test_scoped_original_sources(self):
        path = 'research/weighted_congestion_frontier/assets/R1/integer_triad/proof.md'
        wc = {'scope_model': 'WC-TARGET v1', 'claims': ['WC-R1-INTEGER-TRIAD']}
        self.assertTrue(valid_asset_role(wc, 'sources', path))
        self.assertFalse(valid_asset_role(wc, 'proof', path))
        self.assertTrue(valid_asset_role(wc, 'proof', 'research/current/weighted_congestion_frontier/README.md'))
        for other in ({'claims': ['SC-PHI-E']},
                      {'scope_model': 'WC-TARGET v1', 'claims': ['SC-PHI-E']},
                      {'scope_model': 'WC-TARGET v1', 'claims': []}):
            self.assertFalse(valid_asset_role(other, 'sources', path))

    def test_legacy_roles(self):
        legacy = {'claims': ['SC-PHI-E']}
        for field, path in [('sources', 'history/source/proof.md'),
                            ('implementation', 'facility_spe/shared_phi.py'),
                            ('tests', 'tests/test_shared_phi.py'),
                            ('records', 'evidence/result.json'),
                            ('examples', 'examples/shared/tiny.json')]:
            self.assertTrue(valid_asset_role(legacy, field, path))
        self.assertFalse(valid_asset_role(legacy, 'sources', 'research/current/new.md'))
        self.assertFalse(valid_asset_role(legacy, 'records', 'unclassified/result.json'))

if __name__ == '__main__':
    unittest.main()
