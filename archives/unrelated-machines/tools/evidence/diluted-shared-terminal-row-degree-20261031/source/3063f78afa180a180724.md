# 作者全文读后：fixed-d whole-row CONFIG trade

Reviewer：/root/sol_general_repair，2026-10-18。此前 Exact-first 独立重构冻结为 sol_general_repair_diluted_row_degree_d_exact_first_reconstruction_v1.md，SHA256 4294c156fa6feb502b6c3e90bec6c0bd8fb9e8e5ecc4008c2cf9b71838cf3447；原件不改。

现由 root 释放并已实际全文读取 sol_diluted_shared_terminal_row_degree_d_author_proof.md，SHA256 7fb8ae7e6635853417963a5ff379406cbc3a0abf347a73015ebc79c1a207c407，约 2807 tokens。未打开作者 enhanced code、旧 first/pair code 或运行；未索取新作者推导。此为有此前 Exact-first 和 raw K2 背景的读后，不是第二张 blind 票。

**结论：作者 Proof §1–6 未发现 fatal，按下列范围通过数学读后攻击。** 作者采用 c-coefficient 范数路线；我的先行重构采用 Var_Qold 路线，不能把其中一个说成另一个的实现或软件证书。

## 1. subset trade 与质量逐项核对

作者 §2 用 finite differences 得 Σ_(|S|≤s)b_S f(1_S)=f(1) 对所有 degree≤s multilinear f。这与我先行对任意具体 A 的 containment identity 的 generating-function 证明等价。其 sign、上标 k−|S|−1、边界 s=k−1 都正确。

at-most-one-unit row space 的分解 p=p0(Y)+Σ_jR_jp_j(Y) 正确，deg p_j≤d−1=s；pure-home p0 可以是 degree d，其在 correction 的 difference 内相消，不能误限到 s。重复 factors 与不同 R clique products 的处理有效。foreground baseline 正是 aδC0,all，作者未把它叠到未替换 H row law 上。

Rfill 给 unit/no-unit 两种 S 的背景下界确为 1/(4LkZ)、1/(4LZ)，两个符号负 correction 的吸收恰同需 M−1≥4kZAmax。所有 corrections 的 unit/no-unit 总质量相消，list 合并合法且非负；不是仅 signed moment match。U 的 missing-one-f probability 3(1−a)/8 来自 Qold 的 1/4 与 Rfill 的 1/2 再各权一半，数值正确。U/terminals 全原 rows 均逐样本合法。

## 2. 作者 c-norm localizer 路线的独立重算

写 local affine q=β+ΣcF+ΣdG，q0=β，qN=β+d，qF=β+c+Σd。则逐个 (j,b,π)

    c_(j,b)=qF_(j,b,π)−Σ_ell qN_(b,ell,π(ell))+(k−1)q0.

三项平方界、对 π 均匀平均及对 j,b 求和给作者 (4.2) 的三个系数：

    ||c||² ≤[12kL+12Lk³+6kL(k−1)²] E_Qold q²
             ≤30Lk³ E_Qold q².

第二项中 permutation 每个 label 的 terminal 边际 1/k 抵消 Cauchy 的 k，而外层 j 的 k 仍保留；作者没有少收这个因子。背景 slack≥1/k，且 Qnew 有半份 Qold，故 E_Qnew[gq²]≥||c||²/(60Lk⁴)，对任意 β,d 一致。

foreground H 的 μ=s/k−k/L≥1/(2k)>0。H 中 G=0，S=Σ_jc_(j,σ(j)) 满足 ES²≤(k/L)||c||²，不要求 σ(j) 独立。完成平方并以 |g|≤1 得

    E_H[g(β+S)²]≥−(1+1/μ)ES²
                 ≥−(1+2k)(k/L)||c||²≥−2||c||².

L=2k²、k≥2 使最后因子实际≤5/4，作者用二是合法宽松界。

## 3. 真正所有 global affine contexts

作者 (4.5) 条件于 I=h 后使用各 component independence。所有其他 component 的 conditional means 与 h selector coefficients 吸收到 β_h；其 centered variances 的总贡献乘 E[g|I=h]。

在 h=i 的 H，E g=μ>0；在 h≠i 的 Qnew，Qold half 给正 slack、Rfill half 非负，所以 E g>0。因此丢弃全 outside-component variance terms 的方向正确，未漏掉随 M 增长的负项。local q_i 的 c,d 与 h 无关，只有 intercept 变化；前两项 bounds 均对所有 intercept 一致。

由此平均后的

    F[gq²]≥[(1−a)/(60Lk⁴)−2a]||c||²≥0

确由 M−1≥120Lk⁴ 支付。若 c=0，两边 lower bound 为零，不能据此反推 q=0，但仍足够证明 PSD；U/terminal 的非负则逐样本成立。此为所有原 endpoint variables 的 arbitrary affine q，非局部 q audit。

## 4. 位复杂度与阶数范围

§5 的 head-only moment generator 正确：固定 D=max(4,d)，先使用原 job identities 将 home endpoints 展开，degree≤D 每项只查询固定数 heads。H 为 partial injection；Qold 为单 f+terminal permutation 或单 e；Rfill 对同 B 的 r 个 distinct e labels 不能落 S 的比例是 Σ_(u≤s)binom(k−r,u)/Z，指定 distinct terminals 再乘 1/(k)_r。指定一个同 B 的 f head 乘 1/(2kL)；无 f 且至少一 e head 乘 1/L。f/e demanded B 不同或同 job incompatible endpoints 先置零。r 超可用 labels/destinations 先置零，不形成零分母。

固定 d 时 M、Z、全部完整 ordinary jobs、即使 dense ∞ matrix、degree-D 表、CONFIG lists 和 affine-localizer matrices 均 polynomial in expanded input；指数可依 d，不冒 uniform variable-d 算法。global M2 需要 degree4，故 D=max(4,d) 正确。此为可生成性的数学证明，未实际生成或运行 enhanced table。

## 5. 最强表述的必要限度

实际 OPT、缩放和 CONFIG-first/ST 的 gap 上界二与先行重构一致。跨机器 event localizer 的负式是给定 law 的 degree-three 值，不受这里 affine q² localizer 合同覆盖。

特别核作者 §6 的明确澄清：next mixed degree d+1 的 a/L 值属于指定 finite law 的自然延伸。如果 d+1>D，它不是输出 degree-D restriction 已有的 coordinate；不能声称该 restriction 没有别的 extension。在 d=2,3 时 D=4 已含该 coordinate；一般 higher d 仍只能陈述自然延伸失败。纯-home all-degree matching 也指 explicit law 与 explicit CONFIG marginals 的恒等，而非声称输出包含所有高阶 coordinates。

因此不给 joint CONFIG selector M2、higher-degree q/event localizers、canonicalization、hardness 或一般 approximation 做认证。作者 enhanced audit 尚未读/运行，旧 k=2 first/pair audit 不转记为新 d 证据。原 Exact-first 保留；本记录仅证明读后攻击，无新增盲票、软件或外部新颖性结论。
