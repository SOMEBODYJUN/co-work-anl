---
id: "customer-attraction/six-player-all-big-topic-nonviolating-witness"
kind: "computation"
type_tag: "计算"
title: "六人全大主题纯SPE下界见证"
status: "exact-full-history-pure-spe-witness"
truth_status: "nonviolating-lower-bound-family"
review_level: "full-source-read-and-exact-fraction-checker"
summary: "六名提供者、一个六客户大主题 B 与五个 singleton 主题的完整策略证书：全历史恒选 B，W=6、OPT_6=11、OPT/W=11/6、2W-OPT=1。脚本用 Fraction 检查全部 55,986 个有序历史/动作偏离；这是 2−1/6 下界见证且满足目标，不是 Q-CAG-HALF-6 反例。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-4ba33d9e7be24b0bb0303308d2bcb2ec/README.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-4ba33d9e7be24b0bb0303308d2bcb2ec/all_b_m6/README.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-4ba33d9e7be24b0bb0303308d2bcb2ec/all_b_m6/verify_all_b.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-4ba33d9e7be24b0bb0303308d2bcb2ec/workspace.json"
---

# 六人全大主题纯SPE下界见证

## 实例和策略

有六名单位提供者和六个共同主题：一个大主题

\[
B=\{q_1,\ldots,q_6\},
\]

以及五个 singleton 主题 `\{q_7\},…,\{q_{11}\}`。策略在**每个有序历史**都选择 `B`，包括所有离轨历史。客户在最终覆盖者之间均分。

若当前节点已有 `k` 次 `B`，剩余提供者数（含当前）为 `r`，当前选择 `B` 时其六名客户各自得到 `1/(k+r)`，总收益

\[
\frac{6}{k+r}\ge1,
\]

因为 `k+r≤6`。任一 singleton 偏离只覆盖一个客户，且所有后继仍选择 `B`。若此前已有 `j` 人选择同一个 singleton，其偏离收益为 `1/(j+1)≤1`；根实际路径上 `j=0` 时恰为 `1`。因此当前选择 `B` 弱优于任一 singleton；该论证对所有完整有序历史成立，给出纯 SPE。

## 福利与下界比

根路径全选 `B`，覆盖六名客户，故

\[
W=6.
\]

最优六主题序列选择 `B` 一次并选择五个 singleton 各一次，覆盖全部十一名客户，因此

\[
OPT_6=11,
\qquad 2W-OPT_6=1,
\qquad \frac{OPT_6}{W}=\frac{11}{6}=2-\frac16.
\]

该实例实现已知 `2−1/m` 型下界在 `m=6` 的取值，却严格满足 `2W≥OPT_6`。它不能被误记作六人半覆盖反例；它说明逼近二的下界族与目标命题可以同时存在。

## 精确核验

`verify_all_b.py` 使用 `fractions.Fraction`，定义：

- `payoff(seq,i)`：按最终序列计算提供者 `i` 覆盖客户的均分收益；
- `welfare(seq)`：六名提供者收益总和；
- `strategy(history)=0`：任意历史都选大主题 `B`；
- `verify_spe()`：对深度 `0,…,5` 的所有历史和当前动作，构造当前策略终局与单步偏离终局，逐一比较当前收益与偏离收益；
- `opt_welfare()`：穷举六个位置各从六个主题中选择的所有序列，计算真正的 `OPT_6`。

六个位置、六个主题的所有历史/动作比较总数为 55,986。脚本断言所有收益差非负，并输出最差 SPE margin、根福利、`OPT_6`、`2W-OPT_6` 与比值。它是确定性精确核验，未使用浮点或随机样本。

## 范围和与既有对象的关系

该来源补充[私有席位谱与六极大证据](私有席位谱与六极大证据--计算.md)中 all-big 前缀计数和非违例边界，但它是一个独立的完整六人策略见证：前者含更广的六极大系数域与多个有限审计，本对象保留该具体实例的全历史 IC 和真实福利数字。

它也必须与七极大 singleton 条件半覆盖定理区分：七极大对象研究结构性上界与 `2W≥OPT_6` 的条件行证书；本对象只有一个六人非违例下界族，不提供任何无条件上界。五人半覆盖、六人有限零违例搜索和 `2−1/6` 下界都不能由这个实例互相替代。

复用该证书时必须保留：所有离轨历史仍选择 `B`、singleton 偏离收益至多1（根实际路径前缀为1）、`OPT_6` 由一次大主题加五个 singleton 达到11。任何把“全选大主题”改成只在根路径成立的策略，都会失去完整 SPE 论证。该对象的证据等级是 exact full-history pure-SPE witness；它不宣称外部文献优先权、一般六人定理或 Q-CAG-HALF-6 的闭合。

## 2026-11-02 离轨单例收益表述订正

原页把所有历史的singleton偏离收益写成恰1，遗漏了过去已有同一singleton覆盖者的情形；例如历史已有一位选该题时，当前再选只能得1/2。这里按均分定义改为1/(j+1)≤1，全部历史SPE证明和W6/OPT11结论保持。另一个七标签、含大主题别名的冻结完整策略及其独立有理核验见[三份有限记录](三份全大主题策略的逐人净缺口有限记录--计算.md)；七标签的节点数不转借本六标签证书。
