#!/usr/bin/env python3
"""Static delivery integrity; do not import/run source or recompute payoff/BI/IC."""
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
BODY=ROOT/'archives/customer-attraction/state/程序/独立吸收主题填充策略的精确有序历史审计程序--程序.md'
RECEIPT=ROOT/'cleanup/workspaces/Boss7/receipts-round18/6f957bfb27488f5b01db.json'
R=HERE/'replay'


def read(path):return json.loads(path.read_text())


def verify(path,item):
    b=path.read_bytes()
    assert len(b)==item.get('bytes',item.get('size')),str(path)
    assert hashlib.sha256(b).hexdigest()==item['sha256'],str(path)


def main():
    own=read(HERE/'artifact-manifest.json')['files']
    for item in own:verify(ROOT/item['path'],item)
    sources=read(HERE/'source-manifest.json')['sources']
    assert len(sources)==11
    assert [x['id'] for x in sources if x['role']=='primary']==['6f957bfb27488f5b01db']
    for item in sources:
        verify(ROOT/item['preserved_path'],item)
        assert item['full_file_reviewed'] is True
    comparisons=read(HERE/'comparison-manifest.json')['files']
    for item in comparisons:verify(ROOT/item['path'],item)
    jsons=sorted(x for x in HERE.rglob('*.json') if x.name!='self-check.json')
    for path in jsons:read(path)
    scripts=sorted(HERE.rglob('*.py'))
    for path in scripts:ast.parse(path.read_text(),filename=str(path))
    body=BODY.read_text();header=body.split('---',2)[1]
    for name in ['id','kind','type_tag','title','status','summary','source_refs']:
        assert re.search(r'^'+name+':',header,re.M),name
    links=[]
    for document in [BODY,HERE/'README.md']:
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',document.read_text()):
            target=target.strip('<>').split('#',1)[0]
            if not target or re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:',target):continue
            assert (document.parent/target).resolve().exists(),(str(document),target)
            links.append({'document':str(document.relative_to(ROOT)),'target':target})
    event=read(R/'execution.json');process=read(R/'process-capture.json')
    assert event['inputs_before']==event['inputs_after']
    for item in event['inputs_before']:
        name=Path(item['path']).name
        path=HERE/'original'/name if name=='all_k_padding.py' else HERE/'dependencies/customer_attraction'/name
        verify(path,item)
    for name,item in event['files'].items():verify(R/name,item)
    assert event['k']==1 and event['assertions_enabled'] is True
    for key in ['helper_replacements','additional_original_calls','new_independent_DAG_or_IC_audits','canonical_certificate_or_verifier_calls','optimization_calls']:assert event[key]==0
    calls=event['call_events']
    for name,number in {'all_k_padding.py:main':1,'all_k_padding.py:instance':1,'all_k_padding.py:build':595,'all_k_padding.py:child_mode':204,'all_k_padding.py:fallback':133,'customer_attraction/exact.py:__init__':1,'customer_attraction/exact.py:outcomes':848,'customer_attraction/exact.py:_solve':1297,'customer_attraction/exact.py:threshold':65,'customer_attraction/exact.py:_utility':804}.items():assert calls[name]==number
    assert 'customer_attraction/exact.py:certificate' not in calls
    assert 'customer_attraction/certificate.py:verify_certificate' not in calls
    assert process['returncode']==0
    for name,item in process['outputs'].items():verify(R/('stderr.txt' if '.stderr.' in name else 'stdout.txt'),item)
    assert (R/'stderr.txt').stat().st_size==0
    original=HERE.parent/'credible-padding-data/original/padding_k1.json'
    assert original.read_bytes()==(R/'report.json').read_bytes()
    report=read(R/'report.json');locals_=read(R/'original-main-locals.json');summary=read(R/'capture-summary.json')
    assert report==locals_['report']==summary['source_report']==read(R/'stdout.txt')
    assert report['k']==1 and report['players']==4
    assert report['nodes']==231 and report['decision_nodes']==99 and report['comparisons']==594
    assert report['path']==[5,0,0,1] and report['terminal']==[2,1,0,0,0,1]
    assert report['minimum_slack']=='0' and report['refined_tax_gap']=='-51/7'
    raw=gzip.decompress((R/'original-dag.json.gz').read_bytes())
    assert len(raw)==summary['dag_uncompressed_bytes']==29200
    dag=json.loads(raw);nodes=dag['nodes'];assert dag['root']==locals_['root']==0 and len(nodes)==231
    assert [x['id'] for x in nodes]==list(range(231))
    assert len({json.dumps([x['counts'],x['mode']],separators=(',',':')) for x in nodes})==231
    assert len({tuple(x['counts']) for x in nodes})==210
    cache=read(R/'original-solver-cache.json')
    assert len(cache['outcomes'])==summary['BI_cached_count_states']==190
    assert len(cache['thresholds'])==summary['BI_cached_thresholds']==64
    assert len(cache['payoffs'])==summary['BI_cached_terminal_payoff_vectors']==126
    assert sum(len(x['terminals']) for x in cache['outcomes'])==summary['BI_retained_terminal_entries']==218
    outcome_map={tuple(x['counts']):{tuple(z) for z in x['terminals']} for x in cache['outcomes']}
    assert len(outcome_map)==190
    fractions=0
    for x in cache['thresholds']:
        assert str(Fraction(x['threshold']))==x['threshold'];fractions+=1
    for x in cache['payoffs']:
        assert len(x['counts'])==len(x['payoffs'])==6 and sum(x['counts'])==4
        for value in x['payoffs']:
            assert str(Fraction(value))==value;fractions+=1
    mode_counts=Counter();decision_modes=Counter();arcs=0;decisions=0
    # Only captured object structure/references are checked, no payoff/IC arithmetic.
    for node in nodes:
        c=node['counts'];mode=node['mode'];assert len(c)==6 and all(type(v) is int and v>=0 for v in c)
        assert len(node['end'])==6 and sum(node['end'])==4
        mode_counts[mode[0]]+=1
        if mode[0]=='S':
            assert len(mode)==2 and mode[1]==sorted(mode[1])
            assert [mode[1].count(a) for a in range(5)]==c[:5] and c[5]<=1
        else:
            assert mode[0]=='F' and len(mode)==3 and mode[1]==c
            assert mode[2]==node['end'] and tuple(mode[2]) in outcome_map[tuple(c)]
        if sum(c)==4:
            assert node['action'] is None and node['children']==[] and node['end']==c
        else:
            assert 0<=node['action']<6 and len(node['children'])==6
            decisions+=1;decision_modes[mode[0]]+=1;arcs+=6
            assert node['end']==nodes[node['children'][node['action']]]['end']
            for a,child in enumerate(node['children']):
                assert type(child) is int and 0<=child<len(nodes)
                expected=c[:];expected[a]+=1
                assert nodes[child]['counts']==expected
    assert dict(mode_counts)==summary['mode_counts']=={'S':40,'F':191}
    assert dict(decision_modes)==summary['decision_mode_counts']=={'S':34,'F':65}
    assert decisions==summary['decision_nodes']==99 and arcs==summary['arcs']==594
    seen=set();pending=[dag['root']]
    while pending:
        sid=pending.pop()
        if sid in seen:continue
        seen.add(sid);pending.extend(nodes[sid]['children'])
    assert len(seen)==231
    sid=dag['root'];path=[]
    while nodes[sid]['children']:
        a=nodes[sid]['action'];path.append(a);sid=nodes[sid]['children'][a]
    assert path==report['path'] and nodes[sid]['counts']==report['terminal']
    scope=read(HERE/'execution-scope.json')
    assert scope['original_main_runs']=={'k1':1,'k5':0,'k10':0}
    assert scope['call_events']==calls and scope['old13_packet_runs']==scope['new_independent_payoff_or_IC_runs']==0
    receipt=read(RECEIPT)
    assert receipt['id']=='6f957bfb27488f5b01db' and receipt['disposition']=='integrated'
    for key in ['full_file_reviewed','related_material_checked','unique_content_accounted_for']:assert receipt[key] is True
    for target in receipt['targets']:assert (ROOT/target).exists(),target
    result={'status':'PASS','scope':'Static source/event fingerprints, JSON/AST/canonical fractions, captured graph structure/end references, caches and local links; no original import, BI, payoff or IC recomputation.',
      'own_fingerprints':len(own),'source_bindings':len(sources),'comparison_bindings':len(comparisons),
      'JSON_files':len(jsons),'Python_AST_files':len(scripts),'local_links':len(links),'receipt_targets':len(receipt['targets']),
      'original_report_bytes_equal':True,'captured_nodes':231,'captured_decisions':99,'captured_arcs':594,'distinct_count_vectors':210,
      'BI_cache_outcome_records':190,'BI_cache_thresholds':64,'BI_cache_payoff_vectors':126,'Fraction_syntax_strings':fractions,
      'new_original_runs':0,'new_payoff_BI_IC_recomputations':0,'links':links}
    (HERE/'self-check.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='links'},ensure_ascii=False))


if __name__=='__main__':main()
