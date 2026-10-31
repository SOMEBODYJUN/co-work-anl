"""Source/hash/scope/link integrity only; does not run the scheduling algorithm."""
from pathlib import Path
import argparse,hashlib,json,re

def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--fallback-root',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();root=a.root.resolve();fallback=(a.fallback_root or root).resolve();er=Path('archives/unrelated-machines/tools/evidence/weighted-literal-pool-v2-history');ws=Path('cleanup/workspaces/Boss4/r3-weighted-literal-pool-v2-history')
 def resolve(rel):
  x=root/rel;return x if x.is_file() else fallback/rel
 def load(rel):return json.loads(resolve(rel).read_text())
 manifests=[load(er/n)['sources'] for n in ['source-manifest.json','comparison-manifest.json']];assert list(map(len,manifests))==[5,5];items={x['id']:x for group in manifests for x in group};assert len(items)==10
 def raw(sid):return resolve(items[sid]['preserved_repo_path']).read_bytes()
 checks=[]
 for sid,x in items.items():
  r=raw(sid);assert len(r)==x['source_size'] and sha(r)==x['source_sha256'],sid;assert x['full_file_reviewed'] is True;checks.append(dict(id=sid,size=len(r),sha256=sha(r),passed=True))
 scope=load(er/'scope-and-sha-chain.json');hashchecks=0
 for chain in scope['hash_chains']:
  record=raw(chain['record_id'])
  for sid in chain['source_ids']:assert sha(raw(sid)).encode() in record,(chain['record_id'],sid);hashchecks+=1
 can=scope['canonical'];r=raw(can['id']);assert len(r)==can['whole_size'] and sha(r)==can['whole_sha256'];end=0
 for part in can['slice_partition']:
  b,e=part['byte_start'],part['byte_end_exclusive'];assert b==end and 0<=b<e<=len(r);assert len(r[b:e])==part['size'] and sha(r[b:e])==part['sha256'];end=e
 assert end==len(r) and len(can['slice_partition'])==6
 for n in range(1,6):assert ('\n## '+str(n)+'.').encode() in r
 boundaries=load(er/'three-constructions-and-boundaries.json');assert boundaries['mathematical_runs_this_batch']==0 and boundaries['blind_reviews_this_batch']==0 and scope['mathematical_runs_this_batch']==0
 receipts=load(ws/'semantic-receipts.json');assert len(receipts)==5 and {x['id'] for x in receipts}=={x['id'] for x in manifests[0]}
 for x in receipts:
  assert all(x.get(k) is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
  assert all(isinstance(x.get(k),str) and x[k].strip() for k in ['read_note','comparison_note','decision_note'])
  assert x['disposition'] in {'integrated','retained','duplicate','retired'};assert all(resolve(t).is_file() for t in x['targets'])
 relations=load(er/'relation-review.json');assert relations['formal_hypergraph_written'] is False
 docs=[Path('archives/unrelated-machines/state/证明/异权文字池的连续槽排名与共同调度--证明.md'),Path('archives/unrelated-machines/state/审查/异权文字池的三种匹配来源与终审先验--审查.md'),er/'README.md'];links=[]
 for rel in docs:
  for url in re.findall(r'\[[^\]]+\]\(([^)]+)\)',resolve(rel).read_text()):
   if '://' in url or url.startswith('#'):continue
   dest=(root/rel.parent/url.split('#',1)[0]).resolve().relative_to(root);assert resolve(dest).is_file() or (root/dest).resolve()==a.output.resolve(),(str(rel),url);links.append(dict(source=str(rel),target=str(dest),passed=True))
 listed=load(ws/'copy-files.json');assert isinstance(listed,list) and listed==sorted(set(listed))
 for rel in listed:assert not Path(rel).is_absolute() and '..' not in Path(rel).parts and resolve(rel).is_file(),rel
 if (root/'cleanup/inventory.jsonl').is_file():mode='repository-listed-files-exist'
 else:mode='staging-exact-file-list';assert listed==sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file())
 report=dict(check_kind='delivery-source-hash-scope-and-link-integrity-only-not-mathematical-run',all_checks_passed=True,primary_source_count=5,comparison_source_count=5,source_byte_checks=checks,source_hash_chain_count=len(scope['hash_chains']),hash_occurrence_checks=hashchecks,canonical_whole_header_and_all_five_sections_partitioned=True,canonical_partition_count=6,whole_hash_not_unopened_record_certification=True,receipt_count=5,markdown_link_count=len(links),markdown_link_checks=links,copy_list_check_mode=mode,mathematical_runs_this_batch=0,blind_reviews_this_batch=0,original_source_bytes_modified=False,other_Boss_formal_page_modified=False,formal_hypergraph_written=False)
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['all_checks_passed','primary_source_count','comparison_source_count','source_hash_chain_count','hash_occurrence_checks','canonical_partition_count','receipt_count','markdown_link_count','copy_list_check_mode','mathematical_runs_this_batch']},ensure_ascii=False))
if __name__=='__main__':main()
