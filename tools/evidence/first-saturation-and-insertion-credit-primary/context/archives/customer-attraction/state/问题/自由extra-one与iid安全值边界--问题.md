---
id: customer-attraction/free-extra-one-iid-security-boundaries
kind: problem
type_tag: 问题
title: 自由extra-one与iid安全值桥的边界
status: structured-subclass-proved; general-extra-one-Mfull-NQ-all-p-WP-refuted; historical-tests-retained
summary: 保结构归属定理和最小反例正规形；银行完整SPE经Jensen同时否定整数extra-one逐人桥及完整根菜单低值候选，历史有限阴性不再代表当前开放。
source_refs:
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-0f99797b33de46bfb498541a0bc5fae9/security/structured_maximal_membership_theta.md
- source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-0f99797b33de46bfb498541a0bc5fae9/security/structured_maximal_membership_theta.md
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-0f99797b33de46bfb498541a0bc5fae9/security/audit_structured_theta.py
- source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-0f99797b33de46bfb498541a0bc5fae9/security/audit_structured_theta.py
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-0f99797b33de46bfb498541a0bc5fae9/security/structured_theta_audit.json
- source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-0f99797b33de46bfb498541a0bc5fae9/security/structured_theta_audit.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-0f99797b33de46bfb498541a0bc5fae9/security/minimal_extra_one_counterexample_normal_form.md
- source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-0f99797b33de46bfb498541a0bc5fae9/security/minimal_extra_one_counterexample_normal_form.md
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-0f99797b33de46bfb498541a0bc5fae9/security/extra_iid_probe.py
- source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-0f99797b33de46bfb498541a0bc5fae9/security/extra_iid_probe.py
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-0f99797b33de46bfb498541a0bc5fae9/security/extra_iid_probe_report.json
- source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-0f99797b33de46bfb498541a0bc5fae9/security/extra_iid_probe_report.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-0f99797b33de46bfb498541a0bc5fae9/security/full_weak_wp_probe.py
- source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-0f99797b33de46bfb498541a0bc5fae9/security/full_weak_wp_probe.py
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-0f99797b33de46bfb498541a0bc5fae9/security/full_weak_wp_report.json
- source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-0f99797b33de46bfb498541a0bc5fae9/security/full_weak_wp_report.json
- source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-0f99797b33de46bfb498541a0bc5fae9/security/README.md
- source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-0f99797b33de46bfb498541a0bc5fae9/security/README.md
---

# 自由 extra-one 与 iid 安全值桥的边界

状态：条件结论、有限实验与障碍均已整理。下文九源的OPEN为历史记述；当前完整根菜单Mfull、全p-WP与低值对称Nash-NQ已有[银行反例](../反例/笛卡尔银行完整根菜单的低值自洽分布失败--反例.md)。自由分数extra-one逐人桥的后续反族见[银行门槛反族](../反例/笛卡尔银行目录的逐人分数门槛反族--反例.md)。本页不认证其它旧OPEN仍为现状；恰六人half未被这些例否定，五人half已有[定理](../定理/五人半覆盖--定理.md)。

本条目处置 R-0f997 的 security 九源。研究对象是六人有限单位客户、有限非空共同目录、完整有序历史纯 SPE；形式推理允许任意合法主题前缀形成的整数背景负载、任意历史依赖平局，以及空主题、重复标签、零客户和离轨历史。这里的“首位桥”是对任意剩余人数 r 和背景 b，完整纯 SPE 的首位收益下界；它不能被静态菜单、末位均衡或有限浮点扫描替代。

## 一、已证的结构子类

源 `structured_maximal_membership_theta.md`（源 ID `80aba6921fb21711d77e`）给出目前最强的确定性结果。把覆盖集合去重后取包含极大主题 A_1,...,A_k；对每个客户 x 记 J_x={j:x∈A_j}。若

    |J_x| ∈ {1, k-1, k},

则对任意合法背景 b、任意 r>=1、任意完整历史纯 SPE，首位以及每个真实中继子博弈首位的最终收益至少

    theta_r(b)=min_(B∈S^(r-1)) max_(A∈S)
              sum_(x∈A) 1/[b_x+1+load_B(x)].

证明采用最小剩余人数反例、强制每个极大根行动后的真实中继、固定主题的静态嵌入

    theta_(r-1)(b+1_A) >= theta_r(b),

以及驻留矩阵支付。逐客户分为单例归属、全体归属和缺一归属三类；三类的根减后继平均收益系数对任意驻留分布的加权和均非负。因而空背景 m 人时

    W >= m theta_m(0) >= m v_m(0) >= m OPT_m/(2m-1),

其中共同核心 C 还给出精确的 residual 分解和

    OPT_m <= c+(2-1/m)(W-c),  c=|C|.

该结构结论不限制 k，内部子主题可任意遗漏核心或互相交叠；它包含 sunflower，但与 laminar 归属条件不可互相替代。最末位严格扩展论证只用于说明实际福利覆盖共同核心，不改变 theta 证明的量词。

`audit_structured_theta.py`（`97017267eec76c218ff9`）逐项实现脚本中的有理标量不等式和有限全 SPE 首位核验。`structured_theta_audit.json`（`474f23b5b52af2f917fc`）的冻结输出为 3744 个标量检查、10 个有限实例；实例的 `all_spe_first_floor` 均不低于对应 theta。报告明确写出“universal result rests on written proof”，所以这些数字是有限证据，不是普遍证明的替代。

### 结构范围的停界

同一 audit 保留一个真正的中间归属障碍：k=4、r=3、b=0，客户只属于极大主题 1、2；四个根分支的后继归属为

    1 -> (2,3),  2 -> (1,4),  3 -> (1,4),  4 -> (2,3).

均匀驻留分布下，若每支实际后继负载为 1，则逐客户系数为 (1/4,1/4,-1/2,-1/2)，加权和为 -1/8。此例只反驳“把结构支付模板直接外推到任意中间归属”；它不是合法完整 SPE，也不是一般 half 反例。后续若处理一般目录，必须使用跨客户或更细真实节点支付。

## 二、一般目录的 extra-one 最小反例正规形

当前原整数静态F_r也已否定，不能只报告自由分数门槛失败：令Q为任意r槽合法整数背景的混合，其均值负载仍在r·conv{1_A}内。逐客户Jensen给max_T E_Q[Σ_(x∈T)1/(b_x+1+c_x)]≥B_r(b)，对Q取min即真正整数静态安全值v_(r+1)(b)≥B_r(b)。银行m4的完整SPE给u=4/3<19/14=B4≤v5；一般m≥4亦然，包含恰六人。这里是下界关系，不把整数值与自由分数值宣称相等。故下面最小反例正规形保其条件推导和已证小目录边界；不再将其一般目标当成尚待证明。Mfull失败、整数F_r失败、自由分数桥失败与half各是不同命题。

源 `minimal_extra_one_counterexample_normal_form.md`（`c3317c7ab24c0a5af1b5`）研究较弱的候选

    F_r: 首位收益 u >= v_(r+1)(b),

其中 v 是静态安全值，静态对手先定 r 个组合且不观察查询实现。若 F_r 在任意合法背景、目录和完整纯 SPE 中失败，按剩余人数取最小反例，记 t=v_(r+1)(b)，实际首位收益 u<t。对每个根行动 A，强制该行动并沿原策略取真实终局 z^A，根收益 d_A<=u<t。最小性和固定主题静态嵌入给出同一真实分支每个后继玩家的收益至少 t。

因此后继主题 B 不能满足 B⊆A；更强的是在该终局中

    outside_A(B;z^A)
      =sum_(x∈B\A)1/[b_x+c_x(z^A)] >= t-d_A >= t-u > 0.

每个根分支的 r-1 个后继必须提供总根外信用至少 (r-1)(t-d_A)。这是必要条件，尚未证明这些信用可以跨根分支聚合支付根损失。该正规形还证明最小反例 r>=3，并完整解决至多两个目录主题的 F_r：一主题被根外信用排除；两主题时每个强制根分支的所有后继只能选另一主题，根收益与后继收益的显式和式给出 d_A>=e_A，而正规形要求 d_A<t<=e_A，矛盾。

所以这部分是**条件归约和已证边界**，不是一般目录的反例，也不是一般 F_r 的证明。它为第三阶段留下的真实义务是：在至少三个且有中间归属的极大主题中，能否把各根分支的正根外信用组织成全局支付；不能把“后继不包含根主题”升级成后继之间两两不包含。

## 三、iid 与弱 WP 两条有限探测路线

`extra_iid_probe.py`（`694285d186bbc6a9ab78`）先以固定 iid Nash 概率 q 计算静态候选 lambda，再用完整有序历史策略锥的所有激励行约束，求固定 q 下首位收益低于候选的线性规划。`extra_iid_probe_report.json`（`d76144d7ff870e374d1c`）共有 115 个可行记录（脚本尝试 120 个 case，跳过不可行或非收敛记录），k=4/5，r=3/4/5，包含随机非负整数权和 0、1、2 的前缀背景；`best_gap=0`。原报告同时记录每例根、q、KKT 误差、gamma 行数、完整历史数和实际 gap；这些均为浮点诊断，不能证明所有目录或所有 q。

`full_weak_wp_probe.py`（`1e291fa347bfff5d3c9e`）测试更强的全 p 形式

    p^T K p <= u

而不是 Mfull 中的 `min_b p^T K[:,b] <= u`。它对 k=4/5、r=3/4/5 的 80 个完整策略和所有非空均匀支持 p 求线性规划；`full_weak_wp_report.json`（`5989499940c8c0986df2`）输出 `best=0`。报告明白标注“all-p WP not Mfull”，所以无正差只说明该有限域未找到这项全p二次型违反，不能作为Mfull、iid桥或一般half的普遍证明。

README（`d18feeb0709a144aadce`）把这四条边界汇总为：结构化 theta 是已证主成果；extra-one 与 extra-iid 仍是候选；有限扫描不构成一般结论。其余脚本还保留了失败路线的名称和停止追加同类样本的理由，不能把 README 摘要当作新的数学证据。

后续校正：上述 `best=0` 仅是历史有限阴性。完整银行四人根例保根共四槽，对每个列分布Q都有 `max_T(KQ)_T>=B4=19/14>u=4/3`；所有对称NE的值更精确为59/36，故一般Mfull、低值NQ及全p-WP均已否定。它不是删根矩阵，不反驳half，也不据此判定其它iid或路径级桥，详[完整根菜单反例](../反例/笛卡尔银行完整根菜单的低值自洽分布失败--反例.md)。

## 四、对当前六人目标的用法与未解决义务

这些来源没有改变当前六人目标的完整量词：所有完整有序历史纯 SPE、所有合法平局、所有空主题/重复/零客户/离轨历史都要保留。可直接使用的部分是结构化归属子类及其共同核心精确式；一般目录只能使用 extra-one 的正规形作为反例筛选条件，不能把它写成半覆盖定理。有限 iid/WP 输出适合第三阶段回放和回归检查，适合发现潜在正差或代码错误，不适合作为证明。

下一步若要推进一般目录，应在真实中继的根外信用上建立跨分支守恒或构造合法完整 SPE 反例；至少要同时满足每个强制根分支的根收益低于 t、每个后继收益不低于 t、以及每个后继的根外折扣至少 t-d_A。任何只读根与末位、只看静态菜单、或把浮点 `best=0` 当成全称安全值的路线均不足以关闭问题。

## 五、源与证据索引

九个冻结源版本均原样保存在 `archives/customer-attraction/tools/evidence/R-0f99797b33de46bfb498541a0bc5fae9/security/`，文件名为源 ID 加 `.raw`；manifest 记录首个冻结提交、路径、blob 和 SHA-256。`raw` 文件是 `clean show` 的完整输出，不是重写后的摘要。

