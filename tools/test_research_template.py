"""A fresh project can use the same entry point without the source archive."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from export_research_template import export


class ResearchTemplateTests(unittest.TestCase):
    def test_export_has_complete_current_inputs_and_can_open_an_empty_seed_studio(self):
        source = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as temporary:
            root = Path(temporary) / 'new-project'
            export(source, root, 'https://github.com/example/new-math.git', 'research')
            for name in ['research-runtime.md', 'research-main-design.md',
                         'research-line-design.md', 'research-review-design.md', 'paper-evaluation.md']:
                self.assertTrue((root / 'prompts' / name).is_file(), name)
            self.assertTrue((root / 'research/agent-design/HYPEREDGE_WORKFLOW.md').is_file())
            self.assertTrue((root / 'research/schemas/research-packet.schema.json').is_file())
            self.assertFalse((root / 'research/operations').exists())
            self.assertFalse((root / 'research/CURATION.md').exists())
            self.assertTrue((root / 'AGENTS.md').is_file())
            self.assertFalse((root / 'research/registry.json').exists())
            self.assertFalse((root / 'archives').exists())
            for original in (source / 'research/agent-design/upstream').rglob('*'):
                if original.is_file():
                    exported = root / original.relative_to(source)
                    self.assertEqual(exported.read_bytes(), original.read_bytes(), str(original))
            entry = (root / 'work.py').read_text()
            self.assertIn('DEFAULT_BRANCH = "research"', entry)
            self.assertIn('REMOTE = "https://github.com/example/new-math.git"', entry)

            def execute(*args):
                result = subprocess.run([sys.executable, 'work.py', *args], cwd=root,
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                return json.loads(result.stdout)

            subprocess.run(['git', 'config', 'wcg.actor', 'Boss2'], cwd=root, check=True)
            subprocess.run(['git', '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
                            'commit', '--allow-empty', '-qm', 'Empty research project'], cwd=root, check=True)
            problem = root / 'problem.md'
            problem.write_text('# Original problem\nProve the exact stated target.\n')
            evaluation = execute('research', 'evaluate', '--paper', 'problem.md')
            self.assertEqual(evaluation['status'], 'awaiting_review')
            self.assertTrue(Path(evaluation['task']).is_file())
            import hashlib
            spec = {'problem_id': 'new-target',
                    'problem': {'path': 'problem.md', 'sha256': hashlib.sha256(problem.read_bytes()).hexdigest()},
                    'definitions': [], 'obstacles': [], 'seed_ids': []}
            (root / 'spec.json').write_text(json.dumps(spec))
            opened = execute('research', 'studio', 'init', 'new-run', '--spec', 'spec.json',
                             '--expect-branch', 'research', '--expect-remote',
                             'https://github.com/example/new-math.git')
            self.assertEqual(opened['agents_launched'], 0)
            state = execute('research', 'studio', 'status', 'new-run', '--session-tag', 'fresh')
            self.assertTrue(state)
            for name in ['main', 'independent', 'informed-a', 'informed-b']:
                self.assertTrue((root / 'research/workspaces/new-run' / name / 'journal.md').is_file())
            self.assertFalse(list(root.glob('**/collaboration')))


if __name__ == '__main__':
    unittest.main()
