"""Local Git integration tests for economical concurrent curation transactions."""
from pathlib import Path
import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import board
import curation
import curation_tasks as task


class CollaborationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir=ROOT/'tests',prefix='collaboration-fixture-')
        self.addCleanup(self.tmp.cleanup)
        self.base=Path(self.tmp.name);self.remote=self.base/'remote.git';self.root=self.base/'work';self.root.mkdir()
        self.run='fixture';self.branch='rebuild/research-v2'
        self.git(self.base,'init','--quiet','--bare',str(self.remote))
        self.git(self.root,'init','--quiet');self.git(self.root,'config','user.name','Fixture');self.git(self.root,'config','user.email','fixture@example.invalid')
        self.git(self.root,'remote','add','origin',str(self.remote));self.git(self.root,'branch','-M',self.branch)
        for key,value in {'wcg.actor':'Boss1','wcg.instance':'a'*32,'wcg.curationRun':self.run,'wcg.branch':self.branch}.items():
            self.git(self.root,'config',key,value)
        h=task.run_home(self.root,self.run);curation._write_json(h/'run.json',{'actor':'Boss1'})
        curation._write_json(h/'people/Boss1.json',{'instance':'a'*32})
        curation._write_json(h/'people/Boss2.json',{'instance':'b'*32})
        self.paths={};self.definitions={}
        for name in ['A','B']:
            path='archives/demo/state/引理/'+name+'[1].md';self.paths[name]=path
            self.write(path,('Exact '+name+'\r\n').encode())
            d={'task_id':name,'inputs':[{'path':path,'sha256':curation.digest((self.root/path).read_bytes())}],
               'write_paths':['curation/workspaces/fixture/groups/'+name],
               'question':'Which structure matters?', 'goal':'Explain the structure',
               'preserve':'Original quantifiers', 'acceptance':'Exact mathematical output', 'budget_minutes':30}
            self.definitions[name]=d
            curation._write_json(task.task_path(self.root,self.run,name),{'definition':d,'state':'available','owner':None})
        self.binary=b'Unrelated\x00data\r\n';self.write('unrelated/deep/binary.dat',self.binary)
        self.git(self.root,'add','.');self.git(self.root,'commit','--quiet','-m','Fixture seed')
        self.seed=self.git(self.root,'rev-parse','HEAD')
        self.git(self.root,'push','--quiet','origin','HEAD:refs/heads/'+self.branch)

    def git(self,cwd,*args):
        result=subprocess.run(['git',*args],cwd=cwd,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        return result.stdout.strip()

    def write(self,path,data):
        p=self.root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)

    def remote_file(self,path):
        return subprocess.check_output(['git','--git-dir',str(self.remote),'show',self.branch+':'+path])

    def remote_task(self,name):
        return json.loads(self.remote_file('curation/runs/'+self.run+'/tasks/'+name+'.json'))

    def count(self):
        return int(self.git(self.base,'--git-dir',str(self.remote),'rev-list','--count',self.branch))

    def assets(self,name):
        return [{'path':self.paths[name],'sha256':curation.digest((self.root/self.paths[name]).read_bytes())}]

    def test_thin_snapshot_keeps_full_tree_without_expanding_unrelated_files(self):
        client=board.Board(self.root,branch=self.branch)
        with client.scratch() as tmp:
            directory=Path(tmp);tip=task.checkout_task_snapshot(client,directory,self.run,'Boss1')
            self.assertFalse((directory/'unrelated/deep/binary.dat').exists())
            self.assertFalse((directory/self.paths['A']).exists())
            self.assertTrue(task.task_path(directory,self.run,'A').is_file())
            task.materialize(directory,tip,[self.paths['A']])
            self.assertEqual((directory/self.paths['A']).read_bytes(),b'Exact A\r\n')
            self.assertIn('unrelated/deep/binary.dat',self.git(directory,'ls-files'))
        task.mutate(self.root,self.run,'A','claim')
        self.assertEqual(self.remote_file('unrelated/deep/binary.dat'),self.binary)

    def test_batch_claim_and_finish_each_make_one_commit_and_allow_shared_reuse(self):
        before=self.count()
        result=task.mutate_many(self.root,self.run,[{'task_id':n,'operation':'claim'} for n in ['A','B']])
        self.assertEqual(result['status'],'pushed');self.assertEqual(self.count(),before+1)
        self.assertTrue(all(self.remote_task(n)['state']=='claimed' for n in ['A','B']))
        task.mutate_many(self.root,self.run,[{'task_id':n,'operation':'finish','assets':self.assets(n),
                         'reuse_paths':[self.paths[n]],'reason':'Exact existing mathematics reused'} for n in ['A','B']])
        self.assertEqual(self.count(),before+2)
        for n in ['A','B']:
            record=self.remote_task(n);self.assertEqual(record['state'],'completed')
            self.assertEqual(record['reused_paths'],[self.paths[n]])
            self.assertEqual(set(record['assets'][0]),{'path','sha256'})
            self.assertIsInstance(record['updated_at'],int)

    def test_one_conflict_does_not_cancel_an_unrelated_claim(self):
        ops=[{'task_id':n,'operation':'claim','write_paths':[self.paths['A']]} for n in ['A','B']]
        result=task.mutate_many(self.root,self.run,ops)
        self.assertEqual([r['status'] for r in result['results']],['pushed','conflict'])
        self.assertEqual(self.remote_task('A')['state'],'claimed')
        self.assertEqual(self.remote_task('B')['state'],'available')

    def test_handoff_all_releases_only_this_owner_in_one_commit(self):
        task.mutate_many(self.root,self.run,[{'task_id':n,'operation':'claim'} for n in ['A','B']]);before=self.count()
        result=task.mutate_many(self.root,self.run,[{'operation':'handoff-all','reason':'Actual stop','draft_note':'Shared draft paths supplied'}])
        self.assertEqual(self.count(),before+1);self.assertEqual(len(result['results']),2)
        self.assertTrue(all(self.remote_task(n)['owner'] is None for n in ['A','B']))

    def test_confirmed_request_is_idempotent_and_cannot_be_reused_for_new_intent(self):
        request='b'*32;ops=[{'task_id':'A','operation':'claim'}]
        first=task.mutate_many(self.root,self.run,ops,request_id=request);before=self.count()
        self.assertEqual(first,task.mutate_many(self.root,self.run,ops,request_id=request))
        self.assertEqual(first,task.retry_request(self.root,self.run,request));self.assertEqual(self.count(),before)
        with self.assertRaisesRegex(ValueError,'different intent'):
            task.mutate_many(self.root,self.run,[{'task_id':'B','operation':'claim'}],request_id=request)

    def test_lost_readback_recovers_the_same_request_without_a_second_commit(self):
        real=task.cleanup.refresh_snapshot;calls=0
        def refresh(client):
            nonlocal calls
            calls+=1
            if calls==2:raise board.BoardError('Transient readback failure')
            return real(client)
        before=self.count()
        with patch.object(task.cleanup,'refresh_snapshot',side_effect=refresh),patch.object(board,'retry_pause',lambda *_:None):
            result=task.mutate(self.root,self.run,'A','claim')
        self.assertEqual(result['status'],'pushed');self.assertEqual(self.count(),before+1)
        self.assertEqual(self.remote_task('A')['request_id'],result['request_id'])

    def test_real_concurrent_ref_advance_retries_receive_pack_error_and_preserves_peer_content(self):
        real=board.git;injected=False
        def git(cwd,*args,**kwargs):
            nonlocal injected
            if args[0]=='push' and '--dry-run' not in args and not injected:
                injected=True;peer=self.base/'peer'
                self.git(self.base,'clone','--quiet','--branch',self.branch,str(self.remote),str(peer))
                self.git(peer,'config','user.name','Peer');self.git(peer,'config','user.email','peer@example.invalid')
                (peer/'peer.txt').write_text('Concurrent unrelated mathematics')
                self.git(peer,'add','peer.txt');self.git(peer,'commit','--quiet','-m','Peer update')
                self.git(peer,'push','--quiet','origin','HEAD:refs/heads/'+self.branch)
                rejected=real(cwd,*args,**kwargs);self.assertNotEqual(rejected.returncode,0)
                return subprocess.CompletedProcess(args,1,rejected.stdout,
                    b"cannot lock ref 'refs/heads/rebuild/research-v2': is at aaa but expected bbb")
            return real(cwd,*args,**kwargs)
        with patch.object(board,'git',side_effect=git),patch.object(board,'retry_pause',lambda *_:None):
            result=task.mutate(self.root,self.run,'A','claim')
        self.assertTrue(injected);self.assertEqual(result['status'],'pushed')
        self.assertEqual(self.remote_file('peer.txt'),b'Concurrent unrelated mathematics')
        self.assertEqual(self.remote_task('A')['state'],'claimed')

    def test_non_race_failure_stays_pending_and_can_be_explicitly_retried(self):
        real=board.git;pushes=0
        def git(cwd,*args,**kwargs):
            nonlocal pushes
            if args[0]=='push' and '--dry-run' not in args:
                pushes+=1;return subprocess.CompletedProcess(args,1,b'',b'Unexpected non-race failure')
            return real(cwd,*args,**kwargs)
        with patch.object(board,'git',side_effect=git):
            with self.assertRaises(task.TaskWriteError):task.mutate(self.root,self.run,'A','claim')
        self.assertEqual(pushes,1)
        client=board.Board(self.root,branch=self.branch)
        intents=[p for p in (client.cache/'curation-outbox').glob('*.json') if not p.name.endswith(('.targets.json','.done.json'))];self.assertEqual(len(intents),1)
        result=task.retry_request(self.root,self.run,intents[0].stem)
        self.assertEqual(result['status'],'pushed');self.assertEqual(self.remote_task('A')['state'],'claimed')

    def test_retry_handoff_all_keeps_the_original_targets(self):
        task.mutate(self.root,self.run,'A','claim')
        real=board.git;request='c'*32
        def git(cwd,*args,**kwargs):
            if args[0]=='push' and '--dry-run' not in args:
                return subprocess.CompletedProcess(args,1,b'',b'Non-race failure')
            return real(cwd,*args,**kwargs)
        with patch.object(board,'git',side_effect=git):
            with self.assertRaises(task.TaskWriteError):
                task.mutate_many(self.root,self.run,[{'operation':'handoff-all','reason':'Stop','draft_note':'Saved'}],request_id=request)
        task.mutate(self.root,self.run,'B','claim')
        task.retry_request(self.root,self.run,request)
        self.assertEqual(self.remote_task('A')['state'],'handoff')
        self.assertEqual(self.remote_task('B')['state'],'claimed')

    def test_list_is_compact_and_full_output_remains_available(self):
        brief=task.task_list(self.root,self.run);full=task.task_list(self.root,self.run,full=True)
        self.assertNotIn('definition',brief[0]);self.assertIn('definition',full[0])
        self.assertEqual(len(task.task_list(self.root,self.run,limit=1)),1)
        self.assertEqual(task.task_status(self.root,self.run)['states'],{'available':2})

    def test_claim_next_skips_changed_input_without_rebinding_it(self):
        self.write(self.paths['A'],b'Changed mathematical premise')
        self.git(self.root,'add',self.paths['A']);self.git(self.root,'commit','--quiet','-m','Changed input')
        self.git(self.root,'push','--quiet','origin','HEAD:refs/heads/'+self.branch)
        result=task.claim_next(self.root,self.run)
        self.assertEqual(result['selection']['selected'],['B'])
        self.assertEqual(result['selection']['skipped'][0]['reason'],'input-changed')
        self.assertEqual(self.remote_task('A')['state'],'available')
        self.assertEqual(self.remote_task('A')['definition']['inputs'],self.definitions['A']['inputs'])

    def test_claim_next_skips_an_occupied_write_scope(self):
        definition=copy.deepcopy(self.definitions['A']);definition['task_id']='C'
        definition['write_paths']=self.definitions['A']['write_paths'][:]
        curation._write_json(task.task_path(self.root,self.run,'C'),
                             {'definition':definition,'state':'claimed','owner':'Boss2'})
        self.git(self.root,'add','.');self.git(self.root,'commit','--quiet','-m','Occupied scope')
        self.git(self.root,'push','--quiet','origin','HEAD:refs/heads/'+self.branch)
        result=task.claim_next(self.root,self.run)
        self.assertEqual(result['selection']['selected'],['B'])
        self.assertEqual(result['selection']['skipped'][0]['reason'],'write-scope-occupied')

    def test_claim_next_reselects_after_another_boss_wins_the_same_task(self):
        peer=self.base/'peer'
        self.git(self.base,'clone','--quiet','--branch',self.branch,str(self.remote),str(peer))
        for key,value in {'user.name':'Peer','user.email':'peer@example.invalid','wcg.actor':'Boss2',
                          'wcg.instance':'b'*32,'wcg.curationRun':self.run,'wcg.branch':self.branch}.items():
            self.git(peer,'config',key,value)
        real=board.git;injected=False
        def git(cwd,*args,**kwargs):
            nonlocal injected
            if args[0]=='push' and '--dry-run' not in args and not injected:
                injected=True;task.claim_next(peer,self.run)
            return real(cwd,*args,**kwargs)
        with patch.object(board,'git',side_effect=git),patch.object(board,'retry_pause',lambda *_:None):
            result=task.claim_next(self.root,self.run)
        self.assertEqual(result['selection']['selected'],['B'])
        self.assertEqual(self.remote_task('A')['owner'],'Boss2')
        self.assertEqual(self.remote_task('B')['owner'],'Boss1')
        self.assertEqual(self.remote_file('unrelated/deep/binary.dat'),self.binary)

    def test_claim_next_lost_readback_does_not_take_extra_tasks(self):
        real=task.cleanup.refresh_snapshot;calls=0;before=self.count()
        def refresh(client):
            nonlocal calls
            calls+=1
            if calls==2:raise board.BoardError('Lost response after successful push')
            return real(client)
        with patch.object(task.cleanup,'refresh_snapshot',side_effect=refresh),patch.object(board,'retry_pause',lambda *_:None):
            result=task.claim_next(self.root,self.run)
        self.assertEqual(result['selection']['selected'],['A'])
        self.assertEqual(self.remote_task('A')['state'],'claimed')
        self.assertEqual(self.remote_task('B')['state'],'available')
        self.assertEqual(self.count(),before+1)

    def test_claim_next_unknown_failure_retry_keeps_its_original_target(self):
        real=board.git;request='d'*32
        def git(cwd,*args,**kwargs):
            if args[0]=='push':return subprocess.CompletedProcess(args,1,b'',b'Unknown delivery failure')
            return real(cwd,*args,**kwargs)
        with patch.object(board,'git',side_effect=git):
            with self.assertRaises(task.TaskWriteError):
                task.mutate_many(self.root,self.run,[{'operation':'claim-next','limit':1}],request_id=request)
        task.mutate(self.root,self.run,'A','claim')
        result=task.retry_request(self.root,self.run,request)
        self.assertEqual(result['results'][0]['status'],'conflict')
        self.assertEqual(self.remote_task('B')['state'],'available')

    def test_claim_next_uses_actual_push_without_a_repeated_write_probe(self):
        real=board.git;probes=[];pushes=[]
        def git(cwd,*args,**kwargs):
            if args[0]=='push':
                (probes if '--dry-run' in args else pushes).append(args)
            return real(cwd,*args,**kwargs)
        with patch.object(board,'git',side_effect=git):result=task.claim_next(self.root,self.run)
        self.assertEqual(result['status'],'pushed');self.assertEqual(probes,[]);self.assertEqual(len(pushes),1)

    def test_claim_next_authentication_failure_does_not_publish_a_claim(self):
        real=board.git;pushes=[]
        def git(cwd,*args,**kwargs):
            if args[0]=='push':
                pushes.append(args);return subprocess.CompletedProcess(args,1,b'',b'Authentication failed')
            return real(cwd,*args,**kwargs)
        with patch.object(board,'git',side_effect=git):
            with self.assertRaises(board.AuthenticationError):task.claim_next(self.root,self.run)
        self.assertEqual(len(pushes),1)
        self.assertTrue(all(self.remote_task(n)['state']=='available' for n in ['A','B']))

    def test_claim_next_cli_filters_prefix_and_returns_only_the_limit(self):
        result=subprocess.run([sys.executable,str(ROOT/'tools/curation_tasks.py'),'--repo',str(self.root),
                               'claim-next','--run',self.run,'--limit','1','--prefix','B'],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(json.loads(result.stdout)['selection']['selected'],['B'])
        self.assertEqual(self.remote_task('A')['state'],'available')

    def test_owner_query_reads_published_claim_without_manual_sync(self):
        task.claim_next(self.root,self.run)
        self.assertEqual(json.loads(task.task_path(self.root,self.run,'A').read_text())['state'],'available')
        result=subprocess.run([sys.executable,str(ROOT/'tools/curation_tasks.py'),'--repo',str(self.root),
                               'list','--run',self.run,'--owner','self'],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        rows=json.loads(result.stdout)
        self.assertEqual([r['task_id'] for r in rows],['A'])
        self.assertEqual(rows[0]['state'],'claimed')

    def test_status_and_show_read_remote_without_touching_local_drafts(self):
        task.claim_next(self.root,self.run);before=self.count()
        draft=self.root/'unfinished.md';draft.write_text('A live mathematical draft')
        for command in [['status'],['show','A']]:
            result=subprocess.run([sys.executable,str(ROOT/'tools/curation_tasks.py'),'--repo',str(self.root),
                                   command[0],'--run',self.run,*command[1:]],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr);record=json.loads(result.stdout)
            if command[0]=='status':self.assertEqual(record['states'],{'claimed':1,'available':1})
            else:self.assertEqual(record['state'],'claimed')
        self.assertEqual(draft.read_text(),'A live mathematical draft')
        self.assertEqual(self.count(),before)
        self.assertEqual(self.git(self.root,'rev-parse','HEAD'),self.seed)

    def test_asset_verification_reuses_one_object_cache(self):
        client=board.Board(self.root,branch='wcg/board-fixture')
        asset=dict(branch=self.branch,commit=self.seed,**self.assets('A')[0])
        real=board.git;fetch_dirs=[]
        def git(cwd,*args,**kwargs):
            if args[0]=='fetch':fetch_dirs.append(Path(cwd))
            return real(cwd,*args,**kwargs)
        with patch.object(board,'git',side_effect=git):
            client.check_asset(asset);client.check_asset(asset)
        self.assertEqual(len(fetch_dirs),2);self.assertEqual(fetch_dirs[0],fetch_dirs[1])
        self.assertTrue((fetch_dirs[0]/'objects/info/alternates').is_file())

    def test_asset_is_checked_once_when_board_publish_retries(self):
        client=board.Board(self.root,branch='wcg/board-fixture');client.initialize()
        asset=dict(branch=self.branch,commit=self.seed,**self.assets('A')[0])
        real=board.git;rejected=False
        def git(cwd,*args,**kwargs):
            nonlocal rejected
            if args[0]=='push' and not rejected:
                rejected=True;raise board.BoardError('Transient board ref update')
            return real(cwd,*args,**kwargs)
        with patch.object(board,'git',side_effect=git),patch.object(client,'check_asset',wraps=client.check_asset) as check,patch.object(board,'retry_pause',lambda *_:None):
            event=client.publish(board.make_intent('Boss1','result',{'text':'Fixture result','asset':asset}))
        self.assertEqual(event['kind'],'result');self.assertEqual(check.call_count,1)


if __name__=='__main__':unittest.main()
