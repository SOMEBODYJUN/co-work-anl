"""Register the same-X analytic projection and completed finite envelopes.

Main owns this serial registration. No frozen proof or cloud output is rewritten.
"""
from hashlib import sha256
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = WS.parents[2]
PREFIX = 'research/workspaces/six-boss1-20261111/'
CID = 'customer-attraction/six-providers/cross-branch-necessary-system-20261111'
LID = 'customer-attraction/shared-maximal-potential-terminal-capacity-projection'
PID = 'customer-attraction/true-last-reply-common-potential-cap-and-overlap-endpoints'
MODEL = 'archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md'
LPATH = 'archives/customer-attraction/state/引理/共同最大潜力主题的末两位容量投影--引理.md'


def bind(path, section=None):
    value = {'path': path, 'sha256': sha256((REPO / path).read_bytes()).hexdigest()}
    if section:
        value['section'] = section
    return value


def cap_section(text):
    marker = '# 一条不花实际末位收益的显式容量行'
    i = text.index(marker)
    j = text.find('\n# ', i + len(marker))
    return text[i:j if j >= 0 else None]


def main():
    registry_path = REPO / 'research/registry.json'
    registry_bytes = registry_path.read_bytes()
    reg = json.loads(registry_bytes)
    comp = next(o for o in reg['objects'] if o['object_id'] == CID)
    parent = next(o for o in reg['objects'] if o['object_id'] == PID)
    assert comp['version'] == 8
    assert comp['body'] == bind(comp['body']['path'])
    assert comp['body']['sha256'] == '8ab413396a16b8726b262cdb5172b83a8a0b0c6de60a95eeeb05b96218381b98'
    assert parent['body']['sha256'] == bind(parent['body']['path'])['sha256']
    assert not any(o['object_id'] == LID for o in reg['objects'])

    body = REPO / comp['body']['path']
    old = body.read_text()
    text = old.replace(
        'status: 九个固定支持必要LP精确闭合；指定164标签路径被真离轨最优性排除；原题开放',
        'status: 九个必要LP精确闭合；共同最大主题容量投影排除第九点；原题开放', 1)
    marker = '旧点被切除与整个最优面被排除必须区分。'
    assert marker in text
    text = text.replace(marker, marker + '\n\n最新进展：第九点已被共同最大潜力主题的普遍必要式MC6精确排除；其438主行根排序包络和177条RZE单查询仍各有精确完成。新22297×21021完整共同X系统已装配，最优值待解。详见本文末三节。', 1)
    text = text.rstrip() + '\n\n' + (HERE / 'stage11-computation-addition.md').read_text().strip() + '\n'
    assert cap_section(text) == cap_section(old)
    body.write_text(text)
    comp['version'] = 9
    comp['title'] = '九个必要系统的精确最优、共同最大主题分离与联合完成边界'
    comp['statement'] += (' 第九cb45点被同一全目录最大潜力主题的MC6必要式精确排除，K归一余量约−.11768241938025059；不是旧最优面全排除。其完整438主行根排序包络有120正μ的精确完成，全部36776不等式/38等式通过；自由E完整177单查询亦精确可行，但这份新E与同B4的两个条件联合上界分别为−.0023925499522877685、−.001404590751783132。完整共同X的1387行/436列已接为22297×21021通用系统，旧下界零扩展有效，新最优待求。')
    comp['scope'] = comp['scope'].replace('八轮精确系统分别绑定各点', '九轮精确系统分别绑定各点')
    comp['scope'] = comp['scope'].replace('第九点SHA cb45ee6f...为当前数值主线；', '第九点SHA cb45ee6f...现已被普遍MC6排除；')
    comp['scope'] += (' 根438与RZE177分别给明定必要包络整锥非分离，不是全根或全E共同客户律。E/B4负诊断只及这份E及两个已证零面，不是普遍old-only切面。MC6的一般性由父档独立引理承担；完整X系统仍限16hist。')
    comp['quantifiers'] += ' MC6对全部原模型客户类型有效，但本页的数值排除保同一K；完整X22297矩阵仍仅指定16hist域。'
    comp['body'] = bind(comp['body']['path'])

    lemma_files = '''
terminal_response_cycles.md
terminal_response_cycles/max_b_symbolic_lift.json
terminal_response_cycles/max_b_exact_certificate.json
terminal_response_cycles/max_b_audit.py
terminal_response_cycles/max_b_independent_preflight.json
terminal_response_cycles/max_b_independent_certificate_audit.json
terminal_response_cycles/freeze_manifest.json
main_verify_maxb_cut.py
main_maxb_cut_audit.json
full624_augmented_lp/recovery/augmented_lp_exact.json
actual_pair_20910/symbolic_rows.json.gz
actual_pair_20910/proof_audit.md
'''.split()
    optional = ['maxb_universal_audit.md', 'maxb_universal_audit/check_exact.json',
                'maxb_universal_audit/check_exact.py']
    for rel in optional:
        if (WS / rel).is_file():
            lemma_files.append(rel)
    lemma_evidence = [bind(MODEL), bind(parent['body']['path'])] + [bind(PREFIX + p) for p in lemma_files]
    lemma = {
        'object_id': LID, 'version': 1,
        'title': '同一最大潜力主题的末两位五参数容量投影',
        'kind': 'lemma', 'truth_status': 'proved', 'model': parent['model'],
        'statement': '在任意真实两人尾子博弈选择同一个全目录f最大标签X，并给全目录裸容量上界K。对两份等长合法配对菜单和任意五非负参数λ,β,γ,δ,ε，MP式将u−U(B,X)、平均u−U(R_i,X)、真实末位v−U(X,A)、K−|X|及平均RC五份预算保同一X后逐客户取正部消元，给普遍齐次必要式。六人参数(12,36,24,1,16)给MC6，其在已认证cb45必要点上K归一精确为−4426145324455836398818752701603934797071201573118130939132148836781341509474/37610930738552016886760210756472139042422876797320439967207958074168853634165。',
        'quantifiers': '每个合法有序历史（含离轨）的真实两人子SPE，或任意整数非负背景两人独立博弈；每份完整纯SPE，每个全目录裸容量上界K，每两份长度m≥1的合法菜单及每五个非负实参数。参数在一次应用内对所有客户和类型固定。',
        'assumptions': ['X从整个共同目录一次选定，在全部五预算中保持同一标签与会员，最大性可有任意弱平局', 'K界整个共同目录；配对菜单项可以重复、空覆盖或同覆盖异标签', '实际末位报价和倒二强制后的真实回复均沿同一完整策略，不能冻结不同分支后继'],
        'scope': '一般解析五预算投影及六人全类型实例；严格分离指定20910系统和490强PAIR上包络通过的cb45点。只排除保原语义及同一K的补全，不排除旧最优面、全部扩目录或六人原命题。共同最大X及RC归旧owner，正部消元不主张外部新颖性或最佳系数。',
        'objections': '不能逐客户重选全局IC权，不能将正部支持视为合法主题；不能把未知交叠各自可达等同共同实现。第九固定点不是SPE反例，新完整X系统最优仍待解。',
        'body': bind(LPATH), 'evidence': lemma_evidence,
        'sources': ['canonical:' + parent['body']['path']] + ['material:' + e['path'] for e in lemma_evidence],
        'keywords': ['共同目录', '最大潜力主题', '真实末两位', '共同身份', '容量正部投影', 'six-providers']
    }
    reg['objects'].append(lemma)

    extra_files = lemma_files + '''
actual_pair_20910.md
actual_pair_20910/freeze_manifest.json
root_sorting_20910.md
root_sorting_20910/symbolic_matrix_exact.json.gz
root_sorting_20910/symbolic_independent_audit.json
root_sorting_20910/root_completion_exact.json.gz
root_sorting_20910/primal_independent_audit.json
root_sorting_20910/completion_analysis.json
root_sorting_20910/verify_result.py
root_sorting_20910/freeze_manifest.json
rze_query_closure_20910.md
rze_query_closure_20910/symbolic_lift.json.gz
rze_query_closure_20910/preflight_literal_audit.json
rze_query_closure_20910/exact_certificate.json
rze_query_closure_20910/independent_certificate_audit.json
rze_query_closure_20910/conditional_B4_diagnostic.json
rze_query_closure_20910/conditional_B4_independent_audit.json
rze_query_closure_20910/verify_conditional_B4.py
rze_query_closure_20910/final_summary.json
rze_query_closure_20910/freeze_manifest.json
main_E_B4_conditional_bound.md
main_E_B4_conditional_bound.py
main_E_B4_conditional_bound.json
compute_dispatch/root-sorting-download-input-audit.json
compute_dispatch/rze-closure-download-input-audit.json
maxb_augmented_lp/full_lift/report.md
maxb_augmented_lp/full_lift/exact_matrix.json.gz
maxb_augmented_lp/full_lift/structure_and_lower_verification.json
maxb_augmented_lp/full_lift/full_coordinate_farkas_projection.json
maxb_augmented_lp/full_lift/verify_certificates.py
maxb_augmented_lp/full_lift/actions_request.json
'''.split()
    extra = [LPATH] + [PREFIX + p for p in dict.fromkeys(extra_files)]
    seen = {e['path'] for e in comp['evidence']}
    comp['evidence'] += [bind(p) for p in extra if p not in seen]
    comp['sources'] = list(dict.fromkeys(comp['sources'] + ['material:' + p for p in extra]))

    materials = {m['path']: m for m in reg['materials']}
    for obj in (comp, lemma):
        oid = obj['object_id']
        for e, is_body in [(obj['body'], True)] + [(e, False) for e in obj['evidence']]:
            path = e['path']
            if path in materials:
                mat = materials[path]
                if mat['sha256'] != e['sha256']:
                    assert path == comp['body']['path'], path
                    mat['sha256'] = e['sha256']
            else:
                mat = dict(bind(path), disposition='objects' if is_body else 'attachment',
                           object_ids=[oid], reason='Main实读解析五预算及对应精确证书，保源历史、共同身份、矩阵域和点/目录边界。')
                reg['materials'].append(mat)
                materials[path] = mat
            if is_body and oid not in mat.get('object_ids', []):
                mat.setdefault('object_ids', []).append(oid)
                mat['disposition'] = 'objects'
    target = HERE / 'stage11-computation-registry-candidate.json'
    assert not target.exists()
    target.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + '\n')
    summary = {'base_registry_sha256': sha256(registry_bytes).hexdigest(),
               'candidate_sha256': sha256(target.read_bytes()).hexdigest(),
               'objects': [{k: obj[k] for k in ('object_id', 'version', 'body')} for obj in (comp, lemma)],
               'total_objects': len(reg['objects']), 'total_materials': len(reg['materials']),
               'unchanged_capacity_bearing_section': True, 'new_comp_evidence_paths': len(extra)}
    for obj, name in ((comp, 'stage11-computation.json'), (lemma, 'stage11-maxb-lemma.json')):
        (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')
    (HERE / 'stage11-registration-summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == '__main__':
    main()
