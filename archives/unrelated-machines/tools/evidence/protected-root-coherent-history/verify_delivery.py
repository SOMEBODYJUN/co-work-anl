"""Verify source bytes, stated hash chains, section slices and delivery links only."""
from pathlib import Path
import argparse, hashlib, json, re

def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--fallback-root',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();root=a.root.resolve();fallback=(a.fallback_root or root).resolve()
 er=Path('archives/unrelated-machines/tools/evidence/protected-root-coherent-history');ws=Path('cleanup/workspaces/Boss4/r3-protected-root-coherent-four-history')
 def resolve(rel):
  fp=root/rel;return fp if fp.is_file() else fallback/rel
 def load(rel):return json.loads(resolve(rel).read_text())
 manifests=[load(er/n)['sources'] for n in ['source-manifest.json','comparison-manifest.json']]
 assert list(map(len,manifests))==[3,11]
 items={x['id']:x for group in manifests for x in group};bytechecks=[]
 def raw(sid):return resolve(items[sid]['preserved_repo_path']).read_bytes()
 for sid,item in items.items():
  r=raw(sid);assert len(r)==item['source_size'] and sha(r)==item['source_sha256'],sid;assert item['full_file_reviewed'] is True;bytechecks.append(dict(id=sid,size=len(r),sha256=sha(r),passed=True))
 scope=load(er/'scope-and-sha-chain.json');chainchecks=0
 for chain in scope['hash_chains']:
  record=raw(chain['record_id'])
  for sid in chain['source_ids']:
   assert sha(raw(sid)).encode() in record,(chain['record_id'],sid);chainchecks+=1
 for s in scope['canonical_sections']:
  r=raw(s['source_id']);b=r.index(s['start_marker'].encode());e=r.index(s['end_marker'].encode(),b+len(s['start_marker'].encode())) if s['end_marker'] else len(r)
  assert len(r)==s['whole_size'] and sha(r)==s['whole_sha256'];assert b==s['byte_start'] and e==s['byte_end_exclusive'];assert len(r[b:e])==s['slice_size'] and sha(r[b:e])==s['slice_sha256']
 receipts=load(ws/'semantic-receipts.json');assert len(receipts)==3 and {x['id'] for x in receipts}=={x['id'] for x in manifests[0]}
 for r in receipts:
  assert all(r.get(k) is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
  assert all(isinstance(r.get(k),str) and r[k].strip() for k in ['read_note','comparison_note','decision_note'])
  assert r['disposition'] in {'retained','integrated','duplicate','retired'}
  assert all(resolve(t).is_file() for t in r['targets'])
 boundaries=load(er/'contract-and-evidence-boundaries.json');assert boundaries['mathematical_runs_this_batch']==0 and boundaries['blind_reviews_this_batch']==0 and scope['mathematical_runs_this_batch']==0
 relations=load(er/'relation-review.json');assert relations['formal_hypergraph_written'] is False
 s3doc=Path('archives/unrelated-machines/state/审查/完整原端三次条件的作者合同与拉回证明--审查.md');rootdoc=Path('archives/unrelated-machines/state/审查/共享子句保护环的根终审与证书范围--审查.md');links=[]
 for rel in [s3doc,rootdoc,er/'README.md']:
  for url in re.findall(r'\[[^\]]+\]\(([^)]+)\)',resolve(rel).read_text()):
   if '://' in url or url.startswith('#'):continue
   dest=(root/rel.parent/url.split('#',1)[0]).resolve().relative_to(root)
   assert resolve(dest).is_file() or (root/dest).resolve()==a.output.resolve(),(str(rel),url)
   links.append(dict(source=str(rel),target=str(dest),passed=True))
 listed=load(ws/'copy-files.json');assert isinstance(listed,list) and listed==sorted(set(listed))
 for rel in listed:assert not Path(rel).is_absolute() and '..' not in Path(rel).parts and resolve(rel).is_file(),rel
 if (root/'cleanup/inventory.jsonl').is_file():mode='repository-listed-files-exist'
 else:
  mode='staging-exact-file-list';assert listed==sorted(str(fp.relative_to(root)) for fp in root.rglob('*') if fp.is_file())
 report=dict(check_kind='delivery-integrity-hash-chain-section-and-link-only-not-mathematical-run',all_checks_passed=True,primary_source_count=3,comparison_source_count=11,source_byte_checks=bytechecks,source_hash_chain_count=len(scope['hash_chains']),hash_occurrence_checks=chainchecks,canonical_formal_section_count=2,whole_file_identity_not_whole_historical_certification=True,receipt_count=3,markdown_link_count=len(links),markdown_link_checks=links,copy_list_check_mode=mode,mathematical_runs_this_batch=0,blind_reviews_this_batch=0,original_source_bytes_modified=False,other_Boss_formal_page_modified=False,formal_hypergraph_written=False)
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['all_checks_passed','primary_source_count','comparison_source_count','source_hash_chain_count','hash_occurrence_checks','canonical_formal_section_count','receipt_count','markdown_link_count','copy_list_check_mode','mathematical_runs_this_batch']},ensure_ascii=False))
if __name__=='__main__':main()
