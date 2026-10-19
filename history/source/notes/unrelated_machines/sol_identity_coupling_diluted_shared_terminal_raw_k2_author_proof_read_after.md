# 稀释共享终端 raw K2 gap：作者 Proof 全文实读后对照

作者：/root/sol_identity_coupling，2026-10-18。此为 Exact-first 独立重构冻结、root 实际全文读后释放作者 Proof 的 read-after。本人已有 K2/SA3/CONFIG 背景，不称全方向盲审；本次不改变原独立记录，也不认证尚未读的 audit。

## 1. 精确对象与阅读次序

先实际全文读 Exact：

sol_diluted_shared_terminal_raw_k2_exact_only.md；SHA256 25888ec48d8000769bcf5d8d2c4ab9cf29825e9084d1f5bb888de6be7c44210b。

再独立完整重构并冻结：

sol_identity_coupling_diluted_shared_terminal_raw_k2_exact_reconstruction.md；SHA256 622cafcc002d4b507ae8905cf2b4d2cc0cc16f538b33974f51695bd9fb58cb0f；14258 bytes，257 行，0444。

root 确认实际全文读该重构后，本次才实际全文读：

sol_diluted_shared_terminal_raw_k2_author_proof.md；SHA256 2e926c6471c68843602f78c101874198e0ad2808b8db12d737cc8a04f27ad948。

作者 Proof §1–5 已全部读到；未读 code、audit、其他未释放 proof 或外部 review。未改 source、旧 records 或 repo。

**结论：作者 Proof 的系数范数论证、全球 conditional-variance 分解、全部原机 CONFIG first/pair 和总位复杂度均核通；未发现新增 fatal。** 本次只将读后认证范围增至这份指定作者 Proof。

## 2. 实际 OPT、完整原 jobs 及 CONFIG 对照

作者下界以 \(k-\lfloor k(C-1)\rfloor\) 表示所需 exports，等于独立重构的 \(\lceil k(2-C)\rceil\)。任一 h 所在 component 都要把至少 r 枚 f 送往互异 B，每个这种 B 又至少导出 r 枚 e；k terminals 的 unit 容量给 \(r^2\le k\)。达到 schedule 包含全部原 jobs、所有 unselected components，故不是 fixed-selector 的 NO。

原 finite assignment law 逐 sample 恰执行每个原 job 一次。F 的所有 Boolean/exclusivity/cover identities 以及完整 raw M2 因此成立；无需、也不暗指该 law 在强阈值内有 schedule。

U 与 terminals 的 row marginals 逐 sample legal。B 的四种实际 row event、first/pair 公式(2.1)与五类替代 CONFIG 相同；非负差项的分子分别为
\[
M-1-4k(k-1),\qquad M-1-4k^2,
\]
由明确 \(M-1=60Lk^4\) 支付。全部 masses 和为一，最大 CONFIG load 为 \(1+1/k\)。

作者的“full CONFIG”仅指完整合法 distribution，匹配合同仍是 first 与 same-row pair。它不表示同 row triple 也已匹配，或 CONFIG 变量已有某个全球 M2 表。此项和 Exact 及独立重构的边界一致。

## 3. 独立核作者系数范数下界 (3.2)

作者在一个 component 上写
\[
q=\beta+\sum c_{j,b}F_{j,b}+\sum d_{b,\ell,t}G_{b,\ell,t}.
\]
记全-home、single-e、single-f-plus-permutation 上的 q 值为 \(q_0,q_N,q_F\)。其恒等式
\[
c_{j,b}
=q_{F,jb,\pi}-\sum_\ell q_{N,b\ell\pi(\ell)}+(k-1)q_0
\]
逐项消去截距及 d，确实成立。

三项平方和界、对 k 个 \(q_N\) 的 Cauchy、permutation 的单项均匀边际及 j 的 k 重计数，给
\[
\|c\|^2
\le3\sum_{j,b}E_\pi q_F^2
+3k\sum_{b,\ell,t}q_N^2
+3kL(k-1)^2q_0^2.
\]
Q 的三类概率分别是二分之一、四分之一、四分之一，故三个和项分别受 \(4kLE_Qq^2,\ 4Lk^2E_Qq^2,\ 2E_Qq^2\) 控制。于是
\[
\|c\|^2
\le[12kL+12Lk^3+6kL(k-1)^2]E_Qq^2
\le30Lk^3E_Qq^2.
\]
该界对任意截距 beta 和任意 d 都成立，常数不依赖 M、矩阵维度或全局 context 数。没有 rank、最小特征值或固定维数连续性的欠付假设。

## 4. H 负贡献及完整全球 affine q

H 下 e-heads 全零，\(S=\sum_j c_{j,\sigma(j)}\)，注入的单项边际给
\[
E_HS^2\le(k/L)\|c\|^2.
\]
固定 B 的 slack g 满足 \(E_Hg=1/(2k)\)、\(|g|\le1\)。对任意截距完成平方并用 Cauchy：
\[
E_H[g(\beta+S)^2]
\ge-(1+2k)E_HS^2
\ge-(1+2k)(k/L)\|c\|^2
\ge-2\|c\|^2.
\]
最后用 \(L=2k^2\)，所以系数实际为 \(1+1/(2k)\le2\)。

Conditional on selector \(I=h\)，其他 components 的随机选择确实相互独立，且与被测 component 独立。任意原全局 affine q 的各 home indicators 可用原 job covers 线性消去；全部 selector endpoints 在此条件下为常数。把其他 components 的 conditional means 合入 \(\beta_h\)，其独立零均值部分贡献恰是
\[
E[g\mid I=h]\sum_{j\ne i}\operatorname{Var}(q_j\mid I=h)\ge0.
\]
这正是作者(4.1)。h=i 时 g 的均值为 \(1/(2k)\)，h 不等于 i 时 g 逐点至少 \(1/k\)。因此不丢任何负项，也不漏含多个 components 或全部 selector endpoints 的 q。

Q 下再乘其 slack 下界 \(1/k\)，作者(3.2)给 \(\|c\|^2/(30Lk^4)\)；H 下用 \(-2\|c\|^2\)。全局合成
\[
F[gq^2]\ge
\left(\frac{1-a}{30Lk^4}-2a\right)\|c\|^2=0
\]
恰用 \(M-1=60Lk^4\)。\(\|c\|=0\) 也包含，没有除零。

这条范数证明与本人 first record 的 \(\operatorname{Var}_Q(g_i)\) 控制不同，二者均给同一个明确 M 足够；不能把两条证明中的截距、系数或符号相互替换后另作未核的主张。

## 5. 有限次数矩的可计算性与位成本

原变量数 N 在 k 中为明确多项式。完整 total-degree 至多四表有 \(O((N+1)^4)\) 项。作者允许先展开 home indicator 为一减其 nonhome endpoints；最多四个因子，至多 O(N⁴) 项，仍是固定次数多项式。

Condition on I 后，每个非空 head monomial 至多涉及四个 components。H 的 compatible f-heads 概率为 \((L)_r^{-1}\)，e-heads 为零；Q 最多一个 f export，e-heads 的 full-export 分支由同 B 的 partial permutation 概率 \((k)_s^{-1}\) 给出，single-e 分支只能支持一个 distinct e head。r、s 至多四；不合法的原 job/注入/置换模式先判零，包含 k 小于所需阶数的情况。

有无 f-head 时的两个系数分别为 \(1/(4kL)\) 和 \(1/(4L)\)，后者由 k 个可选 f-label 相加消去 k 得到；single-e 系数 \(1/(4Lk^2)\) 正确。空 monomial 单独取一，不能拿非空规则错误套它。

这些规则无需枚举所有 injections/permutations；仅做多项式数量的有理运算，至多四阶 falling factorial 及 selector \(1/M\) 的位长多项式。完整 CONFIG lists 的 supports 与已审 Exact 相同；所有 localizer matrix entries 由至多三阶 moments 和有限行系数求得，亦在多项式总时间、总位长内可生成。

这里证明的是特定证书的生成，不是 exact SDP finder；没有把指数 support 的存在当成算法，也没有借局部 50×50 数值检查认证全球 localizers。

## 6. 缩放、强条件反证和状态

同乘全部 finite times by \(k/(k+1)\) 后，原同点 moments/CONFIG weights 不改，slack 为旧 slack 的正倍数，真实 OPT 变为
\[
\frac{2-\lfloor\sqrt{k}\rfloor/k}{1+1/k}\to2.
\]
这是 raw K2 的实际 near-two gap。

另一方面，selector endpoint \(A_i\) 乘 unit incoming occupancy \(C_{i,b}\) 的条件只保留 H 命中该 B 的事件，故
\[
F[A_iC_{i,b}(T_0-\mathrm{load}_B)]
=a(k/L)(T_0-2)<0.
\]
同 row one-unit/two-home triple 也与 legal CONFIG 不符。作者末节诚实限定这一点；没有把 raw affine-square PSD 冒作任意两事件条件、canonical export gate 或更强 native-C2/S3。

本次通过完整作者 Proof 的当前数学与复杂度；software、verifier、数值或 exact audit 本人均未读未跑，不作认证。一般 UM 非存在性/统一算法问题及真实 hardness source 仍未解决，旧 first record 保持原 bytes。
