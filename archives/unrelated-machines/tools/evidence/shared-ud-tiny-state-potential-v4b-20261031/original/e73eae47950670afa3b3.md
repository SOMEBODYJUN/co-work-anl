# Shared-UD v4 追加稿：知情全文实读与量词扩域审

审者：`/root/sol_nsw_independent_attack`，2026-10-18。结论：实际读完指定 v4b 全部 204 行并重新核算两个新分支，未发现 fatal。支持的数学范围是 k=1 无额外 tiny 限制、k≥2 时 ν≤1/(16384k²) 的本页 typed Q-alone deterministic 19/10；不签一般 UM，不认证软件或全球新颖性。

## 1. 实际身份、顺序及没有读取的内容

本次新增本地读取仅 `/workspace/scratch/038d9dcc4cac/sol_general_repair_shared_ud_tiny_state_potential_canonical_append_v4b.md`。实际 SHA-256 为 `1e3710870c8fbef4d4235cf2f90fe2d8ec6ca84b99ec6cd234464cc9d260df44`，22847 bytes、204 lines；按 1–105、106–204 两块真正全文读完，没有截断，覆盖 §12–20、§14.1 及全部 metadata/source/software 文字。

真实先后为：旧新 k⁴ Exact `80fd4ff5…` 全文读取 → 冻独立 Exact-first `ee7f19b141ced5d231bfa22229473b644306782e15ff700f79fee4315edc2d90`（171 行）→ 父 agent 实际全文读该票 → 释放作者 Proof `409ce884…` → 我实际读其 1–164 行并冻 read-after `e4ad54e800e8f349e4cd451118e5d78582b4341e07075825e44c67afa4e41369`（117 行）→ 父 agent 实际读该票 → 本次完整阅读 v4b。两份先行记录没有改字节。

父 agent 送审时已经告知 k² 扩域及 k1 submodular greedy 的机制，因此本票是知情作者稿/量词扩域审，不是 fresh Exact-only blind，不冒充另一审者尚未完成的独立票。我的 ee7f19b dual 强凸势路线只先行证明了旧 k⁴ 域；它不自动覆盖这里的 k² 域，也没有拿它来填本稿证明。

未打开 v4 新 Exact、v3 Exact、其他审者草稿、任何新 working note/self-audit/code/run/links，也没有向 fresh reviewer 传机制。未读取或改动原 175 行 v1 prefix；这里不重新代签 prefix。此前我确曾实际读过其 `84d603…` 原件，但本票只针对新增 204 行。本轮也没有 repo/Git/Work/token 操作。

## 2. 正式字段与新旧对象分离

§12 的新正式 ID 是 `UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-19-10-APPROX-v4`。Objects/Domain、Quantifiers、Exact Statement、Assumptions、Scope、Conclusion、Dependencies、Evidence、Counterevidence、Status、Related Files 都已实际阅读；没有把旧 v1 的 SA1/CDF/MW/条件期望算法偷偷改成新算法。v4 的两个分支只共享 typed 输入、实际值桥和真实 helper/home 恢复。

§13 明确所有 normalized 菜单非空、single-state outers、全局不同 homes、每 home 唯一 unit-own helper、任意 normalized B-only fallback、任意多 B-only leaves；每叶用固定 ε=15/16 和整菜单 E_l 检查 b_l<ε。原零 incidence 可以列在任意原资源，资格度只按正支持；indexed duplicate states、inactive payload、unused resources 全保留。没有把本域 recognition from arbitrary P 当成算法义务。

新 bound 关系正确：k≥2 时 new/old 上界比为 k²/4，故 k=2 与旧 1/(4096k⁴) 相等，k>2 更宽；k=1 完全解除旧 tiny 条件。旧无额外叶输入以 leaf 集为空嵌入；未发布 v2/v3 仅历史字节，不凭这次签票追认其算法、量词或审查身份。

每原 state 独立 private、每原 resource 一机、每 group 原 unit selector、每 listed incidence 的 private 系数与 resource unit time 构成完整 ordinary P。S+U machines、G+I jobs、S+2I finite endpoints 与全文一致；即便展开稠密矩阵也为显式 input 的多项式。

## 3. 实际值、叶判别与固定 profile 的 oracle

§13 的 OPT=2−V、1≤OPT≤2 仍是实际 allocation ↔ 全部 ordinary jobs 的双向桥。反向 C<2 只使用 selector 所在 state 的导出价值，允许原 schedule 有 inactive exports；正向重新路由全部 payload，包含每枚 zero job。叶 value≥ε iff bundle 遇 E_l，是原菜单值的 exact iff，并非说每个 leaf state 本来是 singleton。若无覆盖叶的 matching，实际 V<ε，全部 jobs 基线 C≤2 的比值<32/17，可靠分支闭合。

有全叶匹配时，resource-side transversal T 的 rank 是叶数，vacancy M=T* 满足 D independent iff B\D 可匹配全部叶；“full rank”在此应理解叶侧已饱和，不是误设 rank(T)=|B|。空叶、空 B、rank0、loops、unused resources 都保留。

§14 的固定 helper profile 只选一个原 fallback 或 empty，后者最终回原 own，并不新增状态。helper claims 没有数量下界，完整叶 matching 与资源容量一给 integral network。每个合法 profile 的 Q_j≤1、W_i≤1；多-option 辅助集合只用于次模 inequality，不把这个 bound 不当地套到同时多state的真实 helper。

给正 λ，令 t_u=max active λ_i(j)w_jp_jsu，f_λ=Σt_u−mincost 全叶 matching 费用，确实可由 ordinary matching 精确算。option blocks 在 parallel matroid copies 上不相交，threshold weighted rank 给 monotone submodularity。实际 V≥ε 的共同 comparator O 用实际外层拿 home 的 helpers 的 fallback states，福利每 outer≥ε²；叶从其原 bundle 内保留一枚 E_l 资源，所以与 helper bundles 仍不交。O 只在反证进展中出现，不是给定点或算法 oracle。

## 4. k=1 新分支：固定 helper 顺序 greedy，完全不需 tiny

我重新推导 §14.1，不用 k⁴ 票的 tiny-rounding 结论。固定 λ=1，f 是以上 integral matching welfare，f(∅)=0。按输入 helper 次序，每步仅枚举当前 helper 全部原 fallback states 加 empty，选择最大 f 的 option。future helpers 都为空，所以每个当前集合是合法 partial profile，oracle 普通匹配即可。

对任意 target profile O，单调次模性给 f(O)≤f(G)+Σ_j[f(G+O_j)−f(G)]。由于 G_(j−1)⊆G，第 j 个 final marginal 不大于 f(G_(j−1)+O_j)−f(G_(j−1))；greedy 的精确选择又不小于这个值。各步 greedy gains 和为 f(G)，故 f(O)≤2f(G)。固定处理 blocks 的顺序不需要额外对 helper 本身做全局贪心；每步重新匹配亦不破坏集合函数 proof。

最终再算一次 integral optimum，连同全叶 matching，得 W=f(G)。若 W<1/4，则 f_opt≤2W<1/2<ε²，所以不能有实际 V≥ε；baseline 分支可靠。若 W≥1/4，原 integral matching 中每 helper Q_j≤1，Good 阈值 q=1/10 给 home mass z≥(1/4−1/10)/(9/10)=1/6>q。直接执行 §19 的真实恢复即可，无 prefix、无 ν 损失，也没有用 1/(16384k²) 或 ν≤1/4096；ν=1 合法。

算法总 matching 查询数至多全部原 helper options 加一个最终优化，cost 由输入 w_jp_jsu 构成，次数和位长均 polynomial。helper 无 fallback 时 empty 仍可选，重复 options 只固定打破 ties。k1 分支不调用 FW、fractional potential、target O 或子程序的 exact optimum finder。

## 5. k≥2 新曲率：逐式核算量词扩域

§15–18 的 primal potential 常数仍为 c=5/16、θ=1/32、ξ=1/(2^20H²)、τ=1/(2048H)、w_stop=25/128。θ 是 potential floor 参数，与最后 q=1/10 不混用。same-profile optimum 的 gradient λ_i=θ/k+2d_i>0 是分析变量；first-order inequality 给该任意 optimum 在对应 linear optimal face。deficit 稳定性来自辅助变量 d 的 convex quadratic 差，未要求 W* 唯一或 Φ 在全部 W 上强凹。

§16 stable exchange 仍覆盖任意给定 λ-optimal fractional point。零 dummy 保 rank，symmetric basis exchange 使删 ground 的一枚已选元素只需一个 replacement，加入新 ground 元素至多一个 fundamental-circuit swap；其他 helpers 在全删除阶段只增、全插入阶段只减。旧/新 helper j weighted values A_0,B_0≤λ_owner w_j，因此 weighted L∞≤max(A_0,B_0)、L1≤A_0+B_0+|A_0−B_0|。同 outer 的其他 helpers 已聚合在 owner gain/loss 中。任意 optimal network flow 分解成同一最优面的 integral vertices，补 dummy 后逐 basis 更新再平均，恰保任意旧点；只是存在性 coupling，不是算法 oracle。

所以 B_j=2(λ_owner/λ_min)²w_j² 及 P(A')−P(A)≥Δ_j−B_j 保持成立。state normalization 只用于每个 helper 的 A_0/B_0 bound，不要求 fallback coefficients 本身 tiny。

关键新代数已直接独立算回：Σ_{j∈J_i}w_j²≤ν、λ_min≥θ/k、Σλ_i²≤θ²/k+4θD/k+4cD，D=Σd_i，给

    ΣB_j≤2νk+(8νk/θ+8cνk²/θ²)D。

代入本次新 ν≤1/(16384k²)，得到 constant≤1/(8192k)≤1/16384；D 系数≤1/(64k)+5/32≤1/128+20/128=21/128，最后一步只用 k≥2。在 k=2 这些界正好与旧最粗界相接，k 变大不会变坏。没有使用旧 H≥const·k⁵、旧 ν≤1/(4096k⁴) 或另一 vector variance lemma。

actual comparator 和 submodular single-swap inequality 给 ΣΔ_j≥(65/128)D−287/8192，减上述曲率仍为 (11/32)D−575/16384。D≥9/80 时余量恰 ρ=293/81920。故新 k² 域仍有单 helper 改善≥ρ/H。此付款不适用于 k1，但本稿已完全分流，不残留 k1-tiny 补丁。

## 6. FW、soundFAIL 和 worst-case 总位复杂度

我实际读过 §18 的全部算法文字，不只验证新 ν 的一行替换。FW 从 W=0 与一份全叶 matching 起，每步用普通 matching 的 linear oracle，完整 flow 同步凸组合；γ_t=2/(t+2)。Φ 的 2-smoothness 和 diameter²≤k 给 gap_{t+1}≤(1−γ_t)gap_t+kγ_t²，t 步 gap≤4k/(t+2)，所以固定 N=ceil(4k/ξ)=O(kH²) 次足够。

γ_0=1 后 vertex r 的实际权重为 2(r+1)/(t(t+1))。payoff 原系数公共分母 D_1 的 bitlength polynomial(input)，因此 W 分母可取 D_1t(t+1)、flow 分母可取 t(t+1)，matching prices、gradient、Φ 平方及阈值比较仍 poly-bit。固定起点/ties/步数使 P_hat 是 profile 的确定函数，没有 free exact QP/SDP、随机请求币、随机停时或期望匹配求值。

若某 W_hat_i<25/128，其 deficit>15/128；P−P_hat≤ξ 与稳定性给精确 optimum D>15/128−sqrtξ>9/80，因为 sqrtξ≤1/1024<3/640。若真实 V≥ε，就存在 candidate 真势改善≥ρ/H，其 observed 改善≥ρ/H−ξ>τ。无 candidate 才输出 baseline，因此 actual V<ε/OPT>17/16 是 soundFAIL，而非把 λ oracle/必要 relaxation 的失败当成实际失败。

每个接受动作使确定的 P_hat 至少增 τ，其 range [-kc²,θ] 给 O(kH) moves；每轮原 fallback options 加 H 个候选、每次 O(kH²) ordinary matching、全部算术 poly-bit。即使真实 V 低也同样终止。这里不依赖 tiny 隐含的 helper 数下界；ν 只在曲率及最终有限 rounding loss 出现。

## 7. 共同 prefix circulation、k1 直达及全 jobs 输出

§19 明确 k1 已有 integral allocation，直接恢复 Good helpers；它不经 prefix。k≥2 的成功 fractional W_hat_i≥25/128，按 a_iu=max_j w_jp_jsu 聚合 claims 只增值。a_iu≤ν、Σa_iu≤1，空 max=0。只列 positive a edges，sorted fractional prefixes F_l 与 floor(F_l) 在同一个 circulation 中处理全部 outers 和 leaves。

本稿现已逐条列出 source→q_m、q_l→q_(l−1)、q_l→u_l、source→leaf、leaf→E_l、resource→sink、sink→source 的整数上下界；m=0 省链，原 aggregated fractional flow 见证 feasibility，resource 总容量一。积分流因此同时覆盖全部叶，非逐 outer 分别选资源。分部求和使每个 outer utility loss≤max a≤ν。新域 ν≤1/65536（k≥2）当然≤1/4096，所以所写松界 W_i≥799/4096>19/100 仍成立，不是错误沿用旧上界。

两分支最终都保证 Good helpers 的 own-home 权重大于 q=1/10，或 k1 至少 1/6。保留其真实 selected-state B bundles，outer 拿释放 homes，其他 helpers 回原 own-home，叶保留共同匹配资源并选原 attaining state。B 与 homes 不交且所有 homes 不同，保证全部组 bundles 全局 disjoint。

逐个 selector 放原选定 private，只导出确实分配的正 incidence jobs；所有其他 incidence jobs，包括显式零、inactive payload、重复 indexed states，都回原 private。每原 job 恰执行一次、有限 endpoint 原封不动，resource 负载≤1、selected private≤19/10、inactive private≤1。成功 C≤19/10≤(19/10)OPT，所有 FAIL/no-leaf-matching 基线比值<32/17。不存在仅输出 active 子实例的问题。

## 8. Source、软件、元数据和本票范围

§19 最后一段固定 0<γ<1/10 的 source 比较条件正确：若一个归约的每个输出都在本 typed 新域，YES actual OPT≤1，则算法实际 C≤19/10；NO actual OPT≥2−γ>19/10，则任何合法输出 C 都越过阈值。仅此全输出归域前提下，P≠NP 排除该实际 source 归约。没有误说所有 normalized-flat source、所有 γ、一般 UM 或一个 LP benchmark gap 都被排除。

§20 及 §12 Evidence/Status 对 v4 新 Exact、未发布 v3、前身 k⁴ Exact/Proof、informed k² audit、自核与新 finite code/run 分工均实际读完。文中目前保留待 fresh independent 审查和 root 统一登记的状态，与本票作为知情实读的角色不冲突。本票没有读取这些链接/文件，故不认证其 SHA、代码或输出数字；只核稿中文字清楚把“作者自核/作者已执行”与“root 是否读跑/独立审查”分开。

有限交换枚举被限定为 4/5 resources、3 helpers/2 outers、1/2 leaves 的 lemma 校准，不满足 k≥2 tiny 域、不是 k1 greedy 测试，未实现 FW/profile/prefix/full UM 后端；这些限制在稿中明确，不借旧 v1 软件重放身份。这次我的软件范围仍只有 Fraction 常数核算，未读跑新 code/run，不能代签。

最终判断：本指定 v4b 全文在新 domain、精确常数、可计算子程序、任意输入的停止界、soundFAIL、共同 disjoint 取整和全部 ordinary jobs 上均核通，未发现 fatal。它是可信的知情作者读后/扩域复核，不是 fresh blind、不是原 prefix 重审，也不是软件或全球新颖性认证。下一份正式合并正文须按其最终 hash 另做 actual final read；本票不提前认证未读的 metadata/links/status 改写。一般 UM-TARGET-v1 仍 OPEN。
