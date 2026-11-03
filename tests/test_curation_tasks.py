"""Editing ownership is separate from source claims, publication and truth."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import curation
import curation_tasks as task
import coordination
import work

class CurationTaskTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir=ROOT/'tests',prefix='task-fixture-');self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.git('init','--quiet');self.git('config','user.name','Fixture');self.git('config','user.email','fixture@example.invalid')
        self.input='archives/demo/state/引理/A.md';p=self.root/self.input;p.parent.mkdir(parents=True);p.write_text('Exact original mathematics')
        h=task.run_home(self.root,'run');curation._write_json(h/'run.json',{'actor':'Boss6'})
        self.d={'task_id':'A','inputs':[{'path':self.input,'sha256':curation.digest(p.read_bytes())}],
                'write_paths':['archives/demo/state/引理/A.md'],'question':'Which coefficients are structural?',
                'goal':'Explain the parameter inequalities','preserve':'Keep the existing quantifiers',
                'budget_minutes':60,'acceptance':'Give the exact construction or concrete missing inequality'}
        self.git('add','.');self.git('commit','--quiet','-m','Original input')
    def git(self,*args):
        p=subprocess.run(['git',*args],cwd=self.root,capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stderr);return p.stdout.strip()
    def old(self):return {'definition':copy.deepcopy(self.d),'state':'available','owner':None}
    def transition(self,old,op,actor='Boss6',others=(),**kw):
        return task.transition(self.root,'run',old,list(others),actor,op,'r1',**kw)
    def claim(self):return self.transition(self.old(),'claim')
    def asset(self):return {'path':self.input,'sha256':curation.digest((self.root/self.input).read_bytes())}
    def test_parent_write_scope_conflicts(self):
        other=self.old();other['definition']['task_id']='B';other['definition']['write_paths']=['archives/demo'];other.update(state='claimed',owner='Boss7')
        with self.assertRaisesRegex(ValueError,'occupied'):self.transition(self.old(),'claim',others=[other])
    def test_changed_source_cannot_be_claimed(self):
        (self.root/self.input).write_text('New premise')
        with self.assertRaisesRegex(ValueError,'changed'):self.claim()
    def test_only_owner_may_submit_or_handoff(self):
        claimed=self.claim()
        with self.assertRaises(ValueError):self.transition(claimed,'submit','Boss7',assets=[self.asset()])
        with self.assertRaises(ValueError):self.transition(claimed,'handoff','Boss7',reason='Boundary')
    def test_missing_output_cannot_be_submitted(self):
        with self.assertRaisesRegex(ValueError,'not published'):self.transition(self.claim(),'submit',assets=[{'path':self.input,'sha256':'b'*64}])
    def test_submitted_is_not_completed_or_truth_admission(self):
        submitted=self.transition(self.claim(),'submit',assets=[self.asset()])
        self.assertEqual(submitted['state'],'submitted');self.assertNotIn('truth_status',submitted)
        done=self.transition(submitted,'complete',reason='Exact finite witness retained; uniform bound remains open')
        self.assertEqual(done['state'],'completed')
    def test_stale_submission_cannot_complete(self):
        submitted=self.transition(self.claim(),'submit',assets=[self.asset()]);(self.root/self.input).write_text('Changed result')
        with self.assertRaisesRegex(ValueError,'changed'):self.transition(submitted,'complete',reason='Complete')
    def test_handoff_releases_ownership_with_reason(self):
        handed=self.transition(self.claim(),'handoff',reason='Quota boundary',draft_note='local-only draft')
        self.assertIsNone(handed['owner']);self.assertEqual(self.transition(handed,'claim','Boss7')['owner'],'Boss7')
    def test_symlink_task_directory_rejected(self):
        other=self.root/'outside';other.mkdir();(task.run_home(self.root,'run')/'tasks').symlink_to(other,target_is_directory=True)
        with self.assertRaisesRegex(ValueError,'symlink'):task.task_path(self.root,'run','A')
    def test_identity_namespace_keeps_old_source_registry_separate(self):
        self.git('config','wcg.curationRun','run')
        person,workspace=coordination.identity_paths(self.root,'Boss6')
        self.assertEqual(person,'curation/runs/run/people/Boss6.json')
        self.assertEqual(workspace,'curation/workspaces/run/Boss6')
        self.assertEqual(work.workspace_path(self.root,'repository-cleanup','Boss6').as_posix(),workspace)

if __name__=='__main__':unittest.main()
