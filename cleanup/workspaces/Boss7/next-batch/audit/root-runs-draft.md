---
id: "customer-attraction/r373d-root-menu-capacity-two-float-runs"
kind: "computational-evidence"
type_tag: "计算"
title: "R-373d 根菜单容量交替 LP 的两份浮点运行记录"
status: "finite-float-replay-validated"
summary: "固定三人六主题、43 个有序历史节点和 215 条非零 IC 行的同一发现器，在 factor=2.5 与 factor=3 两份冻结 JSON 输出；factor=3 出现 gap≈0.0625 的浮点候选，但两份都明确没有普遍断言。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/root_menu/root_cap_group_factor2.5.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/root_menu/root_cap_group_factor2.5.json"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/root_menu/root_cap_group_factor3.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/root_menu/root_cap_group_factor3.json"
---

# R-373d 根菜单容量交替 LP 的两份浮点运行记录

## 固定对象与输入

两份 JSON 都声明 `floating discovery; no universal assertion`，固定 `full_histories=43`、`true_rows=215`、同一 `seed=3738` 与两个 `root_backgrounds`。这对应一个三人六主题确定策略的全部深度 0、1、2 有序历史 (1+6+36=43)；`true_rows` 是从该策略逐坐标 IC 生成并保留的非零行数。客户类型是 63 个非空主题掩码的浮点权重，根背景是首步后继的静态负载集合。

同一工作区的已有资源对象《R-373d 根菜单容量交替LP浮点发现器--资源》已说明发现器的数学语义：外层在给定查询分布 (p) 时求非负客户掩码权重 (w) 与最小背景收益 (v)，内层对固定 (w) 反求最大化六个根背景最小期望收益的 (p)，目标为 `factor*v-W`。每次 SciPy/HiGHS 运行、Dirichlet 起点和交替迭代都是浮点有限搜索；没有精确有理化、全局最优证书或对所有策略/所有完整 SPE 的量词。

## 两份冻结输出

|源|factor|trace 条数|最佳迭代 (W)|最佳 (cap)|最佳 `gap`|浮点候选 (p)|
|---|---:|---:|---:|---:|---:|---|
|`25261bdccbe1c27d137b`|2.5|278|0.6388888888888888|0.224537037037037|−0.07754629629629628|约 ((0,0,2/3,0,0,1/3))|
|`3b4b9db523e90c02ffef`|3|190|0.8749999999999999|0.3125|0.06250000000000011| ((1,0,0,0,0,0))|

报告内部的简单恒等式 `factor*cap-W=gap`、(p) 和为 1、非负权重、43 历史、215 IC 行和 trace 长度均已独立脚本核验。因浮点舍入，0.8749999999999999 与 0.06250000000000011 不是有理证书字段。

此外，逐字节导出的已有 `probe_root_cap.py`（source ID `69b425c3a07fd27d928d`，SHA-256 `fbcfaa77701ea290c43cd30609e489740e9ad940bc39edddfe6bf1501d76feb1`）以 `--starts 2 --factor 3` 重放，首条最佳记录与 factor=3 JSON 的 (W,cap,gap,p,w) 完全一致。这只确认控制流/数值状态，不能把同一浮点候选升级成精确反例。

## 处置与接续边界

两份源都保留为**有限计算证据**，不进入定理或反例。factor=3 的正浮点 gap 只表明某一固定策略、固定 63 类客户锥和有限起点中出现候选；它没有证明存在完整纯 SPE、没有覆盖离轨后继、没有证明因子 3 的普遍预算失败，也不触及六人 Q-CAG-HALF-6 主命题。factor=2.5 的负 gap 同样不证明安全界。

原始 JSON、导出的同源探针、验证脚本与 stdout 应作为 evidence manifest 保存；数学内容与既有 `R-373d 根菜单容量交替LP浮点发现器--资源` 合并引用，不能重复创建“反例”对象。`workspace.json` 只作工作区 provenance，不承担这些数值结论。
