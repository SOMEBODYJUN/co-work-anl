# 一般 Q-CAG-HALF：本轮并行工作稿

状态：OPEN。程序身份 R-8918a9ea76c74f88a9de75e2c4a948e9。只研究原 CAG-MODEL 的任意 m、任意有限共同目录、全部有序历史纯 SPE。

## 真实目标

固定原完整 SPE σ、实际叶 z、实际福利 W，任意 m 主题比较元组 T，O=其并集大小。目标 2W≥O；最终取最优元组。零客户、空主题、重复和任意历史平局均保留。

## 父方当前判别：真实查询 ROW 净差

对每个实际位置 i，Z_i(A) 是实际前缀强制 A 后沿同一 σ 的完整叶；d_i(A)=u_i(Z_i(A))，R_i(T)=Σ_j d_i(T_j)。候选 ROW-NET 要求 R_i(T)≥O−W（全部实际 i、全部比较元组）。这是已有开放候选的定向推进，不认领新颖性。若成立，SPE 给 R_i≤m u_i；对 i 求和闭合 half。

来源：R-e05f01e191354b028004b433016ae1c9/penultimate_true_query_row.md 已证明末/倒二 ROW；更早位置 OPEN。旧 portfolio_matching_counterexample.md 否定遗漏客户付款，不否 O−W。实际在比较并集外的覆盖信用不可丢。

## 六个竞争一般分支

- global_exchange/：全深度交换、精确势与积分核。
- menu_security/：完整 m 槽 Mpath 的 U-unif 支付。
- credible_induction/：保留原全树 IC 的联合退款与删位。
- source_payment/：同客户跨 context 共同钱包。
- strategy_geometry/：真实全树非负乘子及完整反例。
- independent_general/：独立一般重构与交叉审查。

所有关系保持候选、解析证明、内审、外审、新颖性分级。计算只做候选攻击与定义核验，有限阴性不支持一般真值。背景增量、静态价格/KKT、纯势及流恒等式已有来源；重复重构不算新增付款。

## 当前缺口

本轮尚无一般 half 证明或目标反例。更早 ROW 或更弱全路径预算需由真实后继 IC 支付；不能冻结后继、删除原玩家后假设保留 SPE，或把互斥子树福利直接送入根钱包。

## 父方精确化中的余量

实际末位逐客户有 R_m≥O−W+u_m；倒二已有 t_b(A) 与新覆盖 F/2 余量，不能分别用同一池相加。研究更早行必须保留真实多后继 IC。浮点策略锥仅生成候选；正点须整数化并逐有序历史重放原完整策略。
