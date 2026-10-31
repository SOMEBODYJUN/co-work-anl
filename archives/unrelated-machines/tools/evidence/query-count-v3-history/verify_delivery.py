"""Check delivered bytes, snapshot identity, receipt fields and links only."""
from pathlib import Path
import argparse, hashlib, json, re

def sha(b): return hashlib.sha256(b).hexdigest()
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',type=Path,required=True)
    ap.add_argument('--fallback-root',type=Path)
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();root=args.root.resolve();fallback=args.fallback_root.resolve() if args.fallback_root else root
    er=Path('archives/unrelated-machines/tools/evidence/query-count-v3-history')
    def resolve(p):
        a=root/p
        return a if a.is_file() else fallback/p
    bytechecks=[];counts={}
    for name in ['source-manifest.json','comparison-manifest.json']:
        sources=json.loads((root/er/name).read_text())['sources'];counts[name]=len(sources)
        for x in sources:
            raw=resolve(x['preserved_repo_path']).read_bytes()
            if len(raw)!=x['source_size'] or sha(raw)!=x['source_sha256']: raise ValueError(('source mismatch',x['id']))
            bytechecks.append({'id':x['id'],'preserved_repo_path':x['preserved_repo_path'],'size':len(raw),'sha256':sha(raw),'passed':True})
    if counts!={'source-manifest.json':5,'comparison-manifest.json':8}: raise ValueError(counts)
    recovery=json.loads((root/er/'canonical-snapshot-recovery.json').read_text())
    inp=resolve(recovery['input_repo_path']).read_bytes();offset=inp.index(b'## 6.')
    expected=inp[:offset].rstrip()+b'\n';saved=(root/er/recovery['output_file']).read_bytes()
    if sha(inp)!=recovery['input_sha256'] or len(inp)!=recovery['input_size'] or offset!=recovery['first_section6_offset']: raise ValueError('Snapshot input mismatch')
    if saved!=expected or len(saved)!=13950 or sha(saved)!=recovery['expected_sha256']: raise ValueError('Snapshot output mismatch')
    receipts=json.loads((root/'cleanup/workspaces/Boss4/query-count-v3-history-next/semantic-receipts.json').read_text())
    if len(receipts)!=5 or len({r['id'] for r in receipts})!=5: raise ValueError('Receipt count')
    for r in receipts:
        for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']:
            if r.get(k) is not True: raise ValueError((r['id'],k))
        for k in ['read_note','comparison_note','decision_note']:
            if not isinstance(r.get(k),str) or not r[k].strip(): raise ValueError((r['id'],k))
        if r['disposition'] not in {'integrated','retained','duplicate','retired'}: raise ValueError(r['id'])
        for t in r['targets']:
            if not resolve(t).is_file(): raise ValueError(('missing receipt target',t))
    docs=[Path('archives/unrelated-machines/state/审查/近单位查询必要条件的端点与最终组合合同--审查.md'),er/'README.md']
    links=[]
    for rel in docs:
        for url in re.findall(r'\[[^\]]+\]\(([^)]+)\)',(root/rel).read_text()):
            if '://' in url or url.startswith('#'): continue
            candidate=(root/rel.parent/url.split('#',1)[0]).resolve();dest=candidate.relative_to(root)
            if not resolve(dest).is_file() and candidate!=args.output.resolve(): raise ValueError(('missing link',rel,url))
            links.append({'from':str(rel),'to':str(dest),'passed':True})
    report={'check_kind':'delivery-and-snapshot-byte-identity-only-not-mathematical-run','all_checks_passed':True,'primary_source_count':5,'comparison_source_count':8,'source_byte_checks':bytechecks,'snapshot_check':{'passed':True,'size':len(saved),'sha256':sha(saved),'input_original_modified':False},'receipt_count':5,'markdown_link_count':len(links),'markdown_link_checks':links,'mathematical_runs_this_batch':0,'blind_reviews_this_batch':0,'original_source_bytes_modified':False,'formal_hypergraph_written':False}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['check_kind','all_checks_passed','primary_source_count','comparison_source_count','receipt_count','markdown_link_count','mathematical_runs_this_batch']},ensure_ascii=False))
if __name__=='__main__': main()
