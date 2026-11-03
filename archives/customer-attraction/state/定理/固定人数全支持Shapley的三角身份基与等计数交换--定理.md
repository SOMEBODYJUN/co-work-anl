---
id: customer-attraction/fixed-population-all-support-triangular-shapley-identities
kind: theorem
type_tag: 定理
title: 固定人数全支持Shapley的三角身份基与等计数交换
status: proved-for-all-positive-integer-m-p; once-original-Fraction-replay; signed-linear-image-only
summary: 固定人数终局收益以可见覆盖坐标为三角参数，恰v-d条独立身份充要刻画共同有符号客户表示；另保等计数标签收益差的正系数交换式。
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/tree/all_support_shapley_circuits.md#1"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/tree/all_support_shapley_circuits.md#2"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/tree/all_support_shapley_circuits.md#3"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c50fecc37aa44fb4a69a2122bb70e5fe/tree/verify_all_support_shapley.py#audit"
---

# 固定人数的对象与正边际

令非空有限标签集P有p个标签，固定整数m≥1。计数q∈Z_{≥0}^P、|q|=m，A=supp(q)，仅对q_a>0定义一位选a者的收益F_(q,a)。同覆盖不同标签、空主题、重复选择和零客户均允许。下文是一份共同终局资料的表示定理；没有把完整策略的有序历史改成计数历史。

对非空兴趣类型B⊆P，以同一张实有符号质量w_B定义
\[
 C(S)=\sum_{B:B\cap S\ne\varnothing}w_B,\qquad
 F_{q,a}=\sum_{B\ni a}\frac{w_B}{q(B)},\quad q(B)=\sum_{b\in B}q_b.
\]
C(∅)=0，只需要|S|≤m的可见覆盖资料。真实单位客户模型还要求w_B为非负整数；本定理的线性等价允许负数。有理非负质量可统一清分母成为单位客户，负号不能这样消除。

对R⊆A\{a}，设
\[
 \lambda_R(q,a)=\int_0^1 t^{q_a-1}
 \prod_{b\in R}(1-t^{q_b})
 \prod_{b\in A\setminus(R\cup\{a\})}t^{q_b}\,dt.
\tag{1}
\]
每个λ_R严格正，和为1/q_a，而且
\[
 F_{q,a}=\sum_{R\subseteq A\setminus\{a\}}\lambda_R
       [C(R\cup\{a\})-C(R)].
\tag{2}
\]
逐类型证明：若a∉B，两侧均零；若a∈B，非零覆盖边际要求R避开B。对其余标签的两种选择求和，被积式成为t^{q(B)-1}，积分为1/q(B)。线性相加给(2)，全过程不需要w≥0。各因子在0<t<1正，给λ的严格正性；对全部R求和后只余t^{q_a-1}，给系数和。

用于精确实现的有限公式是
\[
 \lambda_R=\sum_{D\subseteq R}\frac{(-1)^{|D|}}{m-q(R)+q(D)}.
\tag{3}
\]
分母至少q_a>0。交错形式应按有理数求值，其一般正性由积分承担。将(2)移项得到两侧非负系数的等式
\[
 F_{q,a}+\sum_{\varnothing\ne R\subseteq A\setminus\{a\}}\lambda_RC(R)
 =\sum_{R\subseteq A\setminus\{a\}}\lambda_RC(R+a).
\tag{4}
\]
等式在signed模型中仍真，只有将每个边际视作非负余项时才额外使用客户非负性。

# 消去低人数层后的完整三角身份基

全部固定m收益顶点为V={(q,a): |q|=m,q_a>0}。它的大小和可见非空覆盖坐标数分别是
\[
 v=p\binom{m+p-2}{p-1},\qquad
 d=\sum_{k=1}^{\min(m,p)}\binom pk.
\]
对每个非空支持A、|A|≤m，从支持恰为A的收益顶点任取一个基准ρ_A=(q^A,a_A)。设β(q,a)=λ_(A\{a})(q,a)>0。把(2)写成
\[
 F_{q,a}=\beta(q,a)C(A)+L_{q,a}(C),
\tag{5}
\]
其中L只含A的真子集覆盖：最高支持项C(A)只由R=A\{a}出现一次。

按|A|递增，用基准方程恢复
\[
 C(A)=\frac{F_{\rho_A}-L_{\rho_A}(C)}{\beta(\rho_A)}.
\tag{6}
\]
将恢复值代入同支持的每个非基准方程(5)，恰得到v−d条齐次线性身份。这些身份独立，且一个固定m的全收益向量具有共同signed客户表示，当且仅当它满足这些身份。

证明充分性包含两个不能省去的步骤。首先，每个非基准方程有一个独有的非基准收益变量、系数1；(6)只递归使用各支持的基准变量，不使用非基准变量。因此v−d条独立，解空间维数d，所有收益由d个恢复覆盖坐标唯一决定。其次，任意这些截断C都确有共同signed实现：任意补充|S|>m的覆盖值，固定C(∅)=0，再取
\[
 w_B=\sum_{D\subseteq B}(-1)^{|B|-|D|}
       [C(P)-C(P\setminus D)]\quad(\varnothing\ne B\subseteq P).
\tag{7}
\]
布尔反演给Σ_(B⊆D,B≠∅)w_B=C(P)−C(P\D)，故所得客户确恢复所有C(S)。由(2)又恢复全部给定F。有理输入使λ、恢复和反演全部有理。必要性直接由(2)。这同时补足原稿以覆盖行满秩描述的存在性论证，不靠有限秩测试证明一般m,p。

同支持效率Σ_a q_aF_(q,a)=C(A)是客户表示的推论，因而已经包含在完整身份中。仅给这个总和并不恢复全部跨标签分配。成熟[正边际与平衡贡献定理](共同客户收益的正边际与平衡贡献--定理.md)用全部1…m层的E+BC扩展变量刻画同一signed空间；这里独有的是只保第m层的显式v−d独立消元基，二者条件相容。

# 等计数标签的正交换

当q_a=q_b=r>0，置D=A\{a,b}，定义
\[
 \theta_R=\int_0^1t^{r-1}\prod_{c\in R}(1-t^{q_c})
                    \prod_{c\in D\setminus R}t^{q_c}\,dt
 \quad(R\subseteq D).
\]
则θ_R>0、Σ_Rθ_R=1/r，而且
\[
 F_{q,a}-F_{q,b}
 =\sum_{R\subseteq D}\theta_R[C(R+a)-C(R+b)].
\tag{8}
\]
同时命中a,b的类型两边都消去；只命中其中一个时同(2)的积分证明。右侧只含A真子集，最高支持覆盖确已消失。没有使用这些覆盖差非负。

两个特例可直接复用：

* A={a,b}、q_a=r、q_b=s、r+s=m时，λ_∅=1/m、λ_{b}=s/(rm)，故mrF_(q,a)+sC(b)=rC(a)+sC(ab)。m3时同双支持有四个收益顶点；加已恢复的单主题覆盖，恰有三个独立约束，须与[完整二主题纠错](固定完整策略的二主题耦合二倍界--定理.md)的秩三条件相符。
* m个不同标签各一次时，λ_R=|R|!(m−|R|−1)!/m!，θ_R=|R|!(m−|R|−2)!/(m−1)!。m3的abc上，6F_a+C_b+C_c+2C_bc=2C_a+C_ab+C_ac+2C_abc，故2(F_a−F_b)=C_a−C_b+C_ac−C_bc。后二式有三支持分配信息，仅查二支持收益顶点不能代替。

# 原代码、一次实跑与准确停止处

3347B原verify_all_support_shapley.py全文读：以Fraction逐个兴趣类型核边际、三角消元、每条身份在全部客户列上为零、身份秩及等计数交换；不导solver、NumPy或SciPy。其本次原样一次执行exit0/stderr0，输出如下。一般定理由前文证明承担。

|m,p|固定层顶点v|覆盖维数d|独立身份v−d|逐类型边际检查|逐类型交换检查|
|---|---:|---:|---:|---:|---:|
|1,3|3|3|0|21|0|
|2,4|16|10|6|240|90|
|3,4|40|14|26|600|180|
|4,3|30|7|23|210|42|
|3,6|126|41|85|7938|3780|

[原件及执行记录](../../tools/evidence/boss3-c16-resumed/README.md)保留源码、完整stdout、SHA及环境。源md与代码全部阅读；程序只验证列出的五组，没有把原稿“独立审查进行中”改成他人已审或外审。

与[共同signed四人障碍](../障碍/共同有符号客户的四人超二福利与局部负原子--障碍.md)的逻辑联系是：那份负质量表自动满足本页所有身份，却有形式SPE的比较值160/79>2和可见负原子。因此完整span仍不代替非负客户cone。接续half支付还需一份完整策略的所有真实激励Γ非负组合以及在非负客户上非负的余项；本定理不自动提供乘子或福利界。阶段三可登记“表示等价/特化”和“线性完整仍不足”的有条件关系，目前以本文准确证据保留，不从旧图复制超边。
