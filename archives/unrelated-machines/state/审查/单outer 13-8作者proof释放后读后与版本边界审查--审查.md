---
id: "unrelated-machines/one-outer-13-8-author-read-after-review"
kind: review
type_tag: 审查
title: "单 outer 13/8 作者证明释放后读后与版本边界审查"
status: integrated
truth_status: "author-read-after-consistent-with-exact-and-independent-reconstruction; no-new-general-UM"
review_level: "full-read-8613-byte-author-read-after-cross-archive-comparison"
scope: "sol_one_outer_13_8_author_read_after.md, one-outer Exact/Proof/independent sources, normalized-menu canonical review, finite backend boundary"
summary: "f608fde… 是作者在独立 Exact-first 之后写成的单 outer 13/8 read-after。本文完整读取该 8613 字节记录，核对其对 v2 Exact、author Proof、独立 128 网格算法、11 次 LP 二分/CDF rounding 算法和现有 finite backend 的版本区分。独有内容是作者证明释放后的逐式 margin、q 分支、全原任务回填和“未运行端到端代码”的审查边界；不建立第二个 13/8 定理，也不推广到一般 unrelated-machines。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_one_outer_13_8_author_read_after.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_one_outer_13_8_author_read_after.md"
  - "source:3858f37087ca3c8a80f0:history/source/notes/unrelated_machines/one_outer_normalized_flat_13_8_approximation_exact_v2.md"
  - "source:47c955a8da722b2e7a1c:history/source/notes/unrelated_machines/one_outer_normalized_flat_13_8_author_proof_v2.md"
  - "source:0f20dfac4647048db69c:history/source/notes/unrelated_machines/one_outer_full_primitive_sa1_rounding_exact_v1.md"
related_objects:
  - "单外层normalized-flat三源精读与13-8版本边界审查--审查.md"
  - "单层平方根配额与单外层选择器双源审查--审查.md"
  - "归一化门控菜单v2三源精读与13-8算法版本审查--审查.md"
  - "多outer双资源后端与tiny-home算法边界有限审查--审查.md"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/one-outer-author-read-after-20261031/original/sol_one_outer_13_8_author_read_after.md"
  - "archives/unrelated-machines/tools/evidence/one-outer-v1-v2-sources-20261031/source-manifest.json"
source_sha256: "2064056e2cbd657f45238b0249516558472a3567568074b4aedba3e5c3bf88d9"
source_size: 8613
---

# 1. 来源身份与阅读顺序

本轮完整读取 f608fde40f368d6acc68 导出的作者 read-after 记录，8613 字节，SHA-256 为 2064056e2cbd657f45238b0249516558472a3567568074b4aedba3e5c3bf88d9。源明确记录作者在 proof 释放前已经独立重构同一 Exact，冻结的 Exact 为 one_outer_normalized_flat_13_8_approximation_exact_v2.md，SHA-256 81b1c6e81d6472aeb55563a6916b8a9a0710cde6718a0c97f80939756a7fdc69；独立记录为 sol_one_outer_13_8_exact_first_reconstruction.md，SHA-256 399c6b29f54b1c0f49ee21e3ef64552edc1fec21fe09579a4dd91eecb5fe710f。

作者 read-after 又完整读取 one_outer_normalized_flat_13_8_author_proof_v2.md，SHA-256 2a6af63654c9ec36a3a83da47b4cdb95065aa298012369cf7c87dbfa5f226eaf，并重读 Exact。阅读顺序是：独立重构冻结，作者释放 Proof，随后作者本人读后核对；本页保留这种 read-after 身份，不倒写成 blind statement-first 或外部同行评审。

仓内已有三源审查页已完整记录 v1 supplied-point、v2 typed-Q Exact 和 author Proof 的原字节、量词与证据目录。本批独有的是 f608fde read-after 对两个算法实现选择、margin 算术、11 次二分安全分支、完整回填和未运行软件边界的再核对。

# 2. Exact 与 Proof 的共同 typed 合同

物理域只有一个 outer。每个 indexed state 有互异 private home；每个 home 有自己的 own-singleton helper；helper 其他 indexed states 是与 homes 不交的共享 B-resource normalized fallback 向量。保留所有 selector、listed incidences、zero incidences、重复 state 索引、unused resources 和未选 state payload。

Exact 的 Q-only 算法声称只接收显式 binary-rational typed Q，使用标准确定性有理 LP 作为内部工具，从 Q 生成完整普通 UM 矩阵 P(Q) 和全部原 jobs 的合法 assignment，满足

Cmax <= (13/8) OPT(P(Q))。

不输入 OPT、福利分配、primitive-SA1 可行点、联合 law、精度参数或调度 oracle；不负责从任意普通 UM 矩阵识别 typed 表示。该合同仅覆盖 single outer、互异 homes、own helper、显式 shared fallback，不能推广到多 outer、home 重合、无 own helper、隐式菜单或一般 UM。

Proof 与 read-after 共同使用完整矩阵值恒等式：

OPT(P(Q)) = 2 − V，1 <= OPT <= 2，

其中 V 是显式 typed 菜单上互不相交资源 bundles 的最大化最小福利。正向把选定 state 的获分配正 incidence 送 resource machines，其余 jobs 留 private；反向在 C<2 时每个 resource 至多容纳一个 unit incidence，从 selector 所在 state 读出互不相交 bundle。该等式计入全部原 jobs，不能以 relaxation 或删 payload 替代。

# 3. 作者 Proof v2 的结构核对

作者使用每次查询的 common primitive-SA1 有理 LP：binary state primitive A、incidence primitive Z、state partition、box、gate、resource capacity、perspective quality，并将每个原行乘同一 primitive 或其补，采用共同对称二阶数组和 binary diagonal。没有 PSD、额外 unit-FSLP、真实 joint law 或 actual allocation oracle。LP 变量为原 primitive 平方规模，行数显式多项式，标准有理 LP 可在总位多项式内求解。

若真实 V>=epsilon，达到阈值的 0/1 state/bundle allocation 给出 LP 可行点，因此 LP infeasible 只可推出 V<epsilon；Proof 不把 feasible 分数点误当 actual allocation。singleton own-state 的 gate/quality/box 行给出 mu_A=mu_Z=Y_AZ；对 fallback incidence 用同一 conditioned row 得 alpha、zeta、f、b packing：

- sum_j w_j b_j >= epsilon；
- f_j >= b_j；
- sum_u p_jsu zeta_jsu >= epsilon alpha_js；
- sum_{j,s} zeta_jsu <= 1。

alpha=0 时 gate 强制 zeta=0，避免 0/0；zero incidence 若有正 LP claim，丢弃只会减少资源需求，不改变质量。

条件化选一个正边际 fallback state 后，每个 helper 独立选择 state/empty，所选 state 的每个正 incidence 以 zeta/alpha 请求 resource。每个 resource 只在实际请求者中按 weighted score 排序，未请求但 state 已选者不参与 winner。阈值 score level d 的 helper 请求概率总和 r<=1，跨 helper 独立性给

1 − product_j(1−beta_j(d)) >= 1 − exp(−r) >= (1−1/e)r > (5/8)r。

按有限有理 score levels 积分得到 W>(5/8)epsilon²。作者 read-after 明确同一 helper 的不同 state 是互斥的，alpha=0 state 不列入候选；不同资源请求可以相关，因为 welfare 只需逐资源期望求和。

# 4. 作者新增的 13/8 margin 和 11 次二分核对

Proof 固定仿射质量线参数

a=13/8，b=10/8，d=1/256，q0=a epsilon−b，q=q0+d。

作者 read-after 逐式检查

(5/8)epsilon² − (2q0−q0²)
= (209epsilon²−468epsilon+260)/64。

在 epsilon∈[0,1] 上该分子导数 418epsilon−468<=−50，故最小值在 epsilon=1，基础余量至少 1/64。若 q>0，则 q0>−d，q<97/256，平移增加量小于 2d+d²=513/65536；相对 1/64=1024/65536 仍留 511/65536 严格余量。若 Good helper 的 home mass z 不超过 q，则 W<=z+q(1−z)<=2q−q²，和严格 welfare 矛盾，因此 z>q，完整恢复达到 C<=2−q。

Unknown V 不用 objective oracle。算法从 l=0,h=1 开始，固定做 11 次 rational LP，midpoint 可行时抬高 l 并保存可行点，不可行时降低 h。唯一保持的不变量是 V<=h；可行 l 可以超过 V，不影响安全性。11 次后 h−l=1/2048。

若最终 q<=0，则由 V<=h、二分误差、d−a eta=51/16384>0 得 V<10/13，全部 incidence 留 private 的 baseline C<=2 严格满足 C<(13/8)(2−V)。若 q>0，最后的 l 必来自某次可行查询，保存点有效；q>=aV−b+d−a eta，故 C<=2−q<(13/8)OPT。作者 read-after 特别指出不能把 feasible l 误当 V 的下界或把 LP fail/feasible 两方向混淆。

# 5. 两种算法实现的版本差异

独立 Exact-first 重构使用固定 128 点网格、枚举实际 fallback welfare 阈值，并以有限 AM-GM/CDF backend 给出 5/8 结构性余量；作者 Proof 使用 11 次 adaptive rational LP threshold、固定仿射质量线和 CDF 的严格 1−1/e>5/8 下界。两者都对同一 typed Q-only Exact 合同给出 13/8，但算法身份和软件接口不同。

因此不能把独立算法的 128 点网格、实际 Q_j 阈值枚举或有限 backend 复写成作者 11 次二分实现；也不能把作者 Proof 的存在性/有理 LP 论证写成独立代码已经运行。既有 32 个小型 Fraction CDF 检查只核独立 backend 的有限实例，不覆盖作者整套算法。

# 6. 完整 jobs 回填和真实实现边界

选定每个 helper 的 state 及不交 bundle 后，只有选定 state 的获分配正 incidence jobs 被送到 exact resource；selector 放选定 state-private machine；其余原 incidence jobs、未选 state、zero incidence、duplicate indexed states 和 unused resource payload 全部留在原 private endpoint。private load 是选定行的 2−value，其余行 load 1；resource load 至多 1；每个原 job 恰好分配一次。

作者 read-after 明确本轮只做数学重读，没有执行作者 11 次 LP 算法或完整 P(Q) 构造程序。标准有理 LP 是证明中的显式 backend 合同，不是已经运行的 repo implementation。既有有限 audits 也不认证 LP 生成、11 次搜索、CDF 去随机化、全部原 jobs 输出或所有输入的位复杂度实现。

# 7. 与仓内对象的去重及开放边界

与单外层 normalized-flat 三源审查重复的主结论是：v1 supplied-point 的 epsilon²/4 版本、v2 Q-only 的 13/8 Exact、author Proof 的 OPT=2−V/CDF/二分/回填链共同属于同一个 typed one-outer 对象。本页不再建立第二份 13/8 定理。

与多 outer tiny-home 19/10 backend 资料的关系仅是同一类 normalized-flat/own-home/resource-winner 语义的相邻有限后端；多 outer v1 的 k^4 tiny-home、MW、整块方差和 two-resource CE 不可迁移为单 outer 13/8 的证明，也不反向证明多 outer。与 gated-menu 13/8 对象虽有相同数值，但其 P_gate、group/allocation 量词和版本身份不同，不能合并。

本对象仍未覆盖多 outer、多个 state 的单 group、重合 homes、无 own helper、隐式 exponential menu、任意 ordinary UM、端到端生产软件、外部同行审阅、新颖性或 UM-TARGET-v1。作者和独立记录都把一般目标保持 OPEN。

# 8. 处置

处置为 integrated：f608fde 原字节已复制到 evidence；作者 read-after 的 Exact/Proof 版本时序、11 次二分 margin、q<=0/q>0 安全分支、完整 jobs 回填和未运行软件边界已归档。正式数学对象继续由现有单外层 normalized-flat 三源审查承载，本页只保留该 read-after 的独有 provenance 与实现边界，不制造新算法、一般近似结论或新颖性声明。

