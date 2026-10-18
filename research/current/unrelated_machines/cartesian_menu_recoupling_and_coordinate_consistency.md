# 笛卡尔菜单的反向放大与逐坐标一致性差距

读取目的：攻击把一个常数 NO gap 裸取笛卡尔积就放大到近二的路线。这里所有 state 本身均为纯 Cartesian 支持，但乘积 group 可以重新选择整个 state；这项普通调度原生具有的自由度足以反转所望 NO 放大。后半页精确计算增加逐坐标一致性后的资源配额，定位尚须实际实现的约束。

## 1. 完整普通调度对象与精确主张

**ID / Version：`UM-NORMALIZED-FLAT-CARTESIAN-TENSOR-REVERSE-AMPLIFICATION-v1`。**

**Objects / Domain / Definitions。** 对整数 \(t\ge1\)，置 \(D=2^t\)。Groups 为 \(g\in\mathbb F_2^t\)，每组有全部 indexed states \(\ell\in\mathbb F_2^t\)，真实资源为 \((a,b)\in\mathbb F_2^t\times\mathbb F_2^t\)。第 \((g,\ell)\) 个 state 的支持是

\[
 S_{g,\ell}=\{(a,b):b_i+g_i a_i=\ell_i\quad(1\le i\le t)\}.
\]

每个 \(a\) 恰给一个 \(b\)，故每 state 恰 \(D\) 个 distinct resources，各项 private 权 \(1/D\)，质量恰1。加法均模2。基例真实资源 \(u=2a+b\in\{0,1,2,3\}\)，两组的 states 分别为

\[
 g=0:\quad\{0,2\},\{1,3\};\qquad
 g=1:\quad\{0,3\},\{1,2\}.
\]

上述 \(t\) 维对象恰为此基例支持的逐坐标 Cartesian 积，没有把共享资源私有化。

完整 ordinary UM 矩阵 \(P_t\) 如下。每资源一台 \(R_{a,b}\)，每 indexed state 一台 \(M_{g,\ell}\)。每组一件 selector \(J_g\)，只可在本组全部 \(M_{g,\ell}\) 耗时1。每 \((g,\ell,u)\) 且 \(u\in S_{g,\ell}\) 一件不同 incidence job \(I_{g,\ell,u}\)，只有两个有限端：在 \(M_{g,\ell}\) 耗时 \(1/D\)，在 \(R_u\) 耗时1。全部未述时间为 \(\infty\)，没有预载或额外任务。全部 indexed states 的 jobs 均实际存在且必须执行。

\(V_t\) 是每组选择一个 state 及其任意子集 \(B_g\subseteq S_{g,\ell(g)}\)、各组子集全局不交时，\(\min_g |B_g|/D\) 的最大值；允许资源不用。并未要求 \(B_g\) 为 Cartesian 子集，也未限制 \(\ell(g)\) 如何依赖整个 \(g\)。

**Exact Statement / Quantifiers / Conclusion。** 对每整数 \(t\ge1\)，

\[
 \boxed{V_t=1-2^{-t}},\qquad
 \boxed{\operatorname{OPT}(P_t)=1+2^{-t}=2-V_t}. \tag{1}
\]

给出全部原 jobs 的确定性具体达界调度，以及任意完整实际调度的下界。特别 \(V_1=1/2\)，但 \(V_t\) 不是 \(V_1^t\)，反而趋近1。

**Assumptions / Scope。** 输入是上面完整显式族，不是任意 UM；\(t=0\) 不在域。只有该明示裸 Cartesian 操作受此反例约束，不排除其它 product、增加真实一致性约束或特定 source image 的归约；没有复杂性假设或 hardness 源。

## 2. 任意状态选择必有一枚真实冲突

任取 \(g\) 及其补组 \(h=g+\mathbf1\)，二者不同。无论选择什么 \(\ell(g),\ell(h)\)，共同资源逐坐标的方程唯一解为

\[
 a_i=\ell_i(g)+\ell_i(h),\qquad
 b_i=\ell_i(g)+g_i a_i.
\]

所以两个完整支持总是恰交一个资源。两组不能都领取各自全部 \(D\) 项，至少一组的整数子集大小至多 \(D-1\)。这对任意部分分配成立，给 \(V_t\le1-1/D\)，没有用仅针对固定 states 的资源池计数代替全状态上界。

## 3. 跨坐标重选给出达界分配

坐标循环编号，令 \(g_{t+1}=g_1\)，选择

\[
 \ell_i(g)=g_{i+1},\qquad
 B_g=\{(a,b):a\ne\mathbf1,\ b_i=g_{i+1}+g_i a_i\ \forall i\}. \tag{2}
\]

这仍是原列表中的一个纯 Cartesian state，只是决定其标签的函数跨坐标。每组恰领取 \(D-1\) 项。

若 \((a,b)\) 同时被 \(g,h\) 领取，置 \(\delta=g+h\)，得到 \(\delta_{i+1}=a_i\delta_i\)。由于 \(a\ne\mathbf1\)，某个 \(a_i=0\)；从此沿环推出全部 \(\delta_j=0\)，故 \(g=h\)。所有 \(B_g\) 全局不交，得到相反不等式并闭合 \(V_t\)。\(t=1\) 时循环就是自身，仍保留 \(a=0\) 的一项，推导有效。

## 4. 全部原任务的实际最优值

上界调度把 \(J_g\) 放 \(M_{g,\ell(g)}\)，只将该 selected state 中对应 \(B_g\) 的 \(D-1\) 件 incidence 真正送到各自资源机；其余所有 incidence 均留原 private 机，包括所有未选 states 的全部 jobs。Selected private 负载恰 \(1+1/D\)，未选 private 恰1，资源机至多一件 unit，故峰恰 \(1+1/D\)。

任取完整实际调度，若峰 \(C\ge2\)，下界平凡成立。若 \(C<2\)，每资源至多接一件 unit incidence。取任意补组，令其 selectors 的实际目的 states 为 \(\ell(g),\ell(h)\)。§2 的共同资源对应两件不同原 jobs，不能同时外送到该机；至少一件留在自己的 selected private 机，与 selector 合计 \(1+1/D\)。其它未选 state 的外送只会进一步占用资源，不破坏这个下界。由此对全部实际调度闭合(1)，无需把 partial allocation 当成已经执行完所有 jobs。

## 5. 精确规模、位复杂度与否定范围

有 \(D\) groups、\(D^2\) indexed states/private machines、\(D^2\) resource machines、\(D^3\) incidence jobs 及 \(D\) selectors。有限处理时间条目恰 \(2D^3+D^2\)；dense 矩阵若要求则有 \((D^3+D)2D^2\) 条目。权 \(1/D\) 和标签位长 \(O(t)\)。逐项生成矩阵、(2)及全 jobs 调度，并按整数 \(D\) 单位回算全部负载，均对显式实例总编码长度多项式；不声称输出 \(8^t\) 个 jobs 可在 \(\operatorname{poly}(t)\) 时间完成。

每真实资源在每个 group 的菜单并集中恰出现一次，故整个菜单的资源跨组度为 \(D\)，不是固定degree3。后接已知精确[三态/度三正规形](degree_three_weighted_menu_cube_embedding.md)可保这个已经下降的实际 OPT，却不会自行恢复被裸乘积丢掉的 NO gap。

此族只否定这里“基例 \(V\le\eta\) 自动推出裸 product \(V\le\eta^t\)”的通用断言：\(\eta=1/2\) 已相反趋1。它不同于[旧终端 palette 的对齐产品](ternary_rainbow_subtree_exact_hardness.md)因 YES 完备性失真的机制；这里是 NO 的跨坐标重选逃逸。没有证明所有 tensor 不能放大。

**Dependencies / Evidence / Counterevidence / Status / Related Files。** 仅需§1显式定义、模2环方程与不可分资源，证明自足；不依赖有限测试或外部近似后端。作者冻结 Exact/Proof、rank 的 Exact-first 独立重构和实际作者读后均保持原字节；root实际读取并独立核全对象。最终章节审查见[实际审查](../../reviews/unrelated_machines/cartesian_menu_reverse_amplification_review.md)。数学完整、无 standing fatal；外审和全球新颖性未认证。§8的实现仅 audit_only，非一般 UM 后端，UM-TARGET-v1 仍 OPEN。

## 6. 额外逐坐标一致性下的精确配额

**ID / Version：`UM-COORDINATE-OBLIVIOUS-CARTESIAN-MENU-QUOTA-v1`。**

**Objects / Domain / Definitions / Quantifiers。** 同§1的 \(t\ge1,D\)、groups/resources/states，另给任意固定函数 \(f_i:\mathbb F_2\to\mathbb F_2\)，强制所有 groups 同时选 \(\ell_i(g)=f_i(g_i)\)。函数可以任意，但不许依赖 \(g\) 的其它坐标。Partial \(B_g\) 仍为所选 state 的任意子集并全局不交。对每一组固定 \((f_i)\)，乃至进一步优化这些函数，最优值都为

\[
 \boxed{V_{\rm obl}(t)=\frac{\lfloor(3/2)^t\rfloor}{2^t}}. \tag{3}
\]

可确定性按显式实例总位长多项式找出每组恰 \(k=\lfloor(3/2)^t\rfloor\) 枚真实资源的 bundles。**这额外限制的是选择语义，不是已经给普通 UM 加上的物理约束。**

证明：每个坐标的两条所选线各2项、恰交一枚 \(c_i\)，另各有一枚独占项 \(e_i(0),e_i(1)\)。全体 groups 遍历使支持并集恰为这三个符号的积，大小 \(3^t\)。任意 disjoint partial allocation 的最小基数 \(s\) 因而满足 \(Ds\le3^t\)，给出整数上界 \(s\le k\)。

对下界，把并集里每项资源按其兼容 groups 均分：若它有 \(h\) 个 common 坐标，恰邻接 \(2^h\) 组，每条邻边给 \(2^{-h}\)。每资源总供给1，每个 group 的分数总量恰 \((1+1/2)^t\)。因此任意 group 集合 \(A\) 均满足

\[
 |N(A)|\ge (3/2)^t|A|\ge k|A|. \tag{4}
\]

这验证了所有 Hall 子集，而非只检查全体 group 的 union。把每 group 拆成 \(k\) 个同邻接槽，任意槽子集涉及的 groups 为 \(A\)，其槽数至多 \(k|A|\le|N(A)|\)，故普通 Hall 给覆盖全部槽的整数 matching。每组恰 \(k\) 项共同不交，证明(3)。半分数仅证 Hall，未拆开最终物品。

由于 \(k\le D\)，槽数不超过 \(D^2\)，边数不超过 \(D^3\)，确定性增广路可按全部显式菜单大小多项式构造。\(k\) 用整数除法 \(\lfloor3^t/2^t\rfloor\) 精确计算；不以浮点取整或按数值时间展开。\(t=1\) 给 \(k=1,V=1/2\)，无退化漏洞。

## 7. 两种语义之间真正缺失的技术

(3)与 \((3/4)^t\) 相差小于 \(2^{-t}\)，所以逐坐标一致的值趋零；同一裸产品的无约束值却由(1)趋1。二者不能在解码里互换。任何声称把本族任意高值 product allocation 修复为满足该逐坐标一致性的 allocation、且保值系数统一大于0的合同，都被这两个精确值排除。此逻辑后果不否定允许更多状态/资源/任务的新归约。

需要实现的是：在真实普通矩阵中，低负载调度必须给出足够的一致性，且 YES 调度仍可行；不能在 source decoder 里免费要求 \(\ell_i(g)\) 只依赖 \(g_i\)。现有[占位胶合](unit_presence_two_witness_sharp_gluing.md)又只限制特定裸 presence 复制合同，不排除全部身份接口或共同源相关 decoder。这里没有构造所需物理 gadget，也没有提供近二 NO 源。

**Assumptions / Scope / Dependencies / Evidence / Counterevidence / Status / Related Files。** 固定函数的语义约束、有限不可分资源和 Hall 整数性是全部前提；(3)自足，不以§1的无约束最优值为必要前提，对照及保值限制才共同用两项 Claim。General reviewer 先只据消息内精确陈述独立重构，之后实际核作者 Exact/Proof，与 root 独立证明一致；最终§6–7范围审查见[实际审查](../../reviews/unrelated_machines/coordinate_oblivious_cartesian_menu_quota_review.md)。没有对应软件或有限枚举，全球新颖性/外审未认证，无 standing fatal；一般 UM 目标及其反面未解。

## 8. 有限原矩阵审计与读取边界

审计代码：[audit_normalized_flat_cartesian_tensor_reverse_amplification.py](../../../tests/audits/unrelated_machines/audit_normalized_flat_cartesian_tensor_reverse_amplification.py)。它从原资源标签筛全部状态支持，生成完整稀疏矩阵，再按整数 \(D\) 单位检查所有任务资格、各机负载和完整 assignment。冻结见[evidence/runs](../../../evidence/runs/unrelated_machines/cartesian_menu_reverse_v1/summary.json)。

| t | 原 jobs | 机器 | 有限条目 | 完整见证峰 | 所有有序补组/state 对 |
| --- | --- | --- | --- | --- | --- |
| 1 | 10 | 8 | 20 | 3/2 | 8 |
| 2 | 68 | 32 | 144 | 5/4 | 64 |
| 3 | 520 | 128 | 1088 | 9/8 | 512 |
| 4 | 4112 | 512 | 8448 | 17/16 | 4096 |

仅 \(t=1\) 另对完整原矩阵穷举1024份 assignments，精确 OPT=3/2；\(t\ge2\) 不做最优枚举。root 未导入审计构造器，另从冻结全部原矩阵身份与有限端重新核4710个 jobs、全 load，并独立重复 \(t=1\) 的1024枚举。原代码输出含完整矩阵/完整调度/交点，不靠删掉未选 state jobs 通过。

这些检查仅对应有限输入，graph 使用 checks，不作为一般(1)或(3)的 derives。代码只实现明示族的 audit_only，未实现受限函数匹配后端或一般调度算法。输出目录须全新；原冻结输出不覆盖。
