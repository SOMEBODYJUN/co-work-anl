# 作者证明：full local-row law 下的直接 canonical pullback 反例族

作者：`/root/sol_general_repair`，2026-10-18。对应 Exact-only SHA256 `f958afc5baac6c031415c735c97ecb1febaa2240149b10c111e70ec2dac6b18b`。本稿不是独立审查；须待fresh reviewer冻结Exact-first记录后才释放。拟议正式ID为 `UM-RAW-K2-LOCAL-LAW-DIRECT-CANONICAL-PULLBACK-OBSTRUCTION-v1`。旧14machine/13job固定证书是诚实前身，不在此改写它的范围。

## 1. 完整普通矩阵与原变量

对任意0<c<1，令T=1+c、epsilon=1-c。Q、全部34个finite assignment端点的affine substitution和ell，均采用Exact的两张完整表。Q有5groups、10indexed states、12listed incidences和8resources；P有18machines、17jobs。所有states normalized，所有listed coefficients正，四个outer homes u,v,r,s跨state物理互异，四位helpers分别有自己的unit home和私有unit fallback；没有未付费额外组。

每个原selector有两个互补的affine端，每个incidence的private/resource端互补。每个端都是b_i、1-b_i、0或1。因此全部Boolean、job one-hot和同job端互斥在三位Boolean商代数中是恒等式，乘至原总degree4也成立。共同L=ell∘substitution是定义在全部原degree<=4多项式上的同一个functional。它并非分别为每机另造全局矩。

## 2. global M2 的两份自足 PSD 论证

ell的单、双、三位distinct矩依次为3/10、3/80、-1/160。对三位degree<=2基

    1,b1,b2,b3,b1b2,b1b3,b2b3

形成Gram矩阵。按此顺序精确Schur正pivots是

    1,21/100,63/320,7/40,7/256,7/288,7/384.

故该7×7矩阵正定。每个原degree<=2 polynomial拉回三位degree<=2 polynomial，所以完整原M2为该正定矩阵的线性拉回，因而PSD。34个原端的1+34+561=596个square-free degree<=2 monomials全部受这一论证覆盖，不仅一个7×7 principal submatrix。

也可不用消元，直接证这一点。ell等价于三位cube上的以下signed weights：000及三个singleton patterns各35/160，三个doubleton patterns各7/160，111权重-1/160。这不是概率分布，但确切产生上述全部矩。任意三位degree<=2 polynomial q满足三阶差分恒等式

    q(111)=q(110)+q(101)+q(011)-q(100)-q(010)-q(001)+q(000).

令S为七个positive patterns上的weighted q²和。weighted Cauchy给

    q(111)² <= [4(160/35)+3(160/7)] S = (608/7)S,
    ell(q²)=S-q(111)²/160 >= (16/35)S >=0.

若S=0则q在这七点和111全零，故Gram正定。此有限维证明完全自足，不依赖外部slice/SOS定理，也不声称全局literal非负。特别ell(b1b2b3)<0是被合同允许、被后文使用的信息。

## 3. 所有机器的全局 affine raw-load localizer

M/state0的raw private load与slack是

    load_0=b1+c(1-b2),
    T-load_0=(1-b1)+c b2.

M/state1则为

    load_1=(1-b1)+c b3,
    T-load_1=b1+c(1-b3).

其余全部private loads及全部home-resource loads恒等于1。fallback-resource loads依次为wu:b2、wv:1、wr:1、ws:1-b3。

对任意原全局affine q，拉回后仍为三位affine。任何literal l满足

    L(l q²)=ell((l q)²)>=0,

因为Boolean l²=l，而lq的degree<=2，受global M2控制。因此上述两个outer slack都是nonnegative coefficients的literal和，其localizer均PSD。其他恒1行的slack=c>0；fallback literal行的slack=c+(1-l)，localizer同样PSD。这个证明对每个有理0<c<1成立，不靠有限参数枚举，也未把raw slack替换为canonical activation slack。

## 4. 每台机器的完整 CONFIG membership law

ell在任意单个bit上的边际是真实Bernoulli，P(1)=3/10、P(0)=7/10；在任意两个bits上的边际也是真实law：

| bit pattern | probability |
|---|---:|
| 00 | 35/80 |
| 10 | 21/80 |
| 01 | 21/80 |
| 11 | 3/80 |

检查每台原physical machine：它的全部assignment endpoint variables同时最多依赖两个bits。M/private0依赖b1,b2；M/private1依赖b1,b3；其余每行至多依赖一个bit或仅常数。故取该行所用bits的上表真实边际，并按该行原assignment variables的substitution推出membership law。它是每行自己的一份真实CONFIG分布，不是全局schedule law。

具体地，M/private0的三个端是selector S=b1、u-private P_u=1-b2、v-private P_v=0，时间分别1,c,1-c。其完整law为：

| CONFIG | weight | load |
|---|---:|---:|
| {P_u} | 35/80 | c |
| {S,P_u} | 21/80 | 1+c=T |
| empty | 21/80 | 0 |
| {S} | 3/80 | 1 |

M/private1的端是selector S'=1-b1、r-private P_r=0、s-private P_s=b3，时间分别1,1-c,c。完整law为：

| CONFIG | weight | load |
|---|---:|---:|
| {S'} | 35/80 | 1 |
| empty | 21/80 | 0 |
| {S',P_s} | 21/80 | 1+c=T |
| {P_s} | 3/80 | c |

其余行都是单位互补pair、单literal或常数membership，所用单bit边际/常数law合法，load至多1。每机law总质量1，所有配置load<=T。

该law共享的不只是first/pair：本行所有endpoints的任何Boolean polynomial经substitution只依赖至多两位；ell对这些位的全部函数就是上述真实边际。因此任意本地square-free monomial、任意mixed membership/complement pattern、任意局部次数均与该同一行law一致。所有local-row triple甚至完整row law已共享，仍没有在机器间统一成真实joint schedule。

## 5. 真OPT=1与两个负式

实际schedule选择M/state0、Hu/fallback-wu、Hv/fallback-wv、Hr/own-r、Hs/own-s。每selector去自己的选中private；所有选中state positive incidence export exact resource，全部未选state incidence留其原private。资源u,v,wu,wv,r,s各一件unit job；所有private loads为0或1。17原jobs各一次，给C=1；unit selector给OPT>=1。所以OPT(P(Q_c))=1，与伪点是否可提取无关。

直接canonicalization给

    A_M0=b1,
    Z_M0u=b1b2,
    Z_M0v=b1,
    A_Hs0=b3.

由于epsilon=1-c，state0的canonical activation-quality slack正好是

    h'=c Z_M0u+(1-c)Z_M0v-epsilon A_M0
      =c b1b2.

因此

    L(Z_M0u A_Hs0)=-1/160,
    L(h' A_Hs0)=-c/160.

第一个违反canonical非负claim row乘原state primitive；第二个违反canonical quality row乘同一primitive。它也等于q=b3时的L(h' q²)。另一方面raw h=(1-b1)+c b2的affine localizer已证明PSD，说明不能把h的localizer自动换成h'=A h的localizer。

三个因子可取三台不同机器上的原端：b1是selector M去private M0，b2是u-incidence去resource u，b3是selector Hs去private Hs0。没有一台机器的full local law包含这三个bits。因此旧14机例的“同机triple未共享”缺口已经消除；本例的负triple完全跨行。增加任意global triple literal非负会排除它；本文未提出或使用source-SA3充分桥。

## 6. 总位成本、实际audit及严格scope

给定c，实例和矩数组维度固定；处理时间为c、1-c、1，证书矩和row laws权重为上述固定有理数。生成时间及输出位长对c的二进制编码多项式，不需要精确SDP求解。参数域只取0<c<1，避免把零权重端及T=1、T=2两个端点混入另一个结构声称。

程序 `sol_general_repair_k2_local_law_canonical_pullback_audit_v1.py` 是纯标准库Fraction。实际audit包括完整18机17job34端构造；Boolean和one-hot的substitution恒等式；7×7全局拉回Gram正pivots；18个4×4raw全affine localizers的精确正pivots（给定有限c）；每机完整law合法性及全部本地72个square-free monomial、72个完整membership patterns；两个负式；17原jobs实际C1 assignment逐一有限端点及load。

参数化PSD、全部degree4 identities和任意局部degree共享由前述代数证明；程序没有枚举完整P的所有assignments、所有原quartic identities或所有有理c。default原stdout在c=3/4；另有限参数c=1/1000,1/2,999/1000通过，不能把这些有限核验称为全参数证明。

本族只否定给定物理K2证书的指定direct canonical pullback自动属于primitive-SA1。它不否定别的R点、改点、重新求解、从K2提取某种更弱packing或单outer13/8算法；此P实际已给C1。它不是一般UM近二间隙、NP-hardness、外审或新颖性声明。一般UM主目标仍OPEN。
