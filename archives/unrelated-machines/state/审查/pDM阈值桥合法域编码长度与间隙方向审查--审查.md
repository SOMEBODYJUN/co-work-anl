---
id: "unrelated-machines/pdm-threshold-domain-gap-review"
kind: review
type_tag: 审查
title: "pDM 阈值桥合法域、编码长度与间隙方向审查"
status: integrated
truth_status: "conditional-threshold-iff-confirmed; domain-and-gap-caveats-retained"
review_level: "full-read-3149-byte-review-cross-archive-pdm-comparison"
scope: "UM-PDM-THRESHOLD-EXACT-v1 domain conditions, gcd/workload iff, encoding length, finite low-load NO escape and slot-rounding boundary"
summary: "36670bbc… 是 pDM threshold bridge 的完整领域与 gap 方向审查。本文完整读取 3149 字节记录，核对 d>=3、m>=n、无孤立顶点、n=m=0 域缺口、固定 b/d 编码、总工作量整除 iff、无完美匹配只给 OPT>=bd+1、d=3,n=2,m=3,b=4 的 OPT/T=13/12 逃逸、assignment-LP 槽舍入和不得升级近二的边界；与部分 MinRep/费用桥/有限反例对象去重。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/reviews/unrelated_machines/pdm_threshold_domain_and_gap_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/pdm_threshold_domain_and_gap_review.md"
  - "related-source:4edaa33bd4a272da6a6a:research/current/unrelated_machines/pdm_threshold_scheduling_bridge.md"
  - "related-source:2ff9d538ae90f44b6e38:evidence/runs/unrelated_machines/pdm_escape_counterexample_audit.json"
related_objects:
  - "部分MinRep费用桥与pDM阈值双源审查--审查.md"
  - "pDM阈值桥低负载NO逃逸的有限反例--计算.md"
  - "../定理/多状态图估值支持域计算障碍--定理.md"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/pdm-threshold-domain-gap-20261031/original/pdm_threshold_domain_and_gap_review.md"
source_sha256: "995c65683b4308781af5b35180c6d0a1180a55c38c09de35bbad38185c7a326c"
source_size: 3149
---

# 1. 读取范围与条件性状态

本轮完整读取 36670bbccbf74359c7a5 的 review 源，3149 字节，SHA-256 为 995c65683b4308781af5b35180c6d0a1180a55c38c09de35bbad38185c7a326c。该记录核查现行 pDM threshold bridge 的完整归约合同，不否定总工作量和整除算术内核，也不认证其引用的新论文。

审查结论是条件性通过：在明确的非退化域和固定参数编码下，阈值 iff 构造成立；原 v1 对 m<n、孤立顶点、n=m=0 和可变二进制 b 的域/位复杂度表述不完整，不能默认为全部输入已闭合。该记录被现有部分 MinRep/费用桥对象引用，但本页保留其独立的域修补和 gap 方向纠错。

# 2. 精确阈值 iff 的合法域

固定 d>=3。源有 d 个两两不相交、各大小 n 的顶点集和 m 条 d-超边，每条超边对应一台机器。每个顶点 v 生成任务 g_v，只能在包含 v 的超边机器上处理时间 b；每台机器再有 b(m−n) 个 dummy jobs，每个 dummy 在该机处理时间 d。取整数 b>d 且 gcd(b,d)=1。

在 m>=n、每个源顶点至少出现在一条超边中、n>=1 的非退化域内，任务资格合法，dummy 数非负，且总工作量为

dn b + b(m−n)d = bdm。

若存在完美 d-dimensional matching，匹配的 n 台机器各放 d 个 vertex jobs，未选机器放 b 个 dummy，峰值为 bd。反向若完整调度峰值不超过 bd，总工作量等于 m·bd，故每台机器恰负载 bd。若一台机器收到 k 个 vertex jobs、ell 个 dummy，则

bk + d ell = bd。

互素性给出 d 整除 k；资格又有 0<=k<=d，所以 k 只能是 0 或 d。恰 n 台机器承载 d 个 vertex jobs，组成完美匹配。因此在该合法域内：

OPT <= bd 当且仅当存在完美 d-dimensional matching。

无完美匹配只能推出 OPT>=bd+1，因为处理时间和阈值是整数；这不是对 NO 值的上界。

# 3. 原 v1 域中需要显式修补的点

若 m<n，则 b(m−n) 为负数，dummy job 定义不是合法 UM 输入。若有孤立源顶点，其 vertex job 没有任何有限端。若 n=m=0，则机器/任务与完备性边界不按主公式定义。当前正文不能靠默认语义把这些情况当作合法。

可选择两种修补：

1. 在归约对象开头显式分支：对非法域输入输出固定 NO 或空 YES；
2. 将源域限定到仍保持 NP-hard 的非退化子类，并在对象中写出 m>=n>=1、无孤立顶点等条件。

修补必须成为 v2 或明确版本合同，不能保持 v1 原文字面而暗中依赖这些条件。

# 4. 固定参数与位复杂度

当 d、b 都是固定参数，例如选 b=d+1 时，dummy 数 b(m−n) 与显式输入规模线性，矩阵规模和任务输出总位长度多项式。若 b 作为二进制可变输入，显式复制 b(m−n) 个 dummy jobs 的输出可能指数于 log b，不能继续声称对这种编码的总位多项式归约。

因此“固定 d、b”必须按两者都固定解释，或改为不显式复制 dummy 的新编码并重新证明。参数数值不应被混入循环界；真正决定位复杂度的是显式任务输出长度。

# 5. 加一 NO 下界不是乘性 gap

无完美匹配只给 OPT>=bd+1，不能推出 OPT<=bd+1，也不能推出所有 NO 实例的比值趋近 2。整数性只提供阈值之外至少一个单位；更大的 NO 值没有被排除。原文中“总工作量守恒把 NO gap 限制为加一”若按乘性/上界理解并无证明支持。

现有有限精确反例取 d=3,n=2,m=3,b=4，三条超边两两相交且无完美匹配。阈值 T=bd=12；对全部有限分配 Fraction 穷举得到 OPT=13、代表负载 (12,11,13)，因此 OPT/T=13/12。它保留阈值 iff 和 OPT>=T+1，但否定“无匹配自动得到近二 NO”的朴素桥。该记录 scope 仅是有限观察，不是一般 NO 上界、gap theorem 或 UM-TARGET hardness。

# 6. 现有槽舍入边界

对合法展开后的该编译形状，最大有限 processing time 为 b=T/d。先解截断 assignment LP(T)：不可行时可靠推出 OPT>T；可行时已有 UM-ST-ROUND-v1 有序槽舍入给出

Cmax <= T + max p_ij = T+b = (1+1/d)T <= 4T/3（d>=3）。

这是已有槽定理对该矩阵形状的直接适用，不是本源新算法。它说明如果某近二归约完全保持此编译形状，则在 P≠NP 下不能以任意 rho>1+1/d 的 promise gap 使用该原样编译：LP 可行将给出反驳 NO 的低调度。它不排除加入真正改变矩阵结构的 gap amplification。

相关二值 max-min literature 只传递至多 1+1/(pq) 级阈值，最小允许 pq 已给 13/12，随 pq 增大趋近 1；它不能替代统一 2−epsilon 反面，也不提供乘性放大。

# 7. 与部分 MinRep、费用桥和其它对象去重

部分 MinRep review 中的 seed certificate、条件费用桥、degree/girth source soundness 与本 pDM iff 是不同层级：前者需要未来真实 UM compiler 和 all-output decoder，后者只锁定整数阈值。它们不能合并为一般近二 hardness。

与 pDM 有限逃逸计算对象的关系是：有限实例支持本页的“加一而非近二”修正，但不改变 iff 核心。与多状态图估值 coNP 对象的关系是：后者讨论 support membership 的复杂度，未提供 pDM 调度矩阵 gap。三者均不迁移到 CAG 或共同目录 SPE。

# 8. 处置与开放义务

处置为 integrated：原 review 已复制到 evidence；正文保存 pDM threshold iff 的合法域、gcd/总工作量证明、m<n/孤立/n=m=0 修补、固定 b/d 位复杂度、13/12 逃逸和槽舍入边界。不创建新的 pDM theorem，也不把无匹配加一阈值写成乘性 gap。

开放义务是：选择并冻结合法非退化源域；在二进制可变 b 时避免输出规模爆炸；设计真正的 multiplicative gap amplification，阻止分数/部分分配逃逸；将其与一般 UM 编译器、source decoder 和近二硬度分开认证。一般 UM-TARGET-v1 仍 OPEN。

