# q元 affine 菜单近满缺项障碍：作者 Proof v1

对应 `UM-QARY-AFFINE-MENU-NEAR-FULL-DEFICIT-v1`，Exact SHA256 ed16808a96e27a50e4d02ab8c2ec83e7f0df9046176531e45db38f5af5170afb。先冻Exact后写本Proof；未主动发给仍在Exact-only阶段的新reviewer。全部selector函数可完全nonlinear。

## 1. 少量缺项排除同坐标groups的支持相交

给Exact(A)的任意ℓ、B，令N=q^t。对不同g,h，设z是g_i=h_i的坐标数。其支持若相交，则在这些z个坐标必须有ℓ_i(g)=ℓ_i(h)，每个这样的坐标有q种(a_i,b_i)；其它t−z个坐标因为g_i≠h_i而各有唯一解。因此非空支持交集精确有q^z项。

每group至多遗漏D项，所以如果q^z>2D，这个交集无法全部由两组遗漏项覆盖，必有某resource同时在B_g和B_h，违反不交。

当2D<q时，只要z≥1就有q^z≥q>2D。因此任何两组若某一group坐标相同，它们所选states的支持必须不交。这里严格使用2D<q；等号下不能推出此结论。

## 2. 资源fibers大小与必须删除的交点计数

对每resource x，令F_x={g:x∈S_(g,ℓ(g))}，k_x=|F_x|。第1节说明F_x中任意不同groups在每一坐标都不同，故k_x≤q（只看第一坐标的互异性即可）。

另一方面，每g恰有(q−1)^t个h在所有坐标都与它不同；每一对这样的g,h无论ℓ如何，都有唯一共同resource。所有其它不同group对没有支持交点。因此

Σ_x binom(k_x,2)=N(q−1)^t/2。

为使B_g不交，在每个k_x≥1的resource上，至多一个group保留该项，至少k_x−1份incidence选择被遗漏。所有groups的总遗漏数≤ND。用k_x≤q得

N(q−1)^t/2
 =Σ_x k_x(k_x−1)/2
 ≤(q/2)Σ_(x:k_x≥1)(k_x−1)
 ≤(q/2)ND。

约去N/2，得到D≥(q−1)^t/q。这是Exact(A)，对全部nonlinear ℓ与任意partial subsets成立。

## 3. 无约束D*与actual界

记a=ceil(q/2)、b=ceil((q−1)^t/q)。若最优整数D*<a，则2D*<q，适用(A)并给D*≥b。因此不可能D*同时小于a与b，故D*≥min(a,b)，即Exact(B)。

一般normalized flat恒等式在此可逐job核对：给实际C<2，每resource至多一unit，取每group实际selector所在state的exports B_g，其private负载2−|B_g|/q^t≤C，得V*≥2−C。C≥2时目标下界≤2平凡。反向每partial B都能把selected jobs对应导出、全部其它incidences留private，得2−V*的完整actual。故OPT=2−V*=1+D*/q^t，包括全部未选state jobs；于是得到Exact(C)的一般actual下界。

## 4. q3,t2的解析闭合

q3,t2时a=ceil(3/2)=2，b=ceil(4/3)=2，所以D*≥2。前一独立recoupling Exact/Proof的cyclic函数ℓ_1(g)=g_2、ℓ_2(g)=g_1，有奇异a满足a_1a_2=1，恰2个；其余9−2=7个a每组都对应独有resource。只取这7个非奇异a对应的resources，即得每组7项且全局不交，D*≤2。

因此D*=2，V*=7/9。把每组selector放这个cyclic state，导出其7件selected incidences，余2件留private，未选states全留private：selected private负载1+2/9=11/9，其它private1，resource≤1。一般actual下界也为11/9，故无约束OPT=11/9。未使用MIP不可行性或未经验证的solver证书。

## 5. 量词与复杂度

本证明不调用ℓ的低次数、仿射或coordinatewise性质；唯一小缺项条件是(A)明列的严格2D<q。若2D≥q，支持中同坐标group对可以相交，k_x≤q便未证明，不能继续套用第2节计数来声称所有q,t全局affine最优。

q3,t3所得一般界只给D*≥2，而cyclicD3，上述计数未排D2。构造与所有给定分配/actual的回算按显式q^(3t) incidence规模及O(tlogq)有理位长计，没有poly(t,logq)输出声称；无近二源hardness或求一般无约束最优算法。
