# 七极大、六人：route-conditioned 基础行族的精确 Farkas 障碍

日期：2026-10-27。此目录只记录一个**方法边界**，不是 Q-CAG-HALF-6 反例。

## Exact Statement

固定七个 distinct inclusion-maximal coverage `B_0,...,B_6`、六位提供者和一个六步 restricted-growth route `a=(a_0,...,a_5)`。重标号令末位真实极大动作为 `B_0`；每个客户 incidence 为非空 `I⊆{0,...,6}`，真实根路径 membership 为 `J⊆{0,...,5}`，并要求 `J` 的每一位只能属于其 route 主题所含的极大集，且 `5∈J` 当且仅当 `0∈I`（末位最大动作引理）。

目标列系数是

`w(J)-[1_{I∩{0,...,5}≠∅}]/2 = 1_{J≠∅} - 1_{I={6}}/2 - 1_{I={6}?0:1}/2`,

即对六个最大集 `B_0,...,B_5` 的比较并集证明 `W-(U-|X_{\{6\}}|)/2≥0` 的逐客户目标。实现中等价写成 `1_{J≠∅}-1/2+1_{I={6}}/2`，因为七极大任意六集最优并集为 `U-|X_{\{6\}}|`（这里把被省略的标签固定成 6）。

允许行族只有原模型可直接推出的三类合法 SPE 非负松弛：

- `M_t`：七极大 mixed private/shared/core suffix floor（`alpha_t` 用 singleton 原始序列 `A_t` 的后缀最小值，`beta_t` 用 shared 原始序列 `B_t` 的后缀最小值，core 为 `1/6`）；
- `L_j`（`j=0,...,6`）：实际末位对合法最大主题 `B_j` 的最佳回复；
- `T_{jk}`（28 个无序对，含重复）：实际倒二—末位 genuine two-remaining tax。

## Exact Farkas witnesses

`farkas_witnesses.json` 冻结了五个 route 的非负有理 Farkas 见证 `y`。每个见证满足：

1. 每个客户列上 `y` 非负；
2. 对行族中每个 41 行，`Σ_col y_col·row_col≥0`；
3. `Σ_col y_col·target_col<0`。

因此这些 route 上，不存在任何非负乘子把**该行族**逐列支付上述目标。`audit_route_obstruction.py` 用 Python `Fraction` 重建每个完整合法 route 列域并逐项验证，完全不依赖浮点 LP。

```sh
python3 research/workspaces/customer-attraction/R-3a870729e9524f6da600542c63297d4c/route_lp_boundary/audit_route_obstruction.py
```

输出的五个 route 与精确负目标均为：

| route | 倒二标签在前四出现次数 | 列数 | `Σ y·target` |
|---|---:|---:|---:|
| `000000` | 4 | 2111 | `-15899/1672822` |
| `000010` | 0 | 1631 | `-3227857/487086288` |
| `001010` | 1 | 1439 | `-14365/40789656` |
| `010010` | 1 | 1439 | `-388595/452054196` |
| `011101` | 1 | 1439 | `-568595/454620276` |

`discover_farkas.py` 仅用于用 SciPy 找小 support，随后以 Fraction 高斯消元生成 JSON；正式核验只需 `audit_route_obstruction.py` 和冻结 JSON。

## 准确边界与依赖

这只是否定“route-conditioned + `M/L/T` 三类行 + 非负乘子”的证明模板。它没有给出可实现的客户重数、完整 SPE 策略或原模型福利违例；Farkas 列分布是行空间分离见证，不能解释成游戏实例。它也不否定跨早期、倒二、末位真实回复的新共同信用。

倒二重复次数与新条件证书的关系：除 `000000` 外，其余四个障碍 route 的倒二标签只被前四主题包含 0 或 1 次（`000010` 为 0；`001010`、`010010`、`011101` 为 1），正落在“实际倒二主题被前四至少两名包含”条件之外。`000000` 虽有 4 次重复，也只说明 `M/L/T` 粗行族本身不足；可由更强真实 `S/Z/V` 与早期偏离行覆盖，不能据此否定该条件证书。

证据等级：精确有理代数核验（Farkas 分离）；不是目标反例、不是一般证明。未闭合义务仍是四个 `0/1` 次包含 route 的真实跨早期付款，或原模型完整反例。
