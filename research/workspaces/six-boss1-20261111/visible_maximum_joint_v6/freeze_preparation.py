#!/usr/bin/env python3
"""Freeze the checked preparation, without creating or consuming an LP release."""
import ast
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = WS.parents[2]


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(name, value):
    (HERE / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    assert not (HERE / 'freeze_manifest.json').exists(), 'Already frozen; stop writing'
    independent = read(HERE / 'independent_check_result.json')
    build = read(HERE / 'build_result.json')
    admission = read(HERE / 'source_admission.json')
    contract = read(HERE / 'preparation_contract.json')
    failure = read(HERE / 'failure_log.json')
    pins = read(HERE / 'source_pins.json')
    assert independent['status'] == 'PASS_INDEPENDENT_COMPLETE_ASSEMBLED_INPUT'
    assert build['status'] == 'PASS_ASSEMBLED_PREPARATION_ONLY'
    assert independent['input_sha256'] == build['input_sha256'] == sha(HERE / 'exact_input.json')
    assert independent['expected_raw_rows'] == build['raw_rows'] == 4177
    assert independent['counts']['new_legal_source_columns'] == 1121 * 513
    assert independent['counts']['all_complete_system_column_positions_checked'] == 4177 * 513
    assert admission['assembly_authorized'] is True and admission['freeze_authorized'] is True
    assert admission['optimizer_authorized'] is False and admission['LP_release'] is False
    assert all(a['admitted'] for a in admission['sources'].values())
    assert all(e['resolved'] for e in failure['events'])
    assert not failure['mathematical_failures']
    for rec in pins['files']:
        assert sha(REPO / rec['path']) == rec['sha256'], rec['path']
    imported = {}
    allowed = {'argparse', 'ast', 'copy', 'hashlib', 'itertools', 'json', 'sys',
               'collections', 'datetime', 'fractions', 'functools', 'pathlib'}
    for filename in ['build_input.py', 'check_independent.py', 'freeze_preparation.py']:
        tree = ast.parse((HERE / filename).read_text(encoding='utf-8'))
        modules = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.extend(x.name for x in node.names)
            elif isinstance(node, ast.ImportFrom):
                modules.append(node.module)
        assert set(modules) <= allowed, (filename, modules)
        imported[filename] = sorted(set(modules))
    raw = read(HERE / 'raw_identity_diagnostics.json')
    write('final_preparation_state.json', {
        'status': 'COMPLETE_FROZEN_PREPARATION_READY_FOR_MAIN_INPUT_REVIEW',
        'actual_agent_id': '/root/visible_joint_v6_prepare', 'run': 'six-boss1-20261111',
        'raw_rows': 4177, 'variables': 513, 'nonnegative_columns': 513, 'equalities': 2,
        'input_sha256': build['input_sha256'],
        'all_requested_source_blocks_included': True, 'source_row_exclusions': [],
        'all_base_objects_literal': True, 'all_source_metadata_preserved': True,
        'old_30_rhs_minus_one_rows_preserved': True,
        'optimizer_calls': 0, 'candidate_or_face_reads': 0,
        'LP_release_created_or_consumed': False, 'SPE_sufficiency_claimed': False,
        'half_status': 'OPEN', 'mathematical_failures': [],
        'resolved_execution_or_read_probe_events': len(failure['events']),
        'future_action_owner': 'Boss1/Main; full frozen-input preflight is a separate action',
        'post_freeze_rule': 'Stop all writes to this directory and the same-name summary.'})
    summary = f'''# 完整可见最大标签联合必要系统 v6：4177×513，冻结准备完成

Boss1；RUN `six-boss1-20261111`；实际 agent ID `/root/visible_joint_v6_prepare`。

**已按Main指定顺序装配全部4177条原尺度必要不等式，独立检查PASS，0优化器。**
保留全部513个非负列、原覆盖目标及两个自由等式；未读候选点或最优面，未创建或消费LP release。
全局O取达到OPT6的最优六标签覆盖并；OPT6>0时按OPT6归一化，零OPT6实例直接处理。新增局部族对任意六查询并成立，在此特化到该最优O。

## 输入组成

| raw闭区间 | 来源 | 行数 | 数值除数 |
|---|---|---:|---|
| 0–3055 | 冻结v5全部原对象literal | 3056 | 旧3056字符串literal |
| 3056–3285 | 第二源λ窗口全部来源 | 230 | 25 |
| 3286–3445 | 第二源λ完整锚域全部来源 | 160 | 25 |
| 3446–3995 | 后部源λ全部闭窗口出现 | 550 | 25 |
| 3996–4175 | 第二源δ六切片全部端点 | 180 | 25 |
| 4176 | Main根严格C外部余项行 | 1 | 1 |

两份第二源λ来源都保留；没有按重复向量、凸生成关系、窗口重合或零型筛选。
δ独立helper的3条ordered ε行和150条仿射段不属于既定180个端点原行，未混入端点块。
父raw868保留，最后根行另加 `−ηc(1−o)`，其K系数不变。

## 数学和schema关键点

已全文实读三份λ证明、δ完整证明和原模型。λ包真实源IC权为 `λ+Στ`；δ包为 `25+τ4+τ5−s`；数值除数25不是该权。
λ的C-only加 `B E_C`，K=1；δ的C-only加 `(S−s/5)E_C`，K=s/5。
每个有符号等式及独立K列都另行检查。

列表源的第k项无损映到 `a[str(k)]`，字典源原键和原字符串保留。
原ID、源内索引、全部非系数metadata及原catalog条目全部保存；新λ/δ全局name采用 `package::原id`，解决两份第二源λ包的原名重合，未改动原id。
Main根行保持整个原对象literal。

## 独立核验

检查器只导入标准库，不导入builder或任何项目模块。它从真实个人份额、所有真实尾态及全部ordered重数重建来源列。

| 检查 | 准确数量 |
|---|---:|
| 原系统literal行 | 3056 |
| 新增合法来源列 | {independent['counts']['new_legal_source_columns']} |
| 整个系统逐行完整列位置 | {independent['counts']['all_complete_system_column_positions_checked']} |
| 新C有符号等式列 | {independent['counts']['new_C_free_equality_columns']} |
| 根行与旧raw868完整差分列 | 513 |
| 独立真实尾成本 | {independent['counts']['independent_true_tail_costs']} |
| 独立条件最小值 | {independent['counts']['independent_conditional_minima']} |
| 全部并列最小尾出现 | {independent['counts']['all_weak_minimum_occurrences']} |
| 旧真实IC/K元数据行 | 2006 |
| 旧ordered客户列重建 | 162816 |
| 两个自由等式列 | 1026 |
| 覆盖目标列 | 513 |

全部30条rhs=−1保留。输出后诊断：恒零原行{len(raw['zero_raw_row_indices'])}条，
不同仿射向量（含零）{raw['distinct_affine_vectors_including_zero']}个，
重复出现{raw['duplicate_occurrences_retained']}次；这些统计不用于删行。
源文件的{len(pins['files'])}个固定SHA在首尾和冻结前均一致。

一次checker接口失败是两份λ的ordered原catalog不含target；已按实际schema修正，并保留失败脚本和记录。
其他只读接口探针或被否决的辅助假设也完整记在failure_log中；未修改来源数学或冻结原包。
冻结前另补明全局最优O与局部任意查询并的语义，并保留更正前已成功的装配/检查记录；原系数对象未变。

## 工件和身份

- [完整原尺度输入](visible_maximum_joint_v6/exact_input.json)
- [行目录](visible_maximum_joint_v6/row_catalog.json)及[逐行来源](visible_maximum_joint_v6/provenance.json)
- [模型合同](visible_maximum_joint_v6/model_contract.json)、[来源核读](visible_maximum_joint_v6/source_review.md)及[全部列路由](visible_maximum_joint_v6/column_routing.json)
- [独立检查](visible_maximum_joint_v6/independent_check_result.json)及[全部raw行检查](visible_maximum_joint_v6/all_raw_row_checks.json)
- [来源pins](visible_maximum_joint_v6/source_pins.json)、[冻结manifest](visible_maximum_joint_v6/freeze_manifest.json)及[SHA256SUMS](visible_maximum_joint_v6/SHA256SUMS)

`exact_input.json` SHA256：

```text
{build['input_sha256']}
```

本包是普遍必要系统的完整输入准备，不是SPE实现证书，没有新优化值，六人half状态仍OPEN。
已冻结并停止写入；交Main对这份准确输入作完整复核。
'''
    adjacent = WS / 'visible_maximum_joint_v6.md'
    adjacent.write_text(summary, encoding='utf-8')
    files = sorted(p for p in HERE.iterdir() if p.is_file() and p.name not in ('freeze_manifest.json', 'SHA256SUMS'))
    manifest = {
        'schema': 'visible_maximum_joint_v6_preparation_freeze_v1',
        'status': 'FROZEN_COMPLETE_INPUT_PREPARATION_NO_OPTIMIZER',
        'frozen': True, 'frozen_preparation_only': True,
        'owner': 'Boss1/Main', 'actual_agent_id': '/root/visible_joint_v6_prepare',
        'run': 'six-boss1-20261111', 'frozen_utc': datetime.now(timezone.utc).isoformat(),
        'raw_rows': 4177, 'columns': 513, 'nonnegative_columns': 513,
        'customer_columns': 512, 'K_column': 512, 'equalities': 2,
        'input_file': 'exact_input.json', 'input_sha256': build['input_sha256'],
        'parent_input_sha256': contract['baseline']['input_sha256'],
        'parent_manifest_sha256': contract['baseline']['manifest_sha256'],
        'source_manifest_pins': {s['package']: s['manifest_sha256'] for s in contract['append_sources']},
        'source_ranges': build['append_ranges'], 'source_row_exclusions': [],
        'base3056_complete_objects_literal': True, 'both_source2_lambda_sources_preserved': True,
        'all_source_occurrences_and_metadata_preserved': True,
        'old_scales_literal': 3056, 'new_lambda_delta_positive_divisor': '25', 'root_positive_divisor': '1',
        'real_source_IC_weight_not_replaced_by_divisor': True,
        'all_raw_scales_original': True, 'all_30_rhs_minus_one_preserved': True,
        'raw_zero_rows_retained': len(raw['zero_raw_row_indices']),
        'raw_duplicate_occurrences_retained': raw['duplicate_occurrences_retained'],
        'diagnostic_distinct_affine_vectors_including_zero': raw['distinct_affine_vectors_including_zero'],
        'independent_checker_status': independent['status'], 'independent_checker_counts': independent['counts'],
        'checker_imported_builder_or_project_module': False, 'script_import_audit': imported,
        'optimizer_calls': 0, 'candidate_or_face_reads': 0, 'LP_release_created_or_consumed': False,
        'optimization_authorized': False, 'K_fixed': False, 'support_restricted': False,
        'new_equality_elimination': False, 'SPE_sufficiency_claimed': False, 'half_status': 'OPEN',
        'failure_events_resolved_and_retained': len(failure['events']), 'mathematical_failures': [],
        'source_files_verified_unchanged': len(pins['files']),
        'artifacts': {p.name: sha(p) for p in files}, 'artifact_bytes': {p.name: p.stat().st_size for p in files},
        'adjacent_summary': {'path': '../visible_maximum_joint_v6.md', 'sha256': sha(adjacent)},
        'checksum_file': 'SHA256SUMS',
        'post_freeze_rule': 'Stop writing this directory and its same-name summary; Main next reviews the full frozen input.'}
    write('freeze_manifest.json', manifest)
    checksum_files = files + [HERE / 'freeze_manifest.json']
    checksum = ''.join(sha(p) + '  ' + p.name + '\n' for p in checksum_files)
    checksum += sha(adjacent) + '  ../visible_maximum_joint_v6.md\n'
    (HERE / 'SHA256SUMS').write_text(checksum, encoding='utf-8')
    print(json.dumps({'status': manifest['status'], 'raw_rows': 4177,
        'input_sha256': build['input_sha256'], 'manifest_sha256': sha(HERE / 'freeze_manifest.json'),
        'SHA256SUMS_sha256': sha(HERE / 'SHA256SUMS'), 'payload_files': len(files),
        'post_freeze': 'STOP_WRITING'}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
