---
id: "unrelated-machines/sparse-config-strong-moment-increment-review"
kind: "review"
type_tag: "审查"
title: "稀疏配置与强矩匹配双源增量审查"
status: "integrated-with-cross-source-boundaries"
truth_status: "general-proofs-scoped; exact-frozen-evidence; no-general-algorithm-or-UM-target-conclusion"
review_level: "full-source-read-and-prior-review-comparison"
scope: "sparse conditioned configuration gap and fixed-degree strong configuration matching-law obstruction"
source_refs:
  - "source:6a58c5bfa643bbb8225a:research/current/unrelated_machines/sparse_conditioned_configuration_gap.md"
  - "source:8cb84917989692a83f31:research/current/unrelated_machines/strong_configuration_matching_moment_obstruction.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/sparse_conditioned_configuration_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/strong_configuration_matching_moment_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:tests/audits/unrelated_machines/sparse_conditioned_configuration.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:tests/audits/unrelated_machines/sparse_conditioned_configuration_independent.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:tests/audits/unrelated_machines/strong_configuration_matching_moment_audit.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/sparse_conditioned_configuration_audit.json"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:evidence/runs/unrelated_machines/strong_configuration_matching_moment_audit.json"
legacy_ids:
  - "UM-SPARSE-CONDITIONED-CONFIG-GAP-v1"
  - "UM-CONTRACTED-SPARSE-CONFIG-GAP-v1"
  - "UM-FIXED-DEGREE-STRONG-CONFIG-MATCHING-LAW-OBSTRUCTION-v1"
---

# 1. 实读范围、版本身份与处置原则

本批完整读取了两个冻结 canonical 正文、`clean show` 的元数据和全文、正文中链接的旧版审查、四个主/独立审计入口及冻结 JSON。inventory 给出的稳定源分别是 `6a58c5bfa643bbb8225a`（文件 SHA-256 `88af645ff4ee5bd81afdeef2b67824ca34ed9183630c180373d1efa2d63c25f2`，15103 bytes）和 `8cb84917989692a83f31`（SHA-256 `32ee2ffae069e9c24cce24ec30963246403aa1f279559232f2ce40e168b4c651`，12027 bytes）。两者均来自冻结提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 的 `research/current/unrelated_machines/`，不是只凭摘要登记。

本页与先前《三选稀疏条件配置与资源星转移有限审查》和《强配置矩与对称重置阈值有限审查》存在明确重叠。重叠内容没有被当成新定理，也没有把旧审查的 evidence ID 误当成本批 canonical ID；本页的任务是为当前两个 source ID 建立可追溯处置，重述可复用的数学合同，核对量词/证据边界，并把两个对象之间能、不能连接的关系写清楚。旧审查中已保存的审计结果作为相关材料复读，新的独有内容限于本页的双源边界表、版本指纹和处置映射。

来源处置均为 `integrated`：稀疏源的定义域、参数族、OPT 下界/上界、逐边配置构造、端点收缩和强合同逃生口写入第 2 节；强矩源的固定阶伪矩、PSD 证明骨架、K2,2 编译、非整数方差障碍和二阶修复半径写入第 3 节；第 4 节保留有限证据的准确层级，第 5 节给出与既有对象的接续关系和未闭义务。两源都不是六人客户/共同目录 SPE 模型，不能移入该主问题。

# 2. 稀疏深树的逐边配置合同

## 2.1 定义域、参数和结论量词

稳定身份为 `UM-SPARSE-CONDITIONED-CONFIG-GAP-v1`，并在正文后半段扩展为 `UM-CONTRACTED-SPARSE-CONFIG-GAP-v1`。固定整数 `k >= 3`，令

\[
r=(k-1)/k,\qquad s_0=\min\{s\ge1:kr^s\le1\},\qquad M=(k-1)k^{s_0-2}.
\]

选 `H >= s_0` 且 `2^(H-2) >= M`，令 `gamma=2^(2-H)`、`T=1+1/k`。实例由两棵互不相交的完整 `k` 叉树、根之间的桥任务、底层核心及 `k` 个终端、路径占位任务和共享机器 `z` 组成。树任务在父端耗时 `1/k`、子端耗时 `1`；星任务在底层核心耗时 `1/k`、相应终端耗时 `1`；占位任务在相邻终端耗时 `1`，并可在 `z` 耗时 `gamma`。每项任务至多三台可用机器，有限处理时间只取 `{1/k,1,gamma}`。

结论量词必须保持为：对每个 `k` 及上述合法 `H`，存在一个实例族；对每条有限边 `e=(i,j)`，可以单独选择一个完整配置点 `y^(e)`，使 `x^(e)_(ij)=1`。不同 `e` 的配置点没有共同基点、共同联合分布或交叠 bag 的联合一致性。因而“配置可行 + 逐边条件探针”合同首轮和迭代都不删边，但这不是一般配置 LP 分离算法，也不是 SA/SDP 固定层级下界。

整数最优值为
\[
\operatorname{OPT}(P_k)=2-1/k,
\qquad \operatorname{OPT}(P_k)/T=2-3/(k+1)\longrightarrow2.
\]
下界依赖真实整数调度：若 `B < 2-1/k`，桥激活根后，每个带单位入边的核心必须至少下传两个小边，故至少有 `2^(H-1)` 个活跃底簇；每个活跃簇至少有两个星任务进入终端，`B<2` 又使每个终端至多接一个单位任务，故至少一个占位任务被迫送到 `z`，得到 `L_z >= gamma 2^(H-1)=2>B`。上界沿一条根到终端路径安排一个下传边，其余小任务留在父端，路径负载为 `2-1/k`，占位任务沿终端路径定向，不使用 `z`。

## 2.2 逐边证书的真实构造

内部核心收到入边边际 `alpha` 时，给每个配置 `{a,b_l}` 权 `alpha/k`，给全体 `{b_1,...,b_k}` 权 `1-alpha`。这些配置负载不超过 `T`，入边边际沿树递推为 `alpha -> r alpha`。当底簇星边际 `beta <= 1/k` 时，终端同时用星任务边际和相邻占位任务边际构造真实路径配置，再以空配置补齐；这是逐终端的完整证书，不是把总容量不等式替代 Hall 论证。当 `beta > 1/k` 时，把该簇的 `k-1` 个占位任务放进 `z` 的同一配置，受影响簇最多 `M` 个，而 `gamma M <=1`。

树边、星边、占位边、桥边四类查询分别通过删去其他查询质量、沿子树递推、终端路径单位配置或 `z` 上单任务配置来使指定边质量恰为 1。每个查询点仍满足每项任务覆盖 1、每台机器配置行和 1、每个配置负载不超过 `T`；投影的大任务基数也不超过 1。因而“每条边都有证书”是每条边各自的存在性，而不是一个证书同时强制全部边。

## 2.3 端点收缩后的增量义务

正文随后按每个底簇左右端点的极小超载星进行收缩。端点的两个单位邻任务总量为 2，删任一后余量 1 不超过 `T`。配置转移要求外部域互斥；给定查询边属于星时，必须优先把指定机器放入剥离顺序，否则替代边的质量可能降为 0。该引理只保证正向配置可行性和指定边的质量保持；从约化实例逆向恢复原调度或容量证书时，不能反推出原实例每条边的逐边 probe。

按固定顺序收缩所有端点，正文对 `k=3,H=5` 给出 `324` 次收缩，最终得到 `405` 台机器、`727` 项任务、`1778` 条有限边且无剩余极小星；一般族的最优值仍为 `2-1/k`。这是一条合法收缩顺序的结论，不是所有并行顺序产生同构终态，也不是一般极小星预处理算法的保证。

## 2.4 强合同的逃生口

机器 primal 图可用大小至多 4 的 bags 表示：底簇路径 bag 为 `{v,t_l,t_(l+1),z}`，树边 bag 含 `{parent,child,z}`，两根由含两根和 `z` 的 bag 连接。若合同改为要求每个 bag 的完整机器配置联合分布，并在交集机器上要求联合分布一致，有限树 gluing 可得到共同样本；任务域落在某个 bag 内，边际覆盖 1 迫使每项任务几乎处处恰选一次，于是识别真实调度。这个逃生口只说明更强合同可以识别本族，未给分离复杂度或通用算法。

# 3. 固定阶强配置矩的共同匹配障碍

## 3.1 精确系统和固定阶量词

稳定身份为 `UM-FIXED-DEGREE-STRONG-CONFIG-MATCHING-LAW-OBSTRUCTION-v1`。对每个固定整数 `r >= 2` 和奇数 `N >= 4r-1`，取 `N` 个互不相交的单位 `K_{2,2}` 块，得到 `2N` 台机器、`2N` 项任务、每个有限端耗时 1，真实 `OPT=1`。源提供次数至多 `2r` 的有理泛函，满足全局 moment matrix PSD、相应 one-hot、degree `r-1` 的负载 localizer PSD、每行 CONFIG 的全部 degree `2r` 矩相容，并使所有相容的短 mixed literal cylinder 非负。

否定的不是从一阶证书找某个最优匹配，而是更强的接口：要求一个真实完整 heavy matching 分布保留给定一阶和跨机器二阶，甚至允许保留每行的全部同阶 CONFIG 矩。对每个固定 `r`，证书大小和生成时间随 `N` 为多项式；`r` 作为输入时显式矩是 `N^{O(r)}`，不能写成关于 `r,N` 联合多项式。

## 3.2 正定性证明骨架

在 Boolean slice 上令 `t=N/2`，对 `|A|<=2r` 定义
\[
L(b_A)=(t)_{|A|}/(N)_{|A|}.
\]
记 `S=sum b_i`。递推 `a mu_a+(N-a)mu_(a+1)=t mu_a` 给出 `(S-t)P_{<=r-1}` 的 radical。齐次层用 up/down 算子
\[
D_{k+1}U_k-U_{k-1}D_k=(N-2k)I
\]
分解为 harmonic 空间 `H_k` 与上一层 up-image。对 `h,g in H_k` 按交叠数做二项反演，得到
\[
L(p_h p_g)=c_k\langle h,g\rangle,
\qquad c_k=(t)_k(N-t)_k/(N)_{2k}>0
\]
（`k<=r` 且 `N>=4r-1`）。不同 harmonic 阶互相正交，故 `M_r` PSD；短 mixed cylinder 则按包含排除给出
\[
L(\prod_{i\in A}b_i\prod_{j\in B}(1-b_j))
=(t)_a(N-t)_b/(N)_{a+b}>0
\]
于 `a+b<=2r` 的相容文字。

这里正性来自符号计算和 harmonic Gram，不是有限矩阵恰好通过数值特征值。`K_{2,2}` 编译不增加 Boolean degree；每行负载恒为 1，故 localizer 恒为零。源还给出一个两台私有机器/每项任务二选一的缩小编译，使失败可以落在“heavy 占用机器”二阶，而不是只落在块内标签。

## 3.3 非整数方差矛盾与锐修复半径

每块的两个完美匹配由 Boolean `B_s` 区分。若真实分布保留源矩，则
\[
E B_s=1/2,\qquad E(B_sB_u)=(N-2)/(4(N-1))\quad(s\ne u).
\]
令 `Q=sum_s B_s`，则 `E Q=N/2` 且 `E Q^2=(N/2)^2`，因此 `Var Q=0`；可是 `N` 为奇数，整数值 `Q` 不可能恒为半整数。只保持一阶时，任务覆盖期望为 1 且逐原子至多 1，又迫使完整匹配几乎处处成立，因此不能用部分匹配绕过矛盾。

允许保留一阶但修改跨块二阶时，所有真实完整匹配分布中的最小最大对误差精确为
\[
\Delta=1/[4N(N-1)].
\]
下界来自整数 `Q` 对半整数均值的方差至少 `1/4`；等号由以概率一半均匀选择大小 `(N-1)/2`、一半均匀选择大小 `(N+1)/2` 的块子集构成。这是强接口的修复半径，不是排程近似下界；它留下允许近似保矩重耦合的研究空间。

## 3.4 证据层级和外部背景

源列出 `Fraction` 审计、三组小矩阵的 Schur 消元、inclusion-exclusion cylinder 核对及冻结 JSON；其一般结论来自前述 slice/harmonic 证明，有限 `N` fixture 不承担任意 `N` 的量词。源引用 Potechin/Grigoriev 作为背景，但本批只接受正文自足证明，不把外部文献摘要替代为本源证明，也不把背景引用写成新的原创性声明。

# 4. 两源的逻辑关系、不能合并之处与用途

两源都区分“局部逐对象可验证”与“一个真实共同全局对象存在”。稀疏源的坏接口是不同边各自拥有完整配置点，却没有跨边共同相关性；强矩源的坏接口是一个共同低阶矩看似 PSD 且每行 CONFIG 相容，却不能由真实完整匹配律实现。两者都不证明一般配置 LP、任意 SA/SDP 层或 UM-TARGET-v1 失败。

它们不能直接拼接成更强的排程下界。稀疏族的 `OPT/T` 趋近 2 来自具体三选树—终端—共享汇点实例；强矩族每个实例 `OPT=1`，只否定保留给定二阶的真实 law。前者缺少共同矩，后者已有共同矩但缺少整数支持；缺口性质不同。强矩的二阶修复半径也不能直接给稀疏族一个可计算舍入误差，因为两者的状态空间、容量合同和任务域不同。

与既有《三选稀疏条件配置与资源星转移有限审查》相比，本页确认当前 source ID 的内容与旧审查的稀疏结论一致，并补充当前 blob 指纹、`UM-CONTRACTED-SPARSE-CONFIG-GAP-v1` 的端点收缩量词和“逆向不保 probe”边界。与既有《强配置矩与对称重置阈值有限审查》相比，本页只集成固定阶强矩 canonical；对称删机 pushforward 阈值是另一 source，不被错误合并到本批。

接入第三阶段关系图时，可建立两条有条件边：

1. `逐边完整配置证书 -> 缺失跨边共同相关性 -> 更强 bag 联合一致性可能识别`；
2. `固定阶 PSD/CONFIG 矩 -> 非整数全局计数 -> 共同 law 不可实现 -> 允许二阶修复才可能继续`。

边的标签应注明合同、量词和证据层级，不能把旧图摘要直接当作本批完成。

# 5. 证据、开放义务和逐源处置

**一般证明：** 稀疏源在声明参数族内的 `OPT=2-1/k`、逐有限边独立配置证书、端点互斥收缩/指定机器优先和收缩族终态结论；强矩源对任意固定 `r` 的 slice/harmonic PSD、短 cylinder 正性、K2,2 编译、非整数二阶 law 障碍及精确 `Delta`。这些结论不依赖把有限脚本当成证明。

**有限精确实验：** 稀疏 `k=3,H=5` 全展开审计、所有有限边 probe、`324` 次收缩和终态统计，以及压缩参数检查；强矩审计列出的有限矩阵/Schur fixture、cylinder 和方差检查。有限审计只证明所列实例和公式行，不扩大一般量词；程序不提供通用 configuration oracle。

**保留的障碍/反例：** 稀疏端点收缩缺外部互斥或不优先指定机器时的失败；逆向容量恢复不保原 probe；不同查询点无共同 base。强矩方面保留“只改动很小二阶即可重耦合”的开放方向，不把障碍说成排程不可行或复杂度下界。

**未闭义务：** 尚无跨查询共同相关性构造、低于 2 的一般稀疏合同近似、固定强矩的通用可计算修复/舍入算法，也无对六人 SPE 目标的结论。若后续研究这些方向，必须先明确是保留全部跨对象矩、只保边际，还是允许二阶修复，并重新写出真实任务覆盖与容量量词。

逐源记录：

- `6a58c5bfa643bbb8225a`：`integrated`。本页第 2 节及第 4、5 节写入其独有的参数族、逐边构造、收缩边界、强合同逃生口；相关旧审查作为比较材料，不重复登记为新的 source。
- `8cb84917989692a83f31`：`integrated`。本页第 3 节及第 4、5 节写入其固定阶矩定义、正定性证明、K2,2 真实 law 矛盾和 `Delta` 修复半径；对称删机阈值被明确排除在本批之外。

两源均为全文件实读、相关 canonical/review/程序/evidence 已比较；独有内容已在本页按对象分流，处置理由和第三阶段接续关系已明确记录。
