---
id: customer-attraction/fixed-owner-net-diagnosis-exact-primal-dual-and-early-stop-scope
kind: program
type_tag: 程序
title: 固定归属NET诊断的精确原始对偶与早停范围
status: full-original-code-and-three-reports-reconstructed; no-new-execution
truth_status: exact-fixed-finite-LP-certification-method; no-universal-NET-budget
review_level: 全9406B代码、2011B说明、三JSON和六实际输入全文；显式有理推导；零导入及优化器
summary: 原程序在三个既存完整SPE上以同一实际Hall网络求NET及独立总价；浮点提案后Fraction核原始、对偶符号、stationarity及目标相等。仅first-owner，找到首个见证即停；不是所有matching、owner或普遍付款证明。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round4/shared/diagnose_net_existing.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round4/shared/diagnose_net_existing.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round4/shared/net_existing_diagnosis.md
---

# 固定数据、原策略与实际采购价格

本对象保全[9406B原代码](../../tools/evidence/existing-net-witnesses-and-exact-duals-primary/original/research/workspaces/customer-attraction/R-cd789330fc7141299ac491bbb3ffa420/round4/shared/diagnose_net_existing.py)的全部功能。它只读取指定名字的游戏JSON和完整策略JSON，不生成客户、策略、重数锥或新实例。模型为[单位客户共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)，不是静态Nash或计数策略压缩。重数展开为不同单位客户；标签次序与客户块次序决定报告的零基编号。

`diagnose(name)`从`examples/customer_attraction/<name>.json`与`evidence/certificates/customer_attraction/<name>.json`取数据，允许证书有`strategy`包装。动作dict的键集合必须等于全部长度小于m的有序合法history；`finish(h)`始终沿同一策略在真实改变后的history完成。每个节点、每个合法行动（含自身）比较单位均分收益。它不冻结后继，也不只检查actual。dict构造本身会覆盖重复键，没有独立重复记录断言；六个本批实际输入已全文读取，三策略分别6/259/21个不同节点。输入的`terminal_counts`、security和expected附字段并不被程序消费。代码不是任意坏JSON的通用验证器，不能把未写的正重数或标签范围检查算进其断言。

令实际叶Z、收益u、覆盖C固定。代码枚举全部可重复m主题多重集得到OPT及optimal列表，然后逐个多重集枚举其不同排列T。对每个最优客户x，owner固定为T中第一个含x的槽。取R=O\C、I=O∩C、G=C\O。

对于遗漏x、actual-prefix查询s=(i,a)，令B_s=finish(Z_<i,a)、D_s=u_i(B_s)，F_s(x)为B_s中覆盖x的future角色，c_s=1+|F_s|。原`price`返回整列角色费用向量，精确递归为

\[
 p^s_{jx}=\mathbf1_{j=i}\frac{u_i}{c_sD_s}
       +\frac1{c_s}\sum_{\ell\in F_s(x)}p^{(\ell,B_{s,\ell})}_{jx}.
\tag{EQUAL}
\]

只从R源开始，所以实际过去无人覆盖x；递归到达的主题仍含x，D_s>0。完整IC给u_i≥D_s。每步当前吸收1/c，向每个真实future coverer各送1/c，角色严格上升，单位源全部吸收。因此列总价v_x=Σ_jp_jx≥1。合流的current吸收先求和，再除同一个D_s购买唯一整主题IC；p只是其来源线性分拆，没有逐客户重权原IC。

这里没有选择最低价recipient，也没有任意合法重查主题：它把同额送到每个future规定动作。因此它是[自然Bellman路由](../算法/自然捕获路由的Bellman价格与Hall取消--算法.md)的一个固定可选规则，与[共同优先级自由重查](../定理/共同优先级下自由合法重查的终端吸收界--定理.md)的随机终端实验不同。不能给本代码附上那些扩张的最优性或world事件性质。

# 同一Hall网络上的两个有限优化

令I_i=u_i(I)、g_i=u_i−I_i=u_i(G)。每个I客户从owner向每个非owner实际coverer给容量1/c_Z(x)，同方向容量聚合为c_ab；每个R客户有取消变量0≤γ_x≤1，I边流0≤f_ab≤c_ab。角色等式为

\[
 \sum_{o(x)=i}\gamma_x+\sum_bf_{ib}-\sum_af_{ai}=g_i.
\tag{FLOW}
\]

所有角色式相加给Σγ=|G|。网络是[固定价格Hall定理](../定理/固定捕获价格的Hall缺额与共同付款对偶--定理.md)中的裸actual网络，没有局部δ或SOURCE-NET下界。终端可行域Γ是同一个rank base。

总价程序最小化−Σ_xv_xγ_x（边流目标0），再加Σv得到minΣv(1−γ)。另独立枚举全部2^m角色割，计算

\[
 r(S)=\min_J\{g(J^c)+c_I(J,J^c)+|S\cap Q(J)|\}.
\]

按v降序、单位编号升序打破平局，取greedy γ_x=r(S_k)−r(S_(k−1))。代码核每增量∈[0,1]、总和G、全部角色割的终端流可行条件，并核greedy费用等于独立LP最优值。`rank_price_layers`保存每一单位客户、列总价、前缀rank和缺额；它不是完整p_ix矩阵。一个向量同时取消全部嵌套价格层，没有每层重复领取G。

NET另加一个**无上下界的自由变量t**，求

\[
 \min t,\qquad K_i-\eta_i\le t,\quad
 K_i=\sum_xp_{ix}(1-\gamma_x),\quad
 \eta_i=I_i+\sum_{o(x)=i}\gamma_x.
\tag{NET}
\]

代码的第i不等式系数为−p_ix−1_(o(x)=i)、边流0、t系数−1，右边I_i−Σ_xp_ix；不是把t约束为非负。输出负margin可合法表示严格余量。Ση=W由同一FLOW保证。报告的γ、I边`flow`、K和η均来自NET原始点；`minimum_total_price`及`total_dual`来自另一LP，总价greedy另由rank层重构。总价原始tx没有原样输出，完整p矩阵亦未输出；不得称JSON独自含两份完整原始向量与矩阵。

# 原始/对偶确切相等为何足以证明固定LP最优

`exact_lp`先让NumPy/SciPy HiGHS选浮点点，然后将原始坐标及四组marginals分别用`Fraction(float).limit_denominator(10**8)`重构。它不是在容差内接受：重构后逐行等式必须恰等、不等式必须≤、每个有限cap变量必须0≤x≤cap。

记原问题min c·x，A_ub x≤b_ub、A_eq x=b_eq、有限变量0≤x_j≤U_j。对偶要求不等式乘子y≤0、等式乘子e自由、下界乘子l≥0、上界乘子h≤0，以及逐变量

\[
 c=A_{ub}^{T}y+A_{eq}^{T}e+l+h.
\]

自由变量t的l_t=h_t必须均0。于是对任意原始可行x，因乘子的符号，

\[
 c\cdot x\ge b_{ub}\cdot y+b_{eq}\cdot e+\sum_{j:\,U_j<\infty}U_jh_j.
\]

重构原始点达到该下界即为精确最优。代码核这些符号、每坐标stationarity及原始/对偶目标恰相等；不需要另查互补松弛才使此证明有效。无法有理重构、浮点失败或某断言失败会中止，**不是**精确不可行或一般NET反例。分母上限10^8也不是对全部输入的保证。

所有`assert`必须启用。该证明是源码实现的合同；本批未调用`exact_lp`、SciPy或原主入口，未把历史输出称成本批新PASS。[三实例计算](../计算/三个既存完整策略的NET见证与分层总价--计算.md)直接从实际输入、价格和显示原始点给出各有限值的解析核算，不依赖新增求解器事件。

# 全λ、首匹配及执行入口边界

固定p、T、owner时，NET有同一γ的精确判别是对**全部**λ≥0有h_Γ(M^Tλ)≥λ·d，其中M_ix=p_ix+1_owner、d_i=Σp_ix−I_i。λ全1仅判总价≤W；不能用这一个方向证明NET。成功的固定原始γ逐行满足NET，故当然同时覆盖所有λ；这里并未逐个扫描无限λ。NET margin的对偶是单位单纯形上最大分离量，与代码的有限行LP一致。

自由matching/owner是外层存在量词。原循环只考虑每个T的first-owner，不枚举所有合法owner，更没有FRAC；nobj≤0马上返回。三报告都只有一个optimal multiset、一个trial，其余不同排列未跑。若所有first-owner排列真走完仍无见证，返回的仅是`first-owner choices exhausted; unrestricted owners not diagnosed`，不能报一般NET失败。代码没有跨角色预算普遍证法、全人数扫描或固定规模专项。

源码有main guard：普通导入只导入标准库、NumPy和SciPy并定义函数，不自动诊断；`--help`在argparse退出前不诊断。真正CLI先`diagnose(case)`，再独占创建源码同目录`net_diagnostic_<case>.json`，不会覆盖既有报告；诊断失败不会写报告，若目标已存在则诊断算完后仍会因`open('x')`失败。ROOT固定为HERE.parents[5]，六真实输入需按原相对层级存在。stdout只打印非trials顶层及最后trial的五字段，不能当完整JSON。当前0源码import、0数学CLI、0LP、0策略重演；只做原字节/绑定/链接结构自查。

2011B说明原记2026-10-23内部诊断及不再扩样的研究停点。它只承重三个固定阳性见证，没有普遍NET、六人half、外部审查或规模最小性认证。逐源原件及全部数组保于[本批证据](../../tools/evidence/existing-net-witnesses-and-exact-duals-primary/README.md)。
