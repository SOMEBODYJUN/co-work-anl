# 本轮精确命题账本

2026-10-24。个人阶段资产，非共享canonical状态提升。

## Q-CAG-HALF（原身份不变）

- Objects / Domain：有限单位客户 N、有限非空共同主题目录 S⊆2^N、任意 m>=1；单位提供者依次观察完整有序历史各选一题。
- Quantifiers：每个实例、每个完整历史依赖纯 SPE；全部离轨历史、任意平局、空主题、重复行动、零客户。
- Definitions：u_i=Σ_(x∈B_i)1/c_x，W=Σu_i，OPT_m=max_m主题并集大小。
- Conclusion：2W>=OPT_m。
- Status：OPEN。本轮无一般证明、无真正反例，无新无条件福利界。
- Dependencies：原[CAG-MODEL](../../../current/customer_attraction/model.md)；新增强化候选的失败不改此身份。

## B18-LOCAL-REFUND-v1 / v2

**Exact Statement。** 固定任意上述实例、根完整SPE终局B、C=∪B_i，最优m主题联合O，D=O\C。令 f_D(r)=max_(T_1,...,T_r∈S)|D∩∪T_j|，f_D(0)=0，e_i(O)=Σ_(x∈B_i\O)1/c_B(x)。

- v1：对每个最优O、每个实际位置i，u_i+e_i(O)>=f_D(m-i+1)−f_D(m-i)。
- v2：存在一个最优O，使全部实际位置i同时满足上述不等式。
- Scope：仅原根实际路径，未加强到任意背景或修改SPE。
- Assumptions：除CAG-MODEL无额外条件；尤其不能假设遗漏全局私有或同计数历史同回复。
- Conclusion / sufficiency：任一版本若成立，对同一O求和给W+|C\O|>=|O\C|，从而half。
- Status：**FALSE（v1、v2均被完整原模型反例否定）**。
- Evidence：179单位客户、7个不同主题、m=3；唯一最优无序组合(0,2,3)。实际(P,A,B)，u=(34,35,38)，W107，OPT111，f_D=(0,36,72,72)，e=(34,0,34)。位置2严格35<36。
- Counterevidence / objections：未发现反例证书的成立异议；全部57历史399比较精确通过。它不否定可转移共享信用，三行总余额103>0。
- Dependencies / source：旧71客户唯一最优遗漏机制经整数放大、轻改A私有客户并加合法不交主题P；不是从头独立的新博弈机制。
- Review：作者解析表及定义审计；独立研究员未读作者证明先核原始JSON；父方第三实现核全部399IC和343有序比较。均为内部审查；无外审或全球新颖性认证。
- Related Files：[自足正文](refund/unique_optimum_refund_floor_counterexample.md)、[原始证书](refund/prefixed_refund_counterexample.json)、[盲审](independent/refund_candidate_blind_review.md)、[父方结果](parent/refund_unit_audit.json)。

## B18-SHARED-REFUND（工作义务，未提升）

放弃逐位置固定e_i，仍需用真实完整树IC支付L−E<=W。自由转账总量条件就是half，故不另设“已证转账定理”。O投影下实际路径后悔总额可由E一次支付，但离轨节点拥有各自不同退款池；投影计划未证SPE、也未证明可共同修复。状态：OPEN接口。见[工作稿](GENERAL_WORKING.md)与[投影记账](refund/shared_refund_projection.md)。

## 静态组件与旧机制特化

EXCHANGE-MULTISLOT-v1 的ME/MM是最优补全可行性的集合恒等/子集计数；对所有输入成立，不使用新后继IC。CA-SC-REACTIVE-TAIL-DEBT-IDENTITY-v1 是旧Taylor/协方差/曲率机制的池化版本；不认领新付款。分别见exchange/与security/正文及实际审查范围。本轮不把二者登记成新增half正面成果。
