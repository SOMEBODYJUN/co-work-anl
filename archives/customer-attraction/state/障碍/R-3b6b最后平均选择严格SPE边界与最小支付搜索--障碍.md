# R-3b6b：最后平均选择器的严格 SPE 边界与最小支付搜索

## 范围和分类

本对象处理 R-3b6b03db882e4de48cfa5b406f57ef8f/potential_exchange 下七个冻结源。证据包在 `archives/customer-attraction/tools/evidence/R-3b6b-potential-exchange-20261031/`，含 clean-show 元数据、依赖包、独立 Fraction verifier、重放和验证器。

这里的主线是一个“最后玩家平均选择器”断言：是否存在一个最低福利 SPE，使最后玩家的效用不超过 (W/n)。源文件给出两个 3-player、4-topic 实例；它们的完整策略树、终局福利和最优覆盖都已做定义级精确核验。结果是固定实例对该选择器断言的反例边界，仍属于三玩家四主题小模型，不能代入当前六人六提供者目标。

## 两个精确证书

### 大证书

`last_average_selection_certificate.json` 有 3 个玩家、4 个主题、49 个单位客户，供应的完整策略树终局计数为 ([0,2,1,0])，源记录 `min_welfare=45`、`opt=49`，并列出唯一的 `all_spe_terminal_counts=[[0,2,1,0]]`。独立 verifier 遍历 21 个决策历史和 63 个单步偏离，得到 (W=45)、(OPT=49)，路径为 ((1,2,1))，玩家效用
[
(91/6,;44/3,;91/6).
]
最后玩家效用 (91/6) 大于 (W/n=15)，所以该实例排除了“最低福利 SPE 的最后玩家必不超过平均福利”的选择器读法。半覆盖余量 (2W-OPT=41) 为正，不能把它写成 half 反例。

### 小证书与严格唯一性

`last_average_selection_small_certificate.json` 有 3 个玩家、4 个主题、16 个单位客户，同一终局计数 ([0,2,1,0])，源记录 (W=16=OPT)。`audit_last_average_selection.py` 不依赖 canonical solver，在所有 21 个 ordered histories、84 个含自身比较和 63 个非自身偏离上以 Fraction 检查；最小严格余量为 (1/6)。每个节点处方动作严格优于其他动作，逆向归纳因此给出唯一完整纯 SPE。路径为 ((1,2,1))，玩家效用
[
(11/2,;5,;11/2),
]
最后玩家效用 (11/2) 比 (W/n=16/3) 高 (1/6)，而 (2W-OPT=16)。独立审计 JSON 与实际重放逐字段相同。

源中的 `milp_optimality_for_this_policy_only` 只说明小证书相关的固定策略 MILP 在 HiGHS 中达到该策略的 LP 最优，不能扩展为所有策略或所有 SPE 的搜索最优性。这里真正支撑唯一性的证据是逐历史严格 Fraction 比较。

## 最小支付搜索

`min_payoff_lp_search.py` 用 repository `ExactSPESolver` 生成固定策略，再把该策略的实际 ordered-history 激励行送入浮点 LP，搜索更强的
[
OPT \le W+(m-1)\min_i u_i
]
桥。两个冻结搜索结果均没有候选：

* `min_payoff_lp_discovery.json`：seed 81891、1000 trials、425 个不重复策略、`best_gap_normalized=8.326672684688674e-17`；
* `min_payoff_k5_m3_discovery.json`：seed 81891、1000 trials、813 个不重复策略、`best_gap_normalized=1.3322676295501878e-15`。

这两个数值接近浮点零，不能视作精确零或不可能性证明。以相同脚本、seed 和依赖运行 20-trial smoke，得到 19 个策略、`result=no counterexample found`；这只是重放链路检查。整个搜索仍是有限固定策略样本，不能证明该桥对任意 full-history SPE 成立。

## 独有内容、障碍与接续

* 相比已有 R-3b6b 辅助锚点提升和 m5k7 证书对象，本批新增了“最低福利并不强迫最后玩家落在平均线以下”的两个精确小实例，并给出 (1/6) 的严格间隔；该内容已写入本对象和 `replay/audit_last_average_selection.json`。
* 大证书的 `all_spe_terminal_counts` 是源文件声明；本批独立 verifier 核对了所给完整策略和 (W/OPT)，没有重新枚举全部策略树的完整 SPE 集合。若要把“唯一最低终局计数”升格为独立全称结论，应另行复现枚举器并保留其平局处理。
* 最小支付搜索输出由浮点 LP 产生，候选恢复和每一行精确验证尚未形成桥的通用证书；因此保留为有限实验和障碍线索。
* 继续工作应先把最后玩家的顺序量词、(W/n) 与 (W/(n-1)) 两种断言分开，再把三玩家证书映射到六人终局客户价值均分模型；当前对象不处理空主题、重复主题、零客户或离轨历史的六人量词。

## 证据索引

`source-manifest.json` 保存七个源的冻结指纹；`run-manifest.json` 记录三条重放命令和局限；`validation.json`/`validate_r3b6potential.py` 检查 SHA、两份证书、63 条偏离、脚本编译与最小支付 smoke。`dependencies/customer_attraction/` 是只用于独立核验的冻结模型实现。
