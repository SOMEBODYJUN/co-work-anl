#!/usr/bin/env python3
"""Build fixed-commit HALF(5) handoff; this is not a mathematical audit."""
from __future__ import annotations
import argparse,ast,hashlib,json,re,subprocess,tarfile,zipfile
from collections import Counter
from datetime import datetime,timezone
from pathlib import Path,PurePosixPath
BASE='82e7d5e5306320e838a2421e698be894141daa98'
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'customer_attraction/model.py').is_file())
PREFIX='Q-CAG-HALF-5/'
A='research/workspaces/customer-attraction/'
DOCS=['00_PROMPT_ZH.md','01_START_HERE_ZH.md','02_FIVE_PLAYER_STATE_ZH.md','03_ASSET_GUIDE_ZH.md','04_REPRODUCTION_ZH.md']
CORE=['research/current/customer_attraction/model.md',
 'research/current/customer_attraction/two_remaining_tax.md',
 'research/current/customer_attraction/four_remaining_profit_bound.md',
 A+'R-a27734a8bba345cbb5fad186c120d0bf/five_closure/root_copy_reply_rigidity.md',
 A+'R-a27734a8bba345cbb5fad186c120d0bf/five_structure/max_theme_root_capacity.md',
 A+'R-ae18a85a07214b22b7b9d614c34779e0/dual/README.md',
 A+'R-ae18a85a07214b22b7b9d614c34779e0/countersearch/shared_root_independent_review.md']
EXTRA={'AGENTS.md','README.md','RESEARCH_STATE.md','CLAIMS.md','FAILED_ROUTES.md',
 'research/current/claims.md','research/review_status.json','research/assets.json','research/graph.json',
 'tests/__init__.py','tests/audits/__init__.py'}
SECRETS=re.compile(rb'(?:github_pat_|gh[pousr]_)[A-Za-z0-9_]{12,}')
VERIFY='''#!/usr/bin/env python3
"""Verify unpacked file identity, not mathematical validity."""
from pathlib import Path,PurePosixPath
import hashlib,json
root=Path(__file__).resolve().parent
m=json.loads((root/'MANIFEST.json').read_text(encoding='utf-8')); expected=set()
for e in m['files']:
 n=e['path']; p=PurePosixPath(n)
 assert not p.is_absolute() and '..' not in p.parts,n
 expected.add(n); f=root/n
 assert f.is_file() and not f.is_symlink(),n
 b=f.read_bytes()
 assert len(b)==e['size_bytes'],n
 assert hashlib.sha256(b).hexdigest()==e['sha256'],n
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
assert actual==expected|{'MANIFEST.json'},(actual-expected-{'MANIFEST.json'},expected-actual)
print(json.dumps({'status':'verified','files':len(expected),'source_commit':m['source_commit'],'mathematical_review':False}))
'''
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def category(p):
 for prefix,label in [(A,'personal_topic_assets'),('research/current/customer_attraction/','shared_mathematics'),
  ('research/customer_attraction/','topic_navigation'),('evidence/','evidence'),('tests/','tests_and_audits'),
  ('examples/','instances'),('customer_attraction/','solver'),('research/reviews/','shared_reviews')]:
  if p.startswith(prefix):return label
 return 'metadata_or_dependency'
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
 tree={}
 for rec in git('ls-tree','-rz','--full-tree',BASE).split(b'\0'):
  if rec:
   info,name=rec.split(b'\t',1);mode,kind,oid=info.decode().split()
   if kind=='blob':tree[name.decode()]=(mode,oid)
 selected={p for p in tree if 'customer_attraction' in p or p.startswith(A)}|(EXTRA&tree.keys())
 assert set(CORE)<=selected
 process=subprocess.Popen(['git','archive','--format=tar',BASE],cwd=ROOT,stdout=subprocess.PIPE)
 original={}
 with tarfile.open(fileobj=process.stdout,mode='r|*') as tar:
  for member in tar:
   if member.isfile():original[member.name]=tar.extractfile(member).read()
 assert process.wait()==0
 added=set();scanned=set();failures=[]
 while True:
  todo=[p for p in selected-scanned if p.endswith('.py')]
  if not todo:break
  for p in todo:
   scanned.add(p)
   try:syntax=ast.parse(original[p].decode('utf-8-sig'))
   except (UnicodeDecodeError,SyntaxError):failures.append(p);continue
   imports=set()
   for n in ast.walk(syntax):
    if isinstance(n,ast.Import):imports.update(a.name for a in n.names)
    elif isinstance(n,ast.ImportFrom) and not n.level and n.module:
     imports.add(n.module);imports.update(n.module+'.'+a.name for a in n.names if a.name!='*')
   for name in imports:
    path=name.replace('.','/');deps={path+'.py',path+'/__init__.py'}&tree.keys()
    if deps:
     bits=path.split('/');deps|={'/'.join(bits[:i])+'/__init__.py' for i in range(1,len(bits))}&tree.keys()
     added|=deps-selected;selected|=deps
 payload={}
 for p in sorted(selected):
  mode,oid=tree[p];assert mode in {'100644','100755'}
  b=original[p];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==oid
  if SECRETS.search(b):raise RuntimeError('Credential-pattern scan blocked packaging; no credential is printed')
  payload['source/'+p]=b
 source_bytes=sum(map(len,payload.values()))
 for name in DOCS:payload[name]=(HERE/name).read_bytes()
 parts=['# 五人精选原文：逐字阅读副本\n\n以下只拼接原文，不提升任何结论。相对链接以各段原路径为基准；导航使用03_ASSET_GUIDE_ZH.md。无需读全再研究。\n']
 for p in CORE:
  b=original[p];parts+=['\n\n---\n\n原路径：`source/'+p+'`\n\nSHA-256：`'+hashlib.sha256(b).hexdigest()+'`\n\n',b.decode()]
 payload['05_CORE_TEXT.md']=''.join(parts).encode();payload['verify_bundle.py']=VERIFY.encode()
 commit_time=git('show','-s','--format=%cI',BASE).decode().strip()
 snapshot={'repository':'https://github.com/SOMEBODYJUN/co-work-anl','branch_at_capture':'main',
  'source_commit':BASE,'source_commit_time':commit_time,'target':'Q-CAG-HALF-5; five providers; arbitrary finite customers/catalogue; every full-history pure SPE','target_status':'OPEN',
  'selection':'All regular tracked paths containing customer_attraction or starting research/workspaces/customer-attraction/, plus named claim/review metadata and statically resolvable repository Python imports',
  'source_file_count':len(selected),'source_bytes':source_bytes,'groups':dict(sorted(Counter(map(category,selected)).items())),
  'statically_added_dependencies':sorted(added),'python_ast_parse_failures':sorted(failures),
  'original_bytes_preserved':True,'source_git_blob_identity_checked':True,'credentials_and_git_metadata_included':False,
  'not_claimed':['full Git history','all unrelated research projects','new independent mathematics audit of archived drafts','fresh replay of all historical computations','proof of HALF(5)','completeness of dynamic Python imports']}
 payload['SOURCE_SNAPSHOT.json']=(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n').encode()
 rows=[]
 for name,b in sorted(payload.items()):
  assert not PurePosixPath(name).is_absolute() and '..' not in PurePosixPath(name).parts
  assert not SECRETS.search(b),'Credential-pattern scan blocked packaging'
  row={'path':name,'size_bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
  if name.startswith('source/'):row.update(source_path=name[7:],git_blob=tree[name[7:]][1])
  rows.append(row)
 payload['MANIFEST.json']=(json.dumps({'schema':'half5-handoff-manifest-v1','source_commit':BASE,'files':rows},ensure_ascii=False,indent=2)+'\n').encode()
 args.output.parent.mkdir(parents=True,exist_ok=True)
 stamp=datetime.fromisoformat(commit_time).astimezone(timezone.utc).timetuple()[:6]
 with zipfile.ZipFile(args.output,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for name,b in sorted(payload.items()):
   info=zipfile.ZipInfo(PREFIX+name,date_time=stamp);info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
   z.writestr(info,b,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
 with zipfile.ZipFile(args.output) as z:
  assert z.testzip() is None
  assert set(z.namelist())=={PREFIX+p for p in payload}
  for row in rows:
   b=z.read(PREFIX+row['path']);assert len(b)==row['size_bytes']
   assert hashlib.sha256(b).hexdigest()==row['sha256']
 report={'status':'built_and_verified','source_commit':BASE,'source_files':len(selected),'total_files':len(payload),
  'uncompressed_bytes':sum(map(len,payload.values())),'zip_bytes':args.output.stat().st_size,
  'zip_sha256':hashlib.sha256(args.output.read_bytes()).hexdigest(),'credential_pattern_scan':'pass',
  'zip_crc_and_all_sha256':'pass','source_git_blob_identities':'pass','mathematical_review_performed':False}
 (HERE/'BUILD_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
