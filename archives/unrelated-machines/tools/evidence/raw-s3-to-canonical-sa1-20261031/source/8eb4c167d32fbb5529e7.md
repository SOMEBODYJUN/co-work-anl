# raw 四次矩到 canonical plain-SA1 的 Exact-only 独立重构

作者：/root/sol_identity_coupling，2026-10-18。此记录只实读下列 Exact 合同并独立作代数重构，未读该候选的作者 Proof、程序或其他审查记录。审者已有 normalized-flat、共同 SA1、raw 矩及 CONFIG 背景，也知此转换的研究方向；不称全方向盲审。

实读对象：sol_raw_sa3_to_canonical_sa1_exact_v1.md；SHA256 为 9c2a180330eed2a9b5f5b35b07eb76e2b33ed7ff853bba7376cc06e060595b71，5572 bytes，50 行。未修改该文件或任何 repo 文件。

**结论：在 Exact 明列的完整 S3 合同下，声称 A、B、C 及固定次数 rational-LP/提取复杂度均通过本次独立重构；未发现 fatal。** 关键付款包括每个原 box 的至多三个 raw-literal 乘子、物理 root slack 的至多三个乘子，以及 unit-cap 的共同乘子。若去掉这些付款，此记录不提供较弱 raw K2 到目标合同的替代证明。

## 1. 本次核对的精确对象

Domain 是完整显式 normalized-flat 菜单。每 indexed state 的全部列出系数非负、和为一；零 incidence、重复 indexed state、unused resource 和全部未选 state 均保留。原 ordinary P 中，每组一枚 unit selector，每 state 一个独立 private root，每 incidence 一枚不可拆原 job，private 端时间为其系数，原 resource 端时间为一；没有附加资格、逻辑条件或先行 inactive-home 约束。

Assumptions 是 Exact 的同一共同有理 functional \(L\)：degree \(\le4\)、\(L(1)=1\)，所有原 Boolean identity 乘 degree \(\le2\) monomial、每原 job cover equality 乘 degree \(\le3\) monomial，以及每原 box/物理 slack/unit-cap-1 行乘任意至多三个 raw literals，全部成立。以下使用的等式乘子可为有符号多项式，由合同逐 monomial 线性推出。

Quantifiers 是每个二进制有理 \(1\le T<2\)、每份满足此 S3 的给定完整有理表。令 \(\epsilon=2-T\)。结论针对指定 pullback \(A_s=a_s,\ Z_e=a_sE_e\)，不另找 canonical 点，也不改变任何使用到的旧 entries。

Dependencies 只有此 Exact 的显式定义与普通有理 LP 的固定次数、固定有限约束求解事实。可选 PSD 部分额外使用同一个 \(L\) 的 raw M2，其他部分不依赖 PSD、CONFIG 或真实联合概率。

Status 为 informed Exact-only 独立重构通过；此文件不是作者历史 Proof 的认证、全球新颖性认证、一般 UM 舍入或实际 gap 结果。Software 为 none。

## 2. 记号和次数账

对 incidence \(e\) 所在 state 记为 \(s(e)\)。记其 private 原变量为 \(b_e\)，unit-head 原变量为 \(E_e\)，selector 在 state \(s\) root 的变量为 \(a_s\)。每原 incidence 的 cover equality 是
\[
b_e+E_e-1=0,
\]
每组 selector 的 cover equality 是
\[
H_g:=\sum_{s\in g}a_s-1=0.
\]
这些均是 \(L\) 意义下带全部所需乘子的等式，不预先解释成真实事件。

记 canonical primitive \(V\) 的 raw pullback 为 \(\phi(V)\)，允许的 canonical 行乘子为 \(W=1,V,1-V\)。其 pullback 有下列**非负系数 raw-literal 展开**：

| \(W\) | \(\phi(W)\) | 每项最多几个 literals |
| --- | --- | --- |
| \(1\) | \(1\) | 0 |
| \(A_t\) | \(a_t\) | 1 |
| \(1-A_t\) | \(1-a_t\) | 1 |
| \(Z_f\) | \(a_{s(f)}E_f\) | 2 |
| \(1-Z_f\) | \((1-a_{s(f)})+a_{s(f)}(1-E_f)\) | 2 |

所有等号都是普通多项式恒等式，重复变量或互补 literals 无需新假设。

两个直接支付规则是：

1. 任意至多四个 raw literals 的乘积具有非负 \(L\) 值：非空时取一个 literal 作 box 行，剩余至多三个作其乘子；空乘积的值为一。
2. 任意原 affine 不等式行 \(h\)，乘至多三个 raw literals 的每项均有非负 \(L\) 值；因而乘这种乘积的非负线性组合也非负。

后面的所有不等式都明确落在这两条规则内，不把度数四的未知表外条目补成真实 law。

## 3. 声称 A：实际 schedule 的必要性与 sound FAIL

给任何 makespan \(\le T\) 的完整原 schedule，每个原 finite endpoint 的 assignment 是 0 或 1，每 job 恰选一个端。以这个完整 assignment 的 Dirac functional 作 \(L\)，所有 Boolean/cover 带乘子等式逐点成立，所有 boxes 与物理 slack 非负。

由于 \(T<2\)，每个原 resource 上至多有一枚 unit-head job。这里也包括 private 系数为零的 incidence job：其 resource 端仍耗时一。因此 unit-cap **1** 行逐点成立，乘任意 raw literals 的非负乘积后仍成立。Unused resource 的该行就是一。

这不要求 inactive incidence 留 home，故所有原合法 schedule 均已计入。S3 不可行便可排除实际 makespan \(\le T\)，而非仅排除某种 canonical schedule。反向可行性未作声称。

## 4. pullback 的规范化、Boolean 与组等式

F 的 entry 直接定义为原表对应 monomial：
\[
\begin{aligned}
F(A_s)&=L(a_s),&
F(Z_e)&=L(a_{s(e)}E_e),\\
F(A_sA_t)&=L(a_sa_t),&
F(A_sZ_e)&=L(a_sa_{s(e)}E_e),\\
F(Z_eZ_f)&=L(a_{s(e)}E_ea_{s(f)}E_f).
\end{aligned}
\]
因此最高需要 raw degree 四；有重复变量时也使用同一完整表及其 Boolean identity。\(F(1)=1\) 且该二阶表对称。

\(A_s\) 的 Boolean identity 是旧 Boolean identity。对 \(Z_e\)，普通多项式恒等式
\[
(aE)^2-aE=(a^2-a)E^2+a(E^2-E)
\]
恰使用 Boolean 乘子的次数二与一，所以 \(F(Z_e^2-Z_e)=0\)。

组等式及其乘任意 canonical primitive 或补，就是 \(L(H_g\phi(W))=0\)。\(\phi(W)\) 的 monomials 次数至多二，严格包含于原 selector-cover equality 允许的次数三。因此所有要求的组等式同时成立。

## 5. boxes 与 gate 的全部共同条件

每个 canonical positive primitive 或其补均有 §2 的非负 literal 展开。其 box 行再乘任意 \(W\)，每个展开项至多有四个 raw literals，故规则 1 支付全部 boxes 及其 primitive/补乘子。

每个 gate 的 raw 多项式恰是
\[
\phi(A_{s(e)}-Z_e)=a_{s(e)}(1-E_e).
\]
再乘 \(\phi(W)\) 后，每项同样至多四个 raw literals。因此每个 gate 的空、任意 primitive、任意 primitive 补乘子全部成立，包括该乘子与 gate 自身重复或共享变量的情况。

## 6. canonical resource 行的全部共同条件

记原 unit-cap 行为
\[
C_u=1-\sum_{e:u(e)=u}E_e.
\]
Canonical resource 行的 raw pullback 有精确恒等式
\[
1-\sum_{e:u(e)=u}a_{s(e)}E_e
=C_u+\sum_{e:u(e)=u}(1-a_{s(e)})E_e.
\]
乘任意 \(\phi(W)\) 后，第一项按 §2 表展开，每个乘子至多两个 literals，故由原 \(C_u\) 行的共同 localizers 支付。后面每个项乘子至多四个 literals，由 boxes 支付。所有加项的系数非负。

故该 canonical resource 行在同一个 F 下乘 \(1,V,1-V\) 均非负。没有只用一阶 cap 后分别拼接条件点，也没有按 state、group 或 resource 更换二阶表。

## 7. quality 行：真正用到第三个 raw literal 的位置

State \(s\) 的原 root slack 为
\[
h_s=T-a_s-\sum_{e\in s}p_e b_e.
\]
记其 canonical quality pullback 为
\[
q_s=\sum_{e\in s}p_e a_sE_e-\epsilon a_s.
\]
由 \(T+\epsilon=2,\ \sum_{e\in s}p_e=1\)，有精确的普通多项式恒等式
\[
q_s-a_sh_s
=(a_s^2-a_s)
+\sum_{e\in s}p_ea_s(b_e+E_e-1).
\]
对任意目标乘子 \(W\)，右边第一项乘 \(\phi(W)\) 使用 Boolean identity 的次数至多二乘子；第二项使用原 incidence-cover equality 的次数至多三乘子 \(a_s\phi(W)\)。因此
\[
L(q_s\phi(W))=L(h_s a_s\phi(W)).
\]
最后 \(a_s\phi(W)\) 按 §2 展开，每项至多**三个** raw literals；原物理 slack 的 S3 localizers 正好全部支付。特别地，\(W=Z_f\) 时使用 \(h_s a_sa_{s(f)}E_f\)，\(W=1-Z_f\) 时分别使用
\[
h_sa_s(1-a_{s(f)}),\qquad
h_sa_sa_{s(f)}(1-E_f).
\]
最高物理次数四，没有引用 degree 五条目。

由此全部 state quality 行在空、任意 canonical primitive、任意补乘子下同时非负。这个步骤也说明只保留更弱的物理一阶或二阶付款不能由本证明免费替代 S3。

## 8. 零、inactive 与给定点保真

零 incidence 的原 \(b_e,E_e\) 及 canonical \(Z_e\) 都未删除。其系数在 §7 中为零，不妨碍 §5 gate/boxes 或 §6 resource 容量；其 unit-head 仍必须进入原 cap 行。未选 state 没有被人为设定 inactive-home：\(Z=aE\) 的新 claim 只是从原出口中截取 selected 部分，原其它 entries 仍保持原值。

Indexed 重复 state 的 selector 端变量与原 jobs 继续独立编号；没有去重。Unused resource 行也没有删去。若某给定原 state 恰有 \(L(a_s)=0\)，本证明从不除以该数或作条件化，仍逐式成立。

提取中的每个 F entry 恰是给定 L 的指定旧 monomial entry；没有修补旧三阶/四阶值，没有重新求另一个点，也没有把 new pullback moments 当成同名 raw assignment moments。

## 9. 声称 C：同点 raw M2 足够支付 canonical M1

任给 canonical affine 多项式
\[
\ell=c_0+\sum_s c_sA_s+\sum_e d_e Z_e,
\]
其 raw pullback
\[
\widetilde\ell=c_0+\sum_sc_sa_s+\sum_ed_ea_{s(e)}E_e
\]
次数至多二。由定义与线性性，
\[
F(\ell^2)=L(\widetilde\ell^{\,2})\ge0
\]
恰是附加的同点 raw M2。故 F 的完整 canonical M1 PSD 成立。这里没有从 SA3 单独推出 PSD，也没有把 raw 二次矩量子 Gram 免费升成 commutative M2。

这仅为给定有限有理证书的保持；不提供 exact SDP finder，不声称任意实 SDP 可行点可由有限有理点替代。

## 10. 固定次数 LP、总位成本与结论边界

Raw 变量数为 N，degree \(\le4\) 的可交换完整 monomial 表有 \(\binom{N+4}{4}=O((N+1)^4)\) 个 entries。令原 affine 不等式行数为 R。至多三个 raw literals 的乘积数为 \(O((N+1)^3)\)，故这些不等式至多 \(O(R(N+1)^3)\) 条。Boolean identities 与 job-cover identities 亦只有固定多项式条数。

Literal 乘积展开最多八项；每 affine 行的原 coefficients、T 及全部 p 来自显式二进制有理输入。写出矩约束时系数的加法、重复合并与符号展开只有多项式 bitlength，因此 S3 为普通显式 rational LP。可用普通 rational LP 可行性算法产生有理可行点或判 infeasible；这是固定次数算法性陈述，不含隐含 CONFIG separation 或概率倒数 oracle。

Canonical primitive 数为 \(O(N)\)，输出一、二阶表有 \(O(N^2)\) entries。每项只是查询一个已给旧 monomial entry，重复索引按原表表示处理；据此在显式输入和给定原点总位长的多项式时间、输出总位长内可完成。无需 \(\epsilon^{-1}\)、\(L(a_s)^{-1}\) 次展开或枚举真实 schedules。

Objections 已实质核对：unit-cap 的 soundness 依赖 \(T<2\)；quality 依赖 state 系数总和一、完整 raw root slack 以及第三个 raw literal；canonical complement 必须按 §2 展开；所有 lifts 必须使用同一个 L。Exact 已明确支付这些条件。

本次通过的范围正是 S3 必要性、同点 product pullback 到 plain common primitive-SA1、可选同点 M2 到 M1 及固定次数 LP/提取。它不证明 raw K2 自动包含 S3、不输出真实共同 schedule law、不证明一般 normalized Q 的固定全组质量，也不完成一般 UM 近二困难性或其否定。
