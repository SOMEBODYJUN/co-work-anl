"""Static source/record/links only; never imports or runs research code."""
import ast
import hashlib
import json
from pathlib import Path
import re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
DOC=ROOT/'archives/customer-attraction/state/资源/全局保底研究入口的充分桥障碍与未成熟菜单边界--资源.md'
RECEIPT=ROOT/'cleanup/workspaces/Boss7/receipts-round19/d0ee70c07950c0cc87e0.json'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(p):return {'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':sha(p)}
manifest=load(HERE/'source-manifest.json')
assert manifest['primary_id']=='d0ee70c07950c0cc87e0'
assert len(manifest['sources'])==12 and manifest['total_source_bytes']==31976
assert manifest['original_program_runs']==manifest['original_helper_calls']==manifest['solver_calls']==manifest['independent_mathematical_runs']==0
ast_count=0;json_count=0;source_bindings=[];byname={}
for row in manifest['sources']:
    p=ROOT/row['preserved_at'];byname[p.name]=p
    assert p.stat().st_size==row['size'] and sha(p)==row['sha256']
    assert len(row['sources'])==2
    if p.suffix=='.py':ast.parse(p.read_text());ast_count+=1
    if p.suffix=='.json':load(p);json_count+=1
    source_bindings.append(bind(p))
assert ast_count==6 and json_count==3
floor=load(byname['floor_only_protection_audit.json'])
assert len(floor)==9 and len(floor['witnesses'])==floor['root_actions_checked']==18
assert floor['players']==3 and floor['topics']==18 and floor['unit_customers']==108
assert floor['OPT']==63 and floor['threshold']=='21/2'
assert [r['root'] for r in floor['witnesses']]==list(range(18))
assert all(r['payoffs']==['10','12','12'] and r['deviation_payoff']=='21' for r in floor['witnesses'])
repeated=load(byname['independent_repeated_prefix_audit.json'])
assert repeated['h_coefficient_numerator']==0
for key,cols,count,rows in [('repeated',131072,126464,8),('containing_prefix',262144,252928,16)]:
    r=repeated[key]
    assert r['literal_columns']==cols and r['aggregate_invariance_checks']==count
    assert r['minimum_scaled_residual']==0 and r['scale']==60000
    assert len(r['corner_table'])==rows and all(len(x['minima'])==6 for x in r['corner_table'])
safe=load(byname['safe_floor_m3p6.json'])
assert safe['parameters']['topics']==6 and safe['parameters']['players']==3
assert set(safe['weights'])=={'10','20','33'} and len(safe['witness'])==6
review=load(HERE/'review-record.json')
for row in review['formal_comparisons']:
    p=ROOT/row['path'];assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256']
for row in review['shared_core_assets']:
    p=ROOT/row['path'];assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256']
receipt=load(RECEIPT)
assert receipt['id']==manifest['primary_id'] and receipt['disposition']=='integrated'
assert all(receipt[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
assert receipt['targets']==[str(DOC.relative_to(ROOT))]
links=[]
for p in [DOC,HERE/'README.md']:
    for href in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text()):
        if href.startswith(('https:','http:','#','source:')):continue
        target=(p.parent/href.split('#')[0]).resolve()
        assert target.exists(),(str(p),href)
        links.append({'source':str(p.relative_to(ROOT)),'target':str(target.relative_to(ROOT))})
own=sorted(p for p in HERE.rglob('*') if p.is_file() and p.name!='self-check.json')
for p in own+[RECEIPT]:
    if p.suffix=='.py':ast.parse(p.read_text())
    if p.suffix=='.json':load(p)
result={'status':'PASS_STATIC_ONLY','sources':source_bindings,'primary_sources':1,'related_full_sources':11,
        'source_python_ast_files':ast_count,'source_json_files':json_count,'floor_rows':18,'repeated_corner_entries':144,
        'safe_displayed_menus':6,'formal_comparison_count':len(review['formal_comparisons']),
        'shared_core_asset_count':len(review['shared_core_assets']),'local_links':len(links),'links':links,
        'artifacts':[bind(p) for p in own+[DOC,RECEIPT]],'self_hash_excluded':True,'new_mathematical_runs':0}
(HERE/'self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','primary_sources','related_full_sources','local_links','new_mathematical_runs']}))
