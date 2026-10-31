"""Verify delivery/source identities, scoped sections and links; no math algorithms."""
from pathlib import Path
import argparse,hashlib,json,re

def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--fallback-root',type=Path);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
 root=a.root.resolve();fallback=a.fallback_root.resolve() if a.fallback_root else root
 er=Path('archives/unrelated-machines/tools/evidence/general-weighted-query-return-history')
 def resolve(p):
  q=root/p
  return q if q.is_file() else fallback/p
 counts={};checks=[]
 for name in ['source-manifest.json','comparison-manifest.json']:
  sources=json.loads((root/er/name).read_text())['sources'];counts[name]=len(sources)
  for x in sources:
   raw=resolve(x['preserved_repo_path']).read_bytes()
   if len(raw)!=x['source_size'] or sha(raw)!=x['source_sha256']:raise ValueError(('source mismatch',x['id']))
   checks.append({'id':x['id'],'size':len(raw),'sha256':sha(raw),'passed':True})
 if counts!={'source-manifest.json':5,'comparison-manifest.json':6}:raise ValueError(counts)
 dep=json.loads((root/er/'dependency-snapshot-check.json').read_text());raw=resolve(dep['repo_path']).read_bytes()
 if sha(raw)!=dep['sha256'] or len(raw)!=dep['size']:raise ValueError('dependency snapshot')
 sc=json.loads((root/er/'canonical-section-scope.json').read_text());can=(root/er/'comparisons/general_weighted_private_clause_exchange_and_shared_outside_boundary.md').read_bytes()
 if sha(can)!=sc['canonical_whole_sha256'] or len(can)!=sc['canonical_whole_size']:raise ValueError('canonical whole')
 st=can.index(b'## 1.');en=can.index(b'## 2.')
 if st!=sc['formal_section_byte_start'] or en!=sc['formal_section_byte_end_exclusive'] or sha(can[st:en])!=sc['formal_section_bytes_sha256']:raise ValueError('canonical section boundary')
 receipts=json.loads((root/'cleanup/workspaces/Boss4/r3-query-return-exchange/semantic-receipts.json').read_text())
 if len(receipts)!=5 or len({x['id'] for x in receipts})!=5:raise ValueError('receipt count')
 for x in receipts:
  for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']:
   if x.get(k)is not True:raise ValueError((x['id'],k))
  for k in ['read_note','comparison_note','decision_note']:
   if not isinstance(x.get(k),str) or not x[k].strip():raise ValueError((x['id'],k))
  if x['disposition']not in {'integrated','retained','duplicate','retired'}:raise ValueError(x['id'])
  for p in x['targets']:
   if not resolve(p).is_file():raise ValueError(('missing target',p))
 docs=[Path('archives/unrelated-machines/state/证明/私有查询返回的两种三半分析实例--证明.md'),Path('archives/unrelated-machines/state/审查/异权查询返回的双构造与指定范围审查--审查.md'),er/'README.md'];links=[]
 for rel in docs:
  for url in re.findall(r'\[[^\]]+\]\(([^)]+)\)',(root/rel).read_text()):
   if '://'in url or url.startswith('#'):continue
   p=(root/rel.parent/url.split('#',1)[0]).resolve();dest=p.relative_to(root)
   if not resolve(dest).is_file()and p!=a.output.resolve():raise ValueError(('missing link',str(rel),url))
   links.append({'from':str(rel),'to':str(dest),'passed':True})
 report={'check_kind':'delivery-and-source-scope-integrity-only-not-mathematical-run','all_checks_passed':True,'primary_source_count':5,'comparison_source_count':6,'source_byte_checks':checks,'dependency_snapshot_sha_verified':dep['sha256'],'canonical_whole_and_section_scope_verified':True,'receipt_count':5,'markdown_link_count':len(links),'markdown_link_checks':links,'mathematical_runs_this_batch':0,'blind_reviews_this_batch':0,'original_source_bytes_modified':False,'formal_hypergraph_written':False}
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:report[k]for k in ['check_kind','all_checks_passed','primary_source_count','comparison_source_count','receipt_count','markdown_link_count','mathematical_runs_this_batch']},ensure_ascii=False))
if __name__=='__main__':main()
