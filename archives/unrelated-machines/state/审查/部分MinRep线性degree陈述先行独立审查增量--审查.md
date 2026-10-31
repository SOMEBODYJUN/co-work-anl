---
id: "unrelated-machines/partial-minrep-linear-degree-statement-first-review-20261031"
kind: "review"
type_tag: "审查"
title: "部分 Min-Rep 线性 degree 陈述先行独立审查增量"
status: "integrated-independent-reconstruction"
truth_status: "full-source-read-scoped-derivation-with-external-source-boundaries"
review_level: "clean-show-full-read-and-cross-archive-comparison"
scope: "partial-MinRep linear-degree v2 statement-first reconstruction, normalization and conditional fee interface"
source_refs:
  - "source:de896618959a7c020fad:history/source/notes/unrelated_machines/partial_minrep_linear_degree_statement_first_row_source.md"
source_sha256: "b01269e878b076f74bade4699134b176d404bdfd3c04ea4d4b45d583f8f580bf"
evidence_paths:
  - "../../tools/evidence/partial-minrep-linear-degree-statement-first-20261031/original/partial_minrep_linear_degree_statement_first_row_source.md"
related_objects:
  - "../资料/partial-MinRep线性degree删边源与外部边界--资料.md"
  - "部分MinRep度数质量v4-v5陈述与域修复补充--审查.md"
  - "部分MinRep高围长v3三源精读与随机repair边界--审查.md"
---

# 部分 Min-Rep 线性 degree 陈述先行独立审查增量

## 1. 来源身份、阅读顺序和处置

本次 `clean show` 后完整读取了
`history/source/notes/unrelated_machines/partial_minrep_linear_degree_statement_first_row_source.md`。
来源 ID 为 `de896618959a7c020fad`，大小 10,395 字节，SHA-256
`b01269e878b076f74bade4699134b176d404bdfd3c04ea4d4b45d583f8f580bf`。原文以字节保全
在 `tools/evidence/partial-minrep-linear-degree-statement-first-20261031/`。

这份来源是读正式 v2 Exact Statement 后、读作者 proof 和其他 child review **之前**完成
的独立重构；它主动声明此前曾见过旧的 O(g log g) 方向提示，但没有把该提示当成证明。
因此本页处置为 **integrated-independent-reconstruction**：把精确常数、删边分支、
degree 必要性、正规化和 fee 条件作为现有线性-degree 资料页的独立核对和版本 provenance，
不建立第二个部分 Min-Rep 定理，也不把“外部 PCP 未读”升级成已认证的归约。

## 2. 定义域和四项主张

对象是显式 regular projection game，允许平行 constraint 边；每边是全投影映射，
multilabeling 的 cost 是所有真实列表长度之和，边 covered 当且仅当列表中存在一对
满足投影。给定二进制 `g>=2` 和 `0<rho<=1`，源采用

\[
\tau=\frac{\rho}{100g^2},\qquad
\gamma=\frac{\rho^3}{10^9g^8},\qquad
H=\frac{4g}{\tau},\qquad
\mu=\left\lceil\frac{1000g\lambda}{\rho\ell}\right\rceil,
\]

其中 `ell=floor(log_2 g)`、`lambda=1+ceil(log_2 Q)`。源的核心重构包含四个不同层级：

1. cheap multilabeling 在原图上的覆盖比例严格小于 `tau`；
2. `D<2mu` 时原图原样保留，`D>=2mu` 时以 `p=2^{-s}` 抽样，随后一次性删除中间
   degree 大于 `Delta=1000mu` 的顶点全部 incident edges；
3. perfect singleton labeling 对任意 seed 保持，NO 输入以至少 0.9 概率输出非空、
   max degree 至多 `Delta` 且同时禁止每个 cost `<=gN` 的列表覆盖 rho 比例；
4. 任意非空 balanced total-projection game 若具有同样的 strict cheap-list 禁止，则
   `M>(g-1/2)N/rho`，从而 `Delta_max>(2g-1)/rho`。

第 1、2、4 项是可在来源内自足检查的数学推导；第 3 项若要成为 PCP/UM hardness
接口，仍依赖外部 perfect-complete source、repetition 和真实 physical compiler。

## 3. 原图 cheap-list 上界

对任意 cost `<=gN` 的 multilabeling，源按 `H=4g/tau` 将列表长度大于 H 的顶点标为
heavy。heavy incident edge 比例至多 `2g/H=tau/2`。若覆盖比例达到 tau，则仍有至少
`tau M/2` 条 covered edge 两端 light；从每个非空 light list 均匀抽 label，每条该边
由至少一对 witness 覆盖，命中概率至少 `1/H^2`。于是能构造单标签赋值，覆盖率至少

\[
\frac{\tau}{2H^2}=\frac{\rho^3}{32\cdot 10^6g^8}>\gamma,
\]

违背 `val<=gamma`。该推导没有枚举列表、不要求所有列表非空、不把平行边合并，故其
量词确实是“所有 cheap lists 同时成立”。它与既有 `partial-MinRep线性degree删边源`
中的同一 deterministic template 相容；本源独有的是先行重算的精确常数和严格不等式。

## 4. 随机删边分支与概率账

当 `D>=2mu`，取最小 `s` 使 `2^s mu>=D`，令 `p=2^{-s}`、`d=pD`、`z=pM`。
最小性给出 `mu/2<d<=mu` 以及 `Nmu/4<z<=Nmu/2`。源共同控制三个事件：

- 中间总边数 `X>=z/2`；
- 一次 degree trimming 删除的边数 `Z<=z/4`；
- 所有 cheap lists 在中间图覆盖边数均 `<rho z/4`。

于是输出边数 `m'=X-Z>=z/4>0`，而删除不会增加任何列表的覆盖绝对数，所以最终
coverage `<rho`，并且是严格不等式。总边数下尾使用 `Pr[X<z/2]<=exp(-z/8)`；固定
list 的 covered-edge 上尾以 `tau z` 为均值，再用
`[e/(25g^2)]^{rho z/4}`，通过 cheap-list 数量上界
`(eQ/g)^{gN}<=exp(gN lambda)` 做 union bound。源给出的粗界是单个列表坏概率
至多 `exp[-(125/2)gNlambda]`，联合后小于 `exp(-492)`，明显强于所需的 0.9。

一次 trimming 的边损失使用 size-bias 恒等式：对 `V~Bin(D,p)`，

\[
\mathbb E[V1_{V>\Delta}]
 =d\Pr[Bin(D-1,p)\ge\Delta]
 \le d(e\mu/\Delta)^\Delta
 \le \mu 2^{-1000\mu}.
\]

源明确强调只做一次 trimming，不迭代按最终 degree 反复删除；输出未被标记的顶点
degree 不会超过中间 degree，故 max degree 对每个 seed 都成立。随机位由每条边的
`s` 个公平 bit 提供，循环按显式 `s<=ceil(log_2 D)`，不按 `mu` 或 `Delta` 的数值
长跑。这里的概率账和位复杂度是 source-level mathematical reconstruction，不是
软件执行结果。

## 5. 线性 degree 必要性、ceil 和严格性

源独立处理任意非空、平衡但不一定 regular 的 total-projection game。先给每个左点
任意一个 singleton label，花费 `N/2`；再选 `t=ceil(rho M)` 条边，把每条边左端
label 的投影加入右端列表，增量至多 t，并覆盖这 t 条边。令
`T=(g-1/2)N`；若 `M<=T/rho`，则 `ceil(rho M)<=T`，从而得到 cost `<=gN`、
coverage 至少 rho 的列表，和 strict cheap-list 禁止冲突。因此

\[
M>\frac{(g-1/2)N}{\rho},\qquad
\Delta_{max}>\frac{2g-1}{\rho}.
\]

该推导保留了 `ceil` 和严格覆盖率，适用于 `rho=1`，不使用 PCP、regularity、随机抽样
或外部来源。它直接记录了为什么固定 rho 时同一类 source 不能把 degree 阶数写成
`o(g)`；它不声称任何 UM 构造已经达到该下界。

## 6. 两个正规化接口

源给出两项自足的 value-preserving normalization：

1. 对左右 degree 分别为 `d_A,d_B` 的 biregular game，按 gcd 复制左右顶点，并把每条
   原边替换成复制对的完整二部 edge set；同值复制赋值给出一个方向，随机选原点 clone
   给出另一个方向，因此 value 和 perfect completeness 保持。边、projection、平行边
   都显式保留，规模至多多项式增长。
2. 两侧 alphabet 不同则取共同 `[Q]`，左侧用 surjection 折回有效旧 label，右侧用
   injection 嵌入有效 image；image 外右 label 不可能满足任何 incident edge，故可
   retraction 而不降 value。该接口只证明字母表统一，不提供 PCP 的 soundness 或 UM
   compiler。

这两步与现有 v4/v5 域修复审查相接：字母表必须非空、平行边按边计数、外部 PCP
参数改变后需重新计算 `lambda,mu,Delta`，不能把旧参数静默沿用。

## 7. 外部 PCP、fee 和 UM 物理边界

来源报告称其另外定向读取了 Manurangsi 与 Minzer–Zheng 的 primary 结果，并以此比较
旧的 O(g log g) degree 与本 v2 的线性目标；本次归档只实读该比较报告，没有把外部文献
复核冒称为本次新阅读。安全结论是范围性的：外部 perfect-complete Label-Cover、
parallel-repetition 和 alphabet 定量是条件输入；`Q=poly_rho(g)` 才可把
`Delta=O_rho(g)` 写出来。随机 source 若串联确定性 promise 判定器，至多给出
`NP subseteq BPP` 型后果，不能用 `P != NP` 单独替代。

fee 接口同样只是条件推论：若另有真实 compiler 使
`cost<=N+B(sigma)/F`、`B<=cM`，且 `M<=Delta N/2`，则
`F>=c Delta/[2(g-1)]` 足以推出 cost `<=gN`，与 good NO source 冲突。这里要求
`F>0,c>=0`；没有 partial-trigger、query、pi 接口、实际 schedule 或 fee=1 证明。

## 8. 与既有档案的关系和接续

本页与 `partial-MinRep线性degree删边源与外部边界--资料.md` 建立
“statement-first independent reconstruction → canonical v2 exact source”关系，补入
该资料页没有单独承载的常数反算、一次 trimming 量词和 strict ceil 边界。与 v4/v5
审查的关系是 domain/normalization consistency；与 v3 高围长审查的关系是随机 source
接口的下一层，不能把 v2 单轮删边自动写成 v3 的 high-girth repair 输出。

可保留的对象是：显式投影游戏上的随机删边与 degree necessary 条件。以下仍开放：

- 外部 PCP/parallel-repetition 的逐项适用性和新颖性；
- 从 source list 到 ordinary UM 的真实位多项式 compiler、低负载 decoder、fee 实现；
- near-two hardness、P/NP 或六人 SPE 目录覆盖结论。

该来源无代码或有限运行需要移入 `tools/evidence` 以外；原文只作为数学 provenance 保存。
