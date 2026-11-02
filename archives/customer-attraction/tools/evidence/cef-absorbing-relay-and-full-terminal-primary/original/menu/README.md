# 全路径额外查询的聚合耦合：工作稿

2026-10-24。任务仍是 **Q-CAG-HALF**：任意有限共同目录、任意人数、每个完整有序历史纯 SPE，证明 `2W>=OPT_m`。允许重复、空主题、零客户及任意历史平局。本文仅保存恢复笔记和一次重复诊断，不声称有新候选或新数学。

**来源纠正。** 本轮称作 AP-extra 的候选、额外槽缓冲恒等式、copositive 与两点接口均已有于 [FULL-TERMINAL-AGGREGATE 原稿](../../R-486bb9adb8cd4d9a940dbf3b1ab0b1de/security/full_terminal_debt.md)。下文重构不计新结果。该 actor 的 [dual/parent_review](../../R-486bb9adb8cd4d9a940dbf3b1ab0b1de/security/dual/parent_review.md) 已给固定 group 完整策略整个63类型锥的全部查询对精确 Γ 证书，严格覆盖本轮一次同锥数值 LP；本轮 LP 因此也不计新有限证据。

原稿的逐对全路径充分条件 PAIR-AP **已有完整四人反例**，不是开放候选：[crosscap_failure_report.json](../../R-486bb9adb8cd4d9a940dbf3b1ab0b1de/security/dual/crosscap_failure_report.json)。其245客户、W=180、OPT=245、实际全员45、查询3/5满足交叉365>2W=360；但两点 FTA 多项式 `143t^2-101t+48` 严格正。这精确说明对角自源缓冲不能从证明里删去。independent_core 本轮已独立重放原核验器。

## 精确候选 AP-extra

固定同一份完整 SPE 及其实际路径 `z`。在真实位置 i 强制主题 B、以后沿同一原策略所得完整 m 槽终局记 `Z_i(B)`。固定查询分布 p，A、B 独立服从 p。定义

    C_i^+(p)=E_(A,B~p) sum_(x in A) 1/[1+c_x(Z_i(B))].

候选为对每个实例、SPE 和 p 都有

    sum_i C_i^+(p) <= W.                         (AP-extra?)

它比自由路径菜单付款强：在位置 i 取列分布 B~p，就有

    min_B E_A g_A(Z_i(B)) <= C_i^+(p).

故 AP-extra 以均匀位置权重给 `M_path<=W/m`，再和现有 `OPT_m<=2m v_(m+1)` 接成 half。这里所有背景都含原被强制玩家本人，是完整 m 槽；不能把旧的 m-1 槽 GB 反例当作此候选反例。

## 原去相关债务与额外一槽的精确关系

记 `B_i(B)` 为从 `Z_i(B)` 删除当前位置后的 m-1 个竞争主题。沿用既有定义

    D_i=E_B f_(B_i(B))(B),
    C_i=E_(A,B) f_(B_i(B))(A),
    e_i=u_i-D_i>=0, kappa_i=D_i-C_i.

定义一次共同缓冲

    delta_i(p)=E_(A,B) sum_(x in A intersect B)
      1/[(1+c_x(B_i(B)))(2+c_x(B_i(B)))].

逐客户消去分母得对全部输入成立的精确恒等式

    C_i^+=C_i-delta_i,
    W-sum_i C_i^+=sum_i(e_i+kappa_i+delta_i).     (EXACT)

`delta_i` 只给一份，不能同时支付同一个位置的多个独立预算。AP-extra 的承重缺口正是 EXACT 右边非负；更强的 `sum_i(kappa_i+delta_i)>=0` 也足够，但未证明或否定。原 GB 已否定 `sum_i(e_i+kappa_i)>=0`，不决定加入 delta 后的总符号。

每个纯查询 p=delta_T 的候选逐位置成立：额外查询 `g_T(Z_i(T))` 不超过当前玩家真实偏离收益，后者由 SPE 不超过 u_i。困难全部来自混合查询对源行动的负相关。

## 对已知 GB 反例的明确判别

仅用已知36客户三人完整 group 策略和原 GB 查询 `p(X2)=p(Y2)=1/2`，直接按兴趣类型计算得到

| i | 原 C_i | 额外查询 C_i^+ | delta_i |
|---|---:|---:|---:|
|1|11|97/12|35/12|
|2|23/2|373/48|179/48|
|3|12|193/24|95/24|

所以 `sum C_i^+=1147/48`、`W-sum C_i^+=485/48>0`。原差额 `W-sum C_i=-1/2` 被 `sum delta_i=509/48` 支付。机器有理记录为 [gb_extra_cushion.json](gb_extra_cushion.json)。这只解释既有反例的范围，不支持全称 AP-extra。

另外对同一 published group 完整策略、同一个固定 p，在全部63种非空兴趣类型的 SPE 权重锥里，用 W=1 归一攻击 `W-sum C_i^+`。该单次 LP 未给反例，数值最小值约0.221816；见 [attack_aggregate_extra.py](attack_aggregate_extra.py) 与其 JSON。该诊断已被上述旧全锥精确证书覆盖，作为重复工作轨迹保留；不继续扩同种扫描。

## 真实后继的势身份与不能省略的量

在一个背景 b、剩余 r 人的真实节点，强制 A 后尾序列记 Y_A，令

    Phi_b(Y)=sum_x sum_(j=1)^(c_x(Y)) 1/(b_x+j),
    F_A=Phi_b(Y_A),
    R_AB=Phi_b(A,Y_B)-Phi_b(A,Y_A),
    d_A=Phi_b(A,Y_A)-Phi_b(Y_A).

现有精确身份为

    K_AB=d_A+F_A-F_B+R_AB-delta_AB.

独立 A,B~p 平均后 F 漂移相消，AP-extra 因而要求沿实际路径的真实后继联合势遗憾满足

    sum_i E R_i <= sum_i(e_i+delta_i).            (DEBT?)

该式只是 EXACT 的另一种写法，尚非付款证明。r=2 时 Y 是单个合法行动，末位真实 IC 给 R<=0；r>=3 时整个 Y_B 不是一个玩家的合法行动，不能这样用。

相同计数的交换历史可以有不同续局。不能把 `(h,A,S_i)` 与 `(h,S_i,A)` 的原策略叶子当作相同，不能在二者间无代价移动源行动，也不能把实际后继冻结。下一步只应寻找真实全树 IC 对 DEBT 的共同付款，或对 AP-extra 的完整严格反例；一般 half 仍 OPEN。
