---
id: "unrelated-machines/diluted-shared-terminal-fixed-d-whole-row-config-five-source-read-after-20261031"
kind: review
type_tag: 审查
title: "稀释共享终端 fixed-d 全行 CONFIG 五源读后"
status: integrated-independent-plus-read-after
truth_status: "fixed-d-row-contract-gap-with-scoped-section13"
review_level: "exact-first-reconstruction-plus-author-read-after-and-final-section-read-after"
scope: "diluted shared-terminal row-degree d; all affine localizers, degree-d row moments, and final §13 limits"
summary: "Exact-first、作者证明读后和最终 §13 读后共同支持固定 d 的 whole-row CONFIG/affine-localizer 合同与 OPT=2-floor(sqrt(k))/k；higher-degree/cross-row 条件和软件审计均保持边界。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_general_repair_diluted_row_degree_d_exact_first_reconstruction_v1.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_general_repair_diluted_row_degree_d_exact_first_reconstruction_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_general_repair_diluted_shared_terminal_row_degree_d_author_proof.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_general_repair_diluted_shared_terminal_row_degree_d_author_proof.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_general_repair_diluted_shared_terminal_raw_k2_with_row_degree_final_v1.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_general_repair_diluted_shared_terminal_raw_k2_with_row_degree_final_v1.md"
source_ids:
  - "0519394159af11fcb87f"
  - "3063f78afa180a180724"
  - "4f6d50940baa581d60d6"
source_sha256:
  - "4294c156fa6feb502b6c3e90bec6c0bd8fb9e8e5ecc4008c2cf9b71838cf3447"
  - "c3ac3d56ef9ae27b1b4041adf7b8bb91b78c63b303f7fc27d3a70757672081d6"
  - "a2807db48cff732c57147cb0b54db28111dc543738750cacc9b6e00f742b1b3b"
evidence_paths:
  - "../../tools/evidence/diluted-shared-terminal-row-degree-20261031/source/0519394159af11fcb87f.md"
  - "../../tools/evidence/diluted-shared-terminal-row-degree-20261031/source/3063f78afa180a180724.md"
  - "../../tools/evidence/diluted-shared-terminal-row-degree-20261031/source/4f6d50940baa581d60d6.md"
related_objects:
  - "稀释共享终端row-degree最终section13读后增量--审查.md"
  - "稀释共享终端rawK2与终端探针共同间隙双源审查--审查.md"
  - "Sol通用repair-k2全局local-law与canonical-pullback三源审查--审查.md"
---

# 读取顺序与版本边界

`0519394159af11fcb87f` 是 fixed-(d) Exact-first 独立重构（11,393 字节，SHA
`4294c156...cf3447`），完整给出参数、实际 OPT、有限 functional、CONFIG 行和
全局 affine localizer；`3063f78afa180a180724` 是作者 Proof 的读后比较（5,876 字节，
SHA `c3ac3d...081d6`），未运行作者 enhanced code；`4f6d50940baa581d60d6` 是最终
raw-K2-with-row-degree 稿新增 §13 的后置读后（4,370 字节，SHA `a2807d...b1b3b`），
只完整读取新增 §13，旧前缀仅作长度/hash 身份检查。三源原件与 SHA 在 evidence 目录
保留。故本页把 exact-first 作为独立数学重构，把作者和 §13 只按其实际读取范围整合，
不把未来软件重放写成已由本页完成。

# 1. fixed-d 普通矩阵与实际最优值

固定 (d\ge2)、(k\ge d)，令 (s=d-1,L=2k^2)。每 component 有一个 (U)、
(L) 个 (B)、(k) 个 terminals；全局 unit (h) 可去一个 (U)。每枚 (f) 在
(U) 的 tiny 时间为 (1/k)，在所有 (B) 有 unit 端；每枚 (e) 在其 (B) 的 tiny
时间为 (1/k)，在全部 terminals 有 unit 端。完整原矩阵计数为

\[
\text{machines}=M(1+L+k),\quad
\text{jobs}=1+Mk(1+L),
\]
\[
\text{finite endpoints}=M+Mk(1+L)+MLk(1+k).
\]

所有原 jobs 必须执行，未列端点为 ∞；不允许因 law 中未选 assignment 而删除工作。
令 (r=\lfloor\sqrt{k}\rfloor)。上界把 (h) 从一个 (U) 移走 (r) 枚 (f)，再
从 (r) 个 (B) 各移 (r) 枚 (e) 到 (r^2\le k) 个 terminals，峰值为
(2-r/k)。若峰值 (C<2-r/k)，被 (h) 影响的 (U) 必输出至少 (r+1) 枚 (f)，
这些 unit (f) 占据不同 (B)；每个此类 (B) 又必须输出至少 (r+1) 枚 (e)，但仅
(k) 个 terminals 可接 unit (e)，矛盾。故完整 assignment 量词下

\[
\operatorname{OPT}=2-\frac{\lfloor\sqrt{k}\rfloor}{k}.
\]

这是真实 ordinary schedule 的精确值，不依赖样本 law；缩放 (k/(k+s)) 后目标可归一
到 1，固定 (d) 且 (k\to\infty) 时该 gap 趋近 2 的上侧。它不是一般 UM 近二障碍。

# 2. 有限 law、subset 插值与 whole-row CONFIG

共同 functional 由 (h) 先选 component (I)：被选 component 用 foreground (H)，其余
用 background (Q_{new})。(Q_{old}) 为 all-home、单 (f)+terminal permutation、
或单 (e) 分支的混合；(R_{fill}) 给指定 (B) 以至多 (s) 个 home (e) 的合法填充。
每个样本均是真实有限端点 assignment，保留 same-job exclusion 和 original job cover
identities；这只定义 joint functional，不等于所有 samples 都满足阈值 (T=1+s/k)。

对每个 (S\subseteq[k])、(|S|\le s)，令

\[
b_S=(-1)^{s-|S|}\binom{k-|S|-1}{s-|S|}.
\]

生成函数恒等式给出对任意 (A\subseteq[k])、(|A|\le s) 的
(\sum_{S\supseteq A}b_S=1)。于是 fixed-(B) 行中：pure-home 的 degree-(d) monomial
在 corrections 中完全相消；含一个 incoming unit 与 (r\le s) 个 distinct home
端点的 monomial 在 H 与配置 mixture 中相同；至少两个不同 incoming unit 的行 monomial
两边均为零；重复 factors 按 Boolean 化简。因而每台机器所有 degree≤d endpoint
monomials 都匹配，而不是只核 diagonal 或 first/pair。

作者 Proof 读后另核了 (c)-norm localizer 路线：任意 local affine (q) 的系数满足

\[
\|c\|^2\le[12kL+12Lk^3+6kL(k-1)^2]E_{Q_{old}}q^2
\le30Lk^3E_{Q_{old}}q^2.
\]

background 至少给 ((1-a)\|c\|^2/(60Lk^4)) 的正 slack，foreground 的负项至多
(2a\|c\|^2)；当 (M-1\ge120Lk^4) 时跨 component 条件方差吸收全部负项。
这覆盖 arbitrary global affine (q)（外部 component 均值吸收入 intercept），但不覆盖
joint CONFIG selector M2 或更高阶 event/load localizer。

# 3. 生成性与固定 d 的严格范围

令 (D=\max(4,d))。固定 (d) 时，(Z\le(s+1)k^s)、(A_{max}\le k^s)，作者的
吸收项使 (M\) 及完整 dense matrix、CONFIG rows 和 degree-(D) moment generator
都随展开输入长度多项式增长；指数可以依赖固定 (d)，不代表把二进制 d 当 variable
时的统一多项式算法。有限-law 生成只枚举至多 (D) 个被查询 endpoints，冲突与不够
destinations 直接置零，不除以零 falling factorial，也不枚举 (k!) 个 permutations。

这些是有限和的位复杂度与数学构造说明；assigned source 没有运行 enhanced audit、
没有读取作者 JSON/code，也没有外部新颖性或 hardness 认证。

# 4. §13 后置边界与不外推项

最终 §13 读后保留以下两条关键边界：

1. 给定 law 中 (A_i=1) 与 (B_{i,b}) incoming 的跨行 event 具有
   (F[A_iC_{i,b}(T-load_B)]=a(k/L)(T-2)<0)，所以把 joint cross-row event 条件
   加入合同会切掉此证书；它不是当前 affine-(q^2) 合同的矛盾。
2. 取一个 incoming (f) 与 (d) 个 distinct home (e) endpoints，真实 law 的
   degree-((d+1)) mixed monomial 为 (a/L>0)，而阈值配置最多允许 (s=d-1) 个
   homes，因此新增 moment 会变为 0。若 (d+1>D)，这只说明给定 finite law 的自然
   延伸失败，不能声称所有 degree-(D) extension 都不可能。

有限 trade audit 仅覆盖 ((d,k)=(2,2),(3,3),(4,4),(4,7))，分别 11、42、163、
1471 个 squarefree row monomials；未枚举 global M2/localizers，不能把数量升级为一般
证明。旧 k=2 first/pair 结果和未来 CLI 重放均需沿各自 evidence/receipt 处理。

# 5. 处置与接续

三源合一为本 fixed-d row-degree 对象的版本 provenance：Exact-first 提供独立关键
代数和 OPT 下界，作者读后核 finite-difference、正质量吸收与 global affine contexts，
§13 只补最终版本的时序、row-degree 量词和跨行/higher-degree 负项。相关 raw K2 与
§13 v2 页已承载后续版本；本页不新造一般定理。

第三阶段可连成 `raw K2 → fixed-d whole-row extension → cross-row/higher-degree
obstruction`。仍开放 joint CONFIG/SDP 可行性、higher-event 合同、一般 UM hardness、
全局 schedule law 和六人 SPE half 主命题。
