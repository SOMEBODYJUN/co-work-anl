# 任意人数的末对冻结税钱包：已付部分与早期未付项

2026-10-24，matching8。对象始终为任意有限共同目录、任意人数和每份完整历史纯 SPE。**Q-CAG-HALF 仍 OPEN；弱静态最优指派预算也未证明。** 本页给一个真正由原 IC 支付的末对局部项，不能把它称为一般 HALF 或全位置共同容量。

## 1. 先纠正静态桥的状态

对实际叶 Z，令

    f_i(T)=u_i(T,Z_-i),
    Q(T_1,...,T_m;pi)=sum_i f_i(T_pi(i)).

原强桥“存在 OPT 元组及排列使 Q<=W”已经为假，不再是开放候选：

- [旧52单位客户证书](../../../R-a0bb57fa24044a8794bc7991918a19c6/static_matching/optimal_static_matching_counterexample.md)有 m=4、W=47、OPT=52、唯一最优支持 0145、全部24排列最小 Q=48；其[旧独立审查](../../../R-a0bb57fa24044a8794bc7991918a19c6/direct_global/static_matching_counterexample_independent_review.md)逐客户通过。
- [另一1953单位客户证书](../../../R-105f776c3e6d4a22bb7c380c5df8edc7/dynamic_exchange/static_optimal_assignment_counterexample.md)有 m=3、W=1735、OPT=1740、唯一最优支持125、全部6排列最小 Q=1736。

这些都不是主目标反例；本页不将它们计作新发现。既有弱桥为

    存在一个最优元组和排列，使 Q<=(1+1/m)W。       (WEAK-Q?)

逐客户静态式无条件给 OPT<=Q+(1-1/m)W，所以 WEAK-Q? 足以推出 HALF。允许重复比较槽和换最优组合的量词不删去。本页未证明 WEAK-Q?。

## 2. 同一实际末对与三个真实 IC

固定 m>=2 的原 SPE。置 p=m-1、A=S_p、B=S_m，b_x 是实际前 m-2 个主题的负载。定义

    U_b(X,Y)=sum_(x in X) 1/(b_x+1+1_(x in Y)),
    F_b(X)=sum_(x in X) 1/(b_x+1),
    gamma_b(X,Y)=sum_(x in X intersect Y) 1/[(b_x+1)(b_x+2)].

于是 U_b(X,Y)=F_b(X)-gamma_b(X,Y)，gamma 对称。记 a=U_b(A,B)=u_p，v=U_b(B,A)=u_m。

对任意合法主题 T，R=R(T) 必须取原 sigma 在**同一完整有序前缀** (S_1,...,S_(m-2),T) 后的真实末位动作。记

    D_T=U_b(T,R),                e_T=a-D_T>=0,
    delta_T^off=U_b(R,T)-U_b(B,T)>=0,
    delta_T^act=U_b(B,A)-U_b(R,A)>=0,
    ell_T=delta_T^off+delta_T^act>=0.

第一条是原倒二节点的完整行动 IC；后两条是 T 后末节点与 A 后末节点的真实 BR，比较动作 B、R 都来自同一个共同目录。此处没有固定真实后继，只有 f_p(T)=U_b(T,B) 这个明确的静态被估量冻结了 B。

gamma 对称直接给一个精确的交叉恒等式：

    D_T+a-U_b(T,B)-U_b(A,R)=ell_T>=0。             (CROSS)

这也就是末位两个 BR 行相加后的两列单调关系。

## 3. 可支付的 actual(A\B) 钱包

置

    L_A=sum_(x in A) 1/(b_x+2),
    C_p=a-L_A
       =sum_(x in A\B) 1/[(b_x+1)(b_x+2)]>=0,
    g_T=U_b(A,R(T))-L_A>=0。

把这些定义代入 CROSS，得到

    f_p(T)=a+C_p-e_T-g_T-ell_T
           <=a+C_p。                              (TAIL-WALLET)

这不是一个未知余量的对偶重述：三个可见信用 e_T、g_T、ell_T 非负，C_p 由**同一实际叶**的 actual(A\B) 利润支付。具体逐客户有

    C_p<=a/2。

实际末位还可以合法改选 A，所以 v>=U_b(A,A)=L_A>=a/2。因此同时有

    C_p<=min(a/2,v),             3C_p<=a+v。       (PAID)

例如最后两位实际主题相同时 A=B，C_p=0；这时倒二静态查询对全部合法 T 都已经由自己的 a 支付，尽管更早位置未必静态最优。

TAIL-WALLET 对每个合法 T 同时成立。所以对任何非负权重 q_T、sum_T q_T=1，也有

    sum_T q_T f_p(T)
      =a+C_p-sum_T q_T(e_T+g_T+ell_T)
      <=a+C_p。

这是一个完整倒二利润行加一份 C_p，不是每个 T 各收一次 C_p。任意配对分布的 p 行边际也可直接使用它；不要求 q 是均匀，不要求 T 来自最优组合。末位原节点比较另给 f_m(T)<=v。

在有背景时 a+v 是这两个未来玩家的利润之和，不是该子局新覆盖数。本页只在根的实际叶使用 a+v<=W。

### 用实际末行进一步扣除利润失衡

同一个静态背景上另有

    f_p(T)-f_m(T)
      =gamma_b(T,A)-gamma_b(T,B)<=C_p。

实际末节点 IC 给 f_m(T)<=v，所以对每个 T 同时有

    f_p(T)<=min(a,v)+C_p。

结合 TAIL-WALLET 的精确式，得到一个非平凡的信用下界

    G_T:=e_T+g_T+ell_T >= (a-v)_+。                (ROW-ANCHOR)

因此任意分给末两行的两个主题，其静态成本之和至多

    a+v+C'_p,
    C'_p=C_p-(a-v)_+=min(a,v)-L_A>=0。            (REDUCED-WALLET)

这个较小的钱包还满足 C'_p<=min(a,v)/2：v>=a 时直接用 L_A>=a/2；v<=a 时用 v-L_A<=v-a/2<=v/2。它扣除的是高倒二利润相对末位利润的失衡，不需要为两个比较主题另付第二个 C_p。这里没有另立固定人数常数优化。

## 4. 真正接入弱指派预算的位置

任取一个最优元组和一个排列，并重标为 T_i 分给角色 i。令

    Y^i=finish_sigma(Z_<i,T_i),
    D_i=u_i(Y^i),    e_i=u_i-D_i>=0,
    E_i=f_i(T_i)-D_i。

所有 e_i 是同一 actual-prefix 原 IC 的真实松弛。对 i=m，真实偏离没有后继，故 E_m=0。对 p=m-1，TAIL-WALLET 精确给

    E_p=C_p-g_(T_p)-ell_(T_p)。

因此整份静态指派满足精确的已付/未付分解

    Q-W
      = C_p + sum_(i<=m-2) E_i
        -sum_i e_i-g_(T_p)-ell_(T_p)。             (ASSIGN-TAIL)

进一步置 h_T=G_T-(a-v)_+>=0，ROW-ANCHOR 给同一账的较紧形式

    Q-W
      = C'_p+sum_(i<=m-2)(E_i-e_i)-e_m-h_(T_p)。 (ASSIGN-REDUCED)

于是一个足够的**剩余**全输入目标为：能共同选择最优元组与排列，使

    sum_(i<=m-2)(E_i-e_i)
      <= W/m-C'_p+e_m+h_(T_p)。                  (EARLY-REMAINDER?)

本页只支付了终端一个正冻结税钱包，并扣除了 ROW-ANCHOR 的必有信用；没有证明 EARLY-REMAINDER?。C'_p<=min(u_p,u_m)/2 不给任意 m 的 C'_p<=W/m，更不给早期 E_i 的共同界。

不能把这份 C_p 再无条件加到 coordinate initialization 的 d/H 银行。那是另一份支付账；要合并，需先证明同一 actual 行上的未重用余额。

## 5. 来源、核验和不能作的归纳

双线性分解和相同背景的两人税机制沿用[旧两人税正文](../../../../../current/customer_attraction/two_remaining_tax.md)；跨真实末节点的组合比较另见[旧平均跨分支接口](../../../../../current/customer_attraction/global_new_uniform_portfolio_two.md)。本页没有重新声称这些代数或两人福利界的新颖性；此处保存的是它们对**一个实际末对的点态静态冻结 regret**的选择性钱包及 ASSIGN-TAIL 接口。root 从所给公式独立重构 CROSS 与 C_p 付款后确认，尚无外审。

[定义级审计](audit_terminal_wallet.py)只读取上述两份已有完整证书，重算全部真实 IC，并对它们每个合法 T 核 CROSS、三个非负信用、钱包恒等式、PAID 及 ROW-ANCHOR。它不生成游戏或扫描策略，不修改原证书。有限实现检查不承担普遍性，普遍性由以上三行原 IC 与 gamma 对称推导。

不能将该机制原样用于较早相邻角色：后面若还有玩家，后继对前两个行动的真实响应改变，收益不再是同一固定背景的 U_b(X,Y)。本页没有让他们合成一个联合 BR，也没有把不同离轨历史的 C_p 汇入同一 actual 钱包。继续推进需要真正控制 EARLY-REMAINDER?，或构造一种保留共同 actual 行预算的全树耦合。
