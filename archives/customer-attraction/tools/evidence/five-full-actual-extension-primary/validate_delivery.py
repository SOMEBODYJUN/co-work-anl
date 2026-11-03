"""Validate staged source identities, receipts, syntax and local links only."""
from pathlib import Path
import ast, hashlib, json, re
HERE=Path(__file__).resolve().parent
STAGE=HERE.parents[4]
REPO=Path('/workspace/scratch/3f8e8ef0ac4e/co-work-anl-Boss4')
CO_STAGE=STAGE.parent.parent/'direction-next/tree'
WORK=STAGE/'cleanup/workspaces/Boss4/full-actual-extension-primary'

def locate(path):
    p=STAGE/path
    if p.exists(): return p
    p=REPO/path
    return p if p.exists() else CO_STAGE/path

def main():
    primary=json.loads((HERE/'source-manifest.json').read_text());related=json.loads((HERE/'related-manifest.json').read_text())
    receipts=json.loads((WORK/'semantic-receipts.json').read_text())
    assert len(receipts)==len(primary)==9 and {r['id'] for r in receipts}=={r['id'] for r in primary}
    for r in receipts:
        assert r['disposition']=='integrated'
        assert all(r[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
        assert all(r[k] for k in ('read_note','comparison_note','decision_note','targets'))
        for p in r['targets']: assert (STAGE/p).is_file()
    byte_checks=[]
    for m in primary+related:
        p=STAGE/m['local_path'];b=p.read_bytes()
        assert len(b)==m['size'] and hashlib.sha256(b).hexdigest()==m['sha256']
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==m['blob']
        if m['path'].endswith('.py'): ast.parse(b)
        byte_checks.append(m['id'])
    index={}
    for line in (REPO/'cleanup/inventory.jsonl').read_text().splitlines():
        m=json.loads(line)
        for source in m['sources']:index[source['commit']+':'+source['path']]=m
    newpages=[STAGE/'archives/customer-attraction/state/程序/显式实际第三位扩展的受限列与旧池定价--程序.md',STAGE/'archives/customer-attraction/state/计算/实际第三位七千四百九十七行的有理必要点--计算.md']
    ids=[];source_refs=[]
    for p in newpages:
        text=p.read_text();front=text.split('---',2)[1];ids.append(re.search(r'^id: (.+)$',front,re.M).group(1))
        refs=re.findall(r'^  - source:(.+)$',front,re.M)
        for r in refs: assert r in index; source_refs.append(r)
    assert len(set(ids))==2
    links=[]
    for p in newpages+[HERE/'README.md']:
        for dest in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            path=dest.split('#')[0]
            if not path or '://' in path:continue
            candidate=p.parent/path
            if not candidate.exists():
                relative=candidate.resolve().relative_to(STAGE.resolve());candidate=locate(relative)
            assert candidate.exists(),(str(p),dest)
            links.append({'from':str(p.relative_to(STAGE)),'to':dest})
    for p in HERE.glob('*.py'): ast.parse(p.read_text())
    relation=json.loads((HERE/'relations-for-phase-three.json').read_text());assert len(relation['relations'])==8
    for r in relation['relations']:
        assert r['conditions'] and r['explanation']
        for e in r['evidence']:assert locate(e.split('#')[0]).is_file(),e
    report={'status':'passed','primary_source_count':9,'related_source_count':3,'receipts':len(receipts),'byte_SHA_and_blob_checks':byte_checks,'new_object_ids':ids,'source_refs_checked':len(source_refs),'local_links_checked':len(links),'explained_relations':8,'co_delivery_forward_links':1,'original_math_runs':0,'scope':'artifacts/links/metadata/AST only; no row engine or SPE check'}
    (HERE/'artifact-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':main()
