# 独立重构 mixed 的 owner-absent I 联合信用核

2026-10-23。审查对象是 mixed 当轮给出的精确陈述，先由消息重构；不是未读陈述的盲审。作者正文待其本人给出，本页不替代完整费用证明。以下源归一、角色信用和 fixed-state 排序界通过解析核对。

固定 x in I 且其 owner o 在原实际叶不覆盖 x。令 J 为实际 coverers，c=|J|>=1，所以 o notin J。使用 relay 同一组独立 Uniform 角色优先级 U，所有客户逐world初始各一单位。

若 max_(j in J)U_j>U_o，则把这一单位记作 J 内优先级最高者的 credit；否则启动 x 的 owner-threshold 查询 token。对每个 j in J，credit事件恰为 j 在 {o} union J 中最高，故

    E credit_j(x)=1/(c+1)=原实际 e_j^Q(x)。

owner 在同一组中最高时才启动查询，所以查询总吸收概率是1/(c+1)，恰为此客户原实际 modified 边际总和 kappa_x。逐world仍是完整一单位在 credit 或查询两者中择一，没有额外创造信用。

对固定非owner查询状态 s=(i,a)，若 i in J，则初始 all-J-below-owner 条件与当前激活 U_i>U_o 矛盾，其吸收概率为0。其余情况下，该状态吸收事件必包含于

    U_i>U_o>max_(j in J union F_s(x))U_j。

令 L=|J union F_s(x)|。owner、i 与此并集互异，排序事件概率为1/[(L+1)(L+2)]。查询状态的真实客户分母为

    c_true=1+|J intersect {1,...,i-1}|+|F_s(x)|。

过去实际 coverers 与未来 F 不交，均包含于 J union F，故 L>=c_true-1。因此吸收概率至多1/[c_true(c_true+1)]，恰为该叶 owner-absent modified 边际。owner状态的吸收概率精确1/(|J union F_s|+1)，至多1/c_true。

这里初始 J 全低于 owner 已经暴露未来 J 的优先级，**不能**套用 relay 最早激活稿的 entry/未来独立等式；事件包含与无条件随机排序直接足够。界也不要求不同客户独立。

本审查只覆盖 owner实际未覆盖的 I 客户。owner实际覆盖时，owner本身属于 J，不能照抄此触发规则或声称相同 kappa 分配。适应取消后仍不可将未取消的上界乘平均残源；多客户在同角色不同 query 的合并费用未付。没有从本核推出 half。

## 两种不同的取消合同

relay 的固定实际 Gamma_A 适应取消仅作用于逐world总存在的 R token，所以每world取消总量恒G。mixed 的固定 Gamma_B 若还含 I^- 的 kappa 终点，且用 lambda/kappa 降低其仅以kappa概率启动的query，则lambda须在U前固定；lambda依U时不能再把期望取消称作E lambda。两者不能把同一G源相加消费。

mixed 后来给出合法的另一种**随机winner coupon**合同，已由 relay 从精确定义独立重构全割如下。每个 actual G 客户的整单位 source 记给其最高U实际coverer。对每个owner实际未覆盖的O客户：若最高实际coverer高于owner，放owner到该coverer的容量1边；否则放owner到该客户query sink的容量1边。R的sink总存在，I^-的sink恰在其query实际启动的世界存在。

任意role集合L，随机G source(L)至多为G中被L覆盖的客户数。HYB将后者界为missing-owner集合 M(L)的大小。每个M(L)客户的owner在L、实际coverers全在L外，故它的coupon要么是一条出L角色边，要么是query sink，均贡献1。全部cut足够，逐world可运满G；整数容量还允许取整数流。

期望source恰是原g_i；角色coupon边期望恰为actual e份额1/(c+1)，query sink期望为R的1或I^-的kappa。这次取消的是逐world真正存在的query token，因此不犯前一lambda/kappa的相关性问题；积分后的whole-IC系数仍可取常数。

**SOURCE-NET不因此自动继承。** 此合同的source数和初始query吸收都依U，不能把期望g_i直接当逐world购买IC的预算。它与固定Gamma_A取消是可选的不同证书。上述核对未证明joint初始化费用或总row collision已付。
