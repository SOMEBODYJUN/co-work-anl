"""Reset unfinished coordination and the live board, preserving verified deliveries."""
from __future__ import annotations
import argparse,hashlib,json,shutil,time,uuid
from pathlib import Path
import board,cleanup
from coordination import config,verify_write


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def inspect(root):
    rows={r['id']:r for r in cleanup.inventory(root)};done=[];pending=[];targets={}
    for path in sorted((root/'cleanup/progress').glob('*.json')):
        if path.relative_to(root).as_posix() not in cleanup.tracked_state(root):continue
        record=json.loads(path.read_text())
        if record.get('disposition') in cleanup.COMPLETE:
            cleanup.validate_receipt(root,record)
            if record.get('source_sha256')!=rows[record['id']]['sha256'] or not record.get('owner'):
                raise ValueError('Completed record is not bound to its frozen source and owner: '+record['id'])
            done.append({'id':record['id'],'path':path.relative_to(root).as_posix(),'sha256':digest(path)})
            for name in record.get('targets',[]):
                name=name.split('#')[0];targets[name]=digest(root/name)
        else:
            pending.append({'path':path.relative_to(root).as_posix(),'previous_owner':record.get('owner'),'disposition':record.get('disposition')})
    remove=[];protected=list(targets)
    workspaces=root/'cleanup/workspaces'
    if workspaces.exists():
        for path in sorted(workspaces.iterdir()):
            relative=path.relative_to(root).as_posix()
            if not any(p==relative or p.startswith(relative+'/') for p in protected):remove.append(relative)
    return {'done_count':len(done),'unfinished_records':pending,'unfinished_count':len(pending),
            'preserved_receipts':done,'preserved_targets':targets,'remove_temporary_workspaces':remove,
            'scope':'Reset task reservations, temporary coordination workspaces and live board. Preserve source inventory, mathematical deliveries and Git history.'}


def prepare_result(root,actor,board_tip):
    report=inspect(root);reset_id=uuid.uuid4().hex
    for item in report['unfinished_records']:(root/item['path']).unlink()
    for name in report['remove_temporary_workspaces']:
        path=root/name
        if path.is_symlink():path.unlink()
        elif path.is_dir():shutil.rmtree(path)
        else:path.unlink()
    # Actor bindings are coordination state; completed provenance stays in receipts.
    people=root/'cleanup/people'
    if people.exists():
        if any(p.startswith('cleanup/people/') for p in report['preserved_targets']):
            raise ValueError('A completed delivery references the identity registry; review before reset')
        shutil.rmtree(people)
    cleanup.coverage(root)
    for item in report['preserved_receipts']:
        if digest(root/item['path'])!=item['sha256']:raise ValueError('Completed receipt changed during reset')
    for name,sha in report['preserved_targets'].items():
        if digest(root/name)!=sha:raise ValueError('Delivered target changed during reset: '+name)
    report.update(reset_id=reset_id,actor=actor,old_board_tip=board_tip,
                  original_result_tip=board.git(root,'rev-parse','HEAD').stdout.decode().strip(),created_at=int(time.time()))
    (root/'cleanup/reset-receipt.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    (root/'cleanup/RESET.md').write_text('# 协作重置\n\n保留'+str(report['done_count'])+'条已交付处置及其正文/证据；清空未完成认领与未被完成成果引用的临时工作区。\n\n旧公屏当前消息清空，新公屏从完成成果摘要开始；历史提交保留可回滚。具体指纹与旧提交见reset-receipt.json。新对话按提示词显式编号登记后再认领。\n')
    return report


def clean_local(root):
    committed=board.git(root,'show','HEAD:cleanup/reset-receipt.json',check=False)
    if committed.returncode:return {'status':'no-reset-receipt','archived_files':0}
    receipt=json.loads(committed.stdout);tracked={p.decode() for p in board.git(root,'ls-files','-z').stdout.split(b'\0') if p}
    candidates=[root/item['path'] for item in receipt.get('unfinished_records',[])]
    for name in receipt.get('remove_temporary_workspaces',[]):
        path=root/name
        if path.is_symlink() or path.is_file():candidates.append(path)
        elif path.is_dir():candidates.extend(p for p in path.rglob('*') if p.is_file() or p.is_symlink())
    common=board.git(root,'rev-parse','--git-common-dir').stdout.decode().strip()
    backup=(root/common).resolve()/'reset-backups'/receipt['reset_id'];archived=[]
    for path in sorted(set(candidates)):
        relative=path.relative_to(root).as_posix()
        if relative in tracked or not (path.exists() or path.is_symlink()):continue
        if not relative.startswith(('cleanup/progress/','cleanup/workspaces/')) or '..' in Path(relative).parts:
            raise ValueError('Reset backup path outside the authorized coordination area')
        if not path.parent.resolve().is_relative_to(root.resolve()):raise ValueError('Reset backup crosses a symlink boundary')
        target=backup/relative;target.parent.mkdir(parents=True,exist_ok=True)
        if target.exists() or target.is_symlink():target=target.with_name(target.name+'.'+uuid.uuid4().hex)
        shutil.move(str(path),str(target));archived.append(relative)
    for name in receipt.get('remove_temporary_workspaces',[]):
        path=root/name
        if path.is_dir() and not path.is_symlink():
            for directory in sorted((p for p in path.rglob('*') if p.is_dir() and not p.is_symlink()),key=lambda p:len(p.parts),reverse=True)+[path]:
                try:directory.rmdir()
                except OSError:pass
    return {'status':'local-reset-copies-archived','archived_files':len(archived),'backup':str(backup)}


def apply(root,actor):
    branch=config(root,'wcg.branch') or 'rebuild/research-v2';chat=config(root,'wcg.boardBranch') or 'wcg/board-cleanup-20261028'
    if branch==chat:raise ValueError('Result and board branches must differ')
    client=board.Board(root,branch=branch)
    with client.scratch() as name:
        directory=Path(name);client.setup(directory)
        board.git(directory,'fetch','--quiet','--no-tags','--depth=1','origin',
                  '+refs/heads/'+branch+':refs/remotes/origin/result',
                  '+refs/heads/'+chat+':refs/remotes/origin/chat')
        result_tip=board.git(directory,'rev-parse','refs/remotes/origin/result').stdout.decode().strip()
        chat_tip=board.git(directory,'rev-parse','refs/remotes/origin/chat').stdout.decode().strip()
        verify_write(directory,branch,result_tip)
        board.git(directory,'checkout','--quiet','--detach',result_tip)
        rules=directory/'cleanup/coordination.json'
        if not rules.exists() or actor not in json.loads(rules.read_text()).get('coordinators',[]):
            raise ValueError('Deploy the reviewed program/policy first; reset requires its named coordinator')
        report=prepare_result(directory,actor,chat_tip)
        board.git(directory,'add','-A','--','cleanup')
        board.git(directory,'commit','--quiet','-m','协作重置：保留已交付成果，清空未完成预约 '+report['reset_id'])
        result_commit=board.git(directory,'rev-parse','HEAD').stdout.decode().strip()
        receipt_sha=digest(directory/'cleanup/reset-receipt.json')
        board.git(directory,'checkout','--quiet','--detach',chat_tip)
        prefix=directory/board.PREFIX
        if prefix.is_symlink():raise ValueError('Board path must be ordinary')
        if prefix.exists():shutil.rmtree(prefix)
        board_client=board.Board(root,branch=chat);board_client.write_empty(directory)
        text=('协作已重置。保留'+str(report['done_count'])+'条通过处置字段、冻结指纹和目标文件检查的已交付记录及正文/证据；未完成认领归零。'
              '这不等于重新证明所有数学。新对话按提示词明确Boss编号并完成写权限检查后领取。成果与指纹清单：结果提交'+result_commit+'的cleanup/reset-receipt.json。')
        asset={'branch':branch,'commit':result_commit,'path':'cleanup/reset-receipt.json','sha256':receipt_sha}
        intent=board.make_intent(actor,'result',{'text':text,'save':'repository-cleanup','thread':'rebuild-v2','asset':asset},report['reset_id'])
        event=dict(intent,schema=board.SCHEMA,seq=1,time=int(time.time()));state=board.transition(board.empty_state(),event)
        (prefix/'events'/('00000001_'+event['id']+'.json')).write_text(board.encode(event))
        (prefix/'BOARD.md').write_text(board.render(state))
        board.git(directory,'add','-A','--',str(board.PREFIX));board.git(directory,'commit','--quiet','-m','重置当前公屏，仅保留已交付成果入口 '+report['reset_id'])
        chat_commit=board.git(directory,'rev-parse','HEAD').stdout.decode().strip()
        pushed=board.git(directory,'push','--atomic','--quiet','origin',
                         result_commit+':refs/heads/'+branch,chat_commit+':refs/heads/'+chat,check=False)
        if board.auth_rejected(pushed):raise board.AuthenticationError('Credential rejected; no reset success is confirmed')
        if pushed.returncode:raise board.BoardError('Atomic reset not confirmed; no success reported. '+pushed.stderr.decode(errors='replace')[:700])
        board.git(directory,'fetch','--quiet','--no-tags','origin',
                  '+refs/heads/'+branch+':refs/remotes/origin/result',
                  '+refs/heads/'+chat+':refs/remotes/origin/chat')
        receipt=json.loads(board.git(directory,'show','refs/remotes/origin/result:cleanup/reset-receipt.json').stdout)
        if receipt.get('reset_id')!=report['reset_id']:raise ValueError('Remote reset receipt differs; check actual state')
        message=board.git(directory,'show','refs/remotes/origin/chat:'+str(board.PREFIX/'events'/('00000001_'+event['id']+'.json')))
        if json.loads(message.stdout)['id']!=event['id']:raise ValueError('Remote board confirmation differs')
        return {'status':'pushed','reset_id':report['reset_id'],'result_commit':result_commit,'board_commit':chat_commit,
                'preserved_done':report['done_count'],'removed_unfinished_records':report['unfinished_count'],'board_events_after_reset':1}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True)
    p.add_argument('command',choices=('plan','apply','clean-local'));p.add_argument('--actor',default='Boss32');p.add_argument('--out',type=Path)
    a=p.parse_args();root=a.repo.resolve()
    try:
        report=inspect(root) if a.command=='plan' else clean_local(root) if a.command=='clean-local' else apply(root,a.actor)
        if a.command=='plan':report.update(status='plan-only-not-applied',source_tip=board.git(root,'rev-parse','HEAD').stdout.decode().strip(),board_policy='Replace current chat by one verified-delivery entry; preserve Git history')
        if a.out:a.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps({k:v for k,v in report.items() if k not in ('preserved_receipts','preserved_targets','unfinished_records')},ensure_ascii=False,indent=2));return 0
    except (ValueError,OSError,board.BoardError) as exc:
        print(json.dumps({'status':'not-confirmed','detail':board.SECRET.sub('[REDACTED]',str(exc))},ensure_ascii=False));return 3


if __name__=='__main__':raise SystemExit(main())
