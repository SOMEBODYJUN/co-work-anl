"""Three reviewed proof edges; full fixed point claims retain their own evidence."""
from hashlib import sha256
from pathlib import Path
import json
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
M = 'CAG-MODEL'
P = 'customer-attraction/true-last-reply-common-potential-cap-and-overlap-endpoints'
L = 'customer-attraction/shared-maximal-potential-terminal-capacity-projection'
C = 'customer-attraction/six-providers/cross-branch-necessary-system-20261111'


def bind(path, section=None):
    d = {'path': path, 'sha256': sha256((REPO / path).read_bytes()).hexdigest()}
    if section:
        d['section'] = section
    return d


def main():
    reg = json.loads((REPO / 'research/registry.json').read_bytes())
    obj = {o['object_id']: o for o in reg['objects']}
    assert obj[C]['version'] == 9 and obj[L]['version'] == 1
    ep = REPO / 'map/edges/six-boss1-20261111'
    common = dict(status='accepted', premises_mode='all', relation_mode='unconditional',
                  reviewed_by='Boss1/Main six-boss1-20261111')
    e1 = dict(common, edge_id='ca-six-boss1-common-max-potential-pays-terminal-capacity-projection',
        kind='implies', source_ids=[M, P], target_ids=[L],
        conditions='同一完整策略的真实两人尾子博弈，整数非负背景p；全目录裸大小上界K及等长合法配对菜单；五非负参数在一次应用内对全部客户类型共同固定。',
        roles={M:'给全部有序历史真实后继IC、同一实际末位查询合法X及布尔会员语义。',
               P:'给同一个全目录f最大X的倒二封顶和全部配对RC。',
               L:'将五份同X预算保会员相加，以正部盒余量消元，得到MP/MC6。'},
        explanation='一次选择X∈argmax_catalog f，以λ、β合并对B及R菜单的cap，以γ加实际末位报价，以δ加K−|X|，以ε加配对RC。X会员系数恰为k=(λb+β平均r)/[(p+1)(p+2)]+ε/(p+1)−γ/(p+a+1)−δ；逐客户加k+−k1X≥0，精确得MP。取m=6及(12,36,24,1,16)得MC6。目标的cb45数值实例另由其绑定点与有理证书复核。',
        scope='支付目标通用五预算族及MC6解析实例，保空题、别名、重复、零客户和任意弱平局。',
        contribution={'result':'同一X在cap、RC、actual末价及裸容量中保持共同会员后，得到普遍必要投影。',
                      'remaining':'不支付完整SPE充分性、六人half、扩大目录后同负值或新有限LP最优；具体cb45数值由绑定证据承担。'},
        evidence=[bind(obj[M]['body']['path'], '策略、真实续局与全部历史量词'),
                  bind(obj[P]['body']['path'], '共同目录F的全配对上限'),
                  bind(obj[L]['body']['path'], '2. 通用五参数必要式'),
                  bind('research/workspaces/six-boss1-20261111/maxb_universal_audit.md')],
        review_note='Main逐式复推同X真实回复分解、五预算系数和参数零面；独立审核另从原份额核通用量词与3360格。旧max-X/RC归原owner，不重复认领。')
    e2 = dict(common, edge_id='ca-six-boss1-terminal-capacity-projection-separates-cb45',
        kind='specializes', source_ids=[L], target_ids=[C],
        conditions='第九cb45点的原16hist语义及同一全目录K；六人actual前四背景，六组B_i,C_i均为同目录合法标签，允许重复。',
        roles={L:'给全类型有效MC6及五预算合法性。', C:'在原4849语义中实例化为17项K归一行，逐分数得到cb45负值；其它有限结论另由各自证据承担。'},
        explanation='参数取(12,36,24,1,16)，由每hist实际收益及六对菜单均值计算κ正部。Main重建17项行与十行Farkas加五个非负列约束消436列完全一致；K归一值−4426145324455836398818752701603934797071201573118130939132148836781341509474/37610930738552016886760210756472139042422876797320439967207958074168853634165严格为负。',
        scope='仅支付目标MC6与cb45点排除，不替代九个LP最优、根438和RZE177完成的独立证书。',
        contribution={'result':'保持第九点语义及同一全目录K的全部完整SPE补全被排除；旧490PAIR通过不免除此必要式。',
                      'remaining':'旧整个最优面、新22297系统最优、自由E共同实现和原六人全域覆盖尚未闭合。'},
        evidence=[bind(obj[L]['body']['path'], '3. 六人实际末两位的一条紧凑实例'),
                  bind(obj[C]['body']['path'], '同一最大潜力主题的容量投影精确排除第九点'),
                  bind('research/workspaces/six-boss1-20261111/terminal_response_cycles/max_b_exact_certificate.json'),
                  bind('research/workspaces/six-boss1-20261111/main_maxb_cut_audit.json'),
                  bind('research/workspaces/six-boss1-20261111/maxb_universal_audit/check_exact.json')],
        review_note='Main实读原owner及新解析证明，逐分数重建并回代，全部16hist含六个零类型保留。严格区分点排除、最优面排除和扩大目录。')
    paths = []
    for name, edge in [('common-max-potential-to-terminal-capacity-projection.json', e1),
                       ('terminal-capacity-projection-to-cb45.json', e2)]:
        p = ep / name
        assert not p.exists()
        p.write_text(json.dumps(edge, ensure_ascii=False, indent=2) + '\n')
        paths.append(p)
    p = ep / 'portfolio-to-capacity-and-new-targets.json'
    edge = json.loads(p.read_bytes())
    for evidence in edge['evidence']:
        if evidence['path'] == obj[C]['body']['path']:
            evidence['sha256'] = obj[C]['body']['sha256']
    edge['review_note'] = 'Boss1/Main逐字核v9式C承重段与v8完全相同；仍只支付actual第二源、四真后继和13/64容量预算。新共同X/MC6、根438、RZE177及同B4条件诊断各由独立正文证书承担，本边不扩大。'
    for k in ('endpoint_pins', 'evidence_pins', 'review_digest'):
        edge.pop(k, None)
    p.write_text(json.dumps(edge, ensure_ascii=False, indent=2) + '\n')
    paths.append(p)
    for p in paths:
        for operation in ('edge-bind', 'edge-check'):
            argv = ['python', 'work.py', 'research', operation, str(p.relative_to(REPO))]
            if operation == 'edge-bind':
                argv.append('--write')
            done = subprocess.run(argv, cwd=REPO, capture_output=True, text=True)
            base = HERE / ('stage11-' + operation + '-' + p.stem)
            base.with_suffix('.stdout.json').write_text(done.stdout)
            base.with_suffix('.stderr.txt').write_text(done.stderr)
            print(json.dumps({'operation': operation, 'edge': p.name, 'exit_code': done.returncode,
                              'result': done.stdout[:300], 'stderr': done.stderr[:200]}, ensure_ascii=False), flush=True)
            assert done.returncode == 0


if __name__ == '__main__':
    main()
