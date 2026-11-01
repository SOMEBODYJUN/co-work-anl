"""Static source-to-object/package checks; no mathematical code is executed."""
import ast
import hashlib
import json
from pathlib import Path
import re

P = Path(__file__).resolve().parent
R = P.parents[4]
manifest = json.loads((P/'source-manifest.json').read_text())
hashes=0
for item in manifest['artifacts']:
    path=R/item['path']
    assert path.is_file() and path.stat().st_size==item['bytes'],path
    assert hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256'],path
    hashes+=1
for item in json.loads((P/'comparison.json').read_text())['records']:
    path=R/item['path']
    assert path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256'],path
    hashes+=1
jsons=asts=0
for path in P.rglob('*'):
    if path.suffix=='.json' and path.name!='self-check.json':
        json.loads(path.read_text());jsons+=1
    elif path.suffix=='.py':
        ast.parse(path.read_text());asts+=1
text=(R/manifest['object']).read_text()
coverage=json.loads((P/'source-to-object.json').read_text())
assert coverage['entire_primary_read'] and coverage['all_appendices_included']
for unit in coverage['units']:
    for section in unit['object_section'].split('；'):
        assert section in text,section
assert coverage['mathematical_programs_run_here']==0
receipt=json.loads((R/manifest['receipt']).read_text())
assert receipt['id']=='dc788d5734387017a027'
for key in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']:
    assert receipt[key] is True
for target in receipt['targets']:
    path=R/target
    assert path.is_file() or path==P/'self-check.json',path
links=0
for path in [R/manifest['object'],P/'README.md']:
    for link in re.findall(r'\]\(([^)\n]+)\)',path.read_text()):
        if '://' in link or link.startswith('#'):continue
        assert (path.parent/link.split('#',1)[0]).resolve().exists(),(path,link)
        links+=1
event=json.loads((R/'archives/customer-attraction/tools/evidence/fixed-background-circuit-audit-program/replay/execution.json').read_text())
assert event['original_function_call_events']['main']==1
assert event['optimization_calls']==event['SPE_solver_calls']==event['additional_original_helper_calls']==0
assert event['files']['fixed_background_audit.json']['sha256']=='f01662cb7c19ebd5725e8fd2b25d3d57bd8fec0668dccb855c2bc2dcec47db1b'
old=json.loads((P/'related/fixed_background_rank_review.json').read_text())
assert old['background_M_cases']==152 and old['all_unit_background_cases']==8
result={'status':'PASS','identity':'static verification; no rank or circuit audit rerun',
        'sha256_checks':hashes,'JSON_parses':jsons,'AST_parses':asts,'markdown_links':links,
        'source_semantic_units':len(coverage['units']),'receipt_targets':len(receipt['targets']),
        'original_main_calls_here':0,'mathematical_functions_called_here':0,'LP_calls_here':0}
(P/'self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False))
