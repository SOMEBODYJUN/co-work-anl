# 最终中文 canonical：逐块实际全文审查记录

日期：2026-10-18。角色：原 Exact-first 独立攻击者，在作者 Proof read-after 及 root 释放最终中文 canonical 后进行的最终正文准确性审查。本轮不是 blind review，不增加一张盲审票。

## 0. 裁定、精确身份与保护边界

**裁定：对下述最终精确字节版本实际阅读全文，未发现 fatal。当前 canonical 的三项 formal ID、算法数学规格、承重证明、常数及 C–F 范围与已审 v5 Exact/Author Proof 一致。** 审查过程中指出的一处非 fatal 空 residual bundle 表述省略，在最终版本已显式补齐，见第 6 节；当前没有因此留下待办。

本轮唯一新增读取的数学正文：

`/workspace/scratch/038d9dcc4cac/explicit_xos_fractional_nsw_and_normalized_robust_gap_boundary_canonical.md`

- **本记录最终绑定的实际 SHA256：`2365f54091786596e75cac20456caaf61cdf607664ba5cf2bd995de6963c6c81`。**
- 最终实际 byte count：40,345。
- 实际行数：651。
- 实际权限：0444。
- 首次释放版为 40,243 bytes / 651 lines / SHA256 `a12af1ccabac09415d48061d4ff80d24a67b67a9e4062d01c5627f2d6db9821b`，四块未截断显示并实际逐行阅读：**1–180、181–360、361–540、541–651（EOF）**。随后仅对同一文件用 `rg` 抽取全部三处 Markdown links，核对其字面 routing；没有打开 links。
- 初稿 review 尚未冻结时，最终身份断言发现同一路径已修订，断言在任何冻结操作之前停止，没有误报旧 review 已冻结。对当前 `2365f540…c6c81` 版本，我又以三块未截断显示，**重新实际全文读完 1–220、221–440、441–651（EOF）**，没有只看新 SHA 或仅看差分。
- 另在内存中从最终版去掉第 394 行新增的 102 bytes，实算重构旧版 hash 恰为 `a12af1cc…9821b`，确认两版本唯一字节变化就是显式 outside-A′′ empty convention；没有写出另一份 canonical，也没有新增读取其他路径。

这不是用 whole-file SHA 代替正文审查。下面分别记录 header、共用计算、三 formal IDs 的各字段、B1–B6、C–F 和末尾 source/scope 的实质核查。

受保护的旧记录不改：

- Exact-first：`sol_nsw_v5_exact_first_attack.md`，SHA256 `a900867a462b030db5cb2556f68f992b89efce28936a5c2658b13aeb03d7d306`。
- Author read-after：`sol_nsw_v5_author_read_after.md`，SHA256 `d70dcc172cdaafaf32ba7cdc842d967d0e8289666fcf77d977a3a94506a0d1cb`。

本轮未新增读取任何其他 canonical、旧 rank、tool reviews、旧版本过程、linked review/source PDF 或证书页。没有仓库/Git/Work/推送/外部通信或 token 操作。本记录不认证 root 的未读历史来源账；root 将其另记于对应 review。

## 1. header、Status 与对象身份

实际读过正文第 1–5 行。header 明示数学证明完整、算法未实现、外审与全球新颖性未认证；给出的 Exact SHA

`3160d7f7dc3265c7753ba558bb6cd21fe58fc5e2ea84562d2558ee852701154e`

与我此前实读的 v5 Exact 相同，Author Proof SHA

`2989351ca6ab45779fecb3c4a4ccefbae2044cdcce7ad3f3fab0d0e2ce55a1af`

与我此前四块实读至 EOF 的作者全文相同。它没有把作者 informed reconstruction 或此轮 canonical 审查重新标为 blind。

第 5 行的范围概述与正文一致：A 为一般单调次可加的 semantic fractional matching；B 是任意有限显式非负 binary-rational XOS 的无权 NSW；C 是原 normalized 菜单的几乎所有组；D 仅同组 singleton REPAIR；E 保留所有原 jobs。最后一项只给全矩阵 makespan≤2 和 selected-root 例外计数。没有在 header 偷换成全部 machines 的近二以下保证。

## 2. 共用有限位计算（第 7–35 行）

正 benchmark 的定义、原物品列容量、重复条目不复制原 item、binary rational 存储均与 v5 一致。

真 product matching 的 gap：n 条 factor 的 product numerator/denominator≤2^(nL)，两个不同 products 的 cross-product integer gap≥1，故 log gap≥G=2^(−2nL−1)。每 edge log absolute error≤G/(4n)，每 matching sum error≤G/4，足以保留全部不等 product 的次序。先删 zero factors，测 covering matching，再对 rational approximate weights 求 exact maximum weight，确为 true maximum product。

正 rational 缩放至 [1,2) 后的 odd-power log series，t≤1/3，tail≤9^(−N)；ln 2 同法近似。e 的大小受输入位长控制。当前文本保留了所需 absolute precision 与 total-bit-polynomial 关系，不含 exact symbolic logarithm oracle。

**核查结果：PASS。** 共用引理适用于 A 的 H、B1 的矩形 U 端以及 B6 的 actual bundle-plus-singleton factors；没有把比较 benchmark 的无理值作为算法输入。

## 3. 三 formal IDs 的全部明列字段

三处 ID 的名称分别是：

1. `UM-FRACTIONAL-BENCHMARK-REMATCHING-v1`。
2. `UM-EXPLICIT-XOS-DETERMINISTIC-FRACTIONAL-NSW-v1`。
3. `UM-NORMALIZED-MENU-ALMOST-ALL-AND-REPAIR-LP-BARRIER-v1`。

逐个核对了 Objects、Domain、Quantifiers、Dependencies、Limitations，以及随后的 Exact/证明。以下不是只核 ID 名称：

| 字段 | 第一 ID（第 37–99 行） | 第二 ID（第 101–497 行） | 第三 ID（第 499–641 行） |
|---|---|---|---|
| Objects | n、真实 U/H/B、rational V/c、finite y | n、m≥0、finite indexed XOS clauses | 同一 n groups、m≥1 resources、total-one indexed states、指定 repair 与其原矩阵 |
| Domain | 一般 finite monotone subadditive、v(empty)=0，可 value queries | 任意显式非负 binary rational；零/duplicate/零总 clause 允许；无 global grid/normalization | 原 clause sums=1；零/unused/duplicate 允许；计数分母始终 n |
| Quantifiers | 全部 feasible fractional residual families；inactive residual value=0 | 同一个 deterministic output 同时比较每个 positive finite y；unweighted | 每个 feasible FSLP 对象、每个 fixed η；repair 的 fixed slack 与小 δ_q |
| Dependencies | 页内运输/Jensen/Hall/permutation 与有限位引理 | A、标准 LP/matching、明确 DLRV inherited framework，替代环节页内证明 | 前两 ID、positive-support FSLP、直接 job-by-job schedule |
| Limitations | 不验证 A2、不求 targets、不解一般指数 log-CONFIG；不可换成 integral-only premise | 非 weighted、非一般 SA backend、非 oracle-only；无已实现软件认证 | 非 all-group max-min、非所有 machines 的 2−epsilon、非 general UM/source hardness/其他 dummy/SC；NP 条件推论 |
| Exact/证明 | A.2 及 A.3–A.4 的完整证明 | B.1 及 B1–B6 全链 | C–F 的 unit witness、计数、repair LP、完整 schedule 和范围 |

第三 ID 的 Quantifiers 清楚区分 δ_q 与 B 的 δ_m=2/35，D 中又使用 a_rep，避免把 active-agent 数 a 或 mask 概率读成 source threshold。

页末把 Evidence、Counterevidence、Status、Related Files 分配给正文、各 ID 的定义/限制与所链 review 共同承载；当前页内数学内容和局限已经实读。对应 linked review 尚未打开，本审不对其将来的实际内容或旧历史账代签。

## 4. A 与 B1–B3

### A：新 fractional matching 不是 integral OPT 的换名

第 60–99 行保留完整构造：每个 H-nonempty positive config 送到其中最大 singleton 的真实 h，row/column deficits 运输填满，inactive 行不可能有 H-empty positive config，故所有使用 factors 正。将 y 投影至 B 是 feasible **fractional** family，因此 A.1 真的可用；expected H-cardinality≤n。positive ratios 上 Jensen 得 log benchmark bound，再以正边 Hall/permutation decomposition 得 matching。

不需要 H 最优；H 只要有 n 个不同真实 items。算法只最大化给定 V 加 singleton 的 factors，不验证 global premise。empty A/B、zero singleton/V、重复配置仍包含。**PASS。**

### B1：总分支

第 126–135 行的无 positive matching Hall argument 同时排除 positive actual allocation 和 positive fractional benchmark，故返回 all-empty 与 OPT NSW=0 相符。正分支 τ 明确在**全部 U** 上 true maximum positive singleton product，满足 B6 的实际 source 条件；不是只在选定 H 上最优。empty residual/inactive 全部直接分支明确。**PASS。**

### B2：全 fractional 量词、终止及固定 vertex 位长

第 139–213 行只在内部把 residual rows 除以 W_i，固定 λ/z polytope 的 constraints 不变。任意 fractional family 选 attaining clauses可 lift；threshold recovery 保持 marginals，actual expectation≥assigned-clause utility。final Vhat≥x 正好给对任意 family 的 B.6，不只是 integral allocation 或 recovered family。

ell=1/(4a)、h=1/(32a²)；M>2a 时 gradient dot D>a/2；Hessian 与坐标 lower bound 给 progress>1/(128a)。F 初值−a ln a、上界 0，更新数<128a³；a=1 起点停。没有计算不可表示的 exact potential。

P 的 0/±1 matrix 与 objective 无关；Cramer/Hadamard 给固定 vertex bit bound。lex optimal-face 取点仍为原 P 的 vertex，common denominator 每轮只添加 fixed-bound denominator 与 h/a 的 polynomial bits。固定 utility coefficients 再求 x 和 reciprocal，不形成 objective-length 递归放大。**PASS。**

### B3：支持内实际 welfare

第 217–248 行的 threshold exceedance sum≤1 源自 item capacities，单个 item 上跨 agents 独立给 union bound≥s/2。有限 bid levels 求和给 proxy expectation≥q/2。strict CDF formula 正确处理 ties；exact rational conditional expectation 固定配置不减 proxy。positive winners 来自其 chosen support config，actual XOS≥chosen clause，故实际 bundle 是原支持集子集且 disjoint。q=0 有直接返回。**PASS。**

## 5. B4–B6：split、全局 masks、数值与 rematching

### B4

第 252–308 行保留 alpha=V/3−ν≥V/6、attaining weights≤ν、greedy extraction、actual trimming 单次损失≤ν。k≤|T|/2 防止 reciprocal-scale expansion。高值 contribution≥2V/3，floor(r)≥r/2 使 inherited mass≥1，按行 normalization 不放大 marginals。

normalized actual values≤6，总和≥q/d，δ_m=1/(7d) 逼出每轮至少 ceil(δ_m q) 离开。所有 S_i、rounds、attaining clauses 先于 labels 固定；rank probability lower bound 与有限截断 0 label 均正确。**PASS。**

### B5

第 312–429 行仅 floor 已固定候选的 relative weights，Q=210m_B，loss<1/210=δ_m/12；auxiliary total≥δ_m/12、≤1，每项≤β。原 valuation/state/resource/processing time 未改。

shifted inverse moment 的 convex chord 方向正确，独立 Bernoulli 得 E[t^Y]≤exp(−μ(1−t))；积分给 E inverse<1/M，再用 log Jensen。只要求同候选不同 items 独立，未错误要求不同 agents 独立 masks。

DP 用 0,…,Q 整数格与 common probability denominator；positive prefix labels 不改变其余独立分布。log table error 1/(2a_0m_B)，每 child score error≤1/(2m_B)，选择 approximate minimum 每步误差≤1/m_B，总 error≤1。全部 bit bounds 与 ops count 仍 polynomial；没有按 tiny β 或 probability reciprocal 展开。

一个 original item 只有一个 global label，跨 agents 若同留则 round 相同，与同轮 candidates disjoint 矛盾。包括 retained zero-weight items。B.23 支付全部 error 后为 `12e^(1+1/a)/δ_m²≤12e²/δ_m²<200/δ_m²=9800d²<10000d²`。**PASS。**

### B6

第 433–497 行的任意 comparison π 允许 zero edges。Eτ 图中删除每个 N outgoing edge，使含多个 N 的 cycles 也切成终止 N 的 disjoint paths。逐 path 单独用一个 residual maximizer 构造合法 alternative to global τ，获得 product inequality；不同 paths maximizer 可重复，因为并非同时分配它们。

Eτ 用 τ、Eπ 用 π 无冲突；外部由 W>0 保护，右 product zero 直接用 τ。final σ factors 用 original actual values，τ 保证 positive feasible matching。三个 agent 区域的 ratios 分别≤2V/(b+ν)、≤6、=1；A′′ empty 不用 empty geometric mean。sum-to-max factor 3、A 的 c+1=3 都已保留。

numeric identity `60000·3·(5/2)²=1125000` 正确。canonical 选择保留 v5 B20 已证明的第一界 1/1125000，而非 reserve 后的更弱界；这没有增强到新对象或偷吃精度预算。**PASS。**

## 6. 过程中发现并已消除的非 fatal 表述省略

首次 `a12af1cc…9821b` 版本第 394 行在 B5 写 `T_i={j∈S_i:r_j=t_i}`，S_i/t_i 仅对 A′′ 有定义；当 A′′ 非空时，该句没有同时重申“i∉A′′ 时 T_i=empty”。第 308 行明确的是整个 A′′ empty 分支，第 135 行明确的是 A empty 分支。随后第 475 行已按 A\A′′ 的 b_i=0、A 外 V_i=b_i=ν_i=0 使用，表达的正是这些 agents 无 residual bundle。

我在该版本上将其判断为可更显式的算法约定，**不是 fatal，也不是结果依赖未证明的新假设**：对于没有固定候选的 agents 直接取 empty，是现有构造的立即确定性完成，保持所有 item disjointness 与后续 inequalities。已审 Exact v5 B5 与 Author Proof §6.4 都明确给出该 empty convention，原页第 475 行的 intended convention 也相容。

我向 root 指明定位后，在冻结 review 前发现 canonical 已更新。**最终 `2365f540…c6c81` 版本第 394 行已实际写明：对所有 i∉A′′ 一律置 T_i=empty，包括 A′′ 非空的情形。** 我没有修改 canonical；我实际重读最终全文，并通过内存重构旧 hash 核定这就是唯一 102-byte 改动。该改动是把既有 Exact/Proof 的定义补显式，不改变结论、对象、常数或复杂度。故最终版本的这项表述问题已解决。

## 7. C–E 的全部原对象及严格计数

### C

第 501–561 行的 normalization 是原 table clause sums=1。正 support value 恰一，positive-support indicators 的 FSLP λ 给 benchmark 一。所有 original utilities≤1，log-CONFIG inequality optimum=0。item-equality 填满用 available mass n−c≥1−c，只加当前 item，row/其他列不变；monotonicity 与上界一保持 value one。没有把这个 fractional witness 误说成 unit integral allocation，也没有新 exponential solver 声称。

B 的 1/1125000 足够给 C 的 1/3000000>2^(−24)。K=ceil(1/η)、q_eta=ρ^(−K)、c_eta=q_eta/2；k≥ηn 个严格低于 q_eta 会使 product<ρ^(−n)，与 strict NSW lower bound 矛盾。≤c_eta 严格落在 <q_eta 内，含 equality boundary、ηn 非整数。variable η 只承诺 polynomial(K,input)。原 attaining state 总从 unfloored table 恢复，demand formula 也是原 coefficients 的 finite max。**PASS。**

### D

第 565–589 行保持同一 n groups，D distinct repairs 全局共享，每组 D singleton alternatives，其他系数零/absent。D1 给至多 D 未满足组不同 repair；D2 投影回原 U，最多 D groups 收 repair，故至少 γn−D bad groups 保持 bad。

YES 全体 unit allocation 的 attaining total-one positive supports disjoint，所以 integral λ witness。NO 若 augmented FSLP feasible，C 低组数<ηn，与 `(γ−a_rep)n>ηn` 矛盾。算法仅 rational LP feasibility，不需执行 NSW finder 或求未知 integral OPT。fixed slack、same n、explicit nD size、D=0/large D 的边界、promise 外允许任一 outcome 和条件 Karp 推论均正确。**PASS。**

### E

第 593–608 行完整保留每个 indexed state 的 root、每个原 resource machine、每组一个原 selector、每个独立 incidence identity。selected state 的 allocated positive incidences 去其原 resource，其余留原 root；每个 unselected state 的全部 incidence 留自己的 root。显式 zeros 留 root，以原 private time 0 执行，未删除。

selected-root load=2−r_g，unselected-root load=1；全局 disjoint allocation 使每 resource≤一个 unit incidence。故全部原 matrix makespan≤2；仅 selected-root 超过 2−q_eta 的数目<ηn。unit case 的完整 schedule makespan≤1，selector lower bound 给 OPT=1。

S+m machines、n+I jobs 的 I 包括对应对象全部显式 incidences。repair 精确增加 nD positive singleton incidences，另行显式 zero incidences 也计入；它没有声称所有表示下总 job increase 都只能为 nD。selector identities 仍是 n，新增 selector endpoints nD。所有旧/新 repair jobs 均保留，dense output polynomial。**PASS。**

## 8. F：条件源域不被夸大

第 612–622 行由 bounded utilities 与 product lower bound 得必要式 `γ ln(1/δ_q)≤lnρ`，δ_q=0 单独由正输出处理。明确 γ 可以依赖固定 target δ_q，不能推出 source-size γ→0 或辅助规模必须随 source size 增长。

第 624 行仅作条件 decoder 数量核对：若在 threshold x≥δ_q 时 b≥x 可以解码至少 xn 个满足 NO 全条件的 bundles，而 NO 禁至少 γn 个，则直接 x=δ_q 的 contradiction 需要 γ≤δ_q；一般至多取 x=max(γ,δ_q) 得相应 bound。它没有把未审的旧 decoding/source 条款当作本页定理。

第 626–641 行明确 C/D 的排除域为 `δ_q≤c_eta<η<γ`，所以不覆盖所述 γ≤δ_q regime；在该 regime，`γ ln(1/δ_q)≤δ_q ln(1/δ_q)≤1/e<lnρ`，F1 自动满足。这里 c_eta<1/K≤η 正确。δ_m=2/35 与 δ_q 始终不同。

因此本页没有声称已经挡住实际主源，更没有解决 main near-two UM 命题。对“典型 source”的措辞，本审只认可其被明确条件化的参数比较；未新增审计任何具体 source/需求树/解码，就不替那类历史事实背书。第 641 行列出的 source、联合量词、解码、证书保持、schedule 关系等未解义务继续保留。**PASS，范围严格限于条件比较。**

## 9. source 分工、历史与链接字面 routing

第 643–651 行已全部读。DLRV §2.1–§2.5/Appendix B 的 inherited matching/splitting/iteration/rematching template 与我先前实际所读 primary 范围相符。当前措辞只说不能把 actual-integral-OPT theorem **直接换成** fractional theorem，并由页内 A/B 推导给新 guarantee；没有声称“原作绝无 A 类型结论”或据此认证全球 novelty。

英文作者稿编写者的 supplied-text full read、未读 PDF/其他 audits 与 boss11 的原文/选页渲染范围明确分开；后者归未打开的 review。我仅检查这种角色区分，没有代认证 root 的旧来源账或未读文件。旧版本历史段落是披露的版本边界，不是本次新增对 v1–v4 的独立实读。数学证明也不依赖那些历史非存在断言。

三处链接只核字面，不打开目标、不验证尚未 materialize 的文件：

| 位置 | 字面 href | routing 含义 |
|---|---|---|
| header | `../../reviews/unrelated_machines/explicit_xos_fractional_nsw_and_normalized_robust_gap_boundary_review.md` | 当前 canonical 所在目录向上两层后的 reviews/unrelated_machines，同 stem review |
| source | `../../../history/source/literature/unrelated_machines/dobzinski_li_rubinstein_vondrak_2023_subadditive_nsw_v1.pdf` | 当前 canonical 所在目录向上三层后的 history/source/literature/unrelated_machines，明确 v1 PDF |
| 对象接口 | `normalized_menu_configuration_certificate_preservation.md` | 同目录既有 normalized-menu 配置证书页 |

三个名称、相对方向和 v1 指定与文本所称预期角色相容；是否在实际 repo 目录中落在相应实体，由 root 完成物化和 routing 检查。本审没有用链接所指的未读内容支撑本页数学 PASS。

## 10. 最终范围与冻结

本审实际覆盖最终 `2365f540…c6c81` 版本的 header、共用有限位计算、三个 formal IDs 的全部明列字段/Exact/Proof、B1–B6、C–F、source-role/版本/复用边界及所有三个链接字面。结论是当前精确字节版本没有 fatal，与已审 v5 相同对象和常数；第 6 节记录的 residual-empty convention 已在最终字节版本补齐，不是未解决的条件 PASS。

前两份冻结 records 不改；若 canonical 字节再变，本记录的 SHA 绑定不能自动转移。main/push/registration 不增加数学真值，不把 source regime γ≤δ_q 变成被排除域，也不替代主目标的未解义务。

**软件：none。算法仅为数学规格与 total-bit-polynomial 证明，没有 backend 实现、运行测试或执行审计；外审和全球新颖性未认证。**
