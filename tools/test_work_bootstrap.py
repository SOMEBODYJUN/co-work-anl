"""First startup and an interrupted checkout use the same downloaded entry."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class BootstrapTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=Path.cwd())
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / 'origin'
        self.source.mkdir()
        self.git(self.source, 'init', '-q', '-b', 'research-test')
        self.git(self.source, 'config', 'user.name', 'Test')
        self.git(self.source, 'config', 'user.email', 'test@example.invalid')
        self.bootstrap = Path(__file__).resolve().parents[1] / 'work.py'
        shutil.copy2(self.bootstrap, self.source / 'work.py')
        (self.source / 'README.md').write_text('Original research entry.\n')
        self.git(self.source, 'add', '.')
        self.git(self.source, 'commit', '-qm', 'Initial research fixture')
        self.remote = self.root / 'remote.git'
        self.git(self.root, 'clone', '-q', '--bare', str(self.source), str(self.remote))
        self.clone = self.root / 'restored'

    def git(self, cwd, *args):
        result = subprocess.run(['git', *args], cwd=cwd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def start(self):
        return subprocess.run([sys.executable, str(self.bootstrap), '--repo', str(self.clone),
            'start', '--actor', 'Boss2', '--role', 'boss', '--save', 'customer-attraction',
            '--remote', str(self.remote), '--branch', 'research-test'], cwd=self.root,
            capture_output=True, text=True, timeout=30)

    def interrupted(self):
        self.git(self.root, 'clone', '-q', '--no-checkout', str(self.remote), str(self.clone))
        self.git(self.clone, 'config', 'wcg.bootstrapCheckout', self.git(self.clone, 'rev-parse', 'HEAD'))

    def test_downloaded_entry_restores_complete_checkout_and_hands_off(self):
        result = self.start()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['actor'], 'Boss2')
        self.assertEqual((self.clone / 'work.py').read_bytes(), self.bootstrap.read_bytes())
        self.assertEqual(self.git(self.clone, 'diff', '--name-only'), '')

    def test_interrupted_checkout_recovers_without_overwriting_an_untracked_draft(self):
        self.interrupted()
        draft = self.clone / 'draft.md'
        draft.write_text('Unfinished original mathematics.\n')
        result = self.start()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.clone / 'work.py').exists())
        self.assertEqual(draft.read_text(), 'Unfinished original mathematics.\n')

    def test_changed_existing_file_is_preserved_and_not_silently_treated_as_clean(self):
        self.interrupted()
        draft = self.clone / 'README.md'
        draft.write_text('A useful local change after interruption.\n')
        result = self.start()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('已保留', result.stderr)
        self.assertEqual(draft.read_text(), 'A useful local change after interruption.\n')


if __name__ == '__main__':
    unittest.main()
