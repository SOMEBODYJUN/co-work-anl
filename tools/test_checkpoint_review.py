"""A reviewed publication is checked at the final Git commit, including merges."""
import json
from argparse import Namespace
from pathlib import Path
import tempfile
import unittest

import checkpoint
import research_runtime as runtime
import research_studio as studio
import test_research_studio as fixtures


class ReviewedCommitTests(unittest.TestCase):
    def setUp(self):
        self.f = fixtures.StudioTests(methodName='runTest')
        self.f.setUp()
        self.addCleanup(self.f.doCleanups)
        record = self.f.backflow()
        result = studio.promote(self.f.root, 'run', self.f.record(record, 'promote'))
        self.plan = result['path']
        self.candidate = result['candidate_registry_ref']['path']

    def commit(self):
        self.f.git('add', '.')
        self.f.git('commit', '-qm', 'Reviewed publication fixture')
        return self.f.git('rev-parse', 'HEAD')

    def install(self):
        runtime.register(self.f.root, self.candidate)
        runtime.build(self.f.root)
        return self.commit()

    def audit(self, head):
        return checkpoint.audit_review_plans(self.f.root, head, [self.plan])

    def local_remote(self):
        tmp = tempfile.TemporaryDirectory(dir=Path.cwd())
        self.addCleanup(tmp.cleanup)
        remote = Path(tmp.name) / 'remote.git'
        self.f.git('clone', '-q', '--bare', str(self.f.root), str(remote))
        self.f.git('remote', 'set-url', 'origin', str(remote))
        self.f.git('config', 'wcg.branch', 'research-test')
        self.f.git('config', 'wcg.role', 'boss')
        return remote

    def publish(self, *, publish_only=True):
        return checkpoint.save(Namespace(repo=str(self.f.root), paths=['.'], message='Reviewed research',
            token_file=None, create_branch=False, local_only=False, publish_only=publish_only,
            review_plan=[self.plan]))

    def remote_head(self, remote):
        return self.f.git('--git-dir=' + str(remote), 'rev-parse', 'refs/heads/research-test')

    def test_final_commit_is_checked_instead_of_later_uncommitted_journal(self):
        head = self.install()
        self.f.write(self.f.work + '/main/journal.md', 'Continue the next mathematical obligation.\n')
        self.assertEqual(self.audit(head), [self.plan])

    def test_mutation_after_promote_cannot_be_published_as_reviewed(self):
        self.install()
        self.f.write('archives/example/state/命题/X--命题.md', 'A different and unreviewed proof.\n')
        with self.assertRaisesRegex(checkpoint.Stop, 'bytes changed'):
            self.audit(self.commit())

    def test_plan_metadata_itself_cannot_change_after_promote(self):
        self.install()
        plan = self.f.read(self.plan)
        plan['claim_scope'] = 'whole-target'
        self.f.write(self.plan, plan)
        with self.assertRaisesRegex(checkpoint.Stop, 'bytes changed'):
            self.audit(self.commit())

    def test_candidate_must_be_installed_but_does_not_require_a_projection(self):
        self.f.write(runtime.REGISTRY, {'schema': 2, 'objects': [], 'materials': [], 'edge_files': []})
        with self.assertRaisesRegex(checkpoint.Stop, 'not installed in the final canonical registry'):
            self.audit(self.commit())
        (self.f.root / runtime.REGISTRY).unlink()
        runtime.register(self.f.root, self.candidate)
        self.assertEqual(self.audit(self.commit()), [self.plan])

    def test_disjoint_peer_metadata_does_not_require_rebuilding_a_projection(self):
        head = self.install()
        self.f.git('branch', 'peer', head)
        self.f.git('checkout', '-q', 'peer')
        registry = self.f.read(runtime.REGISTRY)
        registry['peer_metadata'] = 'A disjoint registry increment'
        self.f.write(runtime.REGISTRY, registry)
        self.commit()
        self.f.git('checkout', '-q', 'research-test')
        self.f.write('peer-independent-note.md', 'Disjoint local research.\n')
        self.commit()
        self.f.git('merge', '--no-edit', 'peer')
        self.assertEqual(self.audit(self.f.git('rev-parse', 'HEAD')), [self.plan])

    def test_unresolved_objection_added_after_promote_blocks_publication(self):
        self.install()
        self.f.review('frozen', verdict='changes-required', rid='late-objection')
        with self.assertRaisesRegex(checkpoint.Stop, 'Unresolved'):
            self.audit(self.commit())

    def test_actual_push_rejects_unreviewed_bytes_and_retains_local_work(self):
        approved = self.install()
        remote = self.local_remote()
        self.f.write('archives/example/state/命题/X--命题.md', 'Unreviewed change after promote.\n')
        local = self.commit()
        with self.assertRaisesRegex(checkpoint.Stop, 'bytes changed'):
            self.publish()
        self.assertEqual(self.remote_head(remote), approved)
        self.assertEqual(self.f.git('rev-parse', 'HEAD'), local)

    def test_push_retry_rechecks_reviewed_bytes_after_merging(self):
        approved = self.install()
        remote = self.local_remote()
        path = 'archives/example/state/命题/X--命题.md'
        original = (self.f.root / path).read_bytes()
        self.f.git('checkout', '-qb', 'peer', approved)
        self.f.write(path, 'Peer changed a reviewed proof.\n')
        peer = self.commit()
        self.f.git('push', '-q', 'origin', 'peer:research-test')
        self.f.git('checkout', '-q', 'research-test')
        self.f.write('local-next-obligation.md', 'Continue the separate local route.\n')
        self.commit()
        with self.assertRaisesRegex(checkpoint.Stop, 'bytes changed'):
            self.publish()
        self.assertEqual(self.remote_head(remote), peer)
        self.assertEqual(len(self.f.git('show', '-s', '--format=%P', 'HEAD').split()), 2)
        (self.f.root / path).write_bytes(original)
        result = self.publish(publish_only=False)
        self.assertEqual(result['status'], 'pushed')
        self.assertEqual(result['review_checked_head'], result['pushed_head'])
        self.assertEqual(self.remote_head(remote), result['pushed_head'])


if __name__ == '__main__':
    unittest.main()
