from pathlib import Path
import json,hashlib,re
BASE=Path(__file__).resolve().parents[4]
CANON=Path('/workspace/scratch/37f0f9248cfc/boss4-research')
WS=BASE/'cleanup/workspaces/Boss4/resume-amount-family-20261101'
EV=BASE/'archives/customer-attraction/subarchives/six-providers/tools/evidence/amount-cap-one-family-primary'
OBJ=BASE/'archives/customer-attraction/subarchives/six-providers/state/程序/金额cap1完整策略锐族的原程序与四百动作证书--程序.md'
manifest=json.loads((EV/'source-manifest.json').read_text())
for m in manifest:
    d=(BASE/m['local_path']).read_bytes()
    assert len(d)==m['size'] and hashlib.sha256(d).hexdigest()==m['sha256']
assert len(manifest)==5 and sum(m['size'] for m in manifest)==54013
receipts=json.loads((WS/'semantic-receipts.json').read_text())
assert {r['id'] for r in receipts}=={r['id'] for r in manifest}
for r in receipts:
    assert all(r[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
    assert all(r[k] for k in ['read_note','comparison_note','decision_note','targets'])
    for target in r['targets']:assert (BASE/target).exists() or (CANON/target).exists(),target
text=OBJ.read_text()
for m in manifest:
    for s in m['sources']:assert 'source:'+s['commit']+':'+s['path'] in text
links=[]
for p in [OBJ,EV/'README.md']:
    for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
        if link.startswith(('http','#')):continue
        q=(p.parent/link.split('#')[0]).resolve()
        good=q.exists()
        if not good:
            try:good=(CANON/q.relative_to(BASE)).exists()
            except ValueError:pass
        assert good,(p.name,link)
        links.append(link)
old=Path('/workspace/scratch/37f0f9248cfc/boss4-next-cache/r3-amount-cap-one-family-certificate-and-reviews-primary/archives/customer-attraction/state/程序/金额cap1锐族的四百节点原证书与审查读序--程序.md').read_text()
# Only compare the unchanged Markdown data segment, without reevaluating a strategy or rescanning raw action structure.
a='## 完整400动作的无损表式';b='本批结构核对这些动作的history键域'
old_table=old[old.index(a):old.index(b)]
new_table=text[text.index(a):text.index('此前同SHA结构核对记录显示这些动作的history键域')]
assert old_table==new_table
scope=json.loads((EV/'execution-scope.json').read_text())
assert all(scope[k]==0 for k in ['current_original_entry_runs','current_imports','current_payoff_or_IC_replays','new_mathematical_implementation_runs','new_solver_or_SPE_search_runs','current_repeated_400_action_structural_scans'])
res={'status':'PASS','scope':'source size/SHA, five semantic receipt targets, source refs, formal links and inherited unchanged Markdown table byte segment only; no IC/payoff/program execution','primary_files':5,'primary_bytes':54013,'receipt_dispositions':[r['disposition'] for r in receipts],'links_checked':len(links),'raw_frozen_actions_revalidated':False,'new_math_runs':0,'inherited_table_segment_unchanged':True}
(WS/'self-check-result.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(res,ensure_ascii=False))
