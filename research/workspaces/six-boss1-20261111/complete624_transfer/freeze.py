"""Freeze the completed local transfer; no Git, registry, RUN or token write."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,sys,time,platform

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
WS=HERE.parent
PEER=REPO/'research/workspaces/six-boss2-20261111-cross'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_bytes())
sources=[
    WS/'union_augmented_lp/augmented_lp_exact.json',
    WS/'union_augmented_lp/exact_matrix.json.gz',
    WS/'main_reverse624.py',
    WS/'main_reverse624_audit.json',
    PEER/'joint_requery/complete624_actual4_R00_v1_contract.md',
    PEER/'joint_requery/complete624_actual4_R00_v1_matrix.json.gz',
    PEER/'joint_requery/complete624_actual4_R00_v1_mapping.json',
    PEER/'joint_requery/build_complete624_actual4_R00_v1.py',
    PEER/'joint_requery/reverse_terminal_624_v1.py',
    PEER/'joint_requery/projection_hierarchy_v2_append_proposal.md',
    PEER/'master_cuts/formal_complete624_12666_gap_v1.md',
    PEER/'master_cuts/complete624_actual4_R00_opt_v2_dual.json',
    PEER/'main_verify_complete624_v1.py',
    PEER/'main_verify_complete624_v1.json',
    PEER/'main_pair_features.py',
    PEER/'main_cross_query_features_v1.py',
    PEER/'main_reverse_terminal_features_v1.py',
    PEER/'joint_requery/selected_cuts_5716.json',
    PEER/'joint_requery/portfolio_selected_5744.json',
    PEER/'joint_requery/portfolio_selected_5752.json',
    PEER/'joint_requery/cross_pairs_selected_5775_v1.json',
    PEER/'joint_requery/reverse_terminal_5799_one_v1.json',
    REPO/'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md',
    REPO/'archives/customer-attraction/state/引理/同源双末对跨枝配对与严格联合投影--引理.md',
    REPO/'archives/customer-attraction/state/引理/共同真实回复与跨查询配对的严格投影层级--引理.md',
    REPO/'map/edges/customer-attraction-boss2-six-cross-20261111/boss2-six-cross-complete624-projection-pays-lift.json',
    REPO/'map/edges/customer-attraction-boss2-six-cross-20261111/boss2-six-cross-shared-pair-to-query-hierarchy.json',
    REPO/'research/GITHUB_RESOURCES.md',
]
assert REPO.name=='co-work-anl-boss1'
receipts={'audit':'transfer.py','solve':'transfer.py','known':'certify.py','separate':'certify.py','compact_wallet':'compact_wallet.py','literal_verify':'verify_literal_row.py','rounded_literal_verify':'verify_rounded_literal_row.py','build_bundle':'build_bundle.py'}
for stage,program in receipts.items():
    receipt=read(HERE/('execution_'+stage+'.json'))
    assert receipt['status']=='SUCCESS' and receipt['script_sha256']==sha(HERE/program),(stage,program)
for fn in ('contract_audit.json','literal_row_verification.json','rounded_literal_row_verification.json','full_lift_bundle_verification.json'):
    assert read(HERE/fn)['status']=='PASS'
pack=read(HERE/'row_transfer_pack.json')
assert pack['selected_negative_rows']==2 and pack['selected_positive_rows']==1
assert read(HERE/'phase1_result.json')['optimizer_calls']==1
inp={'inputs':[{'path':str(p.relative_to(REPO)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sources],
     'navigation_registry_pin':read(HERE/'research_context.stdout.json')['registry_pin'],
     'core_object_ids':['M-e394b173b9b1419588c6c380da4bd326','M-b1b4276f0ec747ed8c347bda65c9e0af','M-ddceaa3d53064498b3e833a32e1f3b6f'],
     'original_point_sha256':pack['point_sha256'],'original_matrix_sha256':pack['matrix_sha256']}
p=HERE/'inputs_manifest.json';assert not p.exists();p.write_text(json.dumps(inp,ensure_ascii=False,indent=2)+'\n')
files=sorted(p for p in HERE.rglob('*') if p.is_file() and p.name!='freeze_manifest.json')+[WS/'complete624_transfer.md']
manifest={'status':'FROZEN_RELEASED','frozen_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'argv':[sys.executable,*sys.argv],'cwd':str(Path.cwd()),'python':platform.python_version(),'scope':'Only actual4/R/family0-off on original16 hist; exact current-point exclusion, not all24 or SPE closure. Generic20910x20585 augmentation ready but not solved.',
          'outcome':{'full624_at_frozen19662_point':'EXACT_INFEASIBLE_BY_TWO_PROJECTED_FARKAS_ROWS','all4849_contract_match':True,'all624_full_hidden_feature_audit':'PASS','independent_literal30x4x16_per_hist_both_rows':'PASS','distinct_new_negative_rows':2,'additional_valid_positive_row_retained':1,'old_reverse624_row_slack':'0','generic_full_lift_bundle_sha256':sha(HERE/'full_lift_bundle.json.gz'),'projected_row_packet_sha256':sha(HERE/'row_transfer_pack.json'),'welfare_increase_claim':False,'new_master_lp_executed':False,'optimizer_calls':1,'general_six_half':'OPEN'},
          'failed_discovery_attempts':read(HERE/'separating_row_exact.json')['discovery']['attempts'][:-1],
          'assets':[{'path':str(p.relative_to(REPO)),'sha256':sha(p),'bytes':p.stat().st_size} for p in files]}
p=HERE/'freeze_manifest.json';assert not p.exists();p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':'FROZEN_RELEASED','manifest_sha256':sha(p),'assets':len(files),'generic_bundle_sha256':sha(HERE/'full_lift_bundle.json.gz'),'row_packet_sha256':sha(HERE/'row_transfer_pack.json')},ensure_ascii=False))
