#!/usr/bin/env python3
"""Static packaging checks only; never import/run mathematical programs."""
import ast
import gzip
import hashlib
import json
from pathlib import Path
import re

HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'cleanup/receipt-example.json').exists())


def check_record(x):
    p=ROOT/x['path']
    b=p.read_bytes()
    assert len(b)==x['bytes'],p
    assert hashlib.sha256(b).hexdigest()==x['sha256'],p
    if 'blob' in x:
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['blob'],p


def main():
    m=json.loads((HERE/'source-manifest.json').read_text())
    checked=0
    for group in ('sources','related','dependencies','comparisons','assets'):
        for x in m[group]:
            check_record(x)
            checked+=1
    jsons=0
    asts=0
    for p in HERE.rglob('*'):
        if p.suffix=='.json' and p.name!='self-check.json':
            json.loads(p.read_text());jsons+=1
        elif p.suffix=='.py':
            ast.parse(p.read_text());asts+=1
    event=json.loads((HERE/'execution.json').read_text())
    assert event['exit_code']==0 and event['source_before']==event['source_after']
    assert event['counts']=={'original_main':0,'original_function':0,'LP':0,'MILP':0,'independent_definition_audit':1}
    assert hashlib.sha256((HERE/'audit_reports.py').read_bytes()).hexdigest()==event['script']['sha256']
    report=json.loads((HERE/'exact/exact-audit.json').read_text())
    raw=gzip.decompress((HERE/'exact/full-history-ledger.json.gz').read_bytes())
    assert len(raw)==report['details']['decoded']['bytes']
    assert hashlib.sha256(raw).hexdigest()==report['details']['decoded']['sha256']
    ledgers=json.loads(raw)
    assert len(ledgers)==2
    for x in ledgers:
        assert len(x['full_history_comparisons'])==1554
        assert len(x['root_query_rows'])==56 and len(x['tail_query_rows'])==6
    docs=[ROOT/x for x in m['bodies']]+[HERE/'README.md']
    links=0
    for p in docs:
        for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
            if target.startswith(('http:', 'https:', '#')):
                continue
            target=target.split('#',1)[0]
            resolved=(p.parent/target).resolve()
            if resolved != HERE/'self-check.json':
                assert resolved.exists(),(str(p),target)
            links+=1
    target_count=0
    all_targets=[]
    for ident in m['primary_ids']:
        p=ROOT/f'cleanup/workspaces/Boss7/receipts-round21/{ident}.json'
        receipt=json.loads(p.read_text())
        assert receipt['id']==ident
        assert all(receipt[x] is True for x in ('full_file_reviewed','related_material_checked','unique_content_accounted_for'))
        for target in receipt['targets']:
            all_targets.append(ROOT/target)
            if ROOT/target != HERE/'self-check.json':
                assert (ROOT/target).exists(),target
            target_count+=1
    out=dict(status='PASS',kind='static checks only; no mathematical replay',
             fingerprints=checked,primary_sources=len(m['sources']),related_sources=len(m['related']),
             dependencies=len(m['dependencies']),comparisons=len(m['comparisons']),
             json_files=jsons,python_AST=asts,actual_links=links,receipt_targets=target_count,
             detail_records=[1554,1554],independent_math_events_in_package=1,
             original_main=0,LP=0,MILP=0)
    (HERE/'self-check.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    assert all(x.exists() for x in all_targets)
    print(json.dumps(out,ensure_ascii=False))


if __name__=='__main__':
    main()
