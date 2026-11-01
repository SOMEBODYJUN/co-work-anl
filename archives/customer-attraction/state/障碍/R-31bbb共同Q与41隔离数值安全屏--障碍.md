# R-31bbb：共同 (Q) 模板与 41 客户隔离探针的数值安全屏

## 身份、范围与对象边界

本对象整理 R-31bbb6cfd6594bc8bb076db7b2950993/aggregate_security 下的六个直接源，并另行纳入一个被 `ssr_41_isolation_probe.py` 明确引用的冻结策略依赖 `e83dd064c0f6a8588794`。七个源均已由 Boss2 逐源 `clean show` 导出，冻结副本、清单、重放与验证位于
`archives/customer-attraction/tools/evidence/R-31bbb-security-root-20261031/`。

它们研究的是固定策略锥中的数值线性屏幕：

* `background_pair_numerical.json`：普通规模 (n\in\{3,4,5\})、有限随机背景与策略锥交替的 first-two pair-payment 探针，共 260 trials；
* `background_pair_large_numerical.json`：较大规模 (n\in\{5,6\})、(k\in\{6,7\}) 的同一数值探针，共 120 trials；
* `common_policy_Q_numerical.json` 与 `common_policy_Q_probe.py`：要求一个共同的背景分布 (Q) 同时压住每个纯查询与整条固定策略锥的线性模板，五个固定历史策略加 80 个随机锥，共 85 个 HiGHS 浮点 LP；
* `ssr_41_isolation_numerical.json` 与 `ssr_41_isolation_probe.py`：以 `all_optimal_query_failure_41.json` 的 41-client 纯策略为固定基线，在保持坏查询最优的面上重优化安全最优查询，共 1500 次浮点扰动；
* 依赖 `e83dd064c0f6a8588794` 是一个 3-player、5-topic 的 41-client 历史策略及其 `bad_optimal_query`/`good_optimal_query` 读数。它只为 SSR 探针提供冻结输入，不能把该源的“非 half 反例”描述扩张为当前六人、六提供者目标。

这些结果属于有限实验/障碍探针，不是完整历史纯 SPE 证书，也不是六人 CAG-HALF 定理或反例。`status` 中的 `numerical_only`、`numerical template screen only` 与脚本中的浮点 HiGHS 语义保持不变。

## 直接结果

### 1. 背景 pair-payment 屏幕

`background_pair_numerical.json` 报告 `status=numerical_only`、`trials=260`、`max_ratio=1.0`、`candidate=null`。其 incumbent 是 (n=3,k=5)，背景 `[1,0,2,5,0]`，`static_security=0.5`，`pair_payment=1.0`。

`background_pair_large_numerical.json` 报告 `status=numerical_only`、`trials=120`、`max_ratio=1.0`、`candidate=null`。其 incumbent 是 (n=5,k=7)，背景 `[1,0,1,3,0,2,1]`，`static_security=0.5`，`pair_payment=1.0`。

这里的比值是该脚本反复在固定策略锥与安全 LP 之间交替所得的数值读数；(2v\le 1) 只说明这些有限实例没有越过当前屏幕，不能推出所有历史或所有模型的 half 覆盖结论。脚本的 candidate 分支若触发只会保存一个浮点候选；本批两份结果均没有候选。

### 2. 共同 (Q) 模板

85 个案例的 `status` 全为 0（HiGHS optimal），维度分为 `(n,k)=(3,6)` 38 例、`(3,5)` 25 例、`(4,5)` 21 例和 `(3,4)` 1 例；`rows` 在 40--207，背景数量在 10--35。每个案例给出一个长度为 ((2^k-1)) 的浮点 (Q)，85 个 (Q) 的坐标和偏离 1 不超过 (2.3\times10^{-15})，最小坐标仅为 ( -3.72\times10^{-14}) 的浮点零，未见小于 (-10^{-10}) 的坐标。

这表示模板 LP 在所测固定策略/随机锥上找到可行的共同 (Q)。它没有给出有理化 (Q)、精确逐类型不等式、任意平局闭包或对六人六提供者模型的统一量词证明；因此归类为有限数值屏幕与可供后续精确化的候选结构。固定五个策略的前五个重放案例与原 `common_policy_Q_numerical.json` 逐字段相同，另外两例随机锥也已保存于 `common_smoke.json`。

### 3. 41-client SSR 隔离探针

原始结果 `ssr_41_isolation_numerical.json` 报告 `status=numerical_only`、`completed=1500`、`max_min_optimal_regret=0.0`、`counterexample_candidate=null`。记录的 incumbent 在 trial 25，`security=1/3`，`good_optimal_query=[1,0,0,0,0]`，五个 `R_values` 均为 1，`chosen_bad_R=1`。脚本明确把“坏查询保持最优”作为浮点容差约束，并在安全最优面上重新优化；因此这个 0.0 是该固定输入与有限扰动的最大最小 regret 读数，不是一个全局不存在性证明。

独立 smoke 以同一冻结依赖重跑两次，完成 2 trials、无 candidate；输出保存在 `ssr_smoke.json`。依赖的原始策略是 3-player/5-topic 41-client 数据，源本身的范围声明是反驳 ALL-optimal-query aggregate-static-regret bridge、而非 half-coverage 反例。这里保留该声明及其边界，不把背景客户数、提供者数或目标量词替换成当前主模型。

## 精确处置与失败机制

* 已精确检查的是：七个源的冻结 SHA/大小；85 个共同 (Q) 案例的 LP 状态、维度、坐标和；两份 background 结果的 trial/max-ratio/candidate 字段；SSR 1500 次结果及两次 smoke；源脚本和依赖脚本的 `py_compile`。
* 未完成且不应伪称完成的是：把浮点 (Q) 恢复为有理数并对所有 ordered histories、所有平局和所有六提供者客户盒逐行验证；把 41-client 依赖转换为当前六人模型；从这些数值屏幕推出 SPE 或 half 覆盖定理。
* 失败/障碍机制是量词与精度同时扩大：当前 LP 只在生成的固定策略锥和采样案例上成立，SSR 还固定了一个外部坏查询与策略；任何精确结论都需重建完整定义域、终局客户价值均分、所有偏离和任意 tie-break，并以 Fraction/整数残差或可审计证书封闭。

## 可接续工作

1. 从 85 个 (Q) 中按 `(n,k,name)` 聚类，尝试恢复低支撑有理候选，并对完整 ordered-history SPE cone 做逐项精确验证；若任一约束失败，保存第一条失败类型与量词位置。
2. 将 background pair 屏幕与 R-31bbb 五人投影必要行对象分开比较，不能把 pair-payment 读数当作 provider coverage 读数。
3. 若继续使用 SSR 依赖，先明确其 41-client、3-player、5-topic 身份，再构造六提供者模型的独立实例；保留坏/好最优查询的“ALL versus EXISTS”逻辑，不作模型替换。
4. 任何新候选必须单独标明“候选/有限实验/完整证明/障碍/原模型反例”，并在精确 verifier 通过前不提升为完整 SPE 结论。

## 证据索引

* `source-manifest.json`：六个 R-31bbb 直接源与一个相关依赖的 id、blob、SHA、字节数；
* `run-manifest.json`：原始结果、smoke 命令、依赖与局限；
* `validation.json`、`validate_r31sec.py`：七源 SHA、85 案例、两份背景结果、SSR 结果及 smoke 的独立断言；
* `source/`：六个原始冻结文件；`dependencies/`：共同 Q 所需 `background_pair_probe.py`、五个证书 JSON 与 SSR 的 41-client 策略；
* `common_smoke.json`、`ssr_smoke.json` 及 stdout/stderr：实际重放记录。
