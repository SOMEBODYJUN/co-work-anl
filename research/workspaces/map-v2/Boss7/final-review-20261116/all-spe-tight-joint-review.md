# Boss7：两组正编译反族的全 SPE 紧预算联合审读

审读身份：Boss7。日期：2026-11-16。仅作窄范围 3D 数学审读；未运行 Git、sync、claim、done、board、checkpoint，未编辑正式边、收据或 canonical。唯一写入文件为本稿。

**结论：Boss5 plan 所述全策略扩张及 tight 查询最大值在数学上成立。** 对源正文固定的两组势、原 `2n` 标签、`K=6M+4` 正整数单位客户输入，结论覆盖**同一输入的每份完整有序历史纯 SPE**、每个共同查询分布 `p`：

\[
\max_{a\in P}Q_a(z)=K\beta_n-F(Z),\qquad
\sum_{i=1}^nR_i(p)\le n\bigl(K\beta_n-F(Z)\bigr)
\le nK\beta_n<W(\sigma).
\]

这里 `z` 是该份 `σ` 自己的 actual 有序叶，`Z` 为其标签集合；不同 `σ` 不必共用 actual 路径或相同福利。一般输入的 SUMmin-full `(U?)` 和无条件恰六人 half 均仍 open。本结果没有声称 `ΣR` 的精确最优值等于 `nKβ_n`。

## 1. 输入身份、计划与实际落盘边界

实读计划：`research/workspaces/map-v2/Boss5/finalization-20261116/summin-all-spe-plan.json`。拟任务 ID 为 `boss5-summin-all-spe-3b-7383c8bf44f753cc`，stage `3B`，三个端点与计划 pins 为：

|端点|当前版本 / truth|计划 registration pin|
|---|---|---|
|`CA-AGGREGATE-LAST-FLOOR-NO`（A）|v2 / proved|`699ba4cd7ebf119cdeb83f960aa4519f05068694f6f8507893ff071f155045ed`|
|`CA-MOBIUS-FULL-HISTORY-EMBED`（M2）|v1 / proved|`42694a561f1d7d9687fce7fe834aa833e5fa2d8b5b7d84eb1bf54115e118d09a`|
|`customer-attraction/e7-summin-full-common-budget-exact-discount-and-finite-tests`|v2 / open|`e37e6d0b6d0236152b44c5bd1d840157a5f2673bfcf99f9170af932a33e87332`|

已从当前 registry 仅抽出并实读这三个完整 object 记录，模型、量词和 body SHA 与计划相容。没有把读取 JSON 的技术解析称作全文审读整个 registry。

本稿收束前检查的本地状态：`research/operations/map-v2/tasks/boss5-summin-all-spe-3b-7383c8bf44f753cc.json`、同 ID 的正式边目录与正式收据路径均未落盘。因此本稿核的是**实际计划与源数学**，不声称该任务已经发布、领取、完成或新正式边已通过核验；也未推断远端状态。正式边落盘后还须逐字核它是否准确保留下述量词、ALL 前提和 contribution 范围。

## 2. 从 M2 的 `4M+1` 到此输入的 `6M+4`

固定整数 `n≥3`，标签 `P=X⊔Y`，两组各有 `n` 个标签。A 正文给

\[
F(S)=\begin{cases}
1,&|S|=n\text{ 且纯组},\\
-1,&|S|=n-1\text{ 且混合},\\
0,&\text{其他},
\end{cases}
\quad M=\sum_{B\ne\varnothing}|x_B|,
\quad K=6M+4,
\quad r_B=x_B+K.
\]

`x_B` 是源给出的整数调和反演，满足 `Σ_B x_B H_|B∩S|=F(S)`。本例不另清分母，`D=1`；全部 `r_B≥1`，展开为不同单位客户是合法原模型。

M2 正式陈述采用 `K₀=4M+1`，这里显式检查其证明对更大 `K` 的延续，而不偷换输入：在任一有序前缀，按剩余深度归纳，给定任意动作后的**真实孩子 SPE**，归纳假设使其后继全部选 fresh。比较 fresh 当前动作与过去出现 `v≥1` 次的 old 动作，均匀全类型偏置可通过未用标签置换对齐后继；signed 部分不置换。偏置差至少

\[
\sum_{C\subseteq P\setminus\{a,b\}}
\left(\frac1{1+s_C}-\frac1{1+v+s_C}\right)\ge\frac12,
\]

signed 收益差至少 `−2M`。故 `K₀` 时差至少 `1/2`，本输入则至少

\[
K/2-2M=M+2>0.
\]

基础末层与归纳各层均严格排除 old；未用标签数足够，因为 `2n≥n`。这覆盖**全部有序历史，包括已重复的离轨历史、任意真实孩子 SPE 和任意平局选择**，没有把策略压成计数函数。fresh 与 fresh 的均匀偏置相同，乘上更大 `K` 仍相同，所以 M2 的辅助投影及重复子树扩展论证也保留。特别地，每份原完整 SPE 的 actual `z` 都有 `n` 个不同标签；无须假定它投影为 A 展示的那一份辅助策略。

## 3. 任意 `n` 标签集合的 signed 福利

令 `Z⊂P`、`|Z|=n`，暂不要求来自 SPE。对每个 `a∈Z`，signed 真实玩家收益为 `F(Z)−F(Z\{a})`。

* 若 `Z` 为纯组，`F(Z)=1`、所有删除集值为零，每人收益 1，总和为 `n`。
* 若 `Z` 为混合，`F(Z)=0`；`a` 所在组在 `Z` 中至少有两名时，删除后仍混合，收益为 1；若 `a` 是其组唯一成员，删除后为纯组的 `n−1` 集合，收益为 0。

因 `n≥3`，两组不可能同时各只有一名。因此混合总 signed 收益为 `n` 或 `n−1`，总有

\[
w_x(Z)=\sum_{a\in Z}[F(Z)-F(Z\setminus\{a\})]\ge n-1.
\]

signed 收益守恒给同一个 signed 覆盖。全部非空类型中与 `Z` 相交的类型数为

\[
C=2^{2n}-2^n,
\]

故任意完整 SPE 的 actual 福利满足

\[
W(\sigma)=KC+w_x(Z)\ge KC+n-1.
\]

`W=KC+n−1` 是源展示的“一 X、`n−1` Y”策略的精确式，**不能当作所有完整 SPE 的等式**；以上普遍下界完全不需要该假设。

## 4. 任意 distinct actual 叶的 tight 查询最大值

向 actual 完整 `n` 槽背景额外插入一个查询标签 `a`，定义

\[
Q_a(z)=\sum_{B\ni a}\frac{r_B}{1+|B\cap Z|}
=K b_a(Z)+s_a(Z),
\qquad |s_a(Z)|\le M.
\]

这是**额外查询价**，不是背景内某位玩家利润。均匀偏置按查询是否已用分为两值：

\[
\begin{aligned}
a\notin Z:\quad
\beta_n&=2^{n-1}\sum_{j=0}^n\binom nj\frac1{j+1}
=\frac{2^{2n}-2^{n-1}}{n+1},\\
a\in Z:\quad
\gamma_n&=2^n\sum_{j=0}^{n-1}\binom{n-1}j\frac1{j+2}
=\frac{(n-1)2^{2n}+2^n}{n(n+1)}.
\end{aligned}
\]

令

\[
\delta_n=C-n\beta_n
=\frac{2^{n-1}(2^{n+1}-n-2)}{n+1};
\qquad \beta_n-\gamma_n=\delta_n/n>1.
\]

最后的严格界对所有 `n≥3` 成立：`2^{n−1}≥n+1` 且 `2^{n+1}>2n+2`，所以 `δ_n≥2^{n+1}−n−2>n`。

若 `a` 未用，`Z∪{a}` 是 `n+1` 标签集合，F 在它上为零；M1 的 Boolean 边际直接给

\[
s_a(Z)=F(Z\cup\{a\})-F(Z)=-F(Z)\in\{0,-1\}.
\]

因此全部 `n` 个未用查询的价格恰为 `Kβ_n−F(Z)`。若 `a` 已用，插入查询后计数重复；这里**不对重复计数误套 Boolean F**，只用调和计数扩张的 `|s_a|≤M`：

\[
Q_a(z)\le K\gamma_n+M<K\beta_n-1,
\]

因为 `K(β_n−γ_n)>K>M+1`。而未用查询价至少 `Kβ_n−1`，故严格压过全部已用查询，得到

\[
\boxed{\max_{a\in P}Q_a(z)=K\beta_n-F(Z).}
\]

该精确式对所有 distinct `n` 标签集合成立，因而覆盖该输入的每份完整 SPE 的 actual 叶。

## 5. 同一 `σ`、共同 `p`、完整槽的付款

固定上述输入任一完整 SPE `σ`，其 actual 叶为 `z=(S_1,\ldots,S_n)`。按 SUMmin 正文，`Z_i(A)` 保留原 actual 前缀、强制行动及沿**同一份 `σ`** 的真实后继，共 `n` 槽，含强制者。对每行取合法列 `A=S_i`，确定策略必重现 actual 路径：

\[
Z_i(S_i)=z.
\]

对同一个任意合法分布 `p`，令 `g_p(z)=E_{a\sim p}Q_a(z)`。于是

\[
\sum_{i=1}^n R_i(p)
\le n g_p(z)
\le n\max_aQ_a(z)
=n(K\beta_n-F(Z))\le nK\beta_n.
\]

最后

\[
W(\sigma)-nK\beta_n
\ge K(C-n\beta_n)+n-1
=K\delta_n+n-1>0.
\]

全部 `p` 的结论由解析界一次覆盖，没有交换 `min` 与期望，也没有逐查询另挑强制列。强制 old 的其他列可能有重复；证明既未假定它们 distinct，也无需给其查询价统一 tight 界。实际动作这一列已足够。

## 6. 图语义与 Boss3 d86 边的关系

依据 `research/IMPLEMENTATION.md` 第三阶段规则，准确形式是一条 `premises_mode:all` 的局部贡献边

`{CA-AGGREGATE-LAST-FLOOR-NO, CA-MOBIUS-FULL-HISTORY-EMBED} ⇒ SUMmin-full 目标的该输入族 / 全 SPE 预算贡献`。

A 提供固定两组势、正编译输入和精确代数；M2 作为显式联合前提支付**该输入的每份完整 SPE / 全有序历史**的 fresh 量词，并由上面严格比较支付 `K₀→K`。二者共同支持的关系已证且可为 `accepted`、`unconditional` 的 `contribution`；target 的一般 `U?` 仍 open，不能填写声称整个 target 已证的 `whole_result`。M1 的反演式已在 A 的构造内部及 M2 的接口中承载，不必机械增设第三个独立 ALL 前提或定义 hub。

已全文实读 Boss3 d86 正式边 `all-n-counterexample-summin-contribution.json`。它准确固定“源指定辅助策略的任意完整扩展”，actual 为一 X、`n−1` Y，因此 `F(Z)=0`、`W=KC+n−1`、`maxQ=Kβ_n`。本计划的独立价值是扩到**同一正编译输入的全部完整 SPE**；tight 形式相应为 `Kβ_n−F(Z)`，福利用 `≥KC+n−1`，不是把 Boss3 等式无条件抄到所有策略。二边可同时保留；本稿没有改写、替代或退休 d86 资产。

## 7. 精确来源 SHA 与实际阅读范围

以下 SHA 均在本 clone 对当时实际字节重新计算。除特别注明外，已阅读全文；有限报告/脚本未被运行或用作全称证明。

|路径|SHA-256|实际阅读|
|---|---|---|
|`AGENTS.md`|`20293db840f907c32f774b0d7f72450c56e6c0ad937720699d14f7c02e693cc9`|全文；具体本次只读/唯一写入范围服从上级任务限制|
|`research/IMPLEMENTATION.md`|`fb6613cd0c429f28b8bcfb1064076a629540cfbee8f7e3d670b0b39e78ff0d4b`|先关键词定位，再实读 L172–218 第三阶段与 ALL/contribution 规则；不声称全文|
|`research/registry.json`|`ee1148cd8c8053496e64e259902fb4890ea9a5add5a9c5a090b0d14739fc64ac`|仅三个上述 object 完整记录及顶层键；未实读全库|
|`research/workspaces/map-v2/Boss5/finalization-20261116/summin-all-spe-plan.json`|`abc1e871000e5b1bc5125afba31e64887e21e67ae2f42dbf7a2e34ac5fe42941`|全文|
|`archives/customer-attraction/state/反例/三人及以上聚合末位保底--反例.md`|`d316702ecc98a5976769d1d2e0094341474e0c4655deaac825bc208ae81d36e7`|全文；F、反演、K、重复历史、重复背景和福利边界|
|`archives/customer-attraction/state/定理/无重复辅助博弈的完整历史编译--定理.md`|`e6e06a43973f7c37673b498074475fdf8aa37338d448aff53b2bf9b2e7fa0dd4`|全文；独立核全有序历史归纳及任意孩子 SPE 对齐|
|`archives/customer-attraction/state/定理/子集调和势的Möbius反演--定理.md`|`9c7e58e4642077607ce2b49c67e7598c97b47b4cdb1b43a34cf335dd2aec5629`|全文；Boolean 与重复计数边际的区别|
|`archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md`|`cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88`|全文；全历史纯 SPE、标签和真实后继|
|`archives/customer-attraction/state/候选/全槽逐行最小价格的共同预算与有限报告--候选.md`|`e952c73849b2ac561ac4ebb761b3ae0c1af06d61f27e743c593ea0103c52698a`|全文；本证明只使用共同 p、真实完整列与目标 open 边界|
|`archives/customer-attraction/state/引理/完整槽末位最小价格的精确折扣与静态充分桥--引理.md`|`a2c504c39c6b1ab1d4a2a8d9f48b5a977ad2aa648aab0ac066771d22ff5ccf2a`|全文；完整槽接口、条件 half 与早期付款边界|
|`map/edges/boss3-summin-budget-repair-d86bee169e3617da/all-n-counterexample-summin-contribution.json`|`4eb5151221da99f7b46822bc4615dff81e6bca8febdb44d4ef1b21410bdd6a71`|全文；仅用于精确比较其指定策略范围；未把边内 review/evidence 的阅读声明算作本次实读|

本次未读 36 客户证书、其独立反例正文、有限辅助回归报告、Boss3 同级 proof/脚本/results 或冻结原版文件；它们不承担上述解析证明。未做新的枚举、LP、BI、IC、SHA 以外计算证书认证或外部检索。未发现本窄数学范围的缺口；尚待正式新边落盘后的文本/绑定/作用范围核验。
