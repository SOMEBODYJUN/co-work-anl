# 门控归一化菜单的福利舍入、真实调度与 robust 参数互补：先冻结精确陈述

冻结日期：2026-10-18。作者身份：boss11 内部研究 subagent；本文件只给完整对象与 Exact，不给作者证明。作者完整证明将另存，不修改本文件以回填审查。所有文件均在 clone 外；未登记 Work、未发公屏/私聊、未改共同账本、未 git 写入。

## E1. 对象与显式正 support LP

令 G 为非空有限组集，n=|G|≥1；U 为有限资源集，m=|U|≥1。每组 g 有非空、有限、显式 indexed state 集 A_g，S=Σ_g|A_g|。每 state 有一个资源集合 U_gs⊆U（同 state 资源标识互异），每列出 incidence (g,s,u) 带二进制非负有理系数 p_gsu，且 Σ_{u∈U_gs}p_gsu=1。允许显式零系数、零 incidence、unused 资源、重复 indexed states。I=Σ_g,s|U_gs|。未列出的系数作零用于效用计算，但不据此生成物理 job。

对 B⊆U，定义 v_g(B)=max_{s∈A_g}Σ_{u∈B∩U_gs}p_gsu∈[0,1]。allocation 指真实的两两不交 B_g⊆U；资源可以未分配。每个输出的效用必须由一个原 indexed state 读出。

P_gs={u∈U_gs:p_gsu>0}。unit-FSLP 为明确有理可行性 LP：

  λ_gs≥0；Σ_sλ_gs=1（每组）；Σ_{g,s:u∈P_gs}λ_gs≤1（每资源）。

此 LP 有 S 个变量、n 个归一化等式和 m 个容量不等式，全部矩阵系数为 0/1；不以零 incidence 计占用。不调用机器 CONFIG 或指数配置 oracle。

## E2. 有限显式状态表的确定性福利输出

**Exact WELFARE。** 对每个 E1 输入，若 unit-FSLP 可行，则有确定性总位多项式算法，输出原 indexed states s_g 与真实不交原资源 bundles B_g，使

  Σ_g Σ_{u∈B_g∩U_g,s_g} p_g,s_g,u > (5/8)n。

同一输出取原效用 r_g=v_g(B_g)（并重新选择 attaining 原 state）后仍满足 Σ_g r_g>(5/8)n。算法可先求显式有理 LP；给一个合法有理 λ 时，其舍入部分仅用有理排序、加乘、比较与有限条件期望，不需随机位、输入值下界或数值展开。

更精确的存在性/同一算法保证为 Σ_g r_g≥(1−1/e)n；算法不以该无理数作数值比较，交付的保守有理保证为上式。该舍入机制是标准配置福利随机舍入的显式特化，不声明技术原创或全球新颖性。

**Exact COUNTS。** 对任意有理 0≤δ<5/8，同一输出的 h_≥(δ)=|{g:r_g≥δ}| 与 h_>(δ)=|{g:r_g>δ}| 均严格大于

  ((5/8−δ)/(1−δ)) n。

特别 δ=3/8 时 h_≥、h_> 均 >2n/5，因而 ≥ceil(3n/8)。严格号按真实整数计数解释，不假设任何比例整除。

## E3. 新的完整 ordinary-UM 门控矩阵

这是 E1 菜单的特定构造 P_gate；不把原 flat 实例悄悄改成门控实例。

机器：一台根 R；每组一台互异 gate X_g；每 indexed state 一台互异 private M_gs；每 resource 一台互异机器 Q_u。四类互异。总机器数 1+n+S+m。

全部原 jobs 恰为：

1. 根 pin J0，仅在 R 有限，时间 1。
2. 每组 connector C_g，恰 R 上时间 1/n、X_g 上时间 1。
3. 每组 selector T_g，恰 X_g 及本组全部 M_gs 上时间 1。
4. 每列出的 incidence 一件不同 job I_gsu，恰 M_gs 上时间 p_gsu、Q_u 上时间 1。含零 incidence jobs 与未选 states 的全部 jobs。

其他时间均为 ∞。作业不可分、无抢占、必须各执行一次。总 job 数 1+2n+I；有限资格数 1+3n+S+2I。dense 编码也只为这些显式量的固定多项式。

定义 balanced value

  β*=max( {0} ∪ { min(|H|/n, min_{g∈H}v_g(B_g)) : ∅≠H⊆G，B_g⊆U(g∈H) 两两不交 } )。

这是有限集合最优值定义，不提供免费求值 oracle。必有 0≤β*≤1。

**Exact VALUE。** 对每个 E1 输入（不要求 FSLP 可行），OPT(P_gate)=2−β*。给任何实际完整 P_gate 调度且峰 C<2，可确定性总位多项式提取一组 H、原 states 和不交原 bundles，满足 |H|/n≥2−C、每个 g∈H 的原质量≥2−C。给上述 H/bundles 的任意 β>0 见证（|H|/n≥β、全部质量≥β）可确定性总位多项式构造全部 jobs 峰≤2−β 的调度。β=0 有显式峰≤2完整调度；C≥2 的分支不误用 resource unit 独占。

**Exact SCHEDULE。** 若 E1 的 FSLP 可行，可确定性总位多项式输出 P_gate 的全部 jobs 调度，峰≤13/8。具体使用 E2 的 h_≥(3/8)>2n/5 个高质量 groups，故 β≥3/8；根、gate、所有未选 state、全部零 incidence、unused resource 同时满足容量。不仅报告 selected-root 数量。

本限定结构 pin 保证 OPT≥1，故在其 FSLP-feasible 子类内上述也是 13/8 近似。FSLP 不可行时不声明同一绝对峰或近似保证。此结果不解决原 flat 全组必须激活的菜单实例、一般 Santa Claus、一般 R||Cmax 或多层私有树。

## E4. 真正的有理 LP promise decider

固定有理 0≤δ<5/8 与 0<γ_hi≤(5/8−δ)/(1−δ)。对 E1 的完整显式输入考虑：

* YES：有不交 allocation，使全部 n 组原质量 1。
* NO_≥：每个不交 allocation 均有 |{g:v_g(B_g)≥δ}|<γ_hi n。

以 unit-FSLP 的有理可行为 YES 判据，不可行为 NO 判据，是确定性总位多项式 promise decider。NO 若将 ≥δ 改为 >δ，结论也成立，但应另按该精确阈值语义使用，不自动互换 source 定义。promise 外无保证。δ=0 时 NO_≥ 是空类，decider 的承诺仍按此退化解释。

特别，对所有固定 0<δ≤3/8、0<γ_hi≤δ，覆盖上述 promise；不依赖未证 SCHA、PCP 或其他困难性假设。若一个 NP-complete language 确定性 Karp-reduces 到这一完整 normalized promise，则 P=NP；若使用满足标准 YES/NO 成功事件的随机归约，则只可按实际合同推出 NP⊆BPP 等，不改成 P=NP。此页没有构造任何源归约。

等价的 P_gate 特定 promise：YES OPT=1；NO OPT>13/8，可由同一 LP 分离。它没有声称一般 UM 的这个 gap 可判。

## E5. robust 源参数与已有正文 §F 的精确纠错位置

原文路径：research/current/unrelated_machines/explicit_xos_fractional_nsw_and_normalized_robust_gap_boundary.md，§F 最后两段，从“本页 C–D 排除的却是”至“完全不能用此 bound 排除该区域”。旧冻结版本保持原字节。

该页 C–D 的 γ_bad 表示“每个 allocation 至少 γ_bad n 组低质量”；需求树 robust-bundle 源的 γ_hi 表示“禁止 ≥γ_hi n 组同时高质量”。同一个 symbol γ 在这两个命题中不代表同一数量。

准确集合互补：令 h=|{g:r_g≥δ}|，则

  h<γ_hi n  ⇔  |{g:r_g<δ}|>(1−γ_hi)n。

这不是“至少 γ_hi n 组低质量”。若高端使用 >δ，其互补为低端 ≤δ。strict 与 weak 边界必须分别写明。C–D 原来针对任意低质量 fraction 的定理与 (F.1) 本身并未因此被反驳；错在据此把 typical root regime γ_hi≤δ 认定为未覆盖。对 E1 的 normalized、FSLP-feasible 对象，该 regime 在充分小常数 δ 上反而被互补后的同一定理排除；E2–E4 以短的独立福利论证把有理阈值加强至上述范围。

不归一化、没有 E1 FSLP witness/可行性、隐式指数 states、only source-image 不保本 LP、未获 all-allocation NO、原 flat 所有 group selector 不门控、跨层一致性等不在该否定范围。此页不能用来否定所有 near-two source 或一般 UM-TARGET-v1。

## 冻结与有限证据边界

当前为数学 Exact-first 待独立攻击；完整作者证明另文件；所有新命题未外审、全球新颖性未认证。将另做 Fraction 条件期望与完整 P_gate 回算的有限核验；有限核验不会证明无限族或 LP 算法的通用实现。尚未执行/验证的内容不在本文件登记为完成。
