"""Package integrity/link checks only. No mathematical program is imported or rerun."""
from pathlib import Path
import ast,hashlib,json,re,sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
BODY=ROOT/'archives/customer-attraction/state/程序/实际第四步强制新回复的嵌套投影程序--程序.md'
RECEIPT=ROOT/'cleanup/workspaces/Boss7/receipts-round11/c467ea968709001dff2c.json'
source=json.loads((HERE/'source-manifest.json').read_text())
for role in ('primary','related_actual_input'):
    item=source[role];p=HERE/source['preserved_paths'][item['id']];data=p.read_bytes()
    assert len(data)==item['size'] and hashlib.sha256(data).hexdigest()==item['sha256']
assert (HERE/'replay/nested_reply_projection.py').read_bytes()==(HERE/'original/nested_reply_projection.py').read_bytes()
receipt=json.loads(RECEIPT.read_text())
assert receipt['id']=='c467ea968709001dff2c' and receipt['disposition']=='integrated'
assert all((ROOT/p).is_file() for p in receipt['targets'])
for p in HERE.rglob('*.py'):ast.parse(p.read_text(),filename=str(p))
for p in HERE.rglob('*.json'):json.loads(p.read_text())
links=[];pending=[]
for p in (BODY,HERE/'README.md'):
    for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
        if '://' in link:continue
        target=(p.parent/link.split('#',1)[0]).resolve()
        if target.name=='self-check.json':continue
        if not target.exists() and '--allow-pending-companion' in sys.argv and target==ROOT/'archives/customer-attraction/state/计算/嵌套回复的有理分离切面--计算.md':
            pending.append({'from':str(p.relative_to(ROOT)),'target':str(target.relative_to(ROOT)),'owner':'Boss7 coordinating parent; planned companion currently being authored'})
            continue
        assert target.exists(),(str(p),link)
        links.append({'from':str(p.relative_to(ROOT)),'target':str(target.relative_to(ROOT))})
comparison=json.loads((HERE/'comparison-manifest.json').read_text())
for item in comparison['full_text_comparisons']:
    data=(ROOT/item['path']).read_bytes()
    assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256']
event=json.loads((HERE/'replay/execution.json').read_text())
assert event['exit_code']==0 and event['original_main_calls']==1 and event['linprog_calls_if_success']==6
assert len((HERE/'replay/stdout.txt').read_bytes())==event['stdout_bytes']==2494
assert (HERE/'replay/stderr.txt').read_bytes()==b'' and event['stderr_bytes']==0
assert (HERE/'replay/stdout.txt').read_bytes()==(HERE/'replay/nested_reply_cuts.json').read_bytes()
output=json.loads((HERE/'replay/nested_reply_cuts.json').read_text())
point=json.loads((HERE/'related/combined_branch_latest_exact.json').read_text())
assert output['source']==event['command'][-1]
assert output['source_sha256']==source['related_actual_input']['sha256'] and output['source_W']==point['W']
assert len(output['selected'])==5
schema=json.loads((HERE/'input-interface-report.json').read_text())
assert schema['columns']==1905 and schema['complete_joint_groups']==194 and schema['overlap_bounds_checked']==1306
assert schema['original_module_imports']==schema['solver_calls']==schema['cut_evaluations']==0
files=[]
for p in sorted([BODY,RECEIPT,*HERE.rglob('*')]):
    if not p.is_file() or p.name=='self-check.json':continue
    assert '__pycache__' not in p.parts
    data=p.read_bytes();files.append({'path':str(p.relative_to(ROOT)),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
record={'status':'owned-package-passed-companion-link-pending' if pending else 'pass','pending_companion_links':pending,'scope':'package/record consistency and links; no mathematical entry or solver rerun','source_and_input_exact_sha':True,'comparison_hashes_still_match':len(comparison['full_text_comparisons']),'links':links,'files':files}
(HERE/'self-check.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':record['status'],'files':len(files),'links':len(links),'pending_companion_links':len(pending),'mathematical_reruns':0},ensure_ascii=False))
