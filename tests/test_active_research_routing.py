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
                    [self.manifest[k] for k in ("prompt", "runbook", "program", "submitter")])
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
        self.assertEqual(result["target"], "UM-TARGET-v1")
        self.assertGreater(result["checked_local_links"], 100)

    def test_standalone_default_cannot_return_to_old_topic(self):
        self.alter(self.manifest["program"], 'DEFAULT_SAVE = "unrelated-machines"', 'DEFAULT_SAVE = "shared"')
        with self.assertRaisesRegex(ValueError, "standalone"):
            CHECKER.check()

    def test_unbound_submitter_cannot_return_to_old_topic(self):
        self.alter(self.manifest["submitter"], 'DEFAULT_SAVE = "unrelated-machines"', 'DEFAULT_SAVE = "shared"')
        with self.assertRaisesRegex(ValueError, "checkpoint"):
            CHECKER.check()

    def test_old_binding_cannot_be_handed_new_topic_prompt(self):
        self.alter(self.manifest["program"], '"research_prompt": None',
                   '"research_prompt": "research/unrelated_machines/BOSS_START.md"')
        with self.assertRaisesRegex(ValueError, "legacy shared"):
            CHECKER.check()

    def test_compatibility_team_must_remain_the_complete_task(self):
        self.alter(self.manifest["team_compatibility_prompt"], "持续推进", "偶尔推进")
        with self.assertRaisesRegex(ValueError, "drifted"):
            CHECKER.check()

    def test_stale_root_instruction_is_rejected_even_with_new_topic_header(self):
        file = self.root / "README.md"
        file.write_text(file.read_text() + "\n当前主攻是加权拥塞。\n")
        with self.assertRaisesRegex(ValueError, "stale unconditional"):
            CHECKER.check()

    def test_broken_active_link_is_rejected(self):
        file = self.root / "README.md"
        file.write_text(file.read_text() + "\n[当前证明](research/current/unrelated_machines/nonexistent_proof.md)\n")
        with self.assertRaisesRegex(ValueError, "broken active navigation"):
            CHECKER.check()


if __name__ == "__main__":
    unittest.main()
