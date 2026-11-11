"""Promote the exact free-outer-weight fee obstruction; keep game scope clear."""
from pathlib import Path
from hashlib import sha256
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = WS.parents[2]
BASE = 'research/workspaces/six-boss1-20261111/'
BID = 'customer-attraction/one-prefix-five-profit-exclusive-charge'


def bind(p):
    return {'path': p, 'sha256': sha256((REPO/p).read_bytes()).hexdigest()}


def main():
    rp = REPO/'research/registry.json'
    reg = json.loads(rp.read_bytes())
    obj = next(x for x in reg['objects'] if x['object_id'] == BID)
    assert obj['version'] == 2
    assert bind(obj['body']['path']) == obj['body']
    body = REPO/obj['body']['path']
    text = body.read_text().rstrip()
    proof = (WS/'background_reweight/free58_66_lower_bound.md').read_text()
    general = proof[proof.index('## 一、可复用的一般解析拼接'):proof.index('## 二、本次选定的64原子输入')]
    rows = proof[proof.index('## 四、七个隐藏真实后继查询的完整角色核定'):proof.index('## 五、逐层独立证书与冻结结果')]
    c53 = json.loads((WS/'background_reweight/free53_lower_certificate.json').read_bytes())
    c66 = json.loads((WS/'background_reweight/free66_lower_certificate.json').read_bytes())
    a53 = json.loads((WS/'background_reweight/free53_lower_independent_audit.json').read_bytes())
    a66 = json.loads((WS/'background_reweight/free66_lower_independent_audit.json').read_bytes())
    assert a53['status'] == 'EXACT-LITERAL-DUAL-REPLAY-PASSED'
    assert a66['status'] == 'EXACT-LITERAL-66-ROW-LOWER-BOUND-PASSED'
    assert a53['lower_bound'] == c53['lower_bound']
    assert a66['lower_bound'] == c66['lower_bound']
    n53,d53=c53['lower_bound'].split('/')
    n66,d66=c66['lower_bound'].split('/')
    text += r'''

# 后续：固定内部源合同的自由外权仍有严格正费用

此前仅固定53个外乘子得到epsilon<1/20。现在给出整个自由外权证明锥的精确方法下界。下列下界不反原游戏BG5或六人half；其对偶类型只位于明确的系数域，未给完整策略或共同目录实现。Main已读回一般拼接证明、真实隐藏节点历史、逐条字面核验器和全部来源绑定。

## 方法锥的量词与两个严格下界

固定本页原53条正确背景化的局部合同及其内部源乘子。允许全部外权任意非负，但b=0/1客户共享同一个向量，所有行共享一个K。每客户余项及总K余项非负构成所研究的证明系统。目标仍为背景五尾总利润`R_Z≤2V+epsilon E_Z`，不换成新覆盖或OPT6。

对原53射线锥，77个精确对偶类型给

\[
\epsilon_{53}^*\ge\frac{N53}{D53}
\approx0.01882600675955369>0.
\]

这严格排除自由重配原53外权后零费，强于只固定原53向量的失败；其上界仍由本页原epsilon证书给出。这个77原子不满足新增实际Z查询或K−|Z|，不能用于较大锥。

另一个65类型对偶同时通过原53、实际五个Z查询、容量K−|Z|和下面七个真实隐藏后继Z查询，共66行。因此连这些明确新约束一并纳入的全非负外权锥也有

\[
\epsilon_{66}^*\ge\frac{N66}{D66}
\approx0.00007931649684860619>0.
\]

此下界也适用于中间58和59行锥；没有认领收费最优值，亦没有把所有可用合法关系等同于这66条。原内部源权、被保留查询和系数域都是结论条件。

'''.replace('N53',n53).replace('D53',d53).replace('N66',n66).replace('D66',d66)
    text += general.rstrip()+'\n\n'
    text += r'''## 两个既有零背景输入的准确复用

77原子使用既有737行记录中的76个正类型，来源`archives/customer-attraction/tools/evidence/dual-terminal-exact-resumed-boss2/original/exact_optimum_primal_dual_terminal.json`，SHA`1c7b256ee4e72c686bb8bb7db4ac2d199cc2890463bf7138cd2761f8756c62fd`。本次重新核35条零K行，33零两正；不认领重验其全部737行。其R−2V约0.042103，按一般拼接增加一个背景独占类型后给第一个下界。

65原子使用既有7497行记录的64类型投影，来源`archives/customer-attraction/tools/evidence/five-full-actual-extension-primary/original/certificate/exact_full_actual_extension_known_v1.json`，SHA`8b28de8d89c76684bc95c3eb3f890e6f4ee4492cb152102281d125912e2a30e2`。本次只重建bits、三族直方图、共同d和菜单，未认领重审全部7497行或额外HQR字段。其R−2V为正、约3.7203e−5；紧正K行为AB:PC:6:eq:2:1，所加独占质量m0约0.4690491403。归一后全部58/59/66行独立字面核验均非负。

容量K−|Z|在第二个对偶上严格为正，约0.35548。原MAXROOT行加1983898倍此容量行，确实得到无显式背景费的普遍合同

\[
46313177u_A-5428464K-10^6R_Z\ge0.
\]

然而它在同一对偶上仍严格正：原MAXROOT余量零，所加容量余量正。用这个替代合同的锥包含于59行锥，故也被上述方法下界阻断；不能从“背景费抵消”跳到免费半利润。

'''
    text += rows.rstrip()+'\n\n'
    text += r'''## 独立核验与新的具体义务

工作区`research/workspaces/six-boss1-20261111/background_reweight/`完整保存77及65原子、全部分数质量、共享容量、源点转换、每行余量与来源SHA。`lower_replay_independent.py`不导入优化器或极大化oracle，逐五索引核原53和实际5行；`capacity59/verify_archived_lower.py`再核MAX:Z；`verify_free66_lower.py`独立展开七个真实后继。最后结果为EXACT-LITERAL-66-ROW-LOWER-BOUND-PASSED，独占质量恰为1，全部66行非负。66证书SHA为`64b45243dcb3a0285f7821eb3528554540871c05d335dd089200f9056375237f`。

独立对偶足以排除整个明示锥的零费，不须等云优化完整扫完类型。已启动的58行云任务仍可给更小的普遍上界或最佳收费，不提前把其运行状态当数学结果。继续追求免费BG5需要原对偶实际违反的新合法关系，或新的内部源合同。

Main指出下一具体来源：实际尾某位强制同目录Z后，后继必须再次最优；SAFE允许任意最坏续局，尚未完整表达这一步。新的重复Z四态合同取背景p=b+实际前缀、初态(Z,Z)，独立付尾实际源收入及末价/容量，保同一C_h轨道。这一步仍在研究，不作为已证零费或新福利结论。
'''
    body.write_text(text.rstrip()+'\n')
    obj['version']=3
    obj['statement'] += ' 后续对固定内部源合同的自由53外权锥给77类型精确收费下界约.018826；另65类型对偶同时通过实际5条Z查询、K−|Z|及7个真实隐藏后继Z查询，故整个66射线锥费用仍至少约7.93165e−5。给一般解析拼接证明及无显式背景费MAXROOT合同，明确为方法障碍而非BG5/SPE反例。'
    obj['scope'] += ' 固定内部源合同且客户/K逐项非负的53、58、59、66外权锥方法下界；所有新隐藏查询只来自真实后继，不对强制座位套IC。'
    extra=[BASE+'background_reweight/'+p for p in (
        'free53_lower_bound.md','free53_lower_certificate.json','free53_lower_construction.json',
        'free53_lower_independent_audit.json','free58_66_lower_bound.md',
        'free58_lower_certificate.json','free58_lower_construction.json','free58_lower_independent_audit.json',
        'free66_lower_certificate.json','free66_lower_independent_audit.json',
        'lower_replay_independent.py','verify_free66_lower.py','hidden_z_probe.py','hidden_z_probe.json',
        'capacity59/archived_lower_certificate.json','capacity59/archived_lower_independent_audit.json',
        'capacity59/verify_archived_lower.py','freeze_65_atom_manifest.json','supplement_manifest.json')]
    extra += ['archives/customer-attraction/tools/evidence/dual-terminal-exact-resumed-boss2/original/exact_optimum_primal_dual_terminal.json',
              'archives/customer-attraction/tools/evidence/five-full-actual-extension-primary/original/certificate/exact_full_actual_extension_known_v1.json']
    obj['body']=bind(obj['body']['path'])
    seen={e['path'] for e in obj['evidence']}
    obj['evidence'] += [bind(p) for p in extra if p not in seen]
    obj['sources']=list(dict.fromkeys(obj['sources']+['material:'+p for p in extra]))
    mats={m['path']:m for m in reg['materials']}
    for e,isb in [(obj['body'],True)]+[(e,False) for e in obj['evidence']]:
        p=e['path']
        if p in mats:
            if mats[p]['sha256']!=e['sha256']:
                assert p==obj['body']['path'],p
                mats[p]['sha256']=e['sha256']
        else:
            m=dict(e,disposition='objects' if isb else 'attachment',object_ids=[BID],reason='Main核一般对偶证明、真实节点预算与独立逐行证书；方法锥和游戏命题范围严格区分。')
            reg['materials'].append(m);mats[p]=m
    candidate=HERE/'stage9-background-registry-candidate.json'
    candidate.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
    summary={'base_registry_sha256':sha256(rp.read_bytes()).hexdigest(),
             'candidate_sha256':sha256(candidate.read_bytes()).hexdigest(),
             'object':{k:obj[k] for k in ('object_id','version','body')},
             'total_objects':len(reg['objects']),'total_materials':len(reg['materials'])}
    (HERE/'stage9-background-registration-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    (HERE/'stage9-background.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False))


if __name__=='__main__':
    main()
