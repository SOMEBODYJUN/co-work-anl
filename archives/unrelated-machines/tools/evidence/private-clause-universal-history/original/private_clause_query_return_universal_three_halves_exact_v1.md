# 私有 clause 查询—返回网络的全公式三半上界：Exact v1

ID/version：`UM-PRIVATE-CLAUSE-QUERY-RETURN-UNIVERSAL-THREE-HALVES-v1`。

作者 rainbow，2026-10-18。本文件仅冻结全部实际对象、局部证书与精确计算/存在量词，不含作者证明或策略，供独立 Exact-only 审查；只在 clone 外 scratch，不改 repo / Work / Git。没有把局部接口的 outside 封装当作真实变量机器。

## 1. 源与显式变量环

给正二进制有理 T>0、显式有限 CNF Φ，每 clause c 有 k_c≥2 枚真实 literal occurrences。允许重复变量、重复文字，每枚 occurrence 是不同物理身份且只属于一个 clause。空公式允许，空 clause、unit clause 不在本域。只保实际出现的变量。

每变量的真实 occurrences 任意排序成环；不足3枚时补 dummy 到环长至少3，dummy 不属于任何 clause。含 dummy 的总索引数为 N，真实 occurrences 数 L=Σ_c k_c，dummy 数 d=N−L。最少必要 padding 时 N≤L+2v，v 为实际出现的变量数。更长 padding 只接受显式表，并按其实际 N 计规模。

每索引 i 有一台不同的原 ring 机 M_i，后继为 i^+。真实 polarity s_i 为正0、负1，真实 return pin(i)=M_i（s_i=0）或 M_{i^+}（s_i=1）。Dummy polarity 不参与 clause 或 return pin；其 q job 仍用自己的变量环两个端。

若 Φ 为空，所有上述集合均空，输出一台 idle 原机、零 jobs，实际 OPT0；以下非空域至少有一台 ring 机。

## 2. 全部实际私有 clause 网络与原有限矩阵

每 clause c 给显式内部原机器集 H_c、显式辅助原 jobs 集 A_c。各 H_c 两两不交，且与全部 ring 机及稍后 dummy 私有机不交；各 A_c 两两不交且与全部边界原 jobs 不交。

每个真实或 dummy 索引 i 都有不同原 jobs q_i、b_i。对每 clause c，记 Q_c={q_i:i∈c}、R_c={b_i:i∈c}；这里 R_c 是 job 集的记号，**不是额外实际机器**。

对每个真实 i∈c：

- q_i 在 H_c 上有任意显式非负有理/∞时间；其全部外部端恰为 M_i:r_i^0、M_{i^+}:r_i^1，其中0≤r_i^0,r_i^1≤T，两端均有限。
- b_i 在 H_c 上有任意显式非负有理/∞时间；其唯一外部端为 pin(i):t_i，其中0≤t_i≤T。

对每个 dummy i：q_i 仅有两个 ring 端 M_i:r_i^0、M_{i^+}:r_i^1，均有限且在[0,T]；b_i 仅在其独有原机 D_i 耗时T。D_i 之间互异且与其它原机均不同。Dummy 不需要 clause 辅助 job、实际 demand job 或 return 端。

每个 A_c job 仅能在自身 H_c 上执行，资格与非负有理处理时间完全任意。没有 A_c 外送资格，没有跨 clauses 的 job / machine 共享，没有其它原 jobs、预载或资格。若候选有实际 clause demand job，它必须作为原 A_c 成员显式列出并始终在 H_c 执行；不能在 proof 中才补需求或删除需求。

这是完整实际 P：原机器 N+Σ_c|H_c|+d 台；原 jobs 2N+Σ_c|A_c| 件。所有原 jobs 只能整件、恰一次执行。内部允许同机异权、零时间、任意资格数及有限时间>T；并不局限统一 slots 或两种时间。A_c 必须有实际有限资格，且下面的局部证书将保证所用模式合法。

## 3. 每索引 strict 局部 aligned 证书

对每 clause c、每个真实 i∈c，要求局部模式

    A_c ∪ {q_i} ∪ (R_c\{b_i})

有实际完整内部 assignment λ_{c,i}：上述每枚原 job 恰一次在自身原 H_c 的有限端执行，全部 H_c 负载同时≤T。q_i 被读入，b_i 返回外部；其它 q 不在这个内部模式，其它 b 均在内部。没有把这些 outside 任务复制或丢弃；最终结论将给完整原 P 中它们的真实 ring / pin 目的地。

局部证书并非整个源 P 的 strict 调度。它仅说明这个私有 clause 接口对每个索引独立可选，不假设任何未知全局 SAT 赋值，也不宣称所有局部证书可以同时用于原变量环。

计算版本将全部 λ_{c,i} 作为显式输入数据，每份列每件指定模式原 job 的真实 H_c 目的机，可确定性核资格、恰一次与有理负载。存在版本只假设每份这样的实际证书存在，不要求已给算法能求未知 strict 见证。

## 4. 全公式实际三半结论

**Exact Statement / Computational Quantifier。** 对每个上述完整实际 P、全部给定合法局部 aligned 证书、任意 Φ（SAT 或 UNSAT）、任意环排序与任意内部异权，存在确定性总位多项式算法输出原 P 全部任务的完整合法实际 τ，满足

    C_max(τ)≤3T/2。

最终任务目的地全部是第2节的原有限端，绝不把用于分析的其它 labels、machines 或 jobs 当实际执行对象。所有 A_c 都实际在自身 H_c，所有 dummy b_i 在自身 D_i，全部 ring / clause / dummy 机器在同一 τ 内同时受控。

输出还可保证每台 ring 机恰执行一件原 q 或真实 b，实际时间≤T；每 clause c 的边界内外模式为以下之一：

- inactive：全部 R_c 在 H_c，全部 Q_c 在真实变量环；
- 某个 query j(c) / return r(c)：恰 q_{j(c)} 在 H_c，恰 b_{r(c)} 在其原 pin，所有其它 q 用 ring 原端、所有其它 b 在 H_c。允许 j(c)=r(c)，也允许错配。

每个 H_c 的实际峰≤3T/2，所有真实外部 ring 负载已由同一个全局 τ 明确保证，不是沿用局部私有 outside 封装的免费延伸。

**Existence Quantifier。** 若仅知每个 λ_{c,i} 存在、没有给出其具体调度，仍有相同的完整原 P 实际上界 OPT(P)≤3T/2。此时不声称算法可从原 P 求出未知 strict 证书。

因此，只要仍满足这些私有、单 query / 单 return、所有索引 strict 局部可选的准确合同，任意增加显式辅助 jobs 与非均匀内部成本，都不能把此模板变成对某个 B>3T/2 保源 NO 的桥。若还额外证明源 YES 的全局 OPT≤T，也不能由此得到 YES≤T / NO>(2−δ)T、δ<1/2；每个源实例已经有上述实际上界。这不依赖 P≠NP，也不是用固定arity严格NP替代 near-2 反面。

## 5. 范围与未覆盖机制

正式对象始终是第2节的全部实际原矩阵，沒有新增实际公共 clause 机器、virtual demand jobs 或私有 outside 机。局部接口证书与最后全局调度的角色分开，最后的 ring 负载必须实际重算。

本结论不覆盖 A_c 可外送到 ring / 其它 source 机器、不同 clauses 共享实际内部机器或 jobs、一个 label 必须同时读入/返回多枚 q/b 的 bundle、非所有索引均 strict 局部可选、以及原外部资格不符合第2节两个 ring / 单 pin 结构的 compiler。没有证明任意 global identity、任意 block coherence 或一般 UM source 不可能。

允许原外部时间取 near-unit (T/2,T]，上界不需要该下界；它也没有仅据该数值条件为任意异权 H_c 自动宣布 strict SAT decoder。若某个具体接口另外有 strict 身份证明，那是它的额外来源义务，本 universal 上界不使用该 decoder。

## 6. 显式规模、依赖扣除与证据状态

设 H=Σ|H_c|、a=Σ|A_c|、E_int 为第2节在所有 H_c 上实际列出的有限条目数。非空原 P 有 N+H+d 机器、2N+a jobs、3N+E_int 有限条目；完整 dense 计 (N+H+d)(2N+a) 项。局部证书长度按实际输入计，不能隐式给指数大小模板或未展开 padding 再声称 source 多项式。

证书验证、构造及全部原机器有理负载回算按完整 P、T、证书的总编码长度多项式。仅处理显式原任务和有限有理数，不按时间倒数、T/s 或分母数值生成 jobs。若只用最少 padding、内部网络和局部证书本来由源以多项式规模显式生成，则该整个构造亦为相应 source bit-polynomial；本 Claim 不额外保证任意压缩网络的规模。

数学依赖为新冻结 `UM-GENERAL-WEIGHTED-QUERY-RETURN-THREE-HALVES-EXCHANGE-v1`（其本身是已存 `UM-TWO-WITNESS-QUERY-SEPARATION-v2` 的直接推论），以及旧保护环 clause-OR 失败中的标准全局二部匹配选择技术。它不冒称新的查询分离/匹配定理；本 Claim 的增量是任意私有异权辅助网络与真实外部变量环的共同完整组合合同。此 Exact 不附证明策略以保独立陈述先行。

无新软件、有限枚举或主困难性结论；未认证外审、全球新颖性和独立成文价值。UM-TARGET-v1 与越出本模板的真实 near-2 source 仍 OPEN。
