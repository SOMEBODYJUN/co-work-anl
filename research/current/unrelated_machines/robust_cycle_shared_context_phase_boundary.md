# 鲁棒双端变量环在任意共享背景中的相位不可读界

读取目的：检查一种具体的可读复制方案——保留双端变量环，再追加共享的 medium 任务或辅助网络读取相位。若环本身在弱阈值下只允许两个一致方向，这个方案有一个精确边界：给任一严格完整调度，背景原任务逐件不动，所有环的相位都能任意切换到负载小于 \(3T-B\)。因此 \(B\ge3T/2\) 时，这种背景不能限制相位向量。它不覆盖给环任务增加第三端、其它共同 core 或不同的全局解码语义，不是一般 UM 近二困难性或近似算法结论。

## 1. 物理对象、严格域与单一身份

**ID / Version：`UM-ROBUST-CYCLE-SHARED-CONTEXT-PHASE-v1`。**

取正有理数 \(T\) 与有理数 \(T\le B<2T\)。一个 **core** 有 \(n\ge2\) 台互异原机器 \(M_1,\ldots,M_n\) 和 \(n\) 件不同原任务 \(j_1,\ldots,j_n\)，下标循环。每件 \(j_i\) 的全部有限端恰为

\[
 j_i:\quad M_i:a_i,\qquad M_{i+1}:b_i,
 \qquad 0\le a_i,b_i\le T.                         \tag{1.1}
\]

phase 0 是全部任务选 \(M_i\)，phase 1 是全部任务选 \(M_{i+1}\)。两份 core 调度的峰均不超过 \(T\)。称该 core **在 \(B\) 鲁棒**，若它单独的每个完整实际调度，只要峰不超过 \(B\)，便是这两个 phase 之一。

一个完整普通 UM 可以有任意有限多个这样的 core，含零个。**不同 core 的机器集彼此不交，任务集也彼此不交，不允许重用 core 机器。** 其余原任务组成 context；另可有任意额外机器。context 任务可同时关联多个不同 core 的机器和额外机器，多个 context 任务可真实共享这些机器，不需按子句或模块划分。context 的全部有限时间为任意非负有理数，资格 arity 任意，未使用的有限时间也可大于 \(T\)。唯一保留的资格限制是每件 core 任务仍恰有式(1.1)的两个有限端。

所有机器、任务和资格均显式给出，未列端为 \(\infty\)，每件原任务至少有一个有限端，原机器数至少一。给整个普通 UM 的一份完整合法实际分配 \(\sigma\)，要求全部原任务恰执行一次，且所有机器同时满足 \(C_{\max}(\sigma)\le T\)。不假设能从未知实例多项式求出这份严格见证。

## 2. 精确结论 A、B、C

**Exact A：碰撞的必要充分条件。** 一个 core 在 \(B\) 鲁棒，当且仅当每台 \(M_i\) 均有

\[
 a_i+b_{i-1}>B.                                      \tag{2.1}
\]

鲁棒时，两个 phase 在 \(M_i\) 的 core 负载都严格大于 \(B-T\)，两者之差满足

\[
 |a_i-b_{i-1}|<2T-B.                                 \tag{2.2}
\]

**Exact B：在同一个共享背景中切换全部相位。** 假设所有 core 在 \(B\) 鲁棒。对任意显式指定的 core phase 向量 \(\theta\)，给定上述完整实际 \(\sigma\le T\)，可以确定性总位多项式构造覆盖全部原任务的完整实际分配 \(\tau_\theta\)，使每个 core 实现指定 phase，每件 context 原任务逐件保持 \(\sigma\) 的目的地，额外机器负载不变，而且

\[
 C_{\max}(\tau_\theta)<3T-B.                         \tag{2.3}
\]

非严格版本 \(C_{\max}\le3T-B\) 当然也成立。式(2.3)在不切换、负载不增或无 core 时也成立，不需要额外的正增量条件。因此

\[
 B\ge\frac32T\quad\Longrightarrow\quad
 C_{\max}(\tau_\theta)\le B
 \quad\hbox{对所有 }\theta.                         \tag{2.4}
\]

这是同一个完整实例的共同实际分配，不是分别可行的逐模块投影。

**Exact C：三半阈值锐。** 对每个有理 \(T\le B<3T/2\)，存在两机两件 core 原任务及一件唯一端 context 原任务，使 core 在 \(B\) 鲁棒，整个实例有完整严格 \(T\) 调度，但另一个 core phase 没有任何峰不超过 \(B\) 的完整扩展。因此不能把(2.4)的全 phase 结论无条件延伸到 \(B<3T/2\)。

**同一身份内的包络补充。** 对每个 \(T\le B<2T\) 和每个正有理 \(e<2T-B\)，存在同样两机三任务的实例，其指定另一 phase 的最小完整扩展峰恰为

\[
 3T-B-e.                                             \tag{2.5}
\]

故(2.3)的 \(3T-B\) 是准确上确界；没有有限实例达到这个严格包络。

Objects / Domain / Quantifiers / Assumptions：第1节全部普通 UM 物理对象、明确的 disjoint cores、所有有理 \(T,B\)、给定完整实际 \(\sigma\) 及任意显式 \(\theta\)。Definitions / Scope / Conclusion：鲁棒性是 core 单独的弱实际调度关系；结论是固定全部 context 原端的相位切换。Dependencies：普通 UM 的非负负载、循环二进制字串碰撞和下文逐机计算，无外部复杂性或 PCSP 定理。Evidence / Status：自足限定证明完成，先 Exact 独立重构和后读作者全文的内审均未发现 standing fatal；无外审、新颖性或一般 UM 正反面认证。

## 3. 碰撞条件的完整两向证明

记 \(z_i=0/1\) 表示 \(j_i\) 选 home/successor。机器 \(M_i\) 只可能收到 \(j_i\) 和 \(j_{i-1}\)，两件同时到达恰当且仅当

\[
 (z_{i-1},z_i)=(1,0),
\]

其真实负载为 \(b_{i-1}+a_i\)。空机负载零，只有一件时负载不超过 \(T\le B\)。

若所有碰撞和严格大于 \(B\)，任何非恒定循环二进制字串必有至少一处 \(1\to0\) 转折，故其实际峰大于 \(B\)。两个恒定字串均可行，所以只有两个 phase。

反向，若某个 \(a_i+b_{i-1}\le B\)，从 phase 0 出发只把 \(j_{i-1}\) 改到其 successor \(M_i\)。该机两件和不超过 \(B\)，原 home \(M_{i-1}\) 变空，其余机器最多一件且负载不超过 \(T\)。这是一份完整非恒定实际分配。\(n=2\) 也成立：两件不同原任务同住 \(M_i\)，另一机空；因为 \(n\ge2\)，它不是 phase 1。因此碰撞等号必须放在非鲁棒端，不能把(2.1)改成非严格。

由 \(a_i+b_{i-1}>B\) 及每项不超过 \(T\)，每项均严格大于 \(B-T\)。两个 phase 的该机负载分别为 \(a_i,b_{i-1}\in(B-T,T]\)，于是得到(2.2)。对象中允许零时间，但鲁棒分支自动没有零端；\(T=B\) 的边界同样覆盖。排除的 \(B=2T\) 端点不可能有鲁棒 core。

## 4. 全部原任务与任意共享 context 的共同切换

从给定完整 \(\sigma\le T\) 删除 context 负载，每个 core 的限制调度仍有峰不超过 \(T\le B\)，由 Exact A 必为某一 coherent phase。不同 core 机器不交，所以每台 core 机器恰有自己 core 的一件原任务。

现在按 \(\theta\) 重排每个 core 的全部 \(j_i\)，全部 context 原任务逐件保持原目的地。每件 core 原任务恰选式(1.1)的一条原有限端，context 没有移动，没有复制、遗漏、拆分、隐藏预载或分析任务；得到合法完整 \(\tau_\theta\)。

固定任一 core 机器。记 \(\sigma\) 的 core 负载为 \(x\)，目标 phase 的 core 负载为 \(y\)，该机所有 context 原任务的真实总负载为 \(c\)。这个 \(c\) 是同一个原机器上的共同总和，不把跨模块 context 分别占用容量。由严格见证及(2.2)，

\[
 c+x\le T,\qquad y-x<2T-B,
\]

因此

\[
 c+y=(c+x)+(y-x)<3T-B.                               \tag{4.1}
\]

额外机器没有 core 原任务，全部原任务目的地不变，负载仍不超过 \(T<3T-B\)。有限多个原机器均满足严格上界，故其最大值也严格小于 \(3T-B\)，证明(2.3)。当 \(B\ge3T/2\) 时 \(3T-B\le B\)，得(2.4)；临界 \(B=3T/2\) 仍有实际峰严格小于 \(B\)，不存在等号漏洞。

这项构造保留了任意 medium 时间、零时间、跨 core 资格及不可私有化的共同辅助资源。它给定一份完整 strict 见证后切换相位，不寻找未知见证，也不需要独立求解每个背景模块。

## 5. 两机三任务的阈值锐例与包络上确界

对 \(T\le B<3T/2\)，两件 core 原任务为重任务 \(h\) 和轻任务 \(l\)，在两台机器 \(M_1,M_2\) 上的时间分别均为 \(T\) 和 \(T/2\)。将其看作二端环，两机任一碰撞和均为 \(3T/2>B\)，故 Exact A 保证鲁棒。

另有一件 context 原任务 \(f\)，唯一端为 \(M_1:T/2\)。把 \(l\) 放 \(M_1\)、\(h\) 放 \(M_2\)，全部三件原任务的真实负载为 \((T,T)\)。另一 phase 把 \(h\) 放 \(M_1\)，该机负载 \(3T/2>B\)；\(f\) 无其它端，故任何该 phase 的完整扩展都失败。这证明 Exact C，且 \(B=T\) 正常。

对于包络补充，给 \(0<e<2T-B\)，令

\[
 d=B-T+e\in(0,T).
\]

保持 \(h\) 两端时间 \(T\)，改令 \(l\) 两端时间均为 \(d\)，context \(f\) 唯一端为 \(M_1:T-d\)。core 的碰撞和 \(T+d=B+e>B\)，仍鲁棒。把 \(l\) 放 \(M_1\)、\(h\) 放 \(M_2\)，加 \(f\) 后仍为 \((T,T)\)。另一 phase 的真实负载恰为

\[
 (2T-d,d)=(3T-B-e,d).
\]

因为 \(d<T\)，全局峰恰 \(3T-B-e\)。该 phase 已固定 core 原端，context 只有一个端，所以它也是该 phase 最小完整扩展值。随正有理 \(e\to0\) 趋近 \(3T-B\)，但每个有限实例均严格低于包络。两例全局 OPT 都恰为 \(T\)，因为 \(h\) 无论去哪台机器都耗时 \(T\)；它们是相位扩展界，不是 OPT gap 或源 NO。

## 6. 承重域条件与总位复杂度

不同 core 机器不交是一项真实限制。若删去它，取 \(T=1,B=6/5\)，两份两机 core 共用 \(M\)，另机各为 \(N_1,N_2\)。每份 core 在 \(M\) 的两 phase 负载为 \(3/10,19/20\)，在 \(N_s\) 的两 phase 负载均 \(9/10\)。两机碰撞和分别 \(5/4,9/5\)，各 core 单独在 \(B\) 鲁棒。加一件仅在 \(M\) 耗时 \(2/5\) 的 context；两 core 都取低态时 \(M\) 为 \(1\)，各 \(N_s\) 为 \(9/10\)，strict 可行。都切为高态后 \(M=23/10>3T-B=9/5\)。这只是域外反例，不是上述 disjoint 定理的反例。

core 任务恰两有限端、端时间不超过 \(T\)、给定完整 strict 实际见证、以及固定 context 原端也都用于证明。新增第三端可能使 strict core 限制分配不再是两个 phase，不能原样调用本定理。

构造先核全部原任务合法性和有理负载，按(2.1)核鲁棒性，再从每个 core 的一件任务读出原 phase并核全部任务一致，随后依输入的 \(\theta\) 重排。总共扫描显式原机器、原任务和有限资格。有限有理和可用输入分母乘积作共同分母，其位长不超过分母位长总和再加多项式项；精确比较和全机负载回算均总位多项式。不按分母、\(T\)、\(B\) 或 \(1/(2T-B)\) 的数值循环，不枚举 \(2^{\text{core数}}\) 个 phase 向量。无 core 时返回 \(\sigma\)，空 context、零时间 context 或未用的大时间端也无额外分支问题。

## 7. 与现有边界的区别、证据与未解义务

[三外接选择器](three_host_selector_sharp_three_halves.md)及[多输出加权预算](weighted_fanout_profile_boundary.md)允许任意内部 gadget，但读出依靠独立空/满预载；本页允许任意共享 context，代价是 core 限定为鲁棒双端环。[任意异权私有子句网络](general_weighted_private_clause_exchange_and_shared_outside_boundary.md)的全公式定理允许环任务进入私有 clause 网络，本页不允许给 core 任务这些资格；本页则能处理其私有性假设排除的共享背景。因此不能将任一页的更宽半边 scope 免费并入另一页。

本项统一审查入口为[实际审查](../../reviews/unrelated_machines/robust_cycle_shared_context_phase_review.md)。独立 Exact-first 重构实际先读冻结 Exact v1，后指出其一处“core共享机器”措辞与明确 disjoint 前提冲突；Exact v2 已明确仅 context 可跨 core 关联，保留 v1 原字节。随后实际后读修复 Exact 和作者完整证明，核过全部 A/B/C、严格包络及上确界补充。实际来源记录为 `cycle_core_exact_first_independent_v1.md`（SHA256 `0bb6a72b29511fc9b342cd327f0bb55aee4370579c0be22722290482a1040f6d`）与 `cycle_core_post_proof_review_v1.md`；原作者 Exact v2 的 SHA256 为 `56e2f03a8a47a7ac9fce3f0baa1bd86605ffeeb068bb6b65dff54eb6e8eb3e3f`，作者 Proof 为 `6e1668e1961bc1cd280ece09ad08eefbb6bd386baeb477ecebdfda9b5d4ffa99`。这些是内部限定审查，不是外部评审。

配套[小规模 Fraction 审计](../../../tests/audits/unrelated_machines/robust_cycle_shared_context_phase.py)枚举明确小 core 的全部 orientations、碰撞等号、两份 machine-disjoint core 加真实共享 context、三半锐例及上确界家族；全部原任务按原端逐机回算，输出 stdout JSON，约定冻结至[有限审计证据](../../../evidence/runs/unrelated_machines/robust_cycle_shared_context_phase_audit.json)，实际运行与文件身份由上述审查登记。有限枚举核实现与这些边界，不代替第3–5节一般证明。

所用循环字串碰撞、单件改派和逐机负载差都是标准技巧的直接推导，全球新颖性及独立论文价值未认证。结论只说：保留鲁棒双端环资格，再仅追加任意共享任务，不能从一个 strict 可行背景筛掉 weak 相位向量。它不证明所有源 NO 实例都 weak 可行，不排除改变 core 资格、非环共同结构或不同源解码，也没有提供一般 UM 算法或对所有固定 \(\epsilon\) 的真实近二归约。`UM-TARGET-v1` 及其一般反面均保持 OPEN。
