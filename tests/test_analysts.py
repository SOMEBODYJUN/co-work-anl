import argparse
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from cncrisis import analysts


def post(modified="2023-05-18T00:00:00Z"):
    return {"ID": 10, "URL": "https://example.wordpress.com/2023/a/",
            "date": "2023-05-18T00:00:00Z", "modified": modified,
            "title": "A &amp; B", "categories": {"China": {}}}


class AnalystInventoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "inventory.json"
        self.args = argparse.Namespace(site="example.wordpress.com", output=str(self.path), max_pages=1)

    def run_inventory(self, row=None, found=1):
        response = {"found": found, "posts": [post() if row is None else row]}
        with patch.object(analysts, "request", return_value=(json.dumps(response).encode(), "", {})):
            return analysts.inventory(self.args)

    def test_complete_directory_does_not_claim_articles_read(self):
        result = self.run_inventory()
        self.assertTrue(result["metadata_inventory_complete"])
        self.assertFalse(result["full_article_distillation_complete"])
        row = json.loads(self.path.read_text())["posts"][0]
        self.assertEqual(row["reading_status"], "metadata_only")
        self.assertEqual(row["title"], "A & B")

    def test_refresh_keeps_work_and_marks_modified_article_for_rereading(self):
        self.run_inventory()
        data = json.loads(self.path.read_text())
        data["posts"][0].update(reading_status="distilled_reviewed", claim_ids=["C-1"], reading_note="notes/a.md")
        self.path.write_text(json.dumps(data))
        self.assertTrue(self.run_inventory()["full_article_distillation_complete"])
        self.run_inventory(post("2024-01-01T00:00:00Z"))
        row = json.loads(self.path.read_text())["posts"][0]
        self.assertEqual(row["reading_status"], "needs_reread")
        self.assertEqual(row["claim_ids"], ["C-1"])
        self.assertEqual(row["reading_note"], "notes/a.md")

    def test_page_limit_preserves_incomplete_coverage(self):
        result = self.run_inventory(found=101)
        self.assertFalse(result["metadata_inventory_complete"])
        self.assertFalse(result["full_article_distillation_complete"])

    def test_different_author_cannot_overwrite_inventory(self):
        self.run_inventory()
        before = self.path.read_bytes()
        self.args.site = "other.wordpress.com"
        with self.assertRaises(ValueError):
            analysts.inventory(self.args)
        self.assertEqual(self.path.read_bytes(), before)
