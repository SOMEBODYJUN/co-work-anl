---
id: customer-attraction/r373-fixed-menu-residual-probe-review
kind: review
type_tag: 审查
title: R-373 固定两人菜单残差探针审查
status: source-read-replayed-and-fraction-exact-rechecked
truth_status: finite-fixed-menu-diagnostic; no-universal-bridge-or-half-result
review_level: full-1486-byte-read; SciPy-LP-rerun; 30-row-Fraction-recheck
summary: 源程序在五个主题的固定两人菜单上解一个福利归一化的线性探针。浮点最优值为零；返回的四个半权重点经有理数重建后逐行满足全部30条偏离不等式，且 C=R=1。它给出一个有限固定菜单的等式点，既不是负残差反例，也没有证明一般桥或六人半覆盖。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/global/residual_probe.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/global/residual_probe.py
  - clean:2f88215182d878146027:research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/global/residual_probe.py
  - clean:203e8d0e345e9da732d9:research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/credible/fixed_bridge_attack.py
  - clean:4281379d12a85ee0d8bc:research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/global/residual_counterexample_audit.json
evidence_paths:
  - cleanup/workspaces/Boss7/current-batch/2f88215182d878146027/source.py
  - cleanup/workspaces/Boss7/current-batch/2f88215182d878146027/run.json
  - cleanup/workspaces/Boss7/current-batch/2f88215182d878146027/audit_exact.py
  - cleanup/workspaces/Boss7/current-batch/2f88215182d878146027/audit_exact.json
  - cleanup/workspaces/Boss7/current-batch/2f88215182d878146027/derived_instance_check.py
  - cleanup/workspaces/Boss7/current-batch/2f88215182d878146027/derived_instance_check.json
related_objects:
  - archives/customer-attraction/state/审查/固定价格取消与入流付款的内部核读--审查.md
  - archives/customer-attraction/state/审查/静态最优指派桥盲审的双求值与量词核对--审查.md
  - archives/customer-attraction/state/审查/R18缺口锥LP与静态机制--审查.md
---

# 来源身份和实际重放

本批冻结源是 `2f88215182d878146027`，路径为 `research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/global/residual_probe.py`，1486 字节，SHA-256 为 `0f70a0715ecd6a0985067ea73df08af41735ac084efb96d91e0dbcc159aa5e06`。两个冻结提交的源字节相同。源头明确写着“Exploratory LP on fixed two-player menu, not a general proof.”

程序在 Python 依赖 `numpy` 和 `scipy.optimize.linprog` 下原样运行，HiGHS 返回 `success=True`、浮点目标最大值 `0.0`。随后用标准库 `Fraction` 独立写出同一 30 条行并重算；没有把浮点字符串本身当作证明。附加的 `derived_instance_check.py` 把半权点整体乘以 2，得到四个单位客户的整数化读法，用来核对有限菜单的直观含义。

# 固定菜单、路径和线性约束

主题编号为 `0,1,2,3,4`，所有非空兴趣类型以位掩码
\(B\in\{1,\ldots,31\}\)表示。第二位的固定回复为
\[
\rho=(1,2,1,2,0),
\]
所以根路径取 `actual=(4,0)`；比较路径仅作目标行，取 `comparison=(1,3)`。对一条两步路径 `path=(a_0,a_1)` 和提供者位置 `i`，源函数为
\[
u(path,i,B)=
\begin{cases}
1/\sum_{j=0}^{1}{\bf1}_{B}(a_j),&a_i\in B,\\
0,&a_i\notin B.
\end{cases}
\]
重复主题在分母中按有序位置计数，不能被集合化。

对每个根首步 `a` 与第二位动作 `b`，源加入第二位的行
\[
u((a,\rho(a)),1,B)-u((a,b),1,B),
\]
共 \(5\times5=25\) 行；再对每个根偏离首步 `b` 加入第一位行
\[
u((4,0),0,B)-u((b,\rho(b)),0,B),
\]
共5行。变量是每个兴趣类型的非负权 \(w_B\)。令
\[
 C_B={\bf1}[B\cap\{4,0\}\ne\varnothing],\qquad
 R_B={\bf1}[B\cap\{1,3\}\ne\varnothing]\,{\mathbf{1}}[B\cap\{4,0\}=\varnothing].
\]
LP 归一化为 \(\sum_B C_Bw_B=1\)，并最大化
\[
 \sum_B(C_B-R_B)w_B
\]
，所有30条行均要求左侧不小于0。这个 `C-R` 是源脚本的固定菜单探针量，不是已证明等于 `OPT-W`、静态 CCE 价值或完整六人目标。

# 返回点和有理精确核对

源返回四个非零位掩码，每个权重为 \(1/2\)：

| 掩码 | 兴趣类型 | \(C_B\) | \(R_B\) |
|---:|---|---:|---:|
| 2 | \(\{1\}\) | 0 | 1 |
| 5 | \(\{0,2\}\) | 1 | 0 |
| 8 | \(\{3\}\) | 0 | 1 |
| 16 | \(\{4\}\) | 1 | 0 |

因此精确得到
\[
W_C=\sum C_Bw_B=1,\qquad R=\sum R_Bw_B=1,\qquad W_C-R=0.
\]
独立核对的全部30条 SPE 行均非负；最小松弛为0。7条非零行的松弛恰为 \(1/4\)，其余23条为0（其中包括规定动作自身行和若干真实平局）。因此这是一个允许平局的固定两阶段菜单可行点，而不是严格不等式的唯一均衡。

将权重整体乘2可读为四个单位客户：兴趣集合分别为 \(\{1\},\{0,2\},\{3\},\{4\}\)。在同一回复表下实际路径 `(4,0)` 的两个提供者收益均为1，覆盖福利为 \(W=2\)；逐根枚举五个主题的有序二元选择，静态最大覆盖也是 \(OPT=2\)。这只是该返回点的整数化核对，不能把 LP 的归一化对象改称一般客户实例定理。

# 与相邻来源的差异和边界

`fixed_bridge_attack.py`（ID `203e8d0e345e9da732d9`）使用六主题、三位提供者和完整策略证书，报告的是另一份有限实例的 `W=13, OPT=14` 及最优比较并集缺一；本源没有该实例的客户表、完整三位策略或 `OPT` 行，不能合并为同一个反例。`residual_counterexample_audit.json`（ID `4281379d12a85ee0d8bc`）也是27客户、六主题的独立审计，且明示“不构成 Q-CAG-HALF 或 B4 失败”；本源仅提供五主题两位菜单的归一化 LP 点。

本源的 `linprog` 目标为零，故没有负的 `C-R` 反例。浮点优化器成功只说明该有限 LP 的数值求解状态；有理重算只证明返回点满足这30条行和归一化，未给出独立的原/对偶有理证书，也没有遍历其它策略、支持大小、回复表或客户权锥。即使把本点整数化，得到的只是一个有限四客户等式例，实际 `W=OPT=2`，不触及半覆盖下界。

# 处置和如何接续

本源独有内容是：固定回复表 \(\rho\)、实际路径/比较路径的精确行定义、零残差的四个半权支持，以及其有理可行性和整数化核对。它应整合到固定菜单残差探针审查对象，并保留源脚本、运行输出、Fraction 核验和与相邻六主题/三人来源的边界说明。若要继续研究，应把全部30行写成有理矩阵并提供 LP 原/对偶证书，明确探针量与目标福利不等式的关系，再扩大到完整策略和所有支持；在此之前不能把本源升级为一般桥、半覆盖反例或定理。
