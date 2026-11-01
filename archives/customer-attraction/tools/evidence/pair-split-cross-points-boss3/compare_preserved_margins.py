"""Compare the newly evaluated prices with already saved old-point audits,
and keep historical report/code versions distinct. No matrix is rebuilt.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import json,hashlib,sys
HERE=Path(__file__).resolve().parent
def main():
    if len(sys.argv)!=2:raise SystemExit('usage: compare_preserved_margins.py /absolute/repository')
    repo=Path(sys.argv[1]);ev=repo/'archives/customer-attraction/tools/evidence'
    old14_path=ev/'cross-source-graph-program/added-row-slacks.json'
    oldfloor_path=ev/'all-reply-actual-floors-program/floor-row-audit.json'
    histreport_path=ev/'r5662-replay-reports-and-identity-boss3/original/terminal_closure_replay.json'
    old14=json.loads(old14_path.read_text());oldfloors=json.loads(oldfloor_path.read_text());history=json.loads(histreport_path.read_text())
    result={}
    for mode,key in (('split','split_point'),('cross','cross_point')):
        new=json.loads((HERE/'replay'/mode/'semantic-and-full-matrix-report.json').read_text())
        prior={r['name']:F(r['slack']) for r in old14[key]}
        comparisons=[]
        for r in new['old_BC_price_rows']:
            name='actual-floor:'+str((r['actual_position']-1,1 if r['family']=='B' else 2))
            assert F(r['slack'])==prior[name]
            comparisons.append({'name':name,'new_slack':r['slack'],'old_saved_slack':str(prior[name])})
        for r in new['old_BC_capacity_rows']:
            name='old-capacity:'+str(1 if r['family']=='B' else 2)
            assert F(r['slack'])==prior[name]
            comparisons.append({'name':name,'new_slack':r['slack'],'old_saved_slack':str(prior[name])})
        # Count the implicit overlap coordinates from raw metadata only.
        raw=json.loads((HERE/'original'/('pair_closure_exact.json' if mode=='split' else 'pair_cross_exact.json')).read_text())
        counts=Counter((v['hist_column'],v['left'],v['right']) for v in raw['variables'])
        expected=sum(n*(n-1)//2 for n in counts.values())
        assert expected==raw['overlap_variables']==new['ZZ_overlap_variables']
        result[mode]={'fixed_source_sha256':new['fixed_source_sha256'],'all_14_old_BC_prices_capacities_equal_prior_independent_audit':True,
            'old_14_values':comparisons,'R_slab_count_from_raw_records':len(counts),'expected_all_slab_pair_overlaps':expected,
            'old_1905_coordinate_changes':new['changed_1905_coordinates_by_kind'],
            'K_attained_after_uniform_index_averaging':new['K_attained_by_symbolic_catalogue_after_index_averaging']}
    cross=json.loads((HERE/'replay/cross/semantic-and-full-matrix-report.json').read_text())
    original=next(x for x in oldfloors['points'] if x['sha256']==cross['fixed_source_sha256'])
    prior_floor={tuple(v['key']):F(v['value']) for v in original['slacks']}
    new_R=[r for r in cross['new_RZ_actual_floor_rows'] if r['member']=='R'];assert len(new_R)==18
    assert all(F(r['slack'])==prior_floor[tuple(r['key'])] for r in new_R)
    new_Z_changes=[{'key':r['key'],'old_slack':str(prior_floor[tuple(r['key'])]),'new_slack':r['slack']} for r in cross['new_RZ_actual_floor_rows'] if r['member']=='Z' and F(r['slack'])!=prior_floor[tuple(r['key'])]]
    split=json.loads((HERE/'replay/split/semantic-and-full-matrix-report.json').read_text())
    assert history['point_sha256']==split['point_sha256']
    assert F(history['W'])==F(split['W']) and history['rows']==split['point_header']['rows']==7931
    assert history['source_sha256']!=split['program_sha256']
    report={'status':'new point prices compared to previously saved exact audits; historical code mismatch retained',
        'old_prices_file':str(old14_path.relative_to(repo)),'old_prices_sha256':hashlib.sha256(old14_path.read_bytes()).hexdigest(),
        'old_floor_file':str(oldfloor_path.relative_to(repo)),'old_floor_sha256':hashlib.sha256(oldfloor_path.read_bytes()).hexdigest(),
        'point_comparisons':result,'cross_all_18_R_floor_values_preserved':True,'cross_new_Z_floor_changes':new_Z_changes,
        'cross_old_Z_negative_count':sum(v<0 for k,v in prior_floor.items() if k[1]==1),'cross_new_Z_negative_count':len(cross['negative_Z_floors']),
        'historical_7931_report':{'file':str(histreport_path.relative_to(repo)),'sha256':hashlib.sha256(histreport_path.read_bytes()).hexdigest(),
          'point_sha256_matches':True,'rows_W_minimum_match':history['minimum_slack']==split['all_rows_minimum']=='0',
          'historical_code_sha256':history['source_sha256'],'current_code_sha256':split['program_sha256'],
          'same_historical_execution_claimed':False,'historical_code_version_gap_resolved':False},
        'limits':'Only comparisons of existing/new data and audits, with no new build, original CLI, optimizer, or historical code recovery.'}
    (HERE/'replay/preserved-margins-and-history.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('point_comparisons','cross_new_Z_floor_changes')},ensure_ascii=False))
if __name__=='__main__':main()
