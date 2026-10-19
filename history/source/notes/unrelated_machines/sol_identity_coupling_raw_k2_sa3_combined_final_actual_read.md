# raw K2 局部 law 边界与 S3 修复：最终新增正文实读

作者：/root/sol_identity_coupling，2026-10-18。本记录为知情 final actual-read，不称全部方向盲审，也不把此次 §13 审查称为 Exact-first。

## 1. 精确阅读范围与顺序

本次对象是 single_outer_flat_with_raw_k2_boundary_and_sa3_repair_final_v1.md：

- 完整 SHA256：404cf16df23cffe7b7c61c498907b744047473cf2d2db4e403630e5b6279edd2。
- 实际核得完整文件 48840 bytes、702 行。
- 前 374 行独立取字节 hash 为 8c5fcf273f9cd99a7b31b6b082a0880fc7ce186a0771cf600241eb07cc86e221，25741 bytes，与 root 指定旧正文一致；本次只作此前缀完整性核对，**不重签**旧两算法或旧软件。
- 本次实际完整读第 375–702 行，分 375–540、541–702 两块；两块输出均未截断。这覆盖全部新 §13、§14 及最后的预期 review link。

§14 已有本人先仅 Exact 独立重构，冻结记录 SHA 5ee6c219ebde7bd459ba1f5afa24442cb8111de21d3bbfd1fea9bbcdc664746e；root 实际全文读后才释放作者 Proof，本人再全文实读并另冻对照记录 SHA 173148aa4baeac7d9fb66c6e4bad76c935999a9599d85473b56c9e0c9bcaa8b3。两个旧记录均未修改。

§13 本人此前未读该候选的作者 Proof；但已有 normalized-flat、raw 矩和 CONFIG 背景，且收到过相关接口讨论。本次直接读作者 final 全节并独立重核其全部数学，不冒称 §13 的 Exact-first 或历史 Proof 审查。

未读取正文指向的 linked review、未读或执行 root 两份程序、未改 source final、旧冻结件或 repo。

**结论：在本次 §13–14 的明确合同内，全文重核未发现 fatal。** 下列结论只认证所列正文数学与阅读范围。

## 2. §13 原矩阵、全部原 jobs 与变量

本节菜单有一个二态 outer、四个二态 singleton helpers，共十个 indexed states。由普通 flat compiler 得十个 private roots、八个物理不同 resources，共十八机器；五枚 selector 加十二枚 incidence jobs，共十七 jobs；五枚 selector 各两个 finite 端，加十二枚 incidence 各两个 finite 端，共三十四 raw variables。原 p 为 \(c,1-c,1\)，在 \(0<c<1\) 内全部正且每 state 总和一。

三位表对五枚 selector 的两个端都给互补值，每枚 incidence 的两个端也按原 job 取补。每原 finite variable 均为 \(0,1,b_i,1-b_i\)。因此在三位 Boolean 商代数中，每原 Boolean identity、每原 job one-hot/exclusivity 及其允许的乘子均恒为零；pullback 后构造 L 是完整的共同 degree-four 表。

不存在先删除 inactive jobs、把 presence 当同一 job、额外设逻辑模式或遗漏原 finite 端的步骤。

## 3. §13 global M2 的统一证明

Signed cube weights 确实为：000 与三个 singletons 各 \(35/160\)，三个 doubletons 各 \(7/160\)，111 为 \(-1/160\)。总和为一，分别给
\[
\ell(b_i)=48/160=3/10,\quad
\ell(b_ib_j)=6/160=3/80,\quad
\ell(b_1b_2b_3)=-1/160.
\]
对任何 Boolean degree \(\le2\) 的三位 q，其三阶差分为零，所以正文的七项插值式成立。若 S 是七个 positive patterns 的 weighted 平方和，则 weighted Cauchy 的系数为
\[
4(160/35)+3(160/7)=608/7,
\]
故
\[
\ell(q^2)\ge\bigl(1-608/1120\bigr)S=(16/35)S\ge0.
\]
这本身就是统一 PSD 证明，不依赖消元 pivots 的有限计算。

任意完整 raw degree \(\le2\) polynomial 经表代入后，确实只落在 \(1,b_i,b_ib_j\) 的七维 span；因此证明覆盖全部 596 个 square-free raw degree \(\le2\) monomials 的 Gram 拉回，而非只检查一个 principal submatrix。所列七个正 pivots 是附加证据，本次不以未读代码为其认证来源。

## 4. §13 全机 raw-affine localizers 与完整局部 laws

直接由全部原端计算两个 outer private loads：
\[
b_1+c(1-b_2),\qquad (1-b_1)+cb_3.
\]
在 \(T=1+c\) 下，其 slacks 分别为 \((1-b_1)+cb_2\)、\(b_1+c(1-b_3)\)，均为非负系数 literal 和。其余八个 private roots 及四个 home resources 的 loads 为一；fallback loads 为 \(b_2,1,1,1-b_3\)。这些已覆盖全部十八机器。

任意原全局 affine q 拉回三位 affine。对任一 literal l，\(lq\) 的 degree 至多二，且 Boolean 恒等式给
\[
L(lq^2)=\ell((lq)^2)\ge0.
\]
因此两条 outer slacks、constant slacks \(c\) 及其余 \(c+(1-l)\) slacks 都有针对**全部原全局 affine q** 的 raw-load localizer PSD。未把带 raw quadratic claim 的 canonical affine 多项式误当成 raw affine。

两位边际的 00、10、01、11 权重依次为 \(35,21,21,3\) 除以八十，均非负、总和一；单位置一概率为三成。每原机器的所有 endpoint variables 同时只依赖至多两位。故取该位集的同一真实边际，能给出本行完整 membership law，并与其全部 Boolean 本地矩一致。

正文两张 outer CONFIG 表逐个模式匹配：M0 的非空配置为 \(P_u\)、\(S,P_u\)、S；M1 的非空配置为 \(S'\)、\(S',P_s\)、\(P_s\)。Load 最高为 \(1+c=T\)。其余机器为 complementary unit pair、单 literal 或常数，所有正权配置 load 至多一。

所以 full local law 并未遗漏某一条本行 triple；每行至多三个原端，所有本地 Boolean 函数又已由其相依的两位边际支付。不同机器的 laws 没有被拼成真实 global schedule law，也没有声称 CONFIG 指标另附未知全局高阶矩。

## 5. §13 真实 OPT 与跨行反例

实际选择 M0、Hu1、Hv1、Hr0、Hs0 后，selected incidence jobs 分别去 \(u,v,w_u,w_v,r,s\)，六个实际 resources 互异。五枚 selectors 分别去所选 root，所有其他 incidence jobs 留其原 private roots。全部十七 jobs 恰执行一次，所有负载至多一；单位 selector 又给下界一。因此真正 \(\operatorname{OPT}=1\)，不是 fixed-pattern 下界或实际 NO。

指定 canonical pullback 给
\[
Z_{M0u}=b_1b_2,\qquad A_{Hs0}=b_3.
\]
故 box row \(Z_{M0u}\ge0\) 乘这个 canonical primitive 的值为 \(-1/160\)，已违反 plain common-SA1。两个变量来自三台不同物理机器所涉及的原端；这一失败不会被每机 full local law 付款。

对应 quality slack 为 \(h'=cb_1b_2\)，因此 \(L(h'A_{Hs0})=-c/160<0\)。在 Boolean 商代数中 h' 也是 selector 乘原 raw slack。取真正 raw-affine \(q=b_3\)，测试 \(L(h'q^2)\) 的物理总次数至多四，仍为 \(-c/160\)。故 raw slack 的 affine localizer 不能自动变成 activation slack 的同类 localizer。

这一负式**不是**对任意 canonical affine 平方的测试；canonical claim 含 raw quadratic，后者可能需六阶矩，正文明确不提供。增加 global triple-literal 非负即切掉本点，也不与下一节 S3 充分命题冲突。

## 6. §14 与已审 Exact/Proof 的逐式对照

本节保持一般 normalized-flat 的全部 listed incidences（包括零）、indexed states、unused resources、原 private/resource 两端和 selectors；目标为给定同一点的指定 pullback。与此前实读 Exact 及作者 Proof 一致。

- Actual \(T<2\) 确保原 unit resources 至多一枚 job，故 cap1 是必要有效行；它不是仅由 \(T-\sum E\) 作形式替代所得。
- 原 boxes 乘至多三个 raw literals 支付全部长度四 cylinder 的非负值。
- \(1-aE=(1-a)+a(1-E)\) 的正展开使任意目标 primitive/补乘子每项只含至多两个 raw literals。
- \((aE)^2-aE=(a^2-a)E^2+a(E^2-E)\) 使用 Boolean multipliers 次数二与一；组 one-hot 乘目标 W 只需原次数至多二。
- Canonical resource 的 \(1-\sum aE=(1-\sum E)+\sum(1-a)E\) 用 cap1 lifts 及四 literal cylinders。
- Quality 乘 W 与 \(h_sa_sW\) 在 L 下相等：精确差值为 \((a_s^2-a_s)+\sum p_ea_s(D_e+E_e-1)\)。Boolean multiplier 次数至多二、原 job identity multiplier 次数至多三，最后物理 slack 的 literal multiplier 长度至多三。

所有 W 均可来自其他 state/group 的 A、Z 或补，且始终使用同一个 L。Zero p、inactive exports、重复 state 和 \(T=1\) 不引入除数、删对象或各自条件点的拼接。

## 7. §14 总位成本、可选 PSD 与最终边界

Degree-four 表的变量数 \(\binom{N+4}{4}\)，原 affine rows 各有 \(O((N+1)^3)\) 个 literal multipliers；等式亦固定多项式条数。所有 coefficients 来自显式有理 p、T 和至多八项 literal 展开，bitlength 多项式。

Box lifts 给全部 square-free degree \(\le4\) moments 在 \([0,1]\)，Boolean identities 消去其余重复幂，故 reduced LP 可行域有界。非空时取 vertex，清分母后用活跃线性系统及 Cramer/Hadamard 得多项式有理位长。普通 rational LP 的可行点/FAIL 规格成立；FAIL 仅单向排除真实 threshold-T schedule。

Raw M2 若另外给在**同一点**，canonical affine q 拉回 raw quadratic，故直接 \(F(q^2)=L(q(a,aE)^2)\ge0\)。这是 canonical M1 的附加保持；并不提供 exact SDP finder、任意实点的有理 witness，也不从 PSD 免费取得 literal lifts。

§13 full local laws 不自动提供 §14 global lifts；S3 本身又没有 M2/CONFIG，所以两合同的方向没有误标。S3 到一般 Q 的 canonical relaxation point 不等于一般 Q 的实际 allocation，更不等于一般 UM 算法；主目标仍 OPEN。

## 8. 软件和认证的具体限度

本次只阅读最终正文及计算文件 hash，未读或运行正文 §13.6 描述的作者 Fraction audit 与 root replay 程序。因此不代签其中十八 localizers、七十二本地 monomials、七十二 membership patterns、四参数重放、十七-job audit 的软件实现或执行状态。一般 c 的数学在本次依靠上述统一证明核通。

同样没有以旧十四机前身的程序或 review 认证新十八机版本；final 对旧前身同机 triple 不相容的限制明确且不作历史升级。§14 本身 implementation/checker/run 为 none 的声明与此次阅读相符。

本次是新增最终 §13–14 的知情全文数学实读通过；不重签 prefix374、不认证未读软件或 unknown review，不对未读历史作者 Proof 作认证，也不据这些局部接口宣称全局 hardness/rounding 已完成。全部 source 及旧证据字节保持不变。
