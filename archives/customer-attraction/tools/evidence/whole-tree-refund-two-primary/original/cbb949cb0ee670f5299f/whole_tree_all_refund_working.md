# 全历史树与全部旧玩家退款：第十轮推导记录

2026-10-24，tree10。对象始终是任意人数、任意有限共同目录、任意完整有序历史纯 SPE，允许全部平局、空主题及零客户。**Q-CAG-HALF 仍 OPEN。** 本页保存未完成的直接推导，不将旧合同、恒等式或更强未证接口重新命名为付款进展。

## 1. 已有合同及本轮不重复的工作

[round8 兄弟曲率](../../round8/tree/sibling_hessian_and_reset.md)保留真实兄弟 IC 与 signed 尾重置；[round8 被动查询税](../../round8/tree/passive_query_tree_tax.md)只共同支付同一叶上的税；[round3 全后继势展开](../../round3/global/full_depth_substitution.md)保留删除当前角色后的真实换枝差。删除所得 profile 没有被证明为更少人数 SPE。

[round3 signed税与绝对surplus](../../round3/tail/signed_tax_surplus_working.md) §3 已包含全部旧背景退款 `DeltaB`。本轮恢复后确认它不是遗漏工具。客户密度、同动作压缩、单context整行 IC、上述去槽势式或单叶退款都不另算本轮正向进展。

## 2. 直接尝试：全部活跃利润替代删除势

固定合法旧前缀，旧背景为非负整数 b，余 r 人。任意合法活跃尾元组 Y 的负载记 c_x，定义

    U_b(Y)=sum_x c_x/(b_x+c_x),

零分子项取零。它是活跃玩家真实总利润，b=0 时等于覆盖。先固定当前主题 A，后接 r-1 槽 Y，置 a_x=1[x in A]、p=b+a，则精确有

    U_b(A,Y)=d_A(Y)+U_p(Y),
    d_A(Y)=sum_(x in A)1/(p_x+c_x).

令 H={x:b_x>0}、旧玩家最后总利润 `B_b=sum_(x in H)b_x/(b_x+a_x+c_x)`，另有

    U_b(A,Y)=|(A union unionY)\H|+|H|-B_b.

其中 `|H|-B_b` 已在活跃利润内，是全部旧玩家交出的利润；不能再当新覆盖加一次。使用 `F_r(b)=max_Y U_b(Y)` 曲线尝试归纳时，子局利润的两倍上界并不直接支付插入实际 A、删除一个比较槽后的最优差；根真实 IC 使用的是各自完整真实续局。

## 3. 插入实际根、随机删除比较槽的精确静态差

固定任意合法 r 元组 T=(T_1,...,T_r)，不要求最优，比较负载为 d_x。对同一个 p=b+a，逐客户计数给

    U_b(T)-(1/r)sum_j U_p(T_(-j))
       =sum_x L_r(b_x,a_x,d_x).

d=0 时 L=0；d>=1 时：

    a=0: L=(d/r)[d/(b+d)-(d-1)/(b+d-1)],
    a=1: L=d(b+r+1)/[r(b+d)(b+d+1)].

第一式中 b=0,d=1 的零分子项取零，故该格 L=1/r；其余 a=0 格可以写成 `bd/[r(b+d)(b+d-1)]`。证明：r 个被删槽中有 d 个覆盖该客户，其尾负载减一，另外 r-d 个保持负载 d。无 SPE、历史压缩或客户重权 IC。

特别在 b=0：a=0,d=1 时 L=1/r；a=0,d>=2 时 L=0；a=1,d>=1 时 L=(r+1)/[r(d+1)]。这是静态最优曲线归纳的准确缺项，**不是一项已经由根真实利润支付的差**。本轮没有证明这种支付，不把它另立新猜想或主线结果。

## 4. 全部旧背景保留时的共同缩尾账

固定同一个完整叶 (A,Y)，尾数 n=r-1，把所有尾玩家的质量统一改为 lambda∈(0,1]，b 与 A 均保留。记原根和尾利润 d、V，根退款 Gamma，全部旧背景退款 DeltaB。逐客户直接有

    Gamma=sum_(x in A) (1-lambda)c_x/
                         [(p_x+c_x)(p_x+lambda*c_x)],
    DeltaB=sum_(x:b_x>0) b_x(1-lambda)c_x/
                         [(p_x+c_x)(p_x+lambda*c_x)],
    V_lambda=V-Gamma-DeltaB.

令 eta=V-n*t，就有旧合同的精确式

    V_lambda-lambda*n*t-Gamma
       =eta+n(1-lambda)t-2Gamma-DeltaB.

一次根比较恢复要 Gamma，尾部原 IC 的同叶总税是 Gamma+DeltaB，因此不能省略旧玩家退款，也不能免费复用 Gamma。上述代数与 round3 一致，不认领新增一般关系。

在真实强制 rollout 上，每次改枝的 c、Gamma、DeltaB、eta 都属于那一步自己的真实完整叶。一叶守恒可以逐次合法应用，却不能使不同叶各自取出的税只用一次 actual 旧利润支付。本轮没有找到保持原有序历史与全部真实后继的共同耦合。

## 5. 一般机制的五人压力结果及停止处

同一静态式代 r=5,b=0：比较客户只覆盖一次且在实际根外时，平均删槽差为1/5；在实际根内、比较负载 d>=1 时为 `6/[5(d+1)]`。无条件 `OPT_5<=2W` 未由这些式子得到。正深度背景的缩尾账仍含 DeltaB，不能由空背景结论删掉。

本次没有新增跨叶付款、distinct-action总容量、ROLE可行性或福利界；新增写出的静态删槽差未接到一般付款，**不计主线正向进展**。没有运行固定规模扫描、制造辅助障碍或扩展特殊类。随后转入本轮成熟结果的独立攻击；[exchange10 静态末对 refinement](exchange_terminal_refinement_review.md)的核查另存。
