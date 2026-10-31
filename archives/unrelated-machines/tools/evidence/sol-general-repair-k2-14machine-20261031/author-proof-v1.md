# 作者证明：物理 K2 到 canonical primitive-SA1 的同点 pullback 反例

作者：`/root/sol_general_repair`，2026-10-18。对应 Exact-only SHA256 `a79fd77dc17c87a8729bc3c4b47088a434f24db98e37f95b0ec9e01ec604323a`。此为作者证明，不是独立审查。原程序、运行和本稿应在fresh reviewer冻结Exact-first记录后才释放。

## 1. 完整实例和 functional

实例、三位Boolean functional、全部原assignment端点的affine substitution，逐字采用Exact表。组M、Hu、Hv、Hr共4；indexed states8；listed incidences9；resources6。完整P含8台private、6台resource、4个selectors和9个incidence jobs，共14machines、13jobs、26有限assignment端点。所有其他单元无穷。T=7/4。

三位Boolean商代数中，设

    ell(1)=1,
    ell(b_i)=3/10,
    ell(b_i b_j)=3/80 (i!=j),
    ell(b1 b2 b3)=−1/160.

重复位合并。每个原assignment变量的substitution为b_i或1−b_i。同一个selector的两个端互补，每个incidence的两个端互补，故所有Boolean和job one-hot/exclusivity等式是商代数中的恒等式，乘至总degree4也成立。ell∘substitution因此给出一致共同原degree<=4 functional，不需要把ell解释为真实三位分布。

## 2. 完整 M2 的精确 PSD

按基

    1,b1,b2,b3,b1b2,b1b3,b2b3

形成7×7矩阵M。每个entry为ell(两基单项式的Boolean并集)。按此顺序，不换pivot的精确Schur/LDL正pivots为

    1, 21/100, 63/320, 7/40, 7/256, 7/288, 7/384.

因全部严格正，M正定。这个矩阵也可逐式复算；本证书不依赖一般Grigoriev/knapsack定理。选择这些有理数时参考了N=5,t=3/2的exchangeable slice公式，但这里全部所需数值及PSD仅由7×7精确矩阵证明。

任意原degree<=2 polynomial经substitution成为三位degree<=2 polynomial，位于上述7维span。故所有原degree<=2 squares的L值非负，完整原M2为该M的线性拉回。26个原变量的degree<=2 square-free monomials有1+26+325=352个，尽管完整M2规模大于7，PSD已由同一线性拉回对所有原多项式同时证明；不只核了部分原端点或一个小principal submatrix。

## 3. 全部 raw affine load localizers

所有原affine q在substitution后属于1,b1,b2,b3的4维span。除M的state0 private以外，每个private的raw load恒等于1；三个home资源u,v,r的raw load也恒等于1。fallback资源wu,wv,wr的raw load分别为b2,1−b3,1−b1。

对于load恒1的行，localizer=(3/4)M1，显然PSD。对于load为某个literal l的fallback行，T−l=(T−1)+(1−l)。其平方测试

    L((T−l)q²)=(T−1)L(q²)+L(((1−l)q)²)>=0,

因为l Boolean、q affine，(1−l)q至多degree2，M2已PSD。这同时覆盖任意全局原affine q。

唯一非平凡行private M/0的raw load为

    load=b1+(1−b2)/2+b3/2
        =1/2+b1−b2/2+b3/2.

在4维affine基1,b1,b2,b3上，K_rs=ell((7/4−load)q_r q_s)。按该顺序精确正Schur pivots为

    19/20, 21/304, 91/384, 5761/41600.

因此此localizer也正定。至此每台原physical machine的raw affine localizer均满足，而不是用canonical quality localizer替代它们。

## 4. 每机合法 CONFIG 与共享 first/pair

除private M/0外，每个physical row至多两个端，它们是互补literal或单literal，且所有同机distinct pair的substitution乘积恒零。用每个端e的singleton配置、权重L(x_e)，并在需要时加empty配置权重1−sum_eL(x_e)。这些权重均非负，各singleton时间1，合法且总权重1。其first与same-machine pair恰匹配L；这些行不要求配置的高阶条目与L一致。

private M/0的三个原端记S（selector，时间1）、P_u（u incidence的private端，时间1/2）、P_v（v incidence的private端，时间1/2）。其substitutions为b1,1−b2,b3。使用以下五个配置：

| configuration | weight | load |
|---|---:|---:|
| {P_u} | 14/80 | 1/2 |
| {S,P_u} | 21/80 | 3/2 |
| empty | 21/80 | 0 |
| {P_u,P_v} | 21/80 | 1 |
| {S,P_v} | 3/80 | 3/2 |

总权重1，全部load<=3/2<7/4。一阶分别为

    S:24/80=3/10,
    P_u:56/80=7/10,
    P_v:24/80=3/10.

三个pairs分别为

    S P_u:21/80=ell(b1(1−b2)),
    S P_v:3/80=ell(b1b3),
    P_u P_v:21/80=ell((1−b2)b3).

所以完整physical K2的CONFIG链接成立。该配置分布等价于本行临时使用三位patterns000,100,010,001,111，权重14,21,21,21,3除80；它只是重构本行first/pair的真实law，绝不被宣称与共同ell的三阶相同。事实上

    L(S P_u P_v)=ell(b1(1−b2)b3)=7/160>0,

但任何合法本行配置的该triple都为零，因为其load为2。因此若另加same-machine triple链接，本证书会被排除。当前K2并未加它。

## 5. 原P的真实OPT=1

选择M的unit r state、Hu own-u、Hv own-v、Hr fallback-wr。每个selector去所选private；所选state的唯一正incidence export到资源；其余所有原incidence jobs保留原private。u,v,r,wr各接收一个unit job，wu,wv不接收job；所有private loads均为0或1。所用13个原jobs全部且各一次，故完整C=1。单位selector给OPT>=1，于是实际OPT=1。

这一步不保上述伪矩，也不需要保任何伪first/pair。它是明确的另一个真实assignment。因此本例只攻击同点提取，不攻击任何允许改点或重新求解的算法。

## 6. canonical pullback 的两个明确负式

canonical state primitive A取对应物理selector端；claim取Z=A times该incidence的resource端。于是

    A_M0=b1,
    Z_M0u=b1b2,
    Z_M0v=b1(1−b3),
    A_Hv0=b3.

canonical degree2矩经substitution至physical degree4是有定义的。其非负box行Z_M0u>=0乘A_Hv0给

    L(Z_M0u A_Hv0)=ell(b1b2b3)=−1/160.

所以它不是plain primitive-SA1 R_(1/4)(Q)点。并且canonical activation quality的同一state lift为

    L(( (Z_M0u+Z_M0v)/2−A_M0/4 ) A_Hv0)
      = (1/4)ell(b1b3)+(1/2)ell(b1b2b3)
        −(1/2)ell(b1b3)
      =−1/80.

raw root slack h=7/4−load，canonical activation slack恰h'=A_M0 h。在这里h'是physical degree2；q=A_Hv0=b3为physical affine，L(h' q²)=−1/80。因此“raw h的affine localizer PSD”不能无代价换成“activation h'=A h的affine localizer PSD”。raw localizer的cross entry L(h A b3)可负而整个raw localizer仍正定，没有矛盾。

这个结论只说明上述**同一**physical K2证书不能按指定direct canonicalization变成所需plain-SA1证书。Q本身实际OPT1，也有别的R_1点；另求点、改矩、使用更强合同、或不经过完整canonicalR的packing提取不受此反例排除。补充global triple literal非负亦立即排除ell的负triple。

## 7. 实际程序范围

`sol_general_repair_k2_canonical_pullback_counterexample.py` 使用Fraction的Boolean多项式字典定义以上functional。实际完成：完整14机13job26端构造；各原job one-hot/endpoint exclusivity及Boolean substitution恒等式；7×7 M2与14个4×4 raw localizer正Schur pivots；每机finite legal CONFIG总权重、first、same-machine pairs精确匹配；负canonical entry和负quality lift；13原jobs实际C1 witness逐项端点/负载核对。

代码SHA256：`2453a3f8160c448a1c4e34d1ab24dde0949233de1142ea05aff524737e28f389`。

实际冻结stdout JSON：`sol_general_repair_k2_canonical_pullback_counterexample_run.json`，SHA256 `19cf02f51162a9cf0c04dbc70a5acfe272525d9284e02ae3c94384fec5de174d`。

有限审计是这个固定证书的精确核对，不是通用SDP求解器、所有P assignments枚举、全局novelty或外审。完整global PSD与所有degree4 identities由上述pullback/商代数证明，不能误说程序独立枚举验证了每一个原degree4等式。
