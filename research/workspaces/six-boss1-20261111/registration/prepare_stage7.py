"""Add reviewed seventh-system evidence and the six-root bridge.

Only prepares a complete additive registry candidate.  Registration, edge
binding and publication are separate serial Main operations.
"""
from pathlib import Path
from hashlib import sha256
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = WS.parents[2]
REG = REPO / 'research/registry.json'
BASE = 'research/workspaces/six-boss1-20261111/'
CID = 'customer-attraction/six-providers/cross-branch-necessary-system-20261111'
BID = 'customer-attraction/one-prefix-five-profit-exclusive-charge'


def digest(path):
    return sha256((REPO / path).read_bytes()).hexdigest()


def evidence(path):
    return {'path': path, 'sha256': digest(path)}


def main():
    reg = json.loads(REG.read_bytes())
    byid = {o['object_id']: o for o in reg['objects']}
    comp, bg = byid[CID], byid[BID]
    assert comp['version'] == 4 and bg['version'] == 1
    comp_path = REPO / comp['body']['path']
    text = comp_path.read_text()
    text = text.replace('六个固定支持必要LP', '七个固定支持必要LP')
    text = text.replace('## 六个有限系统的精确证书', '## 七个有限系统的精确证书')
    text = text.replace('第六轮再次提高；', '第六、七轮再次提高；')
    previous = '| 再加22具名同源行：19578行、15593列 | 精确原始与127个正对偶行权匹配 | 0.4913710398913766 |'
    assert previous in text
    text = text.replace(previous, previous + '\n| 再加42同行新行和1旧行：19621行、15593列 | 精确原始与105个正对偶行权匹配 | 0.4925763826272197 |')
    audit = json.loads((WS / 'main_19621_audit.json').read_bytes())
    assert audit['matched_exact_optimum'] and audit['nonnegative_primal_and_dual']
    assert (audit['rows'], audit['columns']) == (19621, 15593)
    num, den = audit['W'].split('/')
    text += r'''

## 共同查询与跨查询PAIR回流：第七个精确系统

Main逐一实读Boss2的共同查询投影层级、独立初段与同一末节点尾价格合同，以及实际支付39条新行的承重超边。共同332/616投影保持同一个真实回复位；跨查询PAIR保留两查询的交集项，不能将它写成独立平均位的乘积。此处使用既有一般机制，不重新认领其证明。

五个同行冻结包共42条不同完整向量。Main核源点SHA、全部4849描述符、源点精确余量和本19578点的新余量：27负、15正；42条均与基准不同，全部接入。另将4906个旧冻结向量重新回代，恰一条旧Boss2跨PAIR变负，作为第43条补入。新行后10744辅助列全零；不沿用旧点符号。

新系统为19621×15593，精确最优值为

\[
v_5=\frac{NUMERATOR}{DENOMINATOR}
\approx0.4925763826272197.
\]

比较覆盖O=1，正原列314、正max辅助1550、正min辅助651。原始支持秩307，7个自由有理值和活动方程完整保存。对偶106变量秩106，105个正行权、无自由变量。Main自写标准库核验器另核全部19621条原始余量与15593列对偶余项、非负性及精确取等，最小两者均0；见`main_19621_audit.json`。计算代理还逐描述符核旧矩阵不变、全部43向量、规范max/min、恢复支持及互补性。

43条新行中5条取零、38条严格正。只有零基行19617与19618、即`cross616-5783:0`和`:1`有正对偶权，约0.21563143743936058和0.51574236187495215；其余103个正权来自旧系统。故旧系统加这两条同行新行已支付本精确值；并不证明两条各自不可缺，也不宣称其它新行永久冗余。第19620条旧补行在新点严格正，权为0。

本轮完整来源审计在`peer_cut_transfer/`及`main_revaluation_19578/`，矩阵、原始、对偶、逐新行结果和独立核验在`peer_augmented_lp/`。点SHA为`d70c26065d42fd73dedc94183e4533dd6f8608d5841f7a6018ff180dc77e2f9f`，矩阵SHA为`6ebf5f2f10843c5cee74391d057fe545449fb45a4e72f18d665e2a00258b6ea9`，对偶SHA为`5063c02089ed387f9490a53f6d726ec205f7202ab8495eb86525988173c485b3`。

所有历史完成结论仍只绑定其原输入：上一节19578点的132节点共同完成不能未经重算移给19621点。新点虽继续低于half，仍只是固定16hist必要系统的可行点；不是原模型反例，也不是全域福利下界。下一义务是该新点更深的共同客户身份、跨根真实回复和新价格合同。
'''.replace('NUMERATOR', num).replace('DENOMINATOR', den)
    comp_path.write_text(text.rstrip() + '\n')
    comp['version'] = 5
    comp['title'] = '七个有限必要系统的精确最优与指定旧末位共同完成'
    comp['statement'] += ' 再加42条已审同行行及1条重新变负的旧行，得19621×15593，精确最优v5约0.4925763826272197；105正对偶中仅两条新cross616-5783行承重。全部19621行与15593列由Main另作Fraction核验。'
    comp['scope'] = comp['scope'].replace('最新指定点的132旧末位节点', '19556及19578指定点的132旧末位节点')
    comp['scope'] += ' 最新19621点须独立重算共同完成，既往完成及符号不自动迁移。'
    comp_extra = [BASE + p for p in (
        'peer_augmented_lp.md', 'peer_augmented_lp/exact_matrix.json.gz',
        'peer_augmented_lp/augmented_lp_exact.json', 'peer_augmented_lp/exact_dual_certificate.json',
        'peer_augmented_lp/certificate_verification.json', 'peer_augmented_lp/new_row_results.json',
        'peer_augmented_lp/primal_exact_audit.json', 'peer_augmented_lp/execution_manifest.json',
        'peer_augmented_lp/artifact_manifest.json', 'peer_augmented_lp/verify_certificates.py',
        'main_19621_audit.json', 'peer_cut_transfer.py', 'peer_cut_transfer/audit_19578.json',
        'peer_cut_transfer/all_reviewed_cuts_19578.json',
        'main_revaluation_19578/existing_at_19578.json',
        'main_revaluation_19578/existing_negative_cuts_19578.json')]

    # The root coefficient below is fixed at one.  The 71 other weights are
    # unrestricted nonnegative numbers, not a normalized simplex.
    bg_path = REPO / bg['body']['path']
    root = (WS / 'background_root_bridge.md').read_text()
    sections = root[root.index('## 3. 量词、六槽比较与真实根身份'):]
    bg_text = bg_path.read_text().rstrip() + r'''

# 后续：六个真实根偏离、完整余项与共同预算

以下是同一收费定理在六个真实根分支上的后续接口。Main已实读并核对所有源行、共同账符号、71权边缘见证及其标准库核验器；70客户参数另对照已登记二元共享客户全历史SPE构造核验。完整工作稿为`research/workspaces/six-boss1-20261111/background_root_bridge.md`，本节省略前两段研究过程，保留承重定义、证明、有限证据边界及下一义务。下文局部文件名均以`research/workspaces/six-boss1-20261111/background_root_bridge/`为根。

ROOT-71中的根IC系数固定为1，71个其它参数可任意非负。因此该指定19578点的统一正余量不要求这些71权归一；若另放开根权ρ，整个合同齐次化后余量仅能写成ρL*。这一点与其它按权和为1归一的分离LP应区分。

''' + sections
    bg_path.write_text(bg_text.rstrip() + '\n')
    bg['version'] = 2
    bg['statement'] += ' 后续对任意六比较槽的六个真实根五尾给Rbar=5O/6、Vbar−V0=DW+s及完整共同账；由根IC、背景余项、末价容量及60安全查询导出ROOT-71。19578点有27原子见证使任意非负71权（根系数固定1）余量至少L*>0。显式708u1+120u6必要行及已知70客户完整SPE否定两种Theta免费付款模板。'
    bg['quantifiers'] += ' 六根接口另要求同一完整六人SPE的真实根IC；71权均对所有客户与六根共同，根行权固定为1。'
    bg['scope'] += ' 六根共同账与普遍ROOT-71必要行、19578点的精确全71权边缘非分离证书；后者不是六根全目录共同完成。'
    bg_extra = [BASE + p for p in (
        'background_root_bridge.md', 'background_root_bridge/verify_root_bridge.py',
        'background_root_bridge/root_bridge_audit.json',
        'background_root_bridge/ordered_root_exact_nonseparation.json',
        'background_root_bridge/artifact_manifest.json')]
    bg_extra += ['archives/customer-attraction/state/构造/二元共享客户的完整均衡负驻留族--构造.md']

    mats = {m['path']: m for m in reg['materials']}
    for obj, extra in ((comp, comp_extra), (bg, bg_extra)):
        obj['body'] = evidence(obj['body']['path'])
        seen = {e['path'] for e in obj['evidence']}
        obj['evidence'] += [evidence(p) for p in extra if p not in seen]
        obj['sources'] = list(dict.fromkeys(obj['sources'] + ['material:' + p for p in extra]))
        for item, isbody in [(obj['body'], True)] + [(e, False) for e in obj['evidence']]:
            p = item['path']
            if p in mats:
                if mats[p]['sha256'] != item['sha256']:
                    assert p in (comp['body']['path'], bg['body']['path']), p
                    mats[p]['sha256'] = item['sha256']
            else:
                record = {'path': p, 'sha256': item['sha256'],
                          'disposition': 'objects' if isbody else 'attachment',
                          'object_ids': [obj['object_id']],
                          'reason': 'Boss1 Main实读承重来源、独立核精确证书及量词后回流；范围以正文为准。'}
                reg['materials'].append(record)
                mats[p] = record
    target = HERE / 'stage7-registry-candidate.json'
    target.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + '\n')
    summary = {'base_registry_sha256': sha256(REG.read_bytes()).hexdigest(),
               'candidate_sha256': sha256(target.read_bytes()).hexdigest(),
               'objects': [{k: obj[k] for k in ('object_id', 'version', 'body')} for obj in (comp, bg)],
               'total_objects': len(reg['objects']), 'total_materials': len(reg['materials'])}
    (HERE / 'stage7-registration-summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    for label, obj in (('computation', comp), ('background', bg)):
        (HERE / ('stage7-' + label + '.json')).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == '__main__':
    main()
