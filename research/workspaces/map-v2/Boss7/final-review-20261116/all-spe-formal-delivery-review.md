# Boss7：ALL-SPE 正编译输入的正式交付审读

身份 Boss7；日期 2026-11-16；clone 为 `co-work-anl-boss7`。本轮独立实读任务定义、三个当前 object 完整记录与下列承重正文，未把旧计划审读当作新资产核验。唯一写入本稿；未运行 Git、sync、queue、board、checkpoint，未修改正式边、收据、canonical 或他人文件。

**正式交付实核通过，无本范围的数学或资产阻塞缺口。** 本轮先在实际 `claimed/Boss5` 任务上独立重建源证明，随后在父 Boss 通知同步完成后，全文实读新正式边、两份 proof、comparison-review 与正式 receipt，并核实际绑定和覆盖。当前本地任务 `boss5-summin-all-spe-3b-7383c8bf44f753cc` 为 `state=done`、`owner=Boss5`、`request_id=f33a0a97589f4765b051eedbc2f5824a`。正式边为 `boss5-all-spe-summin-budget-7383c8bf44f753cc`，单条 `{A,M2}` ALL、accepted、unconditional、仅 contribution。

父 Boss 报告本次同步远端 tip 为 `6b552f87eedfd744ae29b227fc1f562aa3b2b91c`；本 worker 按分工未运行 Git，独立核的是实际落盘字节、当前任务及当前 registry。这里没有声称 canonical 已集成此新包。

## 1. 当前任务与输入身份

本地 `research/registry.json` SHA 为 `ee1148cd8c8053496e64e259902fb4890ea9a5add5a9c5a090b0d14739fc64ac`。仅抽出并实读以下三份完整 object 记录，不声称全文审读整个 registry。按当前实现的规范 JSON SHA 算法独立重算 registration pins，三项均与实际任务 `input_pins` 一致。

|记号与端点|版本 / truth_status|实际 registration pin|
|---|---|---|
|A：`CA-AGGREGATE-LAST-FLOOR-NO`|v2 / proved|`699ba4cd7ebf119cdeb83f960aa4519f05068694f6f8507893ff071f155045ed`|
|M2：`CA-MOBIUS-FULL-HISTORY-EMBED`|v1 / proved|`42694a561f1d7d9687fce7fe834aa833e5fa2d8b5b7d84eb1bf54115e118d09a`|
|SUMmin：`customer-attraction/e7-summin-full-common-budget-exact-discount-and-finite-tests`|v2 / open|`e37e6d0b6d0236152b44c5bd1d840157a5f2673bfcf99f9170af932a33e87332`|

任务精确固定源正文的两组势、原 `2n` 个标签与 `K=6M+4`；新贡献的策略量词为这个同一正整数输入的**每份完整有序历史纯 SPE**。它不是在 A 的一般存在性陈述里任取其他反例，也不把 SUMmin 的一般输入量词证明出来。

## 2. 原标签目录与单位客户合法性

取整数 `n≥3`，原标签集 `P=X⊔Y`，两组大小各为 `n`。使用 A 的精确势

\[
F(S)=\begin{cases}
1,&|S|=n\text{ 且纯组},\\
-1,&|S|=n-1\text{ 且混合},\\
0,&\text{其他}.
\end{cases}
\]

A 的整数反演为

\[
c_A=\sum_{T\subseteq A}(-1)^{|A|-|T|}F(T),\quad
z_A=(-1)^{|A|+1}|A|c_A,\quad
x_B=\sum_{A\supseteq B}(-1)^{|A|-|B|}z_A.
\]

它给全部 Boolean 集合的身份 `Σ_B x_B H_|B∩S|=F(S)`；本输入 `D=1`，无隐藏清分母。令 `M=Σ_B|x_B|`、`K=6M+4`、`r_B=x_B+K`，则每个非空兴趣类型 `B` 的重数为严格正整数，至少 `K−M=5M+4>0`。将它展开为 `r_B` 个不同单位客户，不会增加主题标签数、行动槽数或提供者权重。singleton 兴趣类型正，故原 `2n` 主题非空且两两不同。

本结果只使用这个原目录，不宣称加空标签、复制同覆盖标签或扩张查询目录后仍有同样常数。`C,β,γ` 都依赖原 `2n` 标签和全部非空类型。完整原模型允许更广标签目录，不会反过来扩大此输入族结论。

## 3. M2 的全历史量词在更大 K 下保留

M2 正式公式写 `K₀=4M+1`。不能仅把它的结论机械套给不同输入，必须重用其严格比较：固定任意长度 `d<n` 的有序前缀，过去允许任意重复；设剩余 `t=n−d` 人。因为原标签数为 `2n`，未用标签数至少 `t`。

按剩余深度归纳。给定当前动作后的任意真实孩子 SPE，归纳假设使其后继全部选 fresh。当前 fresh 标签 `a` 与一个过去出现 `v≥1` 次的 old 标签 `b` 比较时，两条真实后继可以完全不同。只计算均匀偏置时，分别用两个置换将后继标签集对齐至不含 `a` 的共同集合：fresh 支置换固定已用标签及 `a`；old 支置换只固定已用标签，可移动 `a`，故也处理该支真实后继选择 `a` 的情形。这不是同时置换真实策略或 signed 类型。signed 部分始终保持各真实分支。两个偏置分别正规化后仅 `a,b` 的计数不同。按客户类型成对相消，fresh 相对 old 的单位偏置差为

\[
\sum_{C\subseteq P\setminus\{a,b\}}
\left(\frac1{1+s_C}-\frac1{1+v+s_C}\right)\ge\frac12.
\]

空集项为 `v/(v+1)≥1/2`，其余项非负。每个 signed 玩家收益绝对值不超过 `M`，故本输入的真实差至少

\[
K/2-2M=M+2>0.
\]

末层没有后继，是同一比较的基础步；归纳遂覆盖全部有序前缀、已重复离轨历史、任意真实孩子 SPE 与全部弱平局。每份完整 SPE 在每个历史都 fresh，actual 叶因此有 `n` 个不同标签。

不同 fresh 行动及各自真实 fresh 后继的均匀偏置相同，较大 `K` 不改变 fresh 比较和平局；M2 的辅助策略投影和补齐重复子树论证也保留。本预算只需要每份原 SPE 的 fresh 结论，完全不要求它等于 A 展示的指定辅助策略，也不要求同计数有序历史共用续局。

## 4. 任意 distinct n 叶的 signed 福利

固定任意 `Z⊂P`、`|Z|=n`，甚至暂不要求它由 SPE 达到。选 `a∈Z` 的 signed 收益为 `F(Z)−F(Z\{a})`，由源 Boolean 调和身份保证。

* 纯组 `Z`：`F(Z)=1`，删除值均零，所有 `n` 人 signed 收益为 1，总和为 `n`。
* 混合 `Z`：`F(Z)=0`。若 `a` 所在组在 `Z` 中至少两名，则删除仍混合，signed 收益为 1；若 `a` 是其组唯一成员，则删除后纯组，signed 收益为 0。

因 `n≥3`，两组不会同时各只有一名。所以

\[
w_x(Z)=\sum_{a\in Z}[F(Z)-F(Z\setminus\{a\})]\in\{n-1,n\},
\qquad w_x(Z)\ge n-1.
\]

signed 均分守恒与普通客户守恒一样逐类型成立。与 `Z` 相交的非空类型数恰为

\[
C=2^{2n}-2^n,
\qquad W(\sigma)=KC+w_x(Z)\ge KC+n-1.
\]

源指定“一 X、`n−1` Y”路径确有 `W=KC+n−1`；一般完整 SPE 不得直接写成这个固定等式。此证明允许不同 `σ` 有不同 actual 路径及福利，不需要对它们作额外分类。

## 5. β、γ、δ 与全标签查询最大值

额外查询在完整 `n` 槽背景 `z` 上的价格为

\[
Q_a(z)=\sum_{B\ni a}\frac{r_B}{1+|B\cap Z|}
=K b_a(Z)+s_a(Z),\qquad |s_a(Z)|\le M.
\]

它是独立额外查询价格，不是背景内某位玩家利润。`z` 顺序不影响这一个价格，而完整策略仍按有序历史定义。分别枚举兴趣类型中其余已用与未用标签，得到

\[
\begin{aligned}
\beta_n=b_{a\notin Z}(Z)
&=2^{n-1}\sum_{j=0}^{n}\binom nj\frac1{j+1}
=\frac{2^{2n}-2^{n-1}}{n+1},\\
\gamma_n=b_{a\in Z}(Z)
&=2^n\sum_{j=0}^{n-1}\binom{n-1}j\frac1{j+2}
=\frac{(n-1)2^{2n}+2^n}{n(n+1)},\\
\delta_n=C-n\beta_n
&=\frac{2^{n-1}(2^{n+1}-n-2)}{n+1},\qquad
\beta_n-\gamma_n=\delta_n/n.
\end{aligned}
\]

对 `n≥3`，`2^{n−1}≥n+1` 且 `2^{n+1}>2n+2`，故 `δ_n>n`、`β_n−γ_n>1`。边界 `n=3` 的短 Fraction 计算为 `C=56, β_3=15, γ_3=34/3, δ_3=11`，严格差为 `11/3`；它只核这个具体边界，不承担任意 `n` 的证明。

当 `a∉Z` 时，`Z∪{a}` 为 `n+1` 标签集合，`F` 值为零，Boolean 边际给

\[
s_a(Z)=F(Z\cup\{a\})-F(Z)=-F(Z),
\quad Q_a(z)=K\beta_n-F(Z).
\]

当 `a∈Z` 时，额外查询使计数重复，不能把 signed 值误写成 Boolean 集合边际。使用正确的粗界已足够：

\[
Q_a(z)\le K\gamma_n+M<K\beta_n-1,
\]

因为 `K(β_n−γ_n)>K=6M+4>M+1`。而每个未用查询值至少 `Kβ_n−1`；原目录尚有恰 `n` 个未用标签。因此对所有 distinct `n` 叶都有精确式

\[
\boxed{\max_{a\in P}Q_a(z)=K\beta_n-F(Z).}
\]

它在 `F(Z)=0` 时为 `Kβ_n`、在纯组 `F(Z)=1` 时为 `Kβ_n−1`；不需要假定所有 SPE 共用源展示路径。

## 6. 同一 σ、同一个 p 与 actual 动作列

固定本输入任一完整 SPE `σ`，令其自己的 actual 叶为 `z=(S_1,…,S_n)`。SUMmin 的行列为在 actual 前缀强制行动 `A`，再沿同一 `σ` 的真实后继完成；保全部 `n` 槽并含强制者。

每行取一个与查询无关的合法列 `A=S_i`，确定策略逐步重现原路径，故 `Z_i(S_i)=z`。对同一个任意目录分布 `p`，

\[
\begin{aligned}
\sum_{i=1}^nR_i(p)
&\le n\,\mathbb E_{a\sim p}Q_a(z)\\
&\le n\max_aQ_a(z)
=n(K\beta_n-F(Z))\le nK\beta_n<W(\sigma).
\end{aligned}
\]

最后一步的统一裕量为

\[
W(\sigma)-nK\beta_n\ge K\delta_n+n-1>0.
\]

此处没有交换 `min` 与期望，没有针对各查询分别选列，没有换 `σ`；其他强制列可能含重复而不影响证明。也没有声称 `ΣR` 的精确最大值等于这个统一上界。即使只用粗福利界 `W≥KC−M` 和查询界 `Q≤Kβ_n+M`，也有

\[
W-n(K\beta_n+M)\ge K\delta_n-(n+1)M
>nK-(n+1)M=(5n-1)M+4n>0,
\]

所以任务所要求的粗证明及紧化证明均已支付。

## 7. 正式图语义与旧边兼容性

实际正式边准确写为单条 `premises_mode:all`：`{A,M2} ⇒ SUMmin 的本输入族 / 每份完整 SPE / 全 p 的严格预算 contribution`。A 固定正编译输入及其精确代数；M2 支付全有序历史与每份原 SPE 的 fresh 量词，并在上面显式核较大 `K`。两个源当前都 proved，局部关系已证，实际 `accepted`、`relation_mode:unconditional` 正确。

target 的一般 SUMmin-full 仍 open；不得有暗示一般输入结论已全证的 `whole_result`。必须保 `contribution.result` 与 `remaining`，后者指出其他输入、人数和完整 SPE 仍未覆盖；也不能把本族结论当作无条件恰六人 half 的一般证明。

已全文实读 Boss3 的 d86 正式边 `all-n-counterexample-summin-contribution.json`，实际 SHA `4eb5151221da99f7b46822bc4615dff81e6bca8febdb44d4ef1b21410bdd6a71`。该边精确限制源指定辅助策略的任意完整扩展，故 `F(Z)=0`、`W=KC+n−1`、`maxQ=Kβ_n` 的更精确等式正确。新 ALL 结果扩大策略量词，不替代、撤回或改写这份固定策略资产。本轮未编辑该边。

## 8. 实际正式资产、绑定与收据终审

以下四个正式资产及 receipt 均已全文实读，并在此 clone 重新计算 SHA；这些是本次实际正式核验对象，不是计划占位。

|正式文件（边目录为 `map/edges/boss5-summin-all-spe-3b-7383c8bf44f753cc/`）|SHA-256|实读判断|
|---|---|---|
|`all-spe-summin-budget.json`|`2fcab5e1df6980e81a0880fe84554f1a1d9b0f83b14704a80481f56264476e86`|单条两源 ALL / unconditional / contribution；完整解释与上述独立证明一致|
|`full-history-parameter-proof.json`|`754b58b16c1e56e1b5c561d27a237e1cdebc5eb167c395a10444735f717244fb`|A1–A4、偏置双置换、B1–B5 全有序历史归纳、C1–C5 完整扩展均闭合；old 支真实后继含 a 的风险已明确处理|
|`all-spe-query-budget-proof.json`|`5d7f8a6135faaa0f9fe4748ee4d0560f9e093ea35d608e02b19a336f3fd74543`|12 步粗界、tight 界与全部量词审计逐步正确；未冻结后继或误用 Boolean F|
|`comparison-review.json`|`97525258b8afc21feaac757a8efdc412e4ff73619b489c7e5b1e9809b67a209f`|独立比较说明保源输入、扩策略量词、旧等式的条件及一般 open 边界|
|`map/receipts/boss5-summin-all-spe-3b-7383c8bf44f753cc.json`|`5814e7d63f26bf076b6eea897d5866687b898a696bf875e3f4a27c9fde5677d6`|三 core linked、同一 edge ID、四 asset SHA、全部对象对处置与 follow-up 审计相容|

本轮独立检查全部通过：

* 当前三个 object pins 与 task、正式 edge、两 proof、receipt 一致；源对象分别为 A v2 proved、M2 v1 proved、target v2 open。
* 正式 edge 的全部 10 项 `evidence` SHA 与当前字节一致；模型和 SUMmin 的两个 section 标题各唯一。三 `endpoint_pins`、10 个 `evidence_pins` 及 `review_digest=e1594a661d6e8eeba7a358adbb28caac964c02040bca2fc45875ba3da54b88f6` 已从实际内容独立重算并完全匹配。
* receipt 的 `definition_pin=76d897e45dabfebd1c84dfcce2dac042d01a73ded74a6b3bdf6705ba58187d62` 等于当前 task.definition 的规范 JSON pin；done 任务内嵌 receipt 与正式 receipt 完全相同。task.edge_paths 精确指向本唯一逻辑边。
* receipt 四个 asset 的 SHA 均准确，且三 core coverage 恰为任务三对象，每项 `linked`、当前 `object_pin`，均列同一已接受 edge ID。三对 `comparison_dispositions` 恰覆盖三对象所有无序对象对，并均按同一联合局部贡献处理，没有拆成独立充分前提。
* `closed_overlaps=[]`、`follow_up_tasks=[]` 与任务没有 overlap/follow-up 标记相符；一般 SUMmin、一般六人 half 与早期共同付款已明确留 open，而不是遗漏具名 follow-up。新包无 supersedes，不改 Boss3 d86；旧边当前 SHA 仍为上列原值。
* 对四新资产内 29 个不同 `path/sha` 来源对作额外当前字节核对，除下面明确的旧任务快照外，均存在且匹配。这只做引用可定位性核对，未把 hash 检查冒称对所有历史附件的数学实读。

附件中任务 SHA `81a38890cec33b16ed3184f6aef42eaab550115cbda9a7d8358e2a14a78c9ae2` 是它们明确标明 `claimed` 时的阅读快照；当前 done 任务 SHA 已变为 `e3e3b4433123b9742c42213e778e5d0505769926e89001d6f8460bb358d7c9a0`。任务 `definition_pin` 保持完全一致，三个数学输入也未变；这个已标时间语境的来源记录不构成承重数学输入漂移，不应把完成后的状态更新误判成证明证据失效。

本 worker 另实际运行一次只读 `python work.py research edge-check …/all-spe-summin-budget.json`，返回 `edge-structure-valid-not-a-mathematical-verdict`、`edge_status=accepted`、`proof_scope=step`。数学判断由本稿对源和实际 proof 的独立实读承担。

旧 `all-spe-tight-joint-review.md` 仍只代表计划审读；本稿这次终审已另核实际正式资产，不用旧稿替代。**本范围数学、输入绑定、正式证据和 receipt 覆盖均无阻塞缺口；没有核或改 canonical。**

## 9. 实际字节与阅读边界

以下 SHA 均在此 clone 重算；除另注外为全文实读。没有读取/运行 36 客户证书、有限辅助回归报告、五人探针、旧 Boss3 脚本/results 或全历史枚举；它们没有承担本次全称证明。为核正式 edge 最后一项 evidence，本轮又全文实读 Boss3 `all-n-budget-proof.json`，其固定策略量词、粗/tight 解析式与新结果的子范围关系准确。没有外部检索。

|路径|SHA-256|范围|
|---|---|---|
|`AGENTS.md`|`20293db840f907c32f774b0d7f72450c56e6c0ad937720699d14f7c02e693cc9`|全文；本次权限按父任务唯一写入范围|
|`prompts/03-map-worker.md`|`6629f71923c54d994297d54c3737b285227b72c463641d318c3f61c9342d07b2`|全文|
|`research/IMPLEMENTATION.md`|`fb6613cd0c429f28b8bcfb1064076a629540cfbee8f7e3d670b0b39e78ff0d4b`|实读第三阶段关系、绑定、收据与 overlap 规则；不声称全文|
|`research/registry.json`|`ee1148cd8c8053496e64e259902fb4890ea9a5add5a9c5a090b0d14739fc64ac`|三 object 完整记录、规范 pin 重算|
|`research/operations/map-v2/tasks/boss5-summin-all-spe-3b-7383c8bf44f753cc.json`|`e3e3b4433123b9742c42213e778e5d0505769926e89001d6f8460bb358d7c9a0`|当前 done 全文；另已全文实读早前 claimed 快照 `81a388…`，definition 相同|
|`research/workspaces/map-v2/Boss7/final-review-20261116/all-spe-tight-joint-review.md`|`cf012116c86d73ca0b4a88dc5551f6c91d1c73ca5c1a0860c05a0171d3264a71`|全文；只作既有计划审读定位|
|`archives/customer-attraction/state/反例/三人及以上聚合末位保底--反例.md`|`d316702ecc98a5976769d1d2e0094341474e0c4655deaac825bc208ae81d36e7`|全文|
|`archives/customer-attraction/state/定理/无重复辅助博弈的完整历史编译--定理.md`|`e6e06a43973f7c37673b498074475fdf8aa37338d448aff53b2bf9b2e7fa0dd4`|全文|
|`archives/customer-attraction/state/定理/子集调和势的Möbius反演--定理.md`|`9c7e58e4642077607ce2b49c67e7598c97b47b4cdb1b43a34cf335dd2aec5629`|全文|
|`archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md`|`cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88`|全文|
|`archives/customer-attraction/state/候选/全槽逐行最小价格的共同预算与有限报告--候选.md`|`e952c73849b2ac561ac4ebb761b3ae0c1af06d61f27e743c593ea0103c52698a`|全文|
|`archives/customer-attraction/state/引理/完整槽末位最小价格的精确折扣与静态充分桥--引理.md`|`a2c504c39c6b1ab1d4a2a8d9f48b5a977ad2aa648aab0ac066771d22ff5ccf2a`|全文|
|`map/edges/boss3-summin-budget-repair-d86bee169e3617da/all-n-counterexample-summin-contribution.json`|`4eb5151221da99f7b46822bc4615dff81e6bca8febdb44d4ef1b21410bdd6a71`|全文边文本；未把其 evidence 阅读声明算成本轮实读|
|`map/edges/boss3-summin-budget-repair-d86bee169e3617da/all-n-budget-proof.json`|`fa494cd2ac03e245f46a158fe6a3169cd945b95e10516b68b7240dfb4da8e154`|全文；仅核其指定策略子范围，未执行旧计算|

四新正式资产及 receipt 的最终 SHA 和全文实读范围已列于第 8 节。唯一新写入仍为本稿。本稿最终状态：**新正式 ALL contribution 数学及资产终审通过，可供父 Boss 后续整合；一般 SUMmin 与一般六人 half 仍 open。**
