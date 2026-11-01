"""Static provenance/links/receipt checks; no mathematical search or verifier."""
from pathlib import Path
import hashlib, json, re

HERE=Path(__file__).resolve().parent
REPO=next(p for p in HERE.parents if (p/'cleanup/receipt-example.json').is_file())
OBJECT=REPO/'archives/customer-attraction/state/引理/分数集合覆盖数的静态安全值下界--引理.md'
RECEIPT=REPO/'cleanup/workspaces/Boss7/receipts-round15/875c24085fdf738259af.json'
load=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=HERE/'original/fractional_cover_safety.md'
assert source.stat().st_size==4140 and sha(source)=='0494f814d2ff53de3fed810470f3a249dc352b6b41fe70afcdab590f7eb5c587'
manifest=load(HERE/'source-manifest.json')
assert manifest['source_id']=='875c24085fdf738259af' and manifest['full_clean_show_read'] is True
assert all(manifest['execution_scope'][k]==0 for k in ('original_mathematical_program_runs','new_mathematical_program_runs','LP_calls','SPE_searches','old_finite_regressions_repeated'))
for record in manifest['artifacts']:
    path=REPO/record['path']
    assert path.stat().st_size==record['bytes'] and sha(path)==record['sha256'],str(path)
comparison=load(HERE/'comparison-manifest.json')
assert len(comparison['full_read_formal_objects'])==8
for record in comparison['full_read_formal_objects']:
    path=REPO/record['path']
    assert path.stat().st_size==record['bytes'] and sha(path)==record['sha256'],str(path)
receipt=load(RECEIPT)
assert receipt['id']=='875c24085fdf738259af' and receipt['disposition']=='integrated'
assert all(receipt[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
for target in receipt['targets']:
    if target.endswith('/self-check.json'):continue
    assert (REPO/target).is_file(),target
links=[]
for path in (OBJECT,HERE/'README.md'):
    for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
        if '://' in link or link.startswith('#'):continue
        target=(path.parent/link.split('#',1)[0]).resolve()
        if target==HERE/'self-check.json':continue
        assert target.is_file(),str(target)
        links.append(str(target.relative_to(REPO)))
text=OBJECT.read_text()
assert text.startswith('---\n') and 'source_ids: ["875c24085fdf738259af"]' in text
result=dict(status='PASS',scope='Static source digest, recorded artifact/comparison digests, receipt targets and Markdown links only; mathematical conclusions rely on the full written proof.',
            source_bytes=4140,source_sha256=sha(source),object_bytes=OBJECT.stat().st_size,object_sha256=sha(OBJECT),
            full_read_comparison_objects=8,artifact_digests_checked=len(manifest['artifacts']),
            receipt_targets=len(receipt['targets']),links_checked=len(links)+1,
            mathematical_program_runs=0,LP_calls=0,SPE_searches=0,links=links)
(HERE/'self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
assert (HERE/'self-check.json').is_file()
print(json.dumps({k:v for k,v in result.items() if k!='links'},ensure_ascii=False,indent=2))
