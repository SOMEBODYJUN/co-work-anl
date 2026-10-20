"""Branch selection tests: rejected paths stop before staging or networking."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
PROGRAM=ROOT/'research/weighted_congestion_frontier/tools/checkpoint.py'
BRANCH='research/topic-selection-boss6-20261020'

class ExplicitBranchCheckpointTests(unittest.TestCase):
    def cli(self,*args):
        p=subprocess.run(['python3',str(PROGRAM),'--repo',str(ROOT),*args,'__topic_test_missing_path__'],capture_output=True,text=True)
        self.assertNotEqual(p.returncode,0)
        return p.stderr
    def test_default_remains_main(self):
        self.assertIn('branch mismatch',self.cli())
    def test_wrong_explicit_branch(self):
        self.assertIn('branch mismatch',self.cli('--branch',BRANCH+'-other'))
    def test_unrelated_branch_is_rejected(self):
        self.assertIn('limited to',self.cli('--branch','research/unauthorized'))
    def test_matching_branch_reaches_scope_guard(self):
        self.assertIn('Unknown checkpoint path',self.cli('--branch',BRANCH))
    def test_descriptor_names_actual_branch(self):
        spec=importlib.util.spec_from_file_location('checkpoint_under_test',PROGRAM)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        head=module.value(ROOT,'rev-parse','HEAD')
        with tempfile.TemporaryDirectory(dir=ROOT/'.git') as td:
            rows=module.describe_assets(ROOT,Path(td),head,['README.md'])
            self.assertEqual(rows[0]['asset']['branch'],BRANCH)
            self.assertEqual(json.loads(Path(rows[0]['descriptor']).read_text())['branch'],BRANCH)

if __name__=='__main__':
    unittest.main()
