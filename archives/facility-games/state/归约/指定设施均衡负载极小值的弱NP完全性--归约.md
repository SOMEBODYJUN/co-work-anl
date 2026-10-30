---
id: "facility-games/designated-facility-equilibrium-load-weak-np-completeness"
kind: "reduction"
type_tag: "归约"
title: "指定设施均衡负载极小值的弱NP完全性"
status: "self-contained-local-reduction; compatible-with-pseudopolynomial-DP"
legacy_ids: ["LOCAL-HARD"]
source_refs: ["source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/local/hardness.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/local/hardness.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/local_and_exact/exact_algorithms_and_extensions.md", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/local_and_exact/exact_algorithms_and_extensions.md", "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/hardness_enum.py", "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:tests/audits/hardness_enum.py"]
---

# 指定设施均衡负载极小值的弱NP完全性

## 目标是局部真实极值

给非负整数私有A,B、正整数共同权及整数Q，问固定双设施布局是否有精确独立混合客户NE满足Δ=L_1−L_2≤−Q。第一负载=(A+B+Σw+Δ)/2，因此阈值NP完全推出指定坐标极小值弱NP难。不是选址SPE问题，未预先限制混合人数，亦非有限菜单最小值。

## 从SUBSET SUM到二次有界源

对正整数b_1,…,b_N、目标0≤S≤Σb，取M=2Σb+1，生成a_(2i+1)=M5^i+b_(i+1)、a_(2i+2)=M5^i，R=MΣ5^i+S。允许每a的重数t∈{0,1,2}。低位Σt_odd b<M，每个五进制位t_odd+t_even≤4无进位，所以等和恰迫每对重数和1，低位正是普通子集和。数位O(N+logΣb)，归约多项式；源变体无需另引未经证明的困难性。可预处理R越界。

## 局部博弈编码及两个方向

令U=Σa_i，Q=2U+R+1。n个变量重Q+a_i，n+1个锚各Q，私有差δ=R−U，以A=max(δ,0),B=max(−δ,0)实现（若要求正私有可两边同加正数）。若Δ<−Q，全部锚只能纯1，即便变量全纯2也有
\[
\Delta\ge\delta+(n+1)Q-\sum_i(Q+a_i)=Q+R-2U>0,
\]
矛盾。因此阈值只可能恰Δ=−Q。

在Δ=−Q，锚纯1/纯2（指定混合端点也是纯2）；变量纯1、实际混合、纯2分别编码t_i=0,1,2。变量混合的坐标−Q、概率a_i/[2(Q+a_i)]确在(0,1)。设总非纯1人数r，包括锚和变量。相对全纯1扣重得
\[
2Q(n+1-r)=\sum_i t_i a_i-R.
\]
右绝对值<2Q，所以r=n+1且Σt_i a_i=R。反向给解，各变量按其t安置，用n+1个锚中恰好n+1−变量非纯1数个纯2补足r，所有NE比较都成立，差恰−Q。

[完整谱定理](../定理/两设施原子客户的完整混合均衡负载谱--定理.md)给NP证书：m≠1支持有多项式位有理点；m1分子0给权端点闭区间，取与阈值交集的有理端点即可。于是阈值NP完全。正整数[DP-W](../算法/两设施均衡谱的阈值动态规划与权类参数化--算法.md)又给数值总重伪多项式界，故保存为弱困难，不声称强NP难。

## 无私有者也足够

先用t→2−t把目标改R'=max(R,2U−R)∈[U,2U]，仍等价。取Q=2U+R'+1，删所有私有；若d=R'−U>0，加一名共同权d<Q客户。任何Δ≤−Q均迫此小客户纯1，恰模拟私有差d；d0不加。因此完全同覆盖、A=B0的对称两设施游戏的指定坐标极小值仍困难。单地点选址却显然有精确均衡，进一步说明局部oracle难不等于全局见证难。

## 最优点可能需要无界实际混合者

A=B、2r个单位共同客户（r≥2），最小差为−(r−1)/r，唯一结构为r−1纯1、r+1实际混合、各p=1/(2r)。纯NE差为偶整数且|Δ|≤1，故仅0；单混合需奇数个±1和0，不可能。m≥2、b名纯2、负差q=−Δ>0时
\[
q=(2r-m-2b)/(m-1)\le1.
\]
分子分母奇偶相反，故q<1。m≤r时整数性得q≤(m−2)/(m−1)<(r−1)/r；m≥r+1时q≤(2r−m)/(m−1)，严格随m降，仅m=r+1,b0取所给值。四单位已需三混合，不能用“最多两人混合”的有限表求精确极值。

原hardness_enum.py只是小域现象发现器：枚举n3..6、权1..7非降、δ−3..3，遇全部最小支持均带pure2且至少两混合即首次退出；本轮真实停在w=(1,3,3,3,5)、δ3、最小gap−2，三型均两名重3混合且有纯2重5。它未跑完所列全域、不证明本归约或无界族；函数的±10^6哨兵只在这个小域安全，不当通用谱求解接口。
