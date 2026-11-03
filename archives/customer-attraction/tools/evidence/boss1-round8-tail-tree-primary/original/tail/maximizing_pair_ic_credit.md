# 真实末二最大势分支：保留第四位 IC 信用的单次尾预算

2026-10-25；Boss14/tail。状态：下述局部表示及充分性有解析证明；最后的五人付款仍 **OPEN**。没有证明 HALF(5)，没有构造目标或 ONE-GAP 反例。没有外审或新颖性认证。

## 精确对象与范围

采用 `research/current/customer_attraction/model.md`。五名单位提供者、任意有限单位客户、有限非空共同目录及任意完整有序历史纯 SPE。空主题、重复行动、全零客户、全部离轨历史与任意历史平局均允许。本节局部结论更一般：任意合法有序前缀负载 q 后只剩两名玩家，实际主题 D,E；五人应用时 q 为真实前三名主题的负载。

定义

    f_q(T)=sum_(x in T) 1/(q_x+1),
    g_q(T,S)=sum_(x in T intersect S) 1/((q_x+1)(q_x+2)),
    P_q(T,S)=f_q(T)+f_q(S)-g_q(T,S),
    M=max_(T,S) P_q(T,S),
    Gamma=M-P_q(D,E),
    tau=sum_(x in D minus E) 1/((q_x+1)(q_x+2)).

M 是增量势最大值，不含共同的 Phi(q)。实际第四位、末位收益记 d,e。

## 1. 最大势比较可以落在原策略的一个真实分支

令

    Astar={T : exists S with P_q(T,S)=M}.

它非空。对 T in Astar，令 Q_T 是同一原 SPE 在精确有序历史 (h,T) 下的真实末位回复。因为最后一人的收益恰为其主题对势的边际增量，Q_T 最大化 P_q(T,Q)。而已有一个 S 使 P_q(T,S)=M，故

    P_q(T,Q_T)=M.                                     (1)

这里没有重新选择平局或用另一个续局替换 Q_T。于是 (T,Q_T) 是背景 q 的静态纯 Nash 对：如果任一成员可改选提高自己的收益，也会严格提高 P_q，违背全局最大性。

定义

    delta_T=f_q(T)-g_q(T,Q_T),
    epsilon_T=d-delta_T >=0.

非负性来自真实第四位偏离 T 的原 IC。若五人应用中 v=v_5(0)，则 q 是三项合法主题负载，故 q+Q_T 是四项合法静态竞争主题；T 对它是最佳回复，从而

    delta_T=max_A U(A; q,Q_T) >= v.                    (2)

这一步只用“任何一个合法静态竞争元组的纯最佳回复值至少为真正 minimax 安全值”，没有说某个纯查询保底为 v。

## 2. 精确保留信用后的尾预算

利用 P_q(D,E)=d+f_q(E) 与 (1) 的 M=delta_T+f_q(Q_T)，有

    Gamma+epsilon_T=f_q(Q_T)-f_q(E).                  (3)

实际末位 E 对合法主题 Q_T 的 IC 给

    f_q(Q_T)-f_q(E)
      <=g_q(D,Q_T)-g_q(D,E)
      <=g_q(D,D)-g_q(D,E)=tau.                       (4)

因此对每个 T in Astar，

    0 <= Gamma+epsilon_T <=tau <=d/2,                 (5)
    Gamma <=delta_T/2-epsilon_T/2 <=delta_T/2.         (6)

(6) 是将 d=delta_T+epsilon_T 代入 (5)，不是额外使用一份 IC 预算。tau≤d/2 仍是已有逐客户尾税界。这里的新增可接续表示是：先把比较第一主题限制到 Astar，便可令末位的原真实回复保持最大势，并准确保留一次第四位 IC slack。此表示是旧三 IC 机制的重组，不认领全新的局部机制。

定义同一真实节点的有限确定量

    delta_star=min_(T in Astar) delta_T,
    epsilon_star=d-delta_star,
    K=Gamma+epsilon_star
     =max_(T in Astar) f_q(Q_T)-f_q(E).

那么

    Gamma<=K<=tau<=d/2,
    max(v,d/2+Gamma)<=delta_star<=d,                  (7)
    Gamma<=delta_star/2-epsilon_star/2.

Astar 的定义只含目录和 q；Q_T 始终由原完整有序策略决定。K 只在一个实际末二节点收费一次，不向三个早期角色分别复制。

## 3. 严格弱于 ONE-GAP 的五人充分义务

令真实五人叶为 (A,B,C,D,E)，P=u1+u2+u3。由 (7)，下列候选比旧 ONE-GAP（P+Gamma>=3v）更弱：

    P+K >=3v.                                       (MAXPAIR-CREDIT? OPEN)

它仍足以推出 HALF(5)：最后两人各有 u4,u5>=v；若候选成立，则

    W=P+u4+u5 >=3v-K+u4+u5
      >=3v+u4/2+u5 >=9v/2 >=OPT_5/2.

最后一步引用已证 OPT_5<=9v。若 v=0 或客户全零，上式仍按不等式成立，不形成比值。

这不是无条件五人付款。特别地，Gamma=0 并不强制 epsilon_star=0：尾势已经达到全局最大时，原第四位仍可能对部分最大势分支有严格 IC 余量。故从 Gamma=0 的子情形攻击旧 ONE-GAP 时，K 仍有可能提供额外信用。

## 4. 局部信息没有支付的部分

(1)--(7) 仅在真实前三前缀固定后构造一个最大势偏离菜单。它们没有控制早期偏离改变的前三主题与末二菜单，也不声称 M_2 对前三负载次模，不把原前三策略变成包络势游戏的 SPE。MAXPAIR-CREDIT 的前三总付款仍需新的跨树关系。

原 ONE-GAP 可以失败而 MAXPAIR-CREDIT 仍成立；本文未证明存在这种完整五人实例。反过来，若找到 MAXPAIR-CREDIT 的反例，它也直接否定 ONE-GAP，因为 K>=Gamma。任何局部或数值反例都不能代替完整有序历史 SPE 核验。

## 依赖与有限诊断边界

解析依赖：精确模型、真实完整历史 IC、调和势的单人边际身份、末两人各有真正安全值下界、静态 OPT_5<=9v_5。后两项的现行正文分别为 `last_two_floor.md`、`oblivious_security.md`。局部尾税原接口和此次目标来自 round13 的 `two_tail_envelope_prefix_payment.md` 及 `two_tail_potential_review.md`。

另对两个明确 fresh 控制器做过浮点定向锥诊断，均未产生反例。没有精确对偶证书，不提升任何普遍命题；无新增数学信息的诊断未保留为共享资产。上述解析结论不依赖这些诊断。

## 5. K 严格大于 Gamma 的真正五人例子

取两个互不相交主题 A、B，分别含五名、一名单位客户。完整策略在全 A 历史上，前四人选 A，末人选 B；每个其余有序历史填入任意有限逆向归纳 SPE。此规则明确可补为完整策略：全 A 在轨历史的每个前四位遵从者最终得 5/4，而改 B 的最终收益至多 1；末位在 A^4 后选 B 得 1，改 A 也得 1。因此上述在轨规定与所有填入的离轨子博弈共同构成完整 SPE。

实际叶 A,A,A,A,B，收益 (5/4,5/4,5/4,5/4,1)。固定 q=3A，增量势

    P(A,A)=5/4+5/5=9/4,
    P(A,B)=5/4+1=9/4,
    P(B,B)=3/2.

所以 Gamma=0、Astar={A,B}。原末位在 q+A 后按规定选 B，在 q+B 后唯一最优选 A。故

    delta_A=5/4, delta_B=1,
    epsilon_star=1/4, K=1/4=tau.

真正 v5=1：纯查询 A 对任意四项竞争者得至少 5/5=1，而竞争元组 A^4 使两种查询均得 1。因而这个例子证明，额外 K 信用不是符号上永远为零的装饰，并且在 Gamma=0 时也可把整个精确尾税预算用满。它仍满足旧 ONE-GAP（前三收益 15/4>3）与 HALF(5)（W=OPT=6），不是任何候选反例。

`verify_selected_credit_example.py` 从单位块直接以 Fraction 计算完整树，重放全部 31 个有序决策历史、62 条含自身行动的 IC，并核对势、K、精确尾税及 v5 的匹配上下界。此有限审计只认证本例；一般局部关系来自前文解析证明。
