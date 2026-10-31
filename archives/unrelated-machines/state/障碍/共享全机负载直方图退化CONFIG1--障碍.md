---
id: "unrelated-machines/shared-global-load-histogram-config-equivalence"
kind: "obstruction"
type_tag: "障碍"
title: "共享全机负载直方图递推退化为 CONFIG1"
status: "proved-exact-equivalence-with-exponential-state-boundary"
summary: "保留所有全机相关性的精确 face递推可可靠拒绝且表达真实共同状态，但时间约为 (K+1)^m；最自然只共享 aggregate hull、各分支仅保本机 face 的弱递推恰等于 CONFIG1 负载直方图投影，继承趋二 gap。均值先截断再凸化有 4 机反例；nondominated frontier、full-support linear law 和逐机 matroid 包络也各有独立边界。"
source_refs:
  - "clean:32339e79dd0d675356b8"
  - "clean:e5ec6c458cfcfcec9dad"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_global_certificate_face_hull_frozen_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66f48:history/source/notes/unrelated_machines/sol_global_certificate_shared_hull_exact_statement.md"
---

# 来源身份和结论层级

两份来源共同审查“共享全机负载直方图/face hull”路线。第一份是冻结推导，第二份是 Exact-only 对象陈述；本轮完整实读。核心结论有两层：

1. 精确共同状态递推 H_j 保留同一完整前缀调度的机器负载直方图，可靠 FAIL，但显式状态最多 (K+1)^m，时间对机器数指数；
2. 为缩小尺寸而只保留 aggregate hull、各分支自己的容量面和行质量的自然弱递推，精确等于 CONFIG1 直方图投影，不能用它推出统一 sub-2 调度。

这不是一般 UM 算法下界，也没有声称所有非线性压缩都不可能。

| clean ID | 原路径 | SHA-256 | 大小 | 实读性质 |
|---|---|---|---:|---|
| `32339e79dd0d675356b8` | `history/source/notes/unrelated_machines/sol_global_certificate_face_hull_frozen_v1.md` | `4a0357981a3f9c3a3ac01e6a2432cb41f88f8e9edc8af76585a3e85abdfccba4` | 16,022 B | 完整读取保面递推、反例、指数表示界、matroid边界和弱递推等价证明 |
| `e5ec6c458cfcfcec9dad` | `history/source/notes/unrelated_machines/sol_global_certificate_shared_hull_exact_statement.md` | `f73acb0f0eb3b6741d1a8a854fbee1d507aadea2a8f2f5e3a533aee50740163a` | 4,080 B | 完整读取 Exact 对象、量词、CONFIG 投影恒等式和伪多项式 LP 合同 |

证据原件和 manifest 位于 `archives/unrelated-machines/tools/evidence/global-certificate-shared-hull-20261031/`，回执草稿在 `cleanup/workspaces/Boss2/global-certificate-shared-hull-receipts-20261031.json`。

# 1. 精确共同状态递推：可靠但指数

输入为一般 UM P、阈值 T>0、固定 rational δ∈(0,1)。去掉 p_ij>T 的端；若 job 无有限端，立即 FAIL。令 q=δT/n、K=floor(n/δ)、a_ij=floor(p_ij/q)。按 job 顺序保存完整机器负载状态：

`R_0={0}`，
`R_j={u+a_ij e_i : u∈R_(j−1), (i,j) finite, u_i+a_ij≤K}`。

同一个状态向量代表同一个完整前缀分配，不能把不同 state 的 coordinate marginal 重新配对。若 OPT≤T，真实 T 调度每台向下舍入负载不超过 n/δ，故逐 prefix 留在 R_j，R_n 非空；所以 FAIL⇒OPT>T。回溯 R_n 得完整 allocation，并有每机

`sum p_ij < q sum a_ij+nq ≤ (1+δ)T`。

每层最多 (K+1)^m states、每 state 至多 m 扩展，前驱表和有理整数操作总时间为 O(nm(K+1)^m)（另有输入位长多项式）。这是真实算法和可靠 FAIL，但不是关于机器数的位多项式。

# 2. 保面全机 hull 公式

整数负载向量 u 用每机的一位直方图编码 Φ(u)_(i,s)=1[u_i=s]。令 H_j=conv{Φ(u):u∈R_j}，它不是逐机直方图单纯形直积，不是 CONFIG1，也不把机器 coordinates 独立重排。

若第 j 个 job 送机器 i，定义 F_ij 为第 i 行禁止超过 K−a_ij 的暴露面；S_ij 将第 i 行 s→s+a_ij。严格恒等式为

`H_j = conv union_(i,j finite) S_ij(H_(j−1) intersection F_ij)`。

原因是：若 y∈F_ij 写成正权原子 y=sum θ_r Φ(u^r)，坏坐标 indicator 的非负加权和为零，故每个正权原子都通过同一容量面；不能用平均负载替代 face。反向显然。

显式 EF 若复制每个分支的旧 formulation，尺寸递推 D_j≤mD_(j−1)+poly(mK)；层状状态网络有 Θ(n(K+1)^m) 节点。环境维度多项式不等于 membership/separation 可计算，也不能把公式直接写成 polynomial-time LP。

# 3. 先截断平均再凸化的实际反例

所有 unit jobs、m 台相同机器、n=m+1、容量 B=1+1/m。只存平均负载集合

`A_j=conv union_i ((A_(j−1)+e_i) intersection [0,B]^m)`。

当 j≤mB 时，A_j 恰为 `{z∈[0,B]^m: sum z_i=j}`；因此最终接受 z=(B,…,B)，但真实 OPT=2，ratio `2m/(m+1)→2`。最小 m=2、n=3、B=3/2 时，第二层幽灵均值 (3/2,1/2) 再到 (3/2,3/2)，没有任何真实完整调度实现。CONFIG 在 B<2 会拒绝，所以这不是新 CONFIG gap，而是“容量截断和凸化可交换”错误。

# 4. 其它表示边界

- **共同 nondominated frontier：** m=2k、n=k、T=1，每 job 只在 pair (2j−1,2j) 上耗时一。2^k 个选择的共同负载向量两两 incomparable，总负载相同；显式 antichain/dominance 表仍指数，但不排除非线性表示。
- **full-support linear law：** n=m、p_ij=1、T=1、扩容 B=2−ε。任何完整共同容量 law 对全部 m! 排列赋正权。按前 k jobs/后 m−k jobs flatten，选每个 k-set 的 prefix/suffix，得到正对角矩阵，rank≥C(m,k)。任何 job-order matrix-product/weighted-automaton 宽度 d≥C(m,k)，中点给 2^m/(m+1)。这打击 full-support 线性状态压缩；Dirac law 或非线性 prefix oracle 仍可能小，故不是一般算法下界。
- **逐机 matroid sandwich：** 单行 T=1 有一个 big 时间一元素 b、k 个 small 时间 1/k。若 matroid 同时包含 {b} 和全部 small k-set，增广公理强迫某个大小 k、含 b 的 independent set，负载至少 2−1/k；不能得到统一固定 (2−ε) 的逐机 matroid 包络。全机相关的非逐行机制不被排除。

# 5. 弱共享 aggregate 递推与 CONFIG1 的精确等价

弱递推保留分支权 θ_i、每分支每行总质量 θ_i、aggregate `sum_i z^i∈H_(j−1)`、分支 i 的本机容量面和输出 `y'=sum_i S_ij z^i`，但删除 `z^i∈θ_i H_(j−1)`。其尺寸可逐层线性增加，因此是真正的共享 EF 候选。

令 P_j 是前 j 个 jobs、整数时间 a_ij、每机容量 K 的 CONFIG1 负载直方图投影（每机独立配置分布、job cover 等式，不假设跨机器共同 coupling）。精确恒等式：

`widehat H_j = P_j`。

**弱递推⇒CONFIG：** 对每机 r、阶段 ℓ、旧 load s，定义 add=z^r_(r,s)、stay=sum_(i≠r)z^i_(r,s)。两类流在 subset-sum DAG 上分别把质量保持或移动 s→s+a_rℓ；层状单位流分解为配置路径。每 job 的机器覆盖概率是 sum_r θ_(r,ℓ)=1，最终直方图相同。

**CONFIG⇒弱递推：** 给每机独立配置分布，令 x_rℓ=Pr(job ℓ∈C_r)，前缀 load 分布 v^+、v^-。分支 i 在自身行取 v^+；其他行按 `x_iℓ v^-/(1−x_rℓ)` 分配，x_rℓ=1 时由 cover 等式强迫所有 i≠r 的 x_iℓ=0，故无除零。各分支 aggregate 恰回旧直方图、本机面通过，移后得到新的 P_j。此构造只需逐机配置分布，不要求一个全局 schedule coupling。

因此任何只保 aggregate、行质量和本机 face 的共享 EF，数学上就是 CONFIG1，继承其趋二 gap；不能以“旧 hull 只查询一次”声称保留跨机器相关性。

# 6. 四机六 job 的幽灵反例

容量 T=1，a=2/3、b=1、d=1/3。前四 jobs 的矩阵：机器1可 j1=b、j4=a、A=d；机器2可 j1=a、j2=b、A=d；机器3可 j2=b、j3=a、B=d；机器4可 j3=b、j4=a、B=d；A/B 为 aux。前四 jobs 的真实旧 hull 是两个完美匹配 `(b,b,a,a)` 与 `(a,a,b,b)` 的凸包；CONFIG 每行各半选择本行 b-prefix 单件或 a-prefix+aux，阈值精确为一。

弱共享递推先对两旧前缀各取 1/2，再以 A 的两个分支分别拆行质量，aggregate 保持旧 hull、本机 face 通过；移后机1、2恒 b，机3、4各半 a/b。再以 B 分支拆行，可得到 Dirac `(b,b,b,b)`，但真实旧 hull 只能从第二个前缀放 A，因而该点不可达。加入最后两个 jobs 后真实 OPT=4/3；弱递推却接受容量一。这是共享分支分解破坏共同相关性的具体反例，不是新的 CONFIG gap family。

# 7. 计算合同与接续义务

整数网格的 CONFIG1/weak hull 可用 subset-sum DAG 单位流 LP 表示，规模 O(mnK+|E|(K+1))，zero-time job 用带标签的 parallel arcs；K 二进制时为伪多项式。对一般有理 P 取 q=δT/n、K=floor(n/δ)，构造、判定、有理证书位长关于输入和 1/δ 多项式；可行不承诺小于 2T 的实际 schedule。不可行 Farkas 证书可靠蕴含 OPT>T。

当前路线真正保真的方案是精确 face hull H_j，但其状态数关于 m 指数。若要继续，需给出一个关于机器数位多项式的非线性共同状态：OPT≤T 时不误删全部真实前缀；成功时能解码同一完整 σ≤(2−ε)T；删光时 sound FAIL；生成、查询和解码均位多项式。环境维度、局部平移、Dirac 存在性或容易写的价格支持函数都不足以支付该接口。

# 本轮实际处置

两源均完整实读，比较精确 face 递推、可靠 FAIL、指数状态、均值截断反例、nondominated/frontier 与 rank 边界、逐机 matroid 限制及弱共享递推与 CONFIG1 的双向精确等价。没有运行程序；原件和 manifest 在 evidence，正文归档为障碍，回执草稿单列。
