---
id: "unrelated-machines/raw-k2-14m-direct-canonical-pullback-obstruction"
kind: "obstruction"
type_tag: "障碍"
title: "固定14机原始 K2 证书的同点 canonical 乘积拉回失败"
status: "exact-fixed-certificate-narrow-obstruction"
truth_status: "proved-for-the-specified-certificate"
summary: "一个固定的14台机器、13个作业、26个有限端点的物理 K2(P,7/4) 有理证书满足全局 M2、全部 raw affine load localizer 和逐机 first/same-machine-pair CONFIG 合同，且实际 OPT=1；但按指定规则把 canonical selector 与 incidence claim 直接作积拉回时，出现 -1/160 与 -1/80 的负行，故该同一点不能直接成为 plain primitive-SA1 点。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_general_repair_k2_canonical_pullback_exact_v1.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_general_repair_k2_canonical_pullback_exact_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_general_repair_k2_canonical_pullback_author_proof_v1.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_general_repair_k2_canonical_pullback_author_proof_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_general_repair_k2_canonical_pullback_independent_exact_first.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_general_repair_k2_canonical_pullback_independent_exact_first.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_general_repair_k2_canonical_pullback_author_read_after.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_general_repair_k2_canonical_pullback_author_read_after.md"
legacy_ids:
  - "UM-RAW-K2-14M-DIRECT-CANONICAL-PULLBACK-OBSTRUCTION-v1"
related_objects:
  - "unrelated-machines/sol-general-repair-k2-local-law-canonical-pullback-v1"
evidence:
  - "archives/unrelated-machines/tools/evidence/sol-general-repair-k2-14machine-20261031/source-manifest.json"
---

# 1. 对象范围与来源身份

本页整理一个固定参数的 raw K2 证书及其指定 canonical 拉回失败。它是一个**已给定点的接口障碍**：它没有证明所有 K2 点都失败，也没有给出不相关机实例的近二间隙。

四份冻结源已逐字读完并按以下顺序比较：Exact 规格（`eac516b08fc0432e1375`）→ 独立 Exact-first 重构（`03b2f588015c42156747`）→ 作者 Proof（`62477f731ee7f46616e9`）→ 作者 Proof read-after（`5f4587b787d364311d6e`）。Exact-first 在未读作者证明的前提下重建同一七维矩、raw localizer、CONFIG 和实际调度；作者 read-after 逐项对齐其 pivots、配置权与负值。四个本地证据副本和冻结指纹见 `tools/evidence/sol-general-repair-k2-14machine-20261031/`。

|来源|冻结 SHA-256|作用|
|---|---|---|
|`eac516b08fc0432e1375`|`a79fd77dc17c87a8729bc3c4b47088a434f24db98e37f95b0ec9e01ec604323a`|Exact-only 的完整 14 机模型、functional、K2 合同与两个负拉回式|
|`03b2f588015c42156747`|`2c35b3b119264c2c78eeeeab96fcd9c761d8ed57a1fe0b2d28d5041f2598e75d`|独立 Exact-first 的 Gram 分块、逐机配置和 `OPT=1` 重构|
|`62477f731ee7f46616e9`|`4f4a57ef7a87e9f3fbb4d15049b8aeb50e70ee3695e35afebf08c8c4313f0412`|作者的精确 LDL、raw localizer、配置表与 canonical 失败推导|
|`5f4587b787d364311d6e`|`6b2c85920c6fcfc10240dfc8322991fb6487141c8011c6c4ad199dc95d0678dd`|作者证明的 read-after 比较；未把未运行的作者程序当成新软件证据|

四源不是四次独立实验：Exact 是规范输入，独立稿是先行重构，Proof 与 read-after 是作者推导及其复核。两次重构相互支持固定证书的数学内容，但不能被写成外部同行评审或全球新颖性认证。

# 2. 固定物理模型和共同 functional

模型包含 4 个 group（`M,H_u,H_v,H_r`），每组 2 个 indexed state；6 台资源机（`u,v,r,w_u,w_v,w_r`）和 8 个 private root，共 14 台机器。4 个 selector jobs 加 9 个 listed incidence jobs，共 13 个作业、26 个有限 assignment 端点；未列端点时间为无穷。每个 selector 的两端互补，每个 incidence 的 private/resource 两端互补，不能因为某个系数为零而删除原 job。

令 `a=b_1,b=b_2,c=b_3` 为形式 Boolean 位，并在三位 Boolean 商代数上定义

\[
\ell(1)=1,\qquad \ell(a)=\ell(b)=\ell(c)=\frac3{10},
\]
\[
\ell(ab)=\ell(ac)=\ell(bc)=\frac3{80},\qquad
\ell(abc)=-\frac1{160}.
\]

重复位先按 Boolean 关系约去。原端点变量都替换成 `a,b,c` 或其补。例如 `M/0` 的 selector 是 `a`，其两个 resource 端是 `b` 与 `1-c`；`H_u/H_v/H_r` 的 selector 和 resource 端分别由相应 literal/补给出。每个 incidence 的 private 端是 resource 端的补，故所有 one-hot、endpoint-exclusivity 和 Boolean 恒等式在 degree 4 内成立。令 `L` 为上述 substitution 与 `ell` 的合成；它是一个共同的有理 functional，而不是每台机器分别选取的矩。

# 3. K2 合同的精确验证

## 3.1 全局 M2

所有原 degree≤2 多项式经 substitution 落在

\[
\mathcal B=(1,a,b,c,ab,ac,bc)
\]

的七维空间。作者稿按此基给出精确 LDL pivots

\[
1,\;\frac{21}{100},\;\frac{63}{320},\;\frac7{40},\;\frac7{256},\;\frac7{288},\;\frac7{384},
\]

均严格为正。独立 Exact-first 不使用该 LDL，而以三位置换的 `(1,a+b+c,ab+ac+bc)` 对称块及两个标准块重构同一正定性；其标准块的整数矩为 `[[42,-7],[-7,7]]`。因此完整 26 端点的 physical M2 是此七维矩的线性拉回，对所有原 quadratic squares 同时非负。`ell(abc)<0` 不与 M2 矛盾，因为该三次 monomial 不是 degree≤2 square。

## 3.2 全部 raw affine load localizer

除 `M/0` private root 外，private 和正资源行的 load 恒为 1，三个 fallback 资源的 load 分别为 `b,1-c,1-a`。对恒 1 的行，localizer 是 `(3/4)L(q^2)`；对 literal `z` 行，

\[
L((7/4-z)q^2)=\frac34L(q^2)+L(((1-z)q)^2)\ge0,
\]

因为 `(1-z)q` 是物理 quadratic。唯一非恒定行的 load 为

\[
\operatorname{load}_{M/0}=\frac12+a-\frac b2+\frac c2,
\quad h=\frac74-\operatorname{load}_{M/0}=\frac54-a+\frac b2-\frac c2.
\]

在基 `(1,a,b,c)` 上，作者与独立稿都得到

\[
K=\frac1{320}
\begin{pmatrix}
304&24&150&66\\
24&24&10&-4\\
150&10&150&17\\
66&-4&17&66
\end{pmatrix}.
\]

其精确主子式（或 successive pivots）为 `304,6720,509600,22583120`（相应 pivots 为 `19/20,21/304,91/384,5761/41600`），均正。因此所有 physical machine 的 raw affine localizer 对任意全局 affine `q` 成立。这里的 slack 是 raw load slack，不是 canonical activation quality。

## 3.3 逐机 CONFIG 与边界

除 `M/0` 外，每台机器最多有两个互补端，使用 singleton/empty 配置即可匹配 `L` 的 first 与同机 pair。`M/0` 有三个 jobs：selector `S=a`（时间 1）、`P_u=1-b`（时间 `1/2`）和 `P_v=c`（时间 `1/2`）。一份合法配置分布为

|配置|权重|
|---|---:|
|`{P_u}`|`14/80`|
|`{S,P_u}`|`21/80`|
|empty|`21/80`|
|`{P_u,P_v}`|`21/80`|
|`{S,P_v}`|`3/80`|

总权为 1，最大负载为 `3/2<7/4`。其 first 为 `S:24/80=3/10`、`P_u:56/80=7/10`、`P_v:24/80=3/10`；pairs 为 `SP_u:21/80`、`SP_v:3/80`、`P_uP_v:21/80`，恰与 `L` 一致。合法配置不含三者全集（其负载为 2），但共同 functional 给出

\[
L(SP_uP_v)=\ell(a(1-b)c)=\frac7{160}>0.
\]

这不是当前 K2 的矛盾：合同只共享每机的 first 与 same-machine pair；若额外要求原三阶 membership 也由该配置分布共享，证书会被排除。该区分是本障碍的关键边界。

# 4. 实际最优值与同点拉回失败

取 `M` 的 `r` state、`H_u` 的 own-u、`H_v` 的 own-v、`H_r` 的 fallback-wr；未选 incidence 留在相应 private，选中 incidence 到对应 unit resource。13 个原作业全部执行一次，最大负载为 1；unit selector 使任何实际调度的 makespan 至少为 1。因此

\[
\operatorname{OPT}(P)=1.
\]

这说明该证书不是 actual-OPT gap 或无可行调度反例。

指定 direct canonicalization 把每个 canonical state primitive `A` 取为物理 selector 端，把 incidence claim `Z` 取为 `A` 与其 resource 端的乘积。对 `M/0` 与 `H_v/0`，

\[
A_{M0}=a,\qquad Z_{M0u}=ab,\qquad Z_{M0v}=a(1-c),\qquad A_{Hv0}=c.
\]

于是 canonical primitive-SA1 的非负 claim 行乘 `A_{Hv0}` 给出

\[
L(Z_{M0u}A_{Hv0})=\ell(abc)=-\frac1{160}<0.
\]

同一 state 的 canonical activation quality 为

\[
g=\frac{Z_{M0u}+Z_{M0v}}2-
rac{A_{M0}}4,
\]

故

\[
L(gA_{Hv0})=-\frac1{80}<0.
\]

这两个负值分别击破 plain primitive-SA1 的非负 claim 行和对应 activation-quality 行；三因子来自不同物理机器。raw slack `h` 的 affine localizer 正定并不约束 `L(hac)`，而 canonical slack 是 `a h`，因此不能把 raw localizer 正性无条件换成 canonical quality localizer 正性。

# 5. 与相邻对象的关系、真值和缺口

本页是固定 14 机证书，和已有的 `unrelated-machines/sol-general-repair-k2-local-law-canonical-pullback-v1`（18 机、17 作业、34 端点的 `0<c<1` 参数族）是不同对象。两者都说明 direct canonical pullback 需要跨机器联合条件，但不能互相替换其模型或量词。

已闭合的内容是：该固定 functional 的 degree≤4 Boolean 恒等式、全局 M2、全部 raw affine localizers、逐机 first/pair CONFIG 分布、实际 `OPT=1` 调度，以及给定 direct map 的两个精确负值。作者与独立稿均把固定证书的有限有理算术说清；本批没有把作者所报代码和 run JSON 当作独立重放。

未闭合的内容包括：所有 K2 点的统一失败、其它 extraction/另求可行点、全局 joint schedule law、全局 M3 或三次 literal 非负、实际近二间隙、NP-hardness、任何一般 unrelated-machines 算法或全球新颖性。若要保留这类点，桥接定理必须增加跨机器三重矩/联合配置条件，或明确选择另一可行点与新的 extraction。
