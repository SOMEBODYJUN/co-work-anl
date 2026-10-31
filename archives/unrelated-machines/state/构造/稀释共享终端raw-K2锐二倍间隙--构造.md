---
id: "unrelated-machines/diluted-shared-terminal-raw-k2-gap"
kind: construction
type_tag: 构造
title: "稀释共享终端 raw K2 锐二倍间隙"
status: proved-in-stated-raw-contract
truth_status: exact-optimum-and-explicit-rational-certificate-with-author-proof
review_status: source-exact-and-author-proof-read; no-new-independent-blind-proof
summary: "对每个 k≥2 构造显式普通不相关机矩阵，真实 OPT=2−⌊√k⌋/k；在仅有 degree-4 common moment/M2、逐机 first/pair CONFIG 与全局 affine-load localizer 的 raw K2 合同中给出多项式位长有理证书，缩放后 gap 趋于 2。"
legacy_ids:
  - SCRATCH-UM-DILUTED-SHARED-TERMINAL-RAW-K2-GAP-v1
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_diluted_shared_terminal_raw_k2_exact_only.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_diluted_shared_terminal_raw_k2_author_proof.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_diluted_shared_terminal_raw_k2_exact_only.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_diluted_shared_terminal_raw_k2_author_proof.md"
evidence_paths:
  - "../../tools/evidence/diluted-shared-terminal-raw-k2-20261031/manifest.json"
  - "../../tools/evidence/diluted-shared-terminal-raw-k2-20261031/original/sol_diluted_shared_terminal_raw_k2_exact_only.md"
  - "../../tools/evidence/diluted-shared-terminal-raw-k2-20261031/original/sol_diluted_shared_terminal_raw_k2_author_proof.md"
related_objects:
  - "稀释共享终端row-degree固定阶间隙--构造.md"
  - "稀释共享终端rawK2与终端探针共同间隙双源审查--审查.md"
---

本文把两份冻结原件的 exact construction 与作者 proof 合并为一个可复用对象。原件 SHA-256 分别为 exact `25888ec48d8000769bcf5d8d2c4ab9cf29825e9084d1f5bb888de6be7c44210b`、proof `2e926c6471c68843602f78c101874198e0ad2808b8db12d737cc8a04f27ad948`；原文副本和大小见证据 manifest。Proof 是作者 proof/read-after，不是本轮新增盲审；本页只承重下述明确合同。

# 1. 普通矩阵和真实最优值

给整数 (kge2)，令
[
 L=2k^2,qquad M=1+60Lk^4,qquad T_0=1+1/k.
]
有 (M) 个物理上互不相同的组件。组件 (i) 含机器 (U_i)、(L) 台 (B_{i,b})（(bin[L])）和 (k) 台终端 (Z_{i,t})（(tin[k])）。有一个选择任务 (h)，在每台 (U_i) 用时 1；每个 (f_{i,j}) 在 (U_i) 用时 (1/k)，在任一 (B_{i,b}) 用时 1；每个 (e_{i,b,ell}) 在 (B_{i,b}) 用时 (1/k)，在任一 (Z_{i,t}) 用时 1；其余端不可用。每个任务不可拆且恰执行一次。

真实最优 makespan 为
[
 \operatorname{OPT}(P_k)=2-\frac{\lfloor\sqrt{k}\rfloor}{k}.
]
下界：设一份完整调度峰值 (t<2)，并令 (h) 位于 (U_i)。至少有
(r=k-lfloor k(t-1)\rfloor) 个 (f) 从 (U_i) 导出；因每个 (B) 不能承受两件 unit 任务，这些 (f) 占据不同 (B)。每个被占 (B) 至多能把 (lfloor k(t-1)floor) 个自己的 (e) 留在 home，故至少导出 (r) 个 unit (e) 到 (k) 个终端；终端不重叠给出 (r^2le k)，于是 (tge2-lfloorsqrt{k}floor/k)。上界由选定 (s=lfloorsqrt{k}floor) 个 (f) 到不同 (B)，每个选定 (B) 导出 (s) 个 (e) 并把这 (s^2) 个 unit 任务放到不同终端；其余任务留在 tiny home。该调度在选定 (U,B) 行达到 (2-s/k)，其余行不超过 1。

# 2. raw K2 合同

共同 functional (F) 只定义到 degree 4，(F(1)=1)，满足 Boolean 与同任务互斥/one-hot 方程（按允许次数乘子），并要求 degree-2 单项式上的 (M_2) PSD。每台机器只要求一个合法 CONFIG( (T_0) ) 分布匹配 (F) 在该机 endpoint 的一阶和同机二阶矩。另对每台机器 (v) 和任意含全输入 endpoint 的 affine (q) 要求
[
F[(T_0-\operatorname{load}_v)q^2]\ge0.
]
该 raw 合同不含 export\(\le\)activation、inactive-all-home、精确 active-tail、joint CONFIG 变量或产品事件 localizer；不能把它称为 canonical C2、S3 或一般 SDP。

# 3. 完整有限法则与 local CONFIG

先均匀抽取组件选择器 (I)，把 (h) 放到 (U_I)。选中组件用 (H)：均匀抽取注入 (sigma:[k]\hookrightarrow[L])，每个 (f_{i,j}) 放到 (B_{i,sigma(j)})，全部 (e) 留在 tiny home。未选组件用 (Q)，三种情况的概率为 (1/2,1/4,1/4)：全 home；随机选 ((j,b))，把一个 (f_{i,j}) 放到 (B_{i,b})，并以均匀双射把该 (B) 的 (k) 个 (e) 送到终端；或只把一个随机 (e_{i,b,ell}) 送到随机终端。每个样本都是完整 assignment，令 (F(p)=\mathbb E[p])。因此所有 Boolean/one-hot 方程和 (M_2) PSD 都来自同一有限概率法则。

(U) 与终端直接使用真实 row marginal，样本中负载至多 1。对固定 (B_{i,b})，令 (p=ak/L)、(b_0=c_0=(1-a)/(4L))、(a=1/M)。用五类合法 CONFIG：

- 一件 unit (f)+一件 home (e)，总质量 (kp)；
- 一件 unit、无 home (e)，质量 (b_0-(k-1)p)；
- 无 unit、无 home (e)，质量 (p)；
- 无 unit、恰 (k-1) 件 home (e)，质量 (c_0-kp)；
- 无 unit、全部 (k) 件 home (e)，质量 (1-b_0-c_0+(k-2)p)。

标签均匀抽取。各质量非负，因为 (M-1=60Lk^4)；所有配置负载至多 (1+1/k=T_0)，并与 (F) 的 (B)-row 一阶和 distinct-pair 矩完全相同。终端每个 incoming singleton 概率为 ((1-a)(k+1)/(4Lk^2))，同机 pair 为零。

# 4. 全局 affine localizer 的无维度证明

固定一个 (B) 行，写 (g=T_0-\operatorname{load}_B)。在 (Q) 下逐点 (g\ge1/k)。在 (H) 下 (g=1/k-1\{\sigma([k])\text{ 选中该 }B\})，故 (\mathbb E_Hg=1/(2k))。把每组件 home endpoint 消去后，组件内 affine 表达式写成
(q=\beta+\sum c_{j,b}F_{j,b}+\sum d_{b,\ell,t}G_{b,\ell,t})，并记 (\|c\|^2=\sum c_{j,b}^2)。对所有 (eta,d) 有
[
\mathbb E_Q[q^2]\ge \|c\|^2/(30Lk^3),\qquad
\mathbb E_H[gq^2]\ge-2\|c\|^2.
]
第一式由 Q 的全 home、单 (e) 导出和单 (f)+双射三类样本逐项平方界得到；第二式令 (S=sum_jc_{j,sigma(j)})，用 (\mathbb E S^2\le(k/L)\|c\|^2) 与对任意截距 (eta) 的 completing-the-square。选择 (a=1/M) 后
[
F[gq^2]\ge((1-a)/(30Lk^4)-2a)\|c\|^2\ge0.
]
对含所有组件 endpoint 的全局 affine (q)，条件于 (I=h) 后组件独立；把其他组件的条件均值吸收到任意 (eta_h)，其条件方差项乘以正的 (\mathbb E[g\mid I=h]) 并可丢弃。因此上述界不随组件数 (M) 或全输入变量数增长。(U) 和终端因 (g\ge1/k) 点态成立。

# 5. 证书规模、缩放和边界

degree-4 moment 表、CONFIG 列表与 localizer 矩阵均可由最多四个 queried heads 的 partial-injection/permutation 概率生成；输入端点数的四次多项式大小、分母和 bit length 均多项式。该断言是**指定证书的生成**，不是一般 SDP 可行性算法，也不要求枚举指数支持。

把全部 processing times 乘 (k/(k+1))，目标变为 1，真实 OPT 为
[
\frac{2-\lfloor\sqrt{k}\rfloor/k}{1+1/k}\to2.
]
由于 raw K2 的任一首阶 CONFIG 仍给标准 slot 上界 2，故这个 raw 合同的 gap supremum 为 2（在本对象输入域内）。

当前法则明确失败于更强的产品事件条件：若 (A_i) 是 selector endpoint、(C_{i,b}) 是选中 (B) 的 unit occupancy，则
(F[A_iC_{i,b}(T_0-\operatorname{load}_B)]=a(k/L)(T_0-2)<0)。因此该对象不能外推到 cross-row event localizer、joint CONFIG-M2、canonical inactive-home 或一般 UM hardness。没有把旧 finite audit 或其他模型的结果回写成对本构造的独立软件认证。
