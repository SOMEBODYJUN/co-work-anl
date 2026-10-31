# 任意归一化加权门控菜单的完整 13/8 近似：作者证明 v2

日期：2026-10-18。先冻结 Exact 是 [gated_weighted_menu_general_ratio_exact_v2.md](gated_weighted_menu_general_ratio_exact_v2.md)，SHA256 `4dd1cff4786ffbccda5ee1bdedc18a34ba9b5c6408829c57e70ba4f92609c04a`。本 Proof 晚于该 Exact，不修改冻结 Exact 或 v1。当前作者证明完整；独立攻击、作者读后审查、外审、新颖性另记，不提前登记。

## 1. 来源扣除、完整模型与范围

DNS（Dobzinski–Nisan–Schapira）作者稿 [cfjournal.pdf](https://www.cs.yale.edu/homes/schapira/cfjournal.pdf) §3.2、PDF8–9 的 Theorem3.2/Lemma3.3 已实际文本核读。它已有独立选配置、取 attaining additive clause、每 item 给最大系数的机制，且给更强有限 n 因子 1−(1−1/n)^n。Feige [SIAM2009 官方原始摘要](https://epubs.siam.org/doi/10.1137/070680977) 也明确给 XOS 的 1−1/e 福利比例。本页不认领这些机制、常数或标准条件期望。为避免免费 oracle 和对外部证明状态的误读，下面在有限显式菜单上自足写出其需要的 LP 与有理特化。新增研究用途仅是 ordinary gated 全作业桥、weighted 未知 OPT 结构结论及 γ 互补纠错。

对象沿先冻 Exact 全域：n≥1 个 groups、m≥1 个 resources；每组非空显式 indexed states，每 state 非负二进制有理 p_gsu 且 Σ_up_gsu=1；同 state 资源标识互异。允许 zero/unused/重复 states，全部表大小 S、全部列出 incidence I、正 incidence I_+。未列权重作零，不据此添物理 job。原效用 v_g(B)=max_sΣ_{u∈B}p_gsu∈[0,1]。

W*=max 不交 bundles Σ_gv_g(B_g)。β*=max_{H≠∅,不交B}min(|H|/n,min_{g∈H}v_g(B_g))，并包含候选零。这两个有限最优值只用于分析，算法不输入它们。

普通矩阵 P_gate 恰有根 R、每组 gate X_g、每 state private M_gs、每资源 Q_u，四类互异；pin J0 仅 R 时间1；connector C_g 在 R 时间1/n、X_g时间1；selector T_g 在 X_g 与本组所有 M_gs时间1；每列 incidence I_gsu 在 M_gs时间p、Q_u时间1，含全部零 job。其余∞，没有其它 job、side constraint、预载或拒绝。机器数1+n+S+m，jobs数1+2n+I，有限端数1+3n+S+2I。

## 2. 一份明确多项式福利 LP

对每 state 设 z_gs≥0，对每 positive incidence 设 x_gsu≥0；零 incidence x 固定零，物理 job 仍保留。约束与目标为

  Σ_sz_gs=1；x_gsu≤z_gs；Σ_g,s x_gsu≤1（每资源）；
  maximize L=Σ_g,s,u p_gsu x_gsu。                                  (7)

这是 S+I_+ 个变量、n 个等式、I_+ 个链接及 m 个资源不等式的有理 LP，非指数列枚举。任意逐组选一个 state 并取 x=0 即可行；非负目标。x≤z 与 norm1 给每组目标贡献≤Σ_sz_gsΣ_up_gsu=1，故 L≤n。

给任何原 allocation，逐组选 attaining state s_g，置 z_g,s_g=1，并对本组收到、在该 state 正系数的资源置 x=1，其他为零。bundles 不交保资源约束，目标恰为原福利。因此最优 LP 值满足

  W*≤L≤n。                                                        (8)

在当前非空 norm1 域有某正系数，可仅给它一个 x=1 而其它组 x=0，故 L>0；写明 L=0 分支仍便于复用舍入接口。

有理 LP 标准确定性位多项式算法给一个多项式位长最优解。本文没有把数值求解器当通用精确 LP 实现；第9节有限实现用数值候选、再由 Fraction 检查完整原对偶可行与等目标，认证的只是所列有限 LP。

## 3. 先选状态、再提议资源的概念分布

各组相互独立按 z_gs 抽一个原 state s。z_gs=0 不抽到，且 x_gsu=0，无 0/0。给抽到的 s，对该 state 每个正 incidence 独立以 θ_gsu=x_gsu/z_gs∈[0,1] 提议其资源 u；组内所有这些 coins 可条件独立，组间全部独立。

对每资源 u，把它交给提议者中原系数 p_g,s_g,u 最大的一组；没有正提议则留未分配；平局按固定组号。不管发生多少提议，资源仍只给一个真实组。每组赢家的 bundle 在它抽到的 state 上的质量可真实读取；取原效用 max 只会更大。

固定 u，令 X_gu 为组 g 提议时的 p_g,s_g,u，否则零。各组 X_gu 独立，且

  Pr[X_gu=p 所对应的 state s 事件]=z_gs(x_gsu/z_gs)=x_gsu。

相同 p 的 states 只是相应事件概率相加。对 t>0，q_gu(t)=Pr[X_gu≥t]=Σ_{s:p_gsu≥t}x_gsu，故 LP 的真实 resource row 给 Σ_gq_gu(t)≤Σ_g,sx_gsu≤1。由

  1−∏_g(1−q_gu(t))≥1−exp(−Σ_gq_gu(t))
                        ≥(1−1/e)Σ_gq_gu(t)

及有限 tail 求和，有

  E[max_gX_gu]≥(1−1/e)Σ_g,s p_gsu x_gsu。

因此可实现的赢家总质量 A 满足

  E[A]≥(1−1/e)L>(5/8)L（L>0）。                                    (9)

这里的 resource claim 概率是 x，不是 z、也不是 p*x；无需所有 positive supports 同时可打包。这个差别正是从 v1 FSLP 可行类扩到整个 gated 类的来源。

## 4. 两阶段精确有理条件期望，含每一枚非平凡 coin

固定全部原不同正系数 levels 0=a_u0<a_u1<⋯<a_uk。给当前条件事件，写 Q_gu(a)=Pr[X_gu≥a|当前]；未固定组贡献

  Q_gu(a)=Σ_{s:p_gsu≥a}x_gsu。

组已固定为 state s，但该 resource coin 未固定时，贡献为 1[p_gsu≥a] x_gsu/z_gs；coin 已固定为 b∈{0,1} 时贡献为 1[p_gsu≥a]b。零 incidence 永远不提议。不同组仍独立，故当前有理条件期望恰为

  E_current[A]=Σ_uΣ_l(a_ul−a_u,l−1)
                   [1−∏_g(1−Q_gu(a_ul))]。                         (10)

**状态阶段。** 逐个未固定组 g，仅测试 z_gs>0 的原 states。把 g 固定为候选 s 后按 (10) 精确算值。当前期望是这些候选值按 z_gs 加权的平均，因为每个 resource 上 z_gs·(x_gsu/z_gs)=x_gsu；故选最大候选不降。不同资源间共享同一 state 的相关性不破坏公式：总目标是各资源贡献的和，而每个资源乘积只跨 groups。没有把同一组在不同资源上的 state 分开选择。

**coin 阶段。** 全部 states 已固定，再逐项处理实际选中 state 的每个 positive incidence。若 θ=0 或1直接固定对应值，不算 0/0；否则分别精确算 E0、E1。当前值是 (1−θ)E0+θE1，故选大者不降。至多 I_+ 枚 coin 决策，未选 states 的 coins 无需展开；它们的所有物理 incidence jobs 仍在后续执行。

最后所有提议固定，按最大原系数为每资源定唯一赢家，得到真实 bundles B_g，其 selected-state 质量和等于最后 A。遍历原 indexed states重新选 attaining state，得 r_g=v_g(B_g)、W=Σ_gr_g≥A。由 (9) 有

  W≥(1−1/e)L，L>0⇒W>(5/8)L。                                    (11)

不需要枚举某 state 的所有资源子集，不生成隐式配置列表，不比较 e 或 sqrt。

### 有理运算位长与操作数

每资源 level 个数≤其显式 positive incidence 数，全部 level 数≤I_+。每次 (10) 扫有限原表、levels 和 groups，操作数多项式。状态候选总数≤S，coin 候选总数≤2I_+。

LP 解 z,x 有输入长度多项式位数；每个 θ=x/z 的位长也是多项式。取所有原 p 分母、全部 LP 解分母、所有可能的正 z 对应 θ 分母之积为公共 D；总条目数是多项式，因此 log D 是这些位数之和，仍为输入长度多项式。每个 Q 的分母整除这个 D 的对应组/项因子；(10) 只跨不同 groups 乘一次，并将有限 levels 差作为系数，完整表达式分母可界为上述输入因子的固定多项式次幂乘积。不存在重复平方递推；每个当前期望直接从原 z,x 和已固定状态重算。其值在 [0,n]，故分子也有多项式位长。精确约分、排序、比较以及最终负载回算均为位多项式。

## 5. 排序得到不丢实际资源的 balanced witness

给任意实际 allocation 的 r_g∈[0,1]，排序 r_(1)≥⋯≥r_(n)，置

  b=max_{1≤k≤n}min(k/n,r_(k))，另允许零。

扫描 n 个有理候选取达到的 k，即得 H 为前 k 个组、同一原 bundles，不变资源身份；|H|/n≥b、min_Hr≥b。

令 h=# {g:r_g>b}。若 h/n>b，则 k=h 同时满足 k/n>b、r_(k)>b，会使候选严格大于 b，矛盾。故 h≤bn。其余组≤b，高组至多一，因而

  W≤h+(n−h)b≤bn+(n−bn)b=n(2b−b²)。                                (12)

0≤b≤1 给

  b≥1−sqrt(1−W/n)。                                                (13)

这只是分析。算法实际只计算原有理 k/n 与 r_(k)。不需要 n·b 整数，h≤n·b 是普通实数不等式；h 的整数性不导致漏掉 ceil 分支。

另一方面，β* 的某个有限 witness H*,B* 达到最优；其 |H*|≥nβ*，每个选中质量≥β*。把未选组给空 bundle 后是全组真实 allocation，故

  W*≥|H*|β*≥n(β*)²。                                              (14)

β*=0 时 (14) 平凡，不求空集合最小值。

## 6. 完整普通 jobs 的双向值恒等

为保证 v2 自足，再给 P_gate 的全部映射。给 H,bundles 与 b=min(|H|/n,min_Hquality)>0：pin 在R；选中 C_g 在X_g、T_g在其 attaining M_gs，未选 C_g在R、T_g在X_g；只有选中 state 的 allocated positive incidences 导出到其 Q_u，其余全部 incidence（含未选 states 和零 jobs）留各自 private。每 job 恰执行一次。

根负载2−|H|/n；每 gate恰一件unit；未选 state负载1；选中state负载2−quality；每resource最多一unit。故完整峰≤2−b。b0用pin+全部connectors在R的峰二基线，其他selector在gate，全部incidence私有。总数及全部有限端就是第1节所列，没有只执行 selected subinstance。

反向给任意完整 C<2 调度，H取 connector真正到gate的groups。根负载精确2−|H|/n≤C，故|H|/n≥2−C>0。每选中gate已有connector unit，selector不得同机，必须在某本组原state根上；该根真实负载2−导出原质量≤C。每resource只收unit，C<2使全局至多一件，故选中state实际导出原资源两两不交、每个质量≥2−C。未选state或未激活组的额外外送只可忽略，不能凭空复用资源。C≥2时仅用 β*≥0，不调用独占。

因此

  OPT(P_gate)=2−β*∈[1,2]。                                         (15)

这些双向转换仅需原 jobs 与原有理负载求和。非抢占的机器串行时序也可按固定 job 编号以有理前缀和输出，不改变 makespan 或位长。

## 7. 不输入未知 OPT 的 13/8 证明

算法依次求 (7) 的有理最优解、执行第4节去随机化、取原实际效用、按第5节扫有理断点、按第6节排全部 jobs。它不输入 β*、W*、原最优调度或 YES 证书。

由 (8)、(11)、(14)，W≥(5/8)n(β*)²；结合 (13) 得完整输出

  C≤2−b≤1+sqrt(1−(5/8)(β*)²)。                                   (16)

设 β=β*∈[0,1]。D=(13/8)(2−β)−1=(18−13β)/8≥5/8>0，且

  D²−[1−(5/8)β²]=(209β²−468β+260)/64。                            (17)

二次式在[0,1]导数418β−468≤−50<0，故最小在β1，值恰1/64>0。D与根号均非负，因此

  1+sqrt(1−(5/8)β²)<(13/8)(2−β)。

结合 (15)–(16) 给 C≤(13/8)OPT。声明用≤，不把分析余量当锐性。β0/1、n1、零系数、unused资源都已在各步骤覆盖；本对象始终有pin，OPT0不属于本域。

原福利比例还能给更精细常数，但本页不需要它，不声明13/8锐。其余步骤均原有理数计算；(16)–(17)的sqrt只用于证明，不进入算法。

## 8. 对 near-two 源与参数比较的真实结论

此定理只说明本页**整个完整 gated 类**已有统一次二算法。因此若某源归约的实际输出全落此类，并给可计算 YES绝对阈值 a>0、NO阈值 b且 b>(13/8)a，则比较实际输出峰与(13/8)a已分离该 promise。不能把未知OPT交给decoder作输入。YES≤1+η、NO≥2−δ时，足够条件为(13/8)(1+η)<2−δ。

这限制一个明确编译器/源接口；不是一般UM存在13/8算法，更不是一般UM不存在任何(2−ε)算法。flat所有组必须激活、未归一化states、多层私有树、隐式指数菜单、不保全部原jobs、只对固定label/完整束NO均不在当前证明范围。

v1 unit-FSLP为positive-support λ，置z=λ、每positive incidence x=λ给L=n；故v1的绝对峰≤13/8及LP promise decider保留。它不需要v2未知OPT分析；v2也没有删除v1的精确源量词。

原正文§F的 γ 互补错误：robust NO若要求全部allocation的h_≥δ<γ_hi n，则其低质量组数是low_<δ=n−h_≥δ>(1−γ_hi)n；不是至少γ_hi n。若高端用>δ，互补低端则≤δ。旧C–D的γ_bad与源的γ_hi是不同、互补参数；最后把δ≤c_eta<eta<γ_bad与γ_hi≤δ直接说“不覆盖”不成立。C–D自身和(F.1)按其低质量参数解释可仍正确。v1已经给不依赖NSW的精确有理LP判别，本v2进一步关闭整个gated类的ratio，但不把任何配置gap称困难性。

## 9. 实际有限核验、未完成项及可信边界

实现：[gated_menu_fraction_audit.py](gated_menu_fraction_audit.py)，本次输出 [gated_menu_fraction_audit_run_v2.json](gated_menu_fraction_audit_run_v2.json)。所有随机输入使用固定seed20261018；每条数学不等式、概率恒等、bundles不交、job合法端和逐机负载都用Fraction。数值LP只提出候选，逐案导出有理primal、dual_ub、dual_eq并精确验证非负、约束、stationarity及同目标；这给该有限LP的精确最优证书，不认证scipy是通用bit-poly solver。

本次实际范围：36个已知FSLP证书的归一化样例（n1..4,m=n..n+2,K1..3），核support期望公式等于全选态枚举、条件期望不降、strict count及全部jobs13/8；72个任意加权显式样例（n1..3,m1..5,K1..3），每个福利LP精确原对偶最优认证，全部资源分配穷举核W*/β*与结构ratio，其中2个LP最优点有非平凡fractional state。该72组basic optima未覆盖非平凡incidence coin，故另添3个明确非basic但同最优值的LP证书（n,m分别(2,1),(3,2),(4,3)），实际20枚非平凡coin决策全部核平均恒等及去随机化不降。另12个n1..2,m1..2,K1..2实例直接枚举/合法incumbent剪枝所有普通jobs调度，核OPT=2−β*。

原首次输出仅72组basic LP，未有非平凡coin；原code与原run保留为 `gated_menu_fraction_audit_initial_no_coins.py` / `gated_menu_fraction_audit_run.json`，不回填成已覆盖coin。当前输出保存完整menus与有理LP证书。观测最大ratio153/130只是有限数值，不用于论证13/8。1025点的ratio多项式grid仅辅助；一般正确性来自(17)的解析单调证明。

负控：两组各只有一个state、共同一个资源、private权均1，原flat OPT2，当前gated OPT3/2；说明门控构造确实改变问题，不能冒称保flat最优值的normalform。所有列出的零incidence都作为真实jobs保留在审计矩阵中。

未实现通用有理LP生产后端；未运行第二套独立代码；未有实际独立Exact-first攻击或作者读后复核；未外审或认证全球新颖性。以上状态与本文完整范围证明、有限实验、源困难性分别登记。没有写共同账本，没有git写入或push。
