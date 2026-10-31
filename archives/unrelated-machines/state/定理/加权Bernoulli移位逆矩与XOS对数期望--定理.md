---
id: "unrelated-machines/weighted-bernoulli-shifted-inverse-moment-xos-log"
kind: "theorem"
type_tag: "定理"
title: "加权 Bernoulli 移位逆矩与显式 XOS 对数期望"
status: "exact-statement-author-proof-independent-review-pass"
truth_status: "proved-under-finite-independent-bernoulli-and-explicit-nonnegative-xos-hypotheses"
review_level: "four-source-full-read"
summary: "有限独立 Bernoulli 和 Z=sum a_jX_j（0≤a_j≤1）的移位逆矩满足 E[1/(1+Z)]≤(1−e^(−mu))/mu≤1/mu；缩放给 E ln(V/(nu+W))≤ln(V/M)。若 v 是有限非负 XOS、S 上某 clause 达到 v(S)>0，且 T 中 S 元素独立入选概率至少 p，则 E ln(V/(nu+v(T)))≤ln(V/(p v(S)))。四源 Exact/Proof/independent/read-after 一致；不含下游 NSW、同时高概率、相关抽样或一般 subadditive 推广。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/weighted_bernoulli_shifted_inverse_moment_statement_only_v1.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/weighted_bernoulli_shifted_inverse_moment_statement_only_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/weighted_bernoulli_shifted_inverse_moment_author_proof_v1.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/weighted_bernoulli_shifted_inverse_moment_author_proof_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/weighted_bernoulli_shifted_inverse_moment_independent_exact_review_v1.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/weighted_bernoulli_shifted_inverse_moment_independent_exact_review_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/weighted_bernoulli_shifted_inverse_moment_author_proof_read_after_review_v1.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/weighted_bernoulli_shifted_inverse_moment_author_proof_read_after_review_v1.md"
source_ids:
  - "cd8ee4486314984e57a1"
  - "f6c98a438711ec00193b"
  - "4ce240477c77fb47dd8f"
  - "dd15ed3674746109dad4"
related_objects:
  - "unrelated-machines/fractional-rematching-normalized-xos-robust-gap"
evidence_manifest: "../../tools/evidence/weighted-inverse-moment-sources-20261031/source-manifest.json"
---

# 1. 四份来源与证据等级

本批完整读取四份冻结文件。双冻结提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 和 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 的同路径版本视为同一材料。

| 稳定 ID | 冻结路径 | 字节 / SHA-256 | 角色 |
|---|---|---:|---|
| `cd8ee4486314984e57a1` | `history/source/notes/unrelated_machines/weighted_bernoulli_shifted_inverse_moment_statement_only_v1.md` | 1377 / `148cfe5ba2f6da74d9ce178281310373a31a057db2cfb0811216a4f7332c5801` | statement-only：精确命题与 XOS 推论，无证明 |
| `f6c98a438711ec00193b` | `history/source/notes/unrelated_machines/weighted_bernoulli_shifted_inverse_moment_author_proof_v1.md` | 1713 / `891c56ecb28481957e93adb3e70e80ae946e152d440e901aebcdcb17421584c7` | author Proof：凸性、Laplace 积分、缩放和 XOS 证明 |
| `4ce240477c77fb47dd8f` | `history/source/notes/unrelated_machines/weighted_bernoulli_shifted_inverse_moment_independent_exact_review_v1.md` | 7339 / `1c2649e6e1c85412c41ab30979d3f8dca6d2c2b205ac8e6419b7da14eb77b284` | independent Exact-first：独立证明、严格性/极限锐性和边界攻击 |
| `dd15ed3674746109dad4` | `history/source/notes/unrelated_machines/weighted_bernoulli_shifted_inverse_moment_author_proof_read_after_review_v1.md` | 3628 / `7130d51bf65187a75a80daad756bd04c55b8c26da6de4e8240e40ff1791db044` | author Proof read-after：逐项复核与范围限制 |

四份材料互补，不是四次独立实验：Exact 给语义，作者 Proof 给首个正式推导，independent review 在未读作者 Proof 时独立重构，read-after 是知情后置比较。证据副本和 manifest 位于 `archives/unrelated-machines/tools/evidence/weighted-inverse-moment-sources-20261031/`。

# 2. 逆矩定理

设有限索引集 `J`、独立 Bernoulli `X_j~Bernoulli(p_j)`，权 `0<=a_j<=1`，
\[
Z=\sum_{j\in J}a_jX_j,\qquad
\mu=\sum_j a_jp_j.
\]
若 `mu>0`，则
\[
\mathbb E\frac1{1+Z}
\le \frac{1-e^{-\mu}}{\mu}
\le\frac1\mu.
\]
若 `J` 为空或 `mu=0`，非负性迫使 `Z=0` a.s.，故期望恰为 1。命题是有限离散语义结论，未声称用有理算法精确计算 `e^{-mu}`。

## 2.1 证明

对任意 `z>=0`，
\[
\frac1{1+z}=\int_0^1t^z\,dt.
\]
当 `0<t<1` 时，`a↦t^a` 在 `[0,1]` 上凸，故弦线给出
\[
t^{a_j}\le1-a_j+a_jt.
\]
有限独立性于是给出
\[
\mathbb E[t^Z]
=\prod_j(1-p_j+p_jt^{a_j})
\le\prod_j(1-a_jp_j(1-t))
\le e^{-\mu(1-t)}.
\]
有限 support 允许交换积分与期望，故
\[
\mathbb E\frac1{1+Z}
\le\int_0^1e^{-\mu(1-t)}dt
=\frac{1-e^{-\mu}}\mu
\le\frac1\mu.
\]
`mu=0` 分支单独如上处理，无隐藏的除零或连续延拓。

independent review 进一步核对：在有限 `J` 且 `mu>0` 时第一不等式实际严格，因为至少一个 `a_jp_j>0`，但它作为上界在稀疏极限 `a_j=1,p_j=mu/n,n→∞` 下可逼近，故常数是极限锐的；这一强化不是后续推论的必要假设。

# 3. 加权缩放与对数期望

设 `nu>0`、`0<=w_j<=nu`，
\[
W=\sum_jw_jX_j,\qquad M=\sum_jw_jp_j>0.
\]
取 `a_j=w_j/nu`，则 `Z=W/nu`、`mu=M/nu`，得到
\[
\mathbb E\frac1{nu+W}
\le\frac{1-e^{-M/nu}}M
\le\frac1M.
\]
对任意 `V>0`，正随机变量 `V/(nu+W)` 上的 Jensen 给出
\[
\mathbb E\ln\frac V{nu+W}
\le\ln\mathbb E\frac V{nu+W}
\le\ln\frac VM.
\]
不要求 `V>=M`，也不要求这些对数非负；正移位 `nu` 和有限 support 保证所有对数/期望有限。若 M=0，右端 `ln(V/M)` 不定义，不能把零均值分支混入该式。

# 4. 显式非负 XOS 推论

设 `v` 是有限个非负 additive clauses 的最大值：
\[
v(A)=\max_{\ell\in L}\sum_{j\in A}b_{\ell j},\qquad b_{\ell j}\ge0.
\]
取给定有限 `S` 上达到 `v(S)>0` 的 clause `ell_*`，令 `w_j=b_{ell_*j}`（`j∈S`）。则
\[
\sum_{j\in S}w_j=v(S),\qquad0\le w_j\le v(\{j\})\le nu.
\]
令 `T` 中 `S` 的元素独立入选，实际概率 `p_j>=p>0`，并定义
\[
W=\sum_{j\in S}w_j1[j\in T],qquad
M=\sum_{j\in S}w_jp_j\ge p,v(S)>0.
\]
该同一 clause 对每个 T 给点态下界
\[
v(T)\ge\sum_{j\in T\cap S}b_{ell_*j}=W,
\]
即使 T 含 S 以外元素也不影响。因为 `x↦ln(V/(nu+x))` 随 x 下降，
\[
\mathbb E\ln\frac V{nu+v(T)}
\le\mathbb E\ln\frac V{nu+W}
\le\ln\frac V{p,v(S)}.
\]
这里不使用 submodularity，只使用有限显式 XOS、非负 clause 和 S 上独立入选。不同 `p_j` 允许不相等；不推出 correlated inclusion 或 generic subadditive valuation 的结论。

# 5. 四源比较、边界攻击和与下游对象的隔离

- statement-only 只陈述以上命题，明确它是 semantic real-parameter lemma，不是 transcendental exact-evaluation algorithm。
- Author Proof 的核心是 `t^a` 弦不等式、独立 product、`1-x<=e^{-x}`、积分、缩放、Jensen 和 XOS supporting clause；没有额外抽样、oracle 或高概率步骤。
- Independent review 在未读 author Proof 时独立重构同一证明，检查 `mu=0`、空集、正对数域、严格性/极限锐性，以及 weight cap 与 independence 的必要性：例如单项 `a=2,p=1/2` 或完全相关的两个 unit terms 给 `2/3`，但它们分别违反 `a<=1` 或 independence，不能反驳本定理。
- Read-after 逐项确认作者 Proof 与独立证明一致，且没有把 standalone lemma 偷换成 downstream NSW constant 或 general subadditive guarantee。

本对象与现有“分数重匹配、归一化 XOS 与稳健小质量缺口”对象的关系是局部数学引理依赖：该引理可以在显式 XOS rounding 的 candidate-local shifted weights 中作为条件工具，但它本身不证明 residual lift、finite mask DP、matching 常数或 unit-FSLP backend。尤其不能用本 lemma 自动认证 `1/1,125,000`、`2^{-24}` 等下游常数；那些依赖各自作者 Proof 和未审计的全链实现。

# 6. 真值层级与实现边界

**精确已证。** 有限独立 Bernoulli、`0<=a_j<=1` 的逆矩不等式；加权 `nu` 缩放；有限非负显式 XOS 在 S 上独立入选概率下的对数期望推论。

**不包含。** 没有 simultaneously-high-probability 事件、多个 agents 联合保证、correlated inclusion、一般 subadditive valuations、NSW approximation、promise reduction、精确有理 exp/log 计算、代码或有限实验。

**接续。** 若下游使用该引理，必须明确给出：每个 `a_j=w_j/nu` 确在 `[0,1]`；入选 indicators 在所用 S 上真正独立；selected XOS clause 是有限显式 clause 且 `v(S)>0`；shift `nu>0`；并单独审计所有 candidate-local floor、DP、matching 和成功事件量词。第三阶段可建立“XOS rounding → shifted inverse-moment tool”边，但不能直接建立“tool → full NSW theorem”边。

本批四源正文、证据与 receipt 已写好；未执行 commit、push 或 clean done。
