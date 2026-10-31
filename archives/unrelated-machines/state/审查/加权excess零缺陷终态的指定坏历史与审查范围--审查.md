---
id: unrelated-machines/weighted-excess-zero-defect-specified-history-review
kind: review
type_tag: 审查
title: 加权excess零缺陷终态的指定坏历史与审查范围
math_scope: fixed-task-equations-and-protected-row-loads-with-permanent-elimination
status: proved-specified-elimination-contract; historical-priors-separated
summary: 真实OPT1凸包初态可经指定m步到满列秩D0坏固定核心；这条方向立即破big-count，不能与完整CONFIG路径反例混同。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/configuration_elimination_support_loss_review.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/configuration_elimination_support_loss_review.md
---

# 加权excess零缺陷终态的指定坏历史与审查范围

## 精确规则与来源边界

31684B/418行主review全文实读；它有global_exchange激活声明先行/规范读后、另一份双符号独立重构、strengthened_relaxation分阶段核查三段载体。本页只处理UM-WEIGHTED-EXCESS-ZERO-DEFECT-TRAP-v1。另全文读624行最终canonical a9c99e79cc528a0a278a812708d410852c5c022a170bfe3ba5f5a5941c5a29d7；其前27043B逐字为旧三身份693ece68235f8ead0523db180849781317bb43101b9bbdef247ecc176aa562d9，新§4 circuit不由此review代签。现有[消元/cover双源页](配置覆盖坍缩与永久消元双源审查--审查.md)已有结果，本页展开精确矩阵、真实秩和本review独有先验。

攻击规则：从给定分数点保持活任务等式和未删机器的“固定负载+活分数负载”等式；当前正活端excess

$$E_i=\sum_{j\text{活},x_{ij}>0}p_{ij}(1-x_{ij})$$

≤(1−ε)T时可永久删除该机器行；沿任一合法零空间方向走至首个0/1边界，整数任务永久固定，零端永久删除。本定理给**一条指定合法坏历史**，不声称所有选向都坏；允许回退固定/恢复端则超出该合同。

## 全矩阵、真实OPT和初态

固定有理0<ε<1，整数m≥3且m>1/ε。T1、q=1−1/m、β=(1−ε)/4。2m机H_i/Z_i，2m+1任务B及A_i/F_i：B在所有H_i时间1；A_i在H_i时间q、Z_i时间β；F_i在H_i时间1/m、Z_i时间β；其余∞，共5m有限端。这里q和β是**两个端的时间**，不是q/β相除。

最优原子S_h：B给H_h，A_h/F_h给Z_h，其余组两件都给各自H_i。H各负载1，Z_h负载2β<1，B的所有有限端1迫OPT1。均匀m原子给

$$x_{H_iB}=1/m,\quad x_{H_iA_i}=x_{H_iF_i}=q,\quad x_{Z_iA_i}=x_{Z_iF_i}=1/m.$$

H负载1/m+q²+q/m=1，Z负载2β/m，确为真实最优凸包点，非仅CONFIG/LST。初始E_Z=2βq<1−ε可全删；E_H=q+q/m+1/m²=1。处理后H只剩活B端，E_H=q>1−ε，未处理仍1，所有H始终保护。

## 每步最大方向、精确秩与所有补全

顺i取四端方向(1,−1,−(m−1),m−1)，依次为H_iA_i/Z_iA_i/H_iF_i/Z_iF_i。任务方向和0，H方向负载q−(m−1)/m=0，外机行已删；所有四个0/1边界比值均1/m，最大步恰1/m。终点四值(1,0,0,1)，永久固定A_i→H_i、F_i→Z_i。

完成t组后a=m−t，活变量N=m+4a、任务J=2a+1、保护P=m。a≥1时所有任务/保护行独立：未处理外端列先迫对应任务行依赖系数0，再由home列迫其H行0、锚端迫B任务行0，最后全部H行0。秩J+P、nullity2a−1，是真实秩不只计数。

a0时N=m、J1、Pm，m个H行在锚变量上为单位矩阵，秩m=N；B任务等式是这些行之和，故无非零方向。不能把N−J−P=−1误作负nullity。

此时每H固定q、活B分数1/m，保护负载仍1。总亏缺

$$D=\sum_{\text{活端}}(T-p_{ij})(1-x_{ij})=0<\varepsilon T(N-J)=\varepsilon(m-1).$$

但任一实际锚端选择都使对应H负载q+1=2−1/m>2−ε，其余H为q、外机β，所以**每个保持固定任务的补全**峰精确2−1/m。full-rank、D0及真实最优凸包初态并不自动保好补全。

## 为什么它不是CONFIG保持反例

q>1/2时H_i可行T1配置至多一个大于1/2任务，有有效不等式x_(H_iB)+x_(H_iA_i)≤1。初态取等，方向保持B不动而增A，任正步立即违反。故本紧凑历史不能攻击全过程维护big-count/CONFIG的不等式规则；另一个[激活提升](完整配置单次激活提升的精确支撑端点与两种初态--审查.md)才在整段保持CONFIG。机器/任务/全部m原子与m步有O(logm+bitε)有理系数、显式多项式总输出，不是NP难实例；任初始原子已直接给OPT1。

## 实际审查身份与有限范围

global_exchange最先只重构**激活**，冻12c271…后读e183…含两身份作者稿；紧凑部分属proof-aware读后，初次未读/跑紧凑audit。后来实际全文读旧三身份693ece…并读紧凑代码/JSON，但仍不执行它；不能把其激活先证或软件重放转记本紧凑反例。

strengthened_relaxation此前独立较大private-sink坏历史不认领此紧凑来源；首次紧凑已见作者证明/代码，属知情复核。其规范复跑包含8组ε,m（最大m11）的全部m步/中间精确秩/末m锚补全，输出与冻结JSON逐字节同。另历史临时Fraction检查(1/2,3),(1/3,4),(1/4,5),(3/4,4),(9/10,10)未import作者代码，但不称规范复用工具。

当前紧凑代码d258dda00769951e9830ce523c33d32c01adbb260cc50e0ecb0dd89531d09ea4，报告35dc6adc3c3447ca5138287e46fa0265c109f58817fcd946afff7235cb4f6beb；旧c70d…作者稿/05e96…代码与后版分开，完整hash见主原件。本批无新数学程序运行，不由历史票数认证外审/新颖性或一般UM反面。[原件/范围](../../../../tools/evidence/um-foundation-composition-configuration-reviews/README.md)。
