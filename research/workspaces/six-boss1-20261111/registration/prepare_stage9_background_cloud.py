"""Register the improved universal fee and the distinct 47/65-type bounds."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction as Q
import json

HERE=Path(__file__).resolve().parent
WS=HERE.parent
REPO=WS.parents[2]
BASE='research/workspaces/six-boss1-20261111/'
BID='customer-attraction/one-prefix-five-profit-exclusive-charge'


def bind(p):return dict(path=p,sha256=sha256((REPO/p).read_bytes()).hexdigest())


def main():
    rp=REPO/'research/registry.json';reg=json.loads(rp.read_bytes())
    obj=next(o for o in reg['objects'] if o['object_id']==BID)
    assert obj['version']==3 and bind(obj['body']['path'])==obj['body']
    summary=json.loads((WS/'background_reweight/actions_full/summary.json').read_bytes())
    upper=Q(summary['exact_upper_bound']);lower=Q(summary['exact_lower_bound'])
    assert Q(0)<lower<upper<Q(451,10000)
    u=json.loads((WS/'background_reweight/actions_upper_local_replay.json').read_bytes())
    l=json.loads((WS/'background_reweight/actions_lower_independent_replay.json').read_bytes())
    body=REPO/obj['body']['path'];text=body.read_text().rstrip()
    text+=r'''

# 58外权完整域证书：严格更小的普遍收费

保持本页原模型与利润目标、53套内部源合同和正确背景分母，另加五个实际尾位对合法Z的安全比较。第i位的新增真行是

\[
S_i^Z=u_i-\sum_x\frac{b_x}{b_x+p_{i,x}+6-i}\ge0,\qquad i=1,\ldots,5.
\]

它先用完整SPE比较真实偏离，再将当前及未来的6−i个会员取分母上界；只有i=5直接是末位精确比较。任意客户均使用同一个58维非负外权，所有行共用唯一容量K。

完整域证书现给

\[
\boxed{R_Z(T_1,\ldots,T_5)\le 2V+\varepsilon_{new}E_Z,\qquad
\varepsilon_{new}=\frac{NUM}{DEN}<\frac{451}{10000}.}
\]

其近似值为0.045031284569913524，较前文固定53权费用减少约9.5216%。该命题量化任意合法长度一历史、任意完整有序五尾纯SPE与任意五个合法比较索引；重复槽、弱平局、空题与零客户保持。E_Z≤r_Z仍给相应第一人利润收费式。五比较和五尾利润的定义未换成OPT6或新覆盖。

## 从全客户系数认证到普遍命题

记合法行S_j=sum_x a_j(omega_x)+k_j K，t=2c/(b+c)−d/(b+d)，e=1_(b=1,c=0)。保存的非负lambda与epsilon满足每个完整类型上的`t+epsilon e−sum lambda_j a_j≥0`，并满足`−sum lambda_j k_j=0`。因此恒等式

\[
2V-R_Z+\varepsilon E_Z
=\sum_j\lambda_jS_j-\Bigl(\sum_j\lambda_jk_j\Bigr)K
+\sum_x[t(\omega_x)+\varepsilon e(\omega_x)-\sum_j\lambda_ja_j(\omega_x)]
\]

逐项非负。证明不需要将扩大后的类型域实现为游戏，也不依赖有限游戏抽样。

全域精确检查覆盖两个背景、全部1024个十位掩码和六个比较重数，共12288个条件态。每态先按当前共同lambda组合一个族目标，再穷尽AB/AE/S三个族的792、792、15504个直方图，并检查完整菜单四角；三族用同一个d。全部分母统一后按Python整数计算，最小余项精确0，共同K余项精确0。保留46个正外权，五个新增Z查询仅尾第一位活跃。没有使用已失效的旧极值模式，也没有先逐行取极大再合权。

云任务run43077553308、job130721374378在实际提交d3938d9f00642d493959c17400d6f745568bf19d上运行46轮，保存18820个完整类型。Main核下载ZIP与API digest相等，并逐一核19份输入SHA；代理保持56份原输出字节，再做一次全域精确重放。上界证书SHA为`3df20bd623a3490906e3d1f3511e6503758679860650e3eaf35ff475b8b1aa6a`。Actions成功只是执行状态，以上整数恒等式与全域结果才承担数学结论。

## 47类型下界与65类型障碍不能混用

另一份47类型精确对偶给本58射线锥

\[
\varepsilon^*_{58}\ge\frac{LNUM}{LDEN}
\approx0.04497639859110952.
\]

全部58行用独立五索引原始公式重放，独占质量为1、唯一容量质量非负。上下界差约5.4886e−5，未证明本锥精确最优。后期浮点对偶在精确恢复中出现微小负行的失败均保留；不能把最后上界与较早的精确下界当作相等。

47类型对偶实际违反K−|Z|≥0，余量约−0.14643898168435043；七个隐藏真后继SAFE-Z全部严格正。故该47类型下界不适用于59或66行锥，前节独立65类型对偶才给那些较大锥的下界。

## 重复Z的完整19参数边界及一个可复用固定行

复用父档已证上一主题四态价格：actual尾第一源、剩余五人、theta=1/2、初态(previous,current)=(Z,Z)，静态十个合法题、五比较平均和Z，另有current/previous两动态查询。保19个全局非负参数，背景p=b、末价前缀ell=b+a+b_tail+c+d_tail；来源预算为sigma*u1+(3alpha_m+alpha_l)u5+(3beta_m+beta_l)K。符号b_tail等指尾主题会员，与前置背景b区分。

在前节65类型测度上，所有归一化19参数都无法分离，统一余量严格大于7/100。一份精确折扣占用流满足每型四个流守恒式；用其固定费用上界Bellman最小值后，19个参数坐标的预算残差均大于7/100。独立程序按三个位重建中间负载，并用路径/环解16个确定下一位策略，核2368个Bellman比较、148个流方程和全部19坐标。这里的占用流是参数LP对偶，非SPE策略。

同次返回的一条合法有理合同只用六个非零权，按(sigma,alpha_m,beta_m,mu_V,mu_W,mu_mean)=(3228,40,5,5,5,425)/3708；其预算为(3228u1+120u5+15K)/3708。它在65类型上为正，却在上述47类型上精确为负，约−0.0026617112286304555。后者仅重新代入冻结行，未另优化19参数；全部1472个字面Bellman比较独立通过。因此加入此行确实改变47类型障碍，但65类型仍阻止据此直接宣称零费。

准确下一问题是让新末题与已有真实末节点的客户价格共同保留，增加真实新查询和明确旧分支收入预算，而不是继续在已封19参数内调权。原六人half与一般零收费BG5仍OPEN。
'''.replace('LNUM',str(lower.numerator)).replace('LDEN',str(lower.denominator)).replace('NUM',str(upper.numerator)).replace('DEN',str(upper.denominator))
    body.write_text(text.rstrip()+'\n')
    obj['version']=4
    obj['statement']+=' 完整58权域现普遍证明独占费用epsilon约.04503128457<451/10000，46正外权、全部12288条件态精确非负；47类型给58专属下界约.04497639859，非精确opt。65类型上整个指定19参数重复Z锥余量>7/100；其固定有理行却可切47类型，严格区分两份方法障碍。'
    obj['scope']+=' 新收费适用于任意合法长度一历史与五比较；47类型下界不含MAX:Z，65类型边界另行保留。'
    extra=[BASE+p for p in (
        'background_reweight.md','background_reweight/cone.py','background_reweight/optimize.py','background_reweight/verify.py',
        'background_reweight/actions_full/exact_upper_certificate.json','background_reweight/actions_full/exact_upper_audit.json',
        'background_reweight/actions_full/exact_lower_certificate.json','background_reweight/actions_full/exact_lower_audit.json',
        'background_reweight/actions_full/summary.json','background_reweight/actions_upper_local_replay.json',
        'background_reweight/actions_lower_independent_replay.json','background_reweight/actions47_new_row_audit.json',
        'background_reweight/probe_actions47.py','background_reweight/freeze_actions_delivery.json',
        'background_reweight/repeated_z_price/contract.md','background_reweight/repeated_z_price/single_case_result.json',
        'background_reweight/repeated_z_price/verify_one.py','background_reweight/repeated_z_price/independent_audit.json',
        'background_reweight/repeated_z_price/manifest.json','compute_dispatch/background58-download-input-audit.json')]
    obj['body']=bind(obj['body']['path']);seen={e['path'] for e in obj['evidence']}
    # Earlier registry versions did not bind this formerly mutable solver note.
    obj['evidence']+=[bind(p) for p in extra if p not in seen]
    obj['sources']=list(dict.fromkeys(obj['sources']+['material:'+p for p in extra]))
    mats={m['path']:m for m in reg['materials']}
    for e,isb in [(obj['body'],True)]+[(e,False) for e in obj['evidence']]:
        p=e['path']
        if p in mats:
            if mats[p]['sha256']!=e['sha256']:
                assert p==obj['body']['path'],p
                mats[p]['sha256']=e['sha256']
        else:
            m=dict(e,disposition='objects' if isb else 'attachment',object_ids=[BID],reason='普遍收费由完整域整数恒等式承担，47/65对偶与固定19参数范围分开核对。')
            reg['materials'].append(m);mats[p]=m
    target=HERE/'stage9-background-cloud-registry-candidate.json';target.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
    out=dict(base_registry_sha256=sha256(rp.read_bytes()).hexdigest(),candidate_sha256=sha256(target.read_bytes()).hexdigest(),
             object={k:obj[k] for k in ('object_id','version','body')},total_objects=len(reg['objects']),total_materials=len(reg['materials']))
    (HERE/'stage9-background-cloud-registration-summary.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    (HERE/'stage9-background-cloud.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(out,ensure_ascii=False))


if __name__=='__main__':main()
