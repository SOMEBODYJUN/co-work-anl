"""Bind actually used inputs, source conditions and completed finite scope."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys

HERE=Path(__file__).resolve().parent;BASE=HERE.parent;REPO=HERE.parents[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(name,obj):(HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')


def main():
    audit=json.loads((HERE/'independent_audit.json').read_text())
    assert audit['status']=='INDEPENDENT_LITERAL_KERNEL_AND_FIXED_MU_OBSTRUCTION_PASS'
    executions=json.loads((HERE/'execution_manifest.json').read_text())
    assert all(r['exit_code']==0 for r in executions)
    numerical=[
      ('union_augmented_lp/augmented_lp_exact.json','Unique old point; hist masses, all actual source payoffs, K, own R/Z and B4 descriptors. Old full 19662 audit is not repeated.'),
      ('root_marginal_closure/marginal_completion_exact.json','All 1216 mu values, 35 positive states and upstream exact single-root slacks.'),
      ('fifth_reply_common/common_atoms_with_D.json','Complete 100 canonical R/Z/B4/D states and masses; all are preserved exactly by the chosen product law.'),
      ('background_five_bridge/fixed53_b0_profit.json','All 192 fixed53 remainder entries for t=0; inherited exact table.'),
      ('background_five_bridge/fixed53_b1_profit.json','All 192 fixed53 remainder entries for t=1; inherited exact table.'),
      ('cross_root_pricing/joint_completion_exact.json','Read by the reused root_model.load_inputs loader into a seed field, but no seed state, seed mass or incidence restriction enters this task domain.'),
      ('main_19662_audit.json','Hashed by the reused input loader only; no new claim of reproducing its global audit.'),
    ]
    source=[
      ('research/workspaces/six-boss1-20261111/root_marginal_closure.md','Full text read; 299-row scope, omitted 46 cross-root rows, group mass H, min-envelope limitation.'),
      ('research/workspaces/six-boss1-20261111/root_marginal_closure/model.py','Relevant constructor sections read; no constructor imported by this task.'),
      ('research/workspaces/six-boss1-20261111/main_glued_terminal_interfaces.md','Full text read; full named U and fixed old-root obstruction distinguished.'),
      ('research/workspaces/six-boss1-20261111/main_glued_terminal_interfaces.py','Full source read; all 198 original true-node/SAFE/PAIR formulas retained.'),
      ('research/workspaces/six-boss1-20261111/main_verify_glued_failures.py','Full source read for previous literal-kernel audit; not imported or run.'),
      ('research/workspaces/six-boss1-20261111/root_pair_joint_19662/model.py','Full source read; readonly use of 76 interfaces and original root budget loader. seed_columns and its 32-incidence domain are not called.'),
      ('research/workspaces/six-boss1-20261111/root_pair_joint_19662/verify_completion.py','Read true_pair_payoffs, interface_literals, root_literals, identity/permutation checks and relevant input checks; not imported or run.'),
      ('research/workspaces/six-boss1-20261111/root_pair_joint_19662/source_reading.json','Read as a provenance locator; mathematical premises separately opened in their actual bodies.'),
      ('research/workspaces/six-boss1-20261111/cross_root_pricing/contract.py','Full source read and imported readonly through root model; row_names, budgets, compressed_column only. Its old-point load_inputs and seed domain are not used.'),
      ('research/workspaces/six-boss1-20261111/fifth_reply_common.md','Relevant sections 1-4 read: D definition, complete 100 atom scope, synchronous S6, correct stabilizer-average marginals.'),
      ('research/workspaces/six-boss1-20261111/fifth_reply_common/verify.py','Relevant payoff and synchronous index sections read; its 62-row output is preserved by network margins, not rerun here.'),
      ('research/workspaces/six-boss1-20261111/fifth_reply_interface.md','Relevant D source/query, fixed D marginal and B4 scope sections read.'),
      ('research/workspaces/six-boss1-20261111/background_five_bridge.md','Relevant sections 1-4 read for fixed53 residual identity and true background/PAIR source; no 53-row recomputation.'),
      ('archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md','Full body read; labelled common catalog, actual ordered histories, all weak ties, duplicates, empty sets and zero customers retained.'),
      ('archives/customer-attraction/state/引理/末两人重叠比较与任意索引聚合--引理.md','Full body read; each strong PAIR has one true actual last pair, three true ICs, one source tax and same-donor overlap. Never applies to an arbitrary forced R/Z pair.'),
      ('archives/customer-attraction/state/引理/真实前缀全目录单步偏离行--引理.md','Full body read; own true source payoff and actual branch prefix with remaining-player bound; no cross-source revenue substitution.'),
      ('archives/customer-attraction/state/引理/真实中间玩家安全行的联合尾会员投影--引理.md','Full body read; complete ordered tail memberships must remain common before projection, no independent per-row hidden events.'),
    ]
    numeric_records=[dict(path=str((BASE/p).relative_to(REPO)),sha256=sha(BASE/p),bytes=(BASE/p).stat().st_size,use=use) for p,use in numerical]
    source_records=[dict(path=p,sha256=sha(REPO/p),bytes=(REPO/p).stat().st_size,read_scope_and_use=use) for p,use in source]
    dump('source_reading.json',dict(scope='Read-only mathematical/source binding for the fixed new mu common-network obligation.',
        numerical_inputs=numeric_records,mathematical_and_code_sources=source_records,
        source_integrity_errors_found=[],
        no_registration_or_edge_writes=True,
        source_conditions='All strong PAIR sources are genuine last two optimal players; all source incomes and one source tax remain their own. Every overlap refers to the same donor event. Equal words are never equal events.',
        finite_scope='Full positive new-mu Cartesian test, full 458-row exact evaluation, seven fixed-margin upper bounds, two full32 necessary-row certificates. No SPE search, no old-only original-point separation.'))
    dump('finalization_receipt.json',dict(actual_argv=sys.argv,utc=datetime.now(timezone.utc).isoformat(),
        script_sha256=sha(Path(__file__)),mathematical_execution_steps=len(executions),
        actual_optimization_calls=0,independent_status=audit['status'],
        scope_closed=True,all_background_processes_complete=True))
    excluded={'artifact_manifest.json','frozen_receipt.json'}
    paths=sorted(p for p in HERE.rglob('*') if p.is_file() and p.name not in excluded)
    paths.append(BASE/'root_network_joint.md')
    records=[dict(path=str(p.relative_to(BASE)),sha256=sha(p),bytes=p.stat().st_size) for p in paths]
    dump('artifact_manifest.json',dict(status='FINAL_LOCAL_FROZEN',artifacts=records,
        main_result='The pinned 35-positive mu fails two general fixed-marginal upper bounds; the old point is not excluded.',
        all_writes_inside_assigned_scope=True))
    dump('frozen_receipt.json',dict(status='COMPLETE_AND_FROZEN',run='six-boss1-20261111',task='root_network_joint',
        artifact_manifest_sha256=sha(HERE/'artifact_manifest.json'),report_sha256=sha(BASE/'root_network_joint.md'),
        audit_sha256=sha(HERE/'independent_audit.json'),full32_rows_sha256=sha(HERE/'full32_obstruction_rows_exact.json'),
        exact_obstructions=[dict(name=r['name'],upper=r['upper']) for r in audit['negative_fixed_mu_upper_bounds']],
        next_obligation='Reselect mu on all 32 states with both new necessary rows, then evaluate full cross-root and true network/root interfaces. Reordering this fixed mu is impossible.',
        no_original_point_exclusion=True,no_full_SPE_claim=True,git_or_registry_writes=0,running_processes=0))
    print(json.dumps(dict(status='COMPLETE_AND_FROZEN',artifacts=len(records),
        report_sha256=sha(BASE/'root_network_joint.md'),full32_rows_sha256=sha(HERE/'full32_obstruction_rows_exact.json'),
        audit_sha256=sha(HERE/'independent_audit.json')),ensure_ascii=False))


if __name__=='__main__':main()
