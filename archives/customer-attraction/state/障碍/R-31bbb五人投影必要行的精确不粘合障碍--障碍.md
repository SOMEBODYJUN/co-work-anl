---
id: "customer-attraction/R-31bbb-saturation-exact-projection-obstruction-20261031"
kind: obstruction
type_tag: "障碍"
title: "五人投影必要行的精确不粘合障碍"
status: "finite-projection-obstruction-retained"
truth_status: "exact-rational-obstruction-to-row-summing; no-SPE-counterexample"
review_level: "six-source-full-read-plus-float-replay-and-Fraction-row-audit"
scope: "R-31bbb saturation actual AP/BNS projections for m=5; necessary rows only"
---

# 五人投影必要行的精确不粘合障碍

本对象清洗 `R-31bbb6cfd6594bc8bb076db7b2950993/saturation/` 的六个源：一般 AP 投影、对称 AP 投影、指定最大主题的对称 BNS 投影、一个有理 witness、其审计程序，以及 AP 建模程序。原件、冻结 SHA、运行和验证见 `archives/customer-attraction/tools/evidence/R-31bbb-saturation-20261031/`。

## 1. 投影模型和浮点 LP

`actual_ap_projection.py` 把五个实际主题与五个终局主题编码成 10 位客户成员 mask。对每个前缀位置 (i)，令 (k=5-i)，实际负载 (b)、实际主题的单位客户份额 (u)，以及任意主题的容量份额 `sizes`。它写入三类必要行：

- `floor`：(u_ige |F_c|/(b+k))；
- `AP`：把当前主题 (c) 强制后，任意主题 (d) 的终局收益不能超过由 (u_i)、(K_c) 与分支系数给出的必要式；
- 指定 `maxima` 时的 `maximum` 和 `BNS` 行：只对报告中指定的最大主题追加更强的有限行。

程序在客户 mask 上做线性规划，把实际覆盖归一为 1、最大化终局主题覆盖。它明确把范围写成 `Necessary projection only; no SPE construction.`，没有策略树、历史节点、支付或完整偏离比较。

复跑结果：

| 导出 | 变量 | 行 | optimum | 备注 |
|---|---:|---:|---:|---|
| 一般 AP m=5 | 1023 | 450 | 2.3158682560504453 | 非对称 mask LP |
| 对称 AP m=5 | 32 | 450 | 2.3158682560504418 | 每个 actual mask 平均到五个终局位 |
| 对称 BNS m=5 | 32 | 930 | 2.225443383452107 | 指定 maxima `[[2,3,5],[4,5],[4,5],[5]]` |

两种 AP 解的浮点目标相同到数值误差；BNS 仍大于 2。`min_slack_float` 约为 (10^{-14}) 至 (10^{-15}) 的负舍入量，不能当成严格违反行。所有复跑都由 HiGHS 返回 status 0，并保存 stdout/stderr。

这些目标大于 2 只说明“把这些必要行单独相加”不足以推出 half。它们没有给出原模型的可实现完整策略，也没有给出 SPE 反例。

## 2. 有理 witness 的实际核验

`exact_projection_witness.json` 给出一个五实际主题、五终局位的对称支持。每个实际成员 mask (a) 的群质量再平均放到五个终局位 (a\mathbin{|}2^{5+t})。总实际福利归一为
\[
W=1.
\]
由这些终局位得到的比较并集是
\[
\operatorname{comparison\_union}=\frac{3311537042}{1488034729}
\approx2.2254433834521077,
\]
所以
\[
\operatorname{comparison\_union}-2W
=\frac{335467584}{1488034729}
\approx0.2254433834521076>0.
\]

该 witness 的独有价值是把 BNS 浮点顶点重新构造成有理群质量，而不是把浮点目标直接写成精确结论。`exact_projection_witness.py` 读取 BNS 支持，使用 `limit_denominator(10000)` 恢复系数，解紧约束线性系统，再用 `Fraction` 逐行重算：50 条 floor、400 条 AP、250 条 `BNS_all_maxima`，总计 700 条必要行全部非负；最小 AP 松弛为
\[
\frac{6484381029}{74401736450}>0.
\]
复跑产生的 JSON 与冻结 witness 字节一致，且 `validation.json` 通过 SHA、大小、编译、目标、行数和这些有理值检查。

“精确”在此处指恢复后的有限投影支持和必要行审计使用有理数；它不指浮点 LP 的最优性已经被形式化证明。witness 也没有 continuation tree、支付表、完整有序历史或偏离检查，因此不能成为 `OPT>2W` 的 SPE 反例。

## 3. 与已有对象的比较与缺口

已有“隐藏回复价格投影审计”已经说明真实源的 (u/K) 局部行必须由同一份客户资料和真实后继共同计账，不能把不同源的投影行直接相加。本批进一步给出一个五人对称投影的有理点：即使 floor/AP/BNS 必要行逐条成立，也能有终局并集超过 (2W)。这与已有“两两非负客户投影不能共同实现”和 R-18 对称投影记录的处置一致：局部投影或浮点候选不是共同客户实例，更不是 SPE。

后续若要把这个障碍升级为原模型结论，必须补齐同一客户集合、六提供者（或明确其他人数）完整有序历史策略、终局客户价值均分、所有离轨历史和任意平局的支付/激励。当前六源没有覆盖空主题、重复主题、零客户和完整六人量词，也没有证明六人 half 命题或构造其反例。保留该源是为了防止后续把“必要行 LP 有 gap”误读为完整博弈证书。
