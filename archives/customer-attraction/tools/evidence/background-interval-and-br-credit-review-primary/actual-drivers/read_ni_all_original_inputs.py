from pathlib import Path
from collections import Counter
from math import comb
import json,hashlib,shutil
ROOT=Path('/workspace/scratch/37f0f9248cfc');C=ROOT/'boss4-next-cache';S=C/'r3-background-interval-and-br-credit-review-primary';E=Path('archives/customer-attraction/tools/evidence/background-interval-and-br-credit-review-primary')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def js(p,x):p=S/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def copy(a,b):p=S/b;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a,p);assert sha(a)==sha(p)
mp=C/'dummy-ni-coordination-necessary-originals/actual-source-manifest.json';m=json.loads(mp.read_text());assert len(m['rows'])==8 and sum(x['size'] for x in m['rows'])==530954
copy(mp,E/'acquisition/normal-original-source-manifest-full-eight.json');rows=[];certs=[]
for x in m['rows']:
 b=Path(x['local_path']).read_bytes();assert len(b)==x['size'] and hashlib.sha256(b).hexdigest()==x['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'];p=E/'related-originals'/x['path'];copy(x['local_path'],p);y=dict(**x,preserved_at=str(p),primary_done=False);rows.append(y)
 cp=Path(x['actual_normal_show_capture']);cap=json.loads(cp.read_text());assert cap['source']['id']==x['id'] and cap['source']['sha256']==x['sha256'];copy(cp,E/'acquisition'/cp.name)
 if x['id'] not in ['c388d1ee1cf9aeeb96fc','fe415b54d0e09b2d0c48']:continue
 d=json.loads(b);n=d['m'];q=n+1;assert n in [5,8] and d['policy_count_states']==len(d['policy'])==comb(n+q-1,q)
 topics=[frozenset(z) for z in d['topics']];assert topics==[frozenset([i,n+i]) for i in range(n)]+[frozenset(range(n))]
 actions={};hist=Counter();ahist=Counter();rowhash=hashlib.sha256();allrows=[]
 for index,z in enumerate(d['policy']):
  assert set(z)=={'counts','action'} and isinstance(z['counts'],list) and len(z['counts'])==q and all(type(t) is int and t>=0 for t in z['counts']) and sum(z['counts'])<n and type(z['action']) is int and 0<=z['action']<q
  key=tuple(z['counts']);assert key not in actions;actions[key]=z['action'];hist[sum(key)]+=1;ahist[(sum(key),z['action'])]+=1;encoded=json.dumps(z,sort_keys=True,separators=(',',':')).encode();rowhash.update(encoded+b'\n');allrows.append(dict(row=index,counts=z['counts'],action=z['action']))
 def comps(total,width):
  if width==1:yield (total,)
  else:
   for first in range(total+1):
    for rest in comps(total-first,width-1):yield (first,)+rest
 expected={v for dep in range(n) for v in comps(dep,q)};assert set(actions)==expected and list(actions)==sorted(actions)
 base=(0,)*q;actual=[]
 for dep in range(n):
  a=actions[base];actual.append(a);base=base[:a]+(base[a]+1,)+base[a+1:]
 assert actual==d['actual_path'] and list(base)==d['actual_terminal_counts'];assert d['optimal_source_unique_multiset']==list(range(n))
 # Read every nonpolicy nested scalar as well; keep all actual metadata without altering input.
 scalars=[]
 def walk(v,path='$'):
  if isinstance(v,dict):
   for k,u in v.items():walk(u,path+'.'+k)
  elif isinstance(v,list):
   for i,u in enumerate(v):walk(u,path+'['+str(i)+']')
  else:scalars.append(dict(path=path,type=type(v).__name__,value=v))
 walk({k:v for k,v in d.items() if k!='policy'});js(E/'input-reading'/('m'+str(n)+'-all-nonpolicy-fields.json'),dict(source_id=x['id'],source_sha256=x['sha256'],all_fields={k:v for k,v in d.items() if k!='policy'},all_nested_scalar_fields=scalars))
 js(E/'input-reading'/('m'+str(n)+'-every-policy-row.json'),dict(source_id=x['id'],source_sha256=x['sha256'],rows=allrows,all_rows_read=True,not_an_SPE_verification=True))
 certs.append(dict(id=x['id'],m=n,topic_count=q,source_sha256=x['sha256'],policy_rows=len(actions),expected_rows=comb(n+q-1,q),rows_by_depth=dict(sorted(hist.items())),depth_action_counts=[dict(depth=k[0],action=k[1],rows=v) for k,v in sorted(ahist.items())],all_counts_integer_nonnegative=True,all_actions_in_range=True,duplicate_rows=0,missing_rows=0,extra_rows=0,raw_policy_lexicographically_sorted=True,canonical_every_row_sha256=rowhash.hexdigest(),all_nonpolicy_scalar_fields=len(scalars),all_nonpolicy_fields_read=True,actual_path_from_complete_policy=actual,actual_counts=list(base),SPE_NOT_yet_verified_by_this_structural_read=True))
js(E/'related-original-program-manifest.json',dict(rows=rows,all_three_code_files_full_read=True,all_three_reports_full_read=True,all_two_certificates_every_row_and_field_read=True,extra_primary_done=0))
js(E/'input-reading/certificate-complete-field-coverage.json',dict(certificates=certs,scope='Complete structural original-input read, NOT yet incentive verification, no new original CLI',extra_primary_done=0));print(json.dumps(certs,ensure_ascii=False))
