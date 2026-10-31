# Exact-only：物理 K2 点的直接 canonical claim pullback 可以违反 primitive-SA1

作者：`/root/sol_general_repair`，2026-10-18。scratch 限定合同候选，不是一般 UM 间隙，不声称全球新颖性。本 Exact 不给作者证明、LDL、CONFIG构造或程序。

## 对象与 domain

使用 `sol_flat_unit_resource_path_c2_exact.md` 中的物理 K2(P,T)：同一个 Boolean degree<=4 functional，全部 job one-hot identities throughout degree4，global M2 PSD，每台物理机的 raw load 在所有全局 affine q 上的 localizer PSD，以及每机一份 legal CONFIG(T)分布共享全部一阶、same-machine pair。该合同不额外要求任意global triple/quartic literal非负。

Q有一个outer M、三个 helpers Hu,Hv,Hr；资源u,v,r,wu,wv,wr全部不同。所有states如下，未列系数为零且没有隐式incidences：

| group | state 0 | state 1 |
|---|---|---|
| M | u,v各1/2 | r系数1 |
| Hu | u系数1 | wu系数1 |
| Hv | v系数1 | wv系数1 |
| Hr | r系数1 | wr系数1 |

P(Q)是完整普通flat矩阵：每group一个unit selector可选其两个distinct private机器；每listed state-resource incidence一个job，在其private时间原系数、在其exact resource时间1，其余无穷。因而有14machines、13jobs、26有限endpoints，没有逻辑侧约束。

令b1,b2,b3为形式Boolean位，定义线性functional ell于三位Boolean商代数的所有degree<=4多项式：ell(1)=1，每个distinct单项式只按其不同位数取值，大小1取3/10，大小2取3/80，大小3取−1/160。重复位按Boolean合并。

全部原job-assignment变量通过下表替换定义共同L=ell∘substitution：

| group/state | selector去本private | 本state incidence去resource |
|---|---|---|
| M/0 | b1 | u incidence: b2；v incidence:1−b3 |
| M/1 | 1−b1 | r incidence:1−b1 |
| Hu/0 | 1−b2 | u incidence:1−b2 |
| Hu/1 | b2 | wu incidence:b2 |
| Hv/0 | b3 | v incidence:b3 |
| Hv/1 | 1−b3 | wv incidence:1−b3 |
| Hr/0 | b1 | r incidence:b1 |
| Hr/1 | 1−b1 | wr incidence:1−b1 |

每个incidence去其private的变量为同job resource变量的补；同group两个selector变量为同一个job的两个端。所有原变量的substitution均affine，因此上述ell足以定义所有原degree<=4矩。阈值固定T=7/4、epsilon=2−T=1/4。

## 精确声称

1. 这个共同L满足上述完整物理K2的所有Boolean/one-hot、M2及全部raw affine load localizer；存在有限有理CONFIG列表与它逐机共享first/same-machine pair。因此K2(P,7/4)可行。
2. P有一个执行所有原jobs的真实makespan1 schedule，因此实际OPT(P)=1；本例不是任何actual-OPT gap。
3. 对每原state令canonical state primitive A为其selector端，对每listed incidence令canonical claim Z=A·(该incidence的resource端)，并把canonical degree<=2矩逐字pull back到上述L（physical degree<=4）。所得点不满足plain common primitive-SA1 R_(1/4)(Q)。具体地，记Z_M0u=b1b2，A_Hv0=b3，则

       L(Z_M0u A_Hv0)=−1/160<0,

   而outer state0的canonical quality行乘A_Hv0亦为

       L([ (Z_M0u+Z_M0v)/2−A_M0/4 ] A_Hv0)=−1/80<0.

因此不能仅由此物理K2合同断言**同一点的直接canonical pullback**自动是primitive-SA1点，或自动给canonical activation quality的任意affine localizer。这不排除改点、另求R、其他packing提取或主算法；也不否定单outer给定R点/typed-Q-alone算法。若增加原全局triple literal非负，本证书立即被排除；若强制逐机CONFIG共享相应原三阶，本证书也不再是这里的合同。
