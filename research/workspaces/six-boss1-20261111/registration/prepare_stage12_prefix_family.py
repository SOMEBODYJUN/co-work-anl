"""Main serial promotion of the audited all-type early SAFE/MAX family."""
from pathlib import Path
from hashlib import sha256
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = WS.parents[2]
PREFIX = 'research/workspaces/six-boss1-20261111/'
OID = 'customer-attraction/shared-maximal-potential-early-safe-prefix-family'
BODY = 'archives/customer-attraction/state/引理/共同最大潜力主题的早期安全预算投影--引理.md'

def bind(path):
    return {'path': path, 'sha256': sha256((REPO / path).read_bytes()).hexdigest()}

def main():
    regraw = (REPO / 'research/registry.json').read_bytes()
    reg = json.loads(regraw)
    byid = {x['object_id']: x for x in reg['objects']}
    assert OID not in byid
    model = byid['CAG-MODEL']
    assert model['body'] == bind(model['body']['path'])
    source = WS / 'main_prefix_safety_maxx_family.md'
    assert sha256(source.read_bytes()).hexdigest() == '4d3f24e686ae38a8593b62abe1807249de6bd3884b428d52198180798ea73b81'
    text = source.read_text()
    assert text.startswith('# Main：同一最大主题的早期SAFE合账，三个更小常数\n\nBoss1；RUN six-boss1-20261111。此处给全类型解析证明，不使用任何固定LP点。')
    text = text.replace('# Main：同一最大主题的早期SAFE合账，三个更小常数\n\nBoss1；RUN six-boss1-20261111。此处给全类型解析证明，不使用任何固定LP点。',
        '# 共同最大潜力主题的早期安全预算投影\n\n采用[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)：有限单位客户、有限非空共同标签目录，以及全部有序历史上定义的纯SPE。恰六人，保留空覆盖、同覆盖异标签、重复行动、零客户及任意历史依赖弱平局。下文直接给全客户类型的解析证明。', 1)
    text = text.replace('本稿先独立证明三个常数都有效', '本引理证明三个常数都有效', 1)
    text = text.replace('新行的普遍性由本稿真实预算证明', '新行的普遍性由上述真实预算证明', 1)
    text += '''
## 6. 来源、独立核查与承重边界

上述证明由Boss1/Main在RUN six-boss1-20261111推导。原工作证明、1440个有序
布尔型记录及其独立审查分别保存在本RUN的main_prefix_safety_maxx_family.md、
同名.py/.json与early3_maxx_cone/audit_main_family.md/.py/.json。
独立程序从实际单客户份额重建，在u=0和u=1分别核2880次付款恒等式，全部
1440型、四角缩减及端点值通过；它不导入Main生成器、不读取LP点、不调用优化器。

形式结论是三个普遍必要不等式。第三位的八权锥最优61/3另有原始/对偶精确
证书；第一、第二位此处只声明有效。没有声称这些常数是真实SPE锐界，也没有
据有限16hist接口声称六人全域half或反例。51行接口、点诊断、最优面排除与
后续联合LP各由其明确证据承担，不从本引理自动得到。
'''
    header = '''---
id: customer-attraction/shared-maximal-potential-early-safe-prefix-family
kind: lemma
type_tag: 引理
title: 共同最大潜力主题的早期安全预算投影
status: proved-all-type-early-prefix-necessary-bounds
truth_status: proved
source_refs:
  - local:archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md
  - local:research/workspaces/six-boss1-20261111/main_prefix_safety_maxx_family.md
  - local:research/workspaces/six-boss1-20261111/early3_maxx_cone/audit_main_family.md
---

'''
    assert not (REPO / BODY).exists()
    (REPO / BODY).write_text(header + text)
    evidence_paths = [model['body']['path']] + [PREFIX + p for p in (
        'main_prefix_safety_maxx_family.md', 'main_prefix_safety_maxx_family.py',
        'main_prefix_safety_maxx_family.json', 'early3_maxx_cone/audit_main_family.md',
        'early3_maxx_cone/audit_main_family.py', 'early3_maxx_cone/audit_main_family.json',
        'early3_maxx_cone/audit_main_family_1440.csv',
        'main_prefix_maxx_interface/rows_51.json', 'main_prefix_maxx_interface/freeze_manifest.json')]
    obj = {
        'object_id': OID, 'version': 1, 'title': '同一最大潜力标签向前三真实源的SAFE/MAX投影',
        'kind': 'lemma', 'truth_status': 'proved', 'model': model['model'],
        'statement': '六人完整有序历史纯SPE，固定长度i−1的合法前缀及其真实续局，i=1,2,3，r=7−i；b为此前负载，P为按同一σ继续到第四位后的负载。固定一个全目录f_P最大标签X。对每个合法Q，C_r u_i−(C_r−1)Σ_X1/(b+r)≥Σ_Q[x/(b+r)+(1−x)/(b+1)]，对应C_6=206/5、C_5=121/4、C_4=61/3。使用源IC、原源分别真改后继标签的SAFE、同一X的最大性和真实末节点查询；四角解析余项全部非负。',
        'quantifiers': '每份原六人完整纯SPE，每个i∈{1,2,3}及合法有序前缀（可离轨），按该前缀真实续局定义u_i和P；任意固定f_P最大标签X、每个合法查询Q。沿同一根实际路径的三个源可以共用X。',
        'assumptions': ['b≤i−1、k=P−b≤5−i，会员逐客户取值但所有预算权对全部客户固定', '每个SAFE由原源真改对应合法后继标签并沿其自己的σ后续支付，不冻结X枝', 'X最大性针对f_P而非最坏分母κ；X不能按客户或查询重新选择'],
        'scope': '全类型普遍必要式，允许全部弱平局、空主题、零客户、重复行动与同覆盖异标签；有限51行仅是一个查询接口。',
        'objections': '第一、第二位此版本只证有效，不证最佳；第三位限定八预算锥的最优不等于真实SPE锐性。该引理不单独证明half、不提供完整策略，也不认证任一有限LP点可共同实现。',
        'body': bind(BODY), 'evidence': [bind(p) for p in evidence_paths],
        'sources': ['canonical:' + model['body']['path']] + ['material:' + p for p in evidence_paths[1:]],
        'keywords': ['共同目录', 'same-X', '真实早期源', 'SAFE', '最大潜力', 'six-providers']
    }
    reg['objects'].append(obj)
    mats = {m['path']: m for m in reg['materials']}
    for e, bodyflag in [(obj['body'], True)] + [(x, False) for x in obj['evidence']]:
        p = e['path']
        if p in mats:
            assert mats[p]['sha256'] == e['sha256']
            if bodyflag:
                mats[p]['disposition'] = 'objects'
                if OID not in mats[p].setdefault('object_ids', []):
                    mats[p]['object_ids'].append(OID)
        else:
            m = dict(e, disposition='objects' if bodyflag else 'attachment', object_ids=[OID],
                reason='Main全类型解析推导，并独立原份额/四角审查；有限接口不升级量词。')
            reg['materials'].append(m)
            mats[p] = m
    candidate = HERE / 'stage12-prefix-registry-candidate.json'
    assert not candidate.exists()
    candidate.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + '\n')
    (HERE / 'stage12-prefix-family.json').write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')
    summary = {'registry_before_sha256': sha256(regraw).hexdigest(), 'new_object': OID,
        'body': obj['body'], 'candidate_sha256': sha256(candidate.read_bytes()).hexdigest(),
        'objects': len(reg['objects']), 'materials': len(reg['materials'])}
    (HERE / 'stage12-prefix-registration-summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
