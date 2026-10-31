---
id: "unrelated-machines/near-unit-implication-pcsp-review"
kind: "review"
type_tag: "审查"
title: "近单位 PCSP 蕴含与物理复制义务最终范围审查"
status: "integrated-with-physical-hardness-open"
truth_status: "general-pcsp-hardness-scoped; physical-UM-reduction-unclosed"
review_level: "full-source-read-cross-object-and-correction-comparison"
scope: "strict/weak near-unit PCSP minion、一般 NP-hardness、native multi-small flow、ternary unit-selector normal form、unit-presence gluing 与后续读后纠错"
summary: "完整读取 35763d19e84e87d2e95a 审查记录并与已归档 canonical PCSP/presence 对象、后续 native/ternary 纠错和有限稀疏审计比较。记录确认一般约束图 PCSP 的精确 minion 与 NP-hardness，但物理 UM 编译、任务出现次数、端口/one-hot、完整调度 decoder 和近二 hardness 仍开放。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/near_unit_implication_pcsp_review.md"
  - "clean:35763d19e84e87d2e95a"
  - "related-source:29d4881762b3773ed35d:research/current/unrelated_machines/near_unit_implication_pcsp_and_physical_copy_obligation.md"
  - "related-source:56ab7cc3466f397ebcfe:research/current/unrelated_machines/unit_presence_two_witness_sharp_gluing.md"
related_objects:
  - "近单位PCSP与单位presence胶合双源审查--审查.md"
  - "PCSP最大最小分配与投影博弈平行重复三篇文献整理--文献.md"
  - "原任务标签提升的一阶PSD与全语境容量块--证明.md"
  - "根树流环正规化与有向需求桥冻结审查--审查.md"
  - "rawSH3真困难性流与容量切最终边界--资料.md"
  - "原作业SH3子树流与包含容量双源续审查--审查.md"
  - "单token共同资格与端点成本--障碍.md"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/near-unit-implication-pcsp-20261031/original/near_unit_implication_pcsp_review.md"
---

# 来源身份、冻结顺序与处置

本页处理 clean source `35763d19e84e87d2e95a`，原路径为 `research/reviews/unrelated_machines/near_unit_implication_pcsp_review.md`，冻结 blob `51801cb5bf9bc40a70aef73a62a190bfa890f3b8`，源 SHA-256 `9ee1c800ceccb7d49dcd5addc9c80ce927ec66a7399cc05077f89e7792fb1749`，大小 8,821 B。原文已复制到 `evidence_paths`。

该记录保存一条较长的审查链，而非单个新 Claim。其先后关系必须保留：先有 necessary-fixing/一般 PCSP hardness statement 和独立重构，再读取作者 Proof 与充分性 addendum；随后以两个精确 ID 再核 strong-fixing/hardness；再读取 root 独立 canonical 与读后稿；最后补 native 多-small、ternary selector normal form 和稀疏审计的实际读后纠错。记录中列出的 scratch SHA 只作为阅读顺序和版本 provenance，不把后见之明倒填成盲审。

本页处置为 **integrated-with-physical-hardness-open**：将一般约束图 PCSP 的精确代数/复杂度结论、物理 copy obligations 和后续纠错整合到既有 near-unit/SH3/token 证据链；明确不把它们升级成 ordinary UM makespan hardness、generic SDP、近二算法或 `UM-TARGET-v1` 结论。

# 1. Strict/weak near-unit PCSP 与精确 minion

## 1.1 模板与 promise 量词

固定 `k≥2`、`1≤r≤k−1`，底域为 `{0,1}`。约束模板包含

\[
A_k(b,x_1,\ldots,x_k)iff b=0\ \lor\ \sum_i x_i\ge k-1,
\]
\[
B_{k,r}(b,x_1,\ldots,x_k)iff b=0\ \lor\ \sum_i x_i\ge r,
\]

以及

\[
AMO_2=\{(0,0),(0,1),(1,0)\},\qquad ONE=\{1\}.
\]

strict 实例要求映射到严格模板，weak 实例允许映射到放宽模板；promise 语言量词是 strict 可满足与 weak 不可满足之间的区分。一般约束图允许变量重复、任意多次出现和任意连接，不带 DAG、端口次数、物理 job 出现次数或 one-hot 复制承诺。

## 1.2 Polymorphism 的完整分类

来源记录的精确身份为：对于任意 arity `n`，Boolean 函数 `f` 是该模板的 polymorphism，当且仅当：

1. `f` 单调；
2. `f` 的 winning-support 族非空且两两相交；
3. 每个 inclusion-minimal winning support 的大小至多 `C=k−r`。

每个 minimal winner 同时是双侧 strong C-fixing set。`r=k−1` 时 `C=1`，只有 projections；`C≥2` 时存在任意大的 essential arity，例如

\[
x_1\land(x_2\lor\cdots\lor x_n).
\]

这一步是 minion/函数层的全称分类，不是对物理机器任务的分类。

### 必要性

- `ONE` 排除空 winning set；
- `AMO_2` 排除两个不相交 winning sets；
- `A_k` 的矩阵替换排除不单调；
- 取一个大于 `C` 的 inclusion-minimal winner 并构造相应的 `A_k/B_{k,r}` 行，排除 minimal winner 大小超过 `C`。

### 充分性与 active rows

给定单调、相交且 minimal winner 大小≤`C` 的 `f`，在 incoming support 中取一个 minimal winning set `S`。只对这些 active rows 进行计数：不包含 `S` 的输出列至多 `|S|` 个，至少 `k−|S|≥r` 个列包含 `S`，因而 weak 关系成立。缺失 `S` 元素的输出列不要求互异；并集上界已经足够。该 active-support 量词是充分性证明的重要边界，不能误读为“所有 rows 都 active”或只检查被选 row 而遗漏 inactive rows。

# 2. 一般 PCSP NP-hardness 与普通 CSP 迁移边界

## 2.1 Strong C-fixing 与 minion homomorphism

对固定 `k,r`，`C=k−r` 是常数，identity minion homomorphism 把该模板的 polymorphisms 送入 Boolean strongly C-fixing minion。依据 BBKO v3 的 PCSP 代数归约条件，得到一般 promise PCSP 的 NP-hardness。

该结论的复杂度对象是一般有限约束图上的 promise decision；它没有给出 ordinary UM 的 makespan gap，也没有给出 source-to-UM 的 Karp/PCP reduction。不能把“PCSP NP-hard”省略 promise、模板或函数层假设后写成一般物理调度 hardness。

## 2.2 Feder/KKR 的普通 CSP 边界

普通 Feder 非-delta-matroid edge-CSP 或 KKR 普通 CSP/edge-CSP 定理不能原样替代 strict/weak promise。固定一个 coordinate 后，strict 端仍要求其余出口几乎全为 1，而 weak 端可以用被量化出口支付配额；当 `r≤k−3` 时 weak projection 甚至成为完整 Boolean cube。自足投影公式表明：pin 一个 `out0`、量化 `k−3` 个 `out`，strict 分支强迫 `y=z=1`，weak 分支只要求

\[
y+z\ge\max(0,r-k+3).
\]

所以普通 non-delta 结论没有直接提供 near-unit soundness。该负结果只禁止直接搬运 ordinary theorem，不排除设计更大 promise gadget 或其它 source。

## 2.3 PCSP 与文献对象的分离

BBKO 的 minion/PCSP 结论、Bateni–Charikar–Guruswami 的 MaxMin allocation、Dinur–Steurer 的 projection-game parallel repetition 是不同模型：前者是 strict/weak homomorphism promise，后者分别是 additive allocation 和二玩家 projection game。它们可作为复杂度背景，但不能直接转成客户目录、均分 payoff 或 ordinary UM continuation theorem。

# 3. 物理 UM 编译的真实 obligations

## 3.1 关系类型与 one-hot 身份

若有限 processing times 只使用 `{1,1/k}`，`C<2` 时 unit incoming 至多一件；但每个真实任务的两端关系必须按物理方向分类：

- `1/k→1` 是 out–in；
- `1→1` 是 in–in；
- `1/k→1/k` 是 out–out NEQ；
- 不存在可免费补入的 out–out EQ。

普通 UM 允许三端以上任务；一个多端任务不能被当成可复制的多个 Boolean occurrences。端口有限数也不等于源变量可任意复用。必须同时证明：YES 源映射到完整 ordinary UM 调度，所有原 jobs 一次执行；NO 的每个低 makespan 调度可解码 weak source assignment；机器/任务数和有理位长保持总多项式。

## 3.2 Near-two grid 条件

只有当具体 compiler 保持 `{1,1/k}`，并且 NO 实例不存在 `C≤2−r/k` 时，才能把物理 gap 推到 `C≥2−(r−1)/k`，对应比率 `2−(r+1)/(k+1)`。若 `r=2` 且对任意大 `k` 具有真正 physical hardness，才可能支撑主反面；当前 compiler 尚未提供这一物理 hardness，必须标为 OPEN。

## 3.3 Native multi-small flow

`UM-MULTISMALL-INCIDENCE-FLOW-APPROX-v1` 的后续陈述给出一条结构化正面边界：在 `{1,1/k}` 时间合同下，把没有 small 端的任务用 unit matching 得到瓶颈 `B`，其余任务用 small-end capacity flow 得到 `F`，输出完整实际调度

\[
C_{\max}\le B+F/k\le B+\max_i\lceil\rho_i\rceil/k,
\qquad
\rho_i=\sum_{j:i\in S_j}1/d_j.
\]

在 small 任务端点数 `D≥2`、每台机器关联数不超过 `k` 时，有至多 `5/3` 的边界；在 `d_j≥k` 且 small 行关联≤`k` 时，`T=1+1/k` 可行当且仅当 Q 存在 unit matching，matching 失败则 `OPT≥2`。这是完整整数流，说明很多均匀多端 source 会落入易解域；它没有构成一般 hardness。

记录的后续读后纠错把 one-small 下界独立加强到 `k−3`（早期草稿曾保留 `k−2r+1` 路线），并明确 unit 机器 A 与 small 机器 `M_i` 必须互异；这些是 native-flow scope 修正，不能追溯改变前述一般 PCSP Claim。

# 4. Ternary unit-selector normal form 与有限实现

`UM-TERNARY-UNIT-SELECTOR-NORMAL-FORM-v1` 用每个原任务的一棵私有二叉树把任意有限端选择压成单位容量结构：根 pin、内部 unit jobs、叶 port jobs。任意原 schedule 可映到新实例，峰值不超过 `max{b,C}`；新实例在 `C<2b` 的完整 schedule 可沿树反解为原 schedule。该正规形保持 small 资格计数，新增机器不带 small 端。

必须保留以下边界：

- `C≥2b` 时不能调用反解；
- `p>b` 的资格必须先删或判阈值超限；
- 正规形不会自动复制原任务，也不会提供 source decoder 或 hardness；
- native 多端任务的 one-hot/one-cold 关系和非 DAG 反馈端都必须显式保留。

后续 actual-read 记录还确认了 `n0` 空输入、`p0/d1` 边界、严格 `C<2b`、`OPT=b` 与 `2b` baseline、剪枝范围、所有物理机器非负子集负载以及 dense/sparse 编码和有理尺度数。上述是数学范围核对，不是一般 compiler 的完成。

有限 sparse audit 只承担实现回归：9 个关键原输入、13 个原调度 `σ`、116 个新完整 `τ`，其中 29 个 `C<2b` 实例逐件投影且核对原机器负载不增；还覆盖大 bit-length、`m=2^80` empty/few-edge、`q0`、`d1`、`b=7/5`、跨 `b/2b` 的 OPT、`p>b`/负值拒绝、`b=0` 和 `C=2b` 拒绝。它不能替代 normal-form 的一般证明，也不实现 generic PCSP solver 或一般 UM 算法。

# 5. Unit-presence 胶合与“裸 Boolean”反面

现有 two-witness unit-presence 对象说明一个自然 Boolean 复制接口的限制：给定同一 ordinary UM 实例的两份完整 schedule `σ0,σ1`，两台测量机在两份见证中分别都不含 unit 或都含 unit；任意 mixed presence pattern 可用 matching union、machine-machine/job-machine 路径和整数 small flow 胶合，得到全部 jobs 一次执行、峰值

\[
B(k)=1+\frac{\lceil(k+2)/2\rceil}{k}.
\]

四机 `2k+6` jobs 的族对该裸 presence 合同给出锐下界，`B(k)→3/2`。tiny `[0,a]` 和 heavy/medium 版本把结论扩展到相应两端成本，但仍要求两份**实际完整 witness**。

因此，单纯把 source variable 解释成“某台机器是否有 unit job”不能锁定 weak assignment；两 witness 胶合会自动产生低于 2 的 mixed schedules。要避免该逃逸，需加入任务身份、共同外部容量、端口限制或独立 source decoder，且不能把 virtual item 当新增执行任务。

这和 PCSP 一般 hardness 是互补边界：PCSP 只保证抽象 strict/weak 约束难，presence 胶合说明一个自然物理接口会破坏 soundness。二者不能合并成已完成的 physical hardness reduction。

# 6. 证据顺序、软件与文献边界

本来源列出了多条 Exact-first、作者 Proof、root canonical/read-after 的 SHA 链，均保留其实际阅读顺序。它还明确：

- 未以 scratch 小真值表替代一般 PCSP 证明；
- 未签作者代码、路径修复、`ROOT=Path.cwd()` 修改或一般 compiler 运行；
- 未读取/认证 BBKO、KKR、Feder 全部证明，只核指定 PDF 页与引用事实；
- 有限 sparse audit 不承担一般 normal-form theorem；
- 外部同行评议、新颖性、ordinary UM hardness、`UM-TARGET-v1` 与六人 SPE 仍未认证。

因此，读后稿的 `no standing fatal` 是所述 scope 内的内部一致性结论，不是 external certification。相关文献资料页、raw SH3 flow/inclusion 资料和 token-label/anonymous M2 审查都保持独立：SH3 提供必要 flow/cut，token-label 提供 aggregate-to-labelled nonextension，PCSP 提供 minion/hardness，但没有一条自动提供完整 physical decoder。

# 7. 已确认项、缺口与处置

**可以安全引用：**

- 近单位 strict/weak Boolean PCSP 的 polymorphism/minion 精确分类；
- 固定 `k,r` 的一般 promise-PCSP NP-hardness（strong C-fixing identity，`C=k−r`）；
- 普通 Feder/KKR 定理不能直接承担该 weak promise soundness；
- `{1,1/k}` native multi-small 的整数流/易解边界与后续 `k−3` one-small scope 修正；
- ternary selector normal form 在 `C<2b` 下的 schedule preservation/反解合同；
- 两份实际 low schedules 的 unit-presence 胶合 sharp `B(k)`，以及 tiny/heavy-medium 的相应 witness-dependent 扩展；
- sparse normal-form audit 的有限样本与明确未覆盖项目。

**仍然开放：**

- 将 PCSP source 编译为满足任务出现次数、端口类型、one-hot 和全机负载的 ordinary UM；
- 对每个低 makespan physical schedule 解码 weak source assignment；
- 在 unit-presence 胶合逃逸之外加入任务身份/容量锁定而不落入 native-flow 易解域；
- 处理多端、混合尺度、反馈环和 non-DAG 结构的全局 soundness；
- generic exact SDP/PCSP finder、一般 UM 近二算法/硬度、source decoder 或 `UM-TARGET-v1` 结论。

处置为 **integrated**：将本审查的精确 minion、一般 hardness、物理关系分类、后续 native/ternary 纠错和 presence 反面接入现有 near-unit/SH3/token 存档；不创建新的 physical-hardness theorem，也不把一般 PCSP hardness 或有限软件审计当作普通 UM makespan 困难性。

# 8. 结论

`35763d19e84e87d2e95a` 的稳健结论分成两层：抽象层上，near-unit strict/weak PCSP 有明确 polymorphism/minion 分类和固定模板 NP-hardness；物理层上，任务端点关系、出现次数、端口和完整调度 decoder 尚未满足足以传递该 hardness 的合同。native multi-small flow 与 ternary normal form 给出的是正向易解/结构保持边界；two-witness unit-presence 胶合则展示裸 Boolean presence 接口会产生低于 2 的 mixed schedules。

后续引用必须同时注明 promise-PCSP、strong C-fixing、active support、physical endpoint relation、`C<2b` 反解、两份实际 witness 和有限 audit scope。任何“near-unit PCSP 已解决 ordinary UM near-two hardness”的表述均超出本对象证据范围。
