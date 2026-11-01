# 同一真末回复的多查询先合再投影

状态：既有 priced-hidden-reply 局部引理的合法多查询推论；本稿给解析行语义与实现，不声称新颖性或全局 half。计算点仍是指定必要图点，没有完整 SPE。

## 一般非负恒等式

固定同一原完整历史纯 SPE。某真实源 h 恰余 n+1>=2 人，背景负载 b，源规定收益 u。强制合法主题 T 后原策略真正后继为 F_1,...,F_n，最后主题为 G=F_n。固定实际全局末位收益 u_m、其前缀负载 ell，以及全目录共同最大主题大小 K。再固定任意有限个合法查询主题 Q_l，非负权 mu_l，令 M=sum_l mu_l。任取非负 alpha_j,beta_j。

对客户会员 t,f_j,g,q_l，z=b+t+sum_j f_j，定义

    h_x = t/z + sum_j [beta_j+alpha_j/(ell+1)] f_j
          - M g/z + [sum_l mu_l q_l]/[b+t+sum_(j<n)f_j+1].

零分子份额为零。则

    u+(sum alpha_j)u_m+(sum beta_j)K - sum_x h_x

恰为以下真实非负行之和：源对 T 的 IC；每个后继主题 F_j 的实际末价行乘 alpha_j；同一 K 的容量行乘 beta_j；**同一个**真实末位 G 对每个 Q_l 的 IC 乘 mu_l。

因此可在整份 mu 查询组合完成后对隐藏 f 统一取最小。不能先对各 Q_l 各自消去 G，再宣称保留了相同的隐藏回复。

本实现取前 n-1 个隐藏位相同价格/容量参数 (alpha_mid,beta_mid)，最后一位用 (alpha_last,beta_last)。固定其会员人数 s、末位会员 g 后，非线性项只依赖 s,g，故精确下界是

    psi = min_(0<=s<=n-1, g=0,1) {
       (t-Mg)/(b+t+s+g)
       + (alpha_mid*s+alpha_last*g)/(ell+1)
       + beta_mid*s+beta_last*g
       + (sum mu_l q_l)/(b+t+s+1) }.

首项仍按零分子约定处理。由此得到合法投影行

    u+[(n-1)alpha_mid+alpha_last]u_m
      +[(n-1)beta_mid+beta_last]K >= sum_x psi_x.

任意固定或离轨源、任意有限目录、空/重复/零客户及全部历史平局均保留。它不使用五人背景定理，也不识别不同有序历史的续局。

## 六人原1905列中的使用

源是实际第 k 位 (k=0,...,4)，独立于回复边 e 中的比较索引 i,j。强制 T 取新索引回复 R_e 或 Z_e。查询菜单按固定顺序取六个实际主题、(T_i,B_i,C_i,T_j,B_j,C_j)、T 自身，共13项。这些会员都已由 actual_bits、旧 group=(f,diag,wi,wj) 及新单会员位 t 保留。

psi 作为 t 的二值函数，在旧 joint-reply(r,z) 状态上线性：hist 放 t=0 的基系数；t=1 的 joint 列放 psi(1)-psi(0) 增量。每个 (f,diag) 轨道按30或6条真实查询平均，源利润和实际末价/K始终只按所得乘子支付一次。

terminal_portfolio_cuts.py 的参数 LP 对一个给定必要点寻找非负参数；最后取有理数并从上述 psi 重建整行。LP仅发现参数；所有返回行的合法性由恒等式承担。有限 LP 没有证明整个目录 SPE 可实现，也没有证明任意实例半覆盖。

特别地，n=1、alpha_last=mu_Q=1、其他参数0时，该投影恰等于已有实际强PAIR(T,Q)，不是一个新的局部福利机制。research_5/tail_r1_pair_identity.py 对此有独立核验。

## 第三索引菜单的保留

实现后续允许 mu 向量长16：前13项合同不变，末三项分别是在比较索引 k 不属于回复边 e=(i,j) 时，对合法主题 T_k、B_k、C_k 的均匀查询。i=j 时剩5个索引，否则剩4个。其客户会员分别为

    [sum_k word_k[q] - word_i[q] - 1_(i!=j)word_j[q]] / [5-1_(i!=j)],

q=0,1,2。它们是非负归一化的真实末位 IC 平均，不是新造目录动作；对应每个菜单项对 M 的贡献仍为 mu（菜单内部系数之和一）。完整 histogram 和两旧词已保留这些分数。

旧13项 cut 不含末三项，重放时系数严格不变。新的16项支持查询索引与回复边 i,j 不同的真实主题；原72 mixed-PAIR只含六actual及两边词的六查询，没有自动包含这个第三索引角色。
