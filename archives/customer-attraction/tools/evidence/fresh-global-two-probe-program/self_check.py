"""Static source/artifact/link audit; never calls the probe or math audit."""
from pathlib import Path
import ast, collections, gzip, hashlib, json, re

HERE=Path(__file__).resolve().parent
REPO=next(p for p in HERE.parents if (p/'cleanup/receipt-example.json').is_file())
OBJECT=REPO/'archives/customer-attraction/state/程序/合法单题背景的全比较主题对探针--程序.md'
RECEIPT=REPO/'cleanup/workspaces/Boss7/receipts-round14/195c9fd7c0bf9575d1f8.json'
load=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=load(HERE/'source-manifest.json')
for f in manifest['artifacts']:
    p=REPO/f['path']; assert p.stat().st_size==f['bytes'] and sha(p)==f['sha256']
source=HERE/'original/probe_fresh_global_two.py'
assert source.stat().st_size==3601 and sha(source)=='6b5bf041c279d9d4def418444b266bdd8b4afdca46f336ea6cc28fa18857830c'
for p in HERE.rglob('*.py'): ast.parse(p.read_text(),filename=str(p))
raw=gzip.decompress((HERE/'replay/lp-capture.json.gz').read_bytes())
assert len(raw)==3108955 and hashlib.sha256(raw).hexdigest()=='f8a4572d3d669f7eb9c2200ceb5bf21d90fd4dd1c5afd10a3ba6fabe35cc6e37'
capture=json.loads(raw); audit=load(HERE/'contract-audit.json'); event=load(HERE/'replay/execution.json')
assert len(capture)==len(audit['records'])==84
assert all(c['result']['success'] and c['result']['status']==0 for c in capture)
assert event['original_main_calls']==1 and event['lp_calls']==84 and event['exit_code']==0
assert event['source_sha256_before']==event['source_sha256_after']==sha(source)
assert audit['status']=='PASS' and audit['original_main']==audit['lp_calls']==audit['original_imports']==0
assert audit['unique_matrix_coefficients']==8820 and audit['objective_coefficients']==audit['certificate_link_identities']==5292
assert audit['exact_ic_evaluations']==2940
assert sum(audit['exact_values'].values())==84 and audit['exact_values']['0']==10
assert sum(c['result']['fun']<0 for c in capture)==2
assert sum(c['result']['fun']==0 for c in capture)==8
assert sum(c['result']['fun']>0 for c in capture)==74
report=load(HERE/'replay/runtime/bounded_probe.json')
assert report['cases']==report['policies']==4 and report['solved']==84 and report['best']==0 and report['found'] is None
assert (HERE/'replay/stderr.txt').stat().st_size==(HERE/'audit-stderr.txt').stat().st_size==0
assert load(HERE/'replay/stdout.txt')==report
receipt=load(RECEIPT)
assert receipt['id']=='195c9fd7c0bf9575d1f8' and receipt['disposition']=='integrated'
assert all(receipt[k] is True for k in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
for target in receipt['targets']:
    if target.endswith('/self-check.json'): continue
    assert (REPO/target).is_file(),target
links=[]
for p in [OBJECT,HERE/'README.md']:
    for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
        if '://' in link or link.startswith('#'): continue
        target=(p.parent/link.split('#',1)[0]).resolve()
        assert target.is_file(),str(target)
        links.append(str(target.relative_to(REPO)))
result=dict(status='PASS',scope='Static hashes, AST, recorded counts, capture integrity, receipt targets and Markdown links only; no original or mathematical rerun.',
            source_bytes=3601,original_main_events=1,original_lp_calls=84,independent_math_audit_attempts=1,
            exact_audit_records=84,receipt_targets=len(receipt['targets']),links_checked=len(links),
            object_sha256=sha(OBJECT),contract_audit_sha256=sha(HERE/'contract-audit.json'),
            compressed_capture_sha256=sha(HERE/'replay/lp-capture.json.gz'),links=links)
(HERE/'self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
assert (HERE/'self-check.json').is_file()
print(json.dumps({k:v for k,v in result.items() if k!='links'},ensure_ascii=False,indent=2))
