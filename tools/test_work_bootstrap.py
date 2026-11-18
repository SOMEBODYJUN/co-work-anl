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
        for path in ('archives/customer-attraction/README.md', 'prompts/research-runtime.md',
                     'tools/research_runtime.py'):
            fixture = self.source / path
            fixture.parent.mkdir(parents=True, exist_ok=True)
            fixture.touch()
        self.git(self.source, 'add', '.')
        self.git(self.source, 'commit', '-qm', 'Initial research fixture')
        self.remote = self.root / 'remote.git'
        self.git(self.root, 'clone', '-q', '--bare', str(self.source), str(self.remote))
        self.clone = self.root / 'restored'

    def git(self, cwd, *args):
        result = subprocess.run(['git', *args], cwd=cwd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def start(self, *extra, actor='Boss2'):
        identity = ['--actor', actor] if actor else []
        return subprocess.run([sys.executable, str(self.bootstrap), '--repo', str(self.clone),
            'start', *identity, '--role', 'boss', '--save', 'customer-attraction',
            '--remote', str(self.remote), '--branch', 'research-test', *extra], cwd=self.root,
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

    def test_handoff_survives_a_public_cli_rename(self):
        current = self.source / 'work.py'
        current.write_text(current.read_text().replace(
            'start_parser.add_argument("--role", choices=tuple(ROLE_PROMPTS))',
            'start_parser.add_argument("--research-role", dest="role", choices=tuple(ROLE_PROMPTS))'))
        self.git(self.source, 'commit', '-qam', 'Rename a public CLI flag')
        self.git(self.source, 'push', '-q', str(self.remote), 'research-test')
        result = self.start()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['role'], 'boss')

    def test_legacy_default_is_accepted_and_active_board_requests_are_rejected(self):
        rejected = self.start('--board-limit', '1')
        self.assertIn('公屏已退役', rejected.stderr)
        self.assertFalse(self.clone.exists())
        compatible = self.start('--board-limit', '0')
        self.assertEqual(compatible.returncode, 0, compatible.stderr)

    def test_failed_first_transfer_leaves_target_empty_and_same_command_retries(self):
        self.clone.mkdir()
        offline = self.root / 'offline.git'
        self.remote.rename(offline)
        broken = self.start()
        self.assertNotEqual(broken.returncode, 0)
        self.assertEqual(list(self.clone.iterdir()), [])
        offline.rename(self.remote)
        recovered = self.start()
        self.assertEqual(recovered.returncode, 0, recovered.stderr)

    def test_bad_archive_does_not_bind_actor_or_save(self):
        result = self.start('--save', 'typo')
        self.assertIn('archives/typo/README.md', result.stderr)
        result = self.start(actor='Boss3')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['actor'], 'Boss3')

    def test_saved_identity_and_untracked_journal_survive_an_update(self):
        first = self.start()
        self.assertEqual(first.returncode, 0, first.stderr)
        personal = self.clone / json.loads(first.stdout)['workspace']['path']
        draft = personal / 'journal.md'
        draft.write_text('Continue the original argument.\n')
        with (self.source / 'work.py').open('a') as stream:
            stream.write('\n# Updated downstream launcher.\n')
        self.git(self.source, 'commit', '-qam', 'Update the remote entry')
        self.git(self.source, 'push', '-q', str(self.remote), 'research-test')
        continued = self.start(actor=None)
        self.assertEqual(continued.returncode, 0, continued.stderr)
        self.assertEqual(draft.read_text(), 'Continue the original argument.\n')
        self.assertEqual((self.clone / 'work.py').read_bytes(), (self.source / 'work.py').read_bytes())

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
