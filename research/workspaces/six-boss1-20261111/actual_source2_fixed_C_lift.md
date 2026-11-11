# 固定最大 C 的第二源同客户联合延拓：734 行未绑定合同

Boss1；RUN six-boss1-20261111。状态：**SYMBOLIC_UNBOUND_FIXED_C**。优化器调用为 **0**。

结论：旧 751 个 genuine kernel 都在任意固定合法外标签时有效，因此可以用于固定 C 的真实历史
\[
(A_1,C,R_3,R_4,R_5,R_6).
\]
失效的是旧模板额外附带的两条外查询矩，而不是 751 行中的某个真实预算。完整迁移视图保留 751 行；17 条纯可见行准确路由到全局前端，局部保留 **734 条隐藏约束**。

## 合同与适用域

完整客户类型是 \((a_1,\ldots,a_6,x,o,c)\in\{0,1\}^9\)，每型保留 16 个四尾态，共 8192 个符号状态。每个完整类型使用同一客户律
\[
\sum_r\nu_{h,r}=w_h.
\]
未来若另行释放的候选有 s 个正类型，物理系统为 **16s 列、s 条质量等式、734 条隐藏不等式、0 条外查询矩**。模板本身仍保留完整 512×16 域。

原 751 行的分工为：

| 块 | 条数 | 处理 |
|---|---:|---|
| 原隐藏预算 | 734 | 保持顺序和全部零/重复行 |
| 9 个 actual RC(C,T) | 9 | 全局 RC_C_C、RC_C_A1…A6、RC_C_X、RC_C_Omean |
| actual FMAX(C)、MX(C) | 2 | 全局 FMAX_C、MX_C |
| actual SAFE_i(C)，i=1,3,4,5,6 | 5 | 相同 actual 源的全局 SAFE_i_C |
| CAP(C) | 1 | \(|C|-K=0\) 的 −1 倍 |

16 条全局不等式是显式前置，没有声称它们由 734 行推出。未来释放必须逐公式确认这些前置和 C 等式。C 的裸大小最大性不授予势值最大性；X 的势最大化始终只属于原 actual 四行动前缀。

## 外查询矩为何必须删除

旧外变量是六个 Qk 强制历史的平均，才满足会员矩区间 \([o/6,o]\)。固定 C 的会员 c 没有这个限制。

本包构造的七单点共同目录具有完整纯 SPE、K=1 和一个大小为 6 的最优六标签并。Q1 客户满足 c=0,o=1，旧下界松弛为 −1/6；C 独有客户满足 c=1,o=0，旧上界松弛为 −1。两侧在同一个合法实例里均失败。

内部 P25 的真实菜单均值和 C30 自身的六查询矩消元保持有效。C30 仍以 \((a_1,c,r_3,r_4,r_5,r_6,o)\) 为键，绝不将其内部查询会员也固定为 c。强制动作 C 不获得新的 source2 最优性；其后的 source3…6 是真正 SPE 决策节点。

## 精确检查

- 17 个前端路由的全 513 列身份：8721 个通过。
- 12 个冻结边界态 × 751 行：9012 个三元组、27036 个 Fraction 标量通过。
- P25：200 个内部态、48 个精确极小值、3072 个单均值情形、768 个双均值情形通过。
- C30：重算全部 2048 内部态和 128 包络；完整 8192 新状态映射及符号通过。
- 三个物理合成实例：全 2253 条预算通过，涵盖七单点、同覆盖异标签/空标签/重复行动和零客户。
- 全部 24 个直接来源保持字节不变；原 751/243 kernel 及 751 目录保存字面审计副本，旧 kernel 未执行。

没有分配大矩阵，没有读取或绑定旧 1002/1003 点，没有 optimizer 或 phase I。本包不声称回放完整 751×8192 矩阵。

## 文件与使用边界

完整论证见 [derivation.md](actual_source2_fixed_C_lift/derivation.md)，源审查和检查范围见 [source_review.md](actual_source2_fixed_C_lift/source_review.md)。

机器接口为 [symbolic_template.json](actual_source2_fixed_C_lift/symbolic_template.json)、[active734_catalogue.json](actual_source2_fixed_C_lift/active734_catalogue.json)、[full751_audit_view.json](actual_source2_fixed_C_lift/full751_audit_view.json) 与 [visible_prerequisite_routing.json](actual_source2_fixed_C_lift/visible_prerequisite_routing.json)。逐行迁移表在 [migration_audit.json](actual_source2_fixed_C_lift/migration_audit.json)，精确结果在 [symbolic_check_result.json](actual_source2_fixed_C_lift/symbolic_check_result.json)。

所有未来点字段保持 null；需要先通过新必要族筛选并由 Main 单独释放。未来普遍投影取每完整 h 上的 16 尾态最小值，质量等式乘子允许为负，且必须检查完整 8192 域。当前合同是完整 SPE 的必要层，不是充分刻画，不给出新的数值界；原六人半覆盖命题仍 OPEN。
