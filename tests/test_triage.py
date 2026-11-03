"""Material triage preserves mathematical inputs and rejects stale/partial batches."""
import json
import csv
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import triage
import triage_clean

class TriageTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir=ROOT/'tests',prefix='triage-fixture-')
        self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.git('init','--quiet');self.git('config','user.name','Fixture');self.git('config','user.email','fixture@example.invalid')
        for name in ['A','B','C']:
            p=self.root/f'archives/demo/state/引理/{name}--引理.md';p.parent.mkdir(parents=True,exist_ok=True)
            p.write_text('# Precise unresolved mathematics\nFor every real x, x*x is nonnegative.\n')
        copy=self.root/'archives/demo/tools/evidence/original/archives/demo/state/引理/copy.md'
        copy.parent.mkdir(parents=True);copy.write_text('historical copy')
        self.git('add','.');self.git('commit','--quiet','-m','Original materials')
        triage.init(self.root,'test',2,'Boss6')
    def git(self,*args):
        p=subprocess.run(['git',*args],cwd=self.root,capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stderr);return p.stdout.strip()
    def batch(self):return triage.next_batch(self.root,'test',1,30,100000)
    def records(self,batch):
        return [dict(path=r['path'],sha256=r['sha256'],category='math-exposition',
                     math_subject_or_nonmath_reason='Contains a precise quantified inequality.',locator='Full body',route='retain') for r in batch['files']]
    def ingest(self,batch,records):
        triage.write(self.root/batch['record_file'],records)
        return triage.ingest(self.root,'test',batch['batch_id'],batch['record_file'])
    def test_scope_and_disjoint_lanes(self):
        h,s=triage.load(self.root,'test');self.assertEqual(len(s['files']),3)
        self.assertEqual([r['display_id'] for r in sorted(s['files'],key=lambda x:x['path'])],
                         ['P25-00001','P25-00002','P25-00003'])
        a=set(json.loads((h/'lanes/1.json').read_text()));b=set(json.loads((h/'lanes/2.json').read_text()))
        self.assertFalse(a&b);self.assertEqual(len(a|b),3)
    def test_partial_or_duplicate_batch_cannot_be_completed(self):
        b=self.batch();records=self.records(b)
        with self.assertRaisesRegex(ValueError,'missing or duplicate'):self.ingest(b,records[:-1])
        self.assertEqual(triage.status(self.root,'test')['classified'],0)
    def test_changed_source_rejected_before_any_record_is_written(self):
        b=self.batch();records=self.records(b);(self.root/records[-1]['path']).write_text('Changed assumption')
        with self.assertRaisesRegex(ValueError,'source changed'):self.ingest(b,records)
        self.assertEqual(triage.status(self.root,'test')['classified'],0)
    def test_math_cannot_be_discarded_by_classification(self):
        r=self.records(self.batch())[0];r['route']='delete'
        with self.assertRaisesRegex(ValueError,'discard mathematics'):triage.validate_record(r)
    def test_no_truth_or_graph_fields(self):
        r=self.records(self.batch())[0];r['status']='proved'
        with self.assertRaises(ValueError):triage.validate_record(r)
    def test_resume_reuses_unfinished_batch(self):
        b=self.batch();self.assertEqual(self.batch(),b)
        self.ingest(b,self.records(b));self.assertEqual(self.batch()['state'],'lane-complete')
    def test_all_materials_need_explicit_reader_decisions(self):
        for lane in (1,2):
            b=triage.next_batch(self.root,'test',lane,30,100000);self.ingest(b,self.records(b))
        result=triage.export(self.root,'test');self.assertEqual(result['remaining'],0)
        self.assertTrue((triage.run_path(self.root,'test')/'INDEX.md').is_file())
    def test_new_run_is_numbered_classification_only(self):
        home,snapshot=triage.load(self.root,'test')
        self.assertEqual(json.loads((home/'run.json').read_text())['operation_mode'],'classification-only')
        for lane in (1,2):
            batch=triage.next_batch(self.root,'test',lane,30,100000)
            records=self.records(batch)
            if lane==1:
                records[0].update(category='non-math',route='delete',math_subject_or_nonmath_reason='Only a process note.')
            self.ingest(batch,records)
        before={r['path']:(self.root/r['path']).read_bytes() for r in snapshot['files']}
        triage.export(self.root,'test')
        rows=json.loads((home/'materials.json').read_text())
        self.assertEqual({r['path']:r['display_id'] for r in rows},
                         {r['path']:f'P25-{i:05d}' for i,r in enumerate(sorted(snapshot['files'],key=lambda x:x['path']),1)})
        self.assertTrue(all(r['material_id'] for r in rows))
        with (home/'materials.csv').open(newline='') as f:csvrows=list(csv.DictReader(f))
        self.assertEqual({r['display_id'] for r in csvrows},{r['display_id'] for r in rows})
        catalog=(home/'by-archive/demo.md').read_text()
        self.assertIn('| 编号 | 材料 | 类别 | 建议去向 | 定位 |',catalog)
        self.assertIn('P25-00001',catalog)
        self.assertIn('Full body',catalog)
        self.assertIn('建议去向供第二阶段处理', (home/'INDEX.md').read_text())
        self.assertEqual(before,{r['path']:(self.root/r['path']).read_bytes() for r in snapshot['files']})
        self.assertFalse((home/'cleanup-plan.json').exists())
    def test_phase_one_cleanup_commands_and_direct_calls_are_rejected(self):
        home,_=triage.load(self.root,'test')
        for fn in (triage_clean.plan,triage_clean.apply):
            with self.assertRaisesRegex(ValueError,'phase 2'):fn(self.root,'test')
        for command in ('plan-clean','apply-clean'):
            p=subprocess.run([sys.executable,str(ROOT/'tools/triage.py'),'--repo',str(self.root),command,'--run','test'],
                             capture_output=True,text=True)
            self.assertNotEqual(p.returncode,0)
            self.assertIn('phase 2',p.stderr)
        self.assertFalse((home/'cleanup-plan.json').exists())
    def test_actor_not_invented_and_snapshot_not_overwritten(self):
        with self.assertRaisesRegex(ValueError,'explicit Boss'):triage.init(self.root,'other',2)
        with self.assertRaisesRegex(ValueError,'already exists'):triage.init(self.root,'test',2,'Boss6')
    def test_increment_reuses_only_identical_previously_read_materials(self):
        b=self.batch();records=self.records(b);self.ingest(b,records)
        changed=records[0]['path'];(self.root/changed).write_text('A different quantified claim')
        self.commit_for_increment()
        result=triage.init(self.root,'increment',2,'Boss6',carry_from='test')
        self.assertEqual(result['reused_identical_materials'],len(records)-1)
        home,snapshot=triage.load(self.root,'increment')
        row=next(r for r in snapshot['files'] if r['path']==changed)
        self.assertFalse((home/'records'/f"{row['material_id']}.json").exists())
    def commit_for_increment(self):
        self.git('add','.');self.git('commit','--quiet','-m','Incremental source change')

if __name__=='__main__':unittest.main()
