# Boss4：一般全历史半覆盖的直接研究与接续

研究存档 `customer-attraction`；本 clone 程序身份 `R-6e3a5707f1f94c1d86bcbc61b4db4345`。
目标固定为 CAG-MODEL 中一般目录、任意人数、每个完整历史依赖纯 SPE 的 **Q-CAG-HALF**。
**主目标仍 OPEN；本轮没有一般证明或主目标反例。** 六名 gpt-6.1-sol ultra 内部研究员实际并行工作。

本目录是本轮可恢复个人备份，不自动升级共享 canonical；不认证外审、新颖性。

## 新认识和精确范围

| 文件 / 身份 | 内容、范围、证据与读取条件 |
| --- | --- |
| [equilibrium_tree/weak_theta_replication.md](equilibrium_tree/weak_theta_replication.md) | 任意 k≥1 的真实完整纯 SPE：m=3k、6k共同主题、36k客户、W=34k、OPT=36k、θ_m=12。因此 k≥4 反驳充分桥 W≥(m−1/2)θ_m。关键不是自动拼块，而是所有 nice 历史的收益10/12归纳，加不可逆坏前缀上的任意有限 BI 接管。需要分清真实随机查询安全值与自适应末位值时读取。 |
| [equilibrium_tree/weak_theta_replication_audit.py](equilibrium_tree/weak_theta_replication_audit.py) | 零求解器导入、展开36单位客户的 Fraction 局部进入表审计；有限算术只核对所有参数归纳中的基本类型。独立研究员从实例重建 nice/LIFO 策略，审查在 potential_representation/。 |
| [parent/weighted_terminal_price.md](parent/weighted_terminal_price.md) | B4-PARAMETRIC-TERMINAL-PRICE-v1：任意固定有序前缀背景 p，恰剩两人实际 A,B，q_x∈[0,1]、η≥0，令 tη=min{1/(p+1),1/(p+2)+η/(p+1+1_A)}，证明 B_q(u_A)≤ηu_B+Σ(q−tη)_+。真实 S,Z,V 共同菜单消去联合会员；保护集 D⊆{p=0}\\A 给 B_D(u_A)≤u_B/2。没有推广到较早玩家。 |
| [charging_duality/parametric_terminal_price_review.md](charging_duality/parametric_terminal_price_review.md) | 独立重构原始三类 SPE 行、所有参数角点及总权<1缩放。说明克隆行只方便表示，原始客户总和上界反而增加非负 λ(u_B−C_A)。 |
| [parent/audit_weighted_terminal_price.py](parent/audit_weighted_terminal_price.py) | Fraction 检查原始三行展开、全部分段角点、η端点；输出同目录 weighted_terminal_price_audit.json。不把有限计算作为一般证明。 |
| [counterexample_search/](counterexample_search/) | 完整历史策略锥价格攻击与核心/相同卫星块的集合值对称商求解。有限范围由实际 JSON 与代码固定；未找到反例无一般真值含义。对称商保留每个可行角色分配，不等于固定对称策略。 |
| [independent_attack/](independent_attack/) | 保护未覆盖客户、组合扩张候选与九个完整策略锥的有限攻击；尚无一般支付。 |
| [continuation_induction/](continuation_induction/) | 任意背景剩余价格信用与全局剩余利润加新覆盖不变量的探索；局部机会成本归纳已有真实失败，不能将其恢复为假设。 |
| [potential_representation/](potential_representation/) | 独立构造攻击与审查；还检查了静态最差PNE比较换成调和势的失败机制。 |

## 主目标的真正缺口

价格 B_q(v)=max_{z≥0}[Σq_x min(1,Σ_{T∋x}z_T)−vΣz]。
若一般能证 B_1(min_i u_i)≤W，则 OPT_m≤W+m min_i u_i≤2W；
现只获得真实末两层菜单的不等式。更早偏离改变多个后继，不能把他们合为末位最佳回复。
末位 θ_m 的弱聚合桥已由本轮真实复制族排除；真正不观察查询的 v_m 聚合桥仍 OPEN。

下一步须带着可核查的跨真实分支补偿去攻击早期价格/受保护集不变量，
或改变表示并构造完整可信反例。不要再将固定尾部保底、静态PNE/CCE福利比较、
最坏末位值聚合或有限无反例当作一般证明。精确模型与既有可靠结果仍从根 README 恢复。
