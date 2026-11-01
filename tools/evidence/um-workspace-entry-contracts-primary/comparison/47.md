---
id: "unrelated-machines/affine-line-primary-marginal-review"
kind: "review"
type_tag: "审查"
title: "仿射线单primary、单边际与多primary的双源审查"
status: "integrated-with-separated-contracts"
truth_status: "scoped-structural-proofs; exact-UM-values; no-hard-image-or-general-UM-conclusion"
review_level: "full-source-read-and-cross-archive-comparison"
scope: "one-primary pairwise-uniform unit contract; distinct single-marginal and multi-primary simplex near-two constructions"
source_refs:
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/tagged_affine_line_pairwise_independence_boundary.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/current/unrelated_machines/tagged_affine_line_uniform_marginal_gap.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/tagged_affine_line_pairwise_independence_boundary_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/reviews/unrelated_machines/tagged_affine_line_uniform_marginal_gap_review.md"
legacy_ids:
  - "UM-TAGGED-AFFINE-LINE-ONE-PRIMARY-PI-ONEHOT-HELPER-UNIT-ESCAPE-v1"
  - "UM-TAGGED-AFFINE-LINE-PI-SIMPLEX-TINY-VALUE-v1"
  - "UM-TAGGED-AFFINE-LINE-BALANCED-MARGINAL-TINY-VALUE-v1"
---

# 1. 实读范围和版本核对

本批完整读取两个当前 canonical 正文、`clean show` 全文、inventory 元数据、相应冻结审查、先前 affine-line/line-set-packing 相关正文与证据说明。当前源 `272262722a54067c48fd` 路径为 `research/current/unrelated_machines/tagged_affine_line_pairwise_independence_boundary.md`，SHA-256 `0b94156ecd6552e8ab29961ce03a5d21ddfa75cb945ab802da7115bf781970bf`；`185276e862541c1855b6` 路径为 `research/current/unrelated_machines/tagged_affine_line_uniform_marginal_gap.md`，SHA-256 `b81d3f53d711d30ac83f5ba94f12a9a14e7ffc8242cd176373d05bf3c457c501`。两源均为冻结提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 的当前版本。

两源共享tagged affine-line的完整普通UM编码：每indexed state一private、每tagged真实资源一resource、每group一selector，全部state-resource incidences均为原任务；私权作private处理时间，resource处理时间1，零私时任务、未选state及fresh padding全部保留。第一源272同时保留两个不同对象：每helper仅一primary且primary/auxiliary pairwise-uniform时的unit正面合同，以及每helper多primary、仍all-pair uniform的PI-SIMPLEX反例。第二源185另给每group恰R states、R(R−1) helpers、V=1/(R−1)的单标签均匀族；其中helper虽仅一primary，但其auxiliary与primary相关，故不满足unit定理的pairwise前提。它不是PI-SIMPLEX的R⁴-states构造。

后续整理发现本页原第3节展开的是272里的PI-SIMPLEX，不能据此称185独有构造已逐项吸收。185的完整构造、任意选态/partial上下界、全任务OPT=2−1/(R−1)、共同arity/R-partite padding及精确计数现见[独立单边际反例正文](../反例/单标签均匀边际仿射线菜单的趋零保留--反例.md)。保稳定ID与旧文件名作引用兼容，不改下述unit与PI-SIMPLEX数学，也不追溯改写原阅读过程。

# 2. 单 primary：pairwise uniform 足以做 unit escape

稳定身份为 `UM-TAGGED-AFFINE-LINE-ONE-PRIMARY-PI-ONEHOT-HELPER-UNIT-ESCAPE-v1`。取素数 `R>=2`。每变量 x 有独立资源平面 `(x,z,y)`，每组 state 为每个变量的一条完整 affine line `y=a_x z+j_x(g)`，私权总和为 1。唯一 main M 参加全部 primary；每个 helper 只含一个 primary `u(h)` 和任意 auxiliary variables，不重复变量。helper 的局部分布 `lambda_h` 对 primary label uniform，并与每个 auxiliary label pairwise uniform；不同 auxiliary 不要求联合独立。

固定任意 main state。对每个 helper 只条件化其唯一 primary label，条件后的状态分布仍使每个辅助 label uniform。定义 helper 唯一正 private cell 的条件质量 `f_(h,r)`。在某 primary 资源平面上，所有相关 lines 斜率相同而截距互异，故两两不交，任一 cell 最多承载一 helper 的条件质量；main 的全部正 cells 也被避开。辅助变量的 `z!=0` cell 对应唯一 slope，条件概率为 `1/R`，同一辅助变量至多 R 个 helpers，列总量至多 1；`z=0` cell 用互异截距直接证明至多一个 helper。于是 `f` 是行和 1、列和不超过 1 的分数二分匹配。

从显式原 state table 建 helper 到资源的二分图，不需要计算 lambda。上述分数支持该图，Hall 条件成立，增广路匹配覆盖所有 helper；每条匹配边保存一个完整原 indexed state，避免拼接不兼容 labels。main 取指定 state 的全部正 cells，helpers 取匹配 state 的唯一正 cell，所有 groups 质量恰 1，故 `V=1`。完整 ordinary UM 调度把选中正 incidence jobs 外送，所有其他 state/jobs 留各自私有机，资源至多一件 unit job，峰值恰 1，selector 给 OPT>=1，故 OPT=1。

该结论可处理 auxiliary 为空、unused variables、R=2、零概率 states、main 非零截距和 state-dependent onehot 点；其复杂度按完整显式 state/line 表多项式。它明确不处理多个 primary 的同时条件化、main 参加 auxiliary、额外 groups、预载或缺少 pairwise 条件边际的输入。局部 LP 只用于检查边际接口，不是实际 UM/configuration oracle。

# 3. Simplex 多 primary：所有 local pairs uniform 仍可趋二

稳定身份为 `UM-TAGGED-AFFINE-LINE-PI-SIMPLEX-TINY-VALUE-v1`。对 odd prime `R>=3`，取二次扩域 `K=F_R[omega]`（`omega^2=nu`，nu 非平方）、trace `Tr` 和公共四维 full projective simplex code C。part 集 `Pi=B x T`，`B=R^2+1`、`|T|=R+1`、共同 arity `q=B(R+1)`。main 含全部 q 个 primary；每个 helper `H_(a,j)` 同时含自身 block a 的 R+1 个 primary 和所有其他 part 的 fresh variables，总 helpers `B(R−1)`；fresh variables 只属于一个 helper，padding 具有真实原任务和零私权，不可删除。

state `zeta=(u,v)` 的 primary labels 是 `E_(a,t)(zeta)=Tr(t w_a(zeta))`；helper 在自身 block 平移 `-j`，其他 parts 使用同一 codeword，故各 helper relation 是公共 C 的非零 coset。每个 group 有全部 `R^4` indexed states。main state 只在一个 block `D_alpha` 的 R+1 点上赋权 `1/(R+1)`；helper state 只在自身 block 的一个 trace-zero 点赋权 1。trace 非退化、`T` 遍历所有一维方向，C 维数 4 且 q=(R^4−1)/(R−1)。uniform state 下所有不同 primary/fresh pairs 都均匀；这不是只核 primary 边际，source 明确保留全部 pairs 和完整 padding。

每个 helper 的正资源邻域恰为整个 `D_a`，因为任意目标 trace direction 都可由某个 state 产生。若某 helper 质量为 0，minimum 已至多 `2/(R+1)`；否则每个 block 的 R−1 helpers 必占 D_a 中 R−1 个不同点，main 的某个 state 只在一个 D_alpha 的 R+1 点上有正权，至多剩两点，故 `V<=2/(R+1)`。取 main 在 D_infinity 预留两点、各 helper 在每 block 取不同其余点，达到
\[
V=2/(R+1).
\]

完整 UM 下界不依赖分数合同：若 `C_max<2`，被选 helper state 的唯一正 job 不能与 selector 留在同一 private root，必须外送；每个资源机至多接一件 unit job。每个 block 的 R−1 helpers 消耗 R−1 个 D_a 点，main 最多外送两个正 jobs，selected main root 至少保留 R−1 个 `1/(R+1)` 正 jobs，再加 selector，负载至少 `2-2/(R+1)`。达到调度把 main 外送两点、helper 各外送一个正点、其余全部 jobs 留 private，因此
\[
OPT_{UM}=2-2/(R+1).
\]
该值趋 2，但只是显式可计算族的精确值。

对应 ordinary additive CSP 的全局值也已单独计算：main code C 不含非零常量向量，非零 cosets 两两不交；满足 main 时不能满足 helper，未满足 main 时每个 block 至多一个 helper，故最多满足 `B=R^2+1` 个 constraints，精确值为
\[
B/[1+B(R-1)].
\]
这项 CSP 值、UM 值和 pairwise independence 都是确定性有限域计数，不是 NP-hard promise、源 NO decoder 或外部文献困难性。

# 4. 比较、反例边界和第三阶段用途

这两个来源涉及三个准确不同的对象。单primary正面合同利用primary/auxiliary的pairwise条件化和Hall实现unit escape。PI-SIMPLEX让每helper同时占R+1 primary，在all-pair uniform下仍发生全局拥塞，值为2/(R+1)。独立单边际族每helper仍仅一primary，却缺pairwise独立，值为1/(R−1)。PI反例逻辑上也说明更弱单边际条件不足，但不能替代185的具体构造、精确值和来源去向；三个量词/状态表均不合并。

与任意权完整并行关系的affine-line半保留相比，这里更强pairwise单primary前提给unit调度；PI-SIMPLEX另外依赖公共四维code、多primary及完整fresh padding。185的单边际反例则有自己的R-states/helper拥塞与零权保值变换。它们均未给source hardness、NP-hardness或一般UM近二近似结论。

第三阶段可据精确对象分别记录关系：

- `one-primary + primary/auxiliary pairwise uniform` → `条件化 + Hall` → `V=1、OPT=1`；
- `multi-primary simplex + common coset + all pairwise uniform` → `每 block R−1 helper 占位` → `V=2/(R+1)、OPT=2−2/(R+1)`。
- `R-states单边际族、相关auxiliary` → `main block的R−1 helpers占R个可用正点` → `V=1/(R−1)、OPT=2−1/(R−1)`；完整论证在上述独立反例正文。

关系边必须标注“显式结构域”和“完整原任务/资源表”条件，不能把 simplex 的趋二族当作 hard image，也不能把 one-primary 的 Hall 证明推广到多 primary。

开放义务包括：在真正的 source hardness image 中同时保留 pairwise/global consistency、建立 multi-primary 结构的可解码 NO 结论、处理删除预算和多层 auxiliary 共享，以及一般 UM 的共同容量算法。两源有限域/匹配和完整 UM 计数都是自足证明或确定性构造；没有外部同行评审或一般算法。

逐源处置：

- `272262722a54067c48fd`：既有`integrated`记录保留。one-primary的pairwise边际、条件Hall、显式状态图、完整unit调度及同源multi-primary simplex对象在第2–4节。
- `185276e862541c1855b6`：既有`integrated`记录保留；其R-states、非pairwise单边际构造、精确V=1/(R−1)、完整OPT=2−1/(R−1)、padding与计数已独立整理为[单标签均匀边际反例](../反例/单标签均匀边际仿射线菜单的趋零保留--反例.md)。本页第3节保留另一个PI-SIMPLEX对象，不再将185错接为该节的独有来源。

两源均为全文件实读，相关审查/程序/证据已比较，独有内容去向和不混量词的理由已明确记录。
