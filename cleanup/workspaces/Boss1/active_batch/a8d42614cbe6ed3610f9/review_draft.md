# `a8d42614cbe6ed3610f9` 独立审查草稿

## 读取范围

已完整读取冻结来源及关联材料：

| ID | 文件 | SHA-256 | 审查用途 |
| --- | --- | --- | --- |
| `a8d42614cbe6ed3610f9` | `two_player_collision_free_bound.json` | `b3d276debe470caa39b299fe7dafcdefe3924b832f1cc20721528bbaaa3efbdb` | 目标对偶证书：ratio `5/4`、6 个非零乘子、48 mask 余项、4 个 primal 支撑 |
| `23c59afb9f2a6498f7c7` | `two_player_collision_free_bound.py` | `867f6f89eb97ab84a4098ed3fb5bd8113e3b3710a2dda2fabf7f037799e79ad3` | LP 发现后 `Fraction` 精确核验；实际代码只处理零背景、`C∩D=∅` |
| `d9e2deb241f3440413f7` | `two_player_collision_free_best.json` | `8470454396d1ae7e138a08c7b01451c648bcc58c7ea7230693f9af91d329958e` | 五客户 `5/4` 端点候选 |
| `8790d2f2ec1c1e3501f0` | `audit_two_player_overlap.json` | `1987f247cd03167e3a8d1597a5b07f2cdc05ae5c76c862349c85d7d31285f9d5` | 64 个二元会员型、两个端点和笛卡尔积摘要 |
| `514a5475422ce77ab849` | `audit_two_player_overlap.py` | `30083784944d6a9b5213936af5df38e31ad43bfecbdb61af1e839c2ce7c8f2e6` | 无 LP 的逐客户恒等式和完整端点核验 |
| `a688a554b33bce8def2f` | `audit_background_two_player.json` | `a8351d053b18f99ef3f02a4c7c0cc742db4cd7e846d22a74a28bc7ff03b111e3` | 576 个背景/会员型检查摘要 |
| `33a7ad7c1c761c51c319` | `audit_background_two_player.py` | `0676cf5b63dbcb4937cb1a63b889f8a84a4c0b36f4eea07a30c6b8c7b6a6b876` | 背景恒等式有限检查；代码自称一般背景靠符号证明 |
| `410387249f58e966c0db` | `background_two_player_refinement.md` | `5dbd316deac78f041204965d5a6b9ced25a5564a95a616b2ec7d22caad8ce86f` | 任意整数背景扩展候选和精确量词边界 |
| `4157a234ca8cf21dc537` | `two_player_overlap_refinement.md` | `1646a1fff26071882c8578f96cf2dc3dcff56ffb86bd4c284bd7db8e0a1205a9` | 零背景任意实际重叠版本、端点和笛卡尔积 |

同时对照既有正文：`state/定理/末两人新生重叠的顺序利润税界--定理.md`、`state/反例/五客户无拥挤SPE负载桥障碍--反例.md`、`state/资源/无拥挤完整均衡族原稿与有限探索的准确范围--资源.md`，以及 `R-2fc` 的两份独立审查/清洗对象。没有修改上述正式档案。

## 复现记录

在干净临时目录复制三份脚本后顺序执行：

```sh
python3 two_player_collision_free_bound.py
python3 audit_two_player_overlap.py
python3 audit_background_two_player.py
```

三次 stderr 均为 0 字节、退出码均为 0。bound 重新生成的 JSON SHA-256 与冻结目标同为 `b3d276de...aa3efbdb`；overlap 输出同为 `1987f247...31285f9d5`；background 输出同为 `a8351d05...b111e3`。结果摘要：

* bound：ratio `5/4`、minimum residual `0`；LP 支撑为 mask `6,26,36,57`，权重 `1/4,1/4,1/4,1/2`。
* overlap：64 个二元会员型，minimum residual `0`；五客户端点 `(W,I,OPT)=(4,0,5)`，全重叠端点 `(2,2,3)`，笛卡尔积端点 `(6,2,8)`。
* background：9 个整数背景值 × 64 个二元会员型 = 576 checks，minimum `psi=0`；脚本输出明确保留“一般背景定理使用符号证明”的限定。

复现副本及 stdout/stderr 保存在本目录 `replay/`，不替代冻结源。

## 证明级别判定

1. **目标 bound JSON：证明级（条件化的精确线性证书）。** `linprog` 只找乘子；`Fraction` 对所有 48 个允许 mask 逐格验证残差非负。因任意客户都落入一个 mask，逐客户求和得到普遍两人零背景、实际无碰撞界。证书未包含代码本身没有写出的背景或任意人数约束。
2. **五客户 endpoint：完整有限 SPE 见证。** 结合 `audit_two_player_overlap.py` 的 20 个有序历史比较，给出 `5/4` 达到；不是“LP primal 支撑自动构成 SPE”。
3. **background refinement：解析候选/正文级边界。** 逐客户 `psi` 表给出任意非负整数背景的符号论证；576 个样本只作回归检查，不能单独承担任意背景量词。其 `R_b` 是剩余两人利润，不是全局覆盖福利。
4. **3/2 无拥挤族：独立存在族，不是本源的推广。** 已有对象给任意 `k` 的完整 Q/B 归纳和有限端点审计；它只说明人数增长后可趋 `3/2`，不否定两人 `5/4`，也不提供一般上界。

## 量词和风险清单

* `C,D` 必须是同一完整纯 SPE 的实际根/末位动作，`Rj` 必须是同一策略在根偏离 `Tj` 后的真实回复；不能为每个 slack 另选一个有利续局。
* 无碰撞条件只在实际 `C∩D=∅`；离轨 `Tj∩Rj` 可碰撞。把“实际无拥挤”改成“所有离轨节点无拥挤”会改变问题。
* 结论对两人末端和零背景；不能沿不同固定前缀累加，也不能替代六人 Q-CAG-HALF 的全局义务。
* 客户是单位权；不能迁移到带权客户、混合策略或不共同的目录。
* LP primal 的四个 mask 权重是松弛紧性记录，不是独立的 SPE 存在证明；真实紧性由五客户端点和独立逐历史审计承担。
* 有限脚本检查不能证明源码之外的 `m`、背景或模型变体；不要把 9 个背景值、64 个会员型或 3 个 `k` 端点写成穷尽所有游戏。

## 建议去向

建议将目标源登记为现有定理“末两人新生重叠的顺序利润税界”的证据补强：绑定 source IDs `a8d42614cbe6ed3610f9`、`23c59afb9f2a6498f7c7`、`d9e2deb241f3440413f7`，并在定理的证据/审查元数据中注明本次源码全文读取和三脚本逐字复现。独立正文草稿见同目录 `proof_draft.md`；本稿适合作为审查附页。五客户负载桥障碍、无拥挤 `3/2` 族和一般 half 的 OPEN 状态保持各自对象与身份，不应合并。
