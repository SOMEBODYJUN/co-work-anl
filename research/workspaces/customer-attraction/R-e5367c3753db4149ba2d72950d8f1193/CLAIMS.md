# 本轮精确命题与证据

本目录为个人恢复资产，未自动并入共享 canonical 账本。所有结果均无外审及全球新颖性认证。

## Q-CAG-HALF：OPEN，身份不变

对象：任意有限单位客户集、有限非空共同集合目录、任意 m>=1；全部有序历史纯 SPE。
允许空主题、重复、零客户和任意历史平局。结论 `OPT_m<=2W`。
本轮没有一般证明或真正反例。规范身份及依赖以仓库共享模型、问题页和账本为准。

## LOCAL-RESERVATION-SPE-v1：一般条件性构造，内部证明并独立重构

**Exact statement.** 对每个 n>=2 的上述旧游戏、每份完整 SPE sigma，若全部旧节点的规定当前
最终收益至少 eta，存在正整数 J 满足 J/2<=eta 及
`J>=max_T(|T|-min_S|T∩S|/2)`，则添加 J 名不交单位客户的一个新主题 B 以及一位新首人，
存在完整 SPE：无 B 历史选 B；恰一个 B 历史擦除 B 执行旧 sigma；第二 B 以下由 BI 补全。
实际根为 B，之后逐字旧实际终局；全部旧历史保留，不只保实际叶。

**Domain/quantifiers/definitions.** 任意旧 n 与目录，不要求目录向下闭合或极大主题；eta 是全历史
规定收益保底，不只实际路径最小值。n=1 需要在上述策略的根另加 `J>=max_T|T|`。
J>0 保证新主题作为集合不同。**Conclusion/scope.** 仅构造指定新 SPE，不声称新游戏所有 SPE 分解。
**Dependencies.** 单位均分、共同目录、有限逆向归纳、同终局含一名其他旧玩家时的交集支付上界。
旧储备构造来源为 R-6bb0323d87294932af2aa23b47b9d4ad；新构造移除其严格退出条件。
**Evidence.** [root 自足推导](GENERAL_WORKING.md#3-新的全历史构造移除旧的严格退出条件)、
[独立证明](independent/reservation_lift_independent_audit.md)；menu/ 的第二份审查和精确回归。
**Counterevidence.** n=1、旧唯一三客户主题、J=2 反驳不加边界条件的版本。

## LOCAL-RESERVATION-MENU-v1：一般条件性闭包，内部证明并独立重构

**Exact statement.** 对任意 n>=1 旧完整 SPE、任意存在的逐字不交储备提升，令 W 为旧实际福利，
M 为旧实际终局的 extra-slot 插入 cap。假设 M<=J 及 (n-1)J/2<=W。
对每个旧位置分布 lambda，令 E=n sum_i lambda_i psi_i(p)-W，psi_i 为实际前缀全部强制行动的
完整 n 槽终局菜单的独立查询最小值。新权重 lambda'=(1,n lambda)/(n+1)。
对每个新查询 p'=alpha delta_B+(1-alpha)p，

    E' <= (1-alpha)E -(1-alpha)(J-L_z(p))
                    -alpha[W-(n-1)J/2].

因此旧全查询时间预算保持；均匀时间预算是其特例。若另有 M<=W/n，则新实际插入 cap
`max(M,J/2)<=(W+J)/(n+1)`。

**Assumptions/scope.** 完整逐字提升的存在是独立假设；不能只从两个标量条件推出存在。
任意新查询支持、alpha=0/1、任意历史平局均包含。原一般 U/Mpath/half 仍未证。
**Dependencies.** 全菜单含实际叶列、旧动作列保持、客户不交、非负最小化与同一组时间权重。
**Evidence.** [自足正文](menu/reservation_menu_budget_closure.md)、
[独立审查](independent/reservation_lift_independent_audit.md)。
**Objections.** 无已成立致命异议；但闭包没有给任意旧游戏预算的初始来源。

## LOCAL-LAST-DELETION-ONE-v1：全称加强 FALSE，完整 SPE 反例并独立重构

**否定的 statement.** 对任意完整 SPE、任何原 i<m 的节点 h，记规定原叶 Z、强制当前 T 后真实原叶 Z_T，
删原末位叶 Z_T^-。全称要求 `max_T u_i(Z_T^-)<=u_i(Z)+u_m(Z)`。
**Counterexample.** 全部35单位客户、四共同主题、三人完整 SPE，实际 ABC 收益(13,13,9)，
真实强制 T 得 TCA，删除末位 A 后收益24>22。原实际根退款为零。
**Scope.** 仅此桥 FALSE。原 OPT=W=35，Q-CAG-HALF 未被反驳；不称最小反例。
**Dependencies/evidence.** [自足反例](harmonic/last_deletion_one_counterexample.md)、同目录完整证书及独立
Fraction 审计；root 重跑，归纳分支独立重构。全部有序历史而非只实际路径。
**Related.** 旧任意删除 q+1 近似 SPE 及退款守恒仍保留；新的分支退款支付必须额外处理真实重置。

## LOCAL-REFUND-POTENTIAL-IC-v1：旧退款关系的全历史组合，解析成立

**Exact statement.** 任意合法固定背景、任意该子局完整纯 SPE、任意固定活跃删位集，至少保留一名活跃者。
按旧因果回放提升每个新历史。原叶 z 上令 R_j 为每名存留玩家（含固定背景）的退款，
H=P_deleted−e=sum_j R_j，e 为真正丢失的覆盖。当前 i 的 epsilon_i=H−R_i>=0。
对每条新当前偏离，原同角色真实 IC 松弛为 Gamma，则

    gain_new−(H_deviation−H_actual)
       = epsilon_actual−epsilon_deviation−Gamma.

若规定叶未来有 r 名存留活跃者，`sum_future epsilon_i=(r−1)H+I_fixed`，I_fixed 为固定 incumbents 退款。
**Definitions/scope.** 规定与偏离叶使用各自真实后继；不能丢弃势差或重用实际 H。固定背景不删除。
此为前驱退款 IC/逐客户守恒的直接组合，不认领新的福利不等式。
**Evidence.** [解析正文](induction/refund_potential_contract.md)、定义级独立 Fraction 审计；root 重跑。
**Remaining objection.** 共税与动作补贴仅为辅助转移支付；未编译为原单位客户模型，储备可随人数增大。
因此不能调用较小原 CAG 的精确 SPE 归纳，BG-HALF 及主目标均仍 OPEN。
