"""Fixed conversation identity and authenticated write endpoint checks."""
from __future__ import annotations
import argparse,json,re,subprocess,sys,time
from pathlib import Path
import board


def config(root,key):
    return board.git(root,'config','--local','--get',key,check=False).stdout.decode().strip()


def verify_write(root,branch,tip=None):
    remote=board.git(root,'remote','get-url','origin').stdout.decode().strip()
    if board.SECRET.search(remote) or re.search(r'https?://[^/]*@',remote):raise ValueError('Origin embeds credentials')
    if tip is None:
        board.git(root,'fetch','--quiet','--no-tags','origin','refs/heads/'+branch)
        tip=board.git(root,'rev-parse','FETCH_HEAD').stdout.decode().strip()
    result=board.git(root,'push','--dry-run','--porcelain','origin',tip+':refs/heads/'+branch,check=False)
    if board.auth_rejected(result):raise board.AuthenticationError('GitHub rejected the credential/write permission. Stop retrying this credential.')
    advanced=bool(result.returncode and re.search(rb'non-fast-forward|fetch first',result.stdout+result.stderr,re.I))
    if result.returncode and not advanced:raise board.BoardError('Write check failed: '+result.stderr.decode(errors='replace')[:700])
    return {'status':'write-verified','branch':branch,'remote_advanced':advanced,'checked_at':int(time.time()),'method':'receive-pack dry-run; no remote change'}


def register(root):
    who=config(root,'wcg.actor');instance=config(root,'wcg.instance')
    if not re.fullmatch(r'Boss[1-9][0-9]*',who):raise ValueError('Use the Boss number assigned by the prompt')
    if not re.fullmatch(r'[0-9a-f]{32}',instance):raise ValueError('Missing conversation instance')
    checked=verify_write(root,config(root,'wcg.branch'));relative='cleanup/people/'+who+'.json'
    fetched=board.git(root,'show','FETCH_HEAD:'+relative,check=False);old=json.loads(fetched.stdout) if fetched.returncode==0 else {}
    if old and old.get('instance')!=instance:raise ValueError('Boss number already belongs to another conversation')
    aliases=old.get('legacy_actors',[]);legacy=config(root,'wcg.legacyActor')
    if legacy and legacy not in aliases:aliases=aliases+[legacy]
    workspace='cleanup/workspaces/'+who
    record={'boss':who,'instance':instance,'legacy_actors':aliases,'workspace':workspace,'status':'registered'}
    if old==record:return dict(checked,status='registered',actor=who)
    path=root/relative;path.parent.mkdir(exist_ok=True);path.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    result=subprocess.run([sys.executable,str(root/'tools/checkpoint.py'),'--repo',str(root),relative,workspace+'/workspace.json',workspace+'/README.md','-m','绑定明确对话身份 '+who],capture_output=True,text=True)
    if result.returncode:raise board.BoardError('Registration not confirmed; local work retained. '+result.stderr[-900:])
    receipt=json.loads(result.stdout)
    if receipt.get('status')!='pushed':raise board.BoardError('Identity remains local-only')
    return dict(checked,status='registered',actor=who,remote_tip=receipt['remote_tip'])


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('command',choices=('doctor','register'));a=p.parse_args();root=a.repo.resolve()
    try:result=register(root) if a.command=='register' else verify_write(root,config(root,'wcg.branch'))
    except (ValueError,OSError,board.BoardError) as exc:
        print(json.dumps({'status':'write-blocked','detail':board.SECRET.sub('[REDACTED]',str(exc)),'action':'Preserve local work, stop new claims and repeated identical credentials; resume after valid authorization.'},ensure_ascii=False));return 3
    print(json.dumps(result,ensure_ascii=False));return 0


if __name__=='__main__':raise SystemExit(main())
