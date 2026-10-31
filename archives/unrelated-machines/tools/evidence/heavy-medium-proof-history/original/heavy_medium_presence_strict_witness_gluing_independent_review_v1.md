# HEAVY–MEDIUM STRICT-WITNESS PRESENCE：Exact-first 独立审查

审查者：general_query_response_review。2026-10-18。

本文件冻结前只读取新 Exact 及 parent 明确允许的既有 `unit_presence_two_witness_sharp_gluing.md`，未读取新作者 Proof，也未询问作者构造。以下独立推导使用既有基础中的匹配分量与不等成本两选择舍入，重新核查新 strict T、near-heavy 域。

读取的 Exact SHA-256：`f9dad0a0f70f272446042091e0bb400c7a87c6a3f96bae512cfbed34c230183e`。
读取的既有基础 SHA-256：`1d5d27a9a80c64dbcca319531da735f23b1d65e29d1ef1f16a011a85a4adf4ba`。

**独立结论：UM-HEAVY-MEDIUM-STRICT-WITNESS-PRESENCE-GLUING-v1 成立，未发现 fatal。上界不需要精确 unit、T=1+a、同 medium 成本或全矩阵两档。**

记 `h=(1−ε)T>T/2`，目标界 `B=[3/2+(ε+a)/2]T`。只用 σ0/σ1 实际端。00、11 分别返回两原见证，以下证明 mixed；交换测量机名称后，设 v 应为0、w 应为1。

## 1. Heavy 匹配及分量

令 `N_t={(j,σ_t(j)):p_{σ_t(j),j}≥h}`。每个 N_t 在“原 job–原 machine”二部图上是匹配：job 在实际见证中只执行一次，每机不能容纳两枚时间>T/2的 heavy。

N0、N1 的共同边是孤立固定边，保留不变；余下并图分解为交替偶环或路径。边颜色是其来自的见证。内部 job 两见证都 heavy，路径的 job 端点恰是 heavy↔medium 的跨角色 job。按端点分类：

- machine–machine 路径：两个 machine 端点边色相反；每种方向在一个端点有 heavy、另一个没有，内部 machine 两方向均 heavy。
- job–machine 路径：两端边色相同。选该颜色为 active，此时端点 job 执行 heavy、端点 machine occupied；另一方向端点 job 执行其另一见证的 medium 端，端点 machine vacant。
- job–job 路径：两端边色相反。每方向恰一枚端点 job heavy，另一枚执行其已知 medium 端；内部 machines 的 heavy-presence 恒1。
- 偶环及固定边：全部相关 machines 的 presence 恒1。

某测量机初态无 heavy、终态有 heavy，因此是颜色1的 machine 端点，只可能落在前两类路径。machine–machine 路径两个端点色相反，故 v,w 不可能在同一这种路径；job–machine 路径只有一个 machine 端点，也不能同时包含两测量机。两测量机亦不可能是这些分量的内部机器，因为内部机器在 σ0 已有 heavy。

## 2. 若 v 在 job–machine 路径：单分量翻转

从 σ1 出发，把 v 所在的 active 颜色1路径整体改为颜色0，端点 job 改放其 σ0 medium 端，其余全部保持 σ1。

v 失去 heavy；w 在其他分量且仍保留 heavy。各内部 machine 都仍有一枚 heavy，但不能像精确 unit 情形那样声称成本完全不变：它可能增加至多

\[
T-(1-\varepsilon)T=\varepsilon T.
\]

端点 machine 只删去 heavy，不增加 heavy；其他机器的 heavy 配置不变。整个翻转只新增一枚 medium 执行，成本≤aT。即使它的 medium 目的机同时发生 heavy 替换，任一机器总负载仍≤

\[
(1+\varepsilon+a)T < [3/2+(\varepsilon+a)/2]T=B,
\]

最后严格不等式用 `ε+a<1`。这是全部机器界，不只测量端。

## 3. 其余情况的 heavy 方向与真实 medium items

若 v 不在 job–machine 路径，则它在 machine–machine 路径，选该分量颜色0。w 的分量不同：若是 machine–machine 选颜色1；若是 job–machine 选 active。所有 job–machine 分量统一 active，其余 machine–machine、偶环及固定边按固定规则选方向。

这已固定 v=0、w=1。余下 medium 选择恰可表示为：

1. 两见证都 medium 的每枚原 job：两选项就是其 σ0/σ1 原端，各有自己的真实成本≤aT。
2. 每条 job–job 路径：一个 virtual item，两选项分别代表两种方向各自留下的那枚原端点 job 的已知 medium 目的机和真实 medium 成本。两端点是不同原 job，因此即使目的机相同，两个成本也可能不同。选项确定整条 heavy 匹配方向及两端点的执行。

所有 job–machine 端点 job 因 active 而执行 heavy，故不产生 medium item。Virtual item 只是整条分量方向的编码，不是额外执行任务。最终解码后，每枚原 job 仍执行恰一次、只用其 σ0/σ1 原端。job–job 方向不改变任何机器的 presence，因此舍入不会破坏两个测量值。

## 4. 不等成本两选择加权舍入

先令每个 item 在两选择上各放1/2。若两选择同一机器，固定到较便宜的那个，负载不超过原半半均值，并按该选项解码；单选项也固定。

其余 items 的两个 incidences 位于不同机器，每 incidence 成本在 `[0,aT]`。每台机器将所属 incidences 按成本非增排序，相邻两两配对，至多剩一个；每个 item 的两 incidences 再组成 job 对。两类对都是匹配，其并图为路径或交替偶环，可确定性二着色，使每个 job 对和机器对均一红一蓝。选全部红 incidences，即每 item 恰选一个真实选项。

若某机待舍入成本为 `q1≥q2≥⋯≥qs≥0`，则相对于其半半均值，任一红选择的增加量≤

\[
\tfrac12(q_1-q_2+q_3-q_4+\cdots)\le q_1/2\le aT/2,
\]

奇数尾项按正号计入。中间不等式由 `q2≥q3,q4≥q5,...` 得出。这同时控制全部机器；固定项只减少原均值。没有要求两选择成本相同、没有随机期望代替实际调度，也没有使用虚拟任务拆分执行。

## 5. 半半 medium 质量与全部机器负载

记 σt 在机器 i 的 medium 总负载为 `M_i^t`，items 半半总负载为 μ_i。真实双 medium job 与 job–job 端点的半半贡献正是两见证 medium 均值中的对应部分；全部 job–machine active 只删除原均值中来自 inactive 见证的非负 half-medium。因此

\[
\mu_i\le(M_i^0+M_i^1)/2.
\]

舍入后实际 medium 负载至多此均值加 aT/2。以 i 在两见证的 heavy-presence 分类：

| 两见证 presence | 两见证 medium 均值上界 | 最终 heavy 上界 | 最终总负载上界 |
|---|---:|---:|---:|
| 都有 heavy | εT | T | `(1+ε+a/2)T` |
| 一有一无 | `(1+ε)T/2` | T | `[3/2+(ε+a)/2]T` |
| 都无 heavy | T | 0 | `(1+a/2)T` |

有 heavy 的见证 medium≤T−h=εT。两见证都无 heavy 的机器在保留的 heavy 图中无任何边，最终也不可能新接 heavy。所有其他机器最终至多一枚 heavy，且真实时间≤T。

表的第一行≤目标 B，因为差为 `(1−ε)T/2>0`；第三行也≤B。第二行正是 B。故全部原机器同时满足目标界，与 mixed 的 heavy-presence 精确性相容。

## 6. 退化、端点限制与位复杂度

- ε=0 时 heavy 恰为 T，内部 heavy 替换增量为零；证明原生适用。
- a=0 时所有 medium 为零，舍入成本全零；没有除 a、按 1/a 展开或正成本假设。
- 相同原端固定；相同 virtual 目的机成本不同，选较便宜项并解码方向。静止 heavy 公共边保持原端，静止 medium 原 job 也保持原端。
- 所有分类与构造都只看两见证实际用过的端；其它有限端无论位于 gap、超过 T、为零或任意值，都不进入图或输出。
- `a<1−ε` 同时保证分类 gap 和 `ε+a<1`，从而 B<2T，并使单分量翻转界足够。
- 全图至多2n条原使用边，分量及 items 数 O(m+n)。排序、配对图二着色、方向恢复及逐原 job 输出均为显式输入规模多项式。所有实际成本是输入有理数，均值只多一个因子2；有理部分和的共同分母位长至多输入分母位长总和加常数。没有按 ε、a 或 gap 倒数展开。
- 边界保证 v,w 两个新 heavy 端点存在，所以 n=0 不形成满足完整输入合同的实例。

物理读出限制随 mixed 实际输出直接成立：当 β≥B/T，禁止混合的裸 heavy-presence 合同被反例调度击破；若 ε+a≤1−κ，则 B≤(2−κ/2)T。指定 job 身份、额外外部边界、源解码和无给定 strict 见证的情形均未被本证明覆盖。

**最终独立判断：新 Exact 全量词下成立；不声明全参数锐性或一般 UM 近似/困难性。冻结本文件后方可读取新作者 Proof。**
