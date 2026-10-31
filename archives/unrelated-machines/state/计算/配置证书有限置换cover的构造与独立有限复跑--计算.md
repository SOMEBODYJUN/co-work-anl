---
id: "unrelated-machines/config-finite-cover-source-and-independent-replay"
kind: "computation"
type_tag: "计算"
title: "配置证书有限置换 cover 的构造与独立有限复跑"
status: "two-original-audits-and-one-source-helper-witness-export-completed"
summary: "给定有理CONFIG点的输出敏感socket/置换实现与独立q6证书分别复跑，保128base调度逐clone无损lift、160真混合/3边界/7拒绝和570短词检查；另执行原自带helper一次导出完整42-job/24-machine证书，不冒高围长group实际生成或位多项式归约。"
source_refs:
  - "clean:1e0d47d8b4a911adfb02"
  - "clean:1960e8b185c6cc6337eb"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/configuration_finite_cover.py"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:tests/audits/unrelated_machines/configuration_finite_cover_independent.py"
legacy_ids:
  - "UM-CONFIG-FINITE-COVER-v1"
---

# 1. 规范realize真正接收什么

原规范8490B、SHA `fe918b144c228e0ca43562654d612400ea32dea8a14a048ac11c9323afaf3378`，独立5809B、SHA `ec33b361e07837b727631f401e80ae7b827f727437a19446b3b58968c64644a6`，均完整读。规范模块不接通配置LP：`realize(p,y,T)`只收非负int/Fraction，拒bool/float及字符串；None是禁止端。p非空矩形、每job至少一finite端；给每机全部配置及精确权，代码逐项检查index、不重复、finite资格、配置负载≤T、行权一、job全覆盖一，**列出的零权配置也检查合法性**。

设q是非零配置权分母的lcm。对每机i建q个copies，按q*y_iC放配置C。每原j的selected sockets总数恰q，逐一分配job-copy标签a。某socket(i,b)被a选中就设pi_ij(a)=b；每incidence的这部分映射域/值都不重复，按固定词典序把剩余域和值补成完整[q]置换。返回每finite边的q项置换、nq枚原job-copies的actual sigma、mq行负载与所放配置。

每(j,a)恰有一个目的(i,pi_ij(a))，处理时间仍原p_ij，峰≤T。每machine-copy对一个原j最多一个邻居，所以反向从actual去标签按q平均也给原CONFIG(T)。这些是same-type incidence permutation cover，不能额外复制/合并端或改时间。

循环显式生成q份对象，时间只承诺对**显式输出规模**和所给证书编码多项式。q可对输入位数指数，logq小不使mq/nq输出小。不是求CONFIG点、最小q或多项式规模hardness归约的算法。

# 2. 四机七job seed和q6真正执行的证书

基机A/B/a/b，共同job c仅A/B时间一；每root r有三原job r0,r1,r2，在r时间1/3、对应terminal时间一。其它端禁止。配置阈值T=4/3：每root以1/2取全部三small，以各1/6取(c,rj)；每terminal三个singleton各1/3。共同分母6。

两个原程序各枚举全部2^7=128个普通base调度，得到OPT5/3。其下界可直接证：c到某root，若峰<5/3它至多再收一small，其余至少两件到terminal造成二；c+两small留root达到5/3。CONFIG阈值恰4/3的反向下界则在[既有cover等价审查](../审查/有限置换cover的配置等价与高围长坍缩审查--审查.md)另证：T<4/3时root含c不能带small，两个terminal容量迫两root各至少期望两small，覆盖c不可能。程序字段`proved_in_account`不能误作通用LP优化。

q6具体实现有24机、42job-copies：每root前三copies放全部small，后三分别放c+一small；每terminal各singleton用两copies。规范与独立程序的copy标签/配置顺序可不同，均按真实socket补全14条原finite incidence的置换，得到实际峰4/3。每个程序还核全部128个base调度无损lift：对原sigma(j)=i，把全部j-copies沿pi_ij送到i-copies，每个clone负载都等于base i负载，**包括原来过载的调度**。

规范程序另从返回actual sigma重新投影机器copy配置，核其恰等原分布，而非直接回读存下的configs。一般配置阈值在任意cover下相等及本seed T_CONF=4/3，才使这个已给4/3调度的cover精确OPT=4/3；单独程序feasible输出不是求cover OPT。恒等置换q6是六份seed，仍OPT5/3，所以同q/同seed不决定整数OPT。

本seed恰为activation seed乘4/3的重命名矩阵（G→c、C0/C1/C2/C3→A/B/a/b）；配置概率相同。这里q-fold graph cover与[激活提升](配置激活提升的一步与双符号支撑删除复跑--计算.md)是不同构造，其24/42和16/12机器/jobs不能混。

# 3. 两原audit的真实有限范围

规范`audit()`本轮一次exit0：128base分配、q6 witness、160个seed20261017生成的真实分布混合、3边界（空jobs、零时间、单finite端）及7非法输入拒绝（float、bool、无finite端、重复job配置、行质量不一、负载超T、bool当index）。random输入由源代码+seed确定，程序没有dump160个fixture，本包也不假称拿到了其完整逐例JSON。

独立脚本不import规范模块，另硬编码base/cover，128base及逐clone lift核查，3退化。它还检查短自由约化词：生成元数d1、g1..10；d2、g1..4；d3、g1..3。按词球B内的partial右乘映射补成置换，负字母用逆；每个非空词w从空词作用后确达w≠空，共570次。

这只检查partial-permutation机制的有限词。一般高围长cover证明必须再用生成有限群对自身的**regular作用**，非恒等置换本身不代表无fixed point。原代码没有枚举生成群、没有实际物化任何高围长group cover，也不计算其规模；完整存在性在current12579B正文自足证明，本轮已全文比较。

# 4. 额外一次原helper导出，非重复audit

为了让读者直接核42个实际job-copy位置与14条完整置换，本轮除两原CLI外另起**一个**进程，调用原规范模块已提供的`serial_fixture()`和`serial_witness()`，导出seed与actual-cover-witness JSON；后一helper执行realize一次，未调用或重跑audit主函数。helper代码/命令/stdout/stderr和新生成全部sigma/loads/permutations在[证据](../../tools/evidence/um-next-actual-audit-set/README.md)。这次明确计为supplemental witness export，不伪称第二独立实现或第三原审计。

历史seed3dd0、witness750a与当前导出逐结构及全字节相同；规范f1b8/独立172b旧摘要和本轮新stdout也独立保存。旧摘要分别另附4、5个provenance字段，其余共有字段完全相同；这些后附字段并非脚本本次stdout自动输出。历史执行仍旧，本轮此family共2原CLI+1helper过程。其它同批activation与single-cycle各有自己的计数，不能相互代签。

# 5. 状态与用途

本页保存可执行构造和真正有限证据，[原seed精确证书](../审查/配置有限覆盖种子精确证书--审查.md)及一般[cover等价/高围长审查](../审查/有限置换cover的配置等价与高围长坍缩审查--审查.md)已有主数学，不重复建立新定理。未认证任意接线保NO、随机cover性质、一般NP源soundness、生成高围长的位多项式规模、一般CONFIG solver或UM近似/困难性。源字节与冻结历史不改，新blind/外审0。
