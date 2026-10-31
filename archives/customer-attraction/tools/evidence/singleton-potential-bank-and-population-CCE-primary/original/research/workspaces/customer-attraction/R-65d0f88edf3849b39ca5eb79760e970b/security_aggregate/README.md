# 聚合安全值分支：本轮到达位置

2026-10-24。原 Q-CAG-HALF 仍 OPEN。本轮**没有新增已证的一般 SPE 承重关系**，没有聚合安全值或 half 反例；以下不以旧等价接口或有限阴性诊断计作正面进展。

一般输入始终是有限单位客户、任意有限非空共同目录、任意 m≥1、全部有序历史纯 SPE，保留任意历史依赖平局。安全值的静态竞争元组先联合确定，不观察查询的抽样实现。

- `population_cce_attempt.md`：未证明的跨人数静态 CCE 比较候选及其精确充分归约；没有构造所需 CCE。
- `population_cce_check.py/.json`：仅在九份已存在完整策略上计算同目录 m+1 人静态 CCE 的有限浮点诊断，没有严格新结论，不继续扩大同种扫描。
- `pair_kernel_check.py/.json`：自然得到的全路径两查询对称菜单预算的一次定义级精确诊断；随后查到其已在旧资产明确登记，故不是新候选或进展。单向加强也已被旧资产否定。

## 已读取、据此停止重复的旧接口

1. `research/current/customer_attraction/security_chain_and_local_boundary.md`：安全链望远镜正确，但局部 D_i≥0 为假；全局 W≥m v_m 和弱充分桥仍 OPEN。
2. `research/current/customer_attraction/global_security_budget_boundaries.md`：全 p 的总去相关及含激励松弛总补偿都为假；不否定安全最优 p 上的聚合支付。
3. `research/workspaces/customer-attraction/R-a0bb57fa24044a8794bc7991918a19c6/security_aggregate/safety_preserving_static_regret.md`：已提出 SSR，即某个安全最优 p 保留实际叶静态聚合无悔；没有证明，不重新命名。
4. `research/workspaces/customer-attraction/R-2d91ff13b4b44effbe7e78a60470bcc7/security/aggregate_subtree_distribution_attempt.md`：全部孩子安全对偶向量的合法嵌入已写清；标量 H_A 下界不足以给便宜混合，替代背景中旧根外部收益也未支付。
5. `research/workspaces/customer-attraction/R-64201cd12083425899e2d643ec9bc087/next_security/cartesian_limit.md`：三人非分解 Cartesian 产品的精确菜单、根门槛复制极限及生成条件已存在；本轮不继续固定三人专项。产品安全值可加性早见 `R-24bfbfd5ec7845b79374a1938c335df7/representation_product/product_representation.md`。
6. `research/workspaces/customer-attraction/R-d3981c0168644971803a9c3380ed687c/continuation_general/tree/pairwise_gap_identity.md`：全路径两查询对称预算 PW 是旧 OPEN 候选，准确缺口为对称差响应债 E 的跨路径支付；单向 Σ_i K_i(T,A)≤W 已被同目录旧例以 75/2>35 否定。
7. `research/workspaces/customer-attraction/R-4ffa8b85fa8847e09e45dcafc8e1326f/counterexample/root_insurance_security_threshold.md`：根保险的 v_m=s 与安全稀释成本一已先算出，不把再次算出这一等价 root-regret 阈值当进展。

## 本轮解析尝试中的实际缺口

在任意背景 b、余 r 人的全部孩子上，即使假设更小人数已证聚合安全桥，所得

    H_A ≥ (r−1) v_(r−1)(b+A) ≥ (r−1) v_r(b)

仍仅为每个孩子的总利润下界。实际利润 G=u+H_actual 的安全差是

    G−r v_r(b) = [u−v_r(b)] + [H_actual−(r−1)v_r(b)].

没有已证关系把第二个括号定量联到第一个；把孩子静态对偶替入其真实终局会改变旧根份额。该断点已被旧正文准确覆盖，本轮未补上。

下一步若继续本分支，应直接构造保留全部真实后继 IC 的跨孩子客户级支付，或对原强/弱聚合桥本身给出完整精确分离；本轮没有以“尚无构造”推断一般目标不可能。

## 后续 root 指定银行任务

`bank_punishment_blind_proof.md` 给新全参数银行命题的独立盲重构证明候选。承重工具是“固定背景下任意全局调和势最大新增计数均可由完整纯 SPE 实现”：当前选择目标已用资源中最终利润最大者，对目标内偏离沿同目标递归，对目标外偏离用一槽势交换封顶。银行惩罚目标取全部严格大于 s 的边际席位，再选当前块的一个 s 席位。

这是直接验证全部孩子 IC 的一般存在性构造，未把 PNE 自动当 SPE。root 已收到可独审通知，独审状态待其回传。本页前部“没有新增承重关系”描述银行任务前安全聚合探索的状态，银行证明只支付修复编译器所问的真实子树，不声称已完成半覆盖或聚合安全桥。

`audit_bank_punishment.py` 用 Fraction 独立于仓库规范求解器实现上述递归拼合，在 2≤m≤7 的全部 j,i,D 上检查目标势最大、每个完整构造 DAG 节点的所有动作 IC 及强制者利润≤s。322 个强制孩子、27061 个记忆目标 DAG 状态、92788 项动作比较通过；`bank_punishment_audit.json` 是本地冻结输出。有限审计只核实现，任意 m,j 的结论由正文归纳承重，不以扫描范围代替证明。
