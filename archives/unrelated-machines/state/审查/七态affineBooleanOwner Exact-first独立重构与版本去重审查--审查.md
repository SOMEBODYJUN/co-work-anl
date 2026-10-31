---
id: "unrelated-machines/seven-state-affine-owner-boundary-exact-first-review"
kind: review
type_tag: 审查
title: "七态 affine Boolean owner Exact-first 独立重构与版本去重审查"
status: integrated
truth_status: "exact-first-independent-reconstruction; author-proof-read-after-kept-separate"
review_level: "full-read-6887-byte-exact-first-record-cross-object-comparison"
scope: "UM-SEVEN-STATE-STAR-AFFINE-BOOLEAN-BOUNDARY-v1 Exact-first record, Exact/Proof/read-after versions, global audit and owner/AND boundaries"
summary: "02671c… 是在未读取作者 Proof 前，仅针对 01379ac Exact 的独立重构记录。它重新证明 Ω0 上实仿射 Boolean 六类分类、共同 M3 Gram-null 到真实支持的 Boolean 落地、同行互补 owner 至多二和跨背景高物理入度例。本文保存其独立时序与独有推导，和已入库 01379 Exact、88eb Proof、5c12 read-after、七态 global audit/AND localizer 去重；不把 Exact-first 变成一般不可能性或软件证明。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_seven_state_affine_boolean_owner_boundary_exact_first_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_seven_state_affine_boolean_owner_boundary_exact_first_review.md"
  - "related-source:01379acdbf1ccafd6d95:history/source/notes/unrelated_machines/sol_seven_state_affine_boolean_owner_boundary_exact_v1.md"
  - "related-source:88ebc1313d383dd51280:history/source/notes/unrelated_machines/sol_seven_state_affine_boolean_owner_boundary_author_proof_v1.md"
  - "related-source:5c12d08ec064dc869f6b:history/source/notes/unrelated_machines/sol_seven_state_affine_boolean_owner_boundary_author_read_after.md"
  - "related-source:ec117f60f81d65a9953b:evidence/runs/unrelated_machines/seven_state_star_global_quadratic_audit.json"
  - "related-source:177bb999d00126ea6ea9:evidence/runs/unrelated_machines/seven_state_star_global_quadratic_root_replay_scope.json"
related_objects:
  - "七态原星仿射Boolean所有者边界Exact与作者Proof版本审查--审查.md"
  - "七态原星仿射Boolean所有者边界作者证明审查--审查.md"
  - "七态星全局二次审计与root重放范围审查--审查.md"
  - "七态AND端点二次localizer作者read-after审查--审查.md"
  - "../计算/七态星全局二次审计与root重放边界--计算.md"
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/seven-state-affine-owner-boundary-exact-first-20261031/original/sol_seven_state_affine_boolean_owner_boundary_exact_first_review.md"
source_sha256: "d3201aba5c072a5a48accffd80347820eb6dead90cf22a30d3ff6799784787d0"
source_size: 6887
---

# 1. 独立 Exact-first 身份与阅读顺序

本轮完整读取 02671c9d2026c3262451 导出的 Exact-first 记录，6887 字节，SHA-256 为 d3201aba5c072a5a48accffd80347820eb6dead90cf22a30d3ff6799784787d0。记录明确：其唯一新原文是 01379acdbf1ccafd6d95 对应的 Exact，作者 Proof、策略稿和其它新分类记录当时均未读；此前只熟悉七态 global learning 背景，因此该记录是对新 affine Boolean、共同 M3 Gram-extension 和 owner scope 的独立重构，不是完全零背景 blind review。

记录结论是 PASS、未见 fatal；不认证新颖性、一般 UM 难度、算法或软件。当前清洗把它的独立时序和推导原字节保留为 provenance，并与已入库 Exact、author Proof、author read-after 和有限 audit 分层。

# 2. 对 Exact 支持与退化端点的先行核验

从 d,s 为正偶数、2<=s<=d/2 得到 d>=4、h=s/2 为整数、1<=h<=d/4，故 h<=d−1。p=(s/d)^3/1000>0，u0=4p(1−eta)>0，eta<=1/2 给 p<=1/8000，e=4/5−p−u0>0。于是 Omega0={0,1}×({0^d,1^d}并h-slice) 每点都有正质量；h=1 与 d=4,s=2 也在核验范围内。

这一步说明后续“非负平方真实期望为零则每个支持点为零”确有逐点正权前提。额外 C=0,d/2 slice 不需要参与 affine 分类。Exact-first 没有将 h>=2 的论证偷偷用于 h=1，也没有把 h=d/4 边界移出域。

# 3. 独立实仿射 Boolean 分类

对 f=a+bC+sum_i c_iY_i，先看 Y=0 的 C=0/1 点：a,a+b 属于 {0,1}，所以 b 属于 {-1,0,1}。若 b=1 或 -1，在每个允许 Y 上两种 C 值的 Boolean 差为 1，h-subset sums 必须恒定；交换坐标得到 c_i 全相等，再由 h>0 得 f=C 或 1−C。

剩下 b=0；用 1−f 将 a=1 化到 a=0，记 g=sum_i c_iY_i。全一向量给 D=sum_i c_i 属于 {0,1}。

h=1 时 singleton 直接给每个 c_i 属于 {0,1}，D 限制至多一个非零系数，得到 0 或 Y_i。h>=2 时，选择不含 i,j 的 h−1 个索引，再交换 i/j，得到 c_i−c_j 属于 {-1,0,1}。故系数同值，或只有两层 t,t+1。

同值时 ht、dt 都 Boolean，且 d/h>=4，只能 t=0。两层时令高层个数为 r。h-subset 中高层计数覆盖区间

[max(0,h−d+r), min(h,r)]。

其长度必须至多 1；若 2<=r<=d−2，因为 h,d−h,r,d−r 都至少 2，长度至少 2，矛盾。因此 r=1 或 d−1。r=1 给 g=Y_i；r=d−1 给 t=−1+1/h，但全一值 D=d/h−1>=3，矛盾。加回常数补得到 Exact 清单：

0、1、C、1−C、Y_i、1−Y_i。

该证明对全部实系数，不用符号、整数性或有理性，也不依赖额外 d/2 slice；d/h>=4 的边界不可删，域外 h=d/2 会出现 H/h−Y_i 这类额外 Boolean 非literal。

# 4. 共同 M3 Gram-null 的独立提升

固定 endpoint X 和 affine f，令 D=X−f。Exact 的共同 M3 PSD 使 D 为 Gram-null，因此 Lhat(D r)=0 对任意次数<=3 的 r。取 B=X+f−1，并令 r=D B²，得到 Lhat[(DB)²]=0。原 endpoint Boolean 矩等式给 Q=X²−X 的二范数 Lhat(Q²)=0。

恒等式 f²−f=Q−DB，Q 和 DB 都在 M3 Gram 中为 null，所以 Lhat[(f²−f)²]=0。该多项式只含 C,Y、次数<=4，由基础矩匹配等于真实 E_P[(f²−f)²]；Omega0 每点正质量，故 f 在真实支持上 Boolean，前一节分类适用。

这个推导明确只乘了总次数<=3 的测试多项式，没有暗加 M4，也没有将 Gram-null 误写成真实联合 assignment law。首矩和 pair 矩更低阶地转移：

Lhat X_e=E_P f_e，
Lhat(X_eX_e')=E_P(f_e f_e')。

允许两个 endpoint 相同或与基础变量重合，不影响这些等式。独立记录特别强调：只有一阶边际相同不足以推出 Boolean；共同 M3 正交和次数四 Boolean identities 才是关键。

# 5. 独立 owner 分类与 pair 支持

Ω0 的 primitive pair patterns 全正：C 与 Y_i 通过 C=0/1 及零/全一 Y，Y_i 与 Y_j 通过全零、全一和适当 h-subset 获得。于是两个非零清单函数的 product 期望为零，当且仅当它们是同一个 primitive bit t 属于 {C,Y_i} 的互补 literals t 与 1−t；常数一与任意非零函数乘积严格正。

同一物理 head w 上不同 unit jobs 的 endpoint 若同行 pair-zero，Gram 转移后变为真实 Boolean product 的零。故被 affine Gram 覆盖的正 owners 至多两个；两个必是同一 t 的互补 pair；第三个非零函数不可能同时不相交。若唯一正 owner 是常数一，其余端点一阶均为零。零一阶端点可很多，不能把正 owner 数写成原资格度。

若 CONFIG(B<2) 与共同矩一致，则 first/pair 合同本身强制不同 unit endpoints pair-zero；但结论始终只限制 A_w 覆盖的 endpoints。未纳入 affine Gram 的非仿射 endpoints 不受本重构约束。

# 6. 固定背景与跨背景高物理入度

独立记录保留 Exact §5 的条件量词：每个固定背景必须重新满足 Omega0 full support、共同矩、Gram 和 pair-zero。未条件化 M3 不能免费产生任意背景条件点；真实 law 若逐背景 affine Boolean，则可逐背景使用前述函数论证。

Exact §6 的 N-job 例逐项核对：新增 N 枚 J_alpha，各有 w 与 u_alpha 两个 unit 端点；均匀独立 beta 决定仅 J_beta 以 C 使用 w，其余 J_alpha 的 w endpoint 为零。固定 beta 时每个新增 endpoint 仿射于 C，w 只有一个可能正 owner；积分后 w 的每个 endpoint first 为 E_P C/N>0，不同 endpoint pair 始终为零。每个样本 w load=C<=1、u_alpha load<=1，全部 jobs 完整执行，且回 private home 的调度峰值为1。

因此该例只否定把 fiber owner<=2 相加成无条件原物理入度<=2；不构成 near-two gap、hardness 或一般 UM 反例。

# 7. 与已入库 Exact、Proof、read-after 和 audit 去重

与 01379 Exact 的关系：Exact 给 statement-only 参数、七类 law、Omega0、M3/owner/背景量词；本源给独立重构和先行验证顺序。它们共同属于同一个 affine owner boundary 对象，不创建第二份 Exact。

与 88eb 作者 Proof：Proof 后来逐步核对 h=1/h>=2 系数分类、h=d/4/h=d/2 边界、Gram-to-support、互补 literals、B<2 owner 和 N-job 例。Exact-first 在未读作者 Proof 时独立得出相同链条，因此保留独立来源角色；两源不能合并成外部盲审或新颖性认证。

与 5c12 author read-after：read-after 是 Proof 释放后的作者自检，确认与 Exact-first/Proof 的关系；本源的独有内容是作者 Proof 尚未读取时的独立证明顺序和 C1/C2/C3 细化。read-after 不覆盖 Exact-first 的独立性时序。

与七态 global audit/root replay：audit 只认证 12 组有限参数的 Fraction PSD/秩/assignment、3 组完整高维矩阵和 output byte identity；其 not_checked 明列 affine classification software、deep owner、AND extension、general scheduling、SDP finder。Exact-first 是解析重构，不是 audit 代码运行。

与 faithful AND localizer：AND read-after 研究忠实非线性 endpoint 在更高次数合同下的负 localizer；当前 Exact-first 只分类 affine endpoints，不能互换为同一障碍。与 canonical/coercivity/全局 global quadratic 对象一样，任何新增接线都要重新支付支持、矩、负载和全原 jobs。

# 8. 处置与未认证边界

处置为 integrated：Exact-first 原字节已复制到 evidence；独立函数分类、M3 Gram-null 提升、owner pair 支持和跨背景例的具体推导已写入本页，并与 01379 Exact、88eb Proof、5c12 read-after、global audit、AND localizer 去重。

未认证内容仍包括：所有非仿射端点的全局 owner degree、不受背景改变的共同 law、deep shared-owner/AND gluing、一般 scheduling/SDP finder、near-two gap、NP/UGC hardness、外部新颖性和主目标算法。该记录只保存 Exact-first 独立重构，不创建新一般不可能性结论。

