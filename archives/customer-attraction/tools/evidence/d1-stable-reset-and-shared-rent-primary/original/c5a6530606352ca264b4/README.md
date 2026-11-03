# 完整动态菜单：本轮工作、旧接口校正与独立审查

2026-10-24。任务始终为任意人数、任意有限共同目录、全部有序历史纯 SPE 的 Q-CAG-HALF。主命题仍 OPEN。本轮尚未得到完成 half 的新全输入共同支付；没有把有限阴性或局部恒等式记作一般推进。root 统一保存，子研究员未 git 或外发。

## 1. 旧实际单列反例与自由菜单的准确区别

原输入为 [coverage_opportunity_failure.json](../../../../../examples/customer_attraction/coverage_opportunity_failure.json)，原完整证书为 [同名证书](../../../../../evidence/certificates/customer_attraction/coverage_opportunity_failure.json)，自足旧来源为 [逐期机会损失正文](../../../../current/customer_attraction/coverage_opportunity_counterexample.md)。这是旧十一单位客户实例，不是本轮新反例。

[本次独立定义级核验](review_actual_extra_failure.py)不导入规范模型、SPE 求解器、证书核验器或原审计；展开全部 11 名单位客户，检查全部 31 个有序历史和 155 项精确比较。实际终局 A,A,B、收益 (5/2,5/2,3)、W=8；主题顺序 A,B,T,D,E 的完整实际终局额外查询为

\[
(5/3,3/2,3,5/2,5/2).
\]

因此 `m max_T Σ_(x∈T)1/(1+c_actual(x))≤W` 被严格否定，坏差为 9−8=1。

这没有否定自由完整菜单 Mpath。一般地，实际末位完整菜单仅把最后一个行动改为任意 C，故其自由混合值**精确等于** `v_2(b_pre-last)`。在本例 b_pre-last=2A，匹配原始/对偶都可取

\[
p=q=(0,1/3,1/3,1/6,1/6),
\]

精确值为 7/3，且 `m v_2=7<W=8`。原始全部行值为 (19/12,7/3,7/3,7/3,7/3)，对偶全部列值为 (35/12,7/3,7/3,7/3,7/3)。故同例明确满足 LAST，并给 Mpath≤7/3。完整矩阵、真实各位置强制叶和结果保存于 [独立有理报告](review_actual_extra_failure.json)。这只是旧例的接口边界恢复。

## 2. α=1 的实际税桥同样已被旧十三人证书否定

确切旧正文：

`research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/security/refined_tax_counterexample.md`

该文已严格否定 α=(m−1)/m 的精确实际税桥。其同一个完整证书也否定 α=1 版本，以及更强 `m u_last≤W+G`。实际路径为 P^10,A,A,B，W=33、末位利润 3，P 客户 25 名负载 10，A 客户 5 名负载 2，B 客户 3 名负载 1，T 客户 3 名未覆盖。因此

\[
G=\sum_{x:c_x>0}\frac1{1+c_x}
=\frac53+\frac32+\frac{25}{11}=\frac{359}{66},
\]

\[
13\max_T\sum_{x\in T}\frac1{1+c_x}-W-G
=13u_{last}-W-G=\frac{37}{66}>0.
\]

[本次独立审计](review_actual_tax_alpha1.py)只读旧冻结 packet，未导入原审计、构造器或规范博弈实现；展开 36 名单位客户，精确复核 27,243 个全部可达自动机节点和 112,050 项 IC。根计数为零，每个决策节点都有全部六条观察行动边，每条边增加该行动一次并使深度加一，且仅深度 13 为终端。因此每个完整有序历史都唯一运行到已核验节点，覆盖全部离轨历史，不需展开指数规模树。真实终局按原规定边递推得到，未把 packet 的 desired 字段当作结果。详情在 [α=1 独立有理报告](review_actual_tax_alpha1.json)。

没有得到任意 padding 参数的解析扩展规则，也没有需要它：这里仅引用旧固定十三人、封闭完整自动机的严格实例。它不否定 LAST、Mpath、FTA、真正安全值聚合或原 half。旧资料若仍称 α=(m−1)/m 精确税桥未决，应按此旧来源校正，不认领新反例。

## 3. 新的末非 B 刚性：已独立盲重构的一般条件组件

见 [末非 B 刚性盲审](review_last_nonB_rigidity.md)。先只收到精确陈述，独立重构证明，再核对同额信用陈述。任意整数背景、任意尾人数、任意目录和完整历史 SPE 均保留；前提是“n−1 个 B 后末位 B 最佳”。最后一个非 B 行动由真实 IC 与最坏分母下界夹成精确平局，产生逐客户前缀刚性，并强制改 B 后原真实后继全为 B。n≥2 时其余尾玩家恰等额损失 ε；更早祖先的 IC 没有自动保存。这个条件引理不是全树付款或一般 half 的证明。

## 4. 未闭合探索及停止点

曾尝试自由 Mfull 动态最大原理、任意背景总尾利润 `V_b≥r v_(r+1)(b)`，以及随机有序前缀的删位势耦合。均未得到新承重关系。删去某个 iid 前缀行动后，真实尾策略仍依赖被删信息，不能用输入分布交换性当作尾叶可交换。

[BG-AGG 定向攻击脚本](attack_background_aggregate.py)及 [数值记录](attack_background_aggregate.json)仅针对上述明确一般候选，以固定完整策略锥、合法主题前缀、固定有理查询和全部静态竞争元组测试；150 次未分离。它是探索备份，不是一般正面证据，不继续同模板扩样。FTA/AP-extra、PAIR 旧反例和非根 relay 漏旧背景返还均已按 root 指示避免重做。
