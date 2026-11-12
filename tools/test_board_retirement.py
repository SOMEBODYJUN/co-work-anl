"""Retired routes cannot recreate chat or send research into map closeout."""
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

import board
import restart

spec = importlib.util.spec_from_file_location('work_entry', Path(__file__).resolve().parents[1] / 'work.py')
work = importlib.util.module_from_spec(spec)
spec.loader.exec_module(work)


class BoardRetirementTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=Path.cwd())
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.git('init', '--quiet', '--initial-branch=rebuild/research-v2')
        self.git('remote', 'add', 'origin', 'https://github.com/SOMEBODYJUN/co-work-anl.git')

    def git(self, *args):
        return subprocess.run(['git', *args], cwd=self.root, check=True, capture_output=True)

    def test_retired_explicit_routes_fail_before_creating_cache_or_using_network(self):
        for route in work.RETIRED_BOARD_BRANCHES:
            with self.subTest(route=route):
                with self.assertRaises(work.Stop):
                    work.board_branch(self.root, route)
                with self.assertRaises(board.ValidationError):
                    board.Board(self.root, branch=route)
        self.assertFalse((self.root / '.git/wcg').exists())

    def test_saved_research_and_cleanup_routes_do_not_fall_through_into_map(self):
        for role in ['boss', 'cleaner', 'curator']:
            self.git('config', 'wcg.role', role)
            for route in work.RETIRED_BOARD_BRANCHES:
                self.git('config', 'wcg.boardBranch', route)
                with self.subTest(role=role, route=route):
                    self.assertIsNone(work.board_branch(self.root, allow_none=True))
                    with self.assertRaises(work.Stop):
                        work.board_branch(self.root)

    def test_mapper_preserves_its_active_board_with_legacy_or_empty_binding(self):
        self.git('config', 'wcg.role', 'mapper')
        self.assertEqual(work.board_branch(self.root), 'wcg/board-map-v2')
        self.git('config', 'wcg.boardBranch', 'wcg/board-cleanup-20261028')
        self.assertEqual(work.board_branch(self.root), 'wcg/board-map-v2')
        self.git('config', 'wcg.boardBranch', 'wcg/board-map-v2')
        self.assertEqual(work.board_branch(self.root), 'wcg/board-map-v2')
        self.assertEqual(board.Board(self.root, branch='wcg/board-map-v2').branch, 'wcg/board-map-v2')

    def test_unbound_clone_and_old_reset_cannot_initialize_a_board(self):
        self.assertIsNone(work.board_branch(self.root, allow_none=True))
        with self.assertRaises(work.Stop):
            work.board_branch(self.root)
        with self.assertRaisesRegex(ValueError, 'retired'):
            restart.apply(self.root, 'Boss32')
        self.assertFalse((self.root / '.git/wcg').exists())


if __name__ == '__main__':
    unittest.main()
