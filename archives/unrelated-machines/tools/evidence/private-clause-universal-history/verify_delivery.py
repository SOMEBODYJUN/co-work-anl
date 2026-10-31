"""Check source bytes, declared proof chain, scope and delivery links, not math."""
from pathlib import Path
import argparse,hashlib,json,re

def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--fallback-root',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 root=a.root.resolve();fallback=a.fallback_root.resolve() if a.fallback_root else root;er=Path('archives/unrelated-machines/tools/evidence/private-clause-universal-history')
 def resolve(rel):
  q=root/rel
  return q if q.is_file() else fallback/rel
 counts={};checks=[];entries={}
 for name in ['source-manifest.json','comparison-manifest.json']:
  sources=json.loads((root/er/name).read_text())['sources'];counts[name]=len(sources)
  for x in sources:
   raw=resolve(x['preserved_repo_path']).read_bytes()
   if len(raw)!=x['source_size']or sha(raw)!=x['source_sha256']:raise ValueError(('source mismatch',x['id']))
   entries[x['id']]=x;checks.append({'id':x['id'],'size':len(raw),'sha256':sha(raw),'passed':True})
 if counts!={'source-manifest.json':5,'comparison-manifest.json':8}:raise ValueError(counts)
 scope=json.loads((root/er/'canonical-section-scope.json').read_text());raw=resolve(scope['canonical_repo_path']).read_bytes();st=raw.index(b'## 2.');en=raw.index(b'## 4.')
 if sha(raw)!=scope['canonical_whole_sha256']or len(raw)!=scope['canonical_whole_size']or st!=scope['formal_section_byte_start']or en!=scope['formal_section_byte_end_exclusive']or sha(raw[st:en])!=scope['formal_section_bytes_sha256']:raise ValueError('scope identity')
 chain=json.loads((root/er/'dependency-and-proof-chain.json').read_text());snap=chain['old_query_snapshot'];sraw=resolve(snap['repo_path']).read_bytes()
 if sha(sraw)!=snap['sha256']or len(sraw)!=snap['size']:raise ValueError('old dependency snapshot')
 pc=chain['primary_two_proofs_read_after'];after=resolve(entries[pc['source_id']]['preserved_repo_path']).read_bytes()
 for idkey,hashkey in [('local_author_proof_id','local_author_proof_sha256'),('global_author_proof_id','global_author_proof_sha256'),('prior_independent_id','prior_independent_sha256')]:
  value=sha(resolve(entries[pc[idkey]]['preserved_repo_path']).read_bytes())
  if value!=pc[hashkey]or value.encode()not in after:raise ValueError(('proof chain',idkey))
 receipts=json.loads((root/'cleanup/workspaces/Boss4/r3-private-clause-universal/semantic-receipts.json').read_text())
 if len(receipts)!=5 or len({x['id']for x in receipts})!=5:raise ValueError('receipt count')
 for x in receipts:
  for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']:
   if x.get(k)is not True:raise ValueError((x['id'],k))
  for k in ['read_note','comparison_note','decision_note']:
   if not isinstance(x.get(k),str)or not x[k].strip():raise ValueError((x['id'],k))
  if x['disposition']not in {'integrated','retained','duplicate','retired'}:raise ValueError(x['id'])
  for rel in x['targets']:
   if not resolve(rel).is_file():raise ValueError(('missing receipt target',rel))
 docs=[Path('archives/unrelated-machines/state/证明/私有子句的正外端染色与压缩共同匹配--证明.md'),Path('archives/unrelated-machines/state/审查/私有子句全公式上界的双证明与分节认证--审查.md'),er/'README.md'];links=[]
 for rel in docs:
  for url in re.findall(r'\[[^\]]+\]\(([^)]+)\)',(root/rel).read_text()):
   if '://'in url or url.startswith('#'):continue
   candidate=(root/rel.parent/url.split('#',1)[0]).resolve();dest=candidate.relative_to(root)
   if not resolve(dest).is_file()and candidate!=a.output.resolve():raise ValueError(('missing link',str(rel),url))
   links.append({'from':str(rel),'to':str(dest),'passed':True})
 report={'check_kind':'delivery-source-proof-chain-and-scope-identity-only-not-mathematical-run','all_checks_passed':True,'primary_source_count':5,'comparison_source_count':8,'source_byte_checks':checks,'dependency_snapshot_sha_verified':snap['sha256'],'two_author_proofs_and_prior_independent_sha_chain_verified':True,'canonical_formal_sections':['2','3'],'canonical_whole_and_formal_scope_verified':True,'receipt_count':5,'markdown_link_count':len(links),'markdown_link_checks':links,'mathematical_runs_this_batch':0,'blind_reviews_this_batch':0,'original_source_bytes_modified':False,'formal_hypergraph_written':False}
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:report[k]for k in ['check_kind','all_checks_passed','primary_source_count','comparison_source_count','receipt_count','markdown_link_count','mathematical_runs_this_batch']},ensure_ascii=False))
if __name__=='__main__':main()
