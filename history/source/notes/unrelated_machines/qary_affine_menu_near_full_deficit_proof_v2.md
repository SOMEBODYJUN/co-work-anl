# q元 affine 菜单fiber缺项合同：作者 Proof v2

对应 `UM-QARY-AFFINE-MENU-NEAR-FULL-DEFICIT-v2`，Exact SHA256 584e7e3ad6ae0ad44b03781a3b9069d6cafa2296e59cfc7eb75070c08eea8759。先完整冻Exact再写本Proof；暂hold，不交未冻结Exact-only记录的reviewer。v1 Exact/Proof原字节均保留。本页不增加逐个数值探针。

全部对象和N=q^t按Exact，ℓ可任意nonlinear。

## 1. Concurrent family的精确union

给resource x=(a0,b0)及非空F⊆F_x。每g∈F满足ℓ(g)=b0+g*a0，其中乘法逐坐标。令a=a0+δ，则该selected state在这个固定a block唯一给出的resource是

(a,b0−g*δ)。

设δ的非零坐标集合为J。乘以δ_i在J内均可逆，J外输出b_i=b0_i固定，所以g∈F产生的不同b恰有|π_JF|种。给定J恰有(q−1)^|J|个δ；不同a blocks互不重叠。包括J空时的唯一x，故整个selected-state union精确为

Σ_(J⊆[t])(q−1)^|J|·|π_JF|。

若F中每组至少分得N−D个不交resources，总计k(N−D)≤该union。利用Σ_J(q−1)^|J|=q^t=N，移项即得Exact(A)的缺项不等式。外部groups是否另占这些resources不影响必要性：忽略外部占位只会把可用union放大。

## 2. 粗projection界与K

每个非空J有|π_JF|≤min(k,q^|J|)；J空则恰1。因此

Σ_J(q−1)^|J|(k−|π_JF|)
≥(k−1)+Σ_(j=1)^t binom(t,j)(q−1)^j·max(k−q^j,0)
=H_(q,t)(k)。

对完整fiberF_x应用第1节，每个非空fiber的k_x满足H(k_x)≤k_xD，从而k_x≤定义中的K(D)。k1的H1=0，所以K定义集合非空。这里未假设每个投影同时饱和，也未声称H是可达到的精确最小缺项函数。

## 3. 全局pair计数与缺项

每g有恰(q−1)^t个h在全部坐标都与g不同。任意这样的不同g,h，无论ℓ如何，逐坐标两个不同斜率方程有唯一解，故它们的selected states有唯一共同resource。因此

Σ_x binom(k_x,2)≥N(q−1)^t/2。

额外同坐标group对若相交，只会多增加左侧，不会减少这个下界。

给定B不交，对每个k_x≥1的resource最多一个group能保留它，故至少k_x−1份selected-state incidence领取被遗漏。全部groups的总遗漏≤ND，于是Σ_(x:k_x≥1)(k_x−1)≤ND。再由k_x≤K(D)，

N(q−1)^t/2
≤Σ_x k_x(k_x−1)/2
≤K(D)·Σ_(x:k_x≥1)(k_x−1)/2
≤K(D)ND/2。

约去N/2给D K(D)≥(q−1)^t。未用2D<q，也未假设fiber内groups每个坐标都互异。

## 4. q3,t3下界与真正actual上界

若q3,t3且D≤2，对任何k≥4，H(k)只取j0及j1项就有

H(k)≥(k−1)+6(k−3)=7k−19>2k≥kD。

所以K(D)≤3，继而D K(D)≤6<8=(q−1)^t，与第3节矛盾。这排除全部nonlinear selector函数的D≤2，故D*≥3。

上界固定cyclic ℓ_i(g)=g_(i+1)。对固定a，kernel满足δ_(i+1)=a_iδ_i，非零kernel当且仅当a_1a_2a_3=1。F3中这种a恰4个，rank均2；其余27−4=23个a的映射为bijection，因此每g在这些a下各有23个真正独有的resources，先全领。

在4个奇异a下，建立groups到实际image resources的二部图。每group degree4，每resource degree3；任意左子集X的邻集至少4|X|/3≥|X|，整数matching可每group再给一项不交resource。因此全部27组同时领取24项，D*≤3；得D*=3、V*=8/9。

完整actual：每selector放上述cyclic state，只导出所领24项的24件selected-state jobs；同state其余3件和所有未选state jobs留各自private。selected private负载1+3/27=10/9；未选private1；resource≤1。所有原jobs各一次，实际峰10/9。

反向任意actual若C<10/9，因unit selector必C≥1，且C<2使每resource至多一件unit incidence。取各实际selector所在state的实际exports；每selected private上的未导出件数u_g满足1+u_g/27≤C<1+3/27，整数性给u_g≤2。于是这些真正exports给D2的不交allocation，与上面解析下界矛盾。故ordinary OPT恰10/9，不依赖先规范化未选state jobs。

## 5. v1边界、位复杂度及范围

v1严格2D<q的合同由其原Proof保持；它排除同坐标支持交点后给k_x≤q。v2不擅自将该前提改成等号；本页第3节用更一般H/K而非声称v1所有参数被严格包含。

H(k)/k=(1−1/k)+Σ_j binom(t,j)(q−1)^j·max(1−q^j/k,0)，每项随正整数k不减，故K(D)可用整数比较H(k)≤kD二分计算。全部整数的位长由q^(O(t))界定，按O(tlogq)量级；H用t项求和，不按2^t枚举投影子集。K仍只是必要边界，不是一般可行性或优化算法。

P/完整见证的输出和回算仍按显式N³ incidence及O(tlogq)private权位长多项式；没有poly(t,logq)输出声称。全局一般q,t的nonlinear最优仍未证明等于affine，主negative tiny-gap源及physical全fiber/block-fiber一致性机制均未由这些toy必要界解决。
