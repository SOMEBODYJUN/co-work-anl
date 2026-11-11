"""Promote reviewed point-specific completions and the full624 separation."""
from pathlib import Path
from hashlib import sha256
import json

HERE = Path(__file__).resolve().parent
WS = HERE.parent
REPO = WS.parents[2]
BASE = 'research/workspaces/six-boss1-20261111/'
CID = 'customer-attraction/six-providers/cross-branch-necessary-system-20261111'


def bind(path):
    return dict(path=path, sha256=sha256((REPO/path).read_bytes()).hexdigest())


def main():
    rp = REPO/'research/registry.json'
    reg = json.loads(rp.read_bytes())
    obj = next(o for o in reg['objects'] if o['object_id'] == CID)
    assert obj['version'] == 6 and bind(obj['body']['path']) == obj['body']
    body = REPO/obj['body']['path']
    old = body.read_text()
    text = old.rstrip() + r'''

## 19662点的全旧网络、同一B4与239根尾预算

本节所有数值均重新绑定第八个精确点，SHA为`b0ca65cfe61e5e3ef09537cba2a986c171aeaa7106f673077f803c80ee2b68e3`。旧19621的600个强制ZZ零格没有迁移到本点。

### 全旧R/Z和同一B4确有共同完成

每个正hist允许四个R/Z区间取向的独立相权；取向内部用同一个客户区间实现全部66节点，再用一张不带节点索引的运输表耦合同一B4状态。此表同时保持16hist×66×4项own边缘和16×8项B4边缘，非负有理解有92个规范正原子。按720个同步索引置换展开为66240个正原子，总质量1，清516位公共分母得到有限单位客户层。

所有17424条旧真实末位查询均非负：RR有4260正/96零，RZ与ZR各4356正，ZZ有4170正/186零。同一B4的15条轨道预算有13正/2零。B4为actual第四源强制A6后的真尾(H1,H2)，其第三状态y=ell/6只代表六个合法菜单查询的线性平均，不把y当新的具名强制主题。所谓330项字面展开是展开旧节点索引后的这些查询/菜单平均，不能据它恢复六菜单标签各自的响应树。

独立核验器不导入构造器，按真实R前缀p3+t_i+(w_j)_(1+f)和真实Z前缀P+r_e重建所有收益；保留零质量hist，并核同步置换下的原词、节点和真正前缀。原1306个RR上包络aux不当作真实交叠。具体原子和全部字面分数见`common_network_19662/common_atoms.json`及`independent_verification.json`。

本点39个非自查ZZ单查询上界均严格正；构造中120个非自查ZZ取零只属于所选测度。然而B4的两条F→Z非对角轨道单查询上界本身恰零。设C_h=|H1|_h、s_h=p3+a6+1，则任意共同实现都满足

\[
\int_h\frac{z_e}{s_h+h_1}
=\frac{v_e}{s_h}-\frac{|Z_e\cap H1|_h}{s_h(s_h+1)}
\ge\frac{v_e}{s_h}-\frac{\min(v_e,C_h)}{s_h(s_h+1)}.
\]

真实IC非负，而固定边缘给出的上界为零，故所有非负缺口必须为零。同步对称化后，对60个非对角节点和每个正hist，均强制`|Z_e∩H1|=min(v_e,C_h)`。因此这15项预算的最大共同最小余量恰为0；原题允许弱平局，不能要求严格正。这一新强制包含来自本点自己的B4，区别于旧点ZZ强制面。

### 同一旧词与六根真尾：239项预算完成

在同一新点重配根状态质量后，17个正原子保持全部16个hist及同步有名旧词的完整分布，满足原203项非根预算、36项新增跨枝强PAIR和根源IC。新增PAIR全部严格正，最小约0.023310485724237766。全部具名旧/根接口有1368项，其中1308正、60零；原子、分数预算和独立全系数核验在`root_pair_joint_19662/`。

新增PAIR只在自己的真实两位尾源使用。对固定背景p，真尾(D,E)，强制X后真末R，并查询合法Z，记U(a,b)=a/(p+1+b)、g(a,b)=ab/[(p+1)(p+2)]。三条真IC给

\[
U(D,E)+U(E,D)+g(D,D)-\frac{X+Z}{p+1}+g(X,Z)
=I_1+I_2+I_3+g(D,D)-g(D,R)\ge0,
\]

其中I1=U(D,E)−U(X,R)，I2=U(R,X)−U(Z,X)，I3=U(E,D)−U(R,D)。末余项非负，且每条行完整支付该源的两份真实收益和一次倒数第二位税。旧尾(B_i,C_i)查询同一新根两题，或新根最后真尾查询同一旧索引的B_i/C_i，均保持同供体交叠；不以actual u5+u6替代离轨尾收入。

根源权固定为1时，本测度给全239非负权族的严格余量下界

\[
L=\frac{4041031686870009635722613407485341280812089022187303706988466563671438419812308478279}
{277572772367441378580955309013415529536718448131428627118612152038976055861365508422816}
\approx0.014558458498662216.
\]

因为任何局部共同min不大于这份合法候选测度的平均，任意非负权lambda均有余量至少L+sum(lambda_j slack_j)≥L，无须把lambda归一。若根权另设rho则只能写rho L。这与上述R/Z+B4测度仍是不同的已给构造；本节尚未在两者间施加新的跨块查询，亦未建立完整SPE。

## 完整624共同隐藏约束严格排除19662冻结点

本次不是只加一个已有624方向，而是在actual第四源、强制旧R、family0非对角的指定结构保留完整624预算。所有4849原描述符、W/O向量精确匹配，原10744aux的新行系数为零；16hist中的6个零质量hist、78个词对group、312个旧R/Z四态边缘和4992个新非负隐藏列全部保留。

固定hist H和有序异索引词对g=(w,w')，轨道重数为n_H(w)(n_H(w')−1_(w=w'))，除30得到omega_Hg。原joint列是条件边缘质量，不再除重数。旧00态为H减其余三态。所有624行读取同一个X_Hg,rz,bcjv，且sum_bcjv X=m_Hg,rz。预算为

\[
R_a=B_a-\sum_{H,g,rz,b,c,j,v}\omega_{Hg}E_a(H,g,rz,b,c,j,v)X_{Hg,rz,bcjv}\ge0.
\]

sourceT/sourceC各付同一actual u4；四个宏主题价格各付同一actual u6，容量各付K；真查询和强PAIR各保自己的真实背景。Main实读了承重正文、代理对全部3115008隐藏特征系数的重建及独立30720次字面隐藏态核验；同一第一枝真末c既是第二枝强制标签，又在所有有关成本中保持同一会员。

一个只用16个正整数权的方向给钱包

\[
36170u_4+13970u_6+1199K.
\]

其权为sourceT=23172、sourceC=12998，price(b,c,j,v)=(3685,3408,2956,3921)，cap(v)=1199，last2:b=4832，last1:q6=last1:q8=2883，pair2:q6,b=72，last1:q10=2846，last2:q10=18，pair2:q14,b=288，oldpair1:6,10:product=3972，priorZ:v=198。q6=T_i、q8=C_i、q10=B_j；q14为删去两个异索引后余四个合法T的平均，非分数强制标签。

合权成本F在同一16隐藏态上取Psi=min F，给原4849维必要行`钱包−sum omega*m*Psi≥0`。其当前点整数尺度余量为

\[
-\frac{49169222696486741435910661376175414586214702639048552449306883270564918877001}
{374341564037353375582545703568752265065109519311538601851678433921391424716202796}<0.
\]

除权和69331后约−1.8945140387341755e−9。另一条独立有理方向也严格负，约−9.41897780044493e−10；早期10^6和10^7网格的正余量失败均保存。同行新精确对偶的624部分与紧整数方向同正射线，已去重，不能计为第三条不同切面。

符号消元恒等式为

\[
\Pi_\lambda=\sum_a\lambda_aR_a
+\sum_{g,s,h}\omega_g(F_\lambda-\Psi_\lambda)X_{g,s,h}
+\sum_{g,s}\omega_g\Psi_\lambda(\sum_hX_{g,s,h}-m_{g,s}).
\]

所有lambda和min余项非负，等式可用正反两行支付；每个新列精确消去。两套独立字面公式程序分别核全部16hist×30有序索引对×4旧态×16新态=30720组合、15593列和严格负值。故结论是完整提升不可能保住该冻结点，不依赖浮点tol。

通用符号包`complete624_transfer/full_lift_bundle.json.gz`（SHA`3031a0710bd3b99fe421889ccb891e671d11f019f7d9cc9b3165818adc759d03`）可一次追加1248行与4992列，形成20910×20585系统。新行不以当前点数值替换rhs，新列目标/归一为0。旧精确对偶零扩展仍有效；原最优面有自由方向，排除一个点不证明新最优值上升。完整增广正作为新独立义务求解，本节不预报其结果。

## 冻结共享R/Z收入桥的完整三权边界

对同行正式共享桥中的两套冻结alpha/beta合同，Main核回原真实份额、四态消元及保持末端v的强A6映射，承重边完整前提成立。令A_r、B_z分别为这两套完整成本，预算为(999alpha+10000beta)u4+(139alpha+1358beta)u6；同一旧family1非对角R/Z查询另加lambda(q−z)/(P+r+1)，q=n/6。

逐客户令k=P+1，a=alpha(A1−A0)，b=beta(B1−B0)，h=lambda*q/[k(k+1)]。准确共同四态min为

\[
J=\alpha A_0+\beta B_0+\lambda q/k+
\min\{0,b-\lambda/k,a-h,a+b-\lambda(k+q)/[k(k+1)]\}.
\]

因两个冻结差值均正，00态最小恰当且仅当a≥h且b≥lambda/k。2560型完整有理核验表明对所有型恒成立的参数域恰为`alpha≥3lambda/1100, beta≥2lambda/3593, lambda≥0`；两个最大比值均由明确类型达到。若复制R、允许A与Z前缀用独立会员，记相应min为S，则直接比较四态给

\[
J-S=\min\{a,h,[b-\lambda/k+h]_+\}.
\]

这也覆盖参数面外及零源权边界，不把49:10当成极限。锐整数射线为(10779,2200,3952300)，保持v的强A6信用后预算为32768221u4−281298u6；完整公式、边界见证及独立真行展开在`rz_income_bridge_review.md`。

更直接的点证书是三份原始合同在19662同一own四态上的余量分别为sA≈1.869842921326725、sB≈0.8577252800841303、sZ≈0.017276819602006718，全部精确正。任意三非负权的raw余量=alpha*sA+beta*sB+lambda*sZ≥0；共同四态min、强移账、覆盖摘要只更弱。因此整个固定三权锥均不能切此点，不必扫参数网格。该范围不包括任意内部源权或新末题与旧R/Z的未合入互查。

## Main新接口与仍未完成的工作

Main另从真末位分母独立生成152条旧T/B/C/R/Z、actual与同一B4的直接线性查询，130正、22零、无负；34条在当前矩阵中不存在正比例副本，但未证明它们线性独立或不可由旧系统推出。完整原4849行向量在`main_19662_terminal_catalog.json`。

因此下一义务保留真正的新回复D_i=σ6(A1,A2,A3,A4,T_i)，由actual u5支付其源IC，再让D_i与旧R/Z、H1/H2和实际目录互查。`main_fifth_reply_contract.md`给通用符号边缘/交叠上界及精确Farkas条件；F→D必须保六索引1/6平均，隐藏前缀不能按独立边缘替代。此时尚未执行完该提升，不把规划写成新切面。原六人完整SPE半覆盖题仍OPEN。
'''
    body.write_text(text.rstrip()+'\n')
    marker = '# 一条不花实际末位收益的显式容量行'
    def capacity_section(s):
        q = s.index(marker)
        end = s.find('\n# ', q+len(marker))
        return s[q:end if end >= 0 else None]
    assert capacity_section(old) == capacity_section(text)
    obj['version'] = 7
    obj['statement'] += ' 第八点有92原子完整旧R/Z+同B4完成及17原子239根尾预算完成；完整actual4/R/family0-off的624共同隐藏系统却以两条精确负行排除该点，已交20910×20585通用提升包，福利是否上升待解。固定共享R/Z三权锥全域不能切该点，给锐参数面及准确共享增益。'
    obj['scope'] += ' 新共同层和完整624分离均只绑定19662点及原16hist域；两共同块尚未施加新的跨块查询；所有有限LP结果与原SPE命题严格区分。'
    extra = [BASE+p for p in (
        'common_network_19662.md','common_network_19662/common_atoms.json',
        'common_network_19662/common_atoms_expanded.jsonl.gz',
        'common_network_19662/verify_common.py','common_network_19662/independent_verification.json',
        'common_network_19662/four_phase_exact_recovery.json','common_network_19662/final_manifest.json',
        'root_pair_joint_19662.md','root_pair_joint_19662/joint_completion_exact.json',
        'root_pair_joint_19662/verify_completion.py','root_pair_joint_19662/independent_audit.json',
        'complete624_transfer.md','complete624_transfer/contract_audit.json',
        'complete624_transfer/compact_separating_row_exact.json','complete624_transfer/separating_row_exact.json',
        'complete624_transfer/verify_literal_row.py','complete624_transfer/literal_row_verification.json',
        'complete624_transfer/verify_rounded_literal_row.py','complete624_transfer/rounded_literal_row_verification.json',
        'complete624_transfer/full_lift_bundle.json.gz','complete624_transfer/full_lift_bundle_verification.json',
        'complete624_transfer/row_transfer_pack.json','complete624_transfer/freeze_manifest.json',
        'rz_income_bridge_review.md','rz_income_bridge_review/source_reading.json',
        'rz_income_bridge_review/audit_bridge.py','rz_income_bridge_review/audit_bridge.json',
        'rz_income_bridge_review/primitive_rows.json','rz_income_bridge_review/final_manifest.json',
        'main_terminal_catalog_audit.py','main_19662_terminal_catalog.json','main_fifth_reply_contract.md')]
    obj['body'] = bind(obj['body']['path'])
    seen = {e['path'] for e in obj['evidence']}
    obj['evidence'] += [bind(p) for p in extra if p not in seen]
    obj['sources'] = list(dict.fromkeys(obj['sources']+['material:'+p for p in extra]))
    mats = {m['path']: m for m in reg['materials']}
    for e, isbody in [(obj['body'], True)]+[(e, False) for e in obj['evidence']]:
        p = e['path']
        if p in mats:
            if mats[p]['sha256'] != e['sha256']:
                assert p == obj['body']['path'], p
                mats[p]['sha256'] = e['sha256']
        else:
            m = dict(e, disposition='objects' if isbody else 'attachment', object_ids=[CID],
                     reason='Main实读真实分母、共享隐藏身份、全域独立核验及严格适用范围；不将有限投影当完整SPE。')
            reg['materials'].append(m)
            mats[p] = m
    target = HERE/'stage9-computation-registry-candidate.json'
    target.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
    summary = dict(base_registry_sha256=sha256(rp.read_bytes()).hexdigest(),
        candidate_sha256=sha256(target.read_bytes()).hexdigest(),
        object={k:obj[k] for k in ('object_id','version','body')},
        total_objects=len(reg['objects']),total_materials=len(reg['materials']),
        unchanged_capacity_bearing_section=True)
    (HERE/'stage9-computation-registration-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    (HERE/'stage9-computation.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summary,ensure_ascii=False))


if __name__ == '__main__':
    main()
