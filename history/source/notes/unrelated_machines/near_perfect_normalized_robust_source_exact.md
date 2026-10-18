# 近完美归一化 robust 菜单源的有理 LP 判别：精确陈述

冻结日期：2026-10-18。作者：current_hardness_sources。本文件仅给 Exact；证明另文件。内容不并进已冻结 v2 Exact，待独立攻击。全程 clone 外，不写共同仓库或 git。

## 对象

有限非空 groups G、n=|G|≥1；有限资源 U。每组有显式非空有限 indexed states A_g；state s 在 distinct 原资源上给二进制非负有理 p_gsu，总和恰1。未列项效用为0；显式零、unused resources、重复 indexed states允许。v_g(B)=max_s sum_{u∈B}p_gsu∈[0,1]。allocation指全 n 组两两不交的真实原资源 bundles，允许空bundle和未分配资源；没有额外coherence/AND/标签相容约束。

给二进制有理参数 0≤eta<1、0≤delta<1、0<gamma_hi≤1，满足

  (5/8)(1−eta) ≥ gamma_hi+(1−gamma_hi)delta。                (E)

参数可作为输入；复杂度按显式菜单与参数的合计总位长计，不按倒数数值展开。

## 两个分别成立的 promise

YES：存在 allocation 使至少 (1−eta)n 组质量一。

NO_≥：每个 allocation 均满足 #{g:v_g(B_g)≥delta}<gamma_hi*n。

另版 NO_>：将上述 ≥delta 改成 >delta。两种 NO 需分别按各自原阈值读取，不擅自互换源语义。

## Exact DECIDER

对 YES/NO_≥ promise，以及分别对 YES/NO_> promise，均有确定性总位多项式判别器。

具体判别器求如下明确有理 LP 的最大目标 L：每state变量 z_gs≥0、仅每正incidence变量 x_gsu≥0；每组 sum_s z_gs=1，每incidence x_gsu≤z_gs，每资源 sum_{g,s}x_gsu≤1；目标 max sum p_gsu*x_gsu。L≥(1−eta)n 判YES，否则判NO。这个 LP 总可行；它不是原positive-support unit-FSLP，不要求后者可行。算法无需源YES见证、未知OPT、NSW finder或任意实际unit配置列表。

(E) 允许等号。非整 (1−eta)n、gamma_hi*n 直接按真实整数count和有理比较解释。delta=0 的 NO_≥ 空类保留其退化语义，NO_> 是另一个promise。promise外LP输出无额外语义。

## 明确统一子域

所有满足

  0<gamma_hi≤delta≤3/8，0≤eta≤1/40

的输入参数满足(E)，因此该全域均可判别；包括 eta=1/40、delta=gamma_hi=3/8 的三重等号。

## 复杂度后果和范围

若某NP完全语言确定性Karp-reduces到这个**完整显式normalized promise**，则P=NP。若归约随机，结论只能按实际YES/NO成功事件给出相应NP⊆BPP等；本陈述没有提供任何这种归约。

这是否定一个明确源合同的困难性候选，不是general UM算法/困难性，不改变一般UM-TARGET-v1状态。不归一state、隐式指数菜单、额外真实共享jobs/coherence、仅控制完整sets/某一固定label选择的NO均在域外。whole-class gated 13/8 ratio不是本陈述的前提；本陈述只依一般福利LP的>5/8舍入性质。
