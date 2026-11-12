# 两条取向—调度 pending 关系的独立 3D 语义复核

本报告严格只读 Boss1 clone `/workspace/scratch/1a53a6eb65ea/co-work-anl-boss1`。先读 AGENTS、IMPLEMENTATION 第三阶段、03-map-worker，然后读取四个当前完整对象、两条旧边、两份旧收据及任务、当前源正文与冻结 primary 的必要完整证明。全部新文件只在本报告所在的 clone 外目录；没有 Git、queue、sync/checkpoint、源、registry、edge 或 receipt 写入，没有子代理或成熟科研程序重跑。

**数学结论：两条旧边均正确且可完整复用原论证，只需正式任务中的当前版本/证据重绑定。623 保持 accepted / ALL / unconditional / whole_result；777 保持 accepted / ALL / unconditional / contribution，只证明等时双端子域的 FPTAS，不能升级为目标全定理。旧 777 的 W/d 网格已经完整有效，不需要为了换成 B_min 网格改写成熟数学。** 两条旧边的只读 `research_runtime.check_edge` 都实际报 Asahiro 正文 stale content binding；不能把本次 3D 阅读冒称它们已是 current canonical 或已经完成正式 repair。

## 实读输入、版本与 delta 边界

初读四对象时 registry SHA 为 `3222487146a50a0ea41a1856e046ab3c21e27b7a6e80d17c1e1bf84b2de17445`。精确初读 UTC、末次 UTC、末次 registry/integration/任务 SHA、对象和全部本范围 refs 的当前字节验证见 `bindings-and-routing.json`；Boss 同期可继续整合，报告只对这些逐项采集的对象与文件负责。

| 对象 | 当前版本 | 当前 registration_pin |
|---|---:|---|
| `M-af28c29d24b14be393e56add3cebfc7c` | 4 | `3d006e3f06c9570a8ccbbb50cf299c465c4a37e8b1d04d1e56d90cb0527365fc` |
| `M-1b8213b483df41bd9fa149b10255daa3` | 2 | `b1f641db6d0df9cc8be5e7fd3d69b3c37578f403733ceea79a752742808b0069` |
| `M-20c5c28925d440e48d955b1293aaddb9` | 4 | `545e9ae7c48db43445d50da866c4888b4ff769007adb88b4892cf8c211a005c2` |
| `M-14dbe6980117492aa7a3b48c52378dcb` | 5 | `8d3c860cc8f5e4d5abd95ab0b8891067fb982bc537b9f4870b161e43a7800372` |

Asahiro 当前全文 SHA 为 `3fe059248d81113e400a7c5fe3084cccc9eb53267d4c4f1a570e086bc1a06e0f`，冻结 PDF 仍为 `5db93652d80fd92b6440e0a0e22edfdeb09f78e2b886c95cb4adf171c67ee147`。本轮直接全文读当前中文，直接提取阅读冻结 PDF 页1–5、11–13、15–19；页12–13及16–18逐页渲染目视。后者覆盖 Theorem10 的全递推和计费，以及 Theorem13 的完整 gadget、二部划分和双向 gap。未声称阅读其余页的新证明。

Page 中文全文在当前目标 body 中直接读过；冻结 `bounded-job-assignments.pdf` SHA 为 `a2fad69bcf3b1e6caed4ce4f29d559e1b0f394695d859f2ca0fd8f05f8296775`，本轮直接读页2–3及6–8，页3目视。数学承重为资格/交叠图定义、入端计负载、diamondless 的非诱导子图含义及其独立2/3归约。

结构参数中文直接读模型、基础界、treewidth 全节及 Theorem3；正式 join audit 全文直接读。冻结 `structural-parameters.pdf` SHA 为 `4b47eaccfcffe81f6713522269b6afa2124bec3d619d6ef3a1b5341db7e48bae`，本轮直接读页1–5、9–11；页10–11目视。实读两条当前 canonical 支持边 9a5cd、ea3c 及其当前 review 的相关完整证明段，核 B_min、cap、真实回溯和独立 PARTITION 来源；这没有把一般资格 DP 冒称为 MMO 原算法。

本 worker 未使用 Git，未恢复两个旧全文版本并做逐字 diff。旧边实际记录的 Asahiro SHA 分别是 58b4be…（623）和93be27…（777）；当前对象 objections 明确说明：Maf 的全页刷新含已付清的安全 join 计费、随后另段 gate 轻边方向澄清，本节 Theorem13 合同及冻结 PDF 不变；M20 当前 v4 保留安全双表算法，仅因同页 gate 澄清刷新全文 SHA。这里的“delta 不影响本关系”由当前承重段及未变 primary 的重新核读支付，不冒称已亲自比较旧全文的每个字节。M14 当前 v5 与旧边 pin 完全相同，当前正文 `113ed833…` 和正式 audit `3b26e5…` 已在旧777正确引用；独立 rankwidth m² 勘误不参与该边。

## 623：k=2 planar bipartite MMO 完整迁移到 diamondless job hardness

旧任务 `unrelated-machines-3a-3a-6231f96071b186d2`，core 为 Maf28…，read 为 M1b821…。源陈述对每个固定整数 k≥2给正权{1,k}的强 NP-hard 判定及严格小于1+1/k的伪多项式近似障碍。目标要求任务作顶点的资格交叠图无菱形子图、每机至多3项资格任务的 R||Cmax，区分 OPT≤2 与 OPT≥3 NP-hard，且 P≠NP 下对每个固定1≤c<3/2无多项式 c 近似。源对象的全部 k 量词不需要、也不能反向由目标恢复。

原 Theorem13 的 k=2 实际归约满足本桥的全部条件。每个出现位置的正负文字节点各有两条变量环边，至多一个附加子句边，度≤3；a 点度2；b 点有两条权1环边和k−1=1条连接 special 的边，度3；q∈{1,2,3}文字子句有q条文字边及k+1−q=3−q条 special 边，度3；special 是4环，每点两条权2环边，偶下标点至多再接一条外部权1边，度≤3。不同位置、不同 gadget 的点不合并，所有边端点不同，无自环、无平行边。冻结稿页3明确困难性归约除 multi-outerplanar 外用简单图，页16–17给出本构造和二部划分；原平面嵌入经变量局部替换、special 局部附着保持平面。0出现变量可先移除，空子句可直接处理；不影响标准非空子句 Planar3SAT 困难核心。

双向 gap 的承重推导也已经在旧 proof 中完整付清。2k环的2k条权k边共贡献2k²出负载；成本≤k时2k点必须各由环边支付恰k，故每点一条环边外向，环一致定向，所有外部权1边只能由外部指入 special。于是 b 点固定外部负载k−1，若两条权1环边都外向就超k；a点两权k边和文字点权k、1两环边同样不能都外向。变量环每点最多一条环边外向，环边数等于点数，故全环一致定向，给一致真假赋值。真文字环负载1，假文字环负载k。满足赋值时每子句选一真文字边指入子句、其余k条边外向，真文字负载至多2≤k，所有点≤k。反向成本≤k迫每个k+1条权1边的子句至少一文字边指入，该尾文字只能真，故满足公式。整数性给不可满足时 OPT≥k+1。固定k=2后全部数值只有1、2，YES≤2、NO≥3；这不是只剩随输入增长的数值阈值的 PARTITION 归约。

建立显式处理矩阵：机器V(G)，任务E(G)，p[v,e]=w(e)当v∈e，其余∞。每件恰有两个不同资格端，两端同正权1或2；每机资格数等于原度≤3。取向的任务给尾端；调度的任务若给u，恢复为u→另一端。两方向互逆，逐机负载、任意方案峰值及OPT都保持。Page按入边计负载只需全弧反向，不能把入出约定误当不同模型。矩阵或稀疏资格清单输出均多项式。Page允许单资格任务/loops与多图的更大模型，不要求本归约也产生loops；本归约使用合法的简单无自环子类。

交叠图是L(G)，并非原机器图G。若简单三角形自由G的线图出现三角形，其三条原边两两相交；无共同端点将组成原三角形，故必有共同端点。一个线图菱形含共享一条线图边的两个三角形，即它们共享两条不同原边e1,e2；简单性使e1,e2只共一个原端点v，两个三角形必须都以v为共同端点，迫四条不同原边接v，违Δ≤3。该证明允许菱形额外两端相邻，故排除普通子图，强于无诱导菱形。二部性给三角形自由；所有桥条件均已付清。不能删简单性或Δ≤3条件，也不能把“平面二部”直接当作diamondless：K1,4的线图K4包含菱形子图。k≥3时本构造b/子句度k+1≥4，同样不能推广本桥。

若固定c<3/2的近似存在，YES输出≤2c<3，NO任一合法调度≥3，检查输出是否<3即可判原公式。严格小于号不能写成≤3/2；它不排斥目标已有3/2匹配算法。源精确强困难性与本固定2/3 gap都得到保留；弱 PARTITION 仅给精确NP-hard，不能代替这里的固定常数近似 gap。

判定：**whole**。源的k=2实际归约与负载/线图桥完整推出目标；旧边无需补新假设、降级proposed或缩为contribution。旧 proof `planar-bipartite-k2-to-diamondless-proof.md` 的完整数学仍有效，可按原SHA retained，并在新review明确其“当前v2”是历史时点。旧边本身因源全文和endpoint pin过时须replaced。

## 777：安全精确 MMO DP 到等时双端 FPTAS 的局部贡献

旧任务 `unrelated-machines-3a-3a-777902a1e6f15125`，core 为 M20c5…，read 为 M14dbe…。当前M20 v4明确给简单图安全平方表时间，并在model/body另付平行边逐边引入扩展；不是只剩未经证明的原印快指数。目标M14除了算法，还包括一般资格、不同端时长和独立弱NP-hard结论。故该迁移只能是目标算法半部的等时双端子域 **step/contribution**，即使本子域的FPTAS已完整证明也不能升whole。

对每件原作业保留身份e_j={u_j,v_j}，其正整数权w_j等于两端相同处理时间；恰两个不同端，故无loops。同端点对的多个任务是不同平行边，不能合并成一个作业。尾端指派双射与623相同，所有调度和取向逐负载对应。支撑简单图就是dual机器图；incidence则是每件作业细分机器边得到的二部图。若输入给宽τ的incidence分解，选每任务的一端u，把该任务点在全部袋的出现替成u并去重。任务袋子树和原u袋子树因某袋覆盖资格边(j,u)而相交，替换后的u出现连通；另一端v与j同袋处变成u,v覆盖dual边。袋不增大，所得dual宽≤τ。这个收缩只合并任务和一端机器，不合并两台机器，重复边可在支撑图忽略但保留作业记录。不能把primal作业交叠图的分解直接交给同一个机器负载DP。

旧边已经给出正确且更直接的网格。非空时令W=max_e w_e、d=max_v incident任务记录数≥1、ε0=min(ε,1)、q=ε0 W/d、a_e=ceil(w_e/q)。每件必须全部落在一个端点，故W≤OPT。对任一取向和任一点，出边至多d条，因此

`load_w(Λ,v) ≤ q load_a(Λ,v) ≤ load_w(Λ,v)+dq`。

令Λ*原最优、Λ_a缩放精确最优，得到

`C_w(Λ_a)≤q C_a(Λ_a)≤q C_a(Λ*)≤OPT+dq=OPT+ε0 W≤(1+ε)OPT`。

并且a_e≤ceil(d/ε0)。令ε0=u/v，a_e=ceil(d v w_e/(u W))由整数除法完成，操作数位长为输入/精度编码长度的多项式；原W不会作为数组长度。d≤任务总数，缩放最大权仅对输入规模和1/ε多项式。空任务先返回空调度及0；不会除d=0。正权条件下其余没有q=0分支。

安全精确DP的完整不变量：每条边唯一归属某覆盖袋，左右子边集不交；表的坐标是当前袋各点已处理边的部分出负载，表值是该子图全部点的最小完整峰值。枚举子表状态对和本地边方向，投影相加形成唯一父向量；父表值取max(左子峰,右子峰,全部父袋合并坐标)。父袋外顶点不能同时在两子树出现，否则袋连通性迫其也在父袋，故没有遗漏的共享负载。固定接口下两子最优可以同时选取实现，反向限制父最优也给可行子接口，递推双向精确。保存两个子状态和本地边方向便可实际回溯每条作业的尾端，输出的是合法调度而非仅目标数。

用N=机器数、J=任务数、H=ceil(d/ε0)避免混淆源正文n,m。简单图每袋≤τ+1点、局部≤O(τ²)边，单表≤(HN+1)^(τ+1)，显式配对给 `O(2^{O(τ²)}(HN+1)^(2τ+2)(N+J))` 次整数算术/比较。多图用nice分解每次只引入一条带身份边，试两方向，坐标≤HJ，安全界 `O(poly(τ)(HJ+1)^(2τ+2)(N+J))`。不能用简单图degree≤N−1界去计多图，也不能将同袋任意多平行边一次枚举2^J而称常数。整数负载与表值位长O(log(HJ+1))，父指针/比较/整数和的位成本另计，均多项式；输出每任务一台机器需要O(J log(N+1))位。给定宽τ分解直接用；未给时采用冻结两primary均明确引用的固定宽度构造，计其费用。固定τ下分解二叉化/nice化与逐边插入的poly(τ)费用均多项式；不声称重新证明外引分解文献。

Asahiro页13完整Cmax递推已经有父坐标最大项，问题在于其从一张表大小直接断言单节点时间，未支付两个子状态的配对。因此只认可当前M20已付的平方表指数；原声称 `O((kN)^(τ+1)J)` 是未付加速实现义务，既未被本FPTAS使用，也未被证明不可能。结构论文dual/incidence的Lemmas13/15原式则确实漏父活跃负载；正式audit反例和加项修正已付清，或可用在forget-machine关闭完整负载的closed-max定义。本边旧解释准确区分二者，无需再次改共享来源。

### B_min 接口的独立核查，不替换旧 W/d 证明

为核当前一般算法来源的 cap 合同，另读ea3c/9a5cd成熟路线。令n=任务数，每任务放到最短有限端，得到实际合法调度峰值B_min。其 `OPT≤B_min≤Σ_j min_i p_ij≤nOPT`，不冒称B_min≤2OPT。正非空时q=ε0 B_min/n²，a_ij=ceil(p_ij/q)，K=floor(n²/ε0+n)。原最优每机至多n件，整数缩放负载≤OPT/q+n≤n²/ε0+n，故≤K。每个partial load是最终非负子和，join只相加不重复贡献，故cap不会删保留见证；坐标集合0..K有K+1值。精确回溯σ_a给 `C_p(σ_a)≤q C_a(σ_a)≤OPT+nq≤(1+ε)OPT`。整数式ceil(n² v p/(u B_min))保多项式位长。

这套一般资格算法用M247的任务flag/机器load状态：引资格边至多选择一次，忘任务要求恰1，join任务计数相加≤1且机器负载相加，忘机器检完整负载/关闭峰值；任务与机器共同出现的incidence分解有自己的状态，不等于MMO原机器DP。dual资格机器团可挂任务叶袋转incidence宽≤k+1，固定k可构造分解；每固定k的总时间为poly(input,1/ε)，次数可依k。这独立验证目标一般FPTAS的当前支持接口，不把M20迁移升级成异端时长/任意资格算法。原W/d对等时双端已足够，正式repair无需换网格、加入额外对象或重写成熟证明。

独立困难性也须分工。当前canonical `um-9a5cd2-exact-load-dp-and-partition-imply-full-fptas-hardness-v5` 为 `{M247, M-e8d9614430ab49fc99125452d10388f1}⇒M14` 的whole ALL边；ea3c为M247⇒M14算法贡献。两条本轮只读check均通过，旧777的remaining准确指向它们，不是全目标尚未证明。两机PARTITION把每个正二进制数作为两机相同处理时间，阈值半总和，固定dual K2宽1、incidence K_{2,n}宽≤2；总负载迫精确半分。它支付弱NP-hard，不支付固定{1,2}权gap，也不是由精确DP自动推出。原777无需新增困难性前提或改whole，保持contribution即可。

## 旧资产与正式路由处置

| 旧任务/资产 | 当前旧字节 SHA256 | 数学处置 |
|---|---|---|
| `unrelated-machines-3a-3a-6231f96071b186d2` 的 `map/edges/unrelated-machines-3a-3a-6231f96071b186d2/k2-mmo-gap-to-diamondless-job-hardness.json` | `dbae92909268536ae25d26b09493dd233fb7682584b23bbc4159afa1ff857e98` | 同edge_id、whole完整保留，新绑定资产replaced |
| 同任务 `map/edges/unrelated-machines-3a-3a-6231f96071b186d2/planar-bipartite-k2-to-diamondless-proof.md` | `d9ad5dd8c4b1d2f46ed93eb18d01dac25fb516acada99a73ad2553bfa057ba21` | 证明可retained原路径/原SHA；新review解释历史版本语言 |
| `unrelated-machines-3a-3a-777902a1e6f15125` 的 `map/edges/unrelated-machines-3a-3a-777902a1e6f15125/orientation-dp-to-two-endpoint-fptas.json` | `0c1f7dbadd9f7567eea7bd9bfde3def20b2e35344de9ddfe8e3c53ed89d2ac5e` | 同edge_id、W/d网格与contribution保留，新绑定资产replaced |

旧623 task为done/Boss5，旧777为done/Boss2。两边当前都不在registry.edge_files，但integration.pending仍定位到它们；只查canonical会漏掉真正待办资产。初次全任务扫描未发现supersedes任一旧任务的正式repair；`boss5-asahiro-sha-current-repair-16bd7e5e49c5be05` 已done/Boss1，仅替代351693…的三条PARTITION/MultiOP/simpleSP/未知target关系，不能冒作本两条repair。M14的ea3c既有repair也只修其独立一般算法来源，不替代旧777。Boss随后可能发布native map-draft定向修复，末次观察精确task ID/state/owner及新资产SHA（若已存在）均写随附JSON；未知值保null，不猜任务ID或输出SHA。

末次扫描确认777已有正式路由 `boss2-wave4-root-repair-5da342428ed683bc`，状态claimed、owner为Boss2，其definition明确supersedes旧777且本范围两对象input pins均current；尚无同edge_id新资产，不应重复派repair。623末次仍未见superseding任务，最小动作是Boss对623旧task做native map-draft --repair-task并按当前core/read pins plan。正式接续均保原edge_id及数学语义，更新Asahiro evidence/evidence_pins到3fe059…、Maf/M20 endpoint_pins到上表、当前reviewed_by/review_note与review_digest。623旧Maf pin32b8ba…→3d006e…，目标pin不变；777旧M20 pinef93b3…→545e9a…，目标pin不变。623独立proof原SHA retained，其余旧边分别replaced到新收据内真实replacement_paths；只有新任务实际done才作supersession，之后assemble纳回有效关系并由Boss准确关闭pending。本审查不写integration，亦不把建议路径当已经存在资产。

本范围无剩余数学缺口或必须新发的研究follow-up。未付原印更快MMO join的实现属于既存明确开放义务，不阻塞这两条关系的恢复，也不因本次新造重复任务。实际必须续办的是两条正式版本修复的发布、认领、重绑定、收据supersession与集成；Boss负责队列及写入。
