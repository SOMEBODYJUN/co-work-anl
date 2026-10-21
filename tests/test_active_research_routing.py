"""Exercise routing regressions using isolated copies of real active entry files."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("active_research_check", REPO / "research/check_active_research.py")
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


class ActiveResearchRoutingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.old_root = CHECKER.ROOT
        CHECKER.ROOT = self.root
        self.manifest = json.loads((REPO / "research/active_research.json").read_text())
        paths = set(self.manifest["active_entrypoints"] + self.manifest["role_prompts"] +
                    [self.manifest[k] for k in ("prompt", "runbook", "program", "submitter", "retired_operations_manifest")])
        paths.update(self.manifest["compatibility_redirects"])
        retirement = json.loads((REPO / self.manifest["retired_operations_manifest"]).read_text())
        paths.update(row["archived_path"] for row in retirement["entries"])
        paths.add("research/active_research.json")
        for path in paths:
            dest = self.root / path
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes((REPO / path).read_bytes())
        # Navigation checks only need target existence; no proof content is invented.
        for path in paths:
            if not path.endswith(".md"):
                continue
            for ref in re.findall(r"(?<!\\)\[[^\]\n]+\]\(([^)\s]+)\)", (REPO / path).read_text()):
                if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", ref) or ref.startswith("#"):
                    continue
                source = ((REPO / path).parent / ref.split("#", 1)[0]).resolve()
                if not source.is_relative_to(REPO) or not source.exists():
                    continue
                dest = self.root / source.relative_to(REPO)
                if source.is_dir():
                    dest.mkdir(parents=True, exist_ok=True)
                else:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    if not dest.exists():
                        dest.touch()

    def tearDown(self):
        CHECKER.ROOT = self.old_root
        self.tmp.cleanup()

    def alter(self, path, old, new):
        file = self.root / path
        text = file.read_text()
        self.assertIn(old, text)
        file.write_text(text.replace(old, new, 1))

    def test_current_routes_pass(self):
        result = CHECKER.check()
        self.assertEqual(result["target"], "Q-CAG-HALF")
        self.assertEqual(result["save"], "customer-attraction")
        self.assertEqual(set(result["roles"]), {"boss", "cleaner", "editor"})
        self.assertGreater(result["checked_local_links"], 0)

    def test_standalone_default_cannot_return_to_old_topic(self):
        self.alter(self.manifest["program"], 'DEFAULT_SAVE = "customer-attraction"', 'DEFAULT_SAVE = "shared"')
        with self.assertRaisesRegex(ValueError, "standalone"):
            CHECKER.check()

    def test_unbound_submitter_cannot_return_to_old_topic(self):
        self.alter(self.manifest["submitter"], 'DEFAULT_SAVE = "customer-attraction"', 'DEFAULT_SAVE = "shared"')
        with self.assertRaisesRegex(ValueError, "checkpoint"):
            CHECKER.check()

    def test_old_binding_cannot_be_handed_new_topic_prompt(self):
        self.alter(self.manifest["program"], '"research_prompt": None',
                   '"research_prompt": "research/unrelated_machines/BOSS_START.md"')
        with self.assertRaisesRegex(ValueError, "legacy save"):
            CHECKER.check()

    def test_retired_role_cannot_duplicate_a_task(self):
        path = next(iter(self.manifest["compatibility_redirects"]))
        file = self.root / path
        file.write_text(file.read_text() + "\n~~~text\nold task\n~~~\n")
        with self.assertRaisesRegex(ValueError, "duplicates"):
            CHECKER.check()

    def test_exactly_three_current_roles(self):
        self.manifest["roles"]["reviewer"] = "research/customer_attraction/EDITOR.md"
        (self.root / "research/active_research.json").write_text(json.dumps(self.manifest))
        with self.assertRaisesRegex(ValueError, "exactly three"):
            CHECKER.check()

    def test_role_receipt_cannot_point_to_other_role(self):
        self.alter(self.manifest["program"],
                   '"editor": "research/customer_attraction/EDITOR.md"',
                   '"editor": "research/customer_attraction/CLEANER.md"')
        with self.assertRaisesRegex(ValueError, "role receipt"):
            CHECKER.check()

    def test_unrelated_save_keeps_its_own_prompt(self):
        self.alter(self.manifest["program"],
                   '"research_prompt": "research/unrelated_machines/BOSS_START.md"',
                   '"research_prompt": "research/customer_attraction/BOSS_START.md"')
        with self.assertRaisesRegex(ValueError, "legacy save"):
            CHECKER.check()

    def test_retired_original_bytes_remain_unchanged(self):
        retirement = json.loads((self.root / self.manifest["retired_operations_manifest"]).read_text())
        file = self.root / retirement["entries"][0]["archived_path"]
        file.write_bytes(file.read_bytes() + b"changed")
        with self.assertRaisesRegex(ValueError, "retired original bytes"):
            CHECKER.check()

    def test_stale_root_instruction_is_rejected_even_with_new_topic_header(self):
        file = self.root / "README.md"
        file.write_text(file.read_text() + "\n当前主攻UM-TARGET-v1。\n")
        with self.assertRaisesRegex(ValueError, "stale unconditional"):
            CHECKER.check()

    def test_broken_active_link_is_rejected(self):
        file = self.root / "README.md"
        file.write_text(file.read_text() + "\n[当前证明](research/current/customer_attraction/nonexistent_proof.md)\n")
        with self.assertRaisesRegex(ValueError, "broken active navigation"):
            CHECKER.check()


if __name__ == "__main__":
    unittest.main()
