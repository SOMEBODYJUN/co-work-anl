# 路径范围审查三处措辞勘误的独立复核

状态：冻结独立复核；Boss5 / 474257b8-path-scope-erratum。本子任务只形成本文与同名前缀 JSON，不改原档、registry、coverage、integration、其它 worker 文件，不操作 Git 或队列。

## 结论与最小性

接受 root 候选 `cube-path-review-erratum-474257b8.md`。旧范围审查 SHA 为 `ee48116b9ceed7277a49a64b045b4ca5239ebbf794322a1bdfc9af8f908c119f`，候选 SHA 为 `1239534319b20364efc91d34af78913b3dfe1b8898a1949c0c9d119c6dc025e0`，原始字节分别为 10073 与 10220。逐行比较恰有三处差异（旧行 25、38、42）：表中路径 D 的不保留量、§2 helper 账本、§2 末句的菜单/selector 保留范围。全文其余字节保持，特别是 §5 历史 BCG 核验说明及 §6 边界逐字未改。两份定理正文不变，未改数学量词、源域、端点或一般性，不新增归约、NO 源或一般 UM 定理。

候选把“保持旧菜单”用于 D 正文中明确的按组资源替换语境：保留全部 indexed states、原 state 私机、private 权和菜单大小，只将旧 incidence 的资源端从 R_u 映到本组 port z_(u,j)。它没有声称原共享资源机名字或每件旧 incidence 的原资源资格字面不变。旧 selector 的全部有限资格则是真正逐项原位保留。

## 逐原任务与资格复核

实读 `完整菜单的资源度三路径归约--定理.md` 全文，尤其 §1–4、§6–8；实读 `归一化菜单的三态资源度三正规形--定理.md` 全文，尤其 §2、§4–6；实读旧范围审查全文、候选全文与三处 diff。

D 对旧组 g_j 的每个原 indexed state s 都保留原 M_(g,s)、原 incidence 任务身份及 p_(g,s,u)，只把所有该组对应 u 的旧 incidence 的资源端统一改到 z_(u,j)，资源端时间仍 1。J_g 仍只在全部原 M_(g,s) 以 1 运行，资格数量 K_g 与每一资格均不改。零 private 权、未选 state、重复 indexed states 与空 state 不被合并或省略。原任务与新增 helper 任务通过 fresh 标签区分，逆向删的是新增任务，不是原零权任务。

一个二态 helper H_j 的真实矩阵为：两台独立私机 M_L、M_R；一件 selector J，可在这两私机各耗 1；一件 i_L，只能在 M_L 或 port z_j 各耗 1；一件 i_R，只能在 M_R 或 port z_(j+1) 各耗 1。其余资格为无穷。因此每 helper 组是 2 私机、3 jobs、6 有限资格，每 state 只有对应的一件 incidence。原审查把组级的 selector 与两 incidence 写成“每个 state”账本，候选已精确修复。

T 与 D 必须区分。K_g>1 时，选择树把旧 J_g 用作 root selector，将资格改到 root 的 child-own singleton states；原 incidence 和原 state 机仍沿用。K_g=1 时 root 即原 leaf，原任务原位不动。D 在任何输入（包括 T(P) 的全部旧/own 资源）上都保其输入各旧组的 selector 资格；复合正规形的不保原 selector 资格来自 T。

## 任意 C<2 输出的独立证明

给任意源完整调度 σ，峰 C<2。selector 的单位处理时间使 C≥1；每原 R_u 最多接一件实际外送的单位旧 incidence。该计数包括未选 state 以及 private 权为零但实际外送的原任务。若唯一外送来自 g_a，留 port a；若没有外送，任选 a。对 j<a 的 H_j 选择左 port，对 j≥a 的 H_j 选择右 port，恰匹配除 a 外的 d−1 ports。每 helper 的 selector 留所选私机、所选 incidence 送匹配 port、未选 incidence 留另一私机。全部三件任务都恰执行一次，新机负载≤1≤C；旧私机与旧任务的 private/外送决定保持，旧资源端只作前述 port 映射。

反向给任意目标完整调度 τ，峰 C<2；不能假定 τ 等于正向构造或有预设 matching。每个 helper 的 selector 实际选中的 state 中，unit incidence 不能留私机，否则两件 unit 共机形成负载 2，故必须外送。每条 d-port 路径有 d−1 件这样的任务，必须占 d−1 个不同 ports。未选 helper incidence 若也外送，只会额外占位，不能释放已被强制占用的 ports。因此该路径至多一件旧 incidence 外送。按任务身份删掉全部 helper jobs/私机，把旧外送 port 合回 R_u，旧私机及旧 selector 保持，原 jobs 全部合法恰一次且峰不增。这覆盖任意部分外送和所有未选旧 state 的真实任务。

d=0 保 unused 资源机，d=1 无 helper。C≥2 时用另一侧全 private≤2≤C 基线，不保给定调度的外送决定；在 C=2 不能沿用 helper 强制外送。有限最优值达到与双向低峰转换闭合 OPT=2。归一化 W=1 时，正 partial 阈值要求每 helper 领取 singleton，完全相同的 port 占位论证保持全部正阈值；有限最大值与反向矛盾闭合 V=0。未归一化 W≤1 不免费套用 V 合同。

## 实际登记与图影响

当前 registry 的单页反向材料 owner 与实际 body/evidence 全扫描一致，恰为三个 owner：C v2→v3，D v3→v4，N v3→v4。只改命中附件 SHA 并 version+1，不改 statement、model、quantifiers、assumptions、scope、objections 或其它来源。精确旧/新 pin、完整新旧对象记录和新材料记录均在 JSON。

canonical `edge_files` 清单中恰两条关系命中这些端点，均未直接引用被改页为边证据，数学原已正确：

- `um-cartesian-reverse-values-transfer-through-three-state-normal-form` 的实际方向是 ALL{Cartesian, N}→`unrelated-machines/bare-cartesian-read-after-normal-form-palette-scope`，只认证目标精确迁移 consequence 的 contribution。它不是 Cartesian→N。其 helper 和先树后路径文字正确，原 selector 资格改变指复合正规形，因此勘误不变其 V、OPT 数值或作用范围。
- `um-real-path-reduction-completes-three-state-normal-form` 的方向为 D→N；边内完整支付 T 的第一阶段并明确 T 改 root 资格，再调 D 到所有旧/own 资源。helper 强制与端点证明正确，完整目标保持。只须新端点 pin 重绑定。

有效 done 恰两包：`unrelated-machines-3a-3a-2cf9efe56bf3d79c`（Boss3，6 核心，N 是 shared）和 `unrelated-machines-3a-3a-4b528c45d7d1e1f8`（Boss5，15 核心，C/D/N 是核心）。两包当前输入均无既存 pin mismatch。应按同层定向替代，旧核心全部保留，两受影响边改到替代资产；另七件资产全部保原 path/SHA，不重判无关数学。4b 旧 C coverage reason 的“路径/正规形是改变组及资格”合写应在新 receipt 中明确 D 保旧 selector、T 才改资格；该旧覆盖措辞也不能跟着原样继承。

unfinished 恰已 plan 的 `boss5-474257b8-cube-3a-0a0c1be8c9ee5558`，本快照为 available/null。应刷新同一任务，保持实际 owner 与 write_paths；共享 C 切到新 pin，并按已有 goal 用 read-add 补 D 为 ALL 前提。复合核心 M-4aa4bcc7358b4ab8bf1bc53f57d3f1d1 不引用被改页，其记录和 pin 保持。无其它有效任务或历史 superseded/withdrawn 任务命中。

## 可供原子发布的数据与范围限制

JSON 含一次 registry/baseline/coverage/integration 和三任务文件的精确追溯快照；真正应用 guard 只有原 source 旧 SHA 与三 owner 旧 registration_pin。root 读取最新整份 registry 后定向替换三 owner/材料，保全部并发对象与 edge_files，不以本报告旧整仓覆盖现行。JSON 另含：三 owner 全记录；保全仓 4006 材料、只换本页 SHA 的历史 inputs 候选（仅表达本次 delta，实际最终分母由 root 重做 prepare-inputs/freeze）；新 baseline 的真实 commit/SHA 生成条件；两条重绑定边与两个定向替代 receipt 的完整候选；七个 retained 资产的精确 SHA；unfinished 同任务刷新蓝图。尚不存在的新 baseline commit/SHA 没有伪造，须由 root 在实际新字节提交后 freeze，并将源、所有 owner/version、新 baseline 和 registry 一致接入同一最终发布 tip。

本 worker 未查询远端、操作 Git/队列或发布 canonical；root 执行前应按 source 与三 owner 的精确 guard 重核；whole-registry SHA 仅作追溯，3D 并发变动不触发整仓旧快照替换。未重跑有限枚举，也未重读 BCG 原 PDF；历史文献核验范围保持原文，仅凭本页自足矩阵和两向映射作上述局部数学判断。复核已冻结，交 root 接续。
