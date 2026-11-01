---
id: customer-attraction/root-menu-cap-floating-discovery
kind: resource
type_tag: 资源
title: 根菜单容量交替LP浮点发现器（相邻因子输出）
status: finite-floating-discovery; no-universal-claim; auxiliary-only
summary: 固定三人六主题与一棵完整策略，交替 LP 在 63 个非空客户掩码和有限根背景上搜索 factor·cap−W；本批补录 factor=2.5 与 factor=3 两份冻结输出及结构核验。所有数值仍是浮点发现，不是 SPE 反例、全局最优或普遍安全界。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/root_menu/probe_root_cap.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/root_menu/probe_root_cap.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/root_menu/root_cap_group_factor2.5.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/root_menu/root_cap_group_factor2.5.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/root_menu/root_cap_group_factor3.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-373daba10913464c93771a808d88fce3/root_menu/root_cap_group_factor3.json
  - source:25261bdccbe1c27d137b:sha256:fa95ba29e2130fa52f1d9fb138064f5c97f90b0d86427555a5456ee762567968
  - source:3b4b9db523e90c02ffef:sha256:89d34bf1f96e51bd7ee571e831a617b59de7128001c7c8e4c39ea0b840cb8028
---

# 对象与固定范围

程序固定三人、六主题和一份确定的完整策略。历史节点为深度 0、1、2 的全部有序前缀，共 (1+6+36=43) 个；非空主题掩码共 63 个。逐历史逐偏离得到 215 条非零 IC 行。根背景取六个首步后继终局计数减去被选主题后的去重集合；本批两个 JSON 均记录两个背景。源自身明确 `floating discovery; no universal assertion`。

外层 LP 在给定查询分布 (p) 下选非负客户掩码权重 (w) 和 (v)，约束 215 条 IC 差值及各根背景下的查询收益至少为 (v)，目标为 `factor*v-W`，其中 (W) 是策略根终局覆盖的客户权重。内层 LP 再对固定 (w) 最大化各根背景的最小期望查询收益。两层均以 SciPy/HiGHS 浮点求解，有限起点和最多 30 次交替；没有保存全局对偶、精确有理化或所有策略量词。

# 两份冻结输出

| 源 | factor | trace | 最优 (W) | 最优 cap | 最优 gap | 实际范围 |
|---|---:|---:|---:|---:|---:|---|
| `25261bdccbe1c27d137b` | 2.5 | 278 | 23/36（浮点显示） | 97/432（浮点显示） | 约 −67/864 | 固定策略、固定客户锥、有限起点；未发现正 gap |
| `3b4b9db523e90c02ffef` | 3 | 190 | 约 7/8 | 5/16 | 约 1/16 | 同上；正数是浮点候选，不是反例 |

独立结构核验确认每条记录的 (p) 和客户权重近似归一、非负，且 `gap=factor*cap-W` 在容差内成立；摘要 trace 长度、43 历史和 215 IC 行与冻结元数据相符。核验不证明 LP 最优性，也不把有限正 gap 升级为完整 SPE 结论。

# 与先有对象的关系与用途

本对象延续 `archives/customer-attraction/state/资源/R-373d根菜单容量交替LP浮点发现器--资源.md` 的程序语义。先有正文已说明 factor=3 的源码、有限模型和发现器边界；本批补入两个相邻结果源的完整指纹、结果表、内部算术核验和可复现副本。factor=2.5 的全负 gap 只能说明该搜索没有找到正值；factor=3 的约 (1/16) 只能说明固定策略/客户锥上的数值候选。两者都不推出六人 Q-CAG-HALF、一般 factor 界、完整 SPE 反例或全局安全定理。

证据与复现依赖位于本批 `evidence/` 目录，包含两个原始 JSON、`verify_root_caps.py` 和 `validation.json`。进入正式仓库时应并入既有 `root-menu-cap-floating-discovery` evidence 目录并更新正文的相邻输出段；不新建重复数学对象。
