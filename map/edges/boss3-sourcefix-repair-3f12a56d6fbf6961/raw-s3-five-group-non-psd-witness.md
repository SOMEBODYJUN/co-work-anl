# 五组 raw S3 点的负 canonical 平方

在完整 normalized-flat 菜单域中，存在有理 raw S3 点，其指定同点拉回满足 canonical plain-SA1，但违反 canonical M1。该点也无法由真实调度的共同概率分布实现。

## 原矩阵与共同 functional

取五组，每组有 indexed states $0,1$。每个 state 有一件系数为 $1$ 的 incidence，且其资源与其余九件 incidence 的资源均不同。普通矩阵有十台 private roots、十台 unit resources、五枚 unit selectors 和十件 incidence jobs，共三十个原有限端变量。取 $T=1$。

用五个 Boolean 位 $b_i$ 作原端代换。第 $i$ 组的 state $1$ 和 state $0$ 的 selector 端分别代为 $b_i$ 和 $1-b_i$。每件 incidence 的 private 端 $D_e$ 代为 $0$，resource 端 $E_e$ 代为 $1$。在五位 Boolean 商代数中，对每个 $|S|\le4$ 定义

$$
\ell\!\left(\prod_{i\in S}b_i\right)=\mu_{|S|},
\qquad (\mu_0,\mu_1,\mu_2,\mu_3,\mu_4)=(1,1/2,1/6,0,0).
$$

每个总次数至多四的原多项式经代换、Boolean 降幂后，用这张表线性求值，得到共同 $L$。对任意至多四个不同位，$\ell$ 在这些位上的限制恰是从四个位置中均匀选择两个位置置 $1$ 后的相应边际。因为任意 $k$ 个指定位置同时取 $1$ 的概率为 $\mu_k$，所有 square-free moments 一致。若 cylinder 指定 $p$ 个正位和 $q$ 个负位且 $p+q\le4$，其值为 $\binom{4-p-q}{2-p}/6$，超出二项式范围时取零。重复 literal 在 Boolean 商内约去，含互补 literal 的乘积为零。

## S3 各约束与负平方

归一化 $L(1)=1$。每条原 Boolean 等式在商代数中为零。每条 selector cover 是 $b_i+(1-b_i)-1=0$，每条 incidence cover 是 $0+1-1=0$，故所有合同允许的等式乘子也给零。每条 box 经代换是 $0,1,b_i$ 或 $1-b_i$。每台 private 的 physical slack 是 $1-a_s$，因为所有 $D_e=0$。每台 resource 的 physical slack 与独立 unit-cap1 都是 $0$，因为恰有一件 incidence 可用该 resource 且 $E_e=1$。任一长度至多三的 raw-literal 乘子经代换是常数或 literal 的积。与任一上述不等式行相乘，结果是零或长度至多四的 Boolean cylinder，故 $L$ 值非负。

指定拉回 $A_s=a_s,\ Z_e=a_sE_e$ 给每个 state 的 $Z_e=A_s$。canonical Boolean 和组等式在商代数中恒成立。gate 与 quality 行均为零，因为 $T=p_e=1$。每条 resource 行是 $1-Z_e$，每条 box 行也是 literal。它们乘空乘积、任一 primitive 或其补后，都是至多两个 literals 的乘积，故完整 canonical plain-SA1 成立。

记 $Y=\sum_{i=1}^5 A_{i,1}$。所得 canonical 表 $F$ 满足

$$
F(Y)=5/2,\qquad F(Y^2)=5/2+2\binom{5}{2}/6=35/6,
\qquad F\big((Y-5/2)^2\big)=-5/12.
$$

因此该 $F$ 的 canonical M1 非 PSD，任意真实调度共同概率分布也无法实现这张二阶表，因为平方在真实分布下期望非负。原端同一 affine 平方也有负值，所以该 $L$ 不满足可选的 raw M2 假设。

该矩阵的真实最优峰为 $1$。任取各组一个 state 执行 selector，将全部十件 incidence 送往各自不同的 resource，便得到完整调度。unit selector 给峰值下界 $1$。因此该反例限定在给定矩点的 PSD 与联合 law，实际调度的 Dirac 点仍满足 S3。
