---
id: customer-attraction/root-menu-cap-floating-discovery
kind: resource
type_tag: 资源
title: 根菜单容量交替LP浮点发现器
status: finite-floating-discovery; no-universal-claim; auxiliary-only
summary: 固定三人六主题、给定完整策略的IC约束下，用交替LP搜索根背景鲁棒查询分布与客户子集，输出 factor*v-W 的有限浮点候选；代码自身明确不作普遍断言。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/root_menu/probe_root_cap.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/root_menu/probe_root_cap.py
  - source:dcaf29192d465aadf5944bc807687e6170d71aae:blob
  - source:fbcfaa77701ea290c43cd30609e489740e9ad940bc39edddfe6bf1501d76feb1:sha256
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/root_menu/root_cap_group_factor2.5.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/root_menu/root_cap_group_factor2.5.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/root_menu/root_cap_group_factor3.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/root_menu/root_cap_group_factor3.json
  - source:25261bdccbe1c27d137b:sha256:fa95ba29e2130fa52f1d9fb138064f5c97f90b0d86427555a5456ee762567968
  - source:3b4b9db523e90c02ffef:sha256:89d34bf1f96e51bd7ee571e831a617b59de7128001c7c8e4c39ea0b840cb8028
---

# 对象与范围

源 ID `69b425c3a07fd27d928d`，冻结路径 `research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/root_menu/probe_root_cap.py`，blob `dcaf29192d465aadf5944bc807687e6170d71aae`，3191 bytes，SHA-256 `fbcfaa77701ea290c43cd30609e489740e9ad940bc39edddfe6bf1501d76feb1`。legacy-cleanup 提交为 `68fad804ec5946cb296f77dc5b336308a66abf12`，main 对应 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`。

程序固定 `n=3,k=6`。历史集合是深度 0、1、2 的全部有序前缀，共 `1+6+36=43` 个节点；`group_policy` 给出一个确定的三人六主题完整策略，`out(h)` 递归生成其终局主题计数。每个非空主题子集（63 个 mask）是一个单位客户类型，`bits` 记录它覆盖的主题。

程序先形成该策略的每节点逐坐标 IC 差值 `gamma`，过滤零行；本次重放得到 215 条非零约束。根背景为六个首步后继 `out((a,))-e_a` 的去重集合。对每个背景、客户 mask 和查询主题构造
`1/(1+背景负载)` 的静态查询收益系数 `coeff`。

# 交替 LP 的实际含义

外层给定查询主题分布 `p`，求一个非负 mask 权重 `w`（总和 1）和标量 `v`，约束全部 215 条 `gamma·w≥0`，并以各根背景下的 `p`-期望查询收益至少为 `v`；目标最大化 `factor*v-c·w`，其中 `c` 只标记原策略根终局覆盖的主题。内层 `cap_lp` 在给定 `w` 时反过来求一个查询分布 `p`，最大化所有六个背景的最小期望查询收益。每个 LP 用 SciPy HiGHS 浮点求解，默认 64 个 Dirichlet 起点和 30 次交替迭代；没有精确有理化、全局最优证明或对所有策略的量词。

因此 `gap=factor*cap-W` 只表示一个固定策略、固定 63 类客户锥和有限起点的数值搜索分数。即便出现正 gap，也不能推出该模型存在完整 SPE 反例；负 gap 也不能证明普遍安全界。代码输出的状态字符串正是 `floating discovery; no universal assertion`。

# 复现与结果核对

按冻结源逐字节导出后，SHA-256 与库存一致。用同一 Python 环境运行 `--starts 2 --factor 3`，43 历史、215 非零 IC 行；输出 23 条 trace，首条及最优条为
`W=0.875, cap=0.3125, gap=0.06250000000000011, p=(1,0,0,0,0,0)`，mask 权重为 `{2:1/8,16:1/8,47:3/8,61:3/8}`（浮点显示）。该重放只确认控制流与数值状态，不把 0.0625 变成精确证书。

对相邻但尚未由本源处置的结果源也做了只读核对：

| 源 | 状态字段 | full histories | nonzero IC rows | trace | best gap |
|---|---|---:|---:|---:|---:|
| `25261bdccbe1c27d137b` `root_cap_group_factor2.5.json` | floating discovery; no universal assertion | 43 | 215 | 278 | `-0.07754629629629628` |
| `3b4b9db523e90c02ffef` `root_cap_group_factor3.json` | floating discovery; no universal assertion | 43 | 215 | 190 | `0.06250000000000011` |

两份冻结 JSON SHA-256 分别为 `fa95ba29e2130fa52f1d9fb138064f5c97f90b0d86427555a5456ee762567968` 和 `89d34bf1f96e51bd7ee571e831a617b59de7128001c7c8e4c39ea0b840cb8028`；它们应由各自源记录另行处置，不因本程序被默认为已完成。

本批已将两份相邻因子输出接入
`archives/customer-attraction/tools/evidence/root-menu-cap-floating-discovery-Boss7/`，并以
`verify_root_caps.py` 做结构与算术核验。`factor=2.5` 的最佳值有理近似为
`W=23/36, cap=97/432, gap=-67/864`；`factor=3` 的最佳值有理近似为
`W=7/8, cap=5/16, gap=1/16`。核验只检查冻结 JSON 的 SHA、字段、归一化、非负性、trace 长度和 gap 恒等式，
不证明 LP 全局最优，也不把正 gap 升级为完整 SPE 反例或一般 factor 界。

# 与现有正文的关系

现有 `archives/customer-attraction/state/资源/根真实菜单与背景化安全探索的版本范围--资源.md` 已把该类 `probe_root_cap.py` 识别为发现器，并明确有限探针没有普遍证书；`archives/customer-attraction/state/资源/任意菜单图入口的有限核验与强遗漏桥版本--资源.md` 也把 R-373d 历史材料与后来的解析对象分开。现有 `archives/customer-attraction/state/资源/根真实菜单与背景化安全探索的版本范围--资源.md` 中的 `root_menu_mixture_family` 解析族是任意 `m≥2` 的完整 SPE 构造；本程序只在 `m=3,k=6` 的一棵策略上做浮点发现，不能替代该解析证明，也不能把候选数值迁移到六人 Q-CAG-HALF。

# 建议处置

建议 `integrated`：将源码、重放 stdout、参数和 SHA 作为 `archives/customer-attraction/tools/evidence/root-menu-cap-floating-discovery-Boss7/` 的程序与有限证据，并在资源对象中保留“发现器而非证明”的边界。正式正文只记录上述有限计算和可复现方法，不写成反例、SPE 结论或普遍 `factor` 界。两份 JSON 虽来自同一发现器，因 factor、trace 和冻结字节不同，分别保留其独有的有限输出记录。
