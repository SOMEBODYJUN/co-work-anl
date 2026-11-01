---
id: customer-attraction/all-same-support-gradient-cycles-do-not-enforce-common-clients
kind: obstruction
type_tag: 障碍
title: 同支持全部梯度环不能替代共同客户表示
status: proved-analytic-cycle-reduction-with-exact-saved-primal;not-SPE-counterexample
summary: 三人六标签的9/4抽象点满足全部同支持任意长度凹梯度环，因每个双支持类只有两计数而归约为十五个非负生成环；共同signed表示仍失败。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-e593a544afa7433cb0e8a7f39ebde6be/coupling_charge/cyclic_gradient_boundary.md
---

# 同支持全部梯度环不能替代共同客户表示

对真实非负单位客户，固定总人数m与同一非空支持A，所有计数q严格正于A、零于外。仅收命中A的客户，令 \(L_A(q)=\sum_x\log q_x\)，梯度是各题一名玩家的真实收益U_a(q)。凹性给 \(L_A(r)-L_A(q)\le(r-q)\cdot U(q)\)，沿任意有限有向闭路q⁰…qᵏ=q⁰望远镜得
\[
\sum_{j<k}(q^{j+1}-q^j)\cdot U(q^j)\ge0.\tag{CG}
\]
二点环逐客户精确余项
\[
(r-q)\cdot[U(q)-U(r)]=\sum_{x:x\text{命中}A}\frac{(q_x-r_x)^2}{q_xr_x}\ge0.
\]
同支持保证分母正；不能把未用题收益补0后越支持套log0。这与[额外查询背景梯度](../引理/主题背景查询梯度的平方正性与自回复边界--引理.md)的log(1+b)域不同，两个必要性质不互换。

## 任意长度如何完整约成十五环

m3/p6时，大小1或3的固定支持只有一个正计数；大小2支持{a,b}只有q=2e_a+e_b、r=e_a+2e_b，共15类。任何闭路非自跳转的q→r与r→q次数相同，故(CG)值为对应二点生成环余项的非负整数倍；自环值0。因此检查15个生成环已涵盖**所有长度**同支持闭路，不是有限截断只查短环。

[现有9/4固定策略点](同支持守恒与局部客户耦合的严格间隔--障碍.md)已完整证明全部43节点258形式IC、2520锐同题稀释、支持守恒、根034覆盖1及固定比较124覆盖9/4。它不是真客户表：例如标签0/1的共同signed必要差式左1/8右0。该已有完整原始/对偶检查不重跑。

本轮从其真实28402B coupling_layers.json只消费头部/43动作/root/portfolio及**第一层全部126个有理收益**，其余六层及对偶字段不扩称本批全审；用自写已知输入Fraction检查第一次新增所需15个环：

| 精确余项 | 支持类数 |
|---|---:|
| 0 | 1 |
| 1/8 | 9 |
| 3/16 | 2 |
| 1/4 | 3 |

全部非负。这给一个明确保存的必要系统点同时满足所有(CG)而固定比较9/4>2，故(CG)强化仍不能推出该固定策略比较的二倍预算。原related稿另指定SHA0630620f…的support_conservation_obstruction.json；该原JSON未在本批取回或逐字节对比。这里用现行已认证点及上述新15环计算独立接续相同数学分布，不声称两物理JSON同版本。

原稿verify_cyclic_gradient_boundary.py的旧运行声明不改成本次已跑。唯一新计算是合并已知输入核的一部分，0原该入口/0LP/0新盲审；全部任意长度和任意客户数量来自上面解析归约与已有精确点，不由采样或浮点输出推断。不能把这点称共同signed/非负客户SPE或原half反例。后续合法跨支持身份与共同非负锥仍需额外信息。

原件、逐项指纹、真实读取范围和本批运行事件见[本批证据](../../../../tools/evidence/cag-maxroot-terminal-share-and-direction-primary/README.md)。
