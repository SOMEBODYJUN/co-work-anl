---
id: customer-attraction/r18-full-terminal-tax-finite-cones
kind: computation
type_tag: 计算
title: 全终局税有限锥与不交族的趋紧机制
status: finite-cones; analytic-disjoint-family; general-tax-bound-open
summary: 客户负载税的有限锥值与经典不交族精确公式分开；完整SPE族给税余量1/(m+1)，一般付款仍未证明。
source_refs:
  - local:archives/customer-attraction/tools/evidence/R-18-round3-terminal-tax-20261031/
---

# R-18 round3：全终局税候选的有限锥探针

## 来源和对象

本页处置 `d3b7b28c92aa8465da20`（round3 README）、`4a7b2a4b9f48676f6020`（改变一次目标行的完整历史联合 MILP）、`f3317489c39e7532b0ad`（其 m=3,p=4 输出）、`ea58dd32069e528f8799`（指定完整 SPE 锥的全终局税探针）和 `0120755c1d3a1646412d`（探针输出）。五份原文和复现记录在 `archives/customer-attraction/tools/evidence/R-18-round3-terminal-tax-20261031/`。

README 明确主目标 Q-CAG-HALF 仍开放，并提出待检验的较弱候选

\[ OPT_m \le W+\tau_{full},\qquad \tau_{full}=\sum_{x:c_x>0}\frac{c_x}{c_x+1}, \]

其中 `x` 是客户，`c_x` 是实际终局中覆盖该客户的提供者人数；税按客户求和，不按主题求和。若真对所有完整纯 SPE 成立，逐客户由0≤c_x≤m得τ_full≤mW/(m+1)，因此OPT_m≤(2−1/(m+1))W；但 README 也明确这不是已证定理，前 m−1 根税反例不能直接否定它。

## 实读算法和复现

`full_terminal_tax_joint.py` 精确读取既有 `cone_attack_joint_milp.joint_candidate` 的全树动作/收益/根保证约束，只替换一次目标行，把每个覆盖系数减去对应负载税 `c/(c+1)`。浮点 MILP 只生成候选；脚本随后调用 `full_terminal_tax_probe.attack`，以 Fraction 重新验证固定策略锥端点。实际在当前复现依赖上以 `--topics 4`、三条路径 `012,001,000`、20 秒限时运行，三次 HiGHS 均 status 0（183 variables、84 binary actions、952 constraints），精确固定锥值分别为 `1/2`、`13/18`、`11/12`。输出中的 `floating_bound_not_a_certificate=true` 被保留，不能把数值最优误称全局证书。

`full_terminal_tax_probe.py` 逐个构造根税四人、经典 `m=1,...,5`、reply_cycle 与 overlap_cycle 的指定完整 SPE 锥，枚举 4 个可信续局模式并在每个支持集上解线性规划，再用有理锥检查。实际 `variants=1` 回放得到：root-tax-four-player `19/20`；classic-1 至 classic-5 为 `1/2,5/6,11/12,19/20,29/30`；reply_cycle 四模式均 `53/60`；overlap_cycle 四模式均 `8/11`。没有 >1 的端点。

## 经典数值的一般机制

有限序列1/2、5/6、11/12、19/20、29/30不是五种不同现象。取m个互不交主题：大主题A含m位客户，其余m−1个主题各含一位私有客户。给每个有序历史后的所有尚未行动者规定选A。若当前深度为d、过去有b位选A，规定行动的收益为m/(b+m−d)≥1；偏离某个单客户主题后，其余人仍选A，偏离收益至多1。因此这是一份在全部历史均成立的完整纯SPE，平局保留。

根终局满足

\[
 W=m,\quad\operatorname{OPT}_m=2m-1,\quad
 \tau_{\rm full}=\frac{m^2}{m+1},
\]

于是探针归一化目标为

\[
 \frac{\operatorname{OPT}_m-\tau_{\rm full}}{W}
 =1-\frac1{m(m+1)},\qquad
 W+\tau_{\rm full}-\operatorname{OPT}_m=\frac1{m+1}>0.
\]

这给出同一整数客户族的严格正税余量，并解释其趋紧机制；它不从有限LP值推出各固定锥的全局最优，更不证明任意目录的税候选。不同负载的客户即使属于同一主题也分别计税。

## 结论、用途和缺口

这些结果是有限指定策略锥上的候选/计算证据：它们支持“当前 14 类锥没有找到全终局税桥的违反端点”，并恢复经典族 `1-1/[m(m+1)]` 的数值图景。它们没有给出跨所有完整 SPE 策略的对偶乘子，也不处理任意平局、离轨历史和共同目录的普遍组合，因此不能证明 `OPT_m<=W+tau_full`，更不能证明 Q-CAG-HALF。

README 中同时保留的四客户块构造给出 `m=2k,W=OPT=4k` 而静态总正遗憾 `R=k/2`，从而排除用固定常数乘以人均福利的更强支付桥；它与全终局税候选是不同障碍。正式处置为 finite-cone-candidate-retained：保留代码、输入、精确回放和“浮点界不是证书”的限制，供第三阶段把候选税桥与已知根税失败、静态遗憾反例分层引用。
