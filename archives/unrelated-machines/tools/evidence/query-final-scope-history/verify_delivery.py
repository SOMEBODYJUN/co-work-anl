"""Check preserved bytes, receipt shape and links; never run mathematical audits."""
from pathlib import Path
import argparse, hashlib, json, re

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--fallback-root', type=Path)
    ap.add_argument('--output', type=Path, required=True)
    args=ap.parse_args()
    root=args.root.resolve(); fallback=args.fallback_root.resolve() if args.fallback_root else root
    er=Path('archives/unrelated-machines/tools/evidence/query-final-scope-history')
    def resolve(p):
        a=root/p
        return a if a.is_file() else fallback/p
    rawchecks=[]
    for manifest in ['source-manifest.json','comparison-manifest.json']:
        data=json.loads((root/er/manifest).read_text())
        for source in data['sources']:
            p=resolve(source['preserved_repo_path']); raw=p.read_bytes()
            check={'id':source['id'],'preserved_repo_path':source['preserved_repo_path'],'size':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
            check['passed']=check['size']==source['source_size'] and check['sha256']==source['source_sha256']
            if not check['passed']: raise ValueError(check)
            rawchecks.append(check)
    receipts=json.loads((root/'cleanup/workspaces/Boss4/query-final-scope-history-next/semantic-receipts.json').read_text())
    if len(receipts)!=4 or len({r['id'] for r in receipts})!=4: raise ValueError('Receipt source count')
    for r in receipts:
        for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']:
            if r.get(k) is not True: raise ValueError((r['id'],k))
        for k in ['read_note','comparison_note','decision_note']:
            if not isinstance(r.get(k),str) or not r[k].strip(): raise ValueError((r['id'],k))
        if r['disposition'] not in {'integrated','retained','duplicate','retired'}: raise ValueError(r['id'])
        for p in r['targets']:
            if not resolve(p).is_file(): raise ValueError((r['id'],'missing target',p))
    files=[Path('archives/unrelated-machines/state/审查/查询分离冻结合同与最终组合适用范围--审查.md'),Path('archives/unrelated-machines/state/审查/单件查询计数与近单位必要条件的版本审查--审查.md'),er/'README.md']
    linkchecks=[]
    for rel in files:
        txt=(root/rel).read_text()
        if rel.parts[-3]=='state' or '/state/' in str(rel):
            if not txt.startswith('---\n'): raise ValueError(('missing frontmatter',rel))
        for url in re.findall(r'\[[^\]]+\]\(([^)]+)\)',txt):
            if '://' in url or url.startswith('#'): continue
            pathpart=url.split('#',1)[0]
            candidate=(root/rel.parent/pathpart).resolve()
            try: dest=candidate.relative_to(root)
            except ValueError: raise ValueError(('outside stage link',rel,url))
            if not resolve(dest).is_file() and candidate != args.output.resolve(): raise ValueError(('missing link',rel,url,dest))
            linkchecks.append({'from':str(rel),'to':str(dest),'passed':True})
    report={'check_kind':'delivery-integrity-only-not-mathematical-run','all_checks_passed':True,'primary_source_count':4,'comparison_source_count':18,'source_byte_checks':rawchecks,'receipt_count':4,'markdown_link_count':len(linkchecks),'markdown_link_checks':linkchecks,'mathematical_runs_this_batch':0,'blind_reviews_this_batch':0,'original_source_bytes_modified':False,'formal_hypergraph_written':False,'checker_initial_issue':'First integrity check encountered the report self-link before output creation; exact output path is now permitted during generation. No mathematical audit was run.'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['check_kind','all_checks_passed','primary_source_count','comparison_source_count','receipt_count','markdown_link_count','mathematical_runs_this_batch']},ensure_ascii=False))
if __name__=='__main__': main()
