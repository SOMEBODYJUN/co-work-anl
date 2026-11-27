"""Real CLI completion gates; all research artifacts here are synthetic tests."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from cncrisis import engine, runtime


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "source" / "work" / "Boss11"
        self.root.parent.mkdir(parents=True)
        subprocess.run(["git", "init", "-q", "-b", "work/cn-crisis", str(self.root.parents[1])], check=True)
        self.args = argparse.Namespace(workspace=self.root, actor="Boss11")

    def tearDown(self):
        self.temp.cleanup()

    def register_complete_fixture(self, input_kind="synthetic_test"):
        runtime.start(self.args)
        for path in runtime.DELIVERABLES:
            file = self.root / path
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text("Synthetic engineering fixture; not economic research.")
        acceptance = {"schema": "cncrisis-acceptance.v1", "input_kind": input_kind,
                      "cycle": 1, "author": "Boss11", "reviewer": "actual-reviewer",
                      "checks": [{"id": key, "verdict": "pass",
                                  "evidence": "Synthetic fixture for exercising version gates.",
                                  "artifacts": ["research/final_review.md"]} for key in runtime.CHECKS]}
        (self.root / runtime.ACCEPTANCE).write_text(json.dumps(acceptance))
        files = [*runtime.DELIVERABLES, runtime.ACCEPTANCE]
        for stage in engine.FIRST_STAGES:
            engine.stage(argparse.Namespace(workspace=self.root, id=stage, files=files, note="Synthetic stage"))
        engine.review(argparse.Namespace(workspace=self.root, verdict="pass", files=files,
                      author="Boss11", reviewer="actual-reviewer", note="Synthetic review"))
        engine.release(argparse.Namespace(workspace=self.root, files=files, judgment="Synthetic fixture"))

    def test_stable_identity_resume_wrong_actor_rejected_and_no_renumbering(self):
        first = runtime.start(self.args)
        resumed = runtime.start(self.args)
        self.assertEqual(first["run_id"], resumed["run_id"])
        self.assertEqual(resumed["actor"], "Boss11")
        self.assertFalse(resumed["complete"])
        self.assertIn("s01_scope", resumed["next_action"])
        with self.assertRaisesRegex(engine.EngineError, "Boss11"):
            runtime.start(argparse.Namespace(workspace=self.root, actor="Boss1"))

    def test_synthetic_release_does_not_pass_research_acceptance(self):
        self.register_complete_fixture()
        result = runtime.progress(self.args)
        self.assertFalse(result["complete"])
        self.assertIn("合成", str(result["blockers"]))

    def test_branch_switch_is_not_silently_adopted(self):
        runtime.start(self.args)
        subprocess.run(["git", "-C", str(self.root.parents[1]), "symbolic-ref", "HEAD", "refs/heads/other"], check=True)
        with self.assertRaisesRegex(engine.EngineError, "分支"):
            runtime.progress(self.args)

    def test_reviewed_completion_tamper_reject_and_update_cycle(self):
        # The literal real_research is solely for testing schema acceptance;
        # this fixture is never shipped or reported as completed research.
        self.register_complete_fixture(input_kind="real_research")
        self.assertTrue(runtime.progress(self.args)["complete"])
        (self.root / "formal/report.md").write_text("Changed after independent review")
        self.assertFalse(runtime.progress(self.args)["complete"])

    def test_copy_restore_and_new_cycle_require_new_acceptance(self):
        self.register_complete_fixture(input_kind="real_research")
        clone = Path(self.temp.name) / "fresh" / "work" / "Boss11"
        clone.parent.mkdir(parents=True)
        subprocess.run(["git", "init", "-q", "-b", "work/cn-crisis", str(clone.parents[1])], check=True)
        shutil.copytree(self.root, clone)
        restored = argparse.Namespace(workspace=clone, actor="Boss11")
        self.assertTrue(runtime.progress(restored)["complete"])
        self.assertEqual(runtime.progress(restored)["run_id"], runtime.progress(self.args)["run_id"])
        engine.initialise(argparse.Namespace(workspace=clone, mode="update"))
        result = runtime.progress(restored)
        self.assertFalse(result["complete"])
        self.assertIn("i01_restore", result["next_action"])
        self.assertIn("当前研究周期", str(result["blockers"]))

    def test_acceptance_paths_and_missing_evidence_cannot_pass(self):
        self.register_complete_fixture(input_kind="real_research")
        path = self.root / runtime.ACCEPTANCE
        document = json.loads(path.read_text())
        document["checks"][0]["artifacts"] = ["../outside.md"]
        path.write_text(json.dumps(document))
        result = runtime.progress(self.args)
        self.assertFalse(result["complete"])
        self.assertIn("inside workspace", str(result["blockers"]))

    def test_cli_identity_only_defaults_and_check_nonzero(self):
        script = Path(__file__).resolve().parents[1] / "work.py"
        result = subprocess.run([sys.executable, str(script), "session", "start", "--actor", "12341234"],
                                cwd=self.temp.name, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        document = json.loads(result.stdout)
        self.assertEqual(document["actor"], "12341234")
        self.assertEqual(Path(document["workspace"]), Path(self.temp.name) / "work/12341234")
        check = subprocess.run([sys.executable, str(script), "session", "check", "--actor", "12341234"],
                               cwd=self.temp.name, capture_output=True, text=True)
        self.assertEqual(check.returncode, 3)
        self.assertFalse(json.loads(check.stdout)["complete"])


if __name__ == "__main__":
    unittest.main()
