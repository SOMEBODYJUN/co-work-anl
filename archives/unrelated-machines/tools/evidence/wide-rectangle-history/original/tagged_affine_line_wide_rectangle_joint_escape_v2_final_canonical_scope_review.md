# Wide-rectangle tagged affine LINE v2：最终 canonical 实读范围审查

Reviewer：bicriteria_set_packing_bridge，2026-10-18。只读 canonical；仅在 clone 外 scratch 新冻本记录，不修改 repo、Git、Work 或任何旧 raw/独立记录。

## 1. 实际读取版本与正式范围

已实际全文读取：

`/workspace/scratch/038d9dcc4cac/co-work-anl-boss11/research/current/unrelated_machines/tagged_affine_line_wide_rectangle_joint_escape.md`

whole-file SHA256：`577e5cf39d579c2dc034334ab1a2b1cb17cdbdf3e698f3330b94f5a2a2e4cb65`。

root 指定的正式审查范围是标题后的身份 header 加全部 §1–5；上述全文读取覆盖此范围。本次不读取 v1 或链接中的其它源、关联 Claims、review 页面，不把这些页面的内容纳入认证。header 将 v1 仅作历史 Exact、只登记成熟 v2 的写法没有冒称 v1 经过本 reviewer 审查；root 报告其自己实际读 v1 不转写成本 reviewer 的读取事实。

候选 ID：`UM-TAGGED-AFFINE-LINE-WIDE-RECTANGLE-JOINT-ESCAPE-v2`。

结论：**PASS，未发现数学、完整调度、量词或位复杂度方面的 fatal。** 最终正文完整保留 v2 Exact 与作者 Proof 的承重范围，并正确加入本 reviewer 独立记录中的严格边界例；不升级为一般 UM、SC 或所有 hard source 的结论。

## 2. 先行证据链及不变原源

本 reviewer 真实顺序为：仅据 v2 Exact 独立全文重构并冻结；root 实读该记录后解封作者 Proof；本 reviewer 再实际全文读作者 Proof 并另冻 read-after；现在实际读最终 canonical。没有倒填成先看作者 Proof 后的独立重构。

本次重新核对的旧文件 SHA 均保持：

- v2 Exact：`tagged_affine_line_wide_rectangle_joint_escape_exact_v2.md`，`6be53020ad2e0f8f810fa1cbc862fa0ba931378c04b60c2e7d81d34a564d9063`。
- v2 作者 Proof：`tagged_affine_line_wide_rectangle_joint_escape_proof_v2.md`，`e7254f500b3331febc2136b478ec40662a60538bcf9b639adbb7945ce0a83d1a`。
- 先行独立记录：`tagged_affine_line_wide_rectangle_joint_escape_v2_independent_review.md`，`f2786b3bed4533bdb273dfe8dfa1eb53e1674afdc81726bcee64a79dfbccdaf4`。
- 作者 Proof 读后：`tagged_affine_line_wide_rectangle_joint_escape_v2_author_proof_read_after.md`，`2c8a01f786f83ba5fe1e48c4e375bd1d89ac516c464b593afc33f6696cddaef6`。

本记录不重写任何一份旧原源的事实身份。root 已先听作者口头策略，因此 header 不将 root 记成该 Claim 的 blind reviewer，符合实际顺序。本 reviewer 没有运行软件实现或有限数值扫描；header 没有把这类认证归给 root、作者或本 reviewer。

## 3. Header 与 §1：精确域及所有量词

正文明确 prime R>=2，非空 groups、每组非空 distinct-variable 集和非空 indexed-state 菜单，完整 variable-tagged F_R² planes，同一变量上不同组 fixed intercepts 单射。所有非负有理 p（含 zero）按完整 state 总和恰为1。同 state 内每变量恰一条完整 line，变量 tag 不混同，因而 incidence 资源无重。unused variables 可以空置。

rectangle 是输入明确给定的 Cartesian product，全部 vectors 均在菜单出现；菜单可以有其它 states，相同 label vector 可以对应任意不同权和 marks。主合同覆盖这些完整输入的全部合法固定 intercept 编号，算法不更改 j；没有将“存在一种可重编号 source”偷换成全域结论。

b 是 binary nonnegative integer，β 是 binary nonnegative rational；每条实际 state-variable line 的 marked 列表<=b，所有本 state 的 unmarked cell 权<=β。marks 可以依赖整个 indexed state、含 zero。主条件严格为 L>b(D−1)，主质量是 v=max(0,1−Mβ)，其中 M=max_gΣ_(x∈X_g)(d_x−1)<=q(D−1)。minquality、normalization、D>=1 均由明确非空前提保证有定义。

合同要求同一个联合整数 allocation 同时保留全部 selected marks、全部 selected 独占点，并给全部组质量保证；未声称完整 selected supports 不交。header 与 §1 都保留了这一点，也保留完整 ordinary jobs 及 infinity 资格的实际矩阵。

## 4. §2–3：任意 state-dependent marks、联合分配与全部任务

§2 的逐组构造正确：一个旧 mark 的 z!=0 时至多禁止当前一个 slope；z=0 时其 y 是不同的旧 intercept，不禁任何 slope。至多 b(d_x−1) 个旧 marks，严格少于 L，使每坐标可取一个合法 label。完整 vector 先由 rectangle containment 查到一个真实 indexed state，随后才绑定该 index 的真实权和 marks 给后续使用。相同 vector 的其它 states 不被合并或以其权/marks 替换当前 index。

因此新完整 line 避开旧 marks，新 marks 自然与旧 marks 不同；无需提前预测这些 marks。新 marks 仍可打中旧 unmarked cells，正文明确保留这类重叠，未宣称整个 T_g 不交。

§3 取 Q_g 为 selected support 中全部独占点、B_g=E_g∪Q_g。这确是一组同时合法的资源子集：marks 两两不交，独占点不可能撞到任何其它 selected support。marked/unmarked 共享点只归 marked owner，全 unmarked 共享点可不领取。任何损失点都在本组 unmarked 且为共享点；每变量至多 d_x−1 个不同-intercept line 交点，跨变量 tag 分离，所以损失点 union 数<=M_g。多对手共点只使计数更松。每点权<=β，逐组取得至少1−M_gβ，结合非负性即 v。该计账覆盖 marks 抢旧 unmarked 的实际损失。

同节实际调度包括全部 selectors、选中 state 的领取/未领取 jobs，以及所有未选 states 的全部 jobs。zero job 不删除；若导出，仍按对应 resource 的真实 unit 时间计费。资源负载<=1，未选 private 行和为1，选中 private 是 selector1加剩余私时，即2−p(B_g)<=2−v。0<=v<=1 也覆盖其它机器。故这是全部原 jobs 的实际 peak bound，非 CONFIG/局部可行或 partial schedule。

至少一个 unit selector 给所有合法调度 OPT>=1；v=1 时输出峰值和 OPT 均恰为1。v=0 时上界2仍合法，无须正质量逆向提取。

## 5. §4：两推论、端点与严格 R2 边界

Sparse-positive 的全部正点标记、β=0，直接保全正质量并给实际 OPT1。每 line 的正点数预算 b 与 variable degree D 明确不同。b=β=0 与非空 norm1 实例不兼容，正文没有为该空子域做无效除法。

Arbitrary-weight half 取 K=2q(D−1)>0、β=1/K、b=K。每 state 总权1，严格超过1/K的 cell 总数<K，故逐 line 也<=b；阈值等号点 unmarked 仍<=β。L>2q(D−1)² 正是主条件，Mβ<=1/2，所以质量>=1/2、实际完整峰值<=3/2。没有按 K 值复制任务。

M0/D1 端点准确：若某出现变量 degree>=2，则任何包含它的组 M_g>=1；反之 D1 使不同组资源块分离。于是 M0等价于D1，任取 states 可全领取、实际 OPT1，不对 D−1 或 M 求逆。unused degree0 不在 M_g 的和中。β0、b0、R2、q1、单组各分支均被证明覆盖。

正文加入的严格边界例与独立记录一致：R2、单变量、两 singleton-state groups，j=0/1、slope=0/1，共同点(x,1,0)分别私权1且 marked，其余权0，各 A singleton，L=1=b(D−1)。两组不能同时领取该唯一正权资源，所以V0。全部 jobs 留 private 给峰值2；若峰值<2，两 selector 被迫在各自唯一 private，而该组私权1的正 incidence 必须导出，导致同一 resource 上两件 unit jobs，矛盾。因此实际 OPT2。

该例不满足主合同的严格 >，仅说明不能对所有输入直接改成 >=。正文没有把一个等号例升级为所有参数的全局 sharp 门槛，也未当作 hardness。

## 6. §5：显式核验、总位长及否定范围

rectangle 核验统计落在 product 内的 distinct label vectors 数，与 binary product ∏|A|比较；这些 vectors 已是 product 的子集，因此等数等价于 containment。product 位长由各 log|A|之和控制，不枚举一个可能比菜单大的 product。同 vector states 仅在这一步计数时去重，实际权/marks/index 不合并。

禁 slope、选 label、查 state、构造 Q/B 和全调度都只扫描真实显式表/列表。giant binary b、极小β及大有理分母只参与精确 binary 运算，不按数值创建对象；β0 不计算倒数，非零场元素才求逆，z0另处置。精确有理求和、Mβ与比较均有完整输入总位多项式界。

n=Σ|S_g|、m=RΣ|S_g||X_g|、u=|X|R²、h=|G| 时，机器n+u、jobs m+h、finite entries2m+n，selector选项之和为n，zero私时端亦保留。dense矩阵大小(n+u)(m+h)和全部 jobs assignment 输出均是显式展开输入的多项式。正文不声称二进制R、compact CSP或权oracle输入的poly(logR)免费展开。

否定范围准确停在满足 wide rectangles、fixed-intercept 注入和 label-slack 条件的输入子域。任意 source 的实际 tables 是否含所需 rectangles、参数是否合界、perfect completeness/hardness/NO decoder 是否成立仍待独立核验。不能由“可扩大 alphabet”或 pairwise independence 自动推出该输入域，也不能把 code-coset 菜单视为必有非平凡 rectangle。`UM-TARGET-v1`保持 OPEN 与本证明范围一致。

## 7. 最终认证

在 whole SHA `577e5cf39d579c2dc034334ab1a2b1cb17cdbdf3e698f3330b94f5a2a2e4cb65` 的实际文本上，header+全部§1–5正确落地先前独立 proof和作者v2 Proof，涵盖同一state-dependent marks、任意合法fixed j、联合整数partial、全部ordinary jobs、两个corollaries、严格R2边界及总位复杂度。无需修改数学合同或放宽范围。

本记录不是对v1、链接中的其它Claims/源、软件实现、有限实验、外审或全球新颖性的认证。所有旧 raw、独立记录、作者读后记录原字节保持。未来 canonical 若改变，应另行给定实际版本并实读，不将本次认证自动延伸到新字节。
