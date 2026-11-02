"""Static delivery integrity only. Does not import or run any mathematics."""
from pathlib import Path
import argparse,hashlib,json,re

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);args=ap.parse_args()
 here=Path(__file__).resolve().parent;delivery=here.parents[4];repo=args.repo
 src=json.loads((here/'source-manifest.json').read_text());receipts=json.loads((here/'receipts.json').read_text());deps=json.loads((here/'reused-dependencies.json').read_text());rels=json.loads((here/'relationship-review.json').read_text());review=json.loads((here/'fixed-record-review.json').read_text());event=json.loads((here/'execution-event.json').read_text())
 assert len(src)==11 and sum(x['size'] for x in src)==1153167
 assert {x['id'] for x in src}=={x['id'] for x in receipts} and len(receipts)==11
 for x in src:
  p=here/'original'/x['id']/Path(x['path']).name
  assert p.stat().st_size==x['size'] and sha(p)==x['sha256']
  assert len(x['sources'])==2 and all(re.fullmatch('[0-9a-f]{40}',s['commit']) for s in x['sources'])
 for r in receipts:
  assert r['full_file_reviewed'] and r['related_material_checked'] and r['unique_content_accounted_for'] and r['disposition']=='integrated'
  assert all((delivery/t).is_file() for t in r['targets'])
 for d in deps:
  p=repo/d['path'];assert p.is_file() and p.stat().st_size==d['size'] and sha(p)==d['sha256'],d['path']
 for r in rels:
  assert (delivery/r['from']).is_file() and ((delivery/r['to']).is_file() or (repo/r['to']).is_file())
 formal=sorted((delivery/'archives/customer-attraction/state').rglob('*.md'));assert len(formal)==4
 ids=[];links=[]
 for p in formal+[here/'README.md']:
  t=p.read_text()
  if p!=here/'README.md':
   ids.append(re.search('^id: (.+)$',t,re.M).group(1));assert t.startswith('---\n') and '\nsource_refs: ' in t
  for target in re.findall(r'\]\(([^)]+)\)',t):
   if '://' in target or target.startswith('#'):continue
   q=(p.parent/target.split('#')[0]).resolve()
   if not q.is_file():
    rel=q.relative_to(delivery);assert (repo/rel).is_file(),(str(p),target)
   links.append({'file':str(p.relative_to(delivery)),'target':target})
 assert len(set(ids))==4
 assert event['actual_driver_invocations']==1 and event['exit_code']==0 and event['stderr_bytes']==0
 assert event['input_pre_sha256']==event['input_post_sha256']
 assert (here/'run.stdout.txt').stat().st_size==event['stdout_bytes']==9628 and (here/'run.stderr.txt').stat().st_size==0
 assert sha(here/'audit_fixed_records.py')==event['input_pre_sha256']['audit_fixed_records.py']
 for rel,h in event['input_pre_sha256'].items():assert sha(here/rel)==h
 assert review['actual_counts']=={'four_point_nonself_IC':29775,'four_point_self_comparisons':4748,'four_point_ordered_decisions_logically_covered':45852,'four_point_ordered_nonself_logically_covered':312561,'original_entry_calls':0,'LP':0,'BI':0,'RNG':0}
 assert [r['distinct_nonzero_integer_rows'] for r in review['records']]==[1266,1483,1260,5551]
 assert [r['OPT_over_W'] for r in review['records']]==['8/5','9/5','9/5','11/6']
 assert all(r['negative_comparisons']==0 for r in review['records'])
 nodes=json.loads((here/'all-node-slacks.json').read_text());assert [len(x['records']) for x in nodes]==[330,330,2801,1287]
 result={'status':'PASS','scope':'static package integrity and saved-result shape only; zero mathematical reexecution','primary_count':len(src),'primary_bytes':sum(x['size'] for x in src),'receipt_count':len(receipts),'formal_count':len(formal),'links_checked':len(links),'dependency_count':len(deps),'relation_count':len(rels),'new_math_driver_reexecution':0,'unique_completed_math_event':1,'source_pre_post_same':True,'links':links}
 (here/'self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='links'},ensure_ascii=False))
if __name__=='__main__':main()
