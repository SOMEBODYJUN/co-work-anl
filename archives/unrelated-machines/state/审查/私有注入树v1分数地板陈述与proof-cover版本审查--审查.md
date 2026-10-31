---
id: "unrelated-machines/private-injective-tree-v1-fractional-floor-review"
kind: review
type_tag: 审查
title: "私有注入树 v1 分数地板陈述与 proof/cover 版本审查"
status: integrated-v1-provenance
truth_status: "v1-exact-proof-independent-cover-consistent; no-new-general-algorithm-or-novelty"
review_level: "full-read-2626-byte-exact-plus-three-related-v1-sources"
scope: "private injective tree v1 exact, frozen proof, independent literal/cover, and v2 theorem/read-after comparison"
summary: "本页保存 UM-Q-PRIVATE-INJECTIVE-TREE-FRACTIONAL-FLOOR-v1 的 exact、proof、independent literal/cover 四源 provenance 与版本对照。四源只支持完全私有满 d 叉树、单状态叶外机单射、同一共同 lambda 证书下的实际存在性；不提供一般不相关机算法或新颖性认证。v2 正式定理已扩展到 CONFIG(T)、非单射 promise 过滤与有界重数对象；v1 本页不另建第二个五三定理。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/private_injective_tree_floor_v1_exact_source.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/private_injective_tree_floor_v1_exact_source.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/private_injective_tree_floor_v1_proof_source.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/private_injective_tree_floor_v1_proof_source.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/private_injective_tree_floor_v1_independent_cover_source.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/private_injective_tree_floor_v1_independent_cover_source.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/private_injective_tree_floor_v1_independent_literal_source.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/private_injective_tree_floor_v1_independent_literal_source.md"
related_objects:
  - "../定理/私有注入树配置五三界与非注入承诺判定--定理.md"
  - "../审查/私有注入树v2作者证明读后与范围续审--审查.md"
  - "../定理/私有菜单树有界叶重数配置界--定理.md"
  - "../定理/单强制根树精确配置间隙--定理.md"
  - "../资料/Annamalai双部超图完美匹配算法--资料.md"
  - "../资源/Santa-Claus超图匹配与配置LP五分之一界--资源.md"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/private-injective-tree-v1-floor-20261031/original/private_injective_tree_floor_v1_exact_source.md"
  - "archives/unrelated-machines/tools/evidence/private-injective-tree-v1-floor-20261031/original/private_injective_tree_floor_v1_proof_source.md"
  - "archives/unrelated-machines/tools/evidence/private-injective-tree-v1-floor-20261031/original/private_injective_tree_floor_v1_independent_cover_source.md"
  - "archives/unrelated-machines/tools/evidence/private-injective-tree-v1-floor-20261031/original/private_injective_tree_floor_v1_independent_literal_source.md"
source_sha256: "aa3ed3a09e04d291b1266468af5814ffd8bd649cac4746514f60a79e791ecf54"
source_size: 2626
---

# 1. 读取范围、来源身份与原字节

本轮实际完整读取导出的 exact 源 private_injective_tree_floor_v1_exact_source.md，2626 字节，SHA-256 为 aa3ed3a09e04d291b1266468af5814ffd8bd649cac4746514f60a79e791ecf54。该源候选身份是 UM-Q-PRIVATE-INJECTIVE-TREE-FRACTIONAL-FLOOR-v1，原文明确标记为“仅陈述”、未登记 canonical claim、未认证新颖性。工作区导出副本与 evidence 副本逐字相同。

同对象的三个历史版本源也逐字读取并复制到本页 evidence：

| 源 | ID | 字节数 | SHA-256 | 作用 |
|---|---|---:|---|---|
| v1 exact | 4b9189efa90c412a130c | 2626 | aa3ed3a09e04d291b1266468af5814ffd8bd649cac4746514f60a79e791ecf54 | 先行候选陈述 |
| v1 frozen proof | 14053ecec125b3cc7064 | 6107 | f4900b3693d6242cd08f218cbc478bb1e40ee6f072fb3205a5619b21fd1f40c5 | blocker、共同 lambda 加权、Haxell 和回填证明 |
| v1 independent cover | 30438cfbab031b78ea57 | 7522 | 96e2fd6d3a98093c3aa923457d23fc5ebdfad570656f3762ced2fb2e977f46c7 | 先读 exact 后的独立陈述核查 |
| v1 independent literal | abbfd208a064a1ba7509 | 8152 | 9f60a21914a49efab98beacfedd93494dd98ddbd2478afee7ff8453f20432a4b | Exact-first 独立重构与外部定理边界 |

proof、cover 与 literal 的 source 字节不是把 v2 读后记录倒写成 v1；四个 v1 文件各有独立 hash 和作用域。v2 读后页另有 proof/read-after 历史记录，本页只把它作为版本比较依据，不冒称本轮新的外部审查。

# 2. v1 exact 的数学对象和精确量词

参数是整数 d,h≥1。root 集合 U 有限且非空，每个 root u 的状态菜单 S_u 有限且非空。每个状态 (u,s) 是完全私有的满 d 叉高度 h 树：深度 0,…,h−1 是内部机器，深度 h 是叶 port jobs；不同状态之间的内部机器也互不相同。所有树共享有限外部机器集合 Z。

完整普通 unrelated-machines 实例 P 只有：每个 root 一枚 unit selector，仅能在各状态树根处理；每个内部 edge job 在父端耗时 1/d、子端耗时 1；每个叶 job 在父端耗时 1/d，并有唯一外部端耗时 1，由显式 f_us:[d]^h→Z 指定。没有其它有限端、job 或预载，f_us 不要求来自 Latin 编译或保色。

前提一：每个完整状态内 f_us 单射；同一状态的 d^h 个原叶对应 d^h 个不同外机。跨状态、跨 root 共享外机允许。

前提二：有一套对每个 root 共同使用的非负有理 lambda_us，满足
Σ_s lambda_us=1（每个 u），以及
Σ_{u,s} lambda_us |f_us^{-1}(z)|≤1（每个 z）。
同一 lambda 同时用于所有外机，不能对不同 z、hitting set 或 root 子集另选分数。

对任意 1≤r≤d，若 (d−r+1)^h≥2r^h−1，则每个 root 都能选一个真实 state 和一个满 r 叉高 h 子树，使选中叶的真实外机全局互异；完整实际调度的 Cmax≤2−r/d。取 r=floor((d+2)/3)=ceil(d/3) 时条件对所有 d,h 成立，从而 Cmax≤5/3。

未选 state、未选分枝和零权 state 的原 jobs 仍必须全父置；结论不是仅匹配叶资源。v1 只给存在性，不把枚举全部 r 子树或有限 Haxell 搜索称为一般参数的确定性总位多项式算法。共享内部机器、非均匀时间、非单射状态、额外 jobs/preloads 均在范围外。

# 3. v1 proof 的逐步核对

## 3.1 精确树 blocker

在满 d 叉高 h 树中，所有满 r 叉高 h rooted pruned subtrees 的叶集，其最小共同 hitting 原叶数为
b_h=(d−r+1)^h。
高度 1 需阻断 d−r+1 个孩子；一般高度至少使 d−r+1 个根孩子各自被阻断，孩子叶域互不相交；反向选择这些孩子并递归放置最小 blocker 达到等号。高度零仅作基例。

单状态内单射把上述原叶数转换成不同外机数。非单射时一个资源可一次命中多枚叶，b_h 不能直接作为资源 blocker 下界；v1 proof 明确将此列为不可迁移边界。

## 3.2 共同 lambda 的资源 hitting 下界

构造二部有限超图：左侧 roots U，右侧资源 Z。每个真实 state 和其中每棵满 r 叉子树生成边，边包含一个 root 和 R=r^h 个不同外机，故总边大小 R+1。重复资源边可去重但须保留真实 state/subtree 见证，root 顶点不可冒充资源 hitting vertex。

对任意非空 I⊆U，令 X⊆Z 命中全部 incident edges。每个 state 都被 X 命中所有 r 子树，故 |f_us^{-1}(X)|≥b_h。用同一共同 lambda 求和：
b_h|I| ≤ Σ_{u∈I,s}lambda_us|f_us^{-1}(X)|
= Σ_{z∈X}Σ_{u∈I,s}lambda_us|f_us^{-1}(z)|
≤ |X|。
最后一步仅用外机容量行，不能针对不同 X、z 或 I 重选 lambda。因此 resource transversal number tau_I≥b_h|I|。

## 3.3 Haxell 参数和匹配

按总边大小 K=R+1 计算，资源侧阈值为 2K−3=2R−1。v1 假设给出
tau_I≥b_h|I|≥(2R−1)|I|>(2R−1)(|I|−1)。
proof、cover、literal 按已读取的 Annamalai 对 Haxell 条件的准确复述使用；三源没有声称重构 Haxell 1995 原文证明全文。有限性、每边一个 root、资源侧 distinct vertices、全部非空 root 子集和严格大于号均已核对。匹配给每个 root 一个真实 state/subtree 见证，选中叶的真实外机全局不交。

不能把边总大小误写成 r 或 r^h：分叉数是 r，子树叶数是 R=r^h，uniform rank 是 R+1。

## 3.4 全部原任务回填

匹配后，selector 放在选中 state 根；选中 r 子树内部向下发送相应 edge jobs 和叶 jobs，其余原 edge/leaf jobs 全部留在父端：

* 活跃内部机器收到一个 unit incoming，并把恰 r 个 outgoing 向下、其余 d−r 个 small 留父，负载 1+(d−r)/d=2−r/d；
* 未活跃内部机器无 unit incoming，d 个 outgoing small 全父置，负载 1；
* 未选 state 的全部原 jobs 全父置，负载 1；
* 每台外机最多收到一枚匹配选中的 unit leaf job，负载不超过 1。

selected subtree 前缀闭合，不会出现后代活跃而父级不活跃。所有原 jobs 恰分配一次，只用原有限端；辅助超边不产生新机器或新任务。

## 3.5 默认五三和退化边界

令 r=floor((d+2)/3)。有 d−r+1≥2r−1，且 (2r−1)^h≥2r^h−1；又 r/d≥1/3，所以 Cmax≤5/3。三源核对 d=1 时退化为 Hall、h=1 的 blocker、r=1 的路径情形、lambda=0 状态仍需回填原 jobs，以及外机不足时共同 lambda 假设本身不成立。空 root 集不是 v1 的非空实质域。

# 4. proof、cover、literal 的关系和独有增量

frozen proof 是作者链条：精确 blocker、共同 lambda 加权的资源 transversal 下界、Haxell、完整 d-tree 回填。

independent literal 是 Exact-first 重构，重点核验对象量词、边 rank R+1、默认 r 算术、所有原 jobs 和无算法/无新颖性边界。

independent cover 是先读 exact 后的独立一致性核查，重点指出不允许逐资源更换 lambda，且 Haxell 常数应按 R+1 换算为 2R−1。

三份源没有引入彼此冲突的模型。共同的可用结论是：完全私有、每状态叶单射、同一共同 full-state 分数证书这一窄结构可以封闭任意外机重编号下的实际 5/3 存在性。三份源没有把此合同升级为一般 unrelated-machines 近二算法、非单射 configuration gap、生产代码或 NP-hardness 结论；“未发现 fatal objection”是有限审查结论，不是外部新颖性证明。

# 5. 与 v2 正式对象的版本对照

现有 私有注入树配置五三界与非注入承诺判定 是正式 v2 数学对象；本页不建立第二个定理：

| 版本 | 保留的模型与结论 | 相对增量或限制 |
|---|---|---|
| v1 fractional-floor | 共同 lambda、每状态叶单射和 T=1 式完整叶证书下，任意 r 条件的实际存在性，默认 5/3。 | 候选 exact-only；没有 CONFIG(T) 的 s,a 边际、非单射过滤 promise 或算法输出承诺。 |
| v1 proof/cover/literal | 同一 blocker/Haxell 链，核对 rank、共同 lambda 和全任务回填。 | 仍是窄合同的存在性证据，未改变量词或模型。 |
| v2 exact/proof/read-after | 将 CONFIG(T) 的边际转成 a=d−floor(d(T−1)) 叉树分布，再用 (a−r+1)^h≥2r^h−1；并给非单射状态过滤后的严格 1,5/3 promise 判定。 | v2 的 proof、独立 cover/literal/shared 和 read-after 已由正式定理与 v2 审查页承载；v1 不应被回写成 v2 新 exact。 |
| bounded multiplicity v3 | 每状态资源重数至多 mu 时另行给 2−1/(mu+2) 型结构界。 | 不是 v1 单射假设的自动推论，不能用 v1 的 b_h 资源计数替代重数计数。 |

v1 是 T=1、s=0、a=d 的窄存在性合同；v2 在更宽 CONFIG(T) 域中重新证明边际系统、共同 b-tree 分布、阻断数和回填，并新增 non-injective promise 过滤。v3 再扩大到叶重数但保留不同计数前提。不能因数值同为 5/3 就互相替代。

# 6. 重复、修正、可用结论与未认证边界

与现有 v2 定理和 read-after 页重复的数学主链是：树 blocker 精确数；单状态注入把叶数变成不同资源数；同一共同 lambda 给 root 子集资源 hitting 下界；Haxell 以总 rank r^h+1 产生互斥资源边；完整原 d-tree 回填给出 2−r/d。重复应归到一个 v2 主定理的历史 provenance，不产生第二份五三 theorem。

本批保留的可引用字段：

* UM-Q-PRIVATE-INJECTIVE-TREE-FRACTIONAL-FLOOR-v1 是 candidate identity，不是 canonical claim；
* lambda 是每个 root 菜单的一套共同分数，资源容量按完整状态叶重数计；
* Haxell 总 rank 是 r^h+1，严格阈值是 2r^h−1；
* 单射只需在每个完整状态内部成立，跨状态和跨 root 资源可共享；
* 匹配只选每个 root 的一个真实 state 和一个真实子树，不能沿路径换 state；
* 未选状态/分枝原 jobs 仍存在并全父置；
* proof 给存在性，不默认全参数 deterministic bit-polynomial schedule；
* 外部 Haxell 依赖只按已读准确复述使用，未宣称亲读 Haxell 1995 原证明全文。

v1 不回答：变参数 d,h 下如何总位多项式输出 sigma；非单射状态是否有同样 CONFIG gap；共享内部机器、额外端点、非均匀时间或预载是否仍可用；typed balanced Latin 是否确实提供同一共同 lambda；窄结构全球新颖性；以及 UM-TARGET-v1 的一般正反问题。有限子树穷举或 Haxell 存在性不能填这些缺口。

# 7. 处置

处置为 integrated-v1-provenance：四份 v1 原字节已保存到 evidence；v1 exact 的对象、proof/cover/literal 一致链条、重复项、修正字段和未认证边界已写入本页；正式结论继续引用现有 v2 定理与 v2 read-after 审查。后续可以从本页链接 v1 的共同 lambda、注入、阻断数合同，但不得把它写成一般 unrelated-machines 五三算法、非单射间隙定理、生产实现或新颖性证明。

