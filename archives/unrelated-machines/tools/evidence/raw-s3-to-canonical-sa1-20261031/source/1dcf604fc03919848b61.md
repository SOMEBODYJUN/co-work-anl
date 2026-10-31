# raw S3 同点提取：作者 Proof 实读后对照

作者：/root/sol_identity_coupling，2026-10-18。此为 Exact-only 重构冻结、root 实际全文读该重构并明确释放作者 Proof 之后的对照记录；不替换、不改写旧独立记录，也不追认更早未读材料。

## 1. 实读及证据顺序

第一阶段仅实读 Exact：

sol_raw_sa3_to_canonical_sa1_exact_v1.md
SHA256：9c2a180330eed2a9b5f5b35b07eb76e2b33ed7ff853bba7376cc06e060595b71。

随后独立重构并冻结：

sol_identity_coupling_raw_sa3_canonical_sa1_exact_reconstruction.md
SHA256：5ee6c219ebde7bd459ba1f5afa24442cb8111de21d3bbfd1fea9bbcdc664746e；11264 bytes，172 行，0444。

本次再**实际全文读**唯一释放的作者 Proof：

sol_raw_sa3_to_canonical_sa1_author_proof_v1.md
SHA256：de3736cf6fd4d601c96f87f2c2af28e5b15bf62b25855b85134b761c6d0d0778。

此前已有 normalized-flat、primitive-SA1、raw/CONFIG 背景；本次不称全方向盲审。未读无关 code 或新的未释放 Proof，未修改 repo。

**对照结论：作者 Proof §1–9 与已冻结独立重构一致；本次实读未发现新增 fatal。** 以下分别记录代数、固定次数有理 LP 和可选 PSD 的付款。

## 2. 全合同代数对照

| 作者 Proof 部分 | 实读后核对 |
| --- | --- |
| §1 原端变量与总次数 | 保留 incidence private 端、unit 端及全部 selector 端；未先要求 inactive-home；pullback 的最大 raw 次数为四。 |
| §2 cylinder 正性 | 四 literal 的非负值直接来自一个原 box 乘其余三个；没有从 PSD 或真实 law 猜测。 |
| §2 补乘子 | \(1-aE=(1-a)+a(1-E)\) 为正系数 raw-cylinder 展开；补变量不会要求未支付的第五次矩。 |
| §3 Boolean | \((aE)^2-aE=(a^2-a)E^2+a(E^2-E)\) 的 Boolean multiplier 次数分别二和一。 |
| §3 selector group | 原 selector cover 乘 canonical pullback 的次数至多二；原合同允许三。可选同组 pair 排除也能由 one-hot、boxes 和 Boolean 推出，不是额外原假设。 |
| §4 boxes/gate | 每一行乘任意 canonical primitive 或补，均展开为至多四个 raw literals 的非负组合。 |
| §5 resource | 用原 cap1 加 \(\sum(1-a)E\)；cap1 的 raw multiplier 至多二，补项至多四 literals。不能以 \(T-\sum E\) 代替 cap1。 |
| §6 quality | 原 job cover 乘 \(a_sW\) 的次数至多三，Boolean 乘 W 的次数至多二；原 physical slack 乘 \(a_sW\) 的 literal 长度至多三。 |
| §7 必要性 | 实际 \(T<2\) 使每原 unit resource 至多执行一枚 job，包括 private 系数零的原 job，故全部 Dirac lifts 有效。 |
| §7 可选 PSD | affine canonical q pullback 为 raw quadratic，原同点 M2 恰支付 q 的平方。 |
| §8–9 范围 | LP、同点提取、sound FAIL 的算法规格与一般 UM 舍入/真实 gap/SDP finder 均明确区分。 |

作者 §6 用模原 identities 的同余式；独立重构中的精确恒等式为
\[
q_s-a_sh_s
=(a_s^2-a_s)+\sum_{e\in s}p_ea_s(D_e+E_e-1).
\]
其中 \(q_s=\sum_{e\in s}p_ea_sE_e-\epsilon a_s\)，\(h_s=T-a_s-\sum p_eD_e\)。两种写法逐项一致。对任意其他 group/state 的 canonical W，仍只用同一个 L；没有拼接各自可行的条件点。

## 3. 作者 §8 有理可行点位长论证的独立核对

在 square-free 表示中，对 degree \(\le4\) 的任意 monomial M，原 boxes 及其至多三个 literal 乘子给
\[
0\le L(M)\le1.
\]
下界取 M 中一个原变量作 box，其余作乘子；上界由 \((1-x)M'\) 非负得到 \(L(xM')\le L(M')\)，反复去掉因子直到 \(L(1)=1\)。常数情形直接成立。

完整次数四表中的重复幂也全部由允许的 Boolean identities 线性消去。例如消去 \(x^2m\) 的一次步骤所用 m 的次数至多二；反复应用覆盖 \(x^4,x^3y,x^2y^2\) 等全部可能重复模式。因此完整表没有未受控的重复幂自由方向，亦可直接使用约化表。

变量数 \(O((N+1)^4)\)，行数为原 affine 行数乘 \(O((N+1)^3)\)，另加固定多项式个 Boolean/cover 等式。Literal 乘积最多八项，source 行只含显式有限端 coefficients；写出、合并系数的 bitlength 由输入多项式控制。

若可行，约化 feasible polytope 非空且有界，故有 vertex。选择确定该 vertex 的线性独立活跃行并逐行清分母，整数系统维数、系数 bitlength 均为输入多项式。Cramer 及 Hadamard 行列式界给 vertex 分子、分母的多项式 bitlength。此处不存在按多项式数量的变量把某个超多项式分母假设偷偷藏进输入的问题。

因此普通有理 LP 可在该显式固定次数 LP 上求有理可行点或判 infeasible。这个结论只针对 S3 的 rational LP，不要求 M2，也不为另附的 PSD 可行性提供 exact finder。

给定完整有限有理 L，所有目标一、二阶条目只是 raw degree 至多四的指定表项；取出这些条目的总时间、输出总位长至多为显式输入及给定点总位长的多项式。没有按 \(\epsilon^{-1}\) 或 selector marginal 倒数循环。

## 4. PSD 与合同强度边界

作者 Proof 没有用 raw M2 代替 S3 literal localizers。没有原 S3 行的输入，§2、§5、§6 的付款就不能由本对照补足。反过来，单独 S3 已给 plain canonical R；若同一点另外满足 raw M2，才有同一点 canonical M1。

可选 PSD 命题是给定证书的代数保持：
\[
F(q^2)=L(q(a,aE)^2)\ge0.
\]
它不把任意实 PSD 点视为已有有限有理证书，不交付 exact SDP finder，也不声称 SA3 自动 PSD。完整 pullback 的实矩也可作同样数学推导，但有限有理输入/输出与 LP 算法声称只在 Exact 指定有理合同内使用。

## 5. 最终记录状态

Exact A、B、C 与作者 Proof 的本次全文对照均通过。零 incidence、inactive exports、重复 indexed states、unused resources、\(T=1\) 和 selector marginal 为零的情形无额外除法或删对象，未发现遗漏。

Software、运行和 exact checker 均为 none；本记录依赖逐式重构及全文实读。它只认证这份作者 Proof 在指定 S3 合同内的当前数学内容，不认证未知历史 Proof，不宣称 raw K2/native C2 已支付 S3，不给实际 all-groups rounding 或一般 UM 主目标结论。
