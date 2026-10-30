---
id: "customer-attraction/middle-incidence-stationary-payment-obstruction"
kind: "obstruction"
type_tag: "障碍"
title: "中间极大关联的平稳逐客户支付障碍"
status: "complete"
truth_status: "proved-template-obstruction"
review_level: "semantic-and-algebraic-reconstruction"
scope: "四个极大主题标签；r≥3；任意非负整数背景；未认证完整SPE"
summary: "无自转移且唯一均匀平稳的真实人数路由模板，对二元中间关联给严格负系数；不能靠换一个平稳分布修复。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/customer_attraction/extreme_maximal_membership_floor.md#6-一般目录的精确停界"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-0f99797b33de46bfb498541a0bc5fae9/parent/stationary_middle_incidence_boundary.md"
---

# 中间极大关联的平稳逐客户支付障碍

## 精确对象

[单例缺一归属定理](../定理/单例缺一极大归属的真实中继保底--定理.md)证明三种客户类型的平稳加权系数非负。
本页构造满足“整数路由人数、无自路由、固定后继人数、平稳概率”这些局部限制的菜单，
说明同一个**逐客户非负系数**结论不能原样扩展到中间归属。
菜单尚未验证各分支的全部SPE最优性，它不是主模型福利反例。

令 $r\ge3$、$n=r-1\ge2$，四个极大主题标签中，一个客户只属于 $I=\{1,2\}$。
客户背景负载为任意整数 $b\ge0$。目的标签为行、强制根标签为列，后继路由人数取

$$
M=\begin{pmatrix}
0&n-1&1&0\\
n-1&0&0&1\\
1&0&0&n-1\\
0&1&n-1&0
\end{pmatrix}.
$$

每列及每行之和均为 $n$，对角为零；所以 $R=M/n$ 为双随机矩阵，均匀概率 $\pi_i=1/4$ 平稳。
其正转移图连通且双向，故不可约，有限不可约链的平稳概率唯一。它是否周期性不影响唯一平稳概率。

若后继实际选对应的整个极大主题，该客户在四个根分支的后继覆盖数恰为

$$K=(n-1,n-1,1,1).$$

根减后继平均收益的逐客户系数为

$$\delta_i=\frac{n\mathbf1_{i\in I}-K_i}{n(b+\mathbf1_{i\in I}+K_i)}.$$

两个内部根系数均为 $1/[n(b+n)]$，两个外部根均为 $-1/[n(b+1)]$，因此

$$\boxed{\sum_i\pi_i\delta_i
=-\frac{n-1}{2n(b+n)(b+1)}<0}.\tag{1}$$

$r=3,b=0$ 时，系数为 $(1/4,1/4,-1/2,-1/2)$，平均为 $-1/8$，
恰是原主文的最小标量障碍。式(1)由直接相减证明所有 $r\ge3,b\ge0$，并非仅有限枚举。

## 失败机制与剩余义务

单例和缺一的正负项能由同一个目的标签的平稳流守恒相抵；
二元中间关联则出现 $b+n$ 与 $b+1$ 两种不对称分母，守恒不能消除差额。
因为本矩阵平稳概率唯一，单纯换一个平稳分布也不能让(1)非负。

这并不说明在真实完整SPE中别的客户、较早中继或跨根最优性不能补足负项。
当前构造没有提供一个共同目录、客户全体及完整策略来认证那些全部最优性条件，
也没有否定 $W\ge r\theta_r$ 的所有可能证明。接续时应区分：

- 已否定：只依赖当前逐客户路由守恒、要求每个客户独立非负的直接扩展。
- 未决：真实更早节点或跨客户支付能否补足(1)的负余量。
- 未建立：一般六人half或任意全历史SPE的实际反例。

该关系应登记为“反驳证明模板”，不能登记为“反驳原六人命题”。
原审计对首个 $-1/8$ 点有Fraction复算；本页带参数结论的依据是显式矩阵及有理恒等式。
