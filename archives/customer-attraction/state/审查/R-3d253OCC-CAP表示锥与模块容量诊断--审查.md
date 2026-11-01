---
id: customer-attraction/r3d253-occ-cap-representation-cone-and-module-capacity-review
kind: review
type_tag: 审查
title: R-3d253 OCC-CAP 表示锥与模块容量诊断审查
status: candidate-and-finite-attacks-reviewed
truth_status: unproved-occupancy-conjecture; no-certified-half-counterexample
review_level: full-source-read-with-program-quantifier-audit
scope: terminal occupancy capacity candidate, collision-free/prefix cone attacks, and static module-capacity diagnostic
source_refs:
  - source:c7971ea3de385864b543:research/workspaces/customer-attraction/R-3d2531ded15f453daef73b30eef82940/representation/README.md
  - source:be12bc369998443fd5e2:research/workspaces/customer-attraction/R-3d2531ded15f453daef73b30eef82940/representation/attack_collisionfree_extension.py
  - source:d9feb819abeae3c12174:research/workspaces/customer-attraction/R-3d2531ded15f453daef73b30eef82940/representation/attack_occupancy_bound.py
  - source:f504be79d5e0a07559fe:research/workspaces/customer-attraction/R-3d2531ded15f453daef73b30eef82940/representation/attack_prefix_cone.py
  - source:6348cb57cda58ef2cb27:research/workspaces/customer-attraction/R-3d2531ded15f453daef73b30eef82940/parent/module_capacity_probe.json
  - source:e61c14218bc09995b0b1:research/workspaces/customer-attraction/R-3d2531ded15f453daef73b30eef82940/workspace.json
---

# R-3d253 OCC-CAP 表示锥与模块容量诊断审查

## 1. 来源范围和主命题

本批四个 representation 文件提出并攻击一个比直接 half 更强的终局占用容量候选，另有 parent/module_capacity_probe.json 给出一个静态模块容量诊断，workspace.json 只记录工作区元数据。README 明确写出：目标仍是任意人数、任意有限共同目录、全部有序历史纯 SPE 的 Q-CAG-HALF；主目标 OPEN，有限攻击未找到反例不能当证明。

给定完整纯 SPE 的实际终局负载 c，记 W 为正负载主题数，候选 OCC-CAP 为：

    OPT_m ≤ W + E(c)
    E(c) = Σ_{x:c_x>0} c_x/(c_x+1)
         = Σ_{x:c_x>0} [1 − 1/(c_x+1)].

因为每个 c_x ≤ m，非零实例上若候选成立就有 OPT_m ≤ (2 − 1/(m+1))W，进而推出 W ≥ OPT_m/2。它是充分候选，不是已证定理，也不要求终局是静态 PNE。

E(c) 的解释是：对每位实际玩家各加一个自己的“额外复制查询”，将这些 m 个查询分别放入完整实际 m 槽背景时，收益总和为 E(c)。这只是等式描述，不能把 m 个静态查询同时加入原博弈。

## 2. 可直接证明的静态部分及动态缺口

固定 m 个合法比较主题 T_j，令 d_x 为 x 在这些比较主题中的客户重数，G(T)=Σ_{x∈T}1/(1+c_x)，B=Σ_j G(T_j)。逐客户有

    1_{d_x>0} ≤ (d_x+c_x)/(1+c_x),

从而

    |⋃_j T_j| ≤ B + E(c).

若终局满足静态 PNE，各玩家的合法静态偏离至少给出 G(T_i)，故 B≤Σ_i u_i=W，OCC-CAP 在静态 PNE 层面成立。完整历史 SPE 的偏离可改变后继，README 没有给出把这条静态比较转成统一 SPE 付款的步骤。

一般终局的精确松弛为：

    B + E(c) − |⋃_j T_j|
    = Σ_{c_x>0,d_x>0}(d_x−1)/(c_x+1)
      + Σ_{c_x>0,d_x=0} c_x/(c_x+1)
      + Σ_{c_x=0,d_x>0}(d_x−1).

因此不能逐比较元组强行要求 B≤W。README 的十四客户残余实例中，取同一未覆盖主题 T 两次得到 B=10>W=9；重复计数正是松弛项来源，但最优并集覆盖仍为10，远低于 OCC-CAP 右端13.5。更强的“m·max_T G(T)≤W”也被该例否定，不能因此改名为对 OCC-CAP 的反例。

## 3. 三个表示锥攻击的实际量词

### 3.1 occupancy_bound.py

attack_occupancy_bound.py 对一组完整策略种子做 discovery LP。每次随机生成 p 个主题、m 个提供者和全部非空客户类型，使用 ExactSPESolver 选一个以 OCC-CAP 右端为目标的完整终局，再固定该证书的全部历史 IC 行。随后在客户重数锥上，对每个 m 主题比较支持最大化并集覆盖。共 20 个小规模种子（p,m 在 (4,3)、(5,3)、(4,5)、(5,4)、(6,3) 间循环），未打印候选违反。

该程序使用 SciPy 浮点 linprog 做发现；若出现数值候选，才另行有理化、重建整数客户输入并逐有序历史核验。本源没有这样的候选输出，也没有把“20 次未见违反”当作普遍结论。

### 3.2 collisionfree_extension.py

该程序固定已知 k=2、m=3 的无拥挤完整策略证书，实际路径为目标索引 (2,5,6)，并允许全部 63 种与该无拥挤路径相容的非空客户类型。它枚举比较主题支持，保留证书的全部 IC 行，用线性规划优化客户锥；客户权重被归一化到实际路径主题上的占用基准。最大 OCC-CAP 比值为 8/9，没有发现大于 1 的支持。

这个数值只覆盖一份固定完整证书和一个相容类型锥，既不是一般无拥挤上界，也不是新固定人数定理。代码本身没有输出 exact SPE 证书升级或 half 反例。

### 3.3 prefix_cone.py

该程序沿已知近二前缀族，固定全部历史计数策略，允许八种客户轨道系数变化，显式枚举最优比较支持。对 m=4、5、6、7、8，最大 (OPT−OCC-CAP-RHS)/W 分别约为 −0.08636、−0.05476、−0.03782、−0.02768、−0.02114，均未违反候选。

README 记载开发中曾把“全目录联合”错误地当作允许额外 A-only/B-only 客户后的 m 主题比较联合，造成伪违反；修正为显式比较支持后伪违反消失，错误输出已删除。这个版本边界是本批重要独有信息：中间数值结果不得作为反例，后续复现必须检查支持集合量词。

## 4. 两个相容性族和多尾停界

README 只核代数而没有增加 SPE 证明：

* 实际无拥挤的 3/2 族有 W=2m、OPT=3m−1、c_x=1，OCC-CAP 右端为 3m，余项为 1；
* 全选大主题的锐 2−1/m 族有 m 名客户、负载 c_x=m，W=m、OPT=2m−1，右端为 2m−m/(m+1)，余项为 1/(m+1)。

两族都与 OCC-CAP 相容，不能证明候选。

源文还分析把无拥挤族的一位末端惩罚者换成 q 位的自然多尾构造。若早期实际选 X_i、偏离为 X_i∪Z_i，尾部用 q 个含 X_i 和不同奖金 Y_j 的目录稀释 Z_i，单看偏离者可使 |Z_i| 接近 q/(q+1)|X_i|；但是当每组提供相同奖金接口 B_{i,j}=X_i∪Y_j 时，末位保留唯一新 Y_j 并换到另一个旧组会以 |X_l|/2 超过 |X_i|/(q+1)，等组且 q>1 时严格盈利。该惩罚尾不是 SPE。若用实际多重覆盖阻止交换，则 E(c) 容量相应增加。这个失败机制只排除该自然构造，不排除非可替换奖金或跨型惩罚，也不证明 OCC-CAP。

## 5. parent 模块容量 JSON 的边界

module_capacity_probe.json 的 scope 明确写作“disjoint union extra-one candidate static module lower support diagnostic only”，max_competitor_slots=10，success=true。它给出三个浮点变量约 (0.25609756, 2.38617886, 9.80081301)，gap_over_root=0.13414634，并列出八个 active 线性约束：六个 slots=2 的两类三点计数、两个 slots=3 的全三点计数；常数为 247/24 或 113/12，slope_p 为 −23/12、3/2 或 −1/3。

这些字段只说明指定有限静态模块支持诊断中，某个 extra-one 根候选与活动约束之间存在正 gap；没有给出客户级完整策略、终局负载、全部历史 SPE IC 或可行的半覆盖反例。它和已有 R-3d253 静态模块/仿射证书对象相互补充：前者给具体容量探针边界，后者给静态局部身份和不交并下界。两者都不能把静态模块值升级成指定模块并目录下的完整 SPE。

workspace.json 只有 schema=1、save=customer-attraction、actor=R-3d2531ded15f453daef73b30eef82940、instance=c80b00f56b1e4556b33c3d180f86edd5；它是工作区协作元数据，不包含数学数据，保留其版本和身份信息但不另造数学结论。

## 6. 结论和接续义务

**已确认。** OCC-CAP 是一个足以推出 half 的终局容量候选；静态 PNE 层面有 B≤W 的代数接口；三个表示锥攻击在声明的有限策略/客户锥上未找到违反；prefix 攻击中的全目录联合伪违反已定位并修正；模块容量 JSON 是有限静态支持诊断。

**有限实验。** 三个 Python 文件使用 SciPy LP 或固定证书的数值检查；本批没有 exact 全局 LP 证书，也没有重新运行外部 solver。数值输出只能支持“未发现候选”的有限状态。

**障碍。** 从完整 SPE 的后继改变 IC 到统一 OCC-CAP 付款关系仍未闭合；不能把静态 PNE 不等式、LP 负 gap、或模块容量正 gap 当作完整历史结论；也不能把删除的全目录伪违反恢复为反例。

**未决。** 需要从完整有序历史 SPE 的真实偏离证人建立使用最优并集松弛、由 E(c) 支付遗漏客户的全局交换关系，或给出经过有理化和逐历史核验的 OCC-CAP 违反。当前对象因此归为 candidate + finite exploration + obstruction，Q-CAG-HALF 保持 OPEN。
