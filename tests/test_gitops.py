import argparse
from pathlib import Path
import subprocess
import tempfile
import unittest
from cncrisis.gitops import checkpoint


class Checkpoints(unittest.TestCase):
    def test_named_checkpoint_preserves_unrelated_work_and_rejects_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            def git(*args):
                return subprocess.run(['git', '-C', tmp, *args], check=True, capture_output=True, text=True).stdout.strip()
            git('init', '-b', 'research')
            git('config', 'user.name', 'Research fixture')
            git('config', 'user.email', 'fixture@example.org')
            workspace = root / 'work' / 'run'
            workspace.mkdir(parents=True)
            (workspace / 'chapter.md').write_text('Substantive fixture chapter.\n')
            (root / 'unrelated.md').write_text('Another task.\n')
            args = argparse.Namespace(workspace=workspace, paths=['work/run'], message='Save chapter', push=False)
            receipt = checkpoint(args)
            self.assertEqual(receipt['saved_files'], ['work/run/chapter.md'])
            self.assertFalse(receipt['pushed'])
            self.assertIn('?? unrelated.md', git('status', '--short'))
            git('add', 'unrelated.md')
            (workspace / 'chapter.md').write_text('Revised fixture chapter.\n')
            with self.assertRaisesRegex(ValueError, '暂存区'):
                checkpoint(args)
            self.assertEqual(git('rev-parse', 'HEAD'), receipt['commit'])
            args.paths = ['../outside']
            with self.assertRaisesRegex(ValueError, '当前仓库'):
                checkpoint(args)


if __name__ == '__main__':
    unittest.main()
