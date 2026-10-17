# 私有注入树：共同分数证书下的实际五三存在性（仅陈述）

读取目的：新 exact-only 候选，供 root/独立研究者先不看证明重构。此稿先只主张实际完整调度的存在性，不自动主张一般参数下的确定性位多项式算法。

Candidate identity：`UM-Q-PRIVATE-INJECTIVE-TREE-FRACTIONAL-FLOOR-v1`。未登记 canonical Claim，未认证新颖性。

## Objects / Domain / Quantifiers

任意整数 d,h≥1，非空有限 root 集 U。每 root u 有非空有限状态菜单 S_u。每 (u,s) 是完全私有的满 d 叉高度 h 树；深0,…,h−1为内部机器，深h为 leaf-port jobs，全部内部机器在不同状态间也互异。所有树共享有限外机集合 Z。

完整普通 P：每 root 一枚 unit selector，仅可在其各状态树根做；每内部 edge job 父端1/d、子端1；每 leaf job 父端1/d、唯一外机端时间1，外机由显式 f_us:[d]^h→Z 给出。没有其他有限端、任务或预载。与 Latin 编译无关，可以是任意 f_us。

关键附加假设：

1. 每个单独 f_us 都是**单射**；即同一完整状态树的所有 d^h 原 leaves 外机不同。
2. 给共同非负有理 λ_us，Σ_{s∈S_u}λ_us=1 对每 u；对每外机 z，Σ_{u,s} λ_us · |f_us^{-1}(z)|≤1。不能为不同外机另选一份 λ。

## Exact Conclusion

对任意整数 r∈[1,d]，若

`(d−r+1)^h ≥ 2 r^h−1`，

则存在对**每个 root**选一个真实状态和一个满 r 叉高度 h 子树，使全部选中叶的真实外机全局不同。故完整 P 存在合法实际 σ，

`Cmax(σ)≤2−r/d`。

特别取 r=⌊(d+2)/3⌋，对所有 d,h 均满足该数值条件，所以总有完整实际调度

`Cmax≤5/3`。

所有未选状态/分枝的原 jobs 也必须计入 σ；此结论不是仅分配叶资源。因而任何满足这两项假设的 Latin-register 编译实例，无论 E 是否保色、是否随机、L或源labels如何，都不能有实际 OPT>(5/3)，只要其自然共同 λ 被核实满足假设。

## Dependencies / Evidence / Scope / Status

- 本候选只给精确存在性，算法复杂度尚未放进 conclusion；不把指数列举全部 r-子树称为总位多项式。
- 当前模型是私有树、unit selectors和unit唯一外机端。共享内部机器、非均匀时间、原单状态非注入叶映射不在范围。
- typed balanced Latin 的另一个待审共同 λ 证书若成立，满足此页假设；该应用不能先于两页证明核查升级。
- 不改变 UM-TARGET-v1；不是一般不相关机五三算法。Proof另冻待独立重构；尚无有限代码审计。
