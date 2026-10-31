---
id: "unrelated-machines/seven-state-star-canonical-v2-actual-read-increment"
kind: "review"
type_tag: "审查"
title: "七态原星 canonical-v2 最终全文实读与范围增量"
status: "integrated-scope-increment-recommended"
truth_status: "full-read-version-audit-with-scoped-mathematical-checks"
review_level: "independent-full-source-read-cross-object-comparison"
summary: "独立完整读取 4c90a874963e76591945 的最终全文及其导出 canonical-v2 正文；核实 218a5c4e 最终字节、三处相对旧版的纠正、四个分层 Claim 的量词/证明承重与证据等级。提出将本票作为现有七态定理、稀疏支撑、affine owner、AND obstruction 及最终审查对象的来源增量，而不改写共享正式正文。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_identity_coupling_seven_state_star_canonical_v2_final_actual_read.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_identity_coupling_seven_state_star_canonical_v2_final_actual_read.md"
  - "source:4c3957d3e5517fdc7ae5:research/current/unrelated_machines/seven_state_star_global_quadratic_and_extension_boundaries.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/unrelated_machines/seven_state_star_global_quadratic_and_extension_boundaries.md"
related_objects:
  - "unrelated-machines/seven-state-star-global-quadratic-local"
  - "unrelated-machines/uniform-cardinality-first-pair-sparse-support"
  - "unrelated-machines/seven-state-affine-owner-boundary"
  - "unrelated-machines/seven-state-and-gate-localizer-obstruction"
  - "unrelated-machines/seven-state-global-quadratic-extension-boundary-20261031"
---

# 来源身份、目标与实际读取

本票清洗的源 ID 是 `4c90a874963e76591945`，元数据给出的原路径为
`history/source/notes/unrelated_machines/sol_identity_coupling_seven_state_star_canonical_v2_final_actual_read.md`，
源 SHA-256 为
`958aa33f7dcc653d4b38213258eb8346cf3809a75752d3ab22be7f22046fab3f`，
大小 9,940 bytes。源记录明确引用七态原星最终规范正文的两个冻结提交：

* `68fad804ec5946cb296f77dc5b336308a66abf12`（legacy-cleanup）；
* `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`（main）。

root 另在本轮导出了最终规范全文到
`cleanup/workspaces/Boss5/resume-20261031-current/seven-state-canonical-final.md`；该导出实际核得 180 行、18,177 bytes、SHA-256
`218a5c4e5b346c8c4816b609a98073958186cb222390839b54229aa5c4beecb6`。
本票从第 1 行至第 180 行完整读取该文件，随后完整读取 4c90 源的 92 行实际阅读记录；没有只凭摘要或旧入口作处置。本文写入的独立清洗目录是
`cleanup/workspaces/Boss5/resume-20261031-current/star_canonical/`，不改共享正文、CLAIMS、Git 或认领状态。

本票的证据身份是“清洗人员对最终稿的全文复核与版本边界核验”。4c90 源自身不是七态数学证明，而是阅读次序、版本和独立性说明；最终正文的数学结论仍须引用其两个原始冻结提交及现有正式对象。本票不把未打开的原作者证明、审计代码或 root 运行再签成自己的程序执行。

# 最终稿与旧稿的字节边界

最终稿与旧稿的版本边界可以复现，而不是只记一串 hash：

1. 旧稿实际 hash 为
   `1c2053ae9bc95b7fb575fd22176dc8db4cb4f25035d5f8f41c6fe2cf5884a30b`，
   同为 180 行；
2. 最终稿 hash 为
   `218a5c4e5b346c8c4816b609a98073958186cb222390839b54229aa5c4beecb6`，
   同为 180 行、18,177 bytes；
3. 将最终稿精确反向恢复以下三处即可得到旧稿 hash，且没有其他字节差异：
   * 第 13 行在边界 Claim 的 Gram 条件中把 `Lhat[(X−f)²]=0` 恢复为旧式 `Lhat(X−f)²=0`；
   * 第 106 行 Cauchy 末端把 `<= (eta/40) sum_(five classes) q_class^2.` 恢复为旧式严格 `<`；
   * 第 154 行共同矩版本把 `Lhat[(X−f)²]=0` 恢复为旧式缺少等号的 `Lhat(X−f)²0`。

第一和第三项是把平方明确置于线性泛函内部，消除歧义。第二项是实质的边界修正：由常数比较得到的严格系数只在右端五项平方和非零时给严格不等式；当所有右端值（特别是 (q=0)）为零，能够安全写出的总链是 ≤，不是 <。这一改动不改变局部化结论，但旧正文不应继续被引用为最终 hash。

# 主 Claim：完整对象、证明承重与边界

最终稿的主对象是 `UM-SEVEN-STATE-STAR-GLOBAL-QUADRATIC-LOCAL-v2`。参数和量词必须整体保留：

* (d,s) 是正偶数，(2≤ s≤ d/2)；(eta=s/d, h=s/2, T=1+eta)。
* 机器为 (u,v,z_1,…,z_d)，原 jobs 是不可拆的 (R,j_1,…,j_d)。有限端点恰为 (R) 在 (u,v) 各用 1，(j_l) 在 (v) 用 (1/d) 或私有 (z_l) 用 1；其余时间无穷，所有原 jobs 必须完整分配。
* (C=1) 表示 (R) 在 (v)，(Y_l=1) 表示 (j_l) 在 (v)，(H=sum_l Y_l)。类别内对固定 (H) 的 home 集均匀取样。七类质量为
  [
  p=eta^3/1000,, u_0=4p(1-eta),, e=4/5-p-u_0
  ]
  以及
  ((C,H)=(1,d),(1,0),(1,h),(0,0),(0,h),(0,d/2),(0,d))
  的质量 (p,1/20,1/20,1/20,1/20,u_0,e)。
* (P) 是一个真实完整 assignment law；其 load 为
  (1-C, C+H/d, 1-Y_l)。把 (R) 放 (u)、所有 payload 留 (v) 给出实际 (OPT=1)。唯一超过 (T) 的原样本类别是 (C=1,H=d)，负载为 2，质量 (p) 与 (d) 无关。
* 同一个 (L=E_P) 的次数六矩 functional（所以共同 (M_3) PSD、原 Boolean 和每 job one-hot 都是同一个真实 law 的恒等式）必须同时满足每台机器、任意实系数 global (q) 且 (deg q≤2) 的
  [
  L[(T-load_i)q^2]≥0.
  ]
  这不是逐个 (q) 另找一个 law，也不是只对局部变量测试。

v 行 CONFIG 证书的承重如下。另一个 (K_v) 在 ((C,H)) 类别中仍均匀取固定大小的 home 集，将 active bad 质量从 ((1,d)) 转移到 ((1,s))，以 ((1,0)) 配平；将 inactive (H=d/2) 的 (u_0) 等分到 (H=0,d)。这保持 (C,H,CH)，而二阶降量
(p,d(d-s)) 与增量 (u_0d^2/4) 因 (u_0=4p(1-eta)) 完全相等，故 v 行所有 original first/pair（含对角）不变。每个 (K_v) 配置的 load 不超过 (T)；u 行和每个 z 行是直接的 Bernoulli 两点配置。这里的 (K_v) 只是一行配置分布，不得称为第二个共同 assignment law。

全局 (q) 的证明有三个必要台阶：

1. 原所有端点都是 (C,Y) 的 affine 函数，故 global degree-two (q) 仍是 (C,Y) 的次数至多二多项式。
2. 对 (Y) 标签置换平均；正 slack 类用 Jensen，唯一负 slack 类 ((1,d)) 在置换下不变。因此只需 (bar q(C,H)=P(H)+C(a+bH))，(deg P≤2)。
3. (q_a(d)) 由 (q_a(h),q_a(0),q_i(h),q_i(0),q_i(d)) 的五项 affine 插值表示，系数平方和为 (4lambda^2-4lambda+3≤16/eta^2)，(lambda=d/h=2/eta)。五个右侧类别的“质量×slack”均至少 (eta/40)。于是 Cauchy 的系数为 (16p(1-eta)/eta^2≤16eta/1000<eta/40)，从而得到安全的 ≤ 局部化链；五项全为零时仍成立。非 v 行逐样本 slack 非负，故同一个 (L) 处理所有机器。

该证明的结论是局部二次噪声控制和 row CONFIG 的 pair 证书。它不构造 growing-depth 的共同 law，不给低载实际调度的 decoder，不产生 near-two gap、NP/UGC/GapETH hardness、一般 unrelated-machines 算法或六人半覆盖结论。实际 (OPT=1) 是必要的 scope 标签；不能从坏样本质量 (p) 把它改写成 relaxation gap。

# 辅助 Claim：定基数 first/pair 稀疏支持

最终稿同时量化所有显式 (d≥1, 0≤ h≤ d)，令
(D=1+d+C(d,2))。目标是输出至多 (D) 个实际 (h)-subsets 和非负二进制有理权，精确保留均匀 slice 的 singleton 边际 (h/d) 与异 pair 边际 (h(h-1)/(d(d-1)))（(d>1)）；(d=1) 无 pair 约束，(h=0,d) 直接输出唯一集合。复杂度只按显式 (d) 计 poly((d))，没有 poly((log d)) 或隐式大支持承诺。

`§7` 的 Fisher–Yates 后端可逐项核验：

* (phi(A)) 是常数、全部 singleton、全部异 pair 的 (D)-维 0/1 特征。每个标签置换只置换坐标，因此是线性作用。
* 从 (A_0={1,…,h}) 出发，阶段 (i=d,d-1,…,2) 均匀选 (j in [i]) 后交换标签 (i,j)。这是均匀排列链，终点 (h)-subset 均匀。
* 每阶段先展开至多 (iD) 个已列候选，再在其特征列上做普通有理消列。常数坐标使任一非零整数依赖的系数和为 0，故可取同时含正负系数的依赖。写权为 (a_l/Q)，取正依赖坐标中使 (a_k/u_k) 最小者，并更新
  [
  Q'=Q u_k;  a'_l=a_l u_k-a_k u_l.
  ]
  该更新保持非负、权和及 phi-均值，并至少删除一列；全程只使用已经显式列出的真实 subsets。
* 每次依赖来自 0/1 的基本 minors，系数位长 (O(Dlog(D+1)))。总阶段候选/消列次数 (O(d^2D))，每次分母最多乘 poly-bit 的正依赖系数，粗位长界
  (O(d^2D^2log(D+1)))，加上 (log(d!))，对显式 (d) 是多项式。输出数量和存储也按显式 (d) 多项式。
* 该 law 只保 first/pair。它不保三阶以上矩，不替换原七态共同 (L)，也不替换 global (q^2) 证明。将它用于 v 的六个固定 ((C,H)) 类别，得到至多 (6D) 个合法原 CONFIG（按非零类别可更少）；每类 (C,H) 固定，所以 (CY)、first/pair 及实际 row load 不变。

仓库已有另一份“左右递归/超几何混合/显式候选 LP”构造。两者量词相同但构造后端不同；Fisher–Yates 的特有内容是阶段线性作用和单链消列。两者均不能被当作共同 law 或高阶矩证明，也没有将数学构造冒称为已运行软件。

# 边界 Claim A：仿射 Boolean 与 owner

固定上述七态正支持的
(Omega_0={0,1}×({0^d,1^d}∪{Y:|Y|=h}))，其中 (1≤ h≤ d/4)。对实仿射
(f(C,Y)=a+bC+sum_i c_iY_i)，若在 (Omega_0) 全部点取 ({0,1})，则完整清单只有
(0,1,C,1-C,Y_i,1-Y_i)。

核验要点是：

* (Y=0) 的两点先给 (b in {-1,0,1})。若 (b=±1)，交换 h-subset 中一个索引迫所有 (c_i) 相同，再用 h≥1 得 (C) 或 (1-C)；若 (b=0)，取补后归约到无常数的 (g(Y))。
* h=1 时每个 (c_i in {0,1})，全一向量迫至多一个为 1。
* h≥2 时交换一个索引给 (c_i-c_j in {-1,0,1})，故系数至多两层。若两层均至少两个索引，h-subset 中高层个数的整数区间宽度至少 2，与 Boolean 值矛盾；唯一高层给 (Y_i)，唯一低层给 (H/h-Y_i)，后者在全一处值 (d/h-1≥3) 被排除。h=d/4 与最小 d=4,s=2 均覆盖；h=d/2 若擅自放宽会出现额外的 (H/h-Y_i)，所以 (h≤ d/4) 不能删除。

将此分类落到共同矩时，不能直接假设新 endpoint 有真实 law。正确假设是共同 degree-six functional (widehat L)，base (C,Y) 的次数至多四矩等于真实 (P)，原 Boolean/one-hot identities 已支付到总次数六，且各选定 endpoint (X) 有
(widehat L[(X-f)^2]=0)。M3 PSD 把 (G=X-f) 与次数至多三的乘子正交；(r=1,2,3,4) 的恒等式
(X^r-f^r=(X-f)sum X^{r-1-j}f^j)
使 (widehat L(f^r)=widehat L(X^r))。四次 Boolean identity 即
(E_P[(f^2-f)^2]=0)，正支持迫 f 逐点 Boolean，回到上述六类。相应一阶/pair 也能用同一 null 正交替换。

若一个 unit head 的不同原 jobs endpoint 全都受该 affine/Gram 覆盖，同行 pair 为零且 CONFIG 阈值 (B<2)，则正一阶 owner 至多两个，恰两个时只能是同一个 primitive bit 的互补 literals。这个结论不约束未覆盖的非 affine endpoint、零一阶资格，也不是整行物理入度上界。

逐固定背景使用时，每个背景都必须重新给出 (Omega_0) 全支持、共同矩和 Gram 条件；不能从未条件化 M3 免费推出。均匀背景 (beta in [N]) 的反例保留任意大的全局正 owner 数：第 (beta) 个 job 才能随 (C) 使用共享 unit head (w)，其余 jobs 在 private head；固定背景每个 w 只有一个正 owner，但积分后 w 有 (N) 个正一阶且 pair 仍零，完整实例仍有峰值 1。该反例不否定 fiber 定理，只否定把 fiber 结论相加成全局 degree≤2。

# 边界 Claim B：忠实 AND 的窄障碍

这里的量词与 affine Claim 必须分开。固定 (i)，新增的 (Z) 必须是真正的 degree-one Boolean endpoint/坐标，且在同一 (widehat L) 中满足忠实
(widehat L[(Z-CY_i)^2]=0)。base 是次数至多五的 (C,Y) 矩匹配，M3、原 Boolean/one-hot 和次数六定义域仍在；原 v load 仍是 (C+H/d)。

取 (g=T-C-H/d)、(q=Z(H-h))。此 q 在新变量中确为 degree 2，故 (gq^2) 是 degree 5。令 (D=Z-CY_i)、(B=g(H-h)^2)（次数 3）。Gram-null 给 (widehat L(DB)=0)；用 (Z^2=Z) 的第五次乘子支付把 (gZ^2(H-h)^2) 化为 (gZ(H-h)^2)，再用 (D) 把 Z 换成 (CY_i)。base≤5 允许按真实 P 计算：
[
widehat L[gq^2]
 =E_P[gCY_i(H-h)^2]
 =-p(1-eta)(d-h)^2<0.
]
仅坏类 ((C,H)=(1,d)) 存活；该值对最小 d=4,s=2 也严格负。因而这组合同不能同时与“所有 global degree-two v-row localizer 非负”成立。

该障碍不等于所有非仿射延拓失败，也不等于普通 UM 自动有 AND 侧约束。它不覆盖改变 base、改动 v load、只保一阶边际、非忠实/近似 AND、其它 localizer 次数或新的跨背景 routing。它也不推出 hardness、gap、一般算法或 SDP finder。

# 证据层级、版本差异与去重处理

本次实际核验把四类证据明确分开：

* **解析主张（final正文）：** 对任意量词内的 (d,s) 及显式 (d,h) 的 Fisher–Yates 算法，按上述代数/消列证明成立；这不是有限代码输出。
* **来源阅读/版本证据（4c90）：** 两遍最终全文读取、独立性、旧/新 hash 和三处 diff；它确认谁读了什么，不能单独证明数学结论。
* **有限软件证据（已有审查/计算对象）：** 129 行 Fraction audit 的 12 组、其中 3 组 small full matrices 及 root fresh-output 同字节，只支持列举参数和实现字段，未实现 sparse support、affine 分类、AND 接线、SDP finder 或一般算法。
* **作者 Proof/独立重构/read-after：** 现有七态 affine/AND/稀疏支撑和全局审查对象已经区分 Exact-first、作者 Proof、读后及 root 参与插值的角色；本票不倒写为独立盲审。

旧 v1 主定理、稀疏支撑 theorem、affine owner 和 AND obstruction 是不同量词/对象，不能合并成一个“所有延拓失败”或“已解决全局目标”的结论。最终 v2 只把四种身份放进同一规范正文，并明确 §7 的显式 row CONFIG 构造新增于 v2；它没有回写旧 v1 source 或其审查记录。Fisher–Yates 与已有左右递归稀疏支持是不同具体后端，标准凸压缩不主张原创性。

# 正式整合建议（仅建议，不在本目录执行）

1. 将本票作为 `unrelated-machines/seven-state-global-quadratic-extension-boundary-20261031` 的最终稿来源增量，补充其 source_refs：4c90 原始 read-after source 与 4c3957d3e5517fdc7ae5 final正文（两个冻结 commit 均可列）。
2. 在现有定理 `archives/unrelated-machines/state/定理/七态原星全局二次负载局部核--定理.md` 的 source_refs 中补入 final正文的 clean ID `4c3957d3e5517fdc7ae5`，但保留 v1/v2 分层，不把其正文改成“全局递归”结论。
3. 在 `archives/unrelated-machines/state/定理/均匀定基数 Fisher–Yates交换压缩--定理.md` 与 `均匀定基数first-pair稀疏支撑--定理.md` 之间加交叉来源说明：前者是 §7 的单链消列后端，后者是左右递归/超几何后端；两者都只保 first/pair。
4. 保留最终审查页对 source 4c90 的独立性和三处 diff 说明；不要把 4c90 的“未读代码/未读 Proof”改写为程序认证。
5. 若需要主图超边，应至少使用以下有解释的联系：v2主Claim—稀疏支持（§7将均匀 slice压成row CONFIG）；v2主Claim—有限审计（审计仅限列出参数）；v2主Claim—affine boundary（共同M3/正支持下的fiber分类）；v2主Claim—AND obstruction（额外faithful合同下的负localizer）；v2主Claim—最终审查（版本与证据身份）。不要建立“主Claim⇒所有非仿射延拓失败”的边。

推荐正式对象路径：
* `archives/unrelated-machines/state/审查/七态全局二次局部化接线与扩展边界最终审查--审查.md`（版本/证据主审查）；
* `archives/unrelated-machines/state/定理/七态原星全局二次负载局部核--定理.md`（v1 主定理落点）；
* `archives/unrelated-machines/state/定理/均匀定基数 Fisher–Yates交换压缩--定理.md`（§7 单链构造）；
* `archives/unrelated-machines/state/定理/均匀定基数first-pair稀疏支撑--定理.md`（递归构造）；
* `archives/unrelated-machines/state/审查/七态原星仿射Boolean所有者边界Exact与作者Proof版本审查--审查.md`（affine scope）；
* `archives/unrelated-machines/state/审查/七态AND端点二次localizerExact量词与障碍范围审查--审查.md`（faithful AND scope）；
* `archives/unrelated-machines/state/计算/七态星全局二次审计与root重放边界--计算.md`（有限软件证据）。

这些是目标建议；本次没有改写其中任何文件。当前目录保留本票和回执，供 Boss 做第三阶段语义整合。

# 本票结论

在最终 218a5c4e 字节和明确量词内，未发现除旧 strict-< 书写外的 fatal 数学问题。主核的正向证明、§7 的有理消列、affine 分类和 faithful-AND 负值各自有完整承重条件；它们的边界也在正文和既有交叉审查中保持。最终稿不能升级为递归共同证书、near-two/hardness、一般调度算法或六人半覆盖结论。建议处置为 `integrated-scope-increment`：将本票加入最终审查来源链，源 4c90 标记 integrated/read-only，正式正文保持现状。

