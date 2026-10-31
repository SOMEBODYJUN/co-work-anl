# raw K2 → canonical product：作者 Proof 实际全文读后对照

审查者：`/root/sol_nsw_independent_attack`。这是 Exact-first 独立重构冻结后、获 parent 释放才做的 author-read-after，不是新的 blind review。原独立记录保持不改。

## 1. 精确来源与实际次序

新的唯一读取文件：

`/workspace/scratch/038d9dcc4cac/sol_general_repair_k2_canonical_pullback_author_proof_v1.md`

- 实核 SHA-256：`4f4a57ef7a87e9f3fbb4d15049b8aeb50e70ee3695e35afebf08c8c4313f0412`。
- 实核 7,629 bytes、123 行、mode `0644`。
- 真正按 **1–120、121–123** 两块显示并逐行读完全部，未截断。
- 包括 §7 作者对程序范围的文字说明；**没有打开、读取、hash、运行或审查作者代码及 run JSON 文件**。文中其 SHA 仅是作者所报，不作为我实核的软件证据。parent 另行做其代码审查与重放，我不代签。

真实次序为：只读新 Exact 49 行 → 独立写出全部 raw K2 证明、CONFIG 与 actual schedule → 冻结 Exact-first → parent 实际全文读完后释放这份 Proof → 本次完整读作者稿。旧记录为：

`/workspace/scratch/038d9dcc4cac/sol_general_repair_k2_canonical_pullback_independent_exact_first.md`

实核仍为 SHA `2c35b3b119264c2c78eeeeab96fcd9c761d8ed57a1fe0b2d28d5041f2598e75d`，10,023 bytes、183 行、`0444`。原 Exact 当前实核仍 SHA `a79fd77dc17c87a8729bc3c4b47088a434f24db98e37f95b0ec9e01ec604323a`，3,594 bytes、49 行。

既有 K2/SA1/empty/slice 背景已在 Exact-first 披露；本次不将后得作者推导倒写入此前独立阶段。

## 2. 实例与完整 functional

作者 7–16 行与 Exact、我的独立记录同一个 P：4 groups、8 indexed roots、9 incidences、6 resources、14 machines、13 jobs、26 finite endpoints，T=7/4。所有原有限端都是三位的 literal，所有 job one-hot/endpoint exclusivity 与 Boolean identities 在商代数中成立，乘到 degree 4 也成立。

作者正确不把 `ell(abc)=−1/160` 解释成真实三位分布，也没有只保留逻辑 state 变量而漏掉 ordinary assignment endpoints。其 352×352 物理 M2 的 PSD 来自全局 affine pullback，不是只核一个小 principal submatrix 后宣布大矩阵 PSD。

## 3. 两种独立 PSD 证明对照

我在 Exact-first 用三位置换的 symmetry block 和 standard blocks 证明七维 bit M2 正定，没有先读作者 LDL。作者 24–28 行按 `(1,a,b,c,ab,ac,bc)` 给出的 pivots 为

`1,21/100,63/320,7/40,7/256,7/288,7/384`。

本次我从同一七维矩阵自行再用 Fraction 消元核对，七个 pivots 全部逐项一致。作者提到选数时参考 N=5,t=3/2 的 slice 公式；数值确为对应前三阶 falling-factorial ratios，但其 PSD 证明明确只依赖本七维精确矩阵，**没有把未满足一般参数范围的 slice theorem 当作免费认证**。

作者 34–51 行的 raw-load 分类与我的逐机表相同。唯一非恒定 root 为

`load_M0=1/2+a−b/2+c/2`，`h=5/4−a+b/2−c/2`。

我的独立 localizer matrix 是整数矩阵

`[[304,24,150,66],[24,24,10,−4],[150,10,150,17],[66,−4,17,66]]/320`。

由原先独立核得的 leading minors 再求 successive ratios，恰是作者报告的

`19/20,21/304,91/384,5761/41600`。

因此作者 localizer 正定断言不是只检查坐标/补，也不是偷换 canonical activation row。其余 roots 与 u/v/r 的 load 恒 1，三个 fallback resources 的 load 为 Boolean literal；公式 `(T−1)L(q²)+L(((1−literal)q)²)` 在 degree 4 内由 Boolean reduction 和 M2 给出全部全局 affine localizers。

## 4. 所有 CONFIG、三阶边界与真实 OPT

作者 55 行对其余 13 台机器使用 singleton/empty，与我独立构造一致。每行同机 pair 是互补 literals 的乘积或不存在第二 job，故为零；权来自同一个 L，合法 unit 配置和一阶 cover 均正确。

作者 M/0 五配置 `{P_u},{S,P_u},empty,{P_u,P_v},{S,P_v}`，权 `(14,21,21,21,3)/80`，与我先前 `(28,42,42,42,6)/160` 对应重排完全相同。其 first `(3/10,7/10,3/10)`、pairs `(21/80,3/80,21/80)` 均一致。

作者 79 行的临时三位 patterns 也核对正确：`000→{P_u}`、`100→{S,P_u}`、`010→empty`、`001→{P_u,P_v}`、`111→{S,P_v}`。这是本行真实 CONFIG law；它没有冒充共同 ell 的全局 law。

特别是原同机三阶 `L(S P_u P_v)=7/160`，但全部真实合法该机 CONFIG 的 triple 为零，因为三 job 全集 load=2。作者明确披露 first/pair 合同不共享这项；加原同机三阶共享便 cut 本证书。Exact-first 也已独立指出这一点。它不违反当前 raw K2，也不能据此把当前合同偷换成更强层级。

作者 87 行的真实 C=1 schedule 与我独立列出的 13-job schedule 相同：M 选 r state，Hu/Hv own u/v，Hr fallback w_r；所有未选 incidence 留各自 private，M/0 两个 1/2 合计 1。全部 selectors/incidences 各执行一次，资源 u,v,r,w_r 各一 job。Unit selector 给 OPT≥1，所以 actual OPT=1。这个 schedule 不保原伪矩，作者并未声称它保。

## 5. canonical 的失败与精确范围

作者 93–111 行与独立计算完全一致：`Z_M0u=ab`、`Z_M0v=a(1−c)`、`A_Hv0=c`。直接 degree≤2 canonical product pullback 给

`L(Z_M0u A_Hv0)=−1/160`，

`L(([Z_M0u+Z_M0v]/2−A_M0/4) A_Hv0)=−1/80`。

第一式违反 canonical nonnegative claim row 的 primitive-SA1 lift；第二式违反 canonical quality row 的同一 lift，并因 c²=c 而违反相应 activation localizer。Physical slack h 的全局 affine-localizer matrix 可正定而 cross entry `L(hac)` 为负；canonical slack 是 a h，合同不能免费把前者换成后者。

作者明确仅反驳 **同一个 raw K2 点的指定直接 product map**。实际 P 有 OPT1，也有其他 integral/R_1 点；改矩、另解 R、更强合同、其他 packing 提取与主算法都没被这个例子排除。它不是趋二 gap、actual-OPT gap 或单 outer 算法反例。作者的范围陈述准确。

## 6. 结论与软件边界

**作者 Proof 实际全文读后未发现 fatal；其数学证明与已冻独立 Exact-first 同实例、同点、同合同、同负值。PASS 仅为上述 raw K2 给定点到 canonical product pullback 的同点失败。** 原独立记录不改、不升级，也不因作者程序存在而追认自己未审的软件证据。

我的实际软件动作仍限于独立 inline Fraction 的小矩阵/配置有理算术；本次新增只复算上述 pivots，没有运行作者程序，没有实现通用 K2 checker、SDP finder 或 UM 算法。作者 §7 所报代码范围、文件 SHA 与 run 内容由 parent 自行核对，本审不认证。

全球新颖性未认证；一般 UM 主目标仍 OPEN。
