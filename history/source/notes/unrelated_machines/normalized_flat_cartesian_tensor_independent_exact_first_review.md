# 裸 Cartesian 菜单反向放大的独立 Exact-first 重构

审查者：boss11 内部 rank_deficiency_fee。

只读取 `normalized_flat_cartesian_tensor_reverse_amplification_exact_v1.md`，SHA256 `60299e46c9677b6fbfc94ac866bfe317151c83154c1fe7c14510eedc84050bac`。未读取作者 Proof、root 或其它审查者推导。本记录先冻结独立结论，供后续读后核验对照。

## 独立结论

对每个整数t≥1，冻结Exact的(A)、(B)、(C)均成立：

    V_t=1−2^(−t)，
    OPT(P_t)=1+2^(−t)=2−V_t。

下面给一般参数的明确分配与全部原jobs调度，及任意partial subsets/实际完整调度的下界。当前没有standing objection；未认证全球新颖性或一般tensor不可能性。

## 1. 统一二进制记号

令n=2^t。每资源写成(a,b)∈F_2^t×F_2^t；第i坐标的原u_i等于2a_i+b_i，符合Exact的0,1,2,3表。group g∈F_2^t；state ℓ的支持是

    S_(g,ℓ)={(a,b):b_i+g_i a_i=ℓ_i，∀i}。

每个a唯一决定b，故每state恰n资源，每项权1/n，总和1。

## 2. V_t 的一般上界：任意state与任意partial subset

取任意group g及其逐位补向量ḡ=g+1^t。t≥1保证二者不同。无论给这两组选择什么state ℓ、ℓ′，联立方程得

    a_i=ℓ_i+ℓ′_i，
    b_i=ℓ_i+g_i a_i。

所以两完整支持总是恰交一个真实资源。

若某个合法不交分配的最小保留值严格大于(n−1)/n，那么每组的B_g都必须有n个资源：其大小是整数且≤n。即每组都保留所选state的完整支持。这与上述补group对的必交性质矛盾。

因此允许B_g任意非Cartesian partial subset也仍有

    V_t≤(n−1)/n。

此上界不是资源池总维数的粗计数，也没有假设各group的state选择逐坐标独立。

## 3. 达界分配：循环移位state和删去一个a向量

把坐标下标按t循环，设g_(t+1)=g_1。为每个完整group g选择

    ℓ_i(g)=g_(i+1)。

这仍是Exact列出的一个纯Cartesian state；只是选择函数允许使用其它group坐标，属于原对象明确允许的全state选择自由度。

该state中对每个a有资源b_i=g_(i+1)+a_i g_i。保留所有a≠1^t对应的资源，即

    B_g={(a,b):a≠1^t，b_i=g_(i+1)+a_i g_i，∀i}。

每组恰n−1枚资源。

证明它们共同不交：固定任意a≠1^t与b，选一个a_j=0的坐标。若(a,b)属于某个B_g，等式给g_(j+1)=b_j；再沿循环用

    g_(i+1)=b_i+a_i g_i

逐项确定全部其它g坐标。回到第j个等式时，因为a_j=0，该式已经满足，不产生另一自由度。因此对该(a,b)存在且仅存在一个g。尤其不同group不能同时拥有该资源。

故所有B_g是一个全局整数不交分配，得V_t≥(n−1)/n，与第2节相合。t=1也合法：循环移位就是ℓ(g)=g，保留a=0的一枚资源；两组选中的完整支持分别为{0,2}、{1,2}，分别保留0、1，V_1=1/2。

## 4. 全部原jobs的实际上界调度

对每group g把其selector放到M_(g,ℓ(g))。仅将该选中state的、属于B_g的n−1件incidence jobs分别送到其原resource machine；其它所有incidence jobs全部放自己的原private machine。这里包括：选中state未保留的那1件，以及全部未选indexed states的全部n件任务。

逐机器实际负荷：

* 被选private机：selector时间1，加恰一件1/n incidence job，合计1+1/n。
* 未选private机：其n件原incidence jobs各1/n，总和1。
* resource机：由B_g共同不交，至多一枚unit incidence job，负荷≤1。

全部n^3+n枚原jobs恰分配一次，所用端均为原矩阵端，故OPT(P_t)≤1+1/n。

## 5. 任意完整实际调度的下界

任取完整合法σ。若Cmax(σ)≥2，则当然≥1+1/n。否则每resource机至多一枚unit job。

每group的selector必须放某一原state机M_(g,ℓ(g))，其时间1。如果该选中state有任一件incidence job仍放private机，其负荷至少1+1/n，已经给所需下界。

若所有group的选中state都没有private incidence job，则它们全部n件都必须送各自原resource机。这样各组选中的完整state支持必须跨组不交，否则同一resource机有两个unit、Cmax≥2。但任取补group对都恰交一个资源，第2节已排除这种全支持不交。

故所有完整实际调度都有Cmax≥1+1/n，得到OPT(P_t)=1+1/n。此证明直接覆盖全部原jobs，没有将部分资源分配冒充完整调度，也不需要在C=2处错误假设unit独占。

## 6. t=1、精确规模和位复杂度

t=1时：2groups、4indexed states/private机、4resource机、8incidence jobs、2selectors；实际调度共有10jobs、8machines，所构造峰3/2。全部支持有2项，未选state jobs仍保留，不存在少算任务的matching假象。

一般t：n groups，每group n states，总private机n²；resource机n²；每state n incidence jobs，总n³；selectors n。每incidence有两条有限边、selector有限边总n²，故sparse有限时间条目恰2n³+n²。dense矩阵条目恰

    (n³+n)·(2n²)=(8^t+2^t)·(2·4^t)。

private时间1/n=2^(−t)位长O(t)。构造完整P、循环state选择、逐a生成B_g及给全部jobs写owner，都按显式输入规模多项式：完整P本身已经指数依t，不声称poly(t)。负荷回算可用整数任务数除n或精确有理部分和，位长受控。

## 7. 准确反候选范围

本例只否定Exact明示的裸Cartesian-menu操作下，一般的“基例NO V≤η推出乘积NO V≤η^t”。在η=1/2处已有V_t=1−2^(−t)，与所望2^(−t)反向。

资源跨group次数也随该操作增长：每个固定(a,b)对每个g恰属于一个state，因此属于全部n个group的完整菜单union。此操作没有保持degree3；不能据本族否定另有degree保持和一致性约束的产品或特定compiler image。不同tensor定义、额外跨坐标一致性与源hardness均不在当前证明范围。

这不是旧ternary palette机制的引用：独立构造直接用上述二进制循环方程及允许的任意partial B_g，原每state始终为所声明的纯Cartesian支持。
