# 安全值与精确终局税：本轮工作区

2026-10-21。主目标 Q-CAG-HALF、一般聚合安全桥 W≥m v_m、一般精确分数税桥均未证明。没有找到这些目标的反例。

## 已证、候选与探索分开

- `pair_common_query.md`：固定任意非负客户背景、恰剩两人时，共同静态查询总收益 F_b(T)≤R+min(u_1,u_2) 的自足证明。`audit_pair_common_query.py` 是独立 Fraction membership 核验，不导入规范求解器。
- 一般 F(T)≤W+min_i u_i 是**已失败候选**：direct_global 的六人填充残余实例已通过本工作区的定义级独立 DAG 审查（见 `padded_residual_m6_review.md`）；本文件不将二人证明外推。
- 尚未证明的分数税候选：α=(m−1)/m，g_α(T)=Σ_{x∈T}1/(1+αc_x)，G_α=Σ_{c_x>0}1/(1+αc_x)，要求 m max_T g_α(T)≤W+G_α。它结合已有 OPT≤mM+W−G_α 即给半覆盖。
- 更强的、仍无证明的逐人候选 u_i≥max_T g_α(T)−G_α/m；仅探索性扫描未见失败，不能因此提升。

## 浮点探索文件的准确边界

`refined_fractional_scan.py` 对指定完整形式策略的非负客户锥做浮点 LP；约束由全部保存历史真实偏离重建，计算时可合并相同浮点系数行。它不产生精确通用证书；所有 negative findings 仅是未发现分离向量。

`random_refined_scan.py` 是固定人数目录规模的浮点全集续局探索和随机/局部优化；`policy_iteration.py` 是新 count-dependent 完整策略的浮点 cone/LP 迭代。这些生成器不证明任意 SPE 的结论，历史依赖策略的一般合同不被 count 策略样本覆盖。

已执行：八个命名旧策略锥上 aggregate 与 individual 分数税目标无浮点 separator；另五人十主题 individual-security 策略锥的 aggregate 目标亦无 separator。随机五人七主题 aggregate 1000 次，individual 5000 次；新五人七主题 individual 策略 cone 300 步，七人八主题 100 步，common-min 五人七主题 500 步均未见正 gap。common-min 扫描随后被另一机制的明确六人候选反例超越，应勿重扫此模板。

## 共享残余 gadget 的两个显式安全边界

设 m−1 个私人 A_i 各有4客户；B,T 各有3私人及2共享块客户；D_i,E_i 各覆盖 A_i 的不同2客户半块与两类 B/T 共享块。实际 A_1,…,A_{m−1},B 时所有实际客户负载为1，W=4m+1，T 的5客户全未覆盖。

此处只核对静态代数，完整 SPE 真实性由 direct_global 的独立证书另外承担：

- F(T)=5m，所以 F(T)−W=m−1；m≥6 时超过 min ui=4。
- G_α=(4m+1)m/(2m−1)，早期玩家 individual fractional 候选余额 4−5+G_α/m=(2m+2)/(2m−1)>0，故不否定该候选。
- 静态不观察查询的纯对手背景 D_1,…,D_{m−1} 下，查询值分别为 A_i=3，D_i=1+4/m，E_i=2+4/m，B=T=3+2/m。因此 v_m≤3+2/m，给 W−m v_m≥m−1>0。它不反驳聚合安全值桥。

## 下一步

六人填充残余 gadget 的定义级独立 DAG 审计已完成并通过，发现并修正 OPT30→26 的错误；详见审查正文、标准库审计脚本与冻结 JSON 结果。不继续扩大随机阴性样本。一般人数共同查询加 G_α、逐人分数税以及全局安全债务仍须新的解析证明或真实完整反例。
