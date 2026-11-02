"""Recovery-only byte, stored-evidence and payoff-scalar checks; no BI/LP imports."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json

def identity(path):
    raw=path.read_bytes()
    return {'path':str(path),'size':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--sources',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    ids=['ddf2520de2255a1c4472','59a90ea11a2df684017e','9536369246be24174433']
    inv={d['id']:d for line in (a.repo/'cleanup/inventory.jsonl').read_text().splitlines() if (d:=json.loads(line))['id'] in ids}
    source_checks=[];paths={}
    for sid in ids:
        p=next(a.sources.glob(sid+'-*'));info=identity(p);assert info['sha256']==inv[sid]['sha256'] and info['size']==inv[sid]['size'];source_checks.append({'id':sid,**info,'matches_frozen_inventory':True});paths[sid]=p
    sep=json.loads(paths[ids[0]].read_text())
    base=a.repo/'archives/customer-attraction/tools/evidence'
    summary_path=base/'coupled-b-fixed-points-boss3/replay/single/summary.json';summary=json.loads(summary_path.read_text());menu=summary['ordinary_Y_menu_prices_not_in_saved_matrix'][0]
    point_path=base/'swap-B-visible-and-histogram-projection-two-primary/source-root/research/workspaces/customer-attraction/R-5662d5cb0e5845a980ed10a3b3224cb1/research_2/coupled_B_master_exact.json'
    assert identity(point_path)['sha256']==sep['point_sha256']==summary['source_point_sha256']
    assert sep['u6']==menu['actual_payoffs'][5] and sep['reply_family_average_price']==menu['Y_query_values'][5]
    assert sep['minimum_row_value']==menu['six_actual_price_slacks'][5]
    assert F(sep['minimum_row_value'])==F(sep['u6'])-F(sep['reply_family_average_price'])==-F(sep['violation'])<0
    assert all(F(s)>0 for s in menu['six_actual_price_slacks'][:5]) and F(menu['capacity_slack'])>0
    seed_path=base/'diagonal-seed-materialization-boss3/original/seed18_Rdiag.json';seed=json.loads(seed_path.read_text())
    report_path=base/'diagonal-seed-materialization-boss3/related/seed18_Rdiag_actual_prefix_audit.json';report=json.loads(report_path.read_text())
    k=len(seed['topics']);assert seed['players']==6 and k==18
    weights=[c['multiplicity'] for c in seed['customers']];total=sum(weights);target=[1]*6+[0]*(k-6)
    assert report['old_actual_path']==list(range(6)) and report['old_actual_counts']==target
    def payoff(q,action):
        return sum((F(w,sum(q[j] for j in c['topics'])) for w,c in zip(weights,seed['customers']) if action in c['topics']),F(0))/total
    actual_coverage=F(sum(w for w,c in zip(weights,seed['customers']) if any(target[j] for j in c['topics'])),total)
    assert str(actual_coverage)==report['old_actual_welfare_over_total']
    rows=[]
    for depth,rec in enumerate(report['checks']):
        assert rec['depth']==depth and rec['current_actual_label']==seed['topics'][depth]
        actual=payoff(target,depth);assert str(actual)==rec['actual_player_u_over_total']
        fa=seed['topics'].index(rec['best_security_action_label']);ft=rec['floor_minimizing_terminal_counts'];assert len(ft)==k and sum(ft)==6
        need=[int(j<depth)+int(j==fa) for j in range(k)];assert all(x>=n for x,n in zip(ft,need))
        floor_value=payoff(ft,fa);assert str(floor_value)==rec['SPE_security_floor_over_total']
        assert str(floor_value-actual)==rec['strict_floor_gap_over_total']
        rows.append({'depth':depth,'actual_payoff_matches_direct_unit_sum':True,'reported_floor_terminal_payoff_matches_direct_unit_sum':True,'reported_terminal_extends_prefix_and_security_action':True,'gap_matches_subtraction':True,'global_floor_optimality_or_SPE_membership_rechecked':False})
    witness_path=base/'diagonal-seed-materialization-boss3/replay/normalized-tail-witness.json';witness=json.loads(witness_path.read_text())['witnesses']['Rdiag']
    assert report['checks'][4]['SPE_security_floor_over_total']==witness['credible_floor_over_N']
    assert report['checks'][4]['actual_player_u_over_total']==witness['actual_u5_over_N']
    assert report['checks'][5]['actual_player_u_over_total']==witness['actual_u6_over_N']
    result={'status':'passed','scope':'Recovery byte and stored-exact-evidence comparison plus direct payoffs for six reported terminal witnesses. No original audit invocation, matrix reconstruction, BI, LP or all-continuation certification.','source_checks':source_checks,'price_evidence':{'input':identity(point_path),'existing_successful_summary':identity(summary_path),'all_original_separation_fields_match_existing_exact_values':True,'five_other_prices_and_CAP_strictly_positive_in_existing_summary':True,'current_price_replay_invocations':0},'prefix_evidence':{'seed':identity(seed_path),'historical_report':identity(report_path),'existing_independent_last_two_witness':identity(witness_path),'customer_types_completely_consumed':len(seed['customers']),'unit_total':str(total),'six_record_checks':rows,'retention_flags_not_recomputed':True,'first_four_security_floors_remain_historical_global_claims':True},'original_program_invocations':0,'BI_solver_invocations':0,'LP_solver_invocations':0}
    a.out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':'passed','sources':len(source_checks),'direct_prefix_payoff_records':len(rows),'original_program_invocations':0,'BI_solver_invocations':0},ensure_ascii=False))
if __name__=='__main__':main()
