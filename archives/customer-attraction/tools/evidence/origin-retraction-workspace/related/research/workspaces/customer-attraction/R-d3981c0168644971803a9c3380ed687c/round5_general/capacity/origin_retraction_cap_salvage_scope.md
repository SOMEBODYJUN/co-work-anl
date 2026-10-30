# 来源回撤与前缀 cap 回收：接口检查及真实停止点

2026-10-24，round5_general/capacity。只研究一般 CAG-MODEL：任意人数、任意有限共同目录、每个全部有序历史纯 SPE；空主题、重复选择及任意历史平局均保留。**Q-CAG-HALF 仍 OPEN。本轮没有新的 full-history joint-cut 不等式或福利常数。** 本页是一次接口核查，不把工具复述、失败推导或新命名计为一般数学推进。

## 1. 实际读取及复用范围

实际读取的是正确作者 R-3bc48d936f044f12b0fa743482ff5eb0 的 [来源回撤](../../../R-3bc48d936f044f12b0fa743482ff5eb0/flow/origin_retraction_shared_capacity.md)、README、[应用审查](../../../R-3bc48d936f044f12b0fa743482ff5eb0/optimal_gap/origin_retraction_application_audit.md)，以及本 actor round4 的 [共享前缀 cap 回收](../../round4_general/menu/shared_prefix_cap_salvage.md)。起初提供的 R-5a157... 路径不存在，root 随后更正作者；未把旧 AMOUNT 材料误认为 RETRACT。

RETRACT 的受控对象是一份已固定的 INIT/I-PAY/R-FLOW，保持原完整 sigma、实际 B、比较 T、I 券 J 和每个 source 的完整实际路由。比例回撤把 R 初始 future 及全部同源后代统一缩小，原 owner current 增加同样金额。它确实允许最后的 d'_i>u_i，只要验证**同一次最终共同 cap** F'_i<=2u_i。这里不需要把旧单次初始化 IC 再领一次，也没有新增每客户 IC。正文明确更改了证书类，未假称保持原 INIT 多面体。

三角贪心及 first-failure CUT 对这个固定比例回撤族给充分必要判定，来源和限域都清楚。它不重选完成叶、不同 action 或源主题；因此在没有额外 SPE 数值关系之前，它本身不控制不同 action 的共同钱包。常价格仍给 |O|<=2W，即原目标，不是可直接调用的资金。

## 2. 为什么 cap-salvage 不能盲接为新来源入口

固定原 sigma 的 actual-prefix 查询 Z_k(A) 本来就满足当前完整 IC，所以它已经属于 D_kA。对**这些原叶**调用 cap-salvage 不增加任何可用完成。

若改取另一份完整尾 SPE 的端点 y in R(h_k,A)，且当前强制者 v_k(y)>u_k，cap-salvage 可能靠更早的最后便宜角色 j<k，把同一个有序 y 送进 D_j,S_j。这一步有实质的菜单用途，但其 cap 现在控制的是

    v_j(y)<=u_j，当前强制行动为实际 S_j。

对 R=O\C 的客户，S_j subseteq C，所以 S_j cap R 为空。原 source action A 在 y 的第 k 位出现，并在新 j 表示中成为尾部的规定行动；它不是第 j 位所强制的行动。故不能把 y in D_j,S_j 当作“第 k 位强制 A 的利润已被 u_k 支付”，也不能将第 j 位的 R 初始密度/正 future 边直接继承为原 owner k 的入口。

这个结论只是比较两个已给合同的控制行：菜单 cap 控制 j，source 初始化所需的 complete query 行控制 k。它没有证明其它初始化或全局分配不可能；特别是 RETRACT 的终端共同 cap 若另行验证，当然可以支付来源标签与实际行动不相交的 current。缺的是验证这份**共同余额**，不是标签必须同客户。

合法的组合方式有两个，但本轮均未补足其数学前提：

1. 仍走 source flow：为新完成 y 重建其初始化，并取得原 owner k 的 whole-IC cap，或一份明确共同的前缀资金分配；再重算全部同源路由和回撤。仅知道某个更早角色便宜不提供这份总资金。
2. 转入 ADM：cap-salvage 保持同一个有序 y，因此所有插入查询值原样保持；若能另从 joint cut 生产 G_p(y)<=W/m 的真实尾 SPE 端点，它立即给合格菜单列。RETRACT/CUT 目前输出金额和价格，不输出这种低 G 的端点。

## 3. 实际尝试的另一条完整历史比较

在 overloaded role l 的每个真实 incoming context g，曾尝试把规定行动与该角色自己的比较主题 T_l 相比，而不是只返回 actual B_l。此比较确实是原完整 SPE 的合法整行 IC，且 T_l subseteq O，有希望把跨 action 债务接回原最优库存。

但它的真实孩子是 finish_sigma(g,T_l)，保留旧首偏离并增加较晚强制动作；它不是 RETRACT 中原 actual-prefix T_l 的固定 source 路由。把两者等同需要重新证明真实尾部及全部过去利润 claim 的资金关系。已有 joint-prefix pushback 只修复单个 child 的过去 claim 域，不免费叠加互斥 child 的 actual 钱包。本轮没有取得能让该新孩子在同一 CUT 中合法相消的共同系数，因此没有保存另一条 signed 恒等式或声称新 kernel。

## 4. all-m 与 m=5 的准确压力结果

来源回撤给每个失败实例一条精确价格分离，first-failure 价格在[0,1]；这缩小了**固定回撤失败的证据对象**，没有使其对完整 SPE 自动非负。需要的新步骤仍是：用原全部有序历史的真实 IC，或共同重选 T/初始化/路由，证明该 cut 不会为负。

同一一般推导代 m=5：第1个角色无 incoming R，第一 cap 可保；其余四条 cap 仍未自动成立。cap-salvage 仍能回收一个已有低 G 端点的成员资格，但不生产低 G，也不控制回撤 cut。因此本轮没有推出 OPT_5<=2W，没有新无条件一般界；这不是目标反例或方法不可能性结论。

本分支没有运行固定人数或固定锥扫描，没有重证 NEW-CAP、逐客户密度、同 action uniform-reset，也没有更改共享稿、Git 或 work.py。下一次继续必须带一条真正支付 joint cut 的新完整 IC 组合，或直接换一般证明方法。
