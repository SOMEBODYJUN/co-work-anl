# 逐机统一时间的查询—返回索引交换障碍

读取目的：检验近二困难性归约的一个实际身份接口。旧[保护环共享子句接线](near_unit_implication_pcsp_and_physical_copy_obligation.md)允许读出的 query 与返回的 blocker 索引错配；本页说明任意容量匹配型内部网络都不能靠固定辅助任务修复这个局部合同。结论读具体原 job 身份，允许多个 small slots，但只保证内部替换，不替代全局 NO decoder。

## 1. 精确对象、模式与结论

**ID / Version：`UM-MACHINE-UNIFORM-QUERY-RETURN-INDEX-EXCHANGE-v2`。** 旧单容量 v1 原字节与独立审查保留；本版改变内部时间域，另立陈述。

**Objects / Domain / Definitions / Quantifiers。** 显式内部机器集 \(H\)，固定必做原任务集 \(A\)，两组边界原任务 \(Q=\{q_1,\ldots,q_k\}\)、\(R=\{b_1,\ldots,b_k\}\)，\(k\ge2\)，三类及族内身份均互异。令实际原任务总数 \(N=|A|+2k\)。给正二进制有理阈值 \(T\)。每内部机 \(h\) 有非负有理 \(s_h\)，该机上每个原 job 的条目仅为 \(s_h\) 或 \(\infty\)，资格任意。允许 \(s_h=0\)、\(s_h>T\)，无其它隐含预载或任务。

对 \(X\subseteq Q\cup R\)，模式可行指 \(A\cup X\) 的每枚 job 恰一次在原 \(H\) 的有限端执行，全部内部负载同时 \(\le T\)；其余边界任务由外部执行。记

\[
 X_\varnothing=R,\qquad X_i=(R\setminus\{b_i\})\cup\{q_i\},\qquad
 X_{j,i}=(R\setminus\{b_i\})\cup\{q_j\}.
\]

分别为 inactive、aligned 和读 \(q_j\) 却返回 \(b_i\) 的 mismatch。读的是这些原 jobs 的目的地，不是机器是否有某件 unit。

**Exact Statement / Conclusion。** 对每个所列系统、任意 \(i\ne j\)，若 \(X_i,X_j\) 在 \(T\) 可行而 \(X_\varnothing\) 在 \(T\) 不可行，则 \(X_{j,i},X_{i,j}\) 均在同一严格阈值 \(T\) 可行。因而全部 aligned 可行且 inactive 不可行时，全部 \(k(k-1)\) 个错配均可行。

更强的构造形式：给两份完整 aligned 内部分配，可确定性总位多项式输出 inactive 或 \(X_{j,i}\) 的完整内部实际分配，全部 \(A\) 保留。不给见证时，可先用显式容量匹配找它们，或可靠报告某个 aligned 不可行。

**Assumptions / Scope。** 辅助集 \(A\) 固定，不可随模式更换；同一内部机有限时间相同，但跨机可不同。没有对真实外端共享负载作保证。局部系统可有不可行模式；如某辅助 job 根本无内部有限端，所有 aligned 前件即失败，只作不可行判定，不把其无资格封装冒称合法 UM 输入。

## 2. 精确容量化，包括零时间与数值规模

每机 strict 整数容量取

\[
 c_h=\begin{cases}\min\{N,\lfloor T/s_h\rfloor\},&s_h>0,\\N,&s_h=0.\end{cases}
\]

该机执行 \(z\) 件 jobs 的真实负载恰 \(zs_h\)。由于 \(z\le N\)，上述容量对任意 job 子集的可行性精确等价；\(s_h>T\) 给容量0，零时间不除零。空 \(H\) 允许，但因 \(k\ge2\) aligned 不可行，不能给假见证。

可用容量网络；也可将每原机换成 \(c_h\) 个同邻接的虚拟 slots，最多 \(|H|N\) 个。原 jobs 不复制，最终每个 slot 的 job 归回原机，所有负载仍 \(\le T\)。从不按未截断 \(T/s_h\) 或分母的数值展开。

## 3. 一次增广证明全部身份交换

令 \(L=|A|+k\)。取 aligned \(i\) 的容量匹配，删掉 \(q_i\) 的一条匹配边，得到覆盖 \(A\cup(R\setminus\{b_i\})\) 的 \(L-1\) 件原 jobs 的匹配 \(M\)。只考虑左侧 jobs

\[
 U=A\cup R\cup\{q_j\}.
\]

第二份 aligned \(j\) 在这个图中有 \(L\) 条匹配边，故 \(M\) 不是最大。普通二部匹配增广性（或先作上述多项式 slots 展开）给一条增广路，起点只能是当前未匹配的 \(b_i\) 或 \(q_j\)，终点是有空余容量的机器。翻转保留全部原先已匹配 jobs：

- 从 \(b_i\) 开始，新增它，得到 \(A\cup R\)，即 inactive；
- 从 \(q_j\) 开始，新增它，得到 \(A\cup X_{j,i}\)，即错配。

原 \(A\) 的任何 job 均不被删去、拆分或匿名代替。若 inactive 不可行，第一种结果不可能，所以必得到错配。交换 \(i,j\) 重做即给另一方向。允许两匹配占不同机器、存在空闲 slots、任意辅助资格，无满载或树结构假设。

等价的标准 matroid 解释：在 slots 图的 job 侧取 transversal matroid，收缩共同 \(C=A\cup(R\setminus\{b_i,b_j\})\)。两对齐模式使 \(\{q_i,b_j\}\)、\(\{q_j,b_i\}\) 独立，而 inactive 不可行使非loop \(b_i,b_j\) 平行，遂两错配独立。若用秩截断，仅为保留这些小集合独立性的证明语言，不是物理加约束。本文已给增广证明，不把拟阵归属当未核后端。

## 4. 全原任务封装、weak 阈值与不可省的外部边界

给每个边界 job \(j\) 一台互异 outside 机 \(O_j\)，仅 \(j\) 可在其上耗时 \(T\)；辅助 \(A\) 没有 outside 端。指定模式 \(X\) 的内部输出后，其余每个边界 job 放自己的 \(O_j\)，得到全部 \(N\) 件原任务恰一次、峰 \(\le T\) 的实际调度。

只要 aligned 可行，全部辅助 job 必已有有限内部端，此封装就是合法普通 UM 矩阵，且至少有 \(2k\) 台 outside 机。若辅助无端而前件失败，不主张该非法原任务成为目标合法输入。模式 \(X\) 本身仍是目的地投影的要求，封装未物理强制它；inactive \(X=R\) 与所有边界在外的 \(X=\varnothing\) 是不同模式。

对任意有理 weak 阈值 \(B\ge T\)，如果一个接口禁止 inactive 在 \(B\) 可行，则尤其禁止它在 \(T\) 可行；上述错配输出本来 \(\le T\le B\)。因此它不能同时实现“所有索引可选择、必须查询、所有 weak 模式都同索引”。这里不需要 \(B<2T\)，也不把只给 \(B\)-可行 aligned 误当成 \(T\)-可行。

如果真实归约把 outside 端接到变量环或共享锁定机器，改变模式也改变外部执行的 jobs，外部负载可能增加。本页只保证内部替换，不能由它推出任意外接公式可行，也不能用两份假见证替代源解码。退出这个局部合同需要分析同机异权、模式相关辅助集、不同边界 bundles 或内部外部不可分容量等额外机制；本页不证明这些条件充分。

## 5. 单容量旧域与位复杂度

旧 `UM-SINGLE-CAPACITY-QUERY-RETURN-INDEX-EXCHANGE-v1` 取 \(T\le B<2T\)、所有有限内部 \(p_{hj}\in(B/2,T]\)，允许同机异权。其 strict/weak 内部每机至多一件，资格 matching 即精确模式可行性。先把其 finite 时间统一为 \(T\) 得本版单slot系统，构造 matching 后恢复原时间 \(\le T\)，才给旧实际输出；不是说原两个矩阵逐项相同或 v1 原时间本来统一。旧 Exact/独立记录保留，不虚构单独 v1 作者 Proof；本版 Proof 的相应节直接处理该化约。

二进制有理比较、正数取整及截 \(N\) 按总编码长度多项式；可先比较 \(Ns_h\le T\) 决定直接取 \(N\)。Slots 最多 \(|H|N\)，资格展开最多原 finite 数乘 \(N\)，dense 输入计入全部矩阵项。判两 aligned、增广、投影原机、回算每机件数乘真实 \(s_h\)，均位多项式，输出具体原 job 目的地。此页没有新通用软件或有限枚举。

**Dependencies / Evidence / Counterevidence / Status / Related Files。** 标准容量匹配及增广交换是既有技巧，已从新颖性扣除；具体回收内容为这个全原 query/return 身份合同，不主张新匹配理论或全球身份复制不可能。作者先冻 v1/v2 Exact，rank分别只据各版陈述独立重构后才实际读 v2 Proof，root实际读原件与审查并独核。共同辅助无端时的封装合法性在本稿明确，不变更交换核心。最终实际范围见[审查](../../reviews/unrelated_machines/machine_uniform_query_return_index_exchange_review.md)。数学完整、无 standing fatal，implementation none、外审/全球新颖性未认证；UM-TARGET-v1 仍 OPEN。
