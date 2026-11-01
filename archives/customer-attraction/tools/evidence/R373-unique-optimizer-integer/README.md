---
id: customer-attraction/evidence/r373-unique-optimizer-integer
kind: resource
type_tag: 证据
 title: R373整数优化器的原件与精确验证
status: source-copied-and-fraction-verified
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/global/unique_optimizer_integer.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/global/unique_optimizer_integer.py
---

本目录保留 clean show 导出的 1169B 原代码副本、独立分析、Fraction 约束复核与精确原—对偶证书。原代码 SHA-256 为 `f2878977624eb4548594ce70ce3a592768398fbdde8650c522aeb4bce332955d`，两个冻结提交对应同一字节。

`source.py` 用 SciPy/HiGHS 求带整数约束的 63 变量模型；`verify_dual.py` 不依赖 MILP 输出，以 `Fraction` 重建全部 63 行和 63 个非空客户类型列，检查候选整数权重的每条约束，并检查下面列出的非负线性对偶乘子。它得到原—对偶值均为 71、所有对偶列系数不超过1，故对该编码线性规划的最小总权重给出精确下界。`analyze.py` 还复跑连续和整数求解器以记录环境与求解状态；该状态不是精确性唯一依据。

复制文件是供正文和后续复查使用的证据，不改变原来源。运行时应在本目录以新输出路径执行，避免覆盖源或报告。
