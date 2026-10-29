"""Real-Git tests for the new target tree, claims, source access and hypergraphs."""
import concurrent.futures, hashlib, json, os, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BRANCH='rebuild/research-v2'


def git(cwd,*args):
    env=dict(os.environ)
    for k in ('GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE','GIT_COMMON_DIR','GIT_ASKPASS','WCG_WORK_ASKPASS','WCG_CHECKPOINT_ASKPASS','WCG_CHECKPOINT_TOKEN_FILE'):
        env.pop(k,None)
    r=subprocess.run(['git',*args],cwd=cwd,capture_output=True,text=True,env=env,timeout=45)
    if r.returncode:raise AssertionError(r.stderr)
    return r.stdout.strip()


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        common=ROOT/'.git'
        self.tmp=tempfile.TemporaryDirectory(dir=common,prefix='workflow-test-');self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name);self.remote=self.base/'remote.git';self.seed=self.base/'seed';self.seed.mkdir()
        git(self.base,'init','--bare',str(self.remote));git(self.seed,'init','--initial-branch=main')
        for key,value in [('user.name','Fixture'),('user.email','fixture@example.invalid')]:git(self.seed,'config',key,value)
        git(self.seed,'remote','add','origin',str(self.remote))
        (self.seed/'raw').mkdir();(self.seed/'raw/a.md').write_text('source A: full mathematical content\n');(self.seed/'raw/b.md').write_text('source B: later correction\n')
        git(self.seed,'add','.');git(self.seed,'commit','-m','raw source');source=git(self.seed,'rev-parse','HEAD')
        shutil.copy2(ROOT/'work.py',self.seed/'work.py');shutil.copytree(ROOT/'tools',self.seed/'tools',ignore=shutil.ignore_patterns('__pycache__'))
        (self.seed/'cleanup').mkdir();rows=[]
        for name in ['raw/a.md','raw/b.md']:
            data=(self.seed/name).read_bytes();oid=git(self.seed,'rev-parse',source+':'+name)
            rows.append({'id':hashlib.sha256(name.encode()).hexdigest()[:20],'path':name,'blob':oid,'sha256':hashlib.sha256(data).hexdigest(),'sources':[{'name':'fixture','commit':source,'path':name}]})
        self.ids=[r['id'] for r in rows]
        data=''.join(json.dumps(r)+'\n' for r in rows).encode();(self.seed/'cleanup/inventory.jsonl').write_bytes(data)
        (self.seed/'cleanup/sources.json').write_text(json.dumps({'inventory_sha256':hashlib.sha256(data).hexdigest(),'snapshots':[{'commit':source}]}))
        for nid in ['A','B','C']:
            self.node(self.seed,nid)
        (self.seed/'archives/demo/map/edges').mkdir(parents=True)
        for p in ['prompts/02-clean.md','prompts/03-map.md','prompts/README.md','tools/README.md','cleanup/README.md']:
            dest=self.seed/p;dest.parent.mkdir(exist_ok=True);dest.write_text('# fixture\n')
        child=self.seed/'archives/facility-games/subarchives/common-two'
        child.mkdir(parents=True);(child/'README.md').write_text('# child problem\n')
        git(self.seed,'add','.');git(self.seed,'commit','-m','result scaffold');git(self.seed,'push','origin','main');git(self.seed,'push','origin','main:refs/heads/'+BRANCH)
        self.a=self.start('A');self.b=self.start('B')

    def node(self,root,nid):
        p=root/f'archives/demo/state/定理/{nid}--定理.md';p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text('---\nid: "demo/'+nid+'"\nkind: "theorem"\ntype_tag: "定理"\ntitle: "'+nid+'"\nstatus: "candidate"\nsummary: "test object"\n---\n\n# test mathematical object\n')
        return p.relative_to(root).as_posix()

    def work(self,repo,*args):
        env=dict(os.environ)
        for key in ('GIT_ASKPASS','WCG_WORK_ASKPASS','WCG_CHECKPOINT_ASKPASS','WCG_CHECKPOINT_TOKEN_FILE'):env.pop(key,None)
        return subprocess.run([sys.executable,str(ROOT/'work.py'),'--repo',str(repo),*args],cwd=self.base,env=env,capture_output=True,text=True,timeout=45)

    def start(self,actor,role='cleaner'):
        repo=self.base/actor
        r=self.work(repo,'start','--remote',str(self.remote),'--actor',actor,'--role',role)
        self.assertEqual(r.returncode,0,r.stderr);receipt=json.loads(r.stdout)
        self.assertEqual(receipt['branch'],BRANCH);self.assertEqual(receipt['save'],'repository-cleanup')
        return repo

    def claim(self,repo,sid):
        r=self.work(repo,'clean','claim',sid);self.assertEqual(r.returncode,0,r.stderr);self.assertEqual(json.loads(r.stdout)['status'],'pushed')

    def record(self,repo,sid,targets=None):
        p=self.base/(repo.name+'-receipt.json')
        p.write_text(json.dumps({'id':sid,'full_file_reviewed':True,'related_material_checked':True,'unique_content_accounted_for':True,'read_note':'Read all content','comparison_note':'Compared A with later source B','decision_note':'Preserved unique assumptions and correction','disposition':'integrated','targets':targets or ['archives/demo/state/定理/A--定理.md']}))
        return self.work(repo,'clean','done','--record-file',str(p))

    def test_defaults_mapper_and_no_extra_branch(self):
        r=self.start('M',role='mapper');receipt=json.loads(self.work(r,'start','--remote',str(self.remote)).stdout)
        self.assertEqual(receipt['context_entry'],'prompts/03-map.md')
        self.assertEqual(set(git(self.remote,'for-each-ref','--format=%(refname:short)','refs/heads').splitlines()),{'main',BRANCH})

    def test_research_subarchive_is_explicit_and_stable(self):
        repo=self.base/'F'
        r=self.work(repo,'start','--remote',str(self.remote),'--save','facility-games','--subarchive','common-two','--role','boss')
        self.assertEqual(r.returncode,0,r.stderr);receipt=json.loads(r.stdout)
        self.assertEqual(receipt['subarchive'],'common-two')
        self.assertEqual(receipt['context_entry'],'archives/facility-games/subarchives/common-two/README.md')
        self.assertIn('subarchives/common-two/workspaces/',receipt['workspace']['path'])
        again=self.work(repo,'start','--remote',str(self.remote));self.assertEqual(again.returncode,0,again.stderr)
        self.assertEqual(json.loads(again.stdout)['subarchive'],'common-two')
        self.assertNotEqual(self.work(repo,'start','--remote',str(self.remote),'--subarchive','other').returncode,0)

    def test_concurrent_claim_has_one_owner(self):
        with concurrent.futures.ThreadPoolExecutor(2) as pool:
            out=list(pool.map(lambda repo:self.work(repo,'clean','claim',self.ids[0]),[self.a,self.b]))
        self.assertEqual(sum(r.returncode==0 for r in out),1,[r.stderr for r in out])
        owner=json.loads(git(self.remote,'show',BRANCH+':cleanup/progress/'+self.ids[0]+'.json'))['owner']
        self.assertIn(owner,['A','B'])

    def test_done_requires_pushed_target_and_updates_checkbox(self):
        self.claim(self.a,self.ids[0]);bad=self.record(self.a,self.ids[0],['archives/demo/not-pushed.md'])
        self.assertNotEqual(bad.returncode,0);self.assertIn('already be pushed',bad.stderr)
        good=self.record(self.a,self.ids[0]);self.assertEqual(good.returncode,0,good.stderr)
        self.assertEqual(json.loads(good.stdout)['status'],'pushed')
        self.assertIn('- [x]',git(self.remote,'show',BRANCH+':cleanup/checklists/0001.md'))
        self.assertEqual(self.work(self.b,'sync').returncode,0)
        self.assertEqual(json.loads(self.work(self.b,'clean','status').stdout)['completed'],1)

    def test_other_actor_cannot_complete_or_release_claim(self):
        self.claim(self.a,self.ids[0])
        self.assertNotEqual(self.record(self.b,self.ids[0]).returncode,0)
        self.assertNotEqual(self.work(self.b,'clean','release',self.ids[0]).returncode,0)

    def test_source_hash_and_inventory_are_checked(self):
        r=self.work(self.a,'clean','show',self.ids[0]);self.assertEqual(r.returncode,0,r.stderr);self.assertIn('source A',r.stdout)
        found=self.work(self.a,'clean','search','full mathematical');self.assertEqual(found.returncode,0,found.stderr)
        self.assertEqual(json.loads(found.stdout)[0]['id'],self.ids[0])
        with (self.a/'cleanup/inventory.jsonl').open('a') as f:f.write('\n')
        self.assertNotEqual(self.work(self.a,'clean','status').returncode,0)

    def test_multi_source_edge_and_stage_gate(self):
        edge=self.a/'archives/demo/map/edges/joint.md'
        edge.parent.mkdir(parents=True,exist_ok=True)
        edge.write_text('---\nid: "joint"\nkind: "implies"\nsource_ids:\n  - "demo/A"\n  - "demo/B"\ntarget_ids:\n  - "demo/C"\nexplanation: "A supplies the object; B supplies its missing condition"\nconditions: "Both premises under the same model"\nevidence:\n  - "archives/demo/state/定理/A--定理.md"\nstatus: "accepted"\nreviewed_by: "A"\n---\n\nA and B are jointly needed; neither is claimed sufficient alone.\n')
        r=self.work(self.a,'map','check');self.assertEqual(r.returncode,0,r.stderr)
        self.assertNotEqual(self.work(self.a,'map','build').returncode,0)
        r=self.work(self.a,'map','build','--draft');self.assertEqual(r.returncode,0,r.stderr)
        graph=json.loads((self.a/'map/graph.json').read_text())
        self.assertEqual(graph['edges'][0]['source_ids'],['demo/A','demo/B']);self.assertEqual(graph['build_status'],'draft-scaffold')
        text=edge.read_text().replace('explanation: "A supplies the object; B supplies its missing condition"','explanation: ""')
        edge.write_text(text);self.assertNotEqual(self.work(self.a,'map','check').returncode,0)

    def test_isolated_objects_are_allowed(self):
        r=self.work(self.a,'map','check');self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(json.loads(r.stdout)['nodes'],3);self.assertEqual(json.loads(r.stdout)['edges'],0)

    def test_scoped_checkpoint_preserves_other_work_and_uses_result_branch(self):
        before=git(self.remote,'rev-parse','main')
        path=self.node(self.a,'D')
        (self.a/'unrelated-draft.md').write_text('keep this local\n')
        r=self.work(self.a,'checkpoint',path,'-m','new mathematical object')
        self.assertEqual(r.returncode,0,r.stderr);receipt=json.loads(r.stdout)
        self.assertEqual(receipt['status'],'pushed');self.assertEqual(receipt['assets'][0]['asset']['branch'],BRANCH)
        self.assertEqual(git(self.remote,'rev-parse','main'),before)
        self.assertEqual((self.a/'unrelated-draft.md').read_text(),'keep this local\n')
        (self.a/'raw/b.md').unlink()
        r=self.work(self.a,'checkpoint','raw/b.md','-m','retire redundant target copy')
        self.assertEqual(r.returncode,0,r.stderr);self.assertEqual(json.loads(r.stdout)['assets'],[])
        # Frozen source is still readable after target deletion.
        self.assertEqual(self.work(self.a,'clean','show',self.ids[1]).returncode,0)

if __name__=='__main__':unittest.main(verbosity=2)
