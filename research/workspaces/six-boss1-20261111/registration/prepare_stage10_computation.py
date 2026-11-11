"""Promote the reviewed ninth exact LP and separately pinned old-point layers."""
from pathlib import Path
from hashlib import sha256
import json

HERE=Path(__file__).resolve().parent
WS=HERE.parent
REPO=WS.parents[2]
PREFIX='research/workspaces/six-boss1-20261111/'
CID='customer-attraction/six-providers/cross-branch-necessary-system-20261111'


def bind(path):
    return dict(path=path,sha256=sha256((REPO/path).read_bytes()).hexdigest())


def main():
    rp=REPO/'research/registry.json'
    reg=json.loads(rp.read_bytes())
    obj=next(o for o in reg['objects'] if o['object_id']==CID)
    assert obj['version']==7 and bind(obj['body']['path'])==obj['body']
    assert obj['body']['sha256']=='e7f6a2079b5f026c17cb4b09cbaa745334614b10f60b44d7dad638ab4ade090f'
    body=REPO/obj['body']['path'];old=body.read_text();text=old
    text=text.replace('status: 八个固定支持必要LP有精确原始对偶证书；132个旧末位节点共同层可行；原题开放',
                      'status: 九个固定支持必要LP精确闭合；指定164标签路径被真离轨最优性排除；原题开放',1)
    oldrow='| 补齐40同行缺行及1反向624：19662行、15593列 | 精确原始与309个正对偶行权匹配 | 0.49304863743650357 |'
    assert oldrow in text
    text=text.replace(oldrow,oldrow+'\n| 完整624共同隐藏提升：20910行、20585列 | 精确原始与531个正对偶行权匹配 | 0.49304863960834766 |',1)
    text=text.replace('第六、七、八轮再次提高；所有值均小于', '第六、七、八、九轮再次提高；所有值均小于',1)
    text=text.replace('## 八个有限系统的精确证书','## 前八个有限系统的精确证书（第九个见后文）',1)
    text=text.replace('这与上述R/Z+B4测度仍是不同的已给构造；本节尚未在两者间施加新的跨块查询，亦未建立完整SPE。',
        '这一步与上述R/Z+B4测度分开构造；后续跨块查询及根边缘障碍见下文第八点跨块节，仍未建立完整SPE。',1)
    text=text.replace('完整增广正作为新独立义务求解，本节不预报其结果。',
        '这一阶段的装配义务后来已完成；第九个精确系统的匹配原始/对偶结论见下文。',1)
    text=text.replace('此时尚未执行完该提升，不把规划写成新切面。原六人完整SPE半覆盖题仍OPEN。',
        '该阶段之后已完成1180行提升及100原子共同层，见下文；这仍不是新切面或完整SPE。原六人完整SPE半覆盖题仍OPEN。',1)
    text=text.rstrip()+'\n'+(HERE/'stage10-computation-addition.md').read_text().strip()+'\n'
    marker='# 一条不花实际末位收益的显式容量行'
    def cap(s):
        i=s.index(marker);j=s.find('\n# ',i+len(marker));return s[i:j if j>=0 else None]
    assert cap(text)==cap(old)
    body.write_text(text)
    obj['version']=8
    obj['title']='九个有限必要系统的精确最优、共同层边界与真实末两位排除'
    obj['statement']=obj['statement'].replace('福利是否上升待解','其第九精确最优值已严格上升')
    obj['statement']+=' 第九完整20910×20585系统精确最优0.49304863960834766，531正对偶匹配，严格提高约2.1718440919348508e-9。旧第八点的100原子D/R/Z/B4层共同完成，却在其164标签目录的全部末两位SPE中无法支持actual路径；Z1非对角强制第五改进约.04226956。旧17根边缘被8个上界排除，完整32态单根边缘299行可修复这些上界但缺46跨根预算。冻结五权及追加四互查仍容许空新末题，Main给统一正下界并明确遗漏的末位对T平均查询。'
    obj['scope']=obj['scope'].replace('最新19621点须独立重算共同完成，既往完成及符号不自动迁移。','各阶段新点均须独立重算共同完成，既往完成及符号不自动迁移。')
    obj['scope']=obj['scope'].replace('两共同块尚未施加新的跨块查询','现已加入跨块查询并明确固定根边缘障碍')
    obj['scope']+=' 第九点SHA cb45ee6f...为当前数值主线；D/根/164标签/冻结五权结果仍分别绑定旧b0ca点，不跨点移用。末两位充要判据为一般子博弈事实；164目录排除只及该实例，增加标签或改变客户律均未排除。'
    extras='''
full624_augmented_lp/recovery_report.md
full624_augmented_lp/exact_matrix.json.gz
full624_augmented_lp/inputs_manifest.json
full624_augmented_lp/verify_certificates.py
full624_augmented_lp/actions_discovery/discovery_execution.json
full624_augmented_lp/actions_discovery/numerical_result.json
full624_augmented_lp/actions_discovery/floating_solver_arrays.npz
full624_augmented_lp/recovery/augmented_lp_exact.json
full624_augmented_lp/recovery/exact_dual_certificate.json
full624_augmented_lp/recovery/certificate_verification.json
full624_augmented_lp/recovery/optimality_analysis.json
full624_augmented_lp/recovery/freeze_manifest.json
main_20910_audit.json
compute_dispatch/full624-download-input-audit.json
main_glued_terminal_interfaces.md
main_glued_terminal_interfaces.py
main_glued_terminal_interfaces.json
main_verify_glued_failures.py
main_glued_terminal_failures_audit.json
main_glued_single_query_upper.py
main_glued_single_query_upper.json
root_marginal_closure.md
root_marginal_closure/model.py
root_marginal_closure/symbolic_coefficients_exact.json
root_marginal_closure/marginal_completion_exact.json
root_marginal_closure/verify_completion.py
root_marginal_closure/independent_audit.json
root_marginal_closure/artifact_manifest.json
fifth_reply_interface.md
fifth_reply_interface/symbolic_lift.json
fifth_reply_interface/exact_lift.json
fifth_reply_interface/D_marginals.json
fifth_reply_interface/verify.py
fifth_reply_interface/independent_verification.json
fifth_reply_common.md
fifth_reply_common/common_atoms_with_D.json
fifth_reply_common/exact_extension.json
fifth_reply_common/verify.py
fifth_reply_common/independent_verification.json
fifth_reply_common/verify_boolean.py
fifth_reply_common/boolean_verification.json
fifth_reply_common/old_network_verification.json
fifth_reply_common/final_manifest.json
main_exact_two_tail_contract.md
finite_two_tail_164.md
finite_two_tail_164/proof_audit.md
finite_two_tail_164/matrix_certificate.json
finite_two_tail_164/labels_and_orbits.json
finite_two_tail_164/integer_orbit_counts.json
finite_two_tail_164/exclusion_certificate.json
finite_two_tail_164/tail_solution.json
finite_two_tail_164/verify.py
finite_two_tail_164/independent_verification.json
finite_two_tail_164/final_manifest.json
main_z_successor_contract.md
rz_fresh_terminal5.md
rz_fresh_terminal5/solve_exact.py
rz_fresh_terminal5/local_tables_exact.json
rz_fresh_terminal5/knapsack_exact.json
rz_fresh_terminal5/completion_exact.json
rz_fresh_terminal5/verify_literal.py
rz_fresh_terminal5/independent_verification.json
rz_fresh_terminal5/final_manifest.json
main_rz_zero_terminal_witness.md
main_rz_zero_terminal_witness.py
main_rz_zero_terminal_witness.json
background_joint_terminal21.md
background_joint_terminal21/contract.md
background_joint_terminal21/inputs.json
background_joint_terminal21/single_case_result.json
background_joint_terminal21/verify_one.py
background_joint_terminal21/independent_verification.json
background_joint_terminal21/manifest.json
'''.split()
    extra=[PREFIX+p for p in extras]
    # Resolve the independently named report from the frozen directory if its
    # filename differs; never manufacture or overwrite a report.
    candidate=PREFIX+'background_joint_terminal21/independent_verification.json'
    if not (REPO/candidate).exists():
        report=WS/'background_joint_terminal21/independent_audit.json'
        assert report.exists()
        extra[extra.index(candidate)]=str(report.relative_to(REPO))
    obj['body']=bind(obj['body']['path'])
    seen={e['path'] for e in obj['evidence']}
    obj['evidence'] += [bind(p) for p in extra if p not in seen]
    obj['sources']=list(dict.fromkeys(obj['sources']+['material:'+p for p in extra]))
    mats={m['path']:m for m in reg['materials']}
    for e,isbody in [(obj['body'],True)]+[(e,False) for e in obj['evidence']]:
        p=e['path']
        if p in mats:
            if mats[p]['sha256']!=e['sha256']:
                assert p==obj['body']['path'],p
                mats[p]['sha256']=e['sha256']
        else:
            m=dict(e,disposition='objects' if isbody else 'attachment',object_ids=[CID],
                reason='Main实读并按真实历史、完整钱包及点/目录范围复核；精确全行列与原始份额支持所列有限结论。')
            reg['materials'].append(m);mats[p]=m
    target=HERE/'stage10-computation-registry-candidate.json'
    target.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
    summary=dict(base_registry_sha256=sha256(rp.read_bytes()).hexdigest(),candidate_sha256=sha256(target.read_bytes()).hexdigest(),
        object={k:obj[k] for k in ('object_id','version','body')},total_objects=len(reg['objects']),total_materials=len(reg['materials']),
        unchanged_capacity_bearing_section=True,new_evidence_count=len(extra))
    (HERE/'stage10-computation-registration-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    (HERE/'stage10-computation.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False))


if __name__=='__main__':main()
