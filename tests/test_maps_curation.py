"""Admission, relation versions and historical-receipt routing on real Git bytes."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import curation
import maps
import cleanup
from vendor.matek.frontmatter import format_flat_frontmatter,parse_flat_frontmatter


class CuratedMapsTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=ROOT.parent)
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.git('init','--initial-branch=main')
        self.git('config','user.name','Fixture')
        self.git('config','user.email','fixture@example.invalid')
        self.paths={}
        for name in ('A','B','C'):
            path=self.root/f'archives/demo/state/定理/{name}--定理.md'
            path.parent.mkdir(parents=True,exist_ok=True)
            meta=dict(id='demo/'+name,kind='theorem',type_tag='定理',title=name,
                      status='complete',summary='Independent fixture claim',source_refs=['fixture-definition'])
            path.write_text(format_flat_frontmatter(meta)+'\n# '+name+'\nA precisely stated fixture claim.\n')
            self.paths[name]=path.relative_to(self.root).as_posix()
        self.git('add','.')
        self.git('commit','-m','original mathematical objects')
        curation.freeze(self.root,manifest_out=curation.DEFAULT_MANIFEST)
        self.manifest_path=self.root/curation.DEFAULT_MANIFEST
        self.manifest=json.loads(self.manifest_path.read_text())
        self.manifest['objects']=[]
        for item in self.manifest['decisions']:
            path=item['path'];name=Path(path).name[0]
            item.update(action='keep',targets=[path],reason='Statement and argument are already complete.')
            self.manifest['objects'].append(dict(path=path,sha256=item['sha256'],role='mathematics',
                object_id='demo/'+name,statement='Fixture claim '+name,conditions='Same real-variable model',
                support='The original argument is retained verbatim.',use='A premise with an independent role.',
                status='proved',dependency_scope='single-object'))
        self.save_manifest()

    def git(self,*args):
        return subprocess.check_output(['git',*args],cwd=self.root,stderr=subprocess.DEVNULL,text=True).strip()

    def save_manifest(self):
        self.manifest_path.write_text(json.dumps(self.manifest,ensure_ascii=False,indent=2)+'\n')

    def edge(self,name='joint',sources=None,targets=None,evidence=None):
        p=self.root/f'archives/demo/map/edges/{name}.md';p.parent.mkdir(parents=True,exist_ok=True)
        meta=dict(id=name,kind='implies',source_ids=sources or ['demo/A','demo/B'],
                  target_ids=targets or ['demo/C'],explanation='Both premises jointly supply the conclusion.',
                  conditions='Same model and variable instantiation',evidence=evidence or [self.paths['A']],
                  status='accepted',reviewed_by='Fixture')
        p.write_text(format_flat_frontmatter(meta)+'\nJoint argument, not two independent implications.\n')
        return p

    def seal(self,path):
        bindings=maps.fingerprints(self.root,path.relative_to(self.root).as_posix())
        meta,body=parse_flat_frontmatter(path.read_text())
        meta.update({k:v for k,v in bindings.items() if k!='limit'})
        path.write_text(format_flat_frontmatter(meta)+body)

    def test_draft_does_not_admit_without_manifest(self):
        self.manifest_path.unlink()
        with self.assertRaisesRegex(ValueError,'missing phase-2.5'):
            maps.build(self.root,draft=True)

    def test_joint_edge_preserves_all_premises_and_ignores_historical_copies(self):
        edge=self.edge();self.seal(edge)
        other=self.root/'archives/demo/tools/evidence/old/archives/demo/state/定理/A--定理.md'
        other.parent.mkdir(parents=True);other.write_text('unparseable historical source')
        historical=edge.parent.parent.parent/'tools/evidence/old/map/edges/wrong.md'
        historical.parent.mkdir(parents=True,exist_ok=True);historical.write_text('unparseable old edge')
        nodes,edges=maps.read_records(self.root)
        self.assertEqual(set(nodes),{'demo/A','demo/B','demo/C'})
        self.assertEqual(edges['joint'].source_ids,('demo/A','demo/B'))
        result=maps.build(self.root,draft=True)
        self.assertEqual(result['accepted_edges'],1)
        graph=json.loads((self.root/'map/graph.json').read_text())
        self.assertEqual(graph['edges'][0]['source_ids'],['demo/A','demo/B'])
        self.assertEqual(graph['build_status'],'draft-curated-partial')

    def test_unbound_or_changed_relation_is_not_accepted(self):
        path=self.edge()
        with self.assertRaisesRegex(ValueError,'relation-content'):
            maps.read_records(self.root)
        self.seal(path)
        path.write_text(path.read_text().replace('Joint argument','Changed argument'))
        with self.assertRaisesRegex(ValueError,'relation-content'):
            maps.read_records(self.root)

    def test_changed_endpoint_needs_both_admission_and_relation_review(self):
        path=self.edge();self.seal(path)
        original=self.root/self.paths['A'];original.write_text(original.read_text()+'New argument.\n')
        with self.assertRaisesRegex(ValueError,'admission invalid'):
            maps.read_records(self.root)
        sha=hashlib.sha256(original.read_bytes()).hexdigest()
        for row in self.manifest['objects']:
            if row['path']==self.paths['A']:row['sha256']=sha
        for row in self.manifest['decisions']:
            if row['path']==self.paths['A']:
                row.update(action='rewrite',preservation='Original assumptions and conclusion remain; argument expanded.')
        self.save_manifest()
        with self.assertRaisesRegex(ValueError,'stale endpoint'):
            maps.read_records(self.root)

    def test_changed_evidence_invalidates_relation(self):
        evidence=self.root/'archives/demo/tools/evidence/certificate.json'
        evidence.parent.mkdir(parents=True);evidence.write_text('{"exact":true}')
        name=evidence.relative_to(self.root).as_posix()
        self.manifest['objects'].append(dict(path=name,sha256=hashlib.sha256(evidence.read_bytes()).hexdigest(),
            role='evidence',owner_ids=['demo/A'],use='The exact certificate supporting premise A.'))
        decision=next(d for d in self.manifest['decisions'] if d['path']==self.paths['A'])
        decision.update(action='rewrite',targets=[self.paths['A'],name],preservation='Mathematical statement and proof unchanged; attach its exact witness.')
        self.save_manifest()
        path=self.edge(evidence=[evidence.relative_to(self.root).as_posix()]);self.seal(path)
        maps.read_records(self.root)
        evidence.write_text('{"exact":false}')
        self.manifest['objects'][-1]['sha256']=hashlib.sha256(evidence.read_bytes()).hexdigest()
        self.save_manifest()
        with self.assertRaisesRegex(ValueError,'stale evidence'):
            maps.read_records(self.root)

    def test_bundle_cannot_be_used_as_independent_logical_endpoint(self):
        path=self.edge();self.seal(path)
        self.manifest['objects'][0]['dependency_scope']='bundle-pending-split';self.save_manifest()
        with self.assertRaisesRegex(ValueError,'split bundle'):
            maps.read_records(self.root)

    def test_impact_requests_review_and_does_not_assign_falsity(self):
        first=self.edge('one',sources=['demo/A'],targets=['demo/C']);self.seal(first)
        alternate=self.edge('alternative',sources=['demo/B'],targets=['demo/C']);self.seal(alternate)
        result=maps.impact(self.root,['demo/A'])
        self.assertEqual(result['status'],'needs-review-not-refuted')
        self.assertIn('demo/C',result['downstream_review_objects'])
        self.assertNotIn('false',result)

    def test_unknown_relation_kind_cannot_bypass_logical_gate(self):
        path=self.edge();meta,body=parse_flat_frontmatter(path.read_text())
        meta['kind']='entails';path.write_text(format_flat_frontmatter(meta)+body);self.seal(path)
        with self.assertRaisesRegex(ValueError,'register the semantics'):
            maps.read_records(self.root)

    def test_unproved_premise_requires_conditional_relation_not_target_status_change(self):
        path=self.edge()
        self.manifest['objects'][0]['status']='conjecture';self.save_manifest();self.seal(path)
        with self.assertRaisesRegex(ValueError,'explicit conditional'):
            maps.read_records(self.root)
        meta,body=parse_flat_frontmatter(path.read_text());meta['relation_mode']='conditional'
        path.write_text(format_flat_frontmatter(meta)+body);self.seal(path)
        nodes,edges=maps.read_records(self.root)
        self.assertEqual(nodes['demo/C'].attributes['knowledge_status'],'proved')
        self.assertEqual(edges['joint'].attributes['open_premises'],('demo/A',))
        self.assertFalse(edges['joint'].attributes['asserts_endpoint_truth'])

    def test_unadmitted_workflow_file_is_not_relation_evidence(self):
        path=self.root/'workflow.txt';path.write_text('We ran the program and it passed.')
        edge=self.edge(evidence=['workflow.txt']);self.seal(edge)
        with self.assertRaisesRegex(ValueError,'not admitted mathematics'):
            maps.read_records(self.root)

    def test_graph_scope_symlink_cannot_overwrite_external_snapshot(self):
        outside=tempfile.TemporaryDirectory(dir=ROOT.parent);self.addCleanup(outside.cleanup)
        external=Path(outside.name);target=external/'graph.json';target.write_text('preserve external graph')
        (self.root/'archives/demo/map').symlink_to(external,target_is_directory=True)
        with self.assertRaisesRegex(ValueError,'escapes|symlink'):
            maps.build(self.root,draft=True)
        self.assertEqual(target.read_text(),'preserve external graph')

    def test_node_change_after_admission_check_is_detected(self):
        original_check=curation.check
        def change_after_check(*args,**kwargs):
            result=original_check(*args,**kwargs)
            node=self.root/self.paths['A'];node.write_text(node.read_text()+'Changed after check.\n')
            return result
        with patch('curation.check',side_effect=change_after_check):
            with self.assertRaisesRegex(ValueError,'bytes changed during graph read'):
                maps.read_records(self.root)

    def test_build_does_not_write_old_status_after_manifest_changes(self):
        def change_during_source_gate(root):
            self.manifest['objects'][0]['status']='gap';self.save_manifest()
            return {}
        with patch('cleanup.inventory',return_value=[]),patch('cleanup.stats',return_value={'local_source_hold':0}),patch('cleanup.curation_target_routes',side_effect=change_during_source_gate):
            with self.assertRaisesRegex(ValueError,'inputs changed during build'):
                maps.build(self.root,draft=False)
        self.assertFalse((self.root/'map/graph.json').exists())

    def test_freshness_expires_when_admission_status_changes(self):
        maps.build(self.root,draft=True)
        self.assertTrue(maps.freshness(self.root)['fresh'])
        self.manifest['objects'][0]['status']='gap';self.save_manifest()
        self.assertFalse(maps.freshness(self.root)['fresh'])

    def test_freshness_includes_changes_to_the_source_completion_gate(self):
        maps.build(self.root,draft=True)
        receipt=self.root/'cleanup/progress/source.json';receipt.parent.mkdir(parents=True)
        receipt.write_text('{"disposition":"needs-decision"}')
        self.assertFalse(maps.freshness(self.root)['fresh'])


class RetiredReceiptTests(unittest.TestCase):
    # Keep these methods separate from the graph cases: the historical target
    # must be a real completed source receipt in the immutable baseline.
    git=CuratedMapsTests.git
    save_manifest=CuratedMapsTests.save_manifest
    def setUp(self):
        CuratedMapsTests.setUp(self)
        (self.root/curation.DEFAULT_BASELINE).unlink();self.manifest_path.unlink()
        self.retired='archives/demo/state/资料/workspace--资料.md'
        old=self.root/self.retired;old.parent.mkdir(parents=True,exist_ok=True)
        meta=dict(id='demo/workspace',kind='metadata',type_tag='资料',title='Workspace identity',
                  status='metadata-only',summary='No mathematical content')
        old.write_text(format_flat_frontmatter(meta)+'\nOnly an actor and workspace UUID.\n')
        self.receipt=dict(id='old-source',source_sha256='1'*64,owner='Fixture',disposition='retained',
             full_file_reviewed=True,related_material_checked=True,unique_content_accounted_for=True,
             read_note='Read the original',comparison_note='Only routing identity',decision_note='Metadata only',targets=[self.retired])
        receipt_path=self.root/'cleanup/progress/old-source.json';receipt_path.parent.mkdir(parents=True)
        receipt_path.write_text(json.dumps(self.receipt))
        self.git('add',self.retired,'cleanup/progress/old-source.json');self.git('commit','-m','original completed metadata receipt')
        curation.freeze(self.root,manifest_out=curation.DEFAULT_MANIFEST)
        self.manifest=json.loads(self.manifest_path.read_text())
        self.manifest['objects']=[]
        for item in self.manifest['decisions']:
            if item['path']==self.retired:
                item.update(action='delete',delete_kind='non-mathematical',targets=[],reason='Only identity metadata; no mathematics to preserve.')
            else:
                path=item['path'];name=Path(path).name[0]
                item.update(action='keep',targets=[path],reason='Independent mathematical claim retained.')
                self.manifest['objects'].append(dict(path=path,sha256=item['sha256'],role='mathematics',
                    object_id='demo/'+name,statement='Fixture '+name,conditions='Same real-variable model',
                    support='Original complete argument.',use='An independent mathematical premise.',
                    status='proved',dependency_scope='single-object'))
        old.unlink();self.save_manifest()

    def test_old_receipt_resolves_reviewed_nonmathematical_deletion(self):
        cleanup.validate_receipt(self.root,self.receipt)

    def test_new_receipt_cannot_claim_a_deleted_old_delivery(self):
        forged=dict(self.receipt,id='new-source')
        with self.assertRaisesRegex(ValueError,'Only a completed receipt'):
            cleanup.validate_receipt(self.root,forged)

    def test_source_binding_change_cannot_reuse_historical_route(self):
        forged=dict(self.receipt,source_sha256='2'*64)
        with self.assertRaisesRegex(ValueError,'Only a completed receipt'):
            cleanup.validate_receipt(self.root,forged)


if __name__=='__main__':unittest.main()
