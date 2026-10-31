---
id: "unrelated-machines/seven-state-star-global-quadratic-exact-v1-review"
kind: review
type_tag: 审查
title: "七态原作业星 Global Quadratic Exact 与审计/延拓边界审查"
status: integrated
truth_status: "exact-only-scope-recorded; audit-owner-and-AND-objects-separated"
review_level: "full-read-5586-byte-exact-cross-archive-comparison"
scope: "UM-SEVEN-STATE-STAR-GLOBAL-QUADRATIC-EXACT-v1, finite global quadratic audit/root replay, affine owner boundary, faithful AND localizer and canonical extension boundaries"
summary: "cf33a00… 的 Exact-only 源给出一个实际 OPT=1 的七态原作业星：同一个真实完整 assignment law 同时满足共同 M3、所有全局次数二负载 localizer、逐行 CONFIG first/pair 和显式总位矩生成合同。本文完整读取 Exact，和既有 global quadratic audit/root replay、affine Boolean owner、faithful AND localizer、canonical/coercivity extension对象去重；不把局部核扩展为递归接线、near-two gap、一般 UM 算法或 hardness。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_seven_state_star_global_quadratic_exact_v1.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_seven_state_star_global_quadratic_exact_v1.md"
  - "source:ee0deff479cc5c374543:history/source/notes/unrelated_machines/sol_seven_state_star_global_quadratic_canonical_v1.md"
  - "source:bb7e2d9338cb057e7cdd:history/source/notes/unrelated_machines/sol_seven_state_star_global_quadratic_coercivity_learning.md"
  - "source:4c3957d3e5517fdc7ae5:research/current/unrelated_machines/seven_state_star_global_quadratic_and_extension_boundaries.md"
  - "source:ec117f60f81d65a9953b:evidence/runs/unrelated_machines/seven_state_star_global_quadratic_audit.json"
  - "source:177bb999d00126ea6ea9:evidence/runs/unrelated_machines/seven_state_star_global_quadratic_root_replay_scope.json"
related_objects:
  - "七态星全局二次审计与root重放范围审查--审查.md"
  - "../计算/七态星全局二次审计与root重放边界--计算.md"
  - "七态原星仿射Boolean所有者边界Exact与作者Proof版本审查--审查.md"
  - "七态AND端点二次localizer作者read-after审查--审查.md"
  - "鲁棒双端环与七态二次局部核双源审查--审查.md"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/seven-state-global-quadratic-exact-v1-20261031/original/sol_seven_state_star_global_quadratic_exact_v1.md"
source_sha256: "939a9b12b0dc8d74aa9809f816140b8569d6c6d091ee6fd809492256d1a0b477"
source_size: 5586
---

# 1. Exact-only 身份与来源范围

本轮完整读取 cf33a00ede88059b1cbe 的 Exact-only 源，5586 字节，SHA-256 为 939a9b12b0dc8d74aa9809f816140b8569d6c6d091ee6fd809492256d1a0b477。ClaimVersion 为 UM-SEVEN-STATE-STAR-GLOBAL-QUADRATIC-EXACT-v1，日期 2026-10-18。原文明确只给精确合同，不含证明；它把对象定位为实际 OPT=1 的局部构件，不声称递归接线、实际 near-two gap、一般求解器或主目标算法。

既有 global quadratic audit/root replay 审查已经登记 12 组有限参数、3 组完整高维矩阵、Fraction PSD/秩/assignment 字段和作者/root 输出字节一致性。本页补齐 Exact-only 原始量词、矩合同和显式输入边界，不把 audit JSON 当成任意参数定理或软件证明。

既有 affine Boolean owner、faithful AND localizer、canonical v1 与 coercivity-learning 资料各自研究延拓接口；本页只保留它们的关系与去重，不合并成一个“所有延拓均失败”的结论。

# 2. 原输入与真实完整 assignment law

取正偶数 d,s，满足 2<=s<=d/2。记 eta=s/d、h=s/2、T=1+eta、p=eta^3/1000、u0=4p(1−eta)、e=1−1/5−p−u0。于是 d>=4、0<eta<=1/2、h 为整数，所有参数是二进制有理数。

机器为 u,v,z_1,...,z_d，共 d+2 台；原 jobs 为 R,j_1,...,j_d，共 d+1 枚不可拆 job。有限 processing times 只有：

- R 在 u、v 上各为 1；
- j_l 在 v 上为 1/d；
- j_l 在 z_l 上为 1；
- 其余端点无穷。

恰有 2(d+1) 个有限条目。实际最优 makespan 为 1，例如将 R 放 u、全部 j_l 放各自 z_l。

令 C 指示 R 在 v，Y_l 指示 j_l 在 v，H=sum_l Y_l。完整 assignment law P 逐类选择 (C,H)，再在 [d] 中均匀选择大小 H 的集合 F，将 Y_l=1 当且仅当 l 属于 F。原端点指示是：

X_(R,v)=C，X_(R,u)=1−C；
X_(j_l,v)=Y_l，X_(j_l,z_l)=1−Y_l。

七类质量为：

| C | H | 质量 |
|---|---|---|
| 1 | d | p |
| 1 | 0 | 1/20 |
| 1 | h | 1/20 |
| 0 | 0 | 1/20 |
| 0 | h | 1/20 |
| 0 | d/2 | u0 |
| 0 | d | e |

所有质量为正且总和为一。P 给出的负载为 load_u=1−C、load_v=C+H/d、load_z_l=1−Y_l。load_v=2 的坏样本概率为 p>0，但其它机器在每个完整 assignment 中负载至多 1；另一方面真实 P 有峰值 1 的完整调度。因此这里的坏样本不是 actual gap 或 hardness witness。

# 3. 共同矩与全局次数二负载 localizer

Exact 取同一个真实完整 law 的线性泛函 L[f]=E_P[f(X)]，可以定义到全部次数；合同只需次数至多六。L 满足原 Boolean、每个 job 恰选一个有限 endpoint 的 one-hot 等式及其矩。

令 M3(L) 的行列为全部原变量次数至多三的单项式，条目为 L[ab]。则 M3(L) PSD。对每台机器 i、任意总次数至多二的实多项式 q(X)，要求

L[(T−load_i(X)) q(X)^2] >= 0。

q 可以同时使用任意机器和任意原 job endpoint，不限于被检查机器或对称多项式；等价地，每行用全局次数至多二 monomial 的负载局部化矩阵均 PSD。共同 M3 与全部行局部化矩阵使用同一个 L，不是每台机器独立换 law。

Exact 的全局合同因此是：同一真实 P 既给出实际完整 assignments 和 degree-six moments，也同时支付全局二次 load inequalities。坏样本的 load_v=2 只以正概率出现，不能通过把 law 改成每点峰值一来满足 localizer；峰值一来自另一个真实完整 assignment。

# 4. 每行完整 CONFIG(T) first/pair 一致性

配置行只使用该机器可处理的原 jobs，负载至多 T。各机器可以有不同配置分布，但必须与同一个 L 的原 endpoint 一阶、二阶矩一致；不要求逐行分布共用一个 joint support。

对于 v 行，Exact 定义 K_v：先选 (C,H)，再均匀选 H 个 j_l 留在 v；C=1 时还包含 R。其质量是：

| C | H | K_v 质量 |
|---|---|---|
| 1 | s | p/eta |
| 1 | 0 | 1/20+p−p/eta |
| 1 | h | 1/20 |
| 0 | 0 | 1/20+u0/2 |
| 0 | h | 1/20 |
| 0 | d | e+u0/2 |

这些质量非负且总和一，每个配置的实际负载不超过 T。对 v 行任一 endpoint a 及任意 endpoint pair a,b（包括 a=b），K_v 与 L 的 first/pair 矩完全一致。u 行只有 (R,u)，z_l 行只有 (j_l,z_l)，其 Bernoulli 真实 law 直接给出合法 CONFIG(T) 与同样 first/pair。

这项合同针对全部原 jobs：没有匿名 token、复制 job 或省略 payload。逐行配置 law 的分布可以不同，不能把 first/pair 通过不同局部点拼成另一份全局 assignment law；全局 law 已由 P 统一提供。

# 5. 显式矩生成和位复杂度

输入、P 和 K_i 都是显式有限描述；uniform H-subset 类别可以紧凑表示，不要求枚举指数多个集合。固定次数 D 时，任意原 endpoint 单项式的 L 矩可由类别和均匀子集参数精确生成；完整列出次数至多 D 的共同矩需要关于显式原输入总位长的确定性多项式时间和多项式位长。特别是 D=6 时可精确生成 M3、全部 global quadratic load-localizer 矩和每行 first/pair 矩。

各 K_i 的 first/pair 矩同样可在总位多项式内生成。该合同不调用优化、精确 SDP 可行性、未知调度或条件 oracle；复杂度按显式 d 个 jobs 的输入长度计，不是按 log d，也不声称枚举配置支持。

# 6. 与审计、canonical 和延拓对象去重

全局二次 audit/root replay 只对 12 组参数做有限 exact Fraction 检查。全部 12 组报告 row CFG first/pair、5 维 signed-slack exact PSD、home assignment 和 degree<=6 字段；只有 (4,2)、(8,2)、(8,4) 物化完整高维 M3/global-q2。审计给出的 full M3/global-q2 维数、秩、assignment states 和 moments 已在既有计算页登记；root replay 只证明指定 fresh CLI 输出与作者输出字节一致。audit 的 not_checked 明列 affine classification software、deep shared-owner、AND extension、general scheduling 和 SDP finder。

canonical v1 / coercivity-learning 以及 research 当前主源的四个身份要分开：

1. global quadratic local：本 Exact 的同一 L 和所有全局 degree-two load localizer；
2. uniform-cardinality sparse-support：通过交换或消列压缩配置支持，只保 first/pair，不自动保 higher moments；
3. affine Boolean owner boundary：对给定 Gram-covered affine endpoints，M3 支持落地后同机正 owners 至多两个；这是 01379ac 对象，不是本 Exact 的全部 localizer；
4. faithful AND localizer obstruction：在额外 base/fifth-moment 合同下，忠实非线性端点可产生负 localizer；这是七态 AND read-after，不等于本 Exact 的 global quadratic existence。

鲁棒双端环与七态局部核双源审查把本 Exact 的实际 OPT=1、共同 M3、全局二次 load localizer、CONFIG first/pair 和延拓边界与双端 phase gadget 分开；它们共同强调新接线必须重新核全部 jobs、负载和共同 law，不产生一般 UM gap。

# 7. 明确范围和未完成义务

本 Exact 支持的内容是：同一个真实完整 assignment law P，在该显式 (d,s) 输入上同时满足共同 M3、所有机器全局次数二负载 localizer、逐行合法 CONFIG(T) first/pair 和多项式位矩生成；并且原实例有实际 OPT=1 调度。

未包含：

- 把 z_l 改为带自有 payload 的内部孩子；
- 向 u 或其它机器添加新原 jobs；
- 递归 shared-head、growing-depth 或 merged-machine 接线；
- 由局部核自动推出 near-two actual gap；
- 一般 scheduling solver、SDP finder、source decoder、hardness 或主目标算法；
- 将有限 12 组 audit 或 root replay 当作任意 d,s 的程序证明。

新增孩子负载、R 回到原上游位置的负载、全局 q 的共同收费、跨背景 owner 或 faithful AND 的高阶矩都需另证。本合同不提供这些义务的支付。

# 8. 处置

处置为 integrated：cf33a00 Exact 原字节已保存到 evidence；正文明确记录实际 OPT=1 的完整 assignment law、共同 M3、global quadratic localizer、逐行 CONFIG first/pair、显式矩生成和所有版本边界；审计/root replay、affine owner、faithful AND、canonical/coercivity 与鲁棒七态对象均保持独立身份。

本页不创建第二份 global quadratic theorem，不把 finite audit 变成软件总证，不把局部构件升级为递归接线、一般近二 gap、一般 UM 算法或 hardness。

