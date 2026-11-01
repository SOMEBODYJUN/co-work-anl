from pathlib import Path
import ast,json,hashlib,re,math
S=Path(__file__).resolve().parent
B=S.parent;R=B/'co-work-anl-boss3';D=B/'self_background_deliverables'
formal=D/'formal-object.md';receipts=D/'receipts-20261101-self-background-three.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sources=json.loads((S/'source-manifest.json').read_text())
for x in sources:
 p=S/'original'/Path(x['path']).name;assert p.stat().st_size==x['size'] and sha(p)==x['sha256']
for x in json.loads((S/'runtime-dependency-manifest.json').read_text()):
 p=S/'runtime-inputs'/x['path']
 if x['path'].endswith('prefix_coupled_seats_strict.json'):p=S/'excluded-current-example'/Path(x['path']).name
 assert p.stat().st_size==x['size'] and sha(p)==x['sha256']
for x in json.loads((S/'related-manifest.json').read_text()):
 p=S/x['path'];assert p.stat().st_size==x['size'] and sha(p)==x['sha256']
for p in S.rglob('*.py'):ast.parse(p.read_text())
for p in S.rglob('*.json'):json.loads(p.read_text())
pre=json.loads((S/'input-preflight.json').read_text());assert len(pre['files'])==22 and pre['explicit_runtime_Instances']==21 and pre['eligible_Instances']==17
old=json.loads((S/'original/signed_self_background_probe.json').read_text());new=json.loads((S/'replay/signed_self_background_probe.json').read_text())
for x in (old,new):x.pop('elapsed')
assert old==new and new['cones']==34 and new['lps']==1654 and new['maximum']==1.950000000000002
comparison=json.loads((S/'report-and-cohort-comparison.json').read_text())
assert comparison['total_new_original_entry_calls']==2 and comparison['total_new_LP_calls']==2764
assert comparison['new_unsigned_entry_calls']==0 and not comparison['unsigned_original_source_available']
assert sum(c['new_LPs'] for c in comparison['cohort'])==1654
assert all(c['new_LPs']==c['new_cones']*math.comb(c['k']+c['m']-1,c['k']-1) for c in comparison['cohort'])
first=json.loads((S/'first-full22-failed/execution-record.json').read_text());second=json.loads((S/'replay/execution-record.json').read_text())
assert first['exit_code']==1 and first['actual_runtime_JSON_files']==22 and not first['output_file_exists']
assert second['exit_code']==0 and second['actual_runtime_JSON_files']==21 and second['stderr_bytes']==0 and second['assertions_enabled']
assert 'invalid customer-attraction instance schema' in (S/'first-full22-failed/stderr.txt').read_text()
assert (S/'replay/stderr.txt').read_text()==''
body=formal.read_text();assert body.count('\\[')==body.count('\\]') and all(l.count('$')%2==0 for l in body.splitlines())
final_rel=Path('archives/customer-attraction/state/程序/终局自背景的有符号有限策略锥探针与双报告边界--程序.md')
link_count=0
for match in re.finditer(r'\]\(([^)]+)\)',body):
 href=match.group(1)
 if '://' in href or href.startswith('#'):continue
 p=(R/final_rel.parent/href.split('#')[0]).resolve();prefix=R/'archives/customer-attraction/tools/evidence/self-background-three-boss3'
 if p.is_relative_to(prefix):p=S/p.relative_to(prefix)
 assert p.exists(),str(p);link_count+=1
rr=json.loads(receipts.read_text());assert {x['id']for x in rr}=={x['id'] for x in sources} and all(x['disposition']=='integrated' for x in rr)
assert not any(S.rglob('__pycache__'))
result={'status':'all staged source/hash/schema/cohort/report/receipt/link checks passed','primary_sources':3,'canonical_code_and_example_sources_bound':27,'full_frozen_examples':22,'explicit_successful_Instances':21,'eligible_Instances':17,'current_entry_events':2,'first_event_exit':1,'successful_event_exit':0,'LP_calls_first_then_second':[1110,1654],'LP_calls_total':2764,'signed_report_equal_except_elapsed':True,'unsigned_old_code_gap_retained':True,'new_exact_negative_dual_certificates':0,'formal_links_checked':link_count,'inline_and_display_math_delimiters_balanced':True,'all_stage_only':True}
(S/'package-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
