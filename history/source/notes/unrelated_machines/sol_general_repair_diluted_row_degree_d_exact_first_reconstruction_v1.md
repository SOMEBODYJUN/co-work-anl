# Exact-first 独立重构：固定 d 的 whole-row CONFIG trade 与稀释 shared-terminal gap

Reviewer：/root/sol_general_repair，2026-10-18。唯一新输入为 sol_diluted_shared_terminal_row_degree_d_exact_only.md，SHA256 e23ae495b4a997f081e0de06323e5dd9563c98d3828b78804ddc7670b16c9f6a，已实际全文读完。未读本新对象或其旧 first/pair 对象的作者 Proof/code/运行；未向 literal/identity 索证。

背景披露：熟悉 raw K2 的 global M2、全原 affine load-localizer 与同机 CONFIG first/pair 语义；自己此前写过 actual OPT=1 的 18m 同点 canonical pullback counter。已从 root 消息知道 literal 有不同的稀释 shared-terminal actual-near-2 候选。不是方向无背景盲审；以下独立重构新固定 d trade、所有原 affine localizers、实际 OPT、尺寸和位复杂度，不代签任何作者软件或外审。

**冻结结论：未发现 fatal。** 下面给可直接复核的完整关键代数。此结论只覆盖 Exact 的指定 row-degree d + affine-q 合同；不升级更高阶 load-localizers、joint CONFIG indicators 或 hardness。

## 1. 普通矩阵、完整原任务与实际 OPT

取 d≥2 固定，k≥d，s=d−1，L=2k²。每分量有 U、L 个 B、k 个 terminals；一枚全局 unit h 可去 M 个 U；每分量 k 枚 f，有 U tiny 1/k 和全部 L 个 B unit ends；每 B 的 k 枚 e，有 B tiny 1/k 和全部 k 个 terminals unit ends。于是三项计数逐字为

    machines = M(1+L+k),
    jobs = 1+Mk+MLk =1+Mk(1+L),
    finite endpoints = M+Mk(1+L)+MLk(1+k).

所有原 jobs 必跑一次；没有 component 间的 f/e edges，唯 h 跨 U。其余 matrix entries 是 ∞，非大有限数。

令 r=floor(sqrt(k))。上界：h 去 U_1，从它输出 r 枚 f 到 r 个不同 B，每个被占 B 输出 r 枚 e 到 r² 个不同 terminals（r²≤k）；其他全部 f/e 留 home。U_1、这 r 个 B 的负载都是 2−r/k，terminal 至多一，其他原机器至多一，所有原 jobs 已执行。

下界：假设 C<2−r/k<2。h 所在 U 必输出至少 q=r+1 枚 f，因为 tiny payload 总一。unit f 在 C<2 时必须落不同 B；每个被 unit 占据的 B 为低于该 C 又必须输出至少 q 枚 e。所有 e 的 unit terminals 在 C<2 时各至多一，只有 k 台，而至少 q²>k 枚 e 被输出，矛盾。故 OPT=2−r/k。此下界量化完整所有普通 assignments，不依赖样本 law 或预设状态。

## 2. 真实共同 functional 与全原语义

Exact 的 H、Qold、Rfill 都是每枚 f/e 恰选一个原有限端点的真实有限分布。h 先选 I、component I 用 H、其他 components 独立 Qnew。故共同 F=E 在所有次数上都可定义且为真 assignment law，所有 Boolean、same-job exclusion 与原 job cover identities 在要求的全部 multipliers 下成立；global M2 及任意 degree 的 global PSD 自动成立。

逐样本：Qold 的每台机器负载≤1；Rfill 只有一个 B 的 incoming unit 加至多 s 枚 tiny homes，所以负载≤1+s/k=T，其他机器≤1；H 在 U 为 h 的一、terminals 零，B 为一或二。全局仅 I 内被 injection 选中的 B 可超过 T。U 和 terminal 的实际行 law 全合法，直接作为 CONFIG 即可。

这不是所有真实分布样本均 threshold-T 可行；恰是稀释的 H 超载被 affine tests 的背景质量遮住。高阶 global PSD 因此不能写成高阶 load/SOS gap。

## 3. subset interpolation 对所有标签子集成立

令 b_S=(-1)^(s−|S|) binom(k−|S|−1,s−|S|)，|S|≤s。对任意具体 A⊆[k]、r=|A|≤s，需要且足够的恒等式是

    Σ_(S⊇A,|S|≤s)b_S =1.                             (3.1)

它不依赖 A 的身份，但确实量化所有 A。令 n=k−r，m=s−r≤n−1，左边变为

    Σ_(t=0)^m binom(n,t)(−1)^(m−t)
                       binom(n−t−1,m−t).

它是下式的 x^m 系数：

    Σ_(t=0)^n binom(n,t)x^t(1−x)^(n−t−1)
      =(1−x)^(-1)(x+1−x)^n=(1−x)^(-1).

多项式/形式幂级数的低次系数只用 t≤m，边界 n−t−1≥0，故没有对负上标 binomial 的偷换；系数恰一。这也处理 r=0、r=s、s=k−1。

H 的固定 B 行 law 是 (1−k/L)δC0,all +(1/L)Σ_jδCj,all。纯 home monomials 在 H 总恒等于一。CFG formula 的各同一 S corrections 对纯 home moments 完全相消：k 个 unit terms 各 a/L b_S 与 no-unit 项 −ak/L b_S 抵消；baseline aδC0,all 正好对应 H 总 home marginal。所以纯 home moments 任意次数都保留。

含一个 incoming R_j 和 r 个 distinct homes 的 monomial，r≤d−1=s 时，CFG 的 foreground 值为 (a/L)Σ_(S⊇A)b_S=a/L，与 F 在 H 的 foreground a/L 相同。含至少两个不同 incoming R 的行 monomial 双边都零；重复 factors 用 Boolean 化简。因此 degree≤d 的**每个** same-machine endpoint monomial 均匹配，包含 d 个 homes 无 unit 的情况，不能错把它也只保到 s。

## 4. 正质量吸收与全部行 CONFIG 尺寸

对 |S|=r，|b_S|=binom(k−r−1,s−r)≤Amax=binom(k−1,s)：相邻比为 (s−r+1)/(k−r)≤1。Qnew 的 fixed-B row 中，Rfill 的一半质量确给每 Cj,S 至少 1/(4LkZ)、每 C0,S 至少 1/(4LZ)。

unit correction 负幅度至多 a Amax/L，被 (1−a)/(4LkZ) 吸收；no-unit correction 负幅度至多 ak Amax/L，被 (1−a)/(4LZ) 吸收。二者同要求 M−1≥4kZAmax，正是给定 M 的一项。重复相同 configurations 先合并只增加这些已计背景，不产生新负项。全部新增 rows 的 load≤T；δC0,all 的 load 一；total mass 的 unit/no-unit correction 自动抵消，剩 (1−a)+a=1。

每 B 的 Qold row 仅 C0,all、k 个 Cj,empty、k 个 C0,all-minus-one；Rfill 加 (k+1)Z 种 Cj,S/C0,S。因此每行 list 为 O(kZ+k)。U 的 list 为 O(k)，terminal 为 empty 或一个原 e，即 O(Lk)。没有枚举 k! terminal bijections 或 L! injections。

## 5. 所有原全局 affine load-localizers：独立定量支配

这是最承重部分。固定 B=B_(i,b)，τ=T−1=s/k，p=k/L=1/(2k)，所以 0<p≤τ/2<1/2、0<τ<1。

任何原全局 affine q，利用原 endpoint cover 等式，可重写为一个常数、h selector 系数 α_I，加各分量的 export-linear 函数 q_j。每 q_i 在 all-home assignment 为零，可写

    q_i=Σ_(j,b)c_(j,b) X_(f_j→B_b)
        +Σ_(b,ell,t)d_(b,ell,t) X_(e_b,ell→Z_t).

这仍包含**全部原 endpoint变量**的任意 affine combination，不预先从合同删除 home endpoints。条件于 I，其他分量独立；令 V=Var_Qold(q_i)，m=E_Qold q_i。

Qold 一半在 all-home，q_i=0。Cauchy 给 m²≤(1/2)E_Qold q_i²，故 E_Qold q_i²≤2V、m²≤V。分别读取 Qold 的单 e-export 分支及单 f+全 e permutation 分支：

    Σ d²≤8Lk²V,
    E_(uniform j,b,pi)(c_(j,b)+Σ_ell d_(b,ell,pi(ell)))²≤8V.

对 D_b(pi)=Σ_ell d_(b,ell,pi(ell))，有 E_pi D_b²≤Σ_(ell,t)d_(b,ell,t)²，故

    Σ c²≤16Lk(1+k²)V,
    E_H q_i²≤(k/L)Σ c²≤16k²(1+k²)V,
    E_H(q_i−m)²≤C_k V,
    C_k:=32k²(1+k²)+2 ≤15Lk³                    (k≥2).       (5.1)

最后的宽松常数核查：C_k≤(321/8)k⁴<60k⁴≤30k⁵=15Lk³，所有 k≥2 含 k=d=2。H 的 injection 每个 f 的边际是 uniform [L]，不需要各 f 独立。

在 I=i 的 foreground，写 q=K+(q_i−m)，K 含其他分量和 h 的全部值。令 C 为该 B 的 incoming occupancy，则 slack h_B=τ−C；E_H h_B=τ−p≥τ/2，E_H h_B²=τ²−2τp+p≤(3/2)τ。对任意固定 K，完成平方并 Cauchy：

    E_H[h_B(K+r)²]
      ≥ E_H[h_B r²]−(E_H[h_Br])²/(E_Hh_B)
      ≥−E_Hr²−3E_Hr²≥−4C_kV,       r=q_i−m.          (5.2)

所以 foreground 的总负贡献至多 4a C_k V；这个 bound 对每个其他分量 realization 和任意 K 都成立，没有偷偷假设 q 只看本分量。

在 I≠i 的 background，component i 用 Qnew。取其中一半 Qold，B slack≥τ；条件其他分量和 I，其 q² 在 Qold 的期望至少 V，因为加任意常数不能降低 variance。Rfill slack 非负，其余可丢。因此 background 正贡献至少 (1−a)τV/2。合并：

    F[(T−load_B)q²]
      ≥[(1−a)τ/2−4aC_k]V≥0,

因为 M−1≥120Lk⁴、τ≥1/k，故 (M−1)τ/2≥60Lk³≥4C_k。若 V=0，(5.1) 使 foreground centered r 也零，仍成立。U 和 terminals 全样本 load≤1，localizers 则逐样本非负。

由此真正闭合所有原 global affine q 的 localizer，而不是只核单分量 q 或只核端点 diagonal。

## 6. 固定 d 的 total-bit 可生成性，含 dense 输入

固定 s=d−1 有 Z≤(s+1)k^s，Amax≤k^s，故 M≤1+240k⁶+4(s+1)k^(2s+1)，是 k 的多项式，指数可依 d。M components、完整 original jobs、finite endpoints 和即使显式写全 ∞ 的 dense machine×job matrix，规模也都是固定 d 下 k 的多项式；不是只以稀疏图偷计规模。

对 degree≤D=max(4,d) monomial，至多 D 个被查询 endpoints。枚举 I∈[M] 后最多 D 个被查询分量需要计算，其他分量积分为一。H 中 r 个指定 f→B distinct assignments 的概率为 1/(L)_r，冲突为零；e 为 all-home。Qold 的单 f/b 和单 e/b/terminal 分支可显式多项式枚举，terminal bijection 的指定 r 对概率 1/(k)_r。Rfill 只枚举 b、|S|≤s 的 Z subsets、coin 和 unit j；被导出 jobs 的至多 D 个指定 distinct terminal images 概率同为 1/(k)_r。home constraints 直接测试 label∈S。r 不会超过可用 destinations；冲突事件为零，不对零 falling factorial 作除法。

于是可生成 O((N+1)^D) 全原 moments；fixed D 下为 expanded input 长度的多项式。所有运算是多项式个显式有限和/积，分母来自 M,L,k,Z 与长度≤D 的 falling factorial，其 bit lengths 多项式；不枚举指数 complete assignments。CONFIG lists 按 §4，affine-localizer matrices 从 degree≤3 entries 加权得出，global M2 从 degree≤4 entries 得出。数学 PSD proof 与“实际实现或运行代码”分开；本记录没有声称执行作者程序。

## 7. 缩放、下一阶失败与精确 scope

统一乘 k/(k+s) 保所有 ordinary finite endpoints、job identities和证书，localizer乘同正数，目标变一，真实 OPT 变 Exact 所列比值。固定 d、k→∞ 时分子趋二、分母趋一。反向上界二来自同机 CONFIG first moments 和原 cover 产生 prune-LST point，再标准 ST≤2T；故该指定系统 gap supremum 二成立。

在该给定 F，A_i=1 仅 I=i；H 的 B 占据概率 k/L，负 event row 是

    F[A_i C_(i,b)(T−load_B)] = a(k/L)(T−2)<0.

这是原 degree-three 的跨机器 product-event load test；不是合同的 affine-q² test，也不是从 global higher PSD 自动得到。

取一个原 incoming f_j endpoint 与 d 个 distinct home e endpoints。Qold mixed part homes empty；Rfill mixed part homes≤s=d−1，二者 product 为零；H 的 foreground product 概率 a/L，所以 F=a/L>0。但任何 CONFIG(T) 有该 unit 时至多 s 个 homes，此 row-degree d+1 moment 必零。这准确描述 supplied point 的下一阶 row matching 失败；不推出 stronger system 对该 P 不可行。

此审查未读作者 Proof/code、未运行全矩表、未给 external review/novelty/hardness。无 standing fatal，仅对本 Exact 指定对象和全部边界的数学重构通过；不覆盖 joint CONFIG indicator M2、higher-degree load localizers 或一般 UM 算法。
