# Boss7：SUMmin 与均匀通用时间的精确身份比较

2026-11-16。独立实读以下四篇原文及三个现行 registry statement；当前正式比较由 Boss3 的 `boss3-uniform-summin-identity-3b-3313f41b4a46c9dc` 承接。本文件是数学审读，未冒作已交付的边或自动改变任一候选的 open 状态。

## 1. 逐列相等，全部量词保持

固定任意有限原模型输入、m≥1、一份所有有序历史有定义的完整纯 SPE σ、同一实际叶 z、原实际前缀和同一合法查询分布 p。固定 i 与合法防御动作 A 后，完整 m 槽 Z_i(A) 已由同一 σ 决定，独立于其后额外查询 T。有限求和给

    E_{T~p} K_i(T,A)
      = Σ_T p_T Σ_x 1[x∈cov(T)]/(1+c_x(Z_i(A)))
      = Σ_x q_x/(1+c_x(Z_i(A))) = G_p(Z_i(A)),
    q_x=Pr_{T~p}[x∈cov(T)].

因此在**相同的完整列集合**上取 min_A，逐点有 R_i(p)=ψ_i(p)。这不是交换 min 与期望；A 可依 i,p，却不依已抽样的 T。两候选的全位置和、W、输入、σ、p 的全称量词完全相同，所以它们的共同预算断言双向等价。纯 p 的 A=T 证明也相同。λ_i=1/m 是同一个均匀位置选择；这里不把另一个仅存在通用 λ 的自由菜单候选一起等同。

m=1、零客户、空覆盖、重复动作、同覆盖异标签、所有弱平局都由同一有限式覆盖；全分母为1+c≥1。未做标签商、计数策略限制或真实后继冻结。证明这个身份不证明一般预算的真假。

## 2. 两稿同名 L 的准确对照

下表用新下标只在本说明中消除重名，不建立新对象。均匀时间稿的 C 是完整槽推送，SUMmin 稿的 C_old 是删强制者的槽。

| 数学量 | SUMmin 原稿 | 均匀时间原稿 | 末两位储备原稿 |
| --- | --- | --- | --- |
| 真实强制收益均值 | D_i | D_i | D_i |
| 完整 m 槽独立额外查询均值 | C_i^full | C_i | P_i |
| 删 forced 槽的额外查询均值 | C_i^old | 非本稿同名 C_i | C_i |
| 真实 IC 松弛 | e_i=u_i−D_i | e_i | e_i |
| 完整槽均值降到自由最小列的收益 | 在 R_i≤C_i^full 中隐含 | L_i=C_i−ψ_i | G_i=P_i−ψ_i |
| 删 forced 槽带来的 extra-query 折扣 | L_i=C_i^old−C_i^full | 不是本稿 L_i | R_i=C_i−P_i |

故原 SUMmin 的 L_i 与均匀时间的 L_i **不是同一量**。前者含额外查询覆盖概率 q_x：

    Δ_i = E_{A~p} Σ_x q_x I_x/[c_x(c_x+1)],
    I_x=1[x∈cov(A)], c_x=c_x(Z_i(A)).

均匀时间协方差展开中的自身插入税是

    τ_i = Σ_x E_{A~p} I_x/[c_x(c_x+1)],

一般没有 q_x 因子。I_x=0 时含 I 的项约定为0；I_x=1 时 c_x≥1，不使用0/0。

记 Cov_i=Σ_x Cov_p(I_x,1/(1+c_x))，κ_i=D_i−C_i^old，G_i=C_i^full−R_i≥0，则两份精确账通过

    D_i−C_i^full = κ_i+Δ_i = Cov_i+τ_i

连接。因而

    Σ_i R_i−W
      = −Σ_i(e_i+κ_i+Δ_i+G_i)
      = Σ_i(−Cov_i−τ_i−e_i−G_i).

这逐点给协方差支付式与 SUMmin 原预算的双向等价。所有税、松弛与重选收益使用同一个 σ、实际前缀和 p；同名符号不能跨稿直接替换，非负税也不自动支付全部有符号 κ 或 Cov。

## 3. 已付款尾部怎样沿身份供 SUMmin 使用

对 m≥2，现行 proved 的末两位资源给

    P_{m−1}=u_{m−1}−e_{m−1}−L_res−V−Q,
    ψ_m≤u_m−e_m−max(V_m,R_m^actual).

由于 ψ_{m−1}≤P_{m−1} 且 R_i=ψ_i，这些同一真实前缀上的准确尾部付款可以被 SUMmin 路线直接消费。L_res 是末位真实最佳回复比较的非负均值，又不同于上一表中的两个 L。最后的两份储备必须取 max，不能相加。原资源还给精确的早期债恒等式；一般 i≤m−2 的共同付款仍未证。

本比较没有新运行 LP、SPE 枚举或有限证书，也没有给一般 SUMmin/六人 half 新证明。等价关系若用于候选互通，应双向完整保留上述模型/量词；尾部若另外写边，应仅列已经完成的局部贡献及早期 remaining。

## 4. 实读证据

- `archives/customer-attraction/state/候选/全槽逐行最小价格的共同预算与有限报告--候选.md`；全文；SHA256 `e952c73849b2ac561ac4ebb761b3ae0c1af06d61f27e743c593ea0103c52698a`。
- `archives/customer-attraction/state/候选/均匀通用时间的完整前缀菜单与关联预算--候选.md`；全文；SHA256 `9f321cd13380ffabb302dd18b17028dfc7eb444c001b29b2b09056bc23164c81`。
- `archives/customer-attraction/state/资源/完整终局推送的自身折扣与末两位储备--资源.md`；全文；SHA256 `b35f22d2e7a802f8b4aa87f503bfe2690273a37bc414932d428d3ad728954bfa`。
- `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md`；全文；SHA256 `cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88`。
