---
id: "unrelated-machines/seven-state-star-exact-first-reconstruction-review"
kind: "review"
type_tag: "审查"
title: "七态原星 Exact-first 独立重构与版本边界"
status: "integrated-increment-recommended"
truth_status: "full-source-read-independent-reconstruction; local-scope-only"
review_level: "full-read-source-and-cross-object-comparison"
summary: "对源 967a84ebc3e0101f1c80 的 224 行 Exact-first 重构记录逐字读取，并以显式五点评估、weighted Cauchy、CONFIG pair trade 和固定次数矩生成重核；与作者 Proof/read-after、canonical v2、有限 audit 及相邻 raw-K2/one-outer 记录去重。结论只覆盖实际 OPT=1 的七态原星局部合同。"
legacy_ids:
  - "967a84ebc3e0101f1c80"
  - "UM-SEVEN-STATE-STAR-GLOBAL-QUADRATIC-EXACT-v1-exact-first-reconstruction"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_identity_coupling_seven_state_star_exact_first_reconstruction.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_identity_coupling_seven_state_star_exact_first_reconstruction.md"
related_objects:
  - "unrelated-machines/seven-state-star-global-quadratic-local"
  - "unrelated-machines/seven-state-star-global-quadratic-exact-v1-review"
  - "unrelated-machines/seven-state-star-global-quadratic-audit-scope"
  - "unrelated-machines/seven-state-star-global-quadratic-extension-boundary-20261031"
  - "unrelated-machines/seven-state-star-global-quadratic-coercivity-learning-20261031"
---

# 1. 来源身份、读取顺序与审查角色

本记录的直接原件是
`cleanup/workspaces/Boss5/resume-20261031-current/967a84ebc3e0101f1c80.md`，即
`history/source/notes/unrelated_machines/sol_identity_coupling_seven_state_star_exact_first_reconstruction.md` 的 Exact-first 重构记录。实读为 224 行、10,797 bytes，SHA-256
`7d61b211b43d03cdf3c64d16605ab745a2ef77dd1e0cf43896ff59b886f8ab86`。`sources.json` 给出的冻结源是 `33573876658083d40e0f91385990ff1e1a33e851`，来源名为 `legacy-cleanup` 的 commit `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `main` 的 commit `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`；两者路径和 SHA 相同。

该原件自述的阅读边界是：先只读作者的 statement-only Exact（不是 Proof、代码或 JSON），然后独立重构；没有把作者 Proof、有限程序或之前的消息当作其 Exact-first 证据。这里保留这个时间顺序和角色，不把该文件改称为作者 Proof，也不把它当作对整个 unrelated-machines 方向的盲审。

本次核验完整读取该 224 行，并在全仓读取与之直接相关的 canonical/local theorem、Exact-only 复核、coercivity 作者 Proof/read-after、最终四对象延拓审查和有限 audit/root-replay 范围；还读取 `sources.json` 列出的 3a1dd9093f4b924ddcb8、4c90a874963e76591945、d38bc86e1cf24e270a1a、3895339d864be003e0f4、c36482710e27da1bc3f7 五个相邻 Boss5 原件。未运行审计程序、未声称代码或 JSON 的 fresh 执行，未改任何共享正文、Git、认领或认证状态。

# 2. Exact 合同：完整输入与真实 assignment law

取正偶数 (d,s)，\(2\le s\le d/2\)，并置
\[
\eta=s/d,\qquad h=s/2,\qquad T=1+\eta,\qquad
p=\eta^3/1000,\qquad u_0=4p(1-\eta),\qquad e=4/5-p-u_0.
\]
于是 \(d\ge4\)、\(0<\eta\le1/2\)、\(e>0.79\)，且这些量有显式有理表示。

机器为 (u,v,z_1,\ldots,z_d)，原 job 为 (R,j_1,\ldots,j_d)。有限 processing times 只有
\[
R\to u=R\to v=1,\qquad j_\ell\to v=1/d,\qquad j_\ell\to z_\ell=1;
\]
其余端点无穷。每个样本必须给全部 \(d+1\) 枚不可拆原 job 指定恰一个有限端点，因而有 \(2(d+1)\) 个有限端点。

令 (C=1) 表示 (R\to v)，(Y_\ell=1) 表示 (j_\ell\to v)，(H=\sum_\ell Y_\ell)。Law \(P\) 先选 ((C,H))，再在 ([d]) 中均匀选大小为 (H) 的集合作为 (Y_\ell=1)：

| (C) | (H) | 质量 |
|---:|---:|---:|
| 1 | (d) | (p) |
| 1 | 0 | (1/20) |
| 1 | (h) | (1/20) |
| 0 | 0 | (1/20) |
| 0 | (h) | (1/20) |
| 0 | (d/2) | (u_0) |
| 0 | (d) | (e) |

所有质量严格为正且和为一。负载逐样本为
\[
load_u=1-C,\qquad load_v=C+H/d,\qquad load_{z_\ell}=1-Y_\ell.
\]
把 (R) 放在 (u)、所有 (j_\ell) 放在自己的 (z_\ell) 给峰值一调度；(R) 在所有有限端点处理时间均为一，故实际 (\mathrm{OPT}=1)。Law \(P\) 只在 ((C,H)=(1,d)) 以概率 (p>0) 产生 (load_v=2)，这个坏样本不是实际 gap 证据。

# 3. 共同 M3 与任意全局 degree-two 负载矩阵

在全部原端点指示变量上定义 (L[f]=\mathbb E_P[f])。由于每个样本是真实完整 assignment，任意次数的 \(L[r^2]\ge0\)；特别地，以全部次数至多三单项式为行列的共同 (M_3) 是 PSD，全部 Boolean、每 job one-hot/exclusivity 及其定义矩等式逐样本成立。该 \(L\) 同时用于每一台机器，不允许逐行换 law。

任意总次数至多二的全局实多项式 \(q\) 在互补端点代入后都可写为
\[
q(C,Y)=a+bC+\sum_\ell u_\ell Y_\ell+\sum_\ell v_\ell CY_\ell
          +\sum_{\ell<r}w_{\ell r}Y_\ell Y_r.
	ag{1}
\]
固定 ((C,H)) 并对均匀 (H)-子集取条件均值，使用
\[
\mathbb E[Y_\ell\mid H]=H/d,\qquad
\mathbb E[Y_\ell Y_r\mid H]=\frac{H(H-1)}{d(d-1)}
\quad(\ell\ne r),
\]
可得
\[
f_C(x):=\mathbb E[q\mid C,H=dx]=A+BC+Dx+ECx+Fx^2.
	ag{2}
\]
关键是两支 (f_0,f_1) 共享同一个二次系数 (F)，因为 (1) 没有 (CY_\ell Y_r) 三次项。正余量类别中 Jensen 给
\(\mathbb E[q^2\mid C,H]\ge f_C(H/d)^2\)；坏类 (C=1,H=d) 的 (Y) 全为一，故 (q=f_1(1)) 无额外非对称余量。

令 (	au=h/d=\eta/2)、(B_*=1/\tau=2/\eta)、(A_*=B_*-1)。由两个二次函数共享 (F)，五点评估恒等式为
\[
f_1(1)=-A_*f_1(0)+B_*f_1(\tau)
       +A_*f_0(0)-B_*f_0(\tau)+f_0(1).
	ag{3}
\]
它可由先用 (f_1(0),f_1(\tau)) 外推到 (1)，再用 (f_0(0),f_0(\tau),f_0(1)) 消掉共同二次余项直接展开得到。五个正状态质量乘 slack 分别至少取为
\[
\frac{\eta}{20},\quad\frac{\eta}{40},\quad
\frac{1+\eta}{20},\quad\frac{1+\eta/2}{20},\quad e\eta.
\]
因此加权 Cauchy 给
\[
f_1(1)^2\le S E_+(q),
\]
其中 \(E_+(q)\) 是全部六类正 slack 对 \(q^2\) 的贡献；上述五类的贡献之和不超过它，且
\[
S=A_*^2\left(\frac{20}{\eta}+\frac{20}{1+\eta}\right)
 +B_*^2\left(\frac{40}{\eta}+\frac{20}{1+\eta/2}\right)
 +\frac1{e\eta}
 <\frac{321}{\eta^3}.
	ag{4}
\]
例如 \(A_*,B_*\le2/\eta\)、\(e>79/100\)、(\eta\le1/2) 给 (S\le(320+25/79)/\eta^3<321/\eta^3)。坏类 slack 为 (-(1-\eta))，所以
\[
L[(T-load_v)q^2]
\ge E_+(q)-p(1-\eta)S E_+(q)
\ge\frac{679}{1000}E_+(q)\ge0.
	ag{5}
\]
这覆盖任意跨机器、跨 job、非对称实系数 \(q\)，不是只核对称子块。对 (u,z_\ell)，\(T-load_i\ge\eta>0\) 逐样本成立，故同一 \(L\) 给所有机器的全局 degree-two localizer PSD。

# 4. 合法 CONFIG(T) 与完整 first/pair 量词

v 行的 CONFIG law (K_v) 仍在每类中均匀选 (H)-子集，质量为

| (C) | (H) | (K_v) 质量 |
|---:|---:|---:|
| 1 | (s) | (p/\eta) |
| 1 | 0 | (1/20+p-p/\eta) |
| 1 | (h) | (1/20) |
| 0 | 0 | (1/20+u_0/2) |
| 0 | (h) | (1/20) |
| 0 | (d) | (e+u_0/2) |

这些质量为正，且 active 类 (C=1,H\le s) 的 v 负载至多 (T)，inactive 类 (C=0,H\le d) 的负载至多一。对 v 行任意原端点 (a) 及任意 pair (a,b)（包含 (a=b)），(K_v) 与 \(L\) 的 first/pair 完全一致。

原因不是只匹配单个 (Y_\ell)：交换对称下所有 first/pair 由
\[
E(C),\quad E(H),\quad E(CH),\quad E[H(H-1)]
\]
决定。第一步把 (C=1,H=d) 的质量 (p) 换成 (C=1,H=s) 的质量 (p/\eta)，以 (H=0) 补质量，保持前三个统计量；它让 (E[H(H-1)]) 减少 \(p\,d(d-s)\)。第二步把 (C=0,H=d/2) 的质量 (u_0) 平分到 (H=0,d)，保持总质量和 (E(H))，并增加 \(u_0d^2/4\)。
由于 \(u_0=4p(1-\eta)\)、\(s=\eta d\)，两项完全抵消。对角 pair 由 Boolean first 决定。u 行只有 (R)，每个 (z_\ell) 行只有 (j_\ell)，取其真实 Bernoulli 边际即为合法 CONFIG(T) law；这些逐行 law 不被拼称为新的共同 assignment law。

# 5. 固定次数的显式矩生成及证据边界

若 endpoint monomial 指定 (a) 个不同 (Y_\ell=1)、(b) 个不同 (Y_\ell=0)，给定 (H) 的条件概率为
\[
\frac{(H)_a(d-H)_b}{(d)_{a+b}},
	ag{6}
\]
冲突 one-hot 取零，空乘积取一；对七类质量求和即得到 \(L\) 的精确有理矩。固定次数 (D) 时变量数 (O(d))，单项式数 (O_D(d^D))，每个有理数位长 (O_D(\log d))，因此 M3（需次数六）、全局 degree-two load entries（至多次数五）及 row first/pair 都可按显式输入长度确定性多项式生成。均匀子集不必展开为指数支持，也没有调用优化、SDP finder、未知调度或条件 oracle；该复杂度不按 \(\log d\) 计时。

有限 audit/root-replay 是另外的证据层：已有记录只对 12 个 ((d,s)) 做 Fraction 字段，前三组才物化完整 M3/global-q2 矩阵，并记录一次 fresh CLI 输出与作者输出字节一致。它不认证上述任意 ((d,s)) 证明，也不认证 sparse-support 软件、affine/AND 接线、shared-owner/growing-depth、一般调度算法或 hardness。

# 6. Exact-first 与作者 Proof、后续版本的去重

`3a1dd9093f4b924ddcb8` 是作者在读 Exact-first 后的 Proof/read-after：它重做同一对称化与五点插值，使用较粗的 (16/\eta^2) Cauchy 系数界；它确认作者 Proof 与 Exact-first 数学相容，但不能反写为 Exact-first 的先行证据。`4c90a874963e76591945` 是最终 canonical v2 的知情全文核对，明确把 global quadratic local、uniform-cardinality first/pair support、affine Boolean boundary 和 faithful AND localizer 分成四个对象，并说明作者参与的边界核对不等于新的盲审；它没有改变 Exact-first 的原始 hash 或阅读顺序。v2 的 Fisher–Yates/消列是额外的显式稀疏 CONFIG 支持构造；967 只给紧凑均匀子集的矩生成，不继承该额外支持算法。

`d38bc86e1cf24e270a1a`、`3895339d864be003e0f4` 是 raw-K2/SA3 相邻机器来源，`c36482710e27da1bc3f7` 是 one-outer fallback 来源；它们改变模型、量词和负载合同，不能作为七态 Exact 的证明或反例。全仓已有 theorem/local、Exact-only review、coercivity learning、extension-boundary 和 audit-scope 对象已覆盖同一七态局部核；本增量的独有去向是源 967 的 Exact-first 阅读身份、上面的显式 \(S<321/\eta^3\) 与 \(679/1000\) 余量、以及完整 endpoint-monomial 公式 (6)。

# 7. 保留范围与正式整合建议

可保留的结论是：对每个合法偶数 (d,s)，同一真实完整 assignment law \(P\) 给共同 (M_3)，全部机器的全局 degree-two 负载 localizer PSD，v 行及其余行的合法 CONFIG(T) first/pair，且固定次数矩可显式生成；原实例实际 OPT=1。

不能由此推出递归 shared-owner/growing-depth law、任何新增 payload 或合并机器的局部化、actual near-two/integrality gap、NP/UGC/GapETH hardness、一般 unrelated-machines 调度器或 six-player/SPE 结论。尤其，正坏样本概率 (p) 与另一个峰值一 home schedule 不是 actual gap；row CONFIG 分布与共同 \(P\) 也不能拼成一个新的全局 assignment law。

建议正式整合路径为
`archives/unrelated-machines/state/审查/七态原星Exact-first独立重构与作者Proof关系--审查.md`，作为现有
`七态原作业星GlobalQuadratic Exact与审计延拓边界审查--审查.md` 的语义增量；不新建第二份 global-quadratic theorem。整合时须在 `source-migration-crosswalk`/语义处置中注明源 ID、原 hash、完整实读、相关对象比较、以及有限 audit 的 `not_checked` 清单。

本文件不是对共享 archive 的写入，也不是 Git checkpoint；它是给 Boss 复制到正式路径前审阅的自足增量。
