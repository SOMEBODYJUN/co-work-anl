"""Compare already computed exact reports; do not rebuild or run a generator."""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import ast
import hashlib
import json

HERE=Path(__file__).resolve().parent
SHA='f6f4d5c28857e8e6350bdc8528daa6109122bce8a6fb00e8ac5c3150ffc42314'


def read(path):
    raw=path.read_bytes()
    return json.loads(raw),{'path':str(path.relative_to(HERE.parent)),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}


def canonical(value):
    return tuple(canonical(x) for x in value) if isinstance(value,(list,tuple)) else value


def main():
    data,datameta=read(HERE/'independent-point-audit.json')
    original,originalmeta=read(HERE/'rerun/original-row-slacks.json')
    floor,floormeta=read(HERE.parent/'all-reply-actual-floors-program/floor-row-audit.json')
    cut,cutmeta=read(HERE.parent/'old-query-grid-cut-data/independent-report.json')
    mixed,mixedmeta=read(HERE.parent/'mixed-pair-reply-rows-program/exact-audit.json')
    assert data['source']['sha256']==cut['point']['sha256']==SHA
    rows=original['ordered_rows']
    assert [r['index'] for r in rows]==list(range(4963))
    assert all(F(r['slack'])>=0 for r in rows)
    byname={r['name']:F(r['slack']) for r in rows}
    assert len(byname)==len(rows)
    overlap={r['column']:r for r in data['overlap_records']}
    groups={(r['hist_column'],canonical(r['group'])):r for r in data['reply_groups']}
    upper_count=0
    for row in rows:
        if not row['name'].startswith('overlap-upper:'):continue
        _,number,source=row['name'].split(':',2)
        ov=overlap[int(number)]
        g=canonical(ast.literal_eval(source))
        independent=F(groups[ov['hist_column'],g]['R'])-F(ov['overlap'])
        assert independent==F(row['slack'])
        upper_count+=1
    assert upper_count==2612
    group_offsets={}
    for record in data['reply_groups']:
        hi=record['hist_column']
        offset=group_offsets.get(hi,0)
        old_column=record['hist_column_old']+1+offset
        assert byname['joint-state-upper:'+str(old_column)]==F(record['implicit00'])
        group_offsets[hi]=offset+1
    assert sum(group_offsets.values())==194
    for item in data['actual_BC_floors']:
        bit=1 if item['theme']=='B' else 2
        name='actual-floor:'+str((item['actual_player']-1,bit))
        assert byname[name]==F(item['slack'])
    for item in data['old_BC_capacities']:
        bit=1 if item['theme']=='B' else 2
        assert byname['old-capacity:'+str(bit)]==F(item['slack'])
    for item in data['optimum_one_replace']:
        assert byname['OPT-one-replace:'+str(item['query'])]==F(item['slack'])
    for item in data['split_capacities']:
        member,f,d=item['member'],item['family'],item['diag']
        name=('new_B_capacity' if member=='R' else str(('basic',0,'capacity'))) if f==0 else str((member,d,'capacity'))
        assert byname[name]==F(item['slack'])
    old=next(p for p in floor['points'] if p['sha256']==SHA)
    assert old['coefficient_equalities']==36*1905
    for item in old['slacks']:
        name='new-reply-floor:'+str(tuple(item['key']))
        assert byname[name]==F(item['value'])
    assert sum(F(s['value'])==0 for s in old['slacks'])==7
    assert len(cut['selected_rows'])==8 and all(F(r['slack'])<0 for r in cut['selected_rows'])
    mp=next(p for p in mixed['points'] if p['input']['sha256']==SHA)
    assert mp['negative_rows']==7 and mp['old_cut_distinct_vectors']==3
    for a,b in zip(cut['selected_rows'],mp['old_cut_mapping']):
        assert a['cut']==b['cut'] and a['mixed_pair_key']==b['mixed_key'] and F(a['slack'])==F(b['slack'])
    blocks=[]
    specifications=[('base',702),('initial_R',37),('R_index_classes',100),('Z_basic_and_old',64),
                    ('joint_state_upper',194),('attractive_R_cross',180),('overlap_upper',2612),
                    ('split_basic',56),('old_floor_capacity',14),('OPT_one_replace',8),
                    ('old_priced',960),('new_reply_floor',36)]
    start=0
    for label,count in specifications:
        block=rows[start:start+count]
        blocks.append({'block':label,'start':start,'count':count,'zero_slacks':sum(F(r['slack'])==0 for r in block)})
        start+=count
    assert start==4963 and sum(x['zero_slacks'] for x in blocks)==2240
    root=next(p for p in HERE.parents if (p/'cleanup/OBJECTS.md').exists())
    floor_point=json.loads((root/data['source']['path']).read_text())
    mixed_point_path=HERE.parent/'mixed-pair-reply-necessary-point/original/all_reply_mixed_pair_exact.json'
    mixed_point,mixed_point_meta=read(mixed_point_path)
    desc=lambda c:{k:v for k,v in c.items() if k!='weight'}
    assert [desc(c) for c in floor_point['columns']]==[desc(c) for c in mixed_point['columns']]
    changed=[i for i,(a,b) in enumerate(zip(floor_point['columns'],mixed_point['columns'])) if F(a['weight'])!=F(b['weight'])]
    differences=dict(Counter(floor_point['columns'][i]['kind'] for i in changed))
    assert len(changed)==124 and differences=={'joint-reply':70,'overlap':54}
    assert floor_point['W']==mixed_point['W']
    report={'scope':'read-only reconciliation of existing exact reports; no repeated graph, 9900 grid, mixed CLI or LP',
            'sources':[datameta,originalmeta,floormeta,cutmeta,mixedmeta,mixed_point_meta],
            'point_sha256':SHA,'independent_to_original_equalities':{'joint_state_upper':194,'overlap_upper':2612,'actual_BC_floors':12,'old_BC_capacities':2,'split_RZ_capacities':6,'OPT_one_replace':8},
            'reused_36_floor_slacks_equal_original':36,
            'reused_36_floor_coefficient_checks':68580,
            'original_row_blocks':blocks,'old_grid_cuts':{'negative_records':8,'distinct_vectors':3,'minimum_slack':str(min(F(r['slack']) for r in cut['selected_rows']))},
            'mixed_pair':{'negative_rows':mp['negative_rows'],'minimum_slack':mp['minimum_slack'],'first_min_key':mp['first_min_key']},
            'later_mixed5043_point':{'all1905_descriptors_equal':True,'W_equal':True,'different_weight_columns':124,'differences_by_kind':differences,'changed_column_ids':changed},
            'all_checks_pass':True}
    (HERE/'reused-report-bindings.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('independent_to_original_equalities','reused_36_floor_slacks_equal_original','all_checks_pass')},indent=2))


if __name__=='__main__':main()
