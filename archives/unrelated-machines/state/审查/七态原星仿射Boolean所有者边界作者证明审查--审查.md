---
id: "unrelated-machines/seven-state-affine-boolean-owner-boundary-author-proof-v1"
kind: "review"
type_tag: "审查"
title: "七态原星仿射 Boolean 分类与 unit-owner 边界作者证明审查"
status: "integrated-author-proof-with-explicit-scope"
truth_status: "author-proof-scoped-algebraic-lemma-and-cross-background-obstacle"
review_level: "full-source-read-cross-object-comparison"
scope: "固定七态背景 Ω0 上的实仿射 Boolean 分类、M3 Gram 替换、unit-owner 至多二结论及跨背景物理高 degree 边界"
summary: "完整读取作者 Proof；核对 Ω0 正支持、h=1 与 h≥2 的系数分类、M3 正交到支持 Boolean、literal pair 互补性、B<2 unit-owner 结论和跨背景 N-job 反例。该页整合既有七态局部核审查，不将作者证明升级为独立盲审、一般 UM 算法、全局 owner degree 定理或 hardness。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_seven_state_affine_boolean_owner_boundary_author_proof_v1.md"
  - "clean:88ebc1313d383dd51280"
  - "related-source:01379acdbf1ccafd6d95:history/source/notes/unrelated_machines/sol_seven_state_affine_boolean_owner_boundary_exact_v1.md"
related_objects:
  - "鲁棒双端环与七态二次局部核双源审查--审查.md"
  - "七态星全局二次审计与root重放范围审查--审查.md"
  - "../计算/七态星全局二次审计与root重放边界--计算.md"
  - "仿射线结构边界合并稿的版本与分域复核--审查.md"
  - "身份耦合稀释raw-K2三源精读与锐二倍范围--审查.md"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/seven-state-affine-owner-boundary-v1/original/sol_seven_state_affine_boolean_owner_boundary_author_proof_v1.md"
---

# 来源身份与证据角色

本页处理 clean source `88ebc1313d383dd51280`，原路径为 `history/source/notes/unrelated_machines/sol_seven_state_affine_boolean_owner_boundary_author_proof_v1.md`，冻结 blob 为 `6c52a7fa2d5e46bf9bb314c962750be29b017fcc`，源 SHA-256 为 `b887d569b134bebe1a99172d2332d670e60088705e41764db24d775d2da97259`，大小 8,086 B。原文已逐字保存到 `evidence_paths` 所列目录。

来源标题为“七态原星：仿射 Boolean 分类与 unit owner 边界的作者证明”。它是 2026-10-18 的 scratch 作者 Proof，明确对应但不修改 statement-only `sol_seven_state_affine_boolean_owner_boundary_exact_v1.md`；来源内记录该 Exact 文件 SHA-256 为 `a38dfcf05158f38d93f1a26c54591944b8a662174018ece9f81388d499bef250`，对应 clean ID 为 `01379acdbf1ccafd6d95`。该 Exact 源尚未在本批导出实读，因此本页不把它写成第二份独立证明；只保留作者 Proof 对其对象的版本指向和全仓 inventory 身份。

本页的处置是 **integrated**：把作者 Proof 的独有代数分类、Gram-to-support 推理和跨背景物理反例整合到既有七态局部核审查链；同时保留“作者 Proof、非独立盲审”的证据角色。既有七态全局二次审计 JSON/root replay 已另有计算与审查页，本页不把有限 PSD 运行冒称为该分类的程序验证。

# 1. 七态背景与正支持

Exact 参数记号为 `d,s,η,h,p,u0,e`，满足

\[
2\le s\le d/2,\qquad \eta=s/d,\qquad h=s/2,
\]
并有 `0<η≤1/2`、`p≤1/8000`、`u0≤4p`。来源给出的常数估计是

\[
e\ge 4/5-5/8000>0.79.
\]

因此七个类别质量都严格为正，各类别中的每个 H-subset 也严格为正。证明的纯函数分类只需要

\[
\Omega_0=\{0,1\}\times\bigl(\{0^d,1^d\}\cup\{Y:|Y|=h\}\bigr),
\]
的全部正支持点；额外的 `C=0,H=d/2` slice 不参与分类。条件 `1≤h≤d/4` 是关键输入，边界 `h=d/4` 仍被覆盖。

这里的“支持”是固定背景下的正概率支持，不是仅由语法上出现的 endpoint 集合。后续正交和非负积分步骤都使用每个 Ω0 点具有严格正的真实 `P` 质量；若条件化或改变背景后支持缩小，必须重新建立同样的假设。

# 2. Ω0 上实仿射 Boolean 函数的完整分类

设实仿射函数

\[
f(C,Y)=a+bC+\sum_i c_iY_i
\]
在 Ω0 全部点取 0/1 值。

## 2.1 消去 C 与 Y 的混合

取 `Y=0`，得到 `a,a+b∈{0,1}`，所以 `b∈{-1,0,1}`。若 `b=1`，则 `a=0`。对任一大小为 h 的集合 F，`f(0,1_F)` 与 `f(1,1_F)` 相差 1 且两者都 Boolean，只能按 `0,1` 排列，因此

\[
\sum_{i\in F}c_i=0.
\]

比较共享 `h−1` 个索引的 `Q∪{i}` 与 `Q∪{j}` 得 `c_i=c_j`；再用 `h≥1`，全部 `c_i=0`，故 `f=C`。`b=-1` 同理给 `f=1-C`。

剩余情况为 `b=0`。若 `a=1`，先用 `1-f` 归约到 `a=0`。于是只需分类

\[
g(Y)=\sum_i c_iY_i,
\]
且它在全部 h-subsets 与全一向量上 Boolean。

## 2.2 h=1 的边界

每个 singleton 都在正支持内，所以每个 `c_i∈{0,1}`。全一向量又要求 `Σ_i c_i∈{0,1}`，故至多一个系数等于 1。于是 `g` 只能是 `0` 或某个 `Y_i`。恢复常数补操作，得到

\[
0,\quad 1,\quad C,\quad 1-C,\quad Y_i,\quad 1-Y_i.
\]

该分支覆盖最小允许参数 `d=4,s=2`，不需要额外假设 `d>4`。

## 2.3 h≥2 的两层分类

仍比较两个只交换一个索引的 h-subsets，得

\[
c_i-c_j\in\{-1,0,1\}.
\tag{1}
\]

若所有系数相等为 `c`，则 `hc` 与 `dc` 都属于 `{0,1}`；因为 `d/h≥4`，只能 `c=0`。

若不全相同，令 `c` 为最小系数。由 (1)，全部系数只可能落在 `c` 与 `c+1` 两层，且两层都非空。设高层大小为 `m`，低层大小为 `d−m`。一个 h-subset 内高层索引数 `k` 的可能值构成整数区间

\[
\max(0,h-(d-m))\le k\le\min(h,m).
\]

对应的 `g` 值为 `hc+k`，必须全部属于 `{0,1}`，所以区间宽度至多 1。由于 `d≥4h`，若高、低两层都至少有两个索引，则该宽度至少 2：两层都至少 h 时宽度为 `h≥2`；高层少于 h 时低层大于 h，宽度为高层数；低层少于 h 时对称。故至少一层只有一个索引。

若唯一高层为 `i`，h-subsets 的两个值是 `hc` 与 `hc+1`，只能为 `0,1`，于是 `c=0`，得到 `g=Y_i`。若唯一低层为 `i`，两个值是 `hc+h−1` 与 `hc+h`，只能为 `0,1`，即 `c=1/h−1`，得到

\[
g(Y)=H/h-Y_i.
\]

但全一向量的值为 `d/h−1≥3`，不是 Boolean，故唯一低层分支被排除。于是实系数分类完整地给出六类函数

\[
f\in\{0,1,C,1-C,Y_i,1-Y_i\}.
\]

这不是对整数系数的枚举，而是对全部实系数的分类。上边界 `h=d/4` 时唯一低层分支的全一值恰为 3，仍被排除；若擅自放宽到 `h=d/2`，则 `H/h-Y_i` 在零、h、d 三个 slice 上都 Boolean，却不是 literal，说明 `d/h≥4` 不能静默删除。

# 3. 从共同 M3 Gram 等式到真实支持上的 Boolean

固定一个新原 endpoint `X` 及其仿射候选 `f`，令 `G=X-f`。共同 M3 中的明确零向量关系给出

\[
\widehat L(GQ)=0\qquad(\deg Q\le3).
\tag{2}
\]

对 `r=1,2,3,4` 使用恒等式

\[
X^r-f^r=(X-f)\sum_{j=0}^{r-1}X^{r-1-j}f^j,
\]

其中第二因子次数不超过 3，故 `Lhat(f^r)=Lhat(X^r)`。原 Boolean 矩等式支付到次数四，得到

\[
\mathbb E_P[(f^2-f)^2]
=\widehat L(X^4-2X^3+X^2)=0.
\tag{3}
\]

被积函数逐点非负，而 `P` 对 Ω0 的每个支持点均为严格正，因此 `f` 在整个真实 P 支持上取 Boolean 值。第 2 节的六类分类即可应用。

这一推导依赖共同 M3 的零向量正交、次数四的原 Boolean identities 和正支持；仅有一阶相等不够。例如独立 Bernoulli(μ) endpoint 与常数函数 `f=μ` 可有相同一阶边际，但 `f` 不 Boolean，且 Gram 差范数为 `μ(1−μ)>0`。因此不能把“一阶边际相同”免费升级为支持上的 literal 分类。

对两个 endpoint `X,X'` 及相应 `f,f'`，用次数一乘子于 (2) 得

\[
\widehat L(XX')-\mathbb E_P(ff')
=\widehat L((X-f)X')+\widehat L(f(X'-f'))=0.
\tag{4}
\]

一阶替换同样成立。来源只使用共同 M3 的正交性；它没有声称 M2 完全不能给出任何类似结论，但本 Proof 的 degree-three 正交性不能归给 M2。

# 4. primitive bits 的 pair 支持与 unit-owner 结论

每个 `t∈{C,Y_1,…,Y_d}` 在 Ω0 上都取 0/1。任两个不同 primitive bits 的四种 joint pattern 在 Ω0 上都出现：`C,Y_i` 通过零/全一 Y 与 C 的两值获得；`Y_i,Y_j` 的 00 来自全零、11 来自全一、10/01 来自包含其中一个而不含另一个的 h-subset（由 `1≤h≤d−1` 保证）。这些点在 P 下全有正质量。

因此两个非零 literal/constant 的乘积期望为零，当且仅当它们是同一 primitive bit 的互补 literals。常数一与任意非零 literal/constant 的乘积期望严格正。

对指定 unit head `w` 的 endpoints，若普通矩阵配置目标 `B<2`，同一行不能同时放入两枚不同原 unit jobs。第 3 节已将被共同 Gram 关系覆盖的 endpoint 替换成真实 P 下 literals；第 4 节的 pair 支持于是给出：若存在两个正 owners，它们只能是同一 primitive bit 的两个互补 literals。

任何第三个非零函数都不可能同时与二者互斥，因为二者之和恒为 1；常数一也只能单独出现。因此，在该仿射 Gram 覆盖的 endpoint 子集上，正 owners 至多两个，而且二者必须是互补 literals。零一阶端点分类后，额外只能是常数零，不限制其原数量。

这是一个**受限 owner 结论**：它只限制被共同 M3/仿射关系覆盖的原 endpoints。原 one-hot 保留每个 job 的身份，但分类本身没有利用同一 job 的额外关系；不能忽略同 head 的非仿射 owner，再把“至多两个”写成整行所有物理 owners 的总 degree 界。

# 5. 跨背景条件化与物理高 degree 反例

逐固定背景使用本分类时，必须在该背景下重新拥有 Ω0 的全支持、共同矩和仿射/pair 条件。若条件化缩小了支持，或只有一个未条件化 M3，不能复用第 2–4 节的前提。

来源保留一个精确的跨背景反例。加入 `N` 枚不同原 jobs `J_alpha`，每枚只可在 `w` 与自己的不同 `u_alpha` 使用时间 1。令 β 独立均匀选 `[N]`；只有 `J_beta` 随 C 在 `w/u_beta` 间切换，其余 `J_alpha` 始终留在各自 `u_alpha`。每枚 job 仍完整执行。

固定 β 后，新 endpoint 只仿射依赖 `C`（以及常数 0、1），且每个背景只有一个正 owner 可到 `w`。但跨 β 的 `w` 边际为

\[
\Pr(J_\alpha\to w)=\Pr(C=1)/N=(1/10+p)/N>0.
\]

任意两个不同 `J_alpha` 的 `w` indicators 点态互斥，因而 pair 仍为零；`w` 的 unit 总负载为 `C`，其它新增机器负载为 1 或 `1−C`，全部不超过 1。于是全局可有任意大的物理 unit 资格数 N，同时每个固定背景仍只有一个正 owner。该全局函数依赖 β，不能改称只仿射依赖同一组 `C,Y` 的 fiber 反例。

这说明 fiber 内的 affine owner 分类不等于全局物理入度界，也说明新增物理 jobs 与跨背景路由必须写进完整共同 law。该例有所有新增 jobs 回自己的 private home 的峰值 1 调度，不能被解释为 actual near-two gap 或 hardness。

# 6. 与既有七态对象的关系

《鲁棒双端环与七态二次局部核双源审查》已记录同一七态原星的实际 OPT=1、共同 M3、全局 degree-two physical-load localizer、逐行 CONFIG first/pair、Fisher–Yates 稀疏支持，以及仿射 Boolean owner/忠实 AND 的边界。当前 Proof 的独有增量是把 affine owner 部分写成自足实系数分类：h=1、h≥2 两层系数、`h=d/4` 边界和 `h=d/2` 域外反例，并显式说明 M3 Gram-null 如何把仿射候选落回真实 P 支持。

《七态星全局二次审计与 root 重放范围审查》及其计算页只认证 12 组有限参数的 Fraction PSD/秩/assignment 字段和一次作者/root 输出字节一致；JSON 的 `not_checked` 明列 affine classification software、deep shared-owner law、AND extension、general scheduling 和 SDP finder。故当前 Proof 不应被有限 audit 的 exact PSD 字段替代，也不能把审计通过解读为任意 `d,s` 的程序证明。

《身份耦合稀释 raw-K2 三源精读与锐二倍范围》是另一 raw K2 typed certificate 与完整 ordinary jobs gap，涉及多个物理 owner 和 global affine localizers；它提示 raw M2、CONFIG pair 与更高阶或跨行共同 law 必须分开。当前七态 fiber 分类不能直接扩展到 raw-K2 全局物理 degree，也不提供二倍上界或一般 hardness。

同样，本页与仿射线合并稿的版本审查只共享“仿射结构必须保留支持、量词与版本范围”的方法边界；它们不是同一个七态 owner 对象。当前 Proof 没有新增生产实现、没有运行软件、没有外部文献新颖性认证。

# 7. 证明级别、已确认项与缺口

**在来源明确范围内确认：**

- `1≤h≤d/4`、正支持 Ω0 和七类别正质量条件下，实仿射 Boolean 函数完整分类为 `0,1,C,1−C,Y_i,1−Y_i`；
- 共同 M3 的零向量正交加次数四 Boolean identities 足以把仿射候选落实为真实 P 支持上的 Boolean；
- 在 `B<2` 的 unit-head 配置且仅对 Gram 覆盖的 affine endpoints，正 owners 至多两个，两个只能是同一 primitive bit 的互补 literals；
- 跨背景 N-job 构造可在每个 fiber 只有一个 owner 时产生任意大的全局正物理资格数，同时保持完整 jobs 与峰值 1 的 private-home 调度。

**本来源没有确认：**

- Exact counterpart 的独立证明或 independent blind review；
- 任意条件化后仍自动存在 Ω0 全支持的结论；
- 非仿射 endpoint、`AND`/乘积 endpoint、深层 shared-owner/common-law 的可行性；
- 所有物理 owners 的总 degree 上界；
- 任意 growing-depth 接线、一般 UM 调度算法、SDP finder、near-two gap 或 NP/UGC hardness。

该作者 Proof 是有限代数 lemma 加物理 scope 反例，不是一般不可能性定理。后续若要把 fiber 结论用于构造，必须对每个背景重新给出正支持、共同 M3、Gram-null 和完整 jobs/负载合同；若要加入跨背景路由，则应把背景变量显式纳入共同 law，而不是把逐 fiber owner 数相加。

# 8. 结论

本页将 `88ebc1313d383dd51280` 归档为既有七态原星局部核的作者证明增量：它严格解释了在 `h≤d/4` 的正支持 slice 上，仿射 Boolean endpoint 只能复制 primitive literals，并由共同 M3 Gram 等式把候选落实到真实 law；在 `B<2` 的相应 unit owner 子集上，正 owner 数至多两个。跨背景 N-job 例子同时证明这一 fiber 结论不能升级为全局物理 degree 界。

所有结论必须携带其参数、支持、共同矩和 endpoint 覆盖条件。该记录与已有七态有限审计、七态局部核解析证明和 raw-K2 证据保持分层；没有新 Claim、软件运行、一般算法、hardness 或外部新颖性认证。
