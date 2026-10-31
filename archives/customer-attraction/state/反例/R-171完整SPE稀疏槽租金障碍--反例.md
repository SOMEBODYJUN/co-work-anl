---
id: customer-attraction/r171-full-spe-sparse-slot-rent-obstruction
kind: counterexample
type_tag: 反例
title: R-171完整SPE稀疏槽租金障碍
status: 完整历史纯SPE的reset租金桥障碍；非半覆盖反例
summary: 两客户任意历史平局的2q人完整SPE族福利最优，却使稀疏单槽reset租金调和发散；超载离轨遵从收益为1/(2q−a)。
source_refs:
- clean:a736ca58ff82a1a2192b
- clean:c814b3d572d72f7d9eaa
- clean:b3335acda0d4782bca24
---

# R-171 完整 SPE 稀疏槽租金障碍

## 稳定身份与范围

- 来源：`b3335acda0d4782bca24`、`5d94d9ce945202efcf2f`、`9022a7d09f082f7bf7de`、`d7b01fbdd33968bc5544`、`83e372de07df77beb979`，以及可执行审计 `2a3ae62cdcb1da780b81`、`251ddedf0a4a923e6fc4`。冻结原文在 `archives/customer-attraction/tools/evidence/R-171-coupling-20261031/original/`。
- 模型是两个单位客户 `x,y`、共同目录 `{A={x}, B={y}}`、`m=2q` 个提供者。任何非终端历史若 `a>=q` 就选 `B`、若 `b>=q` 就选 `A`，未满时允许任意历史依赖平局；因此根及两计数均未满的历史遵循策略后终局为 `q/q`；若离轨历史已有 `a>=q`，终局为 `(a,2q-a)`，`b>=q` 对称。所有离轨历史均有明确终局。

## 精确结论

选取平局使实际路径为
\[
 A,\;B^q,\;A^{q-1}.
\]
则 `W=2` 且 `OPT=2`。对每个 `j=1,...,q-1` 选择未来槽 `I_j={q+1+j}`，权重 `theta_j=1/j`，每一槽拥塞为 `j theta_j=1`，所以 `Gamma=1`。reset 租金在任意 `rho>0` 下为
\[
 \sum_{j=1}^{q-1}\frac{1}{j(\rho+1)(\rho+2)}
 =\frac{H_{q-1}}{(\rho+1)(\rho+2)},
\]
随 `q` 调和发散。因此不存在只依 `rho` 的常数乘 `Gamma W`，即“任意稀疏未来槽位仍沿用连续窗口同一预算”是错误的。

这不是 Q-CAG-HALF 反例：这里福利与最优均为 2，即 `W=OPT`；原目标 `2W>=OPT` 严格成立；它否定的是一个用于证明目标的稀疏租金桥。

## 为什么确实是完整 SPE

在两计数均小于 `q` 的节点，当前任选一类及后继任意平局均使终局为 `q/q`，当前两个行动收益都为 `1/q`。若离轨节点已有 `a>=q`，遵从选 B 并沿同一规则终结于 `(a,2q-a)`，当前收益为 `1/(2q-a)`；偏离 A 后后继仍全选 B，当前收益为 `1/(a+1)`。由 `0<2q-a<=q<a+1`，遵从严格更好；`b>=q` 对称。`audit_sparse_slot_complete_spe.py` 对 `q=1,...,6` 的全部有序历史、四种历史依赖变体逐一做 Fraction 比较，并对 `q<80` 与多种 `rho` 重核租金恒等式；这支持定义级有限审计，不替代一般证明。

## 可接续边界

该族只说明稀疏槽位的 reset 费用可能无界；它没有证明原模型的效率下界失败，也没有给出一般全树运输反例。后续必须把真实激励不等式产生的费用嵌入共同根路径，或证明带符号松弛能够支付该项。
