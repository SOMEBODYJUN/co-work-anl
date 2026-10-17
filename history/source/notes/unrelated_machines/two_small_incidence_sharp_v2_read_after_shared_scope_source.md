# 两条 small 资格锐三半合同：root 冻结证明读后审查

对象 Exact：`UM-TWO-SMALL-INCIDENCE-SHARP-APPROXIMATION-v2`，SHA256 `051148816053f0c150ee70c9efa1b3f7cb76ecc46b999d793155b4070e3cd065`。

本次实际全文读取 root proof：`/workspace/scratch/038d9dcc4cac/two_small_incidence_sharp_approximation_v2_root_frozen_proof.md`，逐字计算 SHA256 `63da068c732421f76efa84cac37ad15d3e6fd24cc86af605403a344eadaf809a`，与交付一致。

来源分层：本人此前只看 Exact，独立得到 max-flow 局部容量表及 `deg(z)-1` unit-job 的3DM归约，已冻结 `/workspace/scratch/038d9dcc4cac/two_small_review/two_small_incidence_sharp_v2_exact_first_review.md`，SHA `d2fbd514316482e7a0c40a035ed65bcc1a909bda584fcb17da29d95b03e67705`。之后才获准读取本 root proof；本次为 READ-AFTER，不倒写旧审查来源。root 本文使用 CONFIG/ordered slots 与 per-A-selector 3DM，不是我先前的容量表与按 z 留空位的归约。本次不读取作者尚未交付的原稿，也未读取其它审查。

**结论：Exact 四项合同及本冻结证明全部数学主链无 standing fatal。没有生产实现认证，不重复运行已过 probe；新颖性与独立论文价值未认证。**

## 1. CONFIG 枚举与有理位复杂度

零任务剥离保存 OPT，回填覆盖全部原 job。对 b<=T<2b，每配置最多一枚时间 b 的资格以及至多两枚 small 资格，至多3 job；即使一个原 job 在其它机器有不同时间或许多资格，原身份覆盖约束仍是一条。按真实 unit job 和 small 子集显式列出配置，O(sum_i(1+|U_i|)) 变量，且所有长度和与 T 的比较位长多项式。每行有空配置，机器配置和1不造成额外假设。

可行有理 LP 选一份位长多项式可行点，边际和、切槽端点和排序均位长多项式。原 job 对 slots 的分数 matching 保每 job 需求1、每 slot 容量1；整数匹配还原真实 finite 端不会产生新资格。unit 边际总数<=1，故所有 unit 片段只位于第1槽（端点重合采用正长度交叠，不产生第2槽 unit 边）。

## 2. 负载分段闭合

- Q_i>2 时，因为 CONFIG 数量的期望超过2，必有一个正权重3-job配置。该行原本只有两枚 small 资格，所以这恰是一 unit 加这两 small，得到 p+q<=a。全行可能被圆整的不同 jobs 无论具体匹配如何，至多一 unit 加这两 small，实际负载<=b+p+q<=T。
- Q_i<=2 时至多两 slots。big 定义为所有 unit 加所有 small p>b/2+a。任一合法 CONFIG 中 big 至多一枚：unit+unit 超 T，unit+该 small 超 T，两个该 small 之和>b+2a>=T。big 的边际总量<=1，且在降序顺序中在前，所以只在第1槽，实际至多一个 big。
- 有 big 的行：其它被选 job 是 small 且 p<=min(b,b/2+a)，因此<=3b/2+a。无 big 的两 small：a<=b/2 时用 b+2a<=3b/2+a；a>=b/2 时用 2b<=3b/2+a。只有0/1 job 也满足。

这些论证用的是每行全部资格至多两枚 small；没有误用每行最终只接两枚小任务，也没有免费合并 unit job 身份。

## 3. 全 OPT 包装

OPT<b 的 exact 匹配、有限 O(m) 临界值与零/空分支正确。b<=T<2b 的配置变化只在显式原行子集负载处发生，外加端点 b；从该有限集选最小 CONFIG 可行阈值是确定性有理多项式运算。若真实 OPT<2b，阈值不超过 OPT；若 OPT>=2b 但 LP 提前可行，仍有阈值<2b<=OPT，所以输出同样合格。

若整个半开区间没有 CONFIG 可行阈值，则真实 OPT>=2b。assignment-load LP 的 L<=OPT，target=max(2b,L)<=OPT。对其边际做有序槽时，第 k>=2 槽匹配的值不大于前一完整槽的平均值；各前槽互异，故它们对最终负载的总贡献不超过分数负载 L。首槽额外最多 b。全行<=target+b<=1.5target<=1.5OPT。这里 target 本身不必是 LP 最小目标，仍可用原 L 的解，因为其负载<=target。

slot 总数<=n+m，所有稀疏 matching 规模多项式；p 的极大分母只增加有理编码长度。实际没有 b 资格、b 是松上界、所有任务可零、空任务、只有单机都未遗漏。此全区间证明与本人 Exact-first 中一般 ell 的容量包络是独立方法；不将后者扩为新 Claim。

## 4. root 的3DM构造

每 A 点一枚 unit selector，其 triple roots 为全部有限端；每 triple root 两枚 leaf jobs 在根时间1/2、分别在 B/C resource 时间1。每 root 恰两枚 small，其余资源全 unit；leaf job 两种时间，selector 一种时间。A 的孤立元素先走合法常量 NO；若 B/C 有孤立元素，不处理也不造成非法 job：该 resource 可为空机器，而反向 pigeonhole 仍正确排除 C<1.5。

完备调度覆盖全部 E 的两 leaf jobs，包括未选 triple roots（它们两枚全父置，根负载1）。每 A 恰选择一 root，所选 root 的两 leaf 外送；perfect matching 保资源 unit 不撞。反向任意 C<1.5 调度使每 A selector 所在根的两 leaf 必外送，并在 B/C 端两 unit 不能共机，于是正好得到覆盖全部三坐标的 q triples。不假定未选根无 leaf 外送，这些额外外送只会减少可用资源，不破反向。NO 因而所有真实调度>=1.5；非空 YES 实际 OPT=1 有 selector 下界。

这是本人现在实际读后核验的 root 第二套归约，不把本人先前另一套独立归约认证成此证明的盲审。标准3DM源已在旧审查亲读 Karp 原文重印的主定理与定义，本次不重复。

## 5. 读后核对2018 prior：范围和可直接复用之处

本次另实际联网读取作者 accepted 版：Page–Solis-Oba–Maack, *Makespan Minimization on Unrelated Parallel Machines with Simple Job-Intersection Structure and Bounded Job Assignments*, COCOA2018；§6 / Fig.5 / Theorem2，PDF页9–11。地址：<https://drpage.pagewizardgames.com/COCOA2018_dpage_solis_maack_accepted.pdf>。此处是后来检索，不能倒记为本人 Exact-first 的来源。

该定理字面覆盖“全部 eligible<=2/3/4”并分别给 exact/3/2/5/3；图5的 big-buffer 只容纳一个 big job，但 big 集本身可有任意多个原身份。本文 common-b 类不字面落在 eligible<=3 中，但将每行至多两枚非单位资格代入其计划，很容易得到所需三半推广；因此不能称新的算法机制。

为清楚说明“直接复用”而不偷换定理范围，给出读后自行核出的实例化：对 b<=T<2b，按该文规则把时间<=T/2 的资格记为 S，其余记为 B。所有 unit b 均属 B，故 |S|<=2；B 的每条时间<=b。更关键地，若 |S|=2，原两枚非单位资格已全在 S 内，所以此时 B 中所有资格都恰为共同 b；若原两枚非单位资格之一升入 threshold-big，则 |S| 至多1。始终用 big-buffer 容量1。如果 |S|<=1，允许总基数至多 |S|+1，负载<=b+T/2。若 |S|=2 且 b+sum(S)<=T，允许总基数3，实际<=T；否则允许总基数2，此时 B 全为共同 b，任何真实 T 配置确实不可能含一 big 加两 small，故全部原可行配置都包含在计划内，实际仍<=max(T,b+T/2)。这完全使用其图5形式，并给<=1.5T，事实上也<=3b/2+a。T<b 时删除 unit 后的 two-eligible exact 部分同样已有原定理对应。大阈值 ordered-slot 加 b 是经典工具。

此实例化仅限本 Exact 的共同 unit b 域。不声称任意多种 big 时间都可直接扩域：若两 threshold-small 与不同时间 big r1<r2 共存，用最大 r2 的总和选 d2 可能错误删除 r1 加两 small 的真实配置；该行通常已有三条低于共同 b 的资格而超出本域。

这些内容只评估本次算法与已有框架重叠，未断言2018文章已逐字写出本 Exact 全域，未断言某个完整原命题文献中从未出现。下界是否已在其它经典证明中同型出现也不认证新颖性。root §7 的审慎说明没有数学 fatal；正式文字宜把“很可能直接导出”改成经上述局部实例化已确认可复用，而不是让读者误会尚不清楚算法机制是否已有。

## 6. 限定结论

本结构类的实际三半算法与 P!=NP 下锐因子被核实。一般 UM-TARGET-v1 的存在/反面均未因此升级。特别本稿不将结构类算法解释成一般统一离二算法，也不把3/2困难性解释成排除所有2-epsilon。
