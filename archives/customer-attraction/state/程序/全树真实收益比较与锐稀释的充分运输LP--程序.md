---
id: customer-attraction/full-tree-real-payoff-comparisons-sharp-dilution-sufficient-transport-lp
kind: program
type_tag: 程序
title: 全树真实收益比较与锐稀释的充分运输LP
status: full-source-contract-and-sufficient-certificate-reconstructed-no-run
truth_status: sufficient-free-payoff-vertex-relaxation-not-counterexample-search-or-universal-half-proof
review_level: full5470source-current-informed-algebraic-and-model-review
scope: 正整数m,p；一份完整有序历史策略/真实叶；非负客户类型的收益顶点及同动作锐稀释；数值LP无精确恢复
summary: 自底向上逐历史随机破平局生成一份SPE，真实IC和全类型锐稀释形成非负弧；matx≤goal可充分推出βW−比较覆盖≥0，但程序只输出浮点β，失败或大于2不反half。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-acd97406d8c4409d962eab2adcdc520c/continuation_transport/gain_transport.py
---

# 全树真实收益比较与锐稀释的充分运输LP

5470B源码全部六函数及main全文，size/SHA/blob核真；原件见[证据](../../tools/evidence/gain-transport-and-workspace-mathematics-primary/README.md)。没有相邻本批原报告，不虚构搜索结果、失败实例或运行成功。本轮0原导入/CLI、0新LP/DP/IC/随机探索/数学checker；以下给源码所对应充分证书的完整数学解释。

## 有限单位模型与一份真实全树

取m,p≥1，标签0,…,p−1共同可选，允许重复与全部有序历史平局。非空兴趣mask的整数w_S≥0代表互异单位客户。终局z中选a的某位收益

$$F(a,z)=\sum_{S\ni a}\frac{w_S}{\sum_{b\in z}\mathbf1_{b\in S}}.$$

该辅助求值只在a实际出现在z时合法，分母正；代码没有为任意缺席a调用定义通用查询利润。零权重类型/全零客户允许，脚本没有按OPT0跳过。

`full_tree`从depth=m−1逆到0，逐个遍历range(p)^depth的所有**有序历史**h。每个行动a的终局在末位是h+a，其余是已经固定的孩子leaves[h+a]；精确Fraction求当前收益，rng在全部最大者中任选规定动作σ(h)，保存leaves[h]。孩子完整策略已固定，当前选择真正最佳回复，所以逐层逆归纳构成一份完整纯SPE。它不导入规范全集solver，也不枚举全部SPE；同计数不同有序节点可各自破平局，全部离轨节点均定义。

`run`为每个非空mask1,…,2^p−1独立取0…8整数权重，每个输入生成上述一张σ。源接口是带标签目录，未检测同覆盖标签或空主题；若需严格集合目录，应逐输入检查，或按[覆盖商定理](../等价/覆盖等价标签的完整策略商--等价.md)重新构造保路径策略，不能直接删原动作表。这里的弧有效性只依覆盖与收益，允许标签别名本身不破推导。

## 收益顶点与真实比较弧

对每个非负整数终局计数q、Σq=m，及q_a>0，建顶点v=(a,q)，记其数值F_v=Σ_(S∋a)w_S/q(S)≥0。顶点数

$$V=p\binom{m+p-2}{p-1}.$$

在完整节点h规定s=σ(h)，真实规定叶q=count(leaves[h])；改a后按同σ真实叶r=count(leaves[h+a])（末位直接h+a），SPE恰给

$$F_{s,q}-F_{a,r}\ge0.$$

代码对应列e_(s,q)−e_(a,r)，保每个有序(h,a)标签；即使两历史得到相同边也不合并。选自身时源/目标同顶点，零列不加入。在σ/leaves一致的合法输入上，a≠s时标签不同，故恰有H(p−1)真实列，H=Σ_(d=0)^(m−1)p^d。

这不是冻结终局其它角色后的静态偏离，也不把未知孩子随查询重新挑有利SPE。外部调用`transport_lp`须提供同一完整σ的真实leaves；函数没有自行核验两者一致或σ全IC，正常`run`由full_tree保证。

## 同动作稀释的全类型锐系数

同一a的两个合法顶点(a,q)、(a,r)，q_a,r_a>0，源码穷尽所有S∋a定义

$$\kappa(a;q,r)=\max_{S\ni a}\frac{r(S)}{q(S)}.\tag{1}$$

各分母≥1，全标签S给比1，故1≤κ≤m。逐类型1/q(S)≤κ/r(S)，乘非负w_S相加即得

$$\boxed{F_{a,q}\le\kappa(a;q,r)F_{a,r}.}\tag{2}$$

最大值类型若独有正权重即取等，所以κ是所有非负客户类型上的最小统一系数；不是只对本次随机正支持锐，也不是可任意选的缩放参数。代码列为−e_(a,q)+κe_(a,r)，所有同动作有序顶点对i≠j均加入；`include_dilution=False`可由函数调用关闭，但CLI没有这个开关，run默认启用。

每个a有T=binom(m+p−2,p−1)个顶点，故稀释列pT(T−1)。默认m3p3时H13、V18、真实列26、稀释列90，再加一β列，总117列。这些是代码的有限结构计数，非本轮执行统计。

## mat x≤goal为何是充分付款

对一份任意m标签比较组合，其计数o；根实际计数r。覆盖的客户预算恒等式给W_o=Σ_a o_aF_(a,o)、W_r=Σ_a r_aF_(a,r)。令c_j为上述真实或稀释列，均满足c_j·F≥0。程序令goal=−o（放在对应收益顶点），附β列−r，非负变量x_j、β，最小化β并约束

$$\sum_jx_jc_j-\beta r\le-o
\quad\text{逐顶点坐标}.\tag{3}$$

也就是残余b=βr−o−Σx_jc_j≥0。因F≥0，

$$\boxed{\beta W_r-W_o=\sum_jx_j(c_j\cdot F)+b\cdot F\ge0.}\tag{4}$$

残余坐标是自由收益顶点的非负性，不是新客户流或重复收取玩家利润。(4)是真实全IC、通用稀释与顶点非负的一个充分非负组合。LP不读随机weights，只有σ/leaves、m/p及比较o；若有精确证书，它对σ满足这些全IC的整个客户重数锥有效，不只对生成σ的原输入。

`run`枚举全部combinations_with_replacement(range(p),m)，共binom(m+p−1,m)个比较标签多重集，**不事先假定哪个在该策略锥上最优**。参数名optimum及内部opt是被测试组合，不是已经算出的OPT。如果每个组合均有精确β≤2证书，便对该固定σ锥得OPT≤2W。各组合可用不同非负弧乘子；代码没有证明所有完整σ都如此。

## 为什么失败不产生half反例

LP把F_v当自由非负变量，只保真实比较和两两同动作稀释，未保所有顶点来自**同一**非负客户资料的精确联合关系。[交集矩表示](../定理/有限阶交集矩的全收益表示与布尔正性--定理.md)将每个F_v和IC写成同一低阶多项式，其完整客户正性锥/Farkas余项包含这种放松没有全部使用的信息。

因此此模板在β2不可行或最优β>2，至多提示模板付款不足；自由F分离点未必有非负客户实现，更未必是原全树SPE。连浮点LP本身都须精确复核，不能直接把result.fun称真实OPT/W或把失败weights/σ称half反例。反过来，线性span/SCC表示存在也不自动提供所需非负弧乘子，不能因所有行落入D维空间就断言(3)可行。

## 数值实现、早停与报告缺口

真实列/κ先以Fraction保存，随后统一转float构造SciPy sparse csc_matrix。HiGHS求解非负变量LP；代码没有有理恢复x/β、精确核(3)残余或保存完整flow证书。即使result.success且fun≤2，也只是数值发现，不是已经认证(4)。判“失败”实际用fun>2+10⁻⁷，故某个略大于2的数值还可能被记录为未触发；不把这个容差当严格half保证。

默认run(seed1701,cases50,m3,p3)，每张σ测十个比较组合。遇result不成功则value=None，或value>2+10⁻⁷，立即返回；failures最多一项，保存case、portfolio、beta、root、weights及全部σ动作。`cases_completed=case+1`包括当前**未测完所有组合的失败case**，不是已完成全部组合的游戏数。maximum只在此前未触发行中更新，可能为None，也不含本失败项，不是完整任务的最大最优β。正常结束才返回cases数量、最高已记录值和空failures。

`transport_lp`返回result/vertices/精确columns/labels供调用者检查，但run输出不保存它们或result.x，只留浮点β与输入；未来认证需另保存/有理重构流、β及全部精确残余。当前本批没有冻结原报告，不从默认50×10计划虚构500次LP成功、失败样本或耗时。

CLI有main保护，接受--seed/--cases/--players/--topics，向stdout打印缩进JSON，不写文件。没有检查参数正性；数学合同m,p≥1、cases非负，非法值可能使递归或root访问失败，不能把无输入验证当一般边界已处理。导入定义不会自动run，但会导入NumPy/SciPy；本轮没有导入。外部依赖为linprog和csc_matrix，无项目模型、作者审计、规范求解器。它只是一条可复用的充分证书发现接口，尚无普遍half或当前运行证据。
