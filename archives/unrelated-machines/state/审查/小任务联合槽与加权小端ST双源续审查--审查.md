---
id: "unrelated-machines/tiny-work-weighted-small-st-continuation-review"
kind: "review"
type_tag: "审查"
title: "小任务联合槽与加权小端ST双源续审查"
status: "integrated-with-conditions-and-boundaries"
truth_status: "scoped-general-proofs; finite exact audits retained; no-general-UM-algorithm"
review_level: "full-source-read-and-cross-archive-comparison"
scope: "tiny-work joint slot rounding and selector stability barrier; weighted small-end ST density barrier"
source_refs:
  - "source:ccda5c07c46ee14b1bcb:research/current/unrelated_machines/tiny_work_stability_joint_rounding_and_selection_barrier.md"
  - "source:acb99150324dcb0d1a48:research/current/unrelated_machines/weighted_small_st_barrier.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/tiny_work_stability_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:tests/audits/unrelated_machines/tiny_work_stability_joint_rounding.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:tests/audits/unrelated_machines/tiny_work_stability_selection_audit.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/mixed_small_endpoint_density_flow_barrier.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:archives/unrelated-machines/state/审查/多小端密度流障碍与单位读出校准槽双源审查--审查.md"
legacy_ids:
  - "UM-TINY-WORK-STABILITY-JOINT-ROUND-v1"
  - "UM-TINY-WORK-STABILITY-SELECTION-NP-v1"
  - "UM-SELECTOR-TINY-ROOT-THREE-VALUES-v1"
  - "UM-WEIGHTED-SMALL-ST-BARRIER-v1"
---

# 1. 读取范围、版本身份和续审定位

本批完整读取 `clean show` 的两个 canonical 正文、冻结/增量元数据、相关审查、构造与独立审计程序以及正文所引用的 evidence。当前 inventory 指纹为：`ccda5c07c46ee14b1bcb` 对应 `tiny_work_stability_joint_rounding_and_selection_barrier.md`，SHA-256 `6f6d28e2c20290873ea77b6771f213534c92f4f3fec0fbce9f70192261384d83`、12284 bytes；`acb99150324dcb0d1a48` 对应 `weighted_small_st_barrier.md`，SHA-256 `c7feceaf4dfb792d7e7ecbb34d073176da2af8ab4cba734caa31947abef03bf0`、3593 bytes。两源均来自冻结提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`，并另有 legacy-cleanup 绑定。

第一源延续已有《小任务稳定联合舍入与选择障碍三源审查》，本页补做当前 source ID 的逐源登记，复述其数学合同并把选择障碍、三值峰值和有限 evidence 的层级保留。第二源是对《多小端密度流障碍与单位读出校准槽双源审查》中等值 `{1,1/k}` 密度障碍的多尺度推广；它与第一源共享 ST 槽舍入思想，却不共享 selector/root/leaf 的复杂度归约。两源均保持 `unrelated-machines` 存档身份，不能转写成六人共同目录 SPE 结论。

# 2. 小任务工作量的联合槽舍入

## 2.1 合同和一般性结论

采用 `UM-MODEL-v1`：输入是合法非负有理/∞ 处理时间矩阵、目标 `T` 和显式有理 `CONFIG(T)` 点 `y`；每台机器配置行和为 1，每项任务列覆盖为 1。先把含零边任务分配到零边并从源配置删除，之后考虑正边。固定 `delta in [0,1]` 与整数 `K>=1`，机器 `i` 上 `p_ij <= delta T` 的边称 tiny，其余称 big；每个正权配置至多 `K` 个 big 任务，tiny 数量不设上限。

记
\[
\tau_i(C)=\sum_{j\in C,\ tiny}p_{ij},\quad
r_i=\min_{y_{iC}>0}\tau_i(C),\quad
s_i=\sum_Cy_{iC}\tau_i(C),\quad
b_i=\max_{tiny,x_{ij}>0}p_{ij}.
\]
令 `alpha_1=1`、`alpha_2=3/2`、`alpha_3=11/6`，`K>=4` 时 `alpha_K=2-K^{-(K-1)}`。给定显式证书可在其二进制编码长度的确定性多项式时间内构造完整调度，使所有机器同时满足
\[
L_i\le\alpha_K(T-r_i)+s_i+b_i.\tag{1}
\]
若 `s_i-r_i <= omega T`，则
\[
L_i\le(\alpha_K+\omega+\delta)T.\tag{2}
\]
这是“证书已给出”的条件桥，未声称能够多项式时间寻找一般 `CONFIG` 点或稳定证书。

## 2.2 全机一致匹配的证明机制

在每台机器上把 big 和 tiny 的边际按处理时间非增排序，切成单位槽；只有严格正的区间交才连槽边。所有槽一次性放入同一任务—槽二分图，每个原任务只有一个左顶点。源 `x` 证书的任务列和 1、槽容量不超过 1，给出该图的分数匹配，Hall 定理给出覆盖全部任务的整数匹配。这个“单次全局匹配”是关键：同一任务在不同机器上 tiny/big 角色不被分别舍入。

从每个正权配置删除 tiny 后，big 数至多 `K`，big 工作至多 `T-r_i`。逐行引用 bounded-configuration cardinality slot 引理，big 槽包络至多 `alpha_K(T-r_i)`；不需要删 tiny 后的 big 列单独覆盖 1。tiny 槽使用 ST 前一满槽收费，负载至多 `s_i+b_i`。同一整数匹配的两部分相加得到 (1)。`T-r_i=0` 时 big 边际全为零。槽数至多原正边数加 `2m`，端点是输入有理数与配置权的有理组合，因此不按处理时间数值大小循环。

参数相容性要保留：只由 `delta` 自动计数会给 `K` 约 `1/delta`，不能把 `K` 固定又让 `delta` 任意小。`K=1,delta=1/2` 给 `(3/2+omega)T`；`K=2` 在 `delta>1/3` 且 `omega<1/2-delta` 时给严格次二。零目标、空任务、单可用机器和 `T-r_i=0` 分支需要预处理，不能把空行或零边混入正任务证明。

## 2.3 稳定证书选择的精确障碍

第一源的第二个身份为 `UM-TINY-WORK-STABILITY-SELECTION-NP-v1`。对固定 `ell>=2`、固定有理 `0<=omega<1/2`，在 selector/root/leaf 实际矩阵族上，判定是否存在 `CONFIG(1)` 点使每行 `s_i-r_i<=omega` 是 NP 完全。矩阵只使用 `{1/ell,1}`，每个配置至多一个 big。该断言依赖完整 perfect3DM 归约及其复杂度事实；不是两三个有限枚举的结论。

选择障碍的核心是 root 的 selector 边际 `z_a`。selector 覆盖给 `sum_{a contains x} z_a=1`，总和为 `q`；root 负载上、下界同时紧，迫使每个正权 root 配置只可能是 selector singleton 或全部 `ell` 个 leaf，因而每个 leaf 在 root 的边际为 `1-z_a`。稳定性 `omega<1/2` 迫每个正的 `z_a` 大于 `1/2`，每个 `x` 只能选一个且等于 1；B/C/D 资源容量再给出 perfect3DM。反向从 perfect3DM 构造 0/1 配置点，振幅为零。该双向投影说明“先找到稳定证书”本身不能被当作免费预处理。

有限 `ell=2,3` parity 案例仅作为精确 Fraction 证据：它们有 `omega=1/2` 证书、拒绝 `omega=1/3`，并枚举完整 assignment。证据不能扩大到 `omega>=1/2` 或任意矩阵。正文还给出同一构造族的三值实际峰值：perfect3DM 大小 `nu=q` 时为 1；`nu<q` 但 X 到 Y/Z 的二部投影匹配 `mu=q` 时为 `1+1/ell`；`mu<q` 时为 `1+2/ell`。这是呈现为该模板族的精确恒等式，不能被写成未标记原矩阵的识别算法或一般近二结论。

# 3. 加权小端 ST 的多尺度障碍

## 3.1 命题和量词

稳定身份为 `UM-WEIGHTED-SMALL-ST-BARRIER-v1`。固定 `0<beta<1`、`0<=gamma<=1`，每个有限端处理时间在 `[0,1]`，令
\[
S_j=\{i:p_{ij}\le\beta\},\quad Q=\{j:S_j=\varnothing\},\quad R=J\setminus Q.
\]
假设 `Q` 的有限边处理时间都是 1，`R` 中每项至少有一个 small 端。定义
\[
s_i=\sum_{j\in R:i\in S_j}p_{ij},\qquad
u_i=\sum_{j\in R:i\in S_j,\ |S_j|\ge2}p_{ij}.
\]
若逐机 `s_i<=1` 且 `u_i>=gamma s_i`，则 `Q` 无容量 1 匹配时 `OPT>=2`；有覆盖 Q 的容量 1 匹配时，确定性位多项式算法输出完整调度，满足
\[
C_{max}\le 2-gamma/2+beta.\tag{3}
\]
当 `Q` 为空，去掉前导 1 得绝对界 `1-gamma/2+beta`，不能自动读作相对 `OPT` 比率。

## 3.2 证明和算法

对 `j in R`、`i in S_j` 设 `x_ij=1/|S_j|`。任务列和 1，机器 i 的分数 small 负载为
\[
w_i=\sum_{j:i\in S_j}p_{ij}/|S_j|.
\]
单端 small (`|S_j|=1`) 的贡献为 `p_ij`，多端 small (`|S_j|>=2`) 的贡献至多 `p_ij/2`，所以
\[
w_i\le(s_i-u_i)+u_i/2=s_i-u_i/2\le1-\gamma/2.\tag{4}
\]
把显式 `x` 送入有序单位槽舍入，正支撑边的最大时间不超过 `beta`，每台机器负载至多 `w_i+beta<=1-gamma/2+beta`。Q 独立做容量 1 二分匹配，每台增加至多一个单位任务，叠加得到 (3)。若 Q 不能容量 1 完整匹配，任何 makespan 小于 2 的调度都只能每台放至多一个 Q，因而反推出容量匹配，故 `OPT>=2`。

这是加权时间的结构性 ST 障碍：不要求所有 small 时间相等，也不要求每个 small 任务恰两台可用机器；只需逐机总 small 工作上界和多端工作占比。其依赖是逐机条件，不能以全局平均密度替代。

## 3.3 与等值密度源的关系和边界

既有多小端密度源把处理时间限制为 `{1,1/k}`，按每机 small incidence 上界 `k` 与柔性计数给出容量流/整数化上界；本源把 `1/k` 替换为任意 `[0,beta]`，并直接用 fractional support `1/|S_j|` 和 ST，所得界是绝对的 `2-gamma/2+beta`。它覆盖等值障碍的机制，却没有继承单位读出双树的深度校准、selector clause 证书或任何固定密度 D 的特化算法。

当 `Q!=empty`，`OPT>=1`，若 `beta<gamma/2`，(3) 是严格次二相对界；更一般的承诺归约若 YES `OPT<=1`、NO 要求超过 `rho<2` 且 `2-gamma/2+beta<rho`，匹配成功时直接输出低于 `rho` 的调度，匹配失败时判 NO。因而接近 2 的硬度编译必须令 `gamma` 趋零、允许较大 small 端或把一致性放入非局部 unit/medium 结构。这个必要形状不是一般不可近似性定理。

# 4. 双源比较、证据层级和接续

第一源的独有对象是“给定 CONFIG 的 tiny/big 共同槽舍入”以及稳定证书选择的 perfect3DM 障碍；第二源的独有对象是任意多尺度 small 时间的逐机密度 ST 界和 Q 的容量匹配分支。二者的共同点是：一份局部/显式分数证书在同一个任务—槽匹配中可被一致读出，但证书的寻找、逐机条件或多端密度假设不能默认为成立。

第一源中的 `alpha_K` 包络、`s_i-r_i` 稳定余量和 selector/root/leaf 选择复杂度，不会由第二源的 `gamma,beta` 公式自动提供；第二源的 `u_i>=gamma s_i` 也不等同于第一源的逐配置 tiny 工作量余量。二者只能在关系图中以“给定证书的 ST 读出”或“多端 small 密度触发次二”建立条件边，不能合并成一般 UM 近二算法。

有限审计与独立程序只核对 Fraction 算术、输入拒绝/接受、有限 assignment 和小规模模板；一般公式与 NP 量词由正文证明或引用的 perfect3DM 复杂度事实承担。未闭义务包括：一般 CONFIG/稳定证书生成器、`omega>=1/2` 的选择端点、无逐机密度时的加权算法、`Q=empty` 的相对比率、通用矩阵的近二硬度和 `UM-TARGET-v1`。

逐源处置：

- `ccda5c07c46ee14b1bcb`：`integrated`。其联合槽公式、单次全局匹配、稳定证书 NP 选择障碍、三值峰值条件和“给定证书而非搜索器”的边界写入第 2 节；有限 evidence 与既有三源审查作相关材料。
- `acb99150324dcb0d1a48`：`integrated`。其加权 small 定义、逐机密度假设、`2-gamma/2+beta` 证明、Q 匹配分支和接近二必要形状写入第 3 节；与等值多小端源的差异和不适用范围写入第 3.3、4 节。

两源均为全文件实读、相关正文/程序/证据已核对，独有内容去向和保留缺口已记录。
