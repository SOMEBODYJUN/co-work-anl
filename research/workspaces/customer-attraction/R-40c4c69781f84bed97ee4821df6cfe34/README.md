# Boss5：共同客户耦合、可信续局与一般半覆盖

研究存档 `customer-attraction`；程序绑定身份 `R-40c4c69781f84bed97ee4821df6cfe34`。
本轮环境重置后恢复独立 main clone；此前 `R-5e9dedd2606746ff8afbbb73bf816e7a/`
及其来源 `R-18e993ca519949aba29e030d3d7b15b3/` 是已推送来源，不改写其历史。

## 精确主目标与状态

**Q-CAG-HALF 仍 OPEN。** 对所有有限单位客户、有限非空共同目录、任意人数，
每一个完整有序历史依赖纯 SPE 都应满足 `2W >= OPT_m`。
离轨历史、任意平局、重复主题、空主题和零客户保持原模型量词。
本目录是阶段研究备份，不自动改变共享 canonical 命题状态。

## 可接续资产与用途

| 路径 | 数学内容、范围与读取条件 |
| --- | --- |
| [counterexample/unanimous_continuation_closure.md](counterexample/unanimous_continuation_closure.md) | 同一剩余人数 q>=2、两个不同覆盖主题在对称差上的背景一致时，两种相应全员同主题 SPE 续局不能并存。给出多惩罚者放大无拥挤族的具体共同目录闭包失败机制；不是 half 反例。 |
| [direct_global/monochromatic_closure_review.md](direct_global/monochromatic_closure_review.md) | 未读发现稿的独立定义级证明与量词攻击；Boss 再从末位最佳式复核。仅内部审查，外审与新颖性均未认证。 |
| direct_global/ | 弱逐人覆盖缺口 `m u_i >= OPT_m-W` 的探索；强残余桥 `OPT_m(N\\C)<=W` 已有真实反例，不再当候选。 |
| security/ | 真正静态混合安全值的聚合支付与策略统一的静态对偶分布；不能以逐人安全值、末位最坏回复或固定实际负载桥替代。 |
| tree_coupling/ | 完整共同非负客户锥与有限支持局部实现之间的缺口。共同 signed Shapley 关系及各局部表示仍不能直接等同全局非负测度。 |
| new_mechanism/ | 频率二 / 二次 fresh 博弈的结构性收益机制及独立攻击；子类不外推成一般结论。 |
| independent/ | 全终局税 `OPT_m <= W + sum c/(c+1)` 的独立攻击与完整策略锥检验。有限阴性结果不作为一般证据。 |

## 已排除的重复工作与关键缺口

近重复终局 `(m-1)A+B` 的末位为 A 时，末位查询单独已经足够 half；末位为 B
由 Boss10 已推送的两支持末两位不同证明覆盖。
两支持末位 B 的鲁棒交叉频次筛选 `l(2k+1)>=k^2-1` 也已存在于
`R-31bbb6cfd6594bc8bb076db7b2950993/credible_search/two_theme_terminal.md`，
本轮重构不算新结果。仍需处理稀末位主题、末两位相同及无界实际支持数。

一般瓶颈仍是将不同真实偏离分支共同支付给实际福利。
新的单色续局障碍只否定一种一致惩罚构造；下一步允许非一致可信续局，
并研究共同客户非负结构怎样产生跨完整树的非负支付。
探索不等待审查；每一项成熟推导分别保存精确范围和真正未完成的义务。
