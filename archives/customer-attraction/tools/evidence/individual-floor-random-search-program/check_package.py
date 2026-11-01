"""Static stored bytes/schema/links only. Never import or run original math."""
import ast
from fractions import Fraction
import gzip
import hashlib
from itertools import combinations
import json
import math
from pathlib import Path
import re

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
BODY=ROOT/'archives/customer-attraction/state/程序/三人六主题固定策略的逐人覆盖比线性探针--程序.md'
SID='75e5e8d6444d274ec58d'


def read(p):return json.loads(p.read_text())


def fingerprint(p):
    b=p.read_bytes()
    return dict(path=str(p.relative_to(ROOT)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())


def main():
    sources=read(HERE/'source-manifest.json')['sources']
    assert len(sources)==7
    for item in sources:
        p=ROOT/item['preserved_path'];b=p.read_bytes()
        assert len(b)==item['size'] and hashlib.sha256(b).hexdigest()==item['sha256']
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==item['blob']
    for p in HERE.rglob('*.py'):ast.parse(p.read_text())
    for p in HERE.rglob('*.json'):
        if p.name!='self-check.json':read(p)
    event=read(HERE/'replay/execution.json')
    assert event['inputs_before']==event['inputs_after'] and len(event['inputs_before'])==6
    assert event['assertions_enabled'] and event['error'] is None
    manifest_by_sha={s['sha256']:s for s in sources}
    for item in event['inputs_before']:
        s=manifest_by_sha[item['sha256']]
        assert s['size']==item['bytes']
    assert event['original_LP_calls']==123
    for key in ['helper_replacements','additional_original_calls','BI_calls','canonical_certificate_calls','new_independent_mathematical_audits']:
        assert event[key]==0
    counts=event['original_call_counts']
    src='research/workspaces/customer-attraction/R-731efdb50dd844178e597d804bdd4596/global_proof/individual_floor_search.py'
    assert counts[src+':<module>']==counts[src+':group_policy']==1
    assert counts['tests/audits/customer_attraction_strategy_lp.py:__post_init__']==1
    for name,record in event['files'].items():
        fp=fingerprint(HERE/'replay'/name)
        assert (fp['bytes'],fp['sha256'])==(record['bytes'],record['sha256'])
    process=read(HERE/'replay/process-capture.json')
    assert process['returncode']==0 and process['stdout_bytes']==147 and process['stderr_bytes']==0
    assert (HERE/'replay/stderr.txt').read_bytes()==b''
    model=read(HERE/'replay/original-model.json')
    assert model['topics']==6 and model['players']==3 and model['root']==[1,0,0,1,1,0]
    assert len(model['actions'])==43 and len(model['terminals'])==259
    assert len({tuple(r['history']) for r in model['actions']})==43
    assert len({tuple(r['history']) for r in model['terminals']})==259
    assert [sum(len(x['history'])==d for x in model['actions']) for d in range(3)]==[1,6,36]
    assert [sum(len(x['history'])==d for x in model['terminals']) for d in range(4)]==[1,6,36,216]
    assert len(model['rational_rows'])==len(model['float_matrix'])==185
    assert all(len(r)==63 for r in model['rational_rows']+model['float_matrix'])
    assert len(model['welfare'])==63
    # Rational string syntax only; no coefficient construction or IC dot products.
    assert all(str(Fraction(v))==v for r in model['rational_rows'] for v in r)
    raw=gzip.decompress((HERE/'replay/original-lp-results.json.gz').read_bytes())
    assert len(raw)==event['raw_LP_bytes']==1060816
    results=json.loads(raw);assert len(results)==123
    nonfinite={}
    def scan_nonfinite(value,path):
        if isinstance(value,dict):
            for key,item in value.items():scan_nonfinite(item,path+'.'+key)
        elif isinstance(value,list):
            for item in value:scan_nonfinite(item,path+'[]')
        elif isinstance(value,float) and not math.isfinite(value):
            assert value==math.inf
            nonfinite[path]=nonfinite.get(path,0)+1
    scan_nonfinite(results,'')
    assert nonfinite=={'[].result.upper.residual[]':7749}
    supports=[list(s) for k in range(1,4) for s in combinations(range(6),k)]
    summary=read(HERE/'replay/capture-summary.json')
    assert summary['LP_calls']==summary['successful']==123 and summary['statuses']=={'0':123}
    expected=[(4.205623901581722,[1,2,5]),(4.125,[1,2,4]),(4.714285714285714,[1,2,4])]
    stdout=[]
    for i,(value,portfolio) in enumerate(expected):
        rows=results[41*i:41*(i+1)]
        assert all(row['player']==i for row in rows)
        assert [row['portfolio'] for row in rows]==supports
        for row in rows:
            r=row['result'];assert r['success'] is True and r['status']==0
            assert len(row['objective'])==len(row['own'])==len(r['x'])==63
            assert all(str(Fraction(v))==v for v in row['objective']+row['own'])
            assert len(r['ineqlin']['residual'])==len(r['ineqlin']['marginals'])==185
            assert len(r['eqlin']['residual'])==len(r['eqlin']['marginals'])==1
            assert len(r['lower']['residual'])==len(r['upper']['residual'])==63
        assert all(row['own']==rows[0]['own'] for row in rows)
        best=min(rows,key=lambda row:row['result']['fun'])
        assert -best['result']['fun']==value and best['portfolio']==portfolio
        assert summary['players'][str(i)]==dict(LPs=41,successful=41,best_float_value=value,best_portfolio=portfolio)
        stdout.append(f'player {i} max O/u {value} support {tuple(portfolio)}\n')
    assert (HERE/'replay/stdout.txt').read_text()==''.join(stdout)
    review=read(HERE/'review-record.json')
    for item in review['bindings']:assert fingerprint(ROOT/item['path'])==item
    links=[]
    for p in [BODY,HERE/'README.md']:
        text=p.read_text()
        assert not any(ord(c)<32 and c not in '\n\t' for c in text)
        assert text.endswith('\n') and not text.endswith('\n\n')
        assert all(t.rstrip()==t for t in text.splitlines())
        for link in re.findall(r'\[[^\]]+\]\(([^)]+)\)',text):
            if '://' in link or link.startswith('#'):continue
            target=(p.parent/link.split('#',1)[0]).resolve()
            assert target.exists() or target==HERE/'self-check.json',(str(p),link)
            links.append(dict(source=str(p.relative_to(ROOT)),target=str(target.relative_to(ROOT))))
    front=BODY.read_text().split('---',2)[1]
    for key in ['id','kind','type_tag','title','status','summary','source_refs']:
        assert re.search('^'+key+':',front,re.M)
    receipt_path=ROOT/'cleanup/workspaces/Boss7/receipts-round19'/f'{SID}.json'
    receipt=read(receipt_path)
    assert receipt['id']==SID and receipt['disposition']=='integrated'
    assert all(receipt[k] for k in ['full_file_reviewed','related_material_checked','unique_content_accounted_for'])
    assert all((ROOT/t).exists() or ROOT/t==HERE/'self-check.json' for t in receipt['targets'])
    files=[fingerprint(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='self-check.json']
    result=dict(status='PASS',scope='Static stored original model/results only; no LP, IC, BI, certificate or original-entry rerun',
        sources_verified=len(sources),event_inputs_verified=6,stored_LP_records_checked=123,
        stored_model_shape=[185,63],stored_policy_nodes=43,stored_terminal_lookup_nodes=259,
        comparisons_bound=len(review['bindings']),owned_fingerprints=files,body=fingerprint(BODY),receipt=fingerprint(receipt_path),
        links_checked=len(links),links=links,original_entries=0,LP_calls=0,independent_math_entries=0)
    (HERE/'self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    assert all((ROOT/t).exists() for t in receipt['targets'])
    print(json.dumps({k:v for k,v in result.items() if k not in ['owned_fingerprints','links']},ensure_ascii=False))


if __name__=='__main__':main()
