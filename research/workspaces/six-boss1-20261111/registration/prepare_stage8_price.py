"""Promote the proved two-source lift and exact ninety-case boundary.

This prepares one additive registry update. It neither registers nor publishes.
"""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = WS.parents[2]
BASE = 'research/workspaces/six-boss1-20261111/'
ID = 'customer-attraction/previous-theme-uniform-positive-price'


def sha(p):
    return hashlib.sha256((REPO / p).read_bytes()).hexdigest()


def binding(p):
    return {'path': p, 'sha256': sha(p)}


def main():
    regpath = REPO / 'research/registry.json'
    reg = json.loads(regpath.read_bytes())
    obj = next(x for x in reg['objects'] if x['object_id'] == ID)
    assert obj['version'] == 1
    body = REPO / obj['body']['path']
    text = body.read_text()
    assert sha(obj['body']['path']) == obj['body']['sha256']
    text = text.replace('status: 任意尾长正价合同已证；后续跨源付款未完成',
                        'status: 任意尾长正价与两源十九权提升已证；原六人目标仍开')
    old = '把本正价用于较早源的未知真实后继，保初态 T/Q 的可见会员与后继会员的同一耦合；分列两个源的收入与同一常数收费。首先检查它能否在已合入同行共同查询/共享末端切面的新点上产生新行。未完成这一步前，不宣称新价格已改进六人覆盖界。'
    assert old in text
    text = text.replace(old, '这一跨源付款现已完成为下文的十九权合同和精确线性提升。当前单个嵌套配置及90个直接报价配置均有指定点上的全归一参数锥非分离证书；尚未由它改进原六人覆盖界。下一步须加入不同的真实共同信息，而不能将返回权非负当作整个参数族的证明。')
    nested = (WS / 'nested_price_contract.md').read_text()
    proof = nested[nested.index('## 1. 固定数据与十九个全局参数'):nested.index('## 5. 与最近既有对象的准确关系')]
    proof = proof.replace('[共同标签目录与完整历史纯SPE定义](../../../archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md)', '共同标签目录与完整历史纯SPE定义')
    proof = proof.replace('[上一主题统一正价](main_previous_theme_price.md)', '本页前半部的上一主题统一正价')
    proof = proof.replace('[固定内价跨源合同](previous_price_search/next_cross_source_contract.md)', '工作区中的固定内价跨源合同')
    text += '\n\n# 后续：两个实际来源的十九权共同提升\n\n'
    text += 'Main先独立推导并实现单案；`/root/nested_price_contract`随后实读完整合同、最近既有共享末端对象，并从原输入独立重算两层占用流。本节保存可复用的一般证明。初段与尾闭包共享真实末题的机制已经存在于对象`M-63c882b0c8414805a43d4d8d4e43f4e3`；这里新增的是两个actual来源的明确付款、十四内权加五外权的完整提升和独立证书，不重新认领一般共享末端机制。以下式号在本后续部分内使用。\n\n'
    text += proof.rstrip() + '\n\n'
    text += '''## 5. 已核单案与九十案的精确停界

本节所有数值结论仅绑定19621×15593必要系统的点，SHA为`d70c26065d42fd73dedc94183e4533dd6f8608d5841f7a6018ff180dc77e2f9f`。该点不是完整SPE，不能将这里的有限参数锥边界推广为原题反例或普遍福利下界。

唯一嵌套配置为内源actual2、外源actual1、种子A6、θ=1/4，静态菜单为六个actual标签及六比较标签的均值。67变量、416条约束的发现返回行slack约0.0029339080942291937；返回权只使用内层四坐标，不能凭它认领跨源增益。更强的独立精确两层占用流证书给整个19权归一非负锥下界约0.0029339080942286013>0。它重算全部19预算残差及32条四状态流方程，证书SHA为`fec4cbb5fde2939f25c57408739026d403f078172b6e48f3837bbbeec94d0e75`；完整分数、量词与验证范围见`nested_price_contract.md`及其目录。没有从单案外推其它源、种子、折扣或菜单。

直接向六比较主题均价的90配置为actual1…5 × actual种子A1…6 × θ∈{1/4,1/2,3/4}。三批真实Actions在run43074273655、提交08d120b3337d3f3fcd608432bb288edcc81f8d33运行，全部输入、输出、下载artifact摘要和实际执行回执均已保存并逐字节绑定。三个目录各30案已由冻结的独立Fraction验证器本地重放，没有再运行优化器。

全部90配置都有精确占用流非分离证书。actual1…4的72案在完整14权归一锥上严格正；actual5的18案保留两个恒无效middle方向时完整14权锥下界恰零，删去这两方向后的有效12权锥严格正。全部90个有效归一锥的精确下界均严格大于1/400。各折扣的最小有效下界约为0.0025199411555453218、0.004582796321532381、0.005164532583751175。

批量复核共2880条折扣流式、436410个原列系数和966960个辅助零系数。全部案没有负行，故未触发逐案448型全Boolean审计；该完整域额外展开只在此前两份实现小试做过。不得将这两种核验范围合并夸大。90案所有精确分数和唯一覆盖集保存在`previous_price_search/all_90_cases.json`，交付审计及总manifest在同目录。

这些结论封住的是指定有限菜单和离散折扣的完整非负权锥。连续折扣、不同静态菜单和其它真实共同状态仍未由本节处理；六人half原题仍OPEN。
'''
    body.write_text(text.rstrip() + '\n')
    obj['version'] = 2
    obj['statement'] += ' 后续固定两个actual源、actual种子和静态菜单，十四内权与五外权可联合提升为有限LP，保留同一真实外末题和分别的源收益；给两层折扣占用流精确对偶。指定19621点上一嵌套19权配置以及90直接14权配置有精确全锥非分离证书；余两人恒无效参数方向明确保留为零界。'
    obj['scope'] += ' 十九权两源合同及完整线性提升为普遍结论；90案和一个嵌套案的非分离均为固定点、菜单和指定折扣的有限边界，不声称六人half或完整SPE。'
    extra = [BASE + p for p in (
        'nested_price_contract.md', 'nested_price_contract/verify_one_case.py',
        'nested_price_contract/independent_one_case_audit.json',
        'main_nested_price/solve_one.py', 'main_nested_price/one_case_exact.json',
        'previous_price_search.md', 'previous_price_search/discover.py',
        'previous_price_search/verify.py', 'previous_price_search/audit_delivery.py',
        'previous_price_search/all_90_cases.json', 'previous_price_search/delivery_audit.json',
        'previous_price_search/manifest.json',
        'previous_price_search/local_replay_theta14.json',
        'previous_price_search/local_replay_theta12.json',
        'previous_price_search/local_replay_theta34.json',
        'compute_dispatch/run43074273655.json', 'compute_dispatch/run43074273655-artifacts.json',
        'compute_dispatch/delivery.json')]
    obj['body'] = binding(obj['body']['path'])
    seen = {e['path'] for e in obj['evidence']}
    obj['evidence'] += [binding(p) for p in extra if p not in seen]
    obj['sources'] = list(dict.fromkeys(obj['sources'] + ['material:' + p for p in extra]))
    mats = {m['path']: m for m in reg['materials']}
    for e, bodyflag in [(obj['body'], True)] + [(e, False) for e in obj['evidence']]:
        p = e['path']
        if p in mats:
            if mats[p]['sha256'] != e['sha256']:
                assert p == obj['body']['path'], p
                mats[p]['sha256'] = e['sha256']
        else:
            m = dict(e, disposition='objects' if bodyflag else 'attachment',
                     object_ids=[ID], reason='Main实读量词、完整两源付款、线性提升和精确流证书后回流；固定点边界不推广。')
            mats[p] = m
            reg['materials'].append(m)
    target = HERE / 'stage8-price-registry-candidate.json'
    target.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + '\n')
    summary = {'base_registry_sha256': hashlib.sha256(regpath.read_bytes()).hexdigest(),
               'candidate_sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
               'object': {k: obj[k] for k in ('object_id', 'version', 'body')},
               'total_objects': len(reg['objects']), 'total_materials': len(reg['materials'])}
    (HERE / 'stage8-price-registration-summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
    (HERE / 'stage8-price.json').write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == '__main__':
    main()
