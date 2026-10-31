## 全种子完备源的拒绝种子证书

**UM-PERFECT-COMPLETE-SEED-CERTIFICATE-v1。** 这是从复杂度定义得到的独立推论，不改变以上v2/v3/v5源的身份，也不声称新PCP或物理归约。设固定确定性程序R(Φ,r)在每条计算路径上均有关于公式长度的硬多项式时间及输出长度界，种子r有固定多项式长度；未用位可忽略。R返回FAIL或明确对象域I内的合法显式实例。设D是全输入确定性多项式程序，在source YES上答1、source NO上答0，在promise外可任意答但必须停机。FAIL直接按1处理，记复合结果为D̂(Φ,r)。要求

\[
\Phi\in\mathrm{SAT}\Rightarrow\forall r\quad\widehat D(\Phi,r)=1,
\qquad
\Phi\in\mathrm{UNSAT}\Rightarrow\exists r\quad\widehat D(\Phi,r)=0. \tag{S1}
\]

则UNSAT∈NP，故NP=coNP。若均匀独立公平位采样另满足一个对所有UNSAT输入都成立的固定逆多项式拒绝概率下界，则进一步有

\[
\mathrm{SAT}\in\mathrm{coRP},\qquad
\mathrm{NP}=\mathrm{RP}=\mathrm{coRP}=\mathrm{coNP}. \tag{S2}
\]

**证明。** UNSAT验证器猜测r，重跑R；FAIL拒绝证书，否则当且仅当D输出0时接受证书。(S1)左边排除可满足公式的所有假证书，右边给每个不可满足公式一个证书。验证器无需辨认source好事件或验证source NO承诺；D在promise外的拒绝也不会给SAT假证书。SAT的确定性many-one完全性给coNP⊆NP，取补即得相等。这里只存在输入各自的种子，不存在或寻找一个公共好种子的声明。

设拒绝概率≥1/q(|Φ|)，q为固定整数值、至少1的多项式上界。独立运行q次，全部答1才接受SAT。SAT永不误拒，UNSAT误受概率≤(1−1/q)^q≤e^(−1)<1/2，故SAT∈coRP。RP⊆NP由接受随机位作证书直接成立，取补给coRP⊆coNP；再用NP⊆coRP和取补夹得(S2)。仅有一个好种子可能只有指数小概率，不能免费推出(S2)。均匀性、最坏多项式时间、硬种子长度和同一个逆多项式界都是前提；期望时间须先截断并重核概率，不能未经转换直接调用本引理；随机advice或仅高概率YES完备不属于本合同。

**应用到已有源。** 先固定g、ρ及需要时的G，再接本文已登记的确定性完美完备PCP起点。以下概率均是好NO且非FAIL的无条件联合概率。

| 源身份 | 每个YES种子的行为 | 每个UNSAT输入的好NO概率 | 确定性总promise判别器的后果 |
| --- | --- | --- | --- |
| UM-PARTIAL-MINREP-SPARSIFICATION-BRIDGE-v2 | 每次删边都保singleton覆盖，空边集也是YES | ≥0.9，且输出非空 | (S2) |
| UM-PARTIAL-MINREP-REGULAR-HIGH-GIRTH-SOURCE-v3 | 非FAIL复制原标签全满足；FAIL按YES处理 | ≥0.8 | (S2) |
| UM-PARTIAL-MINREP-DEGREE-MASS-REGULARIZATION-v5 | 非FAIL保原typed标签完备；FAIL按YES处理 | ≥0.8 | (S2) |

原文NP⊆BPP是仍正确的较弱后果；这里提高的是复杂度后果，未更改源的度数、alphabet、概率或费用合同。固定参数的PCP指数可依赖g、ρ、G，不声明它们随公式长增长时整条链仍统一多项式。v2的空边YES必须被D接受；v3/v5的FAIL不提交给D。既有Qγ域、typed非空域及capped sampling硬位界保持。

**条件UM推论。** 对每个先固定整数k≥2，设上述R_k的每个非FAIL输出H还可由一个确定性总位多项式编译器产生合法完整模型(P_H,T_H)，T_H为正有理数，令β_k=2−1/k。必须额外证明：

1. SAT的所有非FAIL种子均有真实整数OPT(P_H)≤T_H。
2. 每个UNSAT至少有一个好、非FAIL种子，其每个真实合法完整分配σ若C_max(σ)<β_kT_H，就能导出违反source NO的见证。因此该种子有OPT(P_H)≥β_kT_H，允许等号。

若UM-TARGET-v1的算法A和常数ε>0存在，选择固定k使1/k<ε，定义

\[
D_A(H)=1\quad\Longleftrightarrow\quad
C_{\max}(A(P_H))<\beta_k T_H. \tag{S3}
\]

SAT时C_max≤(2−ε)OPT≤(2−ε)T_H<β_kT_H；好NO时任何A的合法输出均有C_max≥β_kT_H。故(S1)成立，推出NP=coNP；满足上述第2项**编译后NO/全输出decoder合同**的非FAIL种子有逆多项式概率时才得到(S2)，不能只引用更大source NO事件的概率。证书接受条件是(S3)的补 **≥β_kT_H**，不能误用严格大于而漏掉NO等号。算法只编码整数k和有理阈值，不需要编码或比较未知实ε。精确逐机有理求和与交叉相乘的位长多项式；坏种子也必须输出合法实例并使A停机。空任务/零OPT给负载0，T_H>0保严格YES分离；∞不参加有限负载求和。

本条件推论保留一个实质缺口：本文没有提供编译器或第2项全输出decoder。原费用桥若能从每个低负载σ产生covered≥ρM且cost≤N+B/F≤gN的列表，才可用其严格NO禁令证明第2项。只给某个调度、LP证书、好事件概率或固定ε的一次gap都不够。

在额外物理合同全部成立之后，NP≠coNP已足以否定原目标；有概率下界时也可采用NP⊄coRP，它比NP⊄BPP弱。任何一项都没有被改写成仅P≠NP，主目标及其一般反面仍OPEN。该推论是标准证书/单侧错误机制的自足应用，全球新颖性未认证。独立先陈述重构、最终正文攻击、精确阈值边界核验见[专门审查](../../reviews/unrelated_machines/perfect_complete_seed_certificate_review.md)。
