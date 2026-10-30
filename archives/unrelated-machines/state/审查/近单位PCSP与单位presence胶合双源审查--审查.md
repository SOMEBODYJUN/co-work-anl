---
id: "unrelated-machines/near-unit-pcsp-presence-gluing-review"
kind: "review"
type_tag: "审查"
title: "近单位PCSP与单位presence胶合双源审查"
status: "integrated-with-physical-copy-obligations"
truth_status: "general-PCSP-and-structured-gluing-results; physical-UM-reduction-open"
review_level: "full-source-read-and-cross-archive-comparison"
scope: "near-unit strict/weak PCSP source, native multi-small flow boundaries, ternary selector normal form, and two-witness unit-presence gluing"
source_refs:
  - "source:29d4881762b3773ed35d:research/current/unrelated_machines/near_unit_implication_pcsp_and_physical_copy_obligation.md"
  - "source:56ab7cc3466f397ebcfe:research/current/unrelated_machines/unit_presence_two_witness_sharp_gluing.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/near_unit_implication_pcsp_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/unit_presence_two_witness_gluing_review.md"
legacy_ids:
  - "UM-NEAR-UNIT-PCSP-EXACT-MINION-v1"
  - "UM-NEAR-UNIT-PCSP-UNRESTRICTED-HARDNESS-v1"
  - "UM-MULTISMALL-INCIDENCE-FLOW-APPROX-v1"
  - "UM-TERNARY-UNIT-SELECTOR-NORMAL-FORM-v1"
  - "UM-TWO-MEASUREMENT-UNIT-PRESENCE-SHARP-GLUING-v1"
  - "UM-TWO-MEASUREMENT-TINY-PRESENCE-GLUING-v1"
  - "UM-HEAVY-MEDIUM-STRICT-WITNESS-PRESENCE-GLUING-v1"
---

# 1. 实读范围与核心分界

本批完整读取两个当前 canonical 正文、inventory 指纹、既有审查、PCSP 原始文献事实和 unit-presence 胶合审查。源 `29d4881762b3773ed35d` 路径为 `research/current/unrelated_machines/near_unit_implication_pcsp_and_physical_copy_obligation.md`，SHA-256 `17b9a0fd3169f7b49bfcd279f17d300c4b2b4cced02be69f1deb05939da97307`，32780 bytes；源 `56ab7cc3466f397ebcfe` 路径为 `research/current/unrelated_machines/unit_presence_two_witness_sharp_gluing.md`，SHA-256 `0b9ab7d50bba3b4b7c5825c6208e51d23d20cdb5460d8e7478a6ef866f986e00`，20393 bytes。两源均来自冻结提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`。

第一源闭合的是一个**一般约束图**上的 strict/weak PCSP minion 与 NP-hardness 来源，并同时记录把它编译成物理 UM 时仍缺失的任务出现次数、端口和共同调度义务。第二源闭合的是：给定同一个 UM 实例的两份实际完整见证，按两台测量机的 unit-presence 指定任意混合位，仍可用真实全部任务构造一个有限峰值调度。两者不能拼成“PCSP hardness 已经是 UM hardness”：第一源的通用实例没有物理任务合同，第二源的胶合算法需要两份实际 YES 见证。

# 2. 近单位 strict/weak PCSP：代数结论与一般源困难性

## 2.1 模板和精确 minion

固定 `k>=2`、`1<=r<=k-1`，底域 `{0,1}`。关系为
\[
A_k(b,x_1,\dots,x_k)\iff b=0\ \lor\sum_i x_i\ge k-1,
\]
\[
B_{k,r}(b,x_1,\dots,x_k)\iff b=0\ \lor\sum_i x_i\ge r,
\]
并有 `AMO_2={(0,0),(0,1),(1,0)}` 与 `ONE={1}`。strict 全约束可满足与 weak 全约束不可满足构成 promise PCSP；一般约束图允许变量重复、任意多次出现和任意约束连接，不带 DAG/端口次数/任务出现次数承诺。

稳定身份 `UM-NEAR-UNIT-PCSP-EXACT-MINION-v1` 的结论是：对任意 arity `n`，Boolean 函数 f 是 polymorphism 当且仅当它单调、winning-support 族非空且两两相交、每个 inclusion-minimal winning support 大小至多 `C=k-r`。每个这样的 minimal winner 同时是双侧 fixing set；`r=k-1` 时只有 projections，`C>=2` 时可有任意大的 essential arity（例如 `x_1 and (x_2 or ... or x_n)`）。

必要性由 ONE 排除空 winning set、AMO 排除不交 winning sets、A_k 矩阵排除不单调以及排除大小大于 `k-r` 的 minimal winner；充分性必须处理 inactive rows：在 active incoming support 中取一个 minimal winner S，未包含 S 的 outgoing 列至多 |S| 个，至少 `k-|S|>=r` 列包含 S，故 weak 关系成立。该点防止把证明误读成只检查被选的 active rows。

## 2.2 一般 PCSP NP-hardness 和 Feder 边界

稳定身份 `UM-NEAR-UNIT-PCSP-UNRESTRICTED-HARDNESS-v1`：对每个固定 `k,r`，上述一般 PCSP NP-hard。证明依赖已实际读取的 Barto–Bulín–Krokhin–Opršal 定理：若 polymorphism minion 同态进入 Boolean strongly C-fixing minion，则 PCSP NP-hard；这里 identity homomorphism 直接适用，`C=k-r` 是常数。该结论只关于 promise decision，不是 makespan 近似比、实际 UM 编译或 `UM-TARGET-v1`。

普通 Feder 非 delta-matroid edge-CSP 定理不能原样替代 strict/weak promise。pin 一个坐标后，strict 关系仍是“incoming=0 或其余出口全 1”，而 weak 端可由被量化出口支付配额，`r<=k-3` 时甚至成为完整 Boolean cube；因此普通 non-delta 见证失去 weak soundness。该失败只否定把 ordinary theorem 直接移用，不排除更大 promise gadget 或其他 source。

## 2.3 物理编译真正的义务

若所有有限时间仅为 `{1,1/k}`，C<2 时 unit incoming 至多一个，机器的 small-out 数量产生 `r` 配额下界；但真实 UM 任务的两端关系必须逐类区分：`1/k-1` 是 out-in，`1-1` 是 in-in，`1/k-1/k` 是 out-out NEQ。一般 UM 允许三端以上任务；一个多端任务也不能被当作可复制的多个 Boolean occurrences。真正尚未闭合的反面义务是：把一个已 hard 的 PCSP source 编译成显式普通 UM，YES 有统一低 makespan，并且每个低负载实际调度都能解码 weak source assignment，保持全部任务/机器负载和总位多项式。只有完成这一步，PCSP hardness 才能传到物理 UM。

## 2.4 native 多 small 的流边界

`UM-MULTISMALL-INCIDENCE-FLOW-APPROX-v1` 给出一条结构化正面结果：时间仅 `{1,1/k}` 时，把没有 small 端的任务 Q 用 unit 二部容量流求最小机器 unit 瓶颈 B，把其余任务 R 用 small 端容量流求 F，则输出完整实际调度
\[
C_{max}\le B+F/k\le B+\max_i\lceil\rho_i\rceil/k,
\quad \rho_i=\sum_{j:i\in S_j}1/d_j.
\]
若每个 small 任务至少 D>=2 个 small 端且每台机器 small 关联数不超过 k，则给出至多 `5/3` 比率；若 `d_j>=k` 且 small 行关联不超过 k，strict `T=1+1/k` 可行当且仅当 Q 有 unit matching，matching 失败时 OPT>=2。这个算法是完整整数流，不把均匀分数分配当实际执行；它说明若 source 只产生这类均匀多端合同，native 实例会落入易解边界。

## 2.5 三端 unit selector 正规形

`UM-TERNARY-UNIT-SELECTOR-NORMAL-FORM-v1` 用每个原任务的一棵私有二叉树把任意有限端选择压成单位容量结构：根 pin、内部 unit jobs、叶 port jobs；任意原 schedule 可映到新实例，且新实例峰值不超过 `max{b,C}`；新实例任意 `C<2b` 的完整 schedule 可沿树反解为原 schedule。对 `{b/k,b}` 时间仍保持 small 资格数，新增机器不带 small 端。它是物理复制/选择的正规形，不能被用来复制原任务或默认建立 source decoder；边界 `C>=2b` 不可解码，`p>b` 的资格必须先删或判阈值超限。

# 3. 两份实际见证下的 unit-presence 胶合

## 3.1 精确单位结论

稳定身份 `UM-TWO-MEASUREMENT-UNIT-PRESENCE-SHARP-GLUING-v1`。输入任意显式 UM，时间集合 `{1,1/k}`，两份同一实例的完整调度 `sigma_0,sigma_1` 峰值均不超过 `T=1+1/k`。定义 `U_i(sigma)` 为机器 i 是否执行至少一件 unit job；两台不同测量机 v,w 在两个见证中分别均为 0 与均为 1。给定任意 mixed bit 向量，可确定性构造完整实际调度，全部任务各执行一次，峰值
\[
B(k)=1+\lceil(k+2)/2\rceil/k.
\]
四机 `2k+6` 任务、每任务恰两端的族使两见证恰 T、每个 mixed 最优值恰 B(k)，故该裸 presence 合同在声明域内锐；`B(k)->3/2`，但不能称一般 3/2 近似。

## 3.2 matching union、共同流与全机负载

两见证中的 unit 边各是一份 matching，因为 `T<2`。并图分成 machine-machine、job-job、job-machine 路径和偶环。指定一个测量机为 0 时选择相应分量方向；若它在 job-machine 路径，单分量翻转只增加一个已知 small 端，负载至多 `T+1/k`。其他情形把 machine-machine 分量选定、job-machine 分量 active，剩余两见证均为 small 的真实 job 及 job-job virtual item 构成二部流；两见证各半给出分数满流，机器容量取 `ceil(mu_i)` 后由整数性得到完整原端选择。virtual item 只编码路径方向，不是新增执行任务。

逐机分类是证明关键：两见证均 unit-present 的机器最终至多一件 unit 且 small 数至多 1；presence 不同的机器 small 数至多 `ceil((k+2)/2)`；两见证均 vacant 的机器不新增 unit 且 small 数至多 `k+1`。所有原任务同一流中一次性恢复，峰值不超过 B(k)，没有只检查测量端而遗漏其他机器。

## 3.3 tiny、heavy-medium 扩展及 sharp 族

`UM-TWO-MEASUREMENT-TINY-PRESENCE-GLUING-v1` 将 tiny 时间扩展到任意 `[0,a]`、`a<1`，两见证峰值 `1+a`，给出全部 mixed 的 `3/2(1+a)`。证明用每项两端的半分数、每机按成本排序配对和 job-pair/机-pair 图二染色，舍入误差至多 `a/2`；它不要求 tiny 成本相同，但仍需两份真实见证。`UM-HEAVY-MEDIUM-STRICT-WITNESS-PRESENCE-GLUING-v1` 进一步把见证端分成 medium `[0,aT]` 与 heavy `[(1-epsilon)T,T]`，在 `a<1-epsilon` 时给
\[
C_{max}\le[3/2+(epsilon+a)/2]T<2T
\]
并只允许每个任务使用两个见证端。它保留 heavy-presence，而非具体 job identity；medium/heavy 交叉和静止 job 都在声明域内。

这些胶合结论依赖两份**实际完整见证**，不接受一个分数点、未知存在量词或替代的 LP/PCSP oracle。严格四机族把 `B(k)` 的下界做成每个 k 的真实 OPT，不能因取大 k 把该局部 sharp 例写成一般 UM 近二下界。

# 4. 两源关系、反面用途和未闭义务

共同结构是“局部关系有精确数学描述，但全局物理实现仍需额外合同”。PCSP 源的 minion/NP-hardness 只解决一般约束图；presence 胶合说明一个很自然的裸 Boolean 复制接口，在有两份 YES 见证时会自动产生低于 2 的 mixed 调度，从而阻止用“同一实例的 unit 占用位”作为唯一锁定机制。它们不能合并成已完成的 UM hardness 归约，也不能把胶合算法反向当作 source solver。

第三阶段关系图可记录：

- `strict/weak near-unit PCSP` → `exact minion + general NP-hardness` → `physical copy/port obligation remains`；
- `two actual low schedules` → `unit matching union + integer small flow` → `all four presence patterns under B(k)`；
- `native {1,1/k} multi-small + row budget` → `integer flow` → `5/3 or exact T0`，标记为易解边界；
- `ternary selector normal form` → `preserves actual schedule under C<2b`，但不提供 decoder/hardness。

开放义务包括：构造满足任务出现次数、端口类型和全机负载的 PCSP-to-UM 编译；在 unit-presence 胶合之外加入任务身份、共同外部容量或 source decoder 的锁定；处理多端/混合尺度而不落入 native flow 的易解合同；以及证明真实 YES/NO promise 的全局 soundness。没有一项来源给出 `UM-TARGET-v1` 或六人 SPE 模型的结论。

逐源处置：

- `29d4881762b3773ed35d`：`integrated`。exact minion、一般 PCSP hardness、Feder promise 失败、多-small flow、ternary selector 正规形和物理编译义务写入第 2、4 节。
- `56ab7cc3466f397ebcfe`：`integrated`。unit-presence sharp B(k)、matching union/流胶合、tiny 与 heavy-medium 扩展、四机锐族和裸 presence 反面用途写入第 3、4 节。

两源均为全文件实读，相关审查/程序/文献事实已比较；独有内容去向、结构域限定与开放数学义务均已记录。
