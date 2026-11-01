# 完整菜单与 LAST：一般推导、来源核对和精确停点

2026-10-24。个人可接续备份。采用 CAG-MODEL 的有限单位客户、有限共同目录、
任意人数 m、全部有序历史纯 SPE 与任意平局。没有得到一般 half 证明、目标反例，
也没有新增能够支付 half 的全输入关系。下面的静态代数复用既有同对象资产，
不认领为新颖结果。

## 1. 真实菜单与四种不同量词

固定完整 SPE sigma，实际叶 z=(S_1,...,S_m)，u_i 为实际最终利润，W=sum_i u_i。
在实际前缀 h_i 强制当前 A，随后完整执行原 sigma，所得完整 m 槽叶记 Z_i(A)。
定义独立额外查询

    K_i(T,A)=sum_(x in T) 1/[1+c_x(Z_i(A))].

当前真实 IC 仅给 d_i(A)=u_i(Z_i(A))<=u_i。Z_i(A) 中过去固定，
后继可全部改变；没有冻结后继或合并相同计数的不同有序历史。

要证明 Mpath<=W/m，需要对每个查询分布 p 找到某个 i,A，使

    sum_T p_T K_i(T,A)<=W/m.

同一个 p 必须对全部列使用；一个列、一个查询或同 p 推送失败不够。
根空背景逐人 Mfull<=u_1、实际路径所有位置各自 Mfull_i<=u_i、
自由 Mpath<=W/m 与只用末位列的 LAST 是不同充分候选，不互相偷换。
已知产品闭包所迫的跨实例通用时机义务见
[PRODUCT-MENU-TIME](../../R-4243b113e6fc4c25a197dec299f08049/parent/product_menu_time_obligation.md)。

**任意背景的逐人 Mfull 已不能作为开放的一般命题。**
[pair_attack](../../R-cd789330fc7141299ac491bbb3ffa420/round5/menu/pair_attack.md)
给合法背景 b 后的完整子 SPE，其前三位 u<s<=v_(r+1)(b)。
完整 r 槽真实菜单是自由 r 槽背景的子集，故 Mfull>=v_(r+1)(b)>u。
该推论仅使用菜单包含关系和原文已证分离，不另声称重审原大构造。
它不否定根空背景 Mfull、根 SPE 实际前缀版本或聚合 Mpath；原前缀可能离轨。

## 2. 冻结实际末位背景后的准确静态结构

令 b_x=sum_(j<m)1_(x in S_j)。末位列由所有合法 A 给出

    K_b(T,A)=sum_(x in T) 1/[b_x+1+1_(x in A)],
    M_b=min_Q max_T E_Q K_b(T,A).

每列是合法 m 槽静态竞争背景，所以 M_b>=v_(m+1)(0)。已有静态覆盖预算
OPT_m<=2m v_(m+1)(0) 因而使全范围 LAST 候选

    M_b<=W/m                                                    (LAST?)

足以 half。它比自由 Mpath 强，尚无证明或反例。

令

    f_b(T)=sum_(x in T)1/(b_x+1),
    H_b(T,A)=sum_(x in T intersect A)1/[(b_x+1)(b_x+2)].

逐客户有 K_b(T,A)=f_b(T)-H_b(T,A)。H_b 是非负对称 PSD Gram 核，
有限 minimax 给

    M_b=max_p [f_b(p)-max_A H_b(p,A)].

最大化凹二次式 J_b(q)=f_b(q)-H_b(q,q)/2 的 q 给一个对称 meta Nash，
其 KKT 上界是 M_b<=f_b(q)-H_b(q,q)。这个上界一般不等于真正菜单值。
严格分离已由 [26 客户同对象例](../../R-ab2c6df20538474c948f5f24e59437ee/global_proof/quadratic_meta_nash_gap.md)
给出：M_b=19/2<135/14=meta 自应值。因此不能将 J 的导数直接当作 M_b 的导数。

末位真实 BR 还给 M_b<=max_T f_b(T)=u_m。但 u_m 可以大于 W/m；
这一静态关系不支付早期实际玩家的利润。

## 3. 已尝试的一般接入及其真正缺口

在固定 b 的 Gram 核中，行列交换和凹性都合法；早期位置 i 偏离 A 时，
末位之前的背景却会变为 b^(i,A)。因此不同真实分支不共用同一个 H_b。
把末位的对称税在每个早期枝各使用一次，会重复消费互斥分支信用。

对一般完整根菜单，已有精确身份

    K_i(T,A)=d_i(T)+F_i(T)-F_i(A)+R_i(T,A)-delta_i(T,A),

其中 R_i 是真实整组后继的联合调和势遗憾。单个末位 BR 能在最后两人
场合支付 R_i；多人后继没有已证的相同符号。最大势排序和高插入图无环
均有旧完整 SPE 反例，固定全槽 stationary 列也有旧完整 SPE 反例。
这些反例不否定自由混合菜单；也不能在旧模板上继续声称一般接入。
完整身份与两人显式列原文在
[full_terminal_reply_column_identity](../../R-d22a706a03c5499d941a6a97f94128a8/tree/full_terminal_reply_column_identity.md)。

本轮没有把 R_i 支付到同一个原路径 W，也没有证明
W>=m M_b、W>=m v_(m+1)(0) 或新的全历史动态 minimax 引理。
把这些未付式重写为债务、协方差或 LP 对偶，不会自动增加其证明状态。

## 4. 唯一有限诊断的范围

只攻击上述明确 LAST?：复用旧 6286 客户例的完整 43 节点形式策略，
固定 m=3、六个主题，将全部 63 个非空客户兴趣类型的非负重数作为变量，
保留全部 258 个真实 IC 比较，以实际 W=1 归一化。对 63 个非空支持的
均匀行分布 p，分别最大化 min_A p^T K_b(:,A)-W/m。

[程序](attack_last_cone.py)与[浮点冻结输出](last_fixed_cone_diagnostic.json)
保留这次实际运行。求解器没有提出正分离。输出的最优负间隔只是数值，
没有 Fraction 对偶证书，因此连该固定锥的精确非分离定理也未认证。
没有从这一阴性推断 LAST? 或 half；按父方要求停止旧锥阴性扩样。

## 5. 可接续任务

当前真实停点仍是：早期强制分支的客户价格如何由同一原路径利润共同支付。
若使用 LAST，应提供包含全部早期真实后继 IC 的 W>=m M_b 关系；
若使用更弱 Mpath，应保留对每个 p 共同选一列的准确量词。
允许改路线。没有新支付关系时，不把这一问号重复登记为进展。
