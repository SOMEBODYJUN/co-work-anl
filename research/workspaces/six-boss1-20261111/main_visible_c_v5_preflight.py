"""Main: full literal 3056-row audit and explicit one-call solver release.

All five new source proofs were independently checked before this script.
This script performs no optimization and never edits a frozen input or solver.
"""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as F
from itertools import product
from collections import Counter
from copy import deepcopy
import json

W=Path(__file__).resolve().parent;R=W.parents[2]
P=W/'visible_maximum_joint_v5';S=W/'visible_maximum_joint_v5_solve';B=W/'visible_maximum_joint_v4'
def read(p):return json.loads(p.read_text())
def h(p):return sha256(p.read_bytes()).hexdigest()
def put(p,d):
    with p.open('x') as f:f.write(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def canonical(v):return sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()

def main():
    assert h(P/'exact_input.json')=='12f456dfbc789a5c1826d248e4851b84f66b428554d181b7ba12cbfdb920f3ac'
    assert h(P/'freeze_manifest.json')=='b49d8bba4197fc6d656005770dace9c5a777816b5e3eaa1105565fb23db51a27'
    assert h(S/'scaffold_manifest.json')=='f3720a30fddd4625321aa0c9b56632ce4854ef30c31de0db43a93703740694b7'
    man=read(P/'freeze_manifest.json');pins=read(P/'source_pins.json')['sources']
    for name,digest in man['artifacts'].items():
        assert Path(name).name==name and h(P/name)==digest,name
    for name,digest in pins.items():assert h(R/name)==digest,name
    data=read(P/'exact_input.json');base=read(B/'exact_input.json')
    scales=read(P/'numerical_scaling.json');oldscales=read(B/'numerical_scaling.json')
    rows=data['raw_rows'];assert len(rows)==data['raw_inequality_count']==3056
    assert data['variables']==513 and data['K_column']==512 and data['nonnegative_columns']==list(range(513))
    assert data['equality_count']==len(data['equalities'])==2
    assert data['bit_order']==['a1','a2','a3','a4','a5','a6','x','o','c']
    assert rows[:1586]==base['raw_rows']
    for key in ['variables','K_column','nonnegative_columns','equality_count','equalities','objective',
                'bit_order','atom_columns','inequality_convention']:
        assert data[key]==base[key],key
    expected=[('all_source_ordered_menu_cells',181),('source2_cap_coupled_internal_safe',28),
              ('source2_minimal_cap_safe',28),('all_source_minimal_cap_safe',1096),('ordered_minimal_cap',137)]
    start=1586;blocks=[]
    for package,count in expected:
        source=read(W/package/'exact_family.json')['rows']
        assert len(source)==count and rows[start:start+count]==source
        blocks.append({'package':package,'start':start,'stop':start+count,'count':count,'source_sha256':h(W/package/'exact_family.json')})
        start+=count
    assert start==3056
    assert scales['raw_order']==[r['name'] for r in rows]
    assert scales['raw_order'][:1586]==oldscales['raw_order']
    assert len(scales['raw_scales'])==len(set(scales['raw_order']))==3056
    for k,row in enumerate(rows):
        name=row['name'];d=scales['raw_scales'][name]
        assert F(d)>0
        assert d==(oldscales['raw_scales'][name] if k<1586 else '25')
        for j in range(513):F(row['a'].get(str(j),'0'))
        F(row['rhs'])
    assert Counter(r['rhs'] for r in rows)=={'0':3026,'-1':30}
    assert rows[45]['a']=={} and rows[45]['rhs']=='0'
    for j,bits in enumerate(product((0,1),repeat=9)):
        atom=data['atom_columns'][j]
        assert atom=={'index':j,'old_index':j//2,'a':list(bits[:6]),'x':bits[6],'o':bits[7],'c':bits[8]}
        assert F(data['objective'].get(str(j),'0'))==int(any(bits[:6]))
        assert F(data['equalities'][0]['a'].get(str(j),'0'))==bits[7]
        assert F(data['equalities'][1]['a'].get(str(j),'0'))==bits[8]
    assert F(data['objective'].get('512','0'))==0
    assert F(data['equalities'][0]['a'].get('512','0'))==0
    assert F(data['equalities'][1]['a']['512'])==-1
    assert [F(e['rhs']) for e in data['equalities']]==[F(1),F(0)]
    reviews=['main_ordered_cells_check.json','main_cap_coupled_complete_check.json',
             'main_minimal_cap_source2_check.json','main_all_source_minimal_cap_safe_check.json',
             'main_ordered_minimal_cap_check.json']
    review_pins={name:h(W/name) for name in reviews}
    for name in reviews:assert read(W/name)['status'].startswith('PASS')
    result={'status':'PASS_MAIN_FULL3056_LITERAL_SOURCE_CONCATENATION_AND_MODEL',
            'input_sha256':h(P/'exact_input.json'),'preparation_manifest_sha256':h(P/'freeze_manifest.json'),
            'raw_rows':3056,'variables':513,'equalities':2,'all_rational_column_positions_checked':3056*513,
            'literal_old_rows':1586,'appended_rows':1470,'rhs_minus_one_rows':30,
            'all_zero_duplicate_root_and_nonoptimal_types_preserved':True,'source_blocks':blocks,
            'independent_source_domain_and_true_cost_review_pins':review_pins,
            'artifact_checks':len(man['artifacts']),'source_sha_checks':len(pins),
            'optimizer_calls':0,'half_status':'OPEN',
            'scope':'Original-model universal necessary rows; complete domains, source proof and all raw coefficients personally reviewed. Does not claim SPE realizability.'}
    put(W/'main_visible_c_v5_preflight.json',result)
    release=read(S/'main_release.template.json')
    release.update(status='MAIN_EXPLICIT_FULL3056_RAW_V5_SINGLE_LP_RELEASE',authorized_by='/root',
                   optimizer_calls_authorized=1,input_read_authorized=True,source_closure_read_authorized=True,
                   planning_contract_confirmed=True,
                   explicit_main_instruction='Boss1/Main已亲读完整来源并独立复核全3056逐字输入，明确授权此冻结输入恰一次完整highs-ds（60秒、presolve=False、原尺度），随后只做精确恢复、全列证书、完整最优面及实际新正付款诊断。先排他写消费标记，任何异常不重跑；不读或纳入新lambda族。')
    for key,name in [('input_sha256','exact_input.json'),('preparation_manifest_sha256','freeze_manifest.json'),
                     ('scaling_sha256','numerical_scaling.json'),('source_review_sha256','source_review.md'),('source_pins_sha256','source_pins.json')]:
        release[key]=h(P/name)
    release['scaffold_manifest_sha256']=h(S/'scaffold_manifest.json')
    release['raw_row_order_sha256']=canonical([r['name'] for r in rows])
    release['expected_dimensions']=deepcopy(release['planned_dimensions_reference_only'])
    release['expected_row_blocks']=deepcopy(release['planned_row_blocks_reference_only'])
    release['literal_parent']['input_sha256']=h(B/'exact_input.json')
    release['literal_parent']['scaling_sha256']=h(B/'numerical_scaling.json')
    release['preparation_manifest_count_pointers']={'raw_inequalities':'/raw_rows','nonnegative_columns':'/columns','equalities':'/equalities'}
    release['source_validity_scope']={k:True for k in release['source_validity_scope']}
    path=str((W/'main_visible_c_v5_preflight.json').relative_to(R))
    release['required_evidence']=[{'role':role,'path':path,'sha256':h(W/'main_visible_c_v5_preflight.json'),
             'expected_status':result['status'],'expected_json_values':{'/raw_rows':3056,'/variables':513,'/equalities':2}}
             for role in ['main_preflight','source_legality','all_raw_column_audit']]
    release['note']='Actual Main release after final source proof, geometric, true-cost and all-column checks. No permission is inferred from a template or file existence.'
    put(S/'main_release.json',release)
    print(json.dumps({'status':result['status'],'input_sha256':result['input_sha256'],
                      'main_release_sha256':h(S/'main_release.json'),'optimizer_calls_authorized':1,
                      'optimizer_calls_by_Main_preflight':0,'complete_column_positions':3056*513},ensure_ascii=False))

if __name__=='__main__':main()
