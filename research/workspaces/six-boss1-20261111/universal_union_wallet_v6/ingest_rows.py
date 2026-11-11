#!/usr/bin/env python3
"""Exact ingestion interface only. No optimizer and no automatic release.

main_release.json must record Main's future explicit release, exact family
and proof SHA, and numerical divisor. A pending preparation config is insufficient.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from copy import deepcopy
import json

HERE=Path(__file__).resolve().parent
WS=HERE.parent
read=lambda p:json.loads(p.read_text())
sha=lambda p:sha256(p.read_bytes()).hexdigest()

def save(n,x):
    (HERE/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')

def main():
    config=read(HERE/'preparation_config.json')
    assert (HERE/'main_release.json').exists(), 'Await Main exact source25 release; no ingestion or optimizer authorized yet'
    release=read(HERE/'main_release.json')
    assert release['authorized_by']=='/root' and release['status']=='MAIN_EXPLICIT_867_ROW_RELEASE'
    assert release['optimizer_calls_authorized']==1
    assert release['family_path']==config['family_path'] and release['proof_path']==config['proof_path']
    for role in ('family','proof'):
        assert len(release[role+'_sha256'])==64
        assert sha(WS/release[role+'_path'])==release[role+'_sha256']
    pins=read(HERE/'prior_frozen_hashes.json')
    for n,h in pins.items():assert sha(WS/n)==h,n
    assert len(pins)==163
    assert sha(WS/config['baseline_input'])==config['baseline_input_sha256']
    assert sha(WS/config['baseline_certificate'])==config['baseline_certificate_sha256']
    assert not (HERE/'exact_input.json').exists() and not (HERE/'single_lp_started.txt').exists()
    base=read(WS/config['baseline_input']);family=read(WS/release['family_path'])
    for n,h in release['source_sha256'].items():assert sha(WS/n)==h,n
    rootrow=read(WS/release['root_row_path'])
    assert sha(WS/release['root_row_path'])==release['root_row_sha256']
    assert rootrow['name']=='ROOT30_B2_CAPACITY_FEEDBACK' and F(rootrow['numerical_divisor'])==1
    assert set(rootrow['a'])=={str(j) for j in range(257)} and F(rootrow['rhs'])==0
    assert len(base['raw_rows'])==546 and len(family['rows'])==320
    assert base['variables']==257 and base['nonnegative_columns']==list(range(257))
    divisor=F(release['new_row_numerical_divisor']);assert divisor>0
    for r in family['rows']:
        assert set(r['a'])=={str(j) for j in range(257)} and F(r['rhs'])==0
        assert F(r['numerical_divisor'])==divisor
    inp=deepcopy(base)
    inp['scope']='v6 planned exact867 raw necessary rows,full256 types+K;546 baseline raw unchanged plus released320 source25 andoneROOT30_CAP2.'
    inp['raw_rows']=deepcopy(base['raw_rows'])+deepcopy(family['rows'])+[deepcopy(rootrow)]
    assert inp['raw_rows'][:546]==base['raw_rows'] and len(inp['raw_rows'])==867
    seen={};unique=[];mapping=[];zeros=[];duplicates=[]
    for k,r in enumerate(inp['raw_rows']):
        key=(tuple(F(r['a'].get(str(j),'0')) for j in range(257)),F(r['rhs']))
        if not any(key[0]) and key[1]==0:
            zeros.append(r['name']);mapping.append({'raw_index':k,'name':r['name'],'status':'zero','unique_index':None});continue
        if key in seen:
            first,uid=seen[key]
            duplicates.append({'name':r['name'],'identical_to':inp['raw_rows'][first]['name']})
            mapping.append({'raw_index':k,'name':r['name'],'status':'duplicate','first_raw_index':first,'unique_index':uid});continue
        uid=len(unique);seen[key]=(k,uid);unique.append(deepcopy(r))
        mapping.append({'raw_index':k,'name':r['name'],'status':'kept','unique_index':uid})
    inp['unique_rows']=unique;inp['raw_inequality_count']=867;inp['unique_inequality_count']=len(unique)
    inp['removed_zero_rows']=zeros;inp['removed_exact_duplicate_rows']=duplicates
    inp['v6_main_release_sha256']=sha(HERE/'main_release.json')
    inp['v6_source_sha256']=release['source_sha256']
    save('exact_input.json',inp);save('duplicate_mapping.json',mapping)
    scales={}
    for r in unique:
        s=F(r['numerical_divisor']) if 'numerical_divisor' in r else max([F(1),abs(F(r['rhs']))]+[abs(F(v)) for v in r['a'].values()])
        assert s>0;scales[r['name']]=str(s)
    save('numerical_scaling.json',{'scope':'Exact original input unscaled; solver may only divide by these positive values.','scales':scales})
    report={'status':'INGESTED_ONLY_NOT_SOURCE_CHECKED','optimizer_calls':0,'raw_rows':867,'unique_rows':len(unique),'columns':257,
        'unchanged_old_raw_rows':546,'old_frozen_files_unchanged':163,'input_sha256':sha(HERE/'exact_input.json'),
        'release_sha256':sha(HERE/'main_release.json'),'requirement':'Independent source preflight required before the sole authorized LP.'}
    save('row_ingest_check.json',report);print(json.dumps(report,indent=2))

if __name__=='__main__':main()
