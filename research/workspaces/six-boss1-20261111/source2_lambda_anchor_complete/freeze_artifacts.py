#!/usr/bin/env python3
"""Write endpoint presentation and the final deterministic package hashes."""
from fractions import Fraction
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def read(name):
    return json.loads((HERE/name).read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    generator=read('generator_output.json')
    checker=read('literal_checker_output.json')
    assert generator['status']==checker['status']=='PASS'
    assert generator['counts']['row_count']==checker['counts']['rows']==160
    assert generator['counts']['full_column_count']==checker['counts']['full_columns']==82080
    pins=read('source_pins.json')['sources']
    for pin in pins:
        assert digest(ROOT/pin['repository_relative_path'])==pin['sha256']
    domains=read('parameter_domains.json')['families']
    catalog=read('row_catalog.json')
    lines=['# 两个完整域的全部32个端点','','参数顺序为 $(\\tau_3,\\tau_4,\\tau_5,\\lambda)$。全部数值为精确有理数；每个域都含16顶点。下面的源IC权 $a$ 与独立K系数 $S$ 均保留原尺度。','']
    for group,title in [('six_mean','六均值 $q_0=1/6$'),('ordered_five','Ordered $q_0=1/5$')]:
        lines += ['## '+title,'','| 顶点 | λ | τ3 | τ4 | τ5 | 源IC权 a |','|---|---|---|---|---|---|']
        records=[]
        for v in domains[group]['vertices']:
            rid=('six_C_only_' if group=='six_mean' else 'ordered_')+v['id']
            meta=next(r for r in catalog if r['id']==rid)
            t3,t4,t5,lam=v['point']
            assert meta['parameters']==v['point']
            lines.append('| '+' | '.join([v['id'],lam,t3,t4,t5,meta['source_IC_weight']])+' |')
            records.append((v,meta))
        lines += ['','| 顶点 | β3 | β4 | β5 | 总中间帽 B | 通用/ordered K系数 S |','|---|---|---|---|---|---|']
        for v,meta in records:
            b=list(map(Fraction,meta['middle_caps']));B=sum(b)
            lines.append('| '+' | '.join([v['id']]+[str(x) for x in b]+[str(B),str(1+B)])+' |')
        lines += ['','所有活跃面及四个独立活跃边界基在 parameter_domains.json 中完整保存。','']
    lines += ['## 行族与等式','','六均值每个端点保留八合法目标通用行和一条C-only行。通用行的K系数为 $S$；C-only的K系数为1，其自由C等式乘子为 $B=S-1$。Ordered每个端点保留一条同六菜单行，K系数为 $S$。全部160 raw行均保留。','']
    (HERE/'endpoint_table.md').write_text('\n'.join(lines))
    index=HERE.with_suffix('.md')
    for path in (HERE/'proof.md',HERE/'geometry.md',HERE/'endpoint_table.md',index):
        content=path.read_text()
        assert not any(ord(c)<32 and c!='\n' for c in content)
    exclusions={'freeze_manifest.json','SHA256SUMS'}
    paths=sorted(p for p in HERE.iterdir() if p.is_file() and p.name not in exclusions)
    artifacts=[{'path':p.name,'sha256':digest(p),'bytes':p.stat().st_size} for p in paths]
    artifacts.append({'path':'../'+index.name,'sha256':digest(index),'bytes':index.stat().st_size})
    manifest={
        'status':'FROZEN',
        'package':'source2_lambda_anchor_complete',
        'research_id':'six-boss1-20261111',
        'scope':'source 2, complete exact anchor domain without an imposed lambda lower bound',
        'optimizer_calls':0,
        'global_LP_inputs_candidates_or_optimum_faces_read':False,
        'added_to_current_3056_plan':False,
        'rows':{'six_general_eight_legal_targets':128,'six_C_only':16,'ordered_same_six_menu':16,'total_raw':160},
        'columns_per_row':513,
        'numeric_positive_divisor':'25',
        'geometry':{'domains':2,'facets_per_domain':10,'vertices_per_domain':16,'lambda_layers':{'six_mean':{'5/3':1,'15':7,'16':8},'ordered_five':{'2':1,'15':7,'16':8}},'lambda_lower_is_research_window':False},
        'generator_status':generator['status'],
        'literal_checker_status':checker['status'],
        'counts':checker['counts'],
        'all_source_pins_unchanged':True,
        'sources':pins,
        'artifacts':artifacts,
        'checksum_note':'SHA256SUMS covers all listed artifacts and this manifest; no circular self hash.',
        'post_freeze_rule':'stop writing this frozen package and its same-name index'
    }
    (HERE/'freeze_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    checks=[(a['sha256'],a['path']) for a in artifacts]+[(digest(HERE/'freeze_manifest.json'),'freeze_manifest.json')]
    (HERE/'SHA256SUMS').write_text(''.join(sha+'  '+name+'\n' for sha,name in checks))
    print(json.dumps({'status':'FROZEN','checksum_entries':len(checks),'manifest_sha256':digest(HERE/'freeze_manifest.json'),'exact_family_sha256':digest(HERE/'exact_family.json'),'proof_sha256':digest(HERE/'proof.md'),'checker_output_sha256':digest(HERE/'literal_checker_output.json'),'SHA256SUMS_sha256':digest(HERE/'SHA256SUMS')},ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
