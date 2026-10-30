---
id: "unrelated-machines/raw-sh3-inclusion-entry-cut-binomial-audit"
kind: "review"
type_tag: "审查"
title: "SH3 包含切口二项式有限审计"
status: "retained-finite-audit"
truth_status: "exact-finite-computation-with-explicit-non-general-boundary"
review_level: "source-and-replay-scope-read"
summary: "120 个有限二项式案例中记录了精确有理切口量、四个边界不等式和 strict_reverse_cut 标志；85 例该标志为真。另有一个 q=2,m=6 的完整小矩阵路径审计，峰值 11/6。结果不构成一般 q、m 的切口定理、SDP 证书或硬度结论。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/raw_sh3_inclusion_entry_cut_binomial_audit.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/raw_sh3_inclusion_entry_cut_binomial_audit.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:evidence/runs/unrelated_machines/raw_sh3_inclusion_entry_cut_root_replay_scope.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/raw_sh3_inclusion_entry_cut_root_replay_scope.json"
---

# SH3 包含切口二项式有限审计

## 对象、输入和证据等级

本对象整理两个同路径冻结版本中的一份主 JSON 和一份 replay-scope JSON。它们属于 `unrelated-machines` 的机器—作业—配置证据，不属于有限客户/六提供者完整历史 SPE。主记录自称“exact finite binomial formulas plus separate small complete original matrix”；它给出 120 个二项式参数案例、85 个 `strict_reverse_cut` 案例，以及一个独立的小矩阵/完整路径审计。每个案例保留 `q,m,scale_exponents,delta,d1,d2,H,M`、精确切口余量 `exact_cut_margin_over_C`、`H_over_C`、`M_over_K` 和 `all_four_binomial_bounds_verified` 字段。

记录中的参数集合为

\[
q\in\{4,8,16,32,64\},\qquad
m\in\{400,416,800,832,1600,1664,3200,3328,6400,6656\},
\]

且 `delta` 取 (1,1/2,1/4,1/8)，还附带四种 `scale_exponents`。120 个案例的四个二项式边界字段均为真；`strict_reverse_cut` 为真者共 85 个。各行同时记录非常大的原始 machine/job/finite-entry 计数，说明这些是参数公式的精确整数检查，而不是把完整矩阵全部物化后的统一调度运行。

replay-scope 逐行读取了原始 158 行脚本和仓库规范 164 行脚本。规范版本只改变 argparse 的 `--output` 要求、拒绝覆盖已有输出以及可移植默认输出路径；`binomial_case`、`small_complete_original_matrix` 和 `main` 中的数学内容按记录逐字节保留。源脚本的输出由原始入口和规范 CLI 两次生成，三份输出 SHA 一致；这证明的是程序重放和输出身份，不是独立数学证明。

## 有限二项式结果

在主 JSON 的 120 个具体案例上，可以安全保留以下结论：

* 对每一行实际存储的整数/有理数，四个二项式边界检查均通过；
* `strict_reverse_cut` 的布尔判定在 85 行为真、35 行为假；
* replay 摘要的 `q64_all_tested_fail` 字段为真。这里保留字段的原语义，表示该审计所定义的 q=64 测试条件在测试集上均未通过；它不是“所有 q=64 实例都失败”的全称命题；
* `exact_cut_margin_over_C` 可以为正或负，不能仅凭 `H_over_C` 或某个比例把所有行归入同一真值类别。

审计未提供可泛化的二项式公式证明文本、一般 q/m 的矩阵生成器、M3 或 localizer SDP 求解器、所有完整调度枚举或未知源解码器。因而其正式状态是**有限精确计算**，并保留切口判定在不同参数行之间变化的边界；不能把 85 行升级成任意规模的 strict reverse-cut 定理，也不能从 q=64 的布尔标志推出一般近似障碍或 hardness。

## 独立小矩阵对象

主记录另列一个与上面参数族分开的完整小矩阵：

\[
q=2,\quad m=6,\quad 45\text{ 台机器},\quad 106\text{ 个原作业},\quad
750\text{ 个有限端点}.
\]

该例显式 `CONFIG1_support=690`，全部 106 条原覆盖等式、750 个有限端点边际和 106 个完整路径分配作业均满足记录的检查；构造出的实际路径峰值为

\[
C_{\max}=11/6.
\]

这个小例的用途是把“配置支持/完整路径/峰值”三种对象在一个完全物化输入上对齐。它的 scope 明确写成 small matrix/config/path audit，而不是渐近切口实例；它不落在主族的 `q` 为 4 的倍数、`m\ge100q` 参数域内，因此不能作为主族的极限行为或反例。

## 文献读取和范围

replay-scope 记录对 `history/source/literature/unrelated_machines/bamas_2025_lift_project_santa_claus_v2.pdf` 的 SHA，并实际读取了第 560–716、908–990、1815–1868 行区间，覆盖目标定义、图/assignment-LP、SA 条件判据和 connecting-dots。它没有声称完成整篇论文证明审查；本对象沿用这一有限读取范围，不把文献中的条件判据当作本审计的普遍结论。

## 与现有对象及后续工作的关系

本审计应与已有 unrelated-machines 的 CONFIG、C2/PSD、稀释和行度审查分开。它们共享“有限 exact 输出不能替代全局耦合”的证据纪律，但变量、矩阵和目标不同；不能把本对象的 `strict_reverse_cut`、(11/6) 或 q/m 计数直接拼到其他对象的近似比。它也与当前六人 SPE 目标保持独立：本对象没有客户、主题目录、终局均分或完整历史量词。

若后续要推进，应先给出：二项式案例到统一机器/作业实例的生成和解码、严格切口条件的明确全称量词、完整配置/路径耦合证书，以及超出小矩阵的真实可行性或最优性证明。在这些缺口关闭前，继续标记为有限审计和条件边界；不要称为一般反例、一般算法或复杂度定理。
