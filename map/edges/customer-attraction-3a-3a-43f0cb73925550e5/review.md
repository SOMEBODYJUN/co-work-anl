# Review: 四人完整策略的末位标量桥接反例

## 任务、对象与读取边界

任务 `customer-attraction-3a-3a-43f0cb73925550e5` 的核心对象是
`customer-attraction/four-player-complete-policy-last-payoff-scalar-bridge-counterexamples`，登记 pin 为
`3829a3289f88d360015cf432341ceeee6c7b2b5242776a3af5522a95eaeab0ad`。
本轮完整读取并按字节核对了任务声明的四份材料：

- `archives/customer-attraction/state/反例/四人完整策略的末位标量桥接反例--反例.md`，SHA256 `7eae7283879241aff280abdb22638ecedfbd19487a3ee60564bcaff050e73cad`；
- `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md`，SHA256 `cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88`；
- `archives/customer-attraction/tools/evidence/global-exchange-resumed-boss2/original/last_reply_bridge_four_topics.json`，SHA256 `ace92519ef692555469b884bff1c8492710c04231fa66a7f45fc3a330ad58611`；
- `archives/customer-attraction/tools/evidence/global-exchange-resumed-boss2/new-global-exchange-exact-check.json`，SHA256 `08f5337748b55498f75865747c27b4133607de1c72486f22845289bb2a6277c4`。

为厘清正文明确提到的独立边界，我也直接阅读了登记对象
`customer-attraction/early-prefix-five-player-last-payoff-scalar-twelve-client-obstruction`、
`customer-attraction/last-payoff-not-uniformly-shared-disjoint-family` 以及精确上界对象
`M-b0ff41c82d5d49e291b7e57bce723426` 的现行正文；没有把共同模型定义自动提升为 hub 边，也没有把这些对象的有限证据当成四人策略的生成来源。

## 共同模型与量词

模型是有限单位客户集 (N)、有限非空**标签**目录 \(\mathcal S\) 与任意覆盖映射。不同标签可有相同覆盖，空覆盖、重复行动、零客户及弱平局均保留。(m) 名单位提供者按固定顺序各选一次并观察全部先前有序行动；客户价值在最终覆盖者之间均分。纯策略定义在每个有序历史，完整纯 SPE 的偏离比较沿同一策略在改变后的历史继续完成，不能冻结在轨后继，也不能仅按历史负载合并不同有序节点。

目标对象的量词是**存在**两份明确的四人完整有序历史纯 SPE：一份两主题五客户策略，一份四主题七客户策略。它们只反驳精确的辅助桥

\[
(m-1)u_m\le W+D,\qquad
D=\sum_{x\in H\setminus L}\frac1{c_x+1},
\]

其中 (H) 是实际覆盖并集，(L) 是实际末主题，(u_m) 是末位实际收益。对象没有断言所有四人 SPE 都违反该式。

## 仍成立的末位税上界

末位在实际节点是真实最佳回复。对任意 (m) 个合法比较主题，按末位前负载给价：(L) 中客户价 (1/c_x)，(H\setminus L) 中客户价 (1/(c_x+1))，未覆盖客户价 1。每个比较主题的价格和不超过 (u_m)，而比较并集中的客户至少被计价一次；把 (H) 内价格补足到 1 的缺额为 (W-u_m-D)。因此目标正文保留有效不等式

\[
\operatorname{OPT}_m\le m u_m+(W-u_m-D)
 =W+(m-1)u_m-D.\tag{1}
\]

这是一个必要上界，不是等式。把 (1) 再用 (W+D\ge(m-1)u_m) 闭合成 \(\operatorname{OPT}_m\le2W\) 的步骤，正是被本对象切断的额外路线。它不削弱 (1)，也不推出存在一个普遍可替换的标量条件。

## 两份四人完整策略的精确证书

### 五客户、两主题

目录为互不相交的 (A,B)，大小分别 3、2。前 3 位在所有历史选 (A)；末位在前三步中 (B) 出现至多一次时选 (B)，出现两次或三次时选 (A)。策略表覆盖 (1+2+4+8=15) 个非终局有序历史。

- 固定证书含自身比较 30 条（每个历史比较两个动作），其中 21 条为零松弛，负比较数为 0；
- 实际路径为 (AAAB)，终局主题计数 ((3,1))，收益 ((1,1,1,2))，(W=5)，(operatorname{OPT}_4=5)；
- (L=B, u_4=2, D=3/4, 	au=9/4)；
- 被否桥左侧 ((m-1)u_4=6)，右侧 (W+D=23/4)，严格超出 (1/4)；
- 有效上界 (1) 为 (operatorname{OPT}_4\le41/4)，没有被否定；实际福利已最优，故这不是福利或 half 反例。

末位四种 (B)-出现次数的收益表为：0 次时保存 (B)（(2>3/4)），1 次时 (B) 与 (A) 均为 1，2 次时保存 (A)（(3/2>2/3)），3 次时保存 (A)（(3>1/2)）。第三、二、根节点的规定行动也分别逐历史满足弱最优性；因此这里确实是完整 SPE，而非只认证在轨路径。

### 七客户、四主题

在 (A,B) 外加入互不相交的单客户主题 (C,D)，保留四主题的完整 85 节点动作表。这里不能把“两主题版本前三位恒选 (A)”机械搬运；四主题表在 (C,D) 分支上另行指定后继。精确检查逐历史沿原动作表完成真实后继：

- 85 个非终局有序历史、340 条含自身比较，103 条零松弛、0 条负比较；
- 实际仍为 (AAAB)，收益仍为 ((1,1,1,2))，(W=5)；
- 四主题目录可覆盖七名客户，(operatorname{OPT}_4=7)，故实际 (W/\operatorname{OPT}_4=5/7>1/2)；
- (D=3/4)，同样有 (6-(5+3/4)=1/4>0)。

该版本说明标量失败不依赖“实际路径覆盖了所有客户”；但它仍不否定 half，因为 (5/7>1/2)。

## global-exchange exact-check 的作用边界

`new-global-exchange-exact-check.json` 的方法标记为 `definition-level Fraction; fixed inputs only; no canonical solver import`。执行范围记录为 1 次固定入口成功调用、3 次策略检查、6 个固定均衡游戏；随机搜索、贪心最小化、优化器和 canonical solver import 均为 0。其 `bridges` 两项与上面两份 15/85 节点证书逐项一致。另用标准库 `Fraction` 对四主题原动作表独立重放 85 个历史、340 个含自身比较，得到 0 负比较、最小松弛 0、实际 `AAAB`、(W=5)、(OPT_4=7)；该短重放只作为本轮读账核验，不冒称新的全局求解器。

同一 JSON 还保存了一个**不同对象**的五人 55 单位客户最小策略（781 历史、3905 条含自身比较、0 负比较，实际 (W=50)，根 SPE 福利集合为 55、55、50）及同一 55 客户实例在 2、3、4、6 人时的计数级固定游戏结果（四人时根 SPE 福利 55 与 50）。这些是 global-exchange 的额外固定输入诊断，不是本对象的四人 AAAB 证书，不是全目录纯 SPE 定理，也不构成六人 half 反例；不能把这些结果拼接进本对象的量词。

## whole / contribution / remaining

**Whole result（本对象完整结论）。** 在共同目录完整历史模型中，确实存在上述两份四人完整纯 SPE；两者精确满足全部离轨 IC，并均使 ((m-1)u_m-W-D=1/4>0)。所以全称“每份四人完整 SPE 都满足该标量充分桥”是假的。两例都满足 half，且有效末位上界 (1) 保持成立。

**Contribution（可复用贡献）。** 这两份策略只支付“额外标量闭合条件”的反例步骤：它们证明末位真实最优性与完整离轨 IC 不足以推出 (W+D\ge(m-1)u_m)。它们可作为任何试图用单一 (u_m,W,D) 标量完成 half 证明的反例检查；四主题版本还保留未实际选择的客户主题。

**Remaining（未支付义务）。** 本对象没有给出所有 (m)、所有目录或所有完整 SPE 的替代标量；没有否定真实末位税上界、共同静态末回复菜单引理、任何已付动态菜单/索引预算；没有给六人完整 SPE 的 half 反例或定理，也没有把固定策略证书提升成策略无关的 LP 全锥结论。五人早期 12 客户点（gap (12/5)，其 `scalar_exact=1/5` 只是可行点，不是最优对偶）与全人数不交族（m≥4 的另一辅助 cap 反例）是独立 corroborating witnesses，不是本四人证书的迁移定理。

## 关系处置与后续

本批保存三条语境引用边：

- 四人对象引用精确末位税上界 `M-b0ff41c82d5d49e291b7e57bce723426`，只说明 (1) 仍有效，不能写成 refutes；
- 四人对象引用全历史不交族，保留“同一辅助 cap 的另一独立反例族”身份，不作 specialization 或一般迁移；
- 四人对象引用五人早期恒题障碍，保留独立五人证书与同一被否桥，不把 (m=4) 点外推到 (m=5) 或六人。

这三条都是 `relation_mode: context` 的 `cites`，不向 canonical coverage 贡献逻辑蕴含。共同模型与 `true-last-reply-menu-common-static-slot-domination` 的完整正文也已读取；它要求恰两名剩余玩家和每个当前主题的真实末位回复菜单，结论是共同静态分布/价格封顶，属于不同的局部菜单路线，本反例没有触碰它，因此不新造 hub 边。没有需要发布的 follow-up；上述 deferred 对端均已能解释其独立作用，剩余开放问题是全局 half/替代付款路线。
