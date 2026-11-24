"""Exercise the real CLI without credentials or a research registry."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]


class PaperEvaluationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.cwd = Path(self.temp.name)
        self.root = self.cwd / "repo"
        self.root.mkdir()
        for name in ("work.py", ".gitignore", "tools/research_runtime.py", "tools/path_utils.py",
                     "tools/paper_evaluation.py", "tools/paper_evaluation_anchors.py",
                     "tools/PAPER_EVALUATION.md", "prompts/paper-evaluation.md"):
            out = self.root / name
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / name, out)
        self.git("init", "-q")
        (self.cwd / "paper.tex").write_text("A bounded subset of the primes can be listed.\n\\input{lemma}\n")
        (self.cwd / "lemma.tex").write_text("The integers between 0 and N form a finite set.\n")
        (self.cwd / "target.md").write_text("Decide whether there are infinitely many primes.\n")

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.root), *args], capture_output=True, text=True, check=True)

    def cli(self, *args, fail=None):
        p = subprocess.run([sys.executable, str(self.root / "work.py"), "--repo", str(self.root),
                            "research", "evaluate", *args], cwd=self.cwd, capture_output=True, text=True)
        if fail:
            self.assertEqual(p.returncode, 2, p.stderr)
            self.assertIn(fail, p.stderr)
            return
        self.assertEqual(p.returncode, 0, p.stderr)
        return json.loads(p.stdout)

    def start(self, include=True):
        options = ["--include", "lemma.tex"] if include else []
        intake = self.cli("--paper", "paper.tex", "--target-file", "target.md", *options)
        return intake["run_id"], Path(intake["directory"]), intake

    def test_dependencies_are_frozen_and_resume_detects_replacement(self):
        _, _, incomplete = self.start(include=False)
        self.assertIn("lemma", incomplete["coverage_warnings"][0])
        name, directory, complete = self.start()
        self.assertEqual(complete["coverage_warnings"], [])
        self.git("check-ignore", str(directory / "inputs/S1.tex"))
        (self.cwd / "lemma.tex").write_text("A revised lemma.")
        self.assertEqual(self.cli("--run", name)["fingerprint"], complete["fingerprint"])
        (directory / "inputs/S2.tex").write_text("Tampered frozen lemma.")
        self.cli("--run", name, fail="Frozen input changed")

    def test_honest_partial_is_reviewable_and_result_is_order_independent(self):
        name, directory, _ = self.start()
        report = json.loads((directory / "review-template.json").read_text())
        report.update(summary="A small observation; it does not resolve the general problem.",
                      tracks={k: {"status": "completed", "reviewer": "test", "coverage": "One statement."}
                              for k in report["tracks"]},
                      evidence=[{"id": key, "kind": "input", "source": source, "start": 1,
                                 "end": 1, "note": note} for key, source, note in
                                [("E1", "S1", "Claim"), ("E2", "S3", "Target")]],
                      readiness={"status": "ready_for_expert_review", "reason": "Correct limited claim.",
                                 "actions": [], "venues": []},
                      search_log=[{"query": "Prime subsets", "source": "test fixture", "outcome": "No related source."}],
                      quality=[])
        report["importance"].update(target="Original problem", rationale="Not calibrated.")
        claim = report["claims"][0]
        claim.update(statement="Bounded subsets are finite.", assumptions="Positive bounded integers.",
                     quantifiers="Every bounded subset.", conclusion="Finite.",
                     prior_art=[], target={"status": "partial", "analysis": "Finiteness of bounded sets only.",
                                           "evidence": ["E2"], "overclaims_target": False},
                     proof={"status": "no_gap_found", "analysis": "The interval is finite.",
                            "evidence": ["E1"], "obligations": []})
        for row in claim["novelty"].values():
            row.update(status="uncertain", analysis="Not claimed or established in this test.")
        path = self.cwd / "review.json"
        path.write_text(json.dumps(report))
        first = self.cli("--run", name, "--report", str(path))
        path.write_text(json.dumps(dict(reversed(list(report.items()))), sort_keys=False))
        self.assertEqual(self.cli("--run", name, "--report", str(path)), first)
        claim["target"]["overclaims_target"] = True
        path.write_text(json.dumps(report))
        self.cli("--run", name, "--report", str(path), fail="Ready requires")
        claim["target"]["overclaims_target"] = False
        report["evidence"].append({"id": "E3", "kind": "public", "url": "https://example.org/proof",
                                   "title": "test fixture", "locator": "p. 1", "accessed": "2026-11-23", "note": "test"})
        report["importance"].update(as_of="2026-01-01", band=[35, 40], evidence=["E3"], comparisons=[
            {"anchor": key, "relation": "higher", "reason": "Deliberate contradictory relation."}
            for key in ("feiges-conjecture", "erdos-planar-unit-distance")])
        path.write_text(json.dumps(report))
        self.cli("--run", name, "--report", str(path), fail="contradicts the score band")
        report["importance"]["comparisons"][0]["relation"] = "comparable"
        report["importance"]["comparisons"][1]["relation"] = "comparable"
        path.write_text(json.dumps(report))
        scored = self.cli("--run", name, "--report", str(path))
        self.assertIn("35–40 / 100", Path(scored["report"]).read_text())
        Path(scored["report"]).write_text("Replaced after generation")
        self.cli("--run", name, "--report", str(path), fail="Previously generated report was modified")
        self.cli("--run", self.start()[0], "--report", str(path), fail="does not match this frozen run")


if __name__ == "__main__":
    unittest.main()
