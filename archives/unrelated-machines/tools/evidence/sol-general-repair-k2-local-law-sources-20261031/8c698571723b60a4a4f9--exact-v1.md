# Exact-only：完整 local-row law 仍不保证直接 canonical primitive-SA1 pullback

作者：`/root/sol_general_repair`，2026-10-18。拟议正式身份 `UM-RAW-K2-LOCAL-LAW-DIRECT-CANONICAL-PULLBACK-OBSTRUCTION-v1`。scratch 新对象；未独立审查、不声称新颖性。此前14machine/13job固定证书的Exact、Proof与code全部保持原字节。本 Exact 不给作者证明、PSD分解、CONFIG law构造或代码。

## 1. 输入族与完整 ordinary P

对任意二进制编码有理数 `0<c<1`，令 `T=1+c`、`epsilon=2−T=1−c`。Q_c只有一个outer M及四个helpers Hu,Hv,Hr,Hs。八个资源u,v,r,s,wu,wv,wr,ws全部不同。全部indexed states如下；每个所列pair是一个真实正incidence，未列pair不存在：

| group | state0 | state1 |
|---|---|---|
| M | u系数c；v系数1−c | r系数1−c；s系数c |
| Hu | u系数1 | wu系数1 |
| Hv | v系数1 | wv系数1 |
| Hr | r系数1 | wr系数1 |
| Hs | s系数1 | ws系数1 |

每个indexed state的系数和为1。四个outer正homes在全部state索引间物理互异；每个home有自己的own-singleton helper，fallback都是与全部homes不交的私有资源unit-singleton。这是显式typed one-outer protected-home结构，没有其他辅助groups。

P(Q_c)是完整普通flat UM矩阵：每group只有一个unit selector，在自己的两个distinct state-private机器上可执行；每listed incidence一个不可拆原job，在该state-private机器时间原系数，在其exact resource机器时间1；其余单元无穷。所有原selectors及incidence jobs必须执行。共有18台机器（10private+8resource）、17个jobs（5selectors+12incidences）、34个有限端点。没有额外allocation/guard逻辑约束。

## 2. 共同 global functional 的完整指定

使用三位形式Boolean变量b1,b2,b3。ell(1)=1；任意distinct单项式仅由其不同位数取值：大小1为3/10，大小2为3/80，大小3为−1/160。重复位按Boolean合并。这定义三位Boolean商代数上的线性functional，并可对substitution后的任意次数解释；只声称其下述degree-four全局PSD合同。

全部原job-assignment变量按下表affine替换，定义共同L=ell∘substitution：

| group/state | selector去该private的变量 | 该state的incidence去resource的变量 |
|---|---|---|
| M/0 | b1 | u:b2；v:1 |
| M/1 | 1−b1 | r:1；s:1−b3 |
| Hu/0 | 1−b2 | u:1−b2 |
| Hu/1 | b2 | wu:b2 |
| Hv/0 | 0 | v:0 |
| Hv/1 | 1 | wv:1 |
| Hr/0 | 0 | r:0 |
| Hr/1 | 1 | wr:1 |
| Hs/0 | b3 | s:b3 |
| Hs/1 | 1−b3 | ws:1−b3 |

每个incidence去其原private的assignment变量为同job resource变量的补。每group两selector端是同一原job，表中之和恒1。该表给出全部34个finite endpoint变量，无省略端或free jobs。

## 3. 强化物理合同与量词

K2使用同一全局Boolean degree<=4 functional：normalized、全部原job one-hot/exclusivity及Boolean identities throughout degree4、global M2 PSD（对所有原degree<=2 polynomial squares），每台physical machine的raw load满足

    L((T−load_i)q²)>=0

对每个原全局affine q。逐机还须有total mass1的有限有理legal CONFIG(T) law。

本 Exact 要求比仅first/pair相容更强：每机上述同一份CONFIG law与共同L共享该机器row内**全部Boolean局部矩**。具体即对该row endpoints任意子集S，CONFIG包含S的概率等于L(product_(e in S)x_e)；empty S取1。由于L已通过三位Boolean商代数解释，任意局部次数都有定义；特别包括全部本地degree<=4条目以及完整row membership law。这里不要求跨机器的完整schedule分布、不要求CONFIG-list weight作为global随机变量，也不另加任意global triple/quartic literal positivity。

精确声称：对每个有理0<c<1，上述**同一个明确指定的L**及某些finite rational legal row laws满足所有这些物理要求。给定c的编码，可在确定性总位多项式时间显式生成P、该固定大小degree-four共同证书和全部row laws；不调用SDP求解器。

## 4. 实际最优与直接canonical pullback的失败

对每个0<c<1，P(Q_c)有执行全部17原jobs的真实makespan1 schedule，因而真实OPT(P(Q_c))=1。此族不是actual-OPT积分间隙，也不阻止改点、另求allocation或13/8 typed单outer算法。

令每canonical state primitive A取其selector端；对每listed incidence，直接令canonical claim Z=A乘该job resource端；canonical degree<=2 moments逐字pull back到上述physical L，使用原degree<=4矩。取

    A_M0=b1,
    Z_M0u=b1b2,
    Z_M0v=b1,
    A_Hs0=b3.

则该直接pullback不满足plain common primitive-SA1 R_epsilon(Q_c)，因为

    L(Z_M0u A_Hs0)=−1/160<0,

而outer state0的canonical activation-quality行乘A_Hs0为

    L([c Z_M0u+(1−c) Z_M0v−epsilon A_M0] A_Hs0)
      =−c/160<0.

产生负值的三个原端可分别选为：M-selector去private(M,0)、incidence(M,0,u)去resource(u)、Hs-selector去private(Hs,0)，三者位于三台不同physical machines。因此本声称特意排除“只是某一row的未共享triple导致失败”的解释；全部local row laws仍须按第3节共享。

它仅否定**给定物理证书同一点的指定direct canonical pullback**自动满足primitive-SA1/activation质量lift。没有声称不存在别的R点，或K2不能通过其他机制产生好实际schedule。未提出未审查的source-SA3充分桥；没有一般UM算法、困难性或全球新颖性结论。
