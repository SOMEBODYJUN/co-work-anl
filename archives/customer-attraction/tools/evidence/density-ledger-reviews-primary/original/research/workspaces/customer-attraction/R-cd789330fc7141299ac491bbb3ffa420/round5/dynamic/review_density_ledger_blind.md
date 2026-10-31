# incoming density ledger 盲重构冻结稿

2026-10-24，dynamic。**本稿在读取 `../rank/incoming_density_diagonal_ledger.md` 之前写成。** 仅收到 root 的精确公式陈述，独立核符号、全父子计数及 IC 适用域；不是 half 审查。

## 1. 必须固定的适用域

原输入保持任意人数、任意有限共同目录、全部有序历史纯 SPE。实际终局 Z、收益 u。这里的 fair-share flow 只跟踪原实际完全遗漏的客户 R：在任何 actual-prefix 查询 q 上，这些客户没有旧前缀覆盖，故其完整负载 c_q(x) 等于当前角色加真实未来 coverer 数，亦即 1+|F_q(x)|。

每客户可注入任意固定非负残源；全源质量记 M。角色严格递增，所以所有源质量最终吸收，且

    M=Σ_(q,x) f_q(x)/c_q(x)。                    (ABS)

若跟踪实际前缀已有覆盖的客户，则 c_q−1 不再等于出流角色数，以下 M−H 必须修改；不能无条件把本组件迁移到 I-query。

把同一 child query 的不同父 context 分拆为 g。若 g 是父查询 q 的真实未来角色 j，令 a=B_j 为父完成叶 B 中该角色的规定主题，A 是原实际 j 前缀下强制同一 a 后沿原 sigma 的叶，W 是 B 的 j 自然历史中改选原实际 S_j 后沿 sigma 的叶。对所有 x∈a，把 f_g 扩为零；正密度只来自 q 实际发送给 j 的跟踪客户。

## 2. 独立局部恒等式

写 D=u_j(A)>0，v=u_j(B)，v_W=u_j(W)，ell=v−v_W。取整行动概率测度

    μ_A(x)=(1/c_A(x))/D， x∈a。

它覆盖 a 的全部客户，不能只归一化到跟踪子集。因 B 中 j 的行动确为 a，对全部 x∈a 都有 c_B(x)>0。定义

    θ_g=E_μ f_g=(Σ_x f_g(x)/c_A(x))/D，
    J_g=Σ_x f_g(x)/c_B(x)。

直接展开 covariance：

    D Cov_μ(f_g,c_A/c_B)=J_g−θ_g v。

因此此 incoming 分量的实际 IC 费用 K_g=θ_g u_j 满足精确恒等式

    K_g=J_g + θ_g(u_j−v_W)
                  −D Cov_μ(f_g,c_A/c_B) −θ_g ell。  (LOCAL)

covariance 前面的负号正确。它可正可负；f_g 不必逐客户等于同一常数。若 D=0，则 incoming 吸收分子也为零，θ_g=K_g=J_g=0；该 g 全部项取零，不定义 μ_A 或除零比值。

## 3. 全父子基准恰为 M−H

对每个父 q 和正密度客户 x，父流向其 c_q(x)−1 名真实未来 coverer 各送 f_q(x)/c_q(x)。每条这样的父子边都以父叶 B=q 作 diagonal 分母 c_B=c_q，因此

    Σ_(g来自q) f_g(x)/c_B(x)
       =(c_q(x)−1)f_q(x)/c_q(x)^2
       =f_q(x)/c_q(x)−f_q(x)/c_q(x)^2。

把所有父子 context 恰各计一次，并用 ABS，得到

    Σ_g J_g=M−H，
    H=Σ_(q,x)f_q(x)/c_q(x)^2。

同一 child state 多父合并不破坏该式：θ 对 incoming 分子线性，K_in 可先按 g 求和后再合并回原唯一整条 query 系数。B、μ 协方差必须按父来源分开，不能把来自不同 B 的 c_B 混成一个分母。

将 LOCAL 求和即得 root 所报

    K_in=M−H+T+COV−L，
    T=Σ_g θ_g[u_j−v_j(W)]，
    COV=−Σ_g D Cov_(μ_A)(f_g,c_A/c_B)，
    L=Σ_g θ_g ell。

## 4. 原完整 IC 的合法性

父 q 当前行动后，未来都沿同一原 sigma；所以在其自然 j 历史 g，a=B_j 是规定行动，W 是该节点合法改选 S_j 的真实完整后继。因此 ell>=0 来自该节点一条完整 SPE IC。每个 θ_g 是固定实例上的非负常数，故 L 是合法整条 IC 的非负加权和；没有对客户分量分别使用 IC。

u_j(A)=D<=u_j 来自原 actual-prefix 的完整比较，也可按 g 分拆后购买同一条 IC。没有一条原 IC 自动比较 u_j 与 v_j(W)，因为两者前缀不同；T 必须保留有符号，不能宣称非负或非正。

结论（盲阶段）：在上述遗漏客户、自然 action-return、全部真实后继和零分母约定下，声明的恒等式、符号及 ell 的 IC 域均通过独立重构。H>=0、L>=0，但 T/COV 未付。此式本身不提供 K_in<=W 或 half，也未消去跨叶重置。
