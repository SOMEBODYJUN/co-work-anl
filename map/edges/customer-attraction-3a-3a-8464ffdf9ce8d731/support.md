# 支撑矩阵与 canonical 去重说明

## 现行承重关系

| 关系 | 现役边 | 本轮处置 |
|---|---|---|
| CAG-MODEL + `M-e960…` + `internal-safe…` ⇒ `M-a90…` 全部 v3 结论 | `ca-six-boss1-pair-and-internal-domains-pay-full-root-requery` | 已有 accepted/unconditional whole 边；当前 pin 与任务一致，复用原字节，不重复发布 |
| CAG-MODEL + `M-e960…` ⇒ `M-a90…` 的旧 C36/C30、ROOT36/30/CAP2 | `ca-six-boss1-real-source3-pair-and-full-history-pay-query-projection` | accepted/unconditional step；只承重 v2 贡献，明确不支付 ROOT270；作为历史分层证据保留 |

两个边的 endpoint/evidence pins 均由现行 registry 指向，原生 `edge-check` 均返回结构有效；本轮没有 `edge-bind --write`，因为没有新边或修改边。

## 证明依赖如何合账

### PAIR30/36

真实末两位钱包的三条 IC 恒等式保留 `g(Y,Y)-g(Y,R_T)`。对 30 个有序异索引，客户重数 `d` 的成本为 `d/(3D)-d(d-1)/(30D(D+1))`；对 36 个有序对为 `d/(3D)-d²/(36D(D+1))`。`Qi=Qj` 仍被允许。因为二者差为 `d(6-d)/(180D(D+1))`，30 对是严格加强但不能替换旧 36 对的全部语义。

### C30/C36

九个真预算在每个 `Qk` 分支中使用该分支自己的真实后继 `(R4k,R5k,R6k)`。对每个旧型和 q 固定后，八态最小与矩区间 `[o/6,o]` 最小给 `m_s(h)`。质量等式自由乘子 `a0(h)` 可为负；只有真实预算、矩界和逐态余项需非负。全部 128 型、2048 状态必须保留，不能把有限 LP 点的客户重数当作普遍菜单假设。

### 根线

ROOT36、ROOT30、ROOT30-CAP2 共享十个真实正预算；每条恒等式均保留独立 `K,O` 参数列和两个质量等式，不把 `K` 或 `O` 预先归一化。ROOT270 只在 ROOT30 的同一根分支增加合法第四源 P25；它不免费添加根 source-1 IC，也不把 P25 族的全部参数域外推成新全称定理。

### ROOT270 严格余项

`ROOT270_STRICT_C_OUTSIDE.json` 在全部 128 根状态上逐列给出 `C\O` 的统一正余项 `η`，并映射到 513 列可见系统。它只加强取等障碍；不证明取等状态能由完整 SPE 实现，也不替代原 270 行必要系统。

## 精确证据读取摘要

| 证据组 | 完整读取与核对内容 | 明确限制 |
|---|---|---|
| `maximal_root_opt_requery/` | 九个正预算、2048 状态、128 包络、质量区间、释放点精确负切面、literal 检查 | 仅固定点不可补全及普遍必要切面；不是 SPE 反例或全局锐界 |
| `main_thirty_index_strengthening/` | 30 对/36 对逐菜单公式、2048 状态、`m30−m36`、ROOT30 131 列身份 | 不求加强根锥新最优；不证明 half |
| `maximal_root_tail_wallet_v2/` | 原 72 行与 129 非负列、固定 K primal/dual、ROOT36 原始线 | 固定必要锥匹配，不是完整 SPE 或全局根 sharpness |
| `main_root30_capacity_feedback/` | `δcap` 最小余项、CAP_B2 与 O 乘子同时增权、131 列重建 | 仅 `O≥K` 时支配 ROOT30 |
| `maximal_root_tail_wallet_v3/` + audits | 270 行、10 正权、两等式、131 列、640/4096/328/896/3584 局部精核 | 只支付指定 270 行必要锥；不称全局最优、SPE、half |
| `main_root270_strict_outside/` | 全 513 列 `C\O` 严格行、所有根状态余项 | 取等必要条件，不是充分条件 |
| `internal-safe…` | 固定半权、最小帽、同菜单条件平均、完整参数域及有限生成器 | 仅其明定预算/锚/参数族；不是任意钱包最优或 SPE 实现 |

## 量词和边界提醒

- 所有真实偏离都沿同一完整策略在新历史继续；冻结原分支、独立抽样四个新会员位或把 `O` 当 action 都是错误迁移。
- 允许空覆盖、重复行动、同覆盖异标签、零客户和弱平局；没有把标签目录强行商成集合目录。
- `O=OPT6` 只在选取最优六标签时成立；对任意查询并的根线不能写成“最优菜单”结论。
- 生产证书中一次发现阶段 optimizer 调用不属于本轮新运行；本轮只读并按精确证书复核数学范围。

## 3B follow-up

任务 definition 的两个 `overlap_comparisons` 均保持 `follow-up`/`3B`。现阶段无需为共同 PAIR 定义或联合内部域另建边；若 3B 要比较“完整参数域”与“C30/ROOT270 合账”是否产生新的严格关系，必须给出新的 endpoint 及真实续局条件，不能只凭共享公式、共同模型或共同证书名称造 hub 边。
