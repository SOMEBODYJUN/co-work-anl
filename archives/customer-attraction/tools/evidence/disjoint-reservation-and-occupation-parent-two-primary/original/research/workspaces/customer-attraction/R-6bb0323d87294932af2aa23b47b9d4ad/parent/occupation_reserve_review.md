# 整数后继占用储备：root 的独立重构

主正文为 ../relay/working.md §§8–9。本文是 root 在未读取其最终证明时独立重构的检查，保留证明所需的整数量词；independent 分支另作盲重构。不是 half 证明，不提升 Q-CAG-HALF 的 OPEN 状态。

## Exact all-input contract

固定任意合法有序前缀及其整数背景 b。当前后尚有 n≥1 位单位玩家。固定任意完整形式计划，对每个合法根主题 A 读取其真实完成叶，客户 x 的根 membership 为 a_A(x)∈{0,1}，后继负载为 n_A(x)∈{0,…,n}。这里不需要这些后继已是 SPE。记

    d_A(x)=1+b_x+a_A(x)+n_A(x)，
    K(T,A)=Σ_(x∈T)1/d_A(x)。

取任意目录分布 p，令 q 为 A∼p 后所有 n 位真实后继主题的平均经验分布。定义

    G=pᵀKp，D=E_AΣ_(x∈A)1/[b_x+1+n_A(x)]，
    V⁺=E_AΣ_x n_A(x)/d_A(x)。

V⁺ 是添加独立一槽后的后继利润，不是原尾部总福利。结论为

    n qᵀKp=V⁺+I， I≥0；
    G+V⁺≤D+n qᵀKp。

若当前节点属于完整纯 SPE，另由真实整行 IC 得 D≤u，于是

    G+V⁺≤u+n qᵀKp。

此关系对任意人数、一般目录、全部有序历史和任意平局成立；空主题、重复主题、零客户均保留。最后一步只用了当前 IC，**没有**得到所缺的后继跨枝比较。

## Independent reconstruction

固定一个客户，简写 a,n_A,d_A，令 A,T iid∼p，Δn=n_A−n_T，Δa=a_A−a_T。因为 nq_x=E n_A，

    I_x=E n_A E(1/d_A)−E(n_A/d_A)
       =(1/2)E[Δn(Δn+Δa)/(d_A d_T)]≥0。

非负性逐对成立：Δn 是整数，Δa∈{−1,0,1}。这正是不能把结论直接搬到任意分数水位尾部的地方。

设 p_{0,k}=Pr(a_A=0,n_A=k)，p_{1,k}=Pr(a_A=1,n_A=k)。另由倒数差展开，

    I_x−(G_x−D_x)
      =Σ_k p_{1,k}(1−p_{0,k})/[(b+1+k)(b+2+k)]
       +(1/2)E[1_(Δn≠0)(Δn²−Δa²)/(d_A d_T)]≥0。

核对关键因子：原差是根 self-tax 加 (1/2)E[(Δn²−Δa²)/(d_A d_T)]。唯一负项发生在同 k、不同 a 的有序交叉对，合计恰为 −p_{1,k}p_{0,k}/[(b+1+k)(b+2+k)]，与 self-tax 的 p_{1,k} 项合并后得到展示式。其余 Δn≠0 项由整数性非负。逐客户求和得到第二个结论。

## Scope / evidence / unresolved step

root 的重构与 relay 最终展开一致，independent 盲重构确认了分母和有序 pair 的 1/2。相邻作者代码中的 Fraction 回归只检查实现，不承担全称证明。

若 G(p)=pᵀKp，q=Pp，沿 q−p 的导数为

    (q−p)ᵀ(K+Kᵀ)p=(V⁺+I)/n+pᵀKq−2G。

占用储备只支付第一侧；pᵀKq 是在原当前节点重新强制后继主题、再独立查询 p 的另一批真实根完成叶。后继在原历史的最优性不能免费跨这个 reset。更强全分布 quantitative derivative 不等式已失败，较弱条件蕴含 G>u ⇒ derivative>0 仍未证明。一般证明的下一项是真正支付此 reset，而非进一步重排上述恒等式。
