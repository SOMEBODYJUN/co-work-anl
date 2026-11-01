# 任意固定 owner 的调和路径信用：独立审查

2026-10-24。审查对象是 random_portfolio 分支交来的全范围陈述：同一个比较元组、同一个任意固定 owner 分割下，强制比较前缀查询的逐客户误差总量仍≤H_a−1。收到陈述时亦收到作者按 owner 前后划分的证明；本审查随后从旧 UNIT/INSERT 自行重构，因此**不是盲审**。

**结论：通过。** first-owner 的确不是该调和界的必要条件。这是既有一般插入势公式的直接推论，对旧文明确写出的 first-owner 假设作一项有效但有限的量词放松；它没有构造新的跨树支付，也没有推进 Q-CAG-HALF 的最终未付预算。

## 1. 精确输入及被核查的陈述

有限客户、共同有限非空目录、任意 m≥1。固定合法比较元组 T=(T₁,…,Tₘ)，并集 O；对每个 x∈O，固定一个覆盖它的比较槽 o(x)。owner 一经确定，在全部 profile 和全部查询中保持不变。

定义 owner 势

\[
 F_Q(B)=|O|+\sum_{x\notin O}H_{c_x(B)}
 -\sum_{\substack{x\in O\colon x\notin B_{o(x)}}}\frac1{1+c_x(B)},
\]

及查询第 i 槽误差

\[
 e_i(B)=u_i(B)-[F_Q(B)-F_Q(B^{-i})].
\]

对于 x∈Bᵢ∩O，旧 UNIT 逐客户公式等价于

\[
 e_i(B;x)=
 \begin{cases}
 0,&i=o(x),\\
 \dfrac1{1+k_x(B)},&i\ne o(x),
 \end{cases}
 \qquad
 k_x(B)=|\{j\ne o(x):x\in B_j\}|.
\tag{INS}
\]

令 Yᵢ 为任意 m 槽合法 profile，其前 i 槽**恰为** (T₁,…,Tᵢ)。不同 i 可以有不同尾部；也可取同一份完整历史策略 σ 在这些有序前缀后的真实完成叶。令 aₓ=|{i:x∈Tᵢ}|。待核查结论为

\[
 \boxed{\sum_{i:x\in T_i}e_i(Y_i;x)\le H_{a_x}-1.}\tag{AH}
\]

结论不需要 T 最优、不需要 SPE。若还调用 0≤F_Q≤|O| 等最优交换结论，则另外需要 T 是最优比较元组；不要把 (AH) 的较广范围传给该上界。

## 2. 独立重构：按非owner查询排序

对固定 x，将包含 x 的 aₓ−1 个**非owner比较槽**按时序写为 i₁<⋯<i_(aₓ−1)。Y_(iₛ) 的强制比较前缀包含 T_(i₁),…,T_(iₛ)，所以至少有 s 个非owner槽覆盖 x，即

\[
 k_x(Y_{i_s})\ge s.
\]

由 (INS)，

\[
 e_{i_s}(Y_{i_s};x)\le\frac1{s+1}.
\]

owner 自己的查询误差为零，故

\[
 \sum_{i:x\in T_i}e_i(Y_i;x)
 \le\sum_{s=1}^{a_x-1}\frac1{s+1}=H_{a_x}-1.
\]

该证明不关心 owner 查询位于第几次覆盖 x 的比较槽，也不假定未来 owner 会不会在某个真实叶覆盖 x。作者按 owner 前后的两个分母下界亦正确，但非owner排序统一了两种情况。

## 3. 退化、范围与真正松绑之处

- aₓ=1 时没有非owner查询，左边精确为零。
- 空主题不含任何 x；重复主题只增加合法槽计数，不破坏排序。
- 零客户时没有需要相加的逐客户项。
- 任意有序历史、任意真实后继及平局都允许；事实上本证明只需要强制的比较前缀。
- **不能把强制比较前缀改成原实际前缀。** 原实际前缀不保证先前非owner比较槽覆盖 x；旧 DIRECT-REPEAT 的 (aₓ−1)/2 界是另一个对象。
- **不能逐查询另选 owner。** (INS) 和整个 F_Q 的共同势身份都要求同一个固定 owner。

旧 first-owner 版本把 owner 强制等于第一个比较覆盖槽。这里允许固定任意 owner 后仍保留同一个 H_a−1 界，因此可把 owner 留给其它同时依赖它的静态/流量约束，而不必为了本界重选 owner。然而本审查没有证明这些额外约束可同时满足，也没有支付任何 incoming/reset 债务。

## 4. 与既有正文的准确关系

核对以下旧资产：

1. `R-cd789330fc7141299ac491bbb3ffa420/round3/shared/owner_exchange_potential.md` §5：明确选 first-owner 后证明 H_a−1。
2. 同 actor 的 `round3/relay/optimal_exchange_potential_and_query_credit.md` §3：OWNER-REPEAT 仍明确 first-owner；原实际前缀另给 DIRECT-REPEAT。
3. 同 actor 的 `round3/parent/audit_beta_slot_potential.py`：owner前缀回归固定 `owner_slots={min(a)}`，未核查任意owner。
4. 同 actor 的 `round3/global/full_depth_substitution.md` §5，式(7)及后文：已明确写出任意固定 owner 的 (INS)，即非owner误差恰等于 1/(1+k)。因此 (AH) 是旧一般公式加前缀计数的立即推论，不能包装成新动态机制。

本次针对这些相邻资产及全工作区 H_a/owner 关键词作了定向去重，未看到旧文**显式陈述**任意owner版本；这不构成穷尽全部历史或全球新颖性的认证。

建议身份：**“旧 owner 插入式的任意固定owner前缀信用推论；解除first-owner限制，独立重构通过；不改变half开放状态”。** 无须增加特殊人数计算来支撑该解析结论。
