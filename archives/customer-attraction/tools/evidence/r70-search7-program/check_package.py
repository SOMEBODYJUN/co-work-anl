"""Static saved-artifact checks; no C++ build, binary execution, DP or payoff recomputation."""
import ast
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
DOC=ROOT/'archives/customer-attraction/state/程序/七个极大主题的六人整数终局集合搜索程序--程序.md'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def binding(p):return dict(path=str(p.relative_to(ROOT)),bytes=p.stat().st_size,sha256=sha(p))
manifest=load(HERE/'source-manifest.json')
for item in manifest['primary_sources']:
    p=HERE/item['preserved_as']
    assert p.stat().st_size==item['size'] and sha(p)==item['sha256']
assert (HERE/'original/search7').read_bytes()[:4]==b'\x7fELF'
for item in manifest['formal_comparisons']:
    p=ROOT/item['path']
    assert p.stat().st_size==item['bytes'] and sha(p)==item['sha256']

run=load(HERE/'binary-event/execution.json')
assert run['source_inputs_before']==run['source_inputs_after']
for name,entry in run['source_inputs_before'].items():
    assert sha(HERE/'original'/name)==entry['sha256']
assert len(run['events'])==9 and all(x['exit_code']==0 for x in run['events'])
assert run['byte_identical_rebuild'] is False and run['short_stdout_stderr_equal'] is True
assert sha(HERE/'binary-event/rebuilt-search7')==run['rebuilt']['sha256']
assert run['requested_budget']==1 and run['explicit_seed']==192711 and not run['historical_scan_replayed']
for suffix in ['stdout','stderr']:
    assert (HERE/f'binary-event/original-short.{suffix}.txt').read_bytes()==(HERE/f'binary-event/rebuilt-short.{suffix}.txt').read_bytes()
assert 'evaluations 2' in (HERE/'binary-event/original-short.stderr.txt').read_text()
assert ' W 352 OPT 359 margin 345 terminal 1 3 0 0 2 0 0' in (HERE/'binary-event/original-short.stdout.txt').read_text()
for entry in run['events']:
    for suffix in ['stdout','stderr']:
        assert (HERE/f"binary-event/{entry['name']}.{suffix}.txt").stat().st_size==entry[suffix+'_bytes']

event=load(HERE/'last-point-execution.json')
audit=load(HERE/'last-point/point-audit.json')
assert event['exit_code']==0 and sha(HERE/'audit_last_point.py')==event['script_sha256']
assert audit['status']=='PASS_EXACT_LAST_LOG_POINT'
assert audit['new_DP_calls']==audit['new_full_strategy_audits']==1
assert audit['LP_calls']==audit['new_static_coverage_scans']==audit['original_binary_calls']==0
assert audit['unit_customers']==159 and audit['root_outcomes']==1
assert audit['minimum_SPE_welfare']==131 and audit['OPT6_from_shared_static_audit']==158
assert audit['actual_ordered_path']==[6,6,6,6,1,1]
assert (HERE/'last-point-stderr.txt').read_bytes()==b''
shared=HERE.parent/'r70-search7-log'
shared_files=[shared/'log-audit.json',shared/'static-coverages.json.gz']
for p,entry in zip(shared_files,audit['inputs']):
    assert p.stat().st_size==entry['bytes'] and sha(p)==entry['sha256']
assert hashlib.sha256(gzip.decompress(shared_files[1].read_bytes())).hexdigest()==audit['coverage_uncompressed_sha256']
assert sha(shared/'original/scan_36155.txt')==manifest['related_log']['sha256']

strategy=load(HERE/'last-point/complete-strategy.json')
assert sha(HERE/'last-point/complete-strategy.json')==audit['complete_strategy']['sha256']
entries={tuple(row['history']):row['action'] for row in strategy['entries']}
assert len(entries)==len(strategy['entries'])==19608
detail_file=HERE/'last-point/exact-details.json.gz'
assert sha(detail_file)==audit['details_gzip']['sha256']
unpacked=gzip.decompress(detail_file.read_bytes())
assert hashlib.sha256(unpacked).hexdigest()==audit['details_uncompressed_sha256']
detail=json.loads(unpacked)
assert len(detail['payoffs'])==924
assert len(detail['all_1716_state_outcomes'])==1716
assert all(len(row['outcomes'])==1 for row in detail['all_1716_state_outcomes'])
rows=detail['all_19608_history_checks']
assert len(rows)==19608 and {tuple(x['history']) for x in rows}==set(entries)
histogram=Counter()
for row in rows:
    action=row['action'];slacks=row['scaled60_slacks']
    assert entries[tuple(row['history'])]==action and len(slacks)==7
    assert slacks[action]==0 and all(v>0 for a,v in enumerate(slacks) if a!=action)
    histogram.update(slacks)
assert sum(histogram.values())==137256 and histogram[0]==19608
assert min(x for x in histogram if x)>0
assert {str(Fraction(k,60)):v for k,v in sorted(histogram.items())}==audit['exact_slack_histogram']
assert min(Fraction(k,60) for k in histogram if k)>0
assert min(Fraction(k,60) for k in histogram if k)==Fraction(1,10)

receipts=[]
for uid in ['5e061edecf721d433678','a7ba166b252219cc543d']:
    p=ROOT/f'cleanup/workspaces/Boss7/receipts-round17/{uid}.json'
    r=load(p)
    assert r['id']==uid and r['disposition']=='integrated'
    assert all(r[k] is True for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
    assert r['targets']==[str(DOC.relative_to(ROOT))]
    receipts.append(p)
links=[]
for p in [DOC,HERE/'README.md']:
    for href in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text()):
        if href.startswith(('http:','https:','#','source:')):continue
        q=(p.parent/href.split('#')[0]).resolve()
        assert q.exists(),(str(p),href)
        links.append(dict(source=str(p.relative_to(ROOT)),target=str(q.relative_to(ROOT))))
files=sorted(p for p in HERE.rglob('*') if p.is_file() and p.name!='self-check.json')
python_count=json_count=0
for p in files+receipts:
    if p.suffix=='.py':ast.parse(p.read_text());python_count+=1
    if p.suffix=='.json':load(p);json_count+=1
report=dict(status='PASS_STATIC_ONLY',scope='Saved-byte and structural consistency only; no fresh payoff, coverage, DP, original binary, compiler or optimizer execution.',
            primary_sources_checked=2,formal_comparison_bindings=8,shared_static_bindings=[binding(p) for p in shared_files],
            saved_event_counts=manifest['new_events'],
            saved_details_summary=dict(payoff_records=924,state_outcome_records=1716,all_saved_R_sizes=1,strategy_nodes=19608,comparisons=137256,self_zeros=19608,strict_nonself=117648,minimum_nonself_slack='1/10'),
            python_ast_files=python_count,json_files=json_count,local_links=len(links),links=links,
            artifacts=[binding(p) for p in files+[DOC]+receipts],self_hash_excluded=True,new_mathematical_runs=0)
(HERE/'self-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['status','primary_sources_checked','python_ast_files','json_files','local_links','new_mathematical_runs']}))
