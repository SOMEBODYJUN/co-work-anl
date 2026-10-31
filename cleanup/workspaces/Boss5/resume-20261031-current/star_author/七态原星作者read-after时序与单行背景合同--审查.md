---
id: "unrelated-machines/seven-state-star-author-read-after-timing-and-background-contract"
kind: "review"
type_tag: "审查"
title: "七态原星作者 read-after 时序与单行背景合同"
status: "integrated-source-specific-scope-review"
truth_status: "local-kernel-confirmed-background-contract-only"
review_level: "full-source-read-and-cross-archive-comparison"
summary: "保留七态原星 Exact-first 冻结后才读作者全文的时序、两种 Cauchy 常数比较、全原 endpoint/CONFIG/总位合同和三个接线压力；不新增重复定理，不代签未读软件，不回填后来 LOCAL-v2 的显式稀疏配置输出。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_identity_coupling_seven_state_star_author_read_after.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_identity_coupling_seven_state_star_author_read_after.md"
source_id: "3a1dd9093f4b924ddcb8"
source_sha256: "7549910df7e0d48cb1835a3408f39e5b77eb2afee34c3779f5981046caed00fb"
source_size: 7527
---

# 七态原星作者 read-after 时序与单行背景合同

本页是来源级审查，不登记第二份七态局部定理。既有定理负责完整原矩与全局二次核；本页保留作者全文读后记录的冻结时序、证明比较、外部背景反例和未读范围。原字节由 source_refs 指向，来源对象为 3a1dd9093f4b924ddcb8。

## 1. 来源身份与阅读顺序

本源完整 7,527 bytes、100 行，SHA-256 为 7549910df7e0d48cb1835a3408f39e5b77eb2afee34c3779f5981046caed00fb；冻结提交为 68fad804ec5946cb296f77dc5b336308a66abf12 与 aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c 的同路径同字节对象。清洗本轮实读该记录及可见的相关正文；不冒充当年的执行者或新的盲审者。

实际 read-after 顺序是：

1. Exact-only 原文，SHA 939a9b12b0dc8d74aa9809f816140b8569d6c6d091ee6fd809492256d1a0b477；在读作者 Proof、插值消息、代码和 JSON 前，先完成独立重构。
2. 独立重构 7d61b211b43d03cdf3c64d16605ab745a2ef77dd1e0cf43896ff59b886f8ab86，10,797 bytes、224 行、0444；完成后才释放作者 Proof。
3. 作者 Proof d560f9cf9a263d75cb1fa518a118078bcd013de91af4a8c771ced9257f3ef072，6,379 bytes、86 行；root 释放后实际全文读 §§1–7，包括外部背景和固定次数方向。
4. 本 read-after 7549910d… 冻结；旧 Exact-first 字节不变，未登记新 Claim。

原独立稿已披露 raw SH3、共同 M2、原 unit-row pair 零向量、旧 diluted-law 和另一 growing-depth 候选背景；其独立性只针对所给新 Exact。root 参与过核心插值，不能算第二名盲审者。本源明确没有打开或运行作者代码、JSON，没有读新的 growing-depth 草稿，也未外审。作者对有限代码的叙述不能当本源执行证据。

## 2. 完整原矩及全称范围

对正偶数 d,s，2≤s≤d/2，令 eta=s/d、h=s/2、T=1+eta、p=eta^3/1000、u0=4p(1-eta)、e=4/5-p-u0。机器是彼此不同的 u,v,z_1,...,z_d；原 jobs 是 R,j_1,...,j_d。R 在 u,v 上时间均为 1；j_l 在 v 上时间 1/d、在自己的 z_l 上时间 1，其余端无穷。共 d+2 台机、d+1 枚不可拆原 jobs、2(d+1) 个有限条目。

令 C 为 R 在 v 的指示，Y_l 为 j_l 在 v 的指示，H=sum Y_l。真实 law P 按类别

| C | H | 质量 |
|---|---:|---:|
| 1 | d | p |
| 1 | 0 | 1/20 |
| 1 | h | 1/20 |
| 0 | 0 | 1/20 |
| 0 | h | 1/20 |
| 0 | d/2 | u0 |
| 0 | d | e |

选类后均匀选大小 H 的 home 子集。每个样本完整分配全部原 jobs，且负载为 load_u=1-C、load_v=C+H/d、load_z_l=1-Y_l。由真实 law 的平方期望，同一个 L[f]=E_P[f] 给共同 M3 PSD、全部 Boolean/one-hot 等式，以及对每台机器和任意全局实系数次数至多二 q 的

    L[(T-load_i) q^2] >= 0.

q 可用任意机器和任意原 job endpoint，不限为行内或对称多项式。P 的 (C,H)=(1,d) 类以质量 p 产生 v 负载二；实际 OPT 仍为 1：R 放 u、全部 j_l 放各自 z_l 给峰一（也可用 R 放 u、全部 j_l 放 v 的峰一调度）。因此这里没有 actual near-two gap。

## 3. 作者证明与独立重构比较

端点代成 C、1-C、Y_l、1-Y_l 后，对 home 标签置换平均，二次 q 的均值必为 P_2(H)+C(a+bH)，其中 deg P_2≤2；active 与 inactive 支共享二次项。正余量类用 Jensen，唯一负类 (1,d) 只有一个 home 集，置换平均不改变 q 的实际值，所以该降维覆盖非对称、跨机器的全部全局 q。

令 lambda=d/h=2/eta，q_a(x) 与 q_i(x) 分别是 C=1、0 两支。作者的五点评估恒等式是

    q_a(d)=lambda*q_a(h)+(1-lambda)*q_a(0)
             +q_i(d)-lambda*q_i(h)-(1-lambda)*q_i(0).

五系数平方和为 4 lambda^2-4 lambda+3，且不超过 16/eta^2。五个正状态的质量乘 slack 都至少 eta/40；因此坏项满足

    p*(1-eta)*16/eta^2 <= 16*eta/1000 < eta/40.

普通 Cauchy 已足够。独立稿的加权 Cauchy 给 S<321 eta^(-3)；作者稿较粗的等价控制可记作 S≤640 eta^(-3)，两者相容且都只给 PSD。乘以非负平方和后，对 q=0 只能使用非严格号；不能把任何版本宣传成冗余 monomial 基上的统一正最小特征值。

## 4. 全部 row CONFIG 与固定次数矩

v 行合法配置 law 将 active 的坏质量改到 H=s、再由 H=0 配平；inactive 的 H=d/2 质量拆到 H=0,d。变化保持 E(C)、E(H)、E(CH)，并以

    -p*d*(d-s) + u0*d^2/4 = 0

保持 E[H(H-1)]。均匀子集于是匹配 v 行全部原端点 first/pair（含对角）；u 与每个 z_l 只有一个可见原 job，可取真实 Bernoulli 边际。逐行 law 不被拼成另一份共同 assignment law。

给定 H 的固定阶矩由下降阶乘 (H)_a(d-H)_b/(d)_(a+b) 生成，冲突 one-hot 单项式为零；固定次数 D 的全部共同矩、M3、全局二次 localizer 和 row first/pair 可按显式原输入长度作确定性多项式位运算生成。没有指数支持枚举、未知调度或精确 SDP finder。后来 LOCAL-v2 的显式稀疏配置输出是额外成果，不能反向写入本作者票。

## 5. 外部背景只有单行合同

固定外部背景 b 时，必须给完整原 assignment 映射 Phi_b(C,Y)，每个坐标仿射于 C,Y，每个样本仍是真实完整 assignment；还必须保证指定 v 行没有固定新增 payload，使其负载仍恰为 C+H/d。这样 q∘Phi_b 仍为二次式，可逐背景应用上述估计并在随机背景上积分。

仅说背景固定并不足够。d=4,s=2 时原 P 有 E[load_v]=37/40；若在 v 固定加入一单位 payload 而仍取 T=3/2，q=1 给

    E[T-(load_v+1)] = -17/40 < 0.

即使 v 公式保持，其它行也不能免费接线：若某 z_j 加固定背景负载 b>eta，取 q=1-Y_j 得

    L[(T-load_zj)(1-Y_j)^2] = (eta-b)*L(1-Y_j) < 0.

u 行同理取 q=1-C。若合并 z_j=z_k，两个 unit endpoint 的 pair 至少为 Pr(H=0)=1/10；若合并 u=z_j，相应 pair 至少为 Pr(C=0,H=0)=1/20。由于 T≤3/2<2，合法 CONFIG(T) 不含两个 unit jobs，故这些 pair 不能匹配原矩。上述均是域外扩展压力，不是原 Exact 的反例；原小星中这些机器互异且无额外 payload。

## 6. 固定次数方向与版本边界

作者把 active-minus-inactive 的次数至多 D-1 作为固定 D 的 Lagrange 方向，提出系数 O_D(eta^(-D+1))、坏质量 c_D eta^(2D-1)，但没有给完整常数、分离节点、全部行 trade 或递归预算。这仍是未完成方向，不能升格为高阶 Exact、共同递归 law 或算法。

与已有七态局部核、coercivity-learning、GlobalQuadratic Exact 和最终扩展边界审查相比，本页唯一职责是保留作者读后身份、两套常数相容、三个数值接线压力和未读代码状态；不新增第二份定理。后续规范稿把两处 Gram 记法改为 Lhat[(X-f)^2]，并把 Cauchy 最后乘平方和的 < 改为 ≤ 以覆盖 q=0；这些后续纠错不改本源旧字节或 read-after 时序。

处置为来源级 integrated review。已知关系仅是：本页确认局部二次核的作者读后与受限单行背景合同，并限制其外推；没有 near-two gap、hardness、一般 UM solver、递归共同证书或六人 SPE 结论，不能造此类超边。
