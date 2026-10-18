# q元 affine 菜单任意选态的fiber缺项合同：Exact v2

ID: UM-QARY-AFFINE-MENU-NEAR-FULL-DEFICIT-v2。
作者 boss11 内部 typed_edge_gap，2026-10-18。v1原字节保持；本v2另冻一般fiber/全局缺项不等式及其q3,t3后果。先仅交Exact供独立攻击，不附作者Proof；不再扩逐个数值探针。

## 1. 完整对象

q≥2为prime power，使用给定标准F_q表示；t≥1为整数，N=q^t。groups为全部g∈F_q^t，resources为全部(a,b)∈F_q^t×F_q^t。每group有全部indexed states ℓ∈F_q^t，支持

S_(g,ℓ)={(a,b):b_i+g_i a_i=ℓ_i，对全部i成立}。

每state恰N项，各private权为普通有理数1/N，总质量1。任意selector选择函数ℓ(g)可看g的所有坐标且可完全nonlinear。每group领取任意B_g⊆S_(g,ℓ(g))，所有B_g两两不交；partial subsets本身没有product或线性限制。

普通actual P：每state一private机，每resource一R；每group恰一件selector，只能在自己全部state private机时间1。每state每resource一件独立incidence job，只有自身private上的1/N及该唯一R上的1两个有限端；其余∞，无其它jobs、预载、资格或约束。所有未选states的jobs也都必须执行。

令m*为使每组至少领取m项的最大整数m，D*=N−m*，V*=m*/N。普通无约束actual最优记OPT_q,t。整数D满足0≤D≤N，讨论任何每组|B_g|≥N−D的给定allocation。

## 2. Concurrent fiber及精确projection合同

固定任何resource x=(a0,b0)，F_x={g:x∈S_(g,ℓ(g))}，k_x=|F_x|。也允许取任意非空F⊆F_x，记k=|F|。对J⊆[t]，π_JF为投影到这些group坐标的集合；空投影π_∅F恰一枚空tuple。

(A) 对每个上述非空concurrent family F，精确有

|⋃_(g∈F)S_(g,ℓ(g))|=Σ_(J⊆[t])(q−1)^|J|·|π_JF|。

且任何每group缺≤D的allocation都满足

kD≥Σ_(J⊆[t])(q−1)^|J|·(k−|π_JF|)。

这个式子不要求D很小；F的concurrency是必要的明示前提，不能对任意非concurrent子family套用第一条恒等式。

(B) 定义对整数1≤k≤N

H_(q,t)(k)=(k−1)+Σ_(j=1)^t binom(t,j)(q−1)^j·max{k−q^j,0}。

则每个非空fiber大小k_x均满足 H_(q,t)(k_x)≤k_xD。定义

K_(q,t)(D)=max{1≤k≤N:H_(q,t)(k)≤kD}。

集合非空（k1总合法）；因此每个fiber k_x≤K_(q,t)(D)。没有把H的粗投影界声称为每个k都可同时达到。

## 3. 全局缺项必要条件

(C) 对任意ℓ、任意每组缺≤D的partial allocation，必有

D·K_(q,t)(D)≥(q−1)^t。

此式允许任意D∈{0,...,N}，没有2D<q前提。它是实际可行性的必要条件，不是充分条件或求最优分配算法。

v1另有的严格近满合同继续保持原域与原字节：若2D<q则D≥(q−1)^t/q；v1给q3,t2的无约束V*=7/9、OPT=11/9。本v2不把v1的严格阈值改成等号，也不声称(C)单独包含v1所有参数的强度。

(D) q=3,t=3时，(B)/(C)排除D≤2；明确cyclic选择ℓ_i(g)=g_(i+1)可给全部27组各24项。因此无约束、允许所有nonlinear selectors的实例精确有

D*=3，V*=24/27=8/9，OPT_3,3=10/9。

actual结论包含全部原jobs的上界调度与任意完整调度下界，不把partial allocation当作全部jobs已经执行。这个端点是解析结论，不依赖MILP返回或有限枚举。

## 4. 位复杂度与范围

P有N groups、N² indexed states/private机、N² resource机、N³ incidence jobs与N selectors；sparse finite资格2N³+N²。权1/N位长O(tlogq)。构造、给定见证回算及达到(D)的实际见证按显式总输入位长polynomial，不声称poly(t,logq)输出规模。

H/K是有限整数表达式；H(k)/k随k不减，可用整数有理比较计算K，不需枚举任何候选selector函数。这个计算只给必要缺项下界，不解决一般nonlinear最优。

本页不声称cyclic/affine在全部q,t的unrestricted域最优，不提供normalized tiny-gap困难性源，不免费施加全fiber或block-fiber一致性。后续承重仍是普通实际P中的真正一致性机制或真实复杂性源；标准finite-grid投影计数与matching不包装原创。
