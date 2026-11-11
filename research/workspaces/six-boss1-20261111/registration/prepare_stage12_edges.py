"""Bind only the precise proof obligations each reviewed edge pays."""
from pathlib import Path
from hashlib import sha256
import json
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
PREFIX = 'research/workspaces/six-boss1-20261111/'
C = 'customer-attraction/six-providers/cross-branch-necessary-system-20261111'
H = 'customer-attraction/shared-maximal-potential-three-tail-prefix-bound'
AP = 'B10-AP-v1'
M = 'CAG-MODEL'

def bind(path, section=None):
    d = {'path': path, 'sha256': sha256((REPO / path).read_bytes()).hexdigest()}
    if section:
        d['section'] = section
    return d

def main():
    reg = json.loads((REPO / 'research/registry.json').read_bytes())
    obj = {o['object_id']: o for o in reg['objects']}
    assert obj[C]['version'] == 10 and obj[H]['version'] == 1
    common = dict(status='accepted', premises_mode='all', relation_mode='unconditional',
                  reviewed_by='Boss1/Main six-boss1-20261111')
    edges = [
        ('complete-history-to-common-X-H3.json', dict(common,
            edge_id='ca-six-boss1-complete-history-pays-common-X-H3', kind='implies',
            source_ids=[M], target_ids=[H],
            conditions='六人任意合法三行动有序前缀h，按同一σ取A4；b≤3，P=b+a4。选择一次全目录f_P最大X，对任意合法Q取强制X后的真实Y/Z。',
            roles={M:'给合法共同标签、同一完整σ真实后继及源/末位弱IC；有限目录使f_P最大者存在。', H:'以10源IC、1和2两条最大性、1真末查询加逐型非负余项证明主式。'},
            explanation='令n=b+1∈1..4。target−10IC−MAX(Y)−2MAX(Z)−BR_Z(Q)逐客户为正文E。x=0和x=1分别取q/a最不利角，四组(y,z)的八个闭式下界全非负。七权锥结论另在目标正文按三份真两尾TP的三IC付款与四型精确对偶证明，不靠模型登记状态。',
            scope='支付通用H3-X主式；正文对限定七预算锥的精确最优有另列完整证明。',
            contribution={'result':'同一个末两位f_P最大X可向前接真实第四位，常数10。',
                          'remaining':'不支付六人half、真实SPE锐性、更大背景或全部LP最优。'},
            evidence=[bind(obj[M]['body']['path']), bind(obj[H]['body']['path'], '2. 常数10的全类型必要式'),
                      bind(PREFIX+'maxb_h3_audit.md'), bind(PREFIX+'maxb_h3_pair_strength.md')],
            review_note='Main重新推导四预算与八个闭式余项，完整实读独立原份额/字面接口核验。X权重不换成1/(b+3)，所有平局与空/零情形保留。')),
        ('H3-to-finite-shared-X-queries.json', dict(common,
            edge_id='ca-six-boss1-H3-specializes-finite-shared-X-queries', kind='specializes',
            source_ids=[H], target_ids=[C],
            conditions='绑定16hist/21021列，158合法标签表达式的17个旧S6轨道；同X不随索引置换，未知XQ只作正系数上包络必要放松。',
            roles={H:'支付所有合法Q的同X H3必要式。', C:'按已核字面频数平均为17行并在新点精确评价；其它计算由自己的证书承担。'},
            explanation='固定菜单平均得到17条同源行。未知交叠系数2/((b+1)(b+3))>0，可用旧上包络放松；420值若升级真实core则行仍合法但不能再规范min。Main在5b1b点17行全正，最小A6余量约.02697761658。',
            scope='仅支付H3的17行实例和其绑定评价，不替代完整LP、AP39整面或own相容证明。',
            contribution={'result':'已审17行/1731非零/零新列及新点全部严格正的有限诊断。',
                          'remaining':'不声称17行独立、全局冗余或该族能分离第十点。'},
            evidence=[bind(obj[H]['body']['path']), bind(obj[C]['body']['path'], '同一个X向真实较早源的接回与新点缺口'),
                      bind(PREFIX+'maxb_h3_bridge/rows_17.json'), bind(PREFIX+'maxb_h3_audit/audit_result.json'),
                      bind(PREFIX+'main_h3_on_5b1b.json')],
            review_note='Main实读全来源并亲自逐分数代入新精确点；未把S6平均当可行动标签。')),
        ('arbitrary-anchor-AP-to-shared-X-early-queries.json', dict(common,
            edge_id='ca-six-boss1-arbitrary-anchor-AP-pays-shared-X-early-queries', kind='specializes',
            source_ids=[AP], target_ids=[C],
            conditions='actual玩家i=1,2,3的真实前缀，r=7−i，b≤i−1；同一个X是共同目录合法标签。AP1只需合法性，M=r+max b≤6。',
            roles={AP:'对每个真实源、每个合法锚和查询给任意锚AP1；SAFE缺额非负允许M统一放宽到6。', C:'代入43、65/2、23并在原坐标生成51行、AP39；点值及面证明分别由绑定证书核验。'},
            explanation='先固定X再将AP1的任意合法锚量词应用到三个actual源。每次当前人改后继标签都沿该标签在本源自己的真实续局，不冻结X分支。C_i=5(r−1)+r²/2；对合法Q作17轨道平均。AP39取第三位和A6，25系数不含未知y。',
            scope='支付旧AP实例及51行普遍必要性，不以此单条边替代W10最优/面零传播恒等式或新的较小最大锚常数。',
            contribution={'result':'同一X必须同时满足早期43、65/2、23查询，AP39的违反确实是原模型必要性缺口。',
                          'remaining':'整个W10最优面排除由目标正文的原dual、全局等式、3384步符号传播及21021列恒等式另行支付；不证明新最优值。'},
            evidence=[bind(obj[AP]['body']['path'], '量词、背景与两个版本'),
                      bind(obj[C]['body']['path'], '同一个X向真实较早源的接回与新点缺口'),
                      bind(PREFIX+'early_x_anchor_queries.md'), bind(PREFIX+'early_x_anchor_queries/ap_source_audit.md'),
                      bind(PREFIX+'main_ap3_cut_audit.json')],
            review_note='实际登记ID为B10-AP-v1，不使用正文frontmatter别名当对象ID。Main实读原量词及完整PAY链，核统一M、空锚和三真实前缀。')),
    ]
    ep = REPO / 'map/edges/six-boss1-20261111'
    paths = []
    for name, edge in edges:
        p = ep / name
        assert not p.exists()
        p.write_text(json.dumps(edge, ensure_ascii=False, indent=2)+'\n')
        paths.append(p)
    for name in ('terminal-capacity-projection-to-cb45.json', 'portfolio-to-capacity-and-new-targets.json'):
        p = ep / name
        edge = json.loads(p.read_bytes())
        for e in edge['evidence']:
            if e['path'] == obj[C]['body']['path']:
                e['sha256'] = obj[C]['body']['sha256']
        if name.startswith('terminal-capacity'):
            edge['contribution']['remaining'] = '本边只支付MC6及cb45实例；整个W9面、W10最优和AP39整面排除由目标正文各自独立证书承担，原六人全域仍OPEN。'
            edge['review_note'] += ' v10只更新目标绑定及已解后续状态，本边承重MP/MC6与cb45参数未变。'
        else:
            edge['review_note'] = 'Main逐字核v10式C承重段与v9完全相同；仍只支付actual第二源、四真后继和13/64容量。第十系统、H3/AP、面传播和own六面均由各自来源承担。'
        for k in ('endpoint_pins', 'evidence_pins', 'review_digest'):
            edge.pop(k, None)
        p.write_text(json.dumps(edge, ensure_ascii=False, indent=2)+'\n')
        paths.append(p)
    for p in paths:
        for operation in ('edge-bind', 'edge-check'):
            argv=['python','work.py','research',operation,str(p.relative_to(REPO))]
            if operation=='edge-bind':
                argv.append('--write')
            run=subprocess.run(argv,cwd=REPO,capture_output=True,text=True)
            prefix=HERE/('stage12-'+operation+'-'+p.stem)
            prefix.with_suffix('.stdout.json').write_text(run.stdout)
            prefix.with_suffix('.stderr.txt').write_text(run.stderr)
            print(json.dumps({'operation':operation,'edge':p.name,'exit_code':run.returncode,'result':run.stdout[:220],'stderr':run.stderr[:200]},ensure_ascii=False),flush=True)
            assert run.returncode==0

if __name__=='__main__':
    main()
