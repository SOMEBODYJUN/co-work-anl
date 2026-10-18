# q元 affine 菜单任意选态的近满缺项障碍：Exact v1

ID: UM-QARY-AFFINE-MENU-NEAR-FULL-DEFICIT-v1。
作者 boss11 内部 typed_edge_gap，2026-10-18。不同于前一recoupling Exact的量词：本页不要求selector函数线性或按坐标分解。先冻完整陈述，不附作者Proof；仅scratch，不以求解器结论代替证明。

## 1. 完整对象

q≥2 为prime power，给标准F_q表示；t≥1为整数。groups为全部g∈F_q^t，resources为全部(a,b)∈F_q^t×F_q^t。每group有全部indexed states ℓ∈F_q^t，state支持

S_(g,ℓ)={(a,b):b_i+g_i a_i=ℓ_i 对所有i成立}，

恰q^t项，各权为普通有理数q^(−t)，总质量1。任意选择函数ℓ(g)可依赖g的全部坐标，可完全nonlinear。

每group选一个ℓ(g)和任意partial subset B_g⊆S_(g,ℓ(g))，跨groups的B_g两两不交。定义m*为最大可使每组|B_g|≥m的整数m；D*=q^t−m*为最优最大缺项数，V*=m*/q^t为无约束菜单值。

完整ordinary P与前一Exact一致：每state一private机，每resource一R；每group恰一件unit selector，可去自己全部states的private机。每state中每resource一件独立incidence job，只在自身private耗时q^(−t)或该唯一R上耗时1；其余∞，无其它jobs/预载/资格。所有未选state jobs也必须执行。记其无约束普通实际最优为OPT_q,t。

## 2. 待独立攻击的 Statements

(A) 对任意上述q,t，任意选择函数ℓ与partial allocation，若整数D≥0满足每组|B_g|≥q^t−D且2D<q，则必有

D≥(q−1)^t/q。

这里2D<q是严格阈值；没有把等号2D=q免费纳入合同。D不必是最优D*。

(B) 对任意q,t，无约束最优缺项数满足

D*≥min{ceil(q/2),ceil((q−1)^t/q)}，

等价地

V*≤1−min{ceil(q/2),ceil((q−1)^t/q)}/q^t。

这与前一recoupling Exact的cyclic下界可并用，但没有证明两者对所有q,t相等。

(C) 实际全部jobs满足

OPT_q,t≥1+min{ceil(q/2),ceil((q−1)^t/q)}/q^t。

特别q=3,t=2时，本页(A)/(B)给D*≥2；前一Exact中明确cyclic选择可达D=2。因此该**无约束**普通实例的值解析精确为

D*=2，V*=7/9，OPT_3,2=11/9。

这是任意nonlinear states及任意partial exports下的解析上/下界，未依赖小MILP的不可行性返回。

## 3. 大小及准确范围

q^t groups、q^(2t) indexed states/private机、q^(2t) resource机、q^(3t) incidence jobs、q^t selectors；sparse finite资格2q^(3t)+q^(2t)。权q^(−t)位长O(t log q)。对象及给定分配/完整actual的分析按显式实例位长计费，不声称poly(t,logq)输出大小。

本页只给近满值的必要缺项数与一个q3,t2全局精确端点。q>2任意t的无约束nonlinear最优一般仍OPEN；尤其q3,t3时本障碍只给D*≥2，cyclic可达D=3，两者之间未关闭。它不提供normalized tiny-gap困难性源、不排所有tensor操作，也不把全局selector一致性作为免费物理约束。
