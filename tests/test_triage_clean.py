"""Cleanup removes wrappers without losing mathematical text or cited evidence."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import curation
import triage
import triage_clean as clean

class TriageCleanupTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir=ROOT/'tests',prefix='triage-clean-fixture-');self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        def git(*args):
            p=subprocess.run(['git',*args],cwd=self.root,capture_output=True,text=True)
            if p.returncode:raise RuntimeError(p.stderr)
        self.git=git;git('init','--quiet');git('config','user.name','Fixture');git('config','user.email','fixture@example.invalid')
        self.a='archives/demo/state/引理/A.md';self.b='archives/demo/state/计算/B.md';self.c='archives/demo/state/资料/C.md';self.d='archives/demo/state/计算/D.md'
        self.code='archives/demo/tools/evidence/check.py'
        for name,body in [(self.a,'For every x, x*x >= 0.\n[Audit](../计算/B.md) [Identity](../资料/C.md)\n'),
                          (self.b,'Fixed run only. [code](../../tools/evidence/check.py)\n'),
                          (self.c,'Actor and UUID only.\n'),(self.d,'Unused PASS counts only.\n'),(self.code,'# Original checker\n')]:
            p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(body)
        git('add','.');git('commit','--quiet','-m','Inputs')
        triage.init(self.root,'run',1,'Boss6');self.home,self.snap=triage.load(self.root,'run')
        batch=triage.next_batch(self.root,'run',1,30,100000)
        records=[]
        for row in batch['files']:
            cat,route=('math-exposition','retain') if row['path']==self.a else ('non-math','delete') if row['path']==self.c else ('evidence-only','attach')
            records.append(dict(path=row['path'],sha256=row['sha256'],category=cat,route=route,math_subject_or_nonmath_reason='Fixture content manually specified.',locator='Full body'))
        triage.write(self.root/batch['record_file'],records);triage.ingest(self.root,'run',batch['batch_id'],batch['record_file'])
    def test_preserves_cited_evidence_and_math_while_deleting_identity_and_unused_wrapper(self):
        plan=clean.plan(self.root,'run');self.assertEqual(plan['needed_evidence_attachments'],1)
        clean.apply(self.root,'run')
        routes=json.loads((self.home/'retired-paths.json').read_text())
        self.assertTrue((self.root/routes[self.b]).is_file())
        self.assertFalse((self.root/self.b).exists());self.assertFalse((self.root/self.c).exists());self.assertFalse((self.root/self.d).exists())
        self.assertEqual((self.root/self.code).read_text(),'# Original checker\n')
        body=(self.root/self.a).read_text();self.assertIn('For every x, x*x >= 0.',body)
        self.assertNotIn('../资料/C.md',body)
        refs=clean.references(routes[self.b],(self.root/routes[self.b]).read_text());self.assertIn(self.code,refs)
    def test_source_changes_reject_before_any_deletion(self):
        clean.plan(self.root,'run');(self.root/self.d).write_text('New mathematical content')
        with self.assertRaisesRegex(ValueError,'Stale cleanup'):clean.apply(self.root,'run')
        self.assertTrue((self.root/self.c).exists());self.assertTrue((self.root/self.b).exists())
    def test_changed_classification_invalidates_old_cleanup_plan(self):
        clean.plan(self.root,'run')
        row=next(r for r in self.snap['files'] if r['path']==self.c);p=self.home/'records'/f"{row['material_id']}.json"
        record=json.loads(p.read_text());record.update(category='mixed/needs-context',route='extract');triage.write(p,record)
        with self.assertRaisesRegex(ValueError,'Classification changed'):clean.apply(self.root,'run')
        self.assertTrue((self.root/self.c).exists())
    def test_full_reader_coverage_required(self):
        next((self.home/'records').glob('*.json')).unlink()
        with self.assertRaisesRegex(ValueError,'Finish material'):clean.plan(self.root,'run')
    def test_context_clarification_is_not_silently_deleted(self):
        row=next(r for r in self.snap['files'] if r['path']==self.c)
        p=self.home/'records'/f"{row['material_id']}.json";record=json.loads(p.read_text())
        record['route']='clarify';triage.write(p,record)
        clean.plan(self.root,'run');clean.apply(self.root,'run')
        self.assertTrue((self.root/self.c).exists())
    def test_indirect_evidence_dependency_is_preserved(self):
        # Change the fixture's frozen source consistently before making its run.
        (self.root/self.b).write_text('Fixed run [dependent record](D.md)\n')
        self.git('add',self.b);self.git('commit','--quiet','-m','Add dependency')
        triage.init(self.root,'chain',1,'Boss6');h,s=triage.load(self.root,'chain')
        for row in s['files']:
            oldrow=next(x for x in self.snap['files'] if x['path']==row['path'])
            record=json.loads((self.home/'records'/f"{oldrow['material_id']}.json").read_text());record['sha256']=row['sha256']
            triage.write(h/'records'/f"{row['material_id']}.json",record)
        self.assertEqual(clean.plan(self.root,'chain')['needed_evidence_attachments'],2)

if __name__=='__main__':unittest.main()
