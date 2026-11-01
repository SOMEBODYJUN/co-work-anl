# R-3b6b：全策略锥/CCE 交替攻击的数值屏幕

## 范围

本对象整理 security_global 的六个直接源：三份随机 full-policy cone/CCE-dual 结果、一个既有障碍策略的 named 结果、两个生成脚本。`cone_security_search.py` 是 Boss4 所有的相关依赖，仅为实际 smoke replay 保留，未冒领其来源。冻结源、依赖、重放和验证位于 `archives/customer-attraction/tools/evidence/R-3b6b-security-global-20261031/`。

所有直接源都明确写出 finite numerical、all ordered histories retained、no universal claim 或 not new instances。这里的 CCE 读数是固定策略锥中的交替线性屏幕；它们不是当前六人六提供者模型的 SPE 证明或反例。

## 冻结结果

* `cone_cce_n3k4.json`：10 个 (n=3,k=4) 案例，每案 21 ordered histories、33--42 个 unique gamma rows，200 个 cone LP；`best_CCE_ratio` 最大为 1（一个案例为约 0.977799）。
* `cone_cce_n4k5.json`：10 个 (n=4,k=5) 案例，每案 156 histories、174--199 gamma rows，200 个 cone LP；全部 `best_CCE_ratio\le1+10^{-12}`。
* `cone_cce_n5k7.json`：8 个 (n=5,k=7) 案例，每案 2,801 histories、1,581--1,698 gamma rows，160 个 cone LP；全部 `best_CCE_ratio=1`。
* `cone_cce_named.json`：对已有 `individual_security_failure`、`local_security_increment`、`global_decorrelation_failure`、`dynamic_iid_local` 四份策略运行；histories 分别 43、43、259、2,801，best ratio 约为 0.993055、0.991746、1、0.997678，未出现 >1 的 candidate。

独立 smoke 以相同 `cone_cce_search.py` 和相关 `cone_security_search.py` 运行 1 个 (3\times4) 案例、2 starts、2 iterations、4 个 cone LP，输出 `best_CCE_ratio=1` 且没有 witness。源脚本和相关依赖均通过 `py_compile`；验证器还逐源核对 direct SHA/size。

## 数学含义与限制

这组屏幕的正确 dual 明确为
[(1-\sum_a\lambda_a)W+\sum_a\lambda_aD_a.]
脚本把完整 ordered-history strategy cone 的 γ 行与静态 CCE dual 交替优化，并保留全历史动作约束；因此它能检验某些已有证书/随机实例是否在这一路线下产生有限的 >1 读数。当前所有读数都未越过 1，说明这些有限锥、固定 seeds 和已有障碍策略没有产生新数值候选。

它仍然不是全称结论：

1. LP 系数是浮点数，未给有理化 dual 或逐行整数残差；
2. `cone_cce_n3k4/n4k5/n5k7` 只覆盖有限随机客户类型和有限 starts/iterations；
3. `cone_cce_named` 复用已有策略，不重新构造所有六提供者、六人、任意 tie-break 的模型；
4. `best_CCE_ratio\le1` 是在该固定策略锥中没有找到候选，不等价于整个 SPE 联集的半覆盖定理。

因此本批归类为有限实验与障碍屏幕。后续若要精确化，应先固定一个候选策略和客户盒，用 Fraction 重建 γ、(W)、(D_a) 全部行，再逐 ordered history、终局均分、空/重复主题和任意平局验证；若发现 >1 浮点 witness，也必须经过独立完整 SPE verifier 才能升格。
