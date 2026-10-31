---
id: customer-attraction/r23-promotion-potential-reset-obstruction
kind: obstruction
category: 障碍
title: R-23ab promotion 势能桥与零遗憾重置精确反例
status: integrated-exact-local-obstruction
truth_status: exact-three-player-bridge-failure; no-half-counterexample
source_refs:
  - clean:9508faf54f13653cddcc
  - clean:66516652bd6f20aae6b5
  - clean:7f1277cb0e28054b940f
  - clean:8795fb352c9ee8f01c6d
  - clean:c7b6dcdc0a321b6d77c7
  - clean:69e41051eebfdcdb436d
  - clean:c1a328df0eff8af9c0b4
  - clean:e102907a8220fb5daf74
  - clean:fd30d9d7e25351f6f3fb
---

# 1. 结论先行

R-23ab 的九个冻结源给出一个可复核的**三提供者、三/四主题局部桥障碍**：把实际历史的末位主题提升到根部或新分支后，势能会下降一个严格正的 reset tax，而原实际首位收益损失可以恰为 0。因此，任何试图用“来源遗憾/首位收益”乘一个固定有限常数去支付该 promotion reset 的证明路线都失败。

同一组精确路径的福利为 $W=OPT_3=7$（或按正整数缩放 $7t$），所以它不是 $OPT_3>2W$ 的 half 反例，也不是六人模型反例。`main_half_status` 在独立输出中明确为 `OPEN; this is not a HALF counterexample`。

# 2. 独立完整历史构造

`independent_zero_source.py` 不导入作者策略、检查器、优化器或游戏求解器。它以四个主题上的七个单位客户构造完整有序树：mask 1 一个、mask 4 两个、mask 6 两个、mask 11 两个。对每个历史分别选可行 continuation，枚举得到 85 个树状态、21 个有序决策历史和 84 个 IC 比较。

实际路径与被提升路径分别为

$$z=(0,1,2),\qquad z'=(2,3,2).$$

逐项 Fraction 核验给出：

$$\Phi(z)=9,\quad \Phi(z')=8,\quad \Phi(z)-\Phi(z')=1,$$

实际首位收益差为 0，两个后续 replay 的 IC slack 也都是 0；删去对应分支时的 signed-deletion reset 为 $(1,0)$。实际覆盖 $W=7$，所有三主题最优覆盖 $OPT_3=7$，被提升路径覆盖 6。因此 reset 不是由实际首位遗憾支付的客户福利损失，而是势能定义在新增分支中的独有费用。

源内重放 exit 0，输出保存在 `R23-promotion-reset-20261031/runs/independent_zero_source.*`。

# 3. 零来源遗憾的精确族

`verify_zero_regret_promotion.py` 和 `zero_regret_promotion_exact.json` 把上述障碍写成正整数缩放族。对每个 $t>0$，三名提供者、四个主题、七类客户权重按 $t$ 倍复制；完整树有 21 个有序历史和 84 个含自身的 IC 比较。实际路径为 $(0,1,2)$，promotion 后的真实路径为 $(2,3,2)$。实际支付为 $(2t,2t,3t)$，promotion 后为 $(2t,2t,2t)$，所以来源首位 regret 为 0，而

$$\Phi_{\rm actual}=9t,\quad \Phi_{\rm promoted}=8t,\quad \Delta\Phi=t.$$

实际和最优福利都为 $7t$，promotion 路径为 $6t$。同一运行还检查 replay path $(2,0,1)$ 的中位 IC slack 为 0，并得到删后势能由 $6t$ 增至 $7t$。因此对任意固定有限 $C$，不可能用 $C\times$（来源首位 regret）支付这个 $t$ 的 reset tax。

`verify_promotion_reset.py` 给出另一个三主题强 pair 家族：实际 $(0,1,1)$、promotion $(1,2,1)$，有 $\Phi=21t/2$ 与 $19t/2$，差为 $t$，new-branch exclusive reset tax 也正好为 $t$，而 $W=OPT_3=7t$。它同样只否定 promotion-potential bridge，不否定 half。

# 4. promoted-terminal fork 的实现审计

`promoted_fork/exact.json` 与 `verify.py` 记录了另一个带权费用分解接口。冻结 JSON 报告：

- literal coefficient states 为 24192，检查 horizon $m=3,4,5,6,7,8$；
- $m=3,4,6$ 的 ordered decision histories 分别为 13、40、364；含自身的完整 IC 行分别为 39、120、1092；real fork rows 分别为 9、36、360；
- 两个外部 necessary-system 点只做单行评价，JSON 明确写有 “no SPE claim”；其中一个 slack 为负且 `strictly_separated=true`，另一个没有严格分离。

本批把它作为实现/系数审计接入，未把“arbitrary $k$ follows from proof”当作已读证明，因为 `verify.py` 还需要两个冻结外部点：`R-964.../combined_702.json` 和 `R-c4f.../attractive_nested_exact.json`。在当前本地取出的 R-23 原目录下运行时，程序在读取第一个外部点处以 `FileNotFoundError` 退出；失败输出与缺口保存在 `runs/promoted_fork_verify.*`。因此该 fork 没有被冒称为完整重放或 SPE 结论。

# 5. 与 half 目标和后续桥接

这组障碍的用途是限定证明路线：

1. 势能可以在 promotion/reset 中下降，但下降量不能由来源最后一步的 regret 统一支付；
2. 真实完整历史 IC 并不会自动消除这个 reset，因为上述 84 个比较和 replay 都是精确相等；
3. welfare 仍可达到实际最优 $W=OPT_3$，所以“桥失败”与“half 失败”是不同对象；
4. 后续若要把三余利润证书、森林根遗漏界或潜势分解接入六人 half，必须另行支付新分支的 exclusive reset tax，并保留完整有序历史、重复/空主题、零客户和任意平局。

本页不把三人 exact obstruction 外推为所有人数的 impossibility，也不把两个 promoted fork necessary-system 点当真实客户 SPE。Q-CAG-HALF 仍为 OPEN。

证据、SHA 和运行输出见 [R23 source evidence](../../tools/evidence/R23-promotion-reset-20261031/README.md)。
