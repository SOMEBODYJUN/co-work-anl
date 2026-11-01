# 完整真实终局的势遗憾分解与两人最大裸回复列

2026-10-22；Boss10/tree。一般 Q-CAG-HALF 仍 OPEN。本文给任意剩余人数的精确身份及一个两剩余人的显式纯列结论；没有声称一般菜单已闭合。root 与 independent_audit 已从定义分别重构两人身份和列选择，未发现数学异议。没有外审或新颖性认证。

## 1. 任意 r 的精确身份

采用 CAG-MODEL。固定一个有序历史，背景客户负载为整数 b_x>=0，尚余 r>=1 人。主题字母 A,B 表示同一个共同有限非空目录中的合法主题，不限制重合、空主题、重复覆盖或历史平局。给定同一份完整纯 SPE，强制首位 A 后的真实 r-1 人后缀记 Y_A，完整 r 人终局为 Z(A)=(A,Y_A)。

定义固定背景调和势

    Phi_b(Z)=sum_x sum_(j=1)^(load_Z(x)) 1/(b_x+j).

对实数非负背景也可用同一有限和定义。设

    d_A = Phi_b(A,Y_A)-Phi_b(Y_A),
    F_A = Phi_b(Y_A),
    R_AB = Phi_b(A,Y_B)-Phi_b(A,Y_A),
    K_AB = sum_(x in A) 1/(b_x+1+load_(B,Y_B)(x)),
    delta_AB = sum_(x in A intersect B)
       1/[(b_x+1+load_(Y_B)(x))(b_x+2+load_(Y_B)(x))].

其中 d_A 是首位强制 A 的真实收益；K_AB 是额外第 r+1 位查询 A，对完整 r 人真实终局 (B,Y_B) 的静态插入收益。R_AB 是在固定首位 A 下，真实后继 Y_A 对固定组合 Y_B 的**联合势遗憾**；SPE 没有直接声称它非正。

**一般精确身份。** 对任意 r、任意 A,B，

    K_AB=d_A+F_A-F_B+R_AB-delta_AB.                    (1)

证明：前三项加 R 恰为 Phi_b(A,Y_B)-Phi_b(Y_B)，即 A 对 r-1 槽 Y_B 的插入收益。再加入源首位 B 后，只有 A intersect B 中的客户分母增加一，其差恰为 delta_AB。证毕。

这是真实分支的记账恒等式，不需要把 Y_A 当作共同最大化势的联盟。它没有单独给 R 的符号。

## 2. r=2 时的显式最大裸回复列

此时 Y_A 只有一个主题，记 rho(A)=R_A，且它是原策略在真实有序历史 A 后的末位最佳回复。定义

    f(X)=sum_(x in X) 1/(b_x+1),
    g_x=1/[(b_x+1)(b_x+2)],
    h_x=2/[(b_x+1)(b_x+2)(b_x+3)],
    U(X,Y)=f(X)-sum_(x in X intersect Y) g_x.

于是 F_A=f(R_A)，d_A=U(A,R_A)，且 R_AB=U(R_B,A)-U(R_A,A)<=0。一般身份的精确两人形式是

    d_A+f(R_A)-f(R_B)-K_AB
      = [U(R_A,A)-U(R_B,A)]
        +sum_(x in A intersect B) [g_x-h_x 1_(R_B)(x)].       (2)

方括号第一项来自真实末位在历史 A 下比较合法主题 R_B 的 BR 松弛。第二项恰为 delta_AB，并满足

    g_x-h_x 1_(R_B)(x) >=1/[(b_x+2)(b_x+3)]>0.

**显式纯列定理。** 取任意

    B* in argmax_B f(rho(B)).

共同有限目录保证最大值存在。则对每个合法查询 A，

    K_(A,B*) <= d_A
       -[f(rho(B*))-f(rho(A))]
       -sum_(x in A intersect B*) 1/[(b_x+2)(b_x+3)]
       <=d_A.                                               (3)

如果当前首位也遵循 SPE，当前收益 u=max_A d_A，因此同一个完整两人真实终局 (B*,rho(B*)) 同时满足所有 extra-query 的 K_(A,B*)<=u。不必混合列，也不必先选择查询分布。

证明就是把 B* 代入 (2)：裸回复值之差、BR 松弛及交集税均非负。只使用真实末位 BR，保留任意有序历史、任意平局；不要求策略对同计数历史匿名化。

## 3. 循环、标量势与一般人数的边界

把每条源 B 到查询 A 的边赋权 K_AB-d_A。由 (2)，

    K_AB-d_A <= f(rho(A))-f(rho(B))-delta_AB.            (4)

因此任何有向循环的边权和不超过相应负交集税。特别地，若画边 B→A iff K_AB>d_A，沿每条边标量 f(rho(.)) 严格增加，故图无有向环；最大裸回复列给出显式终点。阈值换成更大的实际首位 u，结论仍成立。

这一标量机制不能无证明地提升到 r>=3：R_AB 此时是多位真实后继的联合势遗憾，而非单个末位 BR。representation 分支的 `high_insertion_2cycle_348_exact.json` 已给三剩余人、348 单位客户、完整纯 SPE，在 K 的阈值 u=147/2 上有 2↔5 的精确二环，两边 K=159/2；全部强制根分支的完整势都等于304。该例不能否定一般混合菜单，因为列0与列3的最大查询仍只有69<u。它准确阻断“一般无环”及“一般每个高插入边必须提高某个共同标量势”的直接提升。

## 4. 真正未支付的混合联合势遗憾

对任意行分布 p、列分布 Q，记 e(p)=u-sum_A p_A d_A>=0。由 (1)，要用完整 r 槽菜单证明 p^T KQ<=u，精确剩余义务为

    E_(A~p,B~Q) R_AB
      <= e(p)+E delta_AB+E_Q F_B-E_p F_A.               (5)

一般菜单需要对每个 p 找到某个 Q 使 (5) 成立。r=2 取最大 F 的纯列即可。r>=3 不得丢弃 R，不得只把 F 取最大便宣称解决，也不能把 (5) 的等价重述当作存在 Q 的证明。

当 Q=p 时 F 漂移完全抵消，得到 C(p)-D(p)=E R_AB-E delta_AB；这正是 strong-push 与 root 激励松弛可以共享支付的联合债务。现有 r=3 strong-push 反例只否定未经 e(p) 支付的该式，不自动否定自由 Q 菜单。是否可由各真实后继节点的单独比较证明 (5)，仍开放。

## 5. 审计范围

`audit_reply_column_identity.py` 用 Fraction 按客户重构两人16种会员模式，并对任意 r 身份的负载变量作定义级检查；冻结输出为 `reply_column_identity_audit.json`。有限计算只核公式实现，全部参数结论由上文代数与末位 BR 证明。

与 `induction/two_player_full_terminal_pushforward.md` 的关系：该文给任意 p 的平均 strong-push；本文给另一种显式列选择、完整联合势遗憾身份及无环标量机制。两者都只在 r=2 的一般真实树接口闭合，没有解决主目标。
