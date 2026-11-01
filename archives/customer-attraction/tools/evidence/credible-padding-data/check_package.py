"""Static bytes, schemas, captured-shape and links only; do not rerun terminal or SPE math."""
import ast
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
PROGRAM=HERE.parent/'credible-padding-program'
BODY=ROOT/'archives/customer-attraction/state/计算/独立主题填充完整策略的三个有限审计点--计算.md'
IDS={1:'a08aeb402b14330df317',5:'dc2bf489908b5745178a',10:'aae53888308314649058'}


def read(p):
    return json.loads(p.read_text())


def fingerprint(p):
    b=p.read_bytes()
    return dict(path=str(p.relative_to(ROOT)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())


def main():
    sources=read(HERE/'source-manifest.json')['sources']
    for s in sources:
        b=(ROOT/s['preserved_path']).read_bytes()
        assert len(b)==s['size'] and hashlib.sha256(b).hexdigest()==s['sha256']
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==s['blob']
    for p in HERE.glob('*.py'):
        ast.parse(p.read_text())
    for p in HERE.rglob('*.json'):
        if p.name!='self-check.json':read(p)
    report=read(HERE/'terminal-audit.json')
    assert report['status']=='PASS' and report['independent_terminal_audit_runs']==1
    assert report['total_unit_clients']==146 and report['coverage_supports_checked']==185
    assert all(report[k]==0 for k in ['original_entries','original_helper_calls','BI_calls','LP_calls','full_DAG_IC_checks'])
    event=read(HERE/'execution.json')
    assert event['exit_code']==0 and event['stderr_bytes']==0
    assert event['script']['sha256']==fingerprint(HERE/'audit_terminal_data.py')['sha256']
    expected_nodes={1:(231,99,594),5:(3064,1771,10626),10:(27243,18669,112014)}
    for point in report['points']:
        k=point['k'];p=HERE/'original'/f'padding_k{k}.json';d=read(p)
        assert len(d)==16 and len(d['g'])==6 and len(d['instance']['customers'])==8
        assert list(d['instance'])==['topics','customers','players']
        assert all(list(c)==['topics','multiplicity'] for c in d['instance']['customers'])
        f=fingerprint(p)
        assert (f['bytes'],f['sha256'])==(point['input']['bytes'],point['input']['sha256'])
        assert tuple(d[x] for x in ['nodes','decision_nodes','comparisons'])==expected_nodes[k]
        assert point['original_DAG_statistics_recomputed'] is False
        assert point['original_DAG_statistics_retained']=={x:d[x] for x in ['nodes','decision_nodes','comparisons','minimum_slack']}
        assert point['g']==d['g'] and point['G']==d['G'] and point['M']==d['M'] and point['refined_tax_gap']==d['refined_tax_gap']
        assert point['actual_path']==d['path'] and point['actual_counts']==d['terminal']
        assert len(point['all_support_coverage_rows'])==point['coverage_supports_checked']
        assert len({r[0] for r in point['all_support_coverage_rows']})==len(point['all_support_coverage_rows'])
        for value in point['g']+[point['M'],point['G'],point['refined_tax_gap'],point['low_player_tax_deficit']]+point['actual_player_payoffs']:
            assert str(Fraction(value))==value
    old=(HERE/'original/padding_k1.json').read_bytes()
    assert old==(PROGRAM/'replay/report.json').read_bytes()
    pe=read(PROGRAM/'replay/execution.json');pc=read(PROGRAM/'replay/process-capture.json')
    assert pe['k']==1 and pe['assertions_enabled'] and pc['returncode']==0
    assert pe['inputs_before']==pe['inputs_after']
    assert pe['call_events']['all_k_padding.py:main']==1
    assert all(pe[x]==0 for x in ['helper_replacements','additional_original_calls','new_independent_DAG_or_IC_audits','canonical_certificate_or_verifier_calls','optimization_calls'])
    summary=read(PROGRAM/'replay/capture-summary.json')
    assert summary['source_report']==json.loads(old)
    raw=gzip.decompress((PROGRAM/'replay/original-dag.json.gz').read_bytes())
    assert len(raw)==summary['dag_uncompressed_bytes']==29200
    dag=json.loads(raw)
    assert dag['k']==1 and len(dag['nodes'])==231
    decisions=[n for n in dag['nodes'] if n['children']]
    assert len(decisions)==99 and all(len(n['children'])==6 for n in decisions)
    assert [n['id'] for n in dag['nodes']]==list(range(231))
    cache=read(PROGRAM/'replay/original-solver-cache.json')
    assert {k:len(v) for k,v in cache.items()}=={'outcomes':190,'thresholds':64,'payoffs':126}
    assert (PROGRAM/'replay/stderr.txt').read_bytes()==b''
    review=read(HERE/'review-record.json')
    for item in review['bindings']:
        assert fingerprint(ROOT/item['path'])==item
    links=[]
    for p in [BODY,HERE/'README.md']:
        s=p.read_text()
        assert not any(ord(c)<32 and c not in '\n\t' for c in s)
        assert s.endswith('\n') and not s.endswith('\n\n')
        assert all(t.rstrip()==t for t in s.splitlines())
        for link in re.findall(r'\[[^\]]+\]\(([^)]+)\)',s):
            if '://' in link or link.startswith('#'):continue
            target=(p.parent/link.split('#',1)[0]).resolve()
            assert target.exists(),(str(p),link)
            links.append(dict(source=str(p.relative_to(ROOT)),target=str(target.relative_to(ROOT))))
    front=BODY.read_text().split('---',2)[1]
    for key in ['id','kind','type_tag','title','status','summary','source_refs']:
        assert re.search('^'+key+':',front,re.M)
    receipts=[]
    for sid in IDS.values():
        p=ROOT/'cleanup/workspaces/Boss7/receipts-round18'/f'{sid}.json';d=read(p)
        assert d['id']==sid and d['disposition']=='integrated'
        assert all(d[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
        assert all((ROOT/t).exists() or ROOT/t==HERE/'self-check.json' for t in d['targets'])
        receipts.append(fingerprint(p))
    files=[fingerprint(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='self-check.json']
    result=dict(status='PASS',scope='Static saved outputs only; 0 payoff/IC/BI/LP or original-main reruns',
        sources_verified=len(sources),primary_reports=3,fields_per_report=16,unit_client_arithmetic_repeated=False,
        shared_and_comparison_bindings=len(review['bindings']),owned_fingerprints=files,body=fingerprint(BODY),receipts=receipts,
        links_checked=len(links),links=links,original_entries=0,independent_math_entries=0,BI=0,LP=0)
    (HERE/'self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    assert all((ROOT/t).exists() for sid in IDS.values() for t in read(ROOT/'cleanup/workspaces/Boss7/receipts-round18'/f'{sid}.json')['targets'])
    print(json.dumps({k:v for k,v in result.items() if k not in ['owned_fingerprints','links','receipts']},ensure_ascii=False))


if __name__=='__main__':main()
