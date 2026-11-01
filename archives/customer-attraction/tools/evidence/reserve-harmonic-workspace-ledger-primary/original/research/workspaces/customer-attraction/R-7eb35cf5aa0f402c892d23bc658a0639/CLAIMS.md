# 本轮精确命题与状态

## Q-CAG-HALF

对象、定义、域、量词、假设与结论全部沿 research/current/customer_attraction/model.md 及原目标。有限单位客户、共同非空有限目录、任意 m≥1、每个全有序历史纯 SPE、任意离轨平局，欲证 2W≥OPT_m；重复、空主题、零客户均保留。状态 **OPEN**。本轮无主目标证明或反例。

## B6-UNIFORM-RESERVE-OBSTRUCTION-v1

- Exact statement / objects / domain：整数 k,t≥1，x,b>0，a,d≥0；所有参数为整数。两两不交客户块 X_i,Y_i,Z_r,V_r 大小分别 x,a,b,d，共同目录恰为 A_i=X_i∪Y_i，C_i=X_i，B_ir=X_i∪Z_r，D_r=Z_r∪V_r（相同集合去重）。m=k+t。
- Quantifiers / assumptions：对每个此类实例、每个完整历史依赖纯 SPE，若其实际先各 C_i 一次再各 D_r 一次，两段内部顺序任意。
- Conclusion / scope：必 a≤x/2；W=kx+t(b+d)，OPT_m=k(x+a)+t(b+d)，所以 OPT_m/W≤3/2。不是一般无拥挤 SPE 的 3/2 定理。
- Definitions / dependencies：原模型；真正实际末位比较给 d≥x/2、a+x/2≤b+d；合法子历史的纯 SPE 限制；人数归纳。无需指定惩罚续局。
- Evidence：自足解析证明、另一分支盲重构后审查、root 独立重构；去重目录及逐单位 Fraction 有限重放。
- Counterevidence / objections：未发现仍成立的致命异议。一般目录可能多动作触及同一储备、复合动作一次触及多个储备、价值不统一；没有外推。
- Status：独立内部解析检查通过；个人研究资产。未外审、未认证新颖性、未正式共享入库。
- Related files：reserve/uniform_reserve_obstruction.md、reserve/audit_uniform_reserve.py、reserve/uniform_reserve_audit.json、reviews/uniform_reserve_independent_review.md。

## B6-HARMONIC-MATCHING-FLOOR-v1

- Exact statement / objects：任意 m≥1、原共同目录模型的任意完整纯策略 σ（不要求 SPE），实际有序终局 S_i、C=∪S_i、W=|C|。任意比较 m 元组 T_j 允许重复，O=∪T_j、Q=|O|、D=|O\C|、c_x=实际客户负载、H_0=0。
- Definitions：V_i(T) 是在真实实际前缀改 T 后沿原完整策略的真实最终收益；M=max_π Σ_i V_i(T_π(i))，排列比较槽索引。
- Quantifiers / assumptions：对全部上述实例、策略、比较组合与离轨历史选择成立；无额外最优性假设。
- Conclusion：M≥(1/m)Σ_(x∈O)[c_x/m+H_m−H_cx]≥[Q+(H_m−1)D]/m。保留 d_x=#{j:x∈T_j} 时可将第一式每项再乘 d_x。若 Q>0 且 W/Q≥1−1/(m−H_m+1)，则 M≥Q−W；Q=0 弱式自动成立。
- Dependencies：真实偏离最终分母≤实际前缀负载+剩余人数，均匀排列平均，逐客户相邻 01→10 前移。
- Evidence：作者与另一分支独立一般证明，root 重构；两份 Fraction 脚本，一份不导入 canonical/被审实现。
- Counterevidence / limitations：该下界在大人数时不足以证明一般弱匹配；不能反推负下界即存在真实反例。旧资产已含相近鲁棒分母和前移公式，不宣称新数学机制或新颖性。
- Status：组合工具表示，独立内审通过；一般弱匹配与 Q-CAG-HALF 仍 OPEN；未外审。
- Related files：weak_matching/ 与 reviews/harmonic_matching_*。
