import argparse
import json
from pathlib import Path
import tempfile
import unittest
from cncrisis.collect import canonical_url, bridge, Extractor


class CollectionTests(unittest.TestCase):
    def test_syndication_tracking_and_economic_query(self):
        self.assertEqual(canonical_url('https://EXAMPLE.org/table?year=2025&utm_source=x#top'),
                         'https://example.org/table?year=2025')
        self.assertNotEqual(canonical_url('https://example.org/table?year=2025'),
                            canonical_url('https://example.org/table?year=2024'))

    def test_script_text_never_counts_as_publication_text(self):
        page = Extractor()
        page.feed('<title>data</title><script>prediction 999</script><p>actual 12</p>')
        self.assertNotIn('999', ''.join(page.parts))
        self.assertIn('actual 12', ''.join(page.parts))

    def test_builtin_search_bridge_is_not_automatic_fact(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / 'search.json'
            source.write_text(json.dumps({'query': 'household debt', 'provider': 'host-built-in-search',
                                         'executed_at': '2026-11-20T00:00:00+00:00',
                                         'results': [{'url': 'https://www.nber.org/papers/w31489', 'title': 'Sufi'}]}))
            result = bridge(argparse.Namespace(file=str(source), workspace=root))
            self.assertEqual(result['imported_results'], 1)
            self.assertFalse((root / 'state.json').exists())
            stored = json.loads(Path(result['file']).read_text())
            self.assertEqual(stored['executed_at'], '2026-11-20T00:00:00+00:00')


if __name__ == '__main__':
    unittest.main()
