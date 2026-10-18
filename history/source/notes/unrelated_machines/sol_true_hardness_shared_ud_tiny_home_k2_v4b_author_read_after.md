# shared-UD tiny-home v4b：作者全文读后记录

审者 `/root/sol_true_hardness`，2026-10-18。本记录是已冻结 Exact-first 之后的知情作者读后；不改、不替代原独立算法记录。

## 1. 实际来源、范围和历史

本次实际全文读取 `sol_general_repair_shared_ud_tiny_state_potential_canonical_append_v4b.md`，全部 §12–20，204 行、22847 bytes，实际 SHA256：

    1e3710870c8fbef4d4235cf2f90fe2d8ec6ca84b99ec6cd234464cc9d260df44

读取前，root 已实际读完我的独立 Exact-first：`sol_true_hardness_shared_ud_tiny_home_k2_v4_exact_first_attack.md`，149 行、12401 bytes，SHA `69036ac605760a193093869fc2af26b6fed35d76ed1c49f776185d17e9089f10`。其字节保持不变。本次不是新 blind；此前背景、Exact 阅读边界见该独立原稿。

没有打开作者旧 v1/v2/v3 Proof、root 的 ba7556 短代数 Proof、作者其他 append/audit/code/json、NSW review 或 canonical 原前缀。v4b 内所报旧前缀、他人实际阅读和软件身份只作为作者的历史陈述，不是我实际核过的事实。本次没有算法实现/软件重放；只另用自己的 Python Fraction 核对文内五处固定有理常数。

## 2. 作者路线与独立稿的关系

作者 k1 是固定 helper 顺序的 partition-submodular greedy；k≥2 是对完整 helper profile 的 fractional primal concave potential，FW 近似每个 profile 的最优势，再单 helper 换 state，最后以共同 prefix-flow 舍入。我的原稿则全程维护实际 independent allocation，做近似局部势上升；不需要 fractional profile optimum、stable-optimal coupling、FW 或最终 prefix-flow。以下逐项核的是作者这另一套算法，不能靠原独立算法的正确性替它补缺口。

结论：所读 v4b 数学及总位复杂度未发现 fatal，v4 的 k1 无 tiny 和 k≥2 的 k² 量词均有付款；没有据此认证软件、新颖性或一般 UM。

## 3. §13–14：实际桥、叶、固定 profile oracle 与共同 benchmark

完整 ordinary 编译、所有零 incidence/重复 indexed states/未用资源保留、OPT=2−V 与 baseline2 均闭合；资源上 unit job 的独占反向只用 C<2，没有把 C=2 硬作正值 decoder。无全叶匹配时，b_l<ε 的 strict exact iff 确实给 V<ε，baseline 比值<32/17<19/10；空叶和 rank0 可由同一分支处理。

vacancy matroid 应按作者给出的独立集定义理解：B 的子集 X 可删 iff B\X 仍匹配所有叶；也就是叶侧 full rank 的 transversal matroid 之 dual，不要求其 rank 等于 |B|。固定 profile 允许 helper empty 只是辅助 bookkeeping，最终仍回原 own-state，不新增普通 state/job。

固定 profile 令 t_u=max_j λ_i(j)w_jp_jsu，则最大 helper welfare 等于 Σt_u 减去 full leaf matching 占用资源的最小 t 成本。每个没被叶占的资源可给一个达到 t 的 helper，或 unused dummy；无每 helper 数量下界，故这一公式确为 integral matching oracle。fractional ownership/leaf flow 的积分性也直接成立。

将各 indexed option 看作带标签平行 copies 集，weighted matroid rank 的阈值-rank 表达给单调次模。数学上多 option 集合只用于证明；Q_j≤1、W_i≤1 的断言确实仅用于合法单 option profile。actual V≥ε 给的是同一个 O：只保留被 outer 拿 home 的 helpers 的实际 B bundles，并给各叶从原实际 bundle 取一个 E_l 代表。该共同 O 同时对所有 λ 给 ε²Σλ 下界，没有对不同 λ 重用互斥见证。

## 4. §14.1：k1 无 tiny

按固定 helper 顺序，每步在原 fallback options 加 empty 中贪心匹配 welfare。对任意 O，各 final add marginal 不大于该 helper 轮到前的 add marginal，后者不大于当步贪心增益，求和得 f(O)≤2f(G)。这一证明对任意 w_j∈(0,1]、empty/no-fallback、重复 indexed options 都成立。

W<1/4 与 actual V≥ε 所给 f(O)≥225/256 冲突，故 FAIL 实际 sound。W≥1/4 时原 integral allocation 中 Good threshold1/10 给 home mass至少1/6；不需要 prefix 或 ν。这里作者比我的 k1 近似局部势更直接，但不是从我原稿代签来的推论。

## 5. §15–16：最优点稳定性与 arbitrary fractional point

profile feasible W 是紧凸多面体的线性像；Φ 可微凹。故其任意 optimum W* 的正 gradient λ 支持同一 feasible region，f_λ(A)=λ·W*。将 deficit 显式提升为 d_i≥c−W_i、d_i≥0 后，凸最优一阶项非负，二次余项就是 deficit 差平方，得到 P(A)−Φ(W_hat)≥‖d_hat−d*‖²；不需要唯一 optimum。

我独立重构了 stable lemma 的 integral 敏感性：

- 删除当前最大权 basis 的一个已选 e，零 dummy 保 rank。对任意删除后 basis D，用 symmetric exchange 找 f∈D\B，使 B−e+f、D−f+e 都是 basis；旧最优给 W(D)≤W(B)−w(e)+w(f)。选最好 replacement 即得删除后 optimum，且不删其他已选元素。
- 插入新 x，若用 x，则与旧最大权 basis 的 fundamental circuit 交换其中最低权元素即可最优。对任意含 x 的新 basis D，symmetric exchange 找可同时交换的 f；D−x+f 是旧可行 basis，故 W(D)≤W(B)+w(x)−w(f)，这正被 circuit 最低权 replacement 支配。loop/不改进则保旧 basis。

因此删全部旧 j copies 期间，其他 helpers 只增；插全部新 j copies 期间，其他 helpers 只减。令旧/新 j 最终贡献 A0,B0，各≤λ_i(j)w_j；其他 helper 增量 G≤A0、损量 L≤B0，来自旧 ground 删除不增最优、加入不降最优。对 owner outer，同 outer 其他 helpers 的增减确实计入，变化在 [−A0,B0]；别的 outer 在 [−B0,A0]。总 weighted L1≤A0+B0+|A0−B0|≤2λ_i(j)w_j，最大坐标≤λ_i(j)w_j，故(16.1)正确。

任意 λ-optimal fractional network point 分解到其 linear-optimal face 的 integral vertices；补 unused zero dummy 后均为同 rank 的最大权 basis。逐 vertex 用上述更新再平均，仍是新 profile 的 optimal fractional point，coordinate/L1 界由凸性保留。这里不用可计算分解，也没有只对某个特别 optimum 成立的偷换。

以 λ_min≥θ/k 将 weighted L∞×L1 转为 ‖ΔW‖²≤2(λ_i(j)/λ_min)²w_j²，再用 Φ 的2-smoothness，真正得到 P(A')−P(A)≥Δ_j−B_j；不要求新 point 最大化新 Φ，也不是实际普通 jobs 迁移途中负载界。

## 6. §17–18：新 k² 付款、FW 位长、sound FAIL

次模 add-versus-replace 及 Σ deletion losses≤f(A) 给(17.1)，empty/同 option 时也成立。代 λ=θ/k+2d、ε²=225/256，作者进展下界的 Dsum 系数65/128、常数287/8192正确。

Σ_jw_j² 按每 outer≤ν 汇总，使总 curvature≤2νk+(8νk/θ+8cνk²/θ²)Dsum；代 k≥2、ν≤1/(16384k²) 后为≤1/16384+(21/128)Dsum。这个关键新域证明没有依赖旧 k⁴ 或 H≥const·k⁵。Dsum≥9/80 给ρ=293/81920>0。

FW 从 W=0 加完整叶匹配开始确为可行，正 gradient 的 linear oracle 即§14 matching。diameter²≤k，smoothness 给 gap_next≤(1−γ)gap+kγ²；γ_t=2/(t+2) 推得 gap_t≤4k/(t+2)，固定 N=ceil(4k/ξ) 足够。t 次后第 r 个 integral vertex 权重2(r+1)/(t(t+1))确实求和一，故 payoff 分母可取 D1·t(t+1)、flow 分母 t(t+1)，没有递归分母爆长。D1 可取所有原分母乘积的固定平方，位长为输入多项式。每次 matching cost、gradient、Φ、阈值比较仍 poly-bit。

若 W_hat 某坐标<25/128，由 gap≤ξ 及 deficit稳定性给 Dsum>15/128−1/(1024H)>9/80。actual V≥ε 会给共同 O，再迫某 profile 真 P 增≥ρ/H；两端下近似误差至多一份 ξ，故其确定性 P_hat 增≥ρ/H−ξ>τ。与无候选矛盾，所以 baseline FAIL 的确推出 actual V<ε；没有把 λ oracle 失败或弱必要系统失败冒 actual infeasibility。

固定初始匹配、打平规则和 FW 步数使 P_hat 成为 profile 的确定函数。每次采用增≥τ，range[-kc²,θ]给 O(kH)次 move；每轮枚举原 options 加 empty，并以 O(kH²) matching 次数估一个 profile，故输入所有实例均 worst-case 总位多项式。指数多个 profiles 的存在不成为枚举费用。

我的单独 Fraction 核：ρ=293/81920；在 H=1 的保守端点，ρ−2^(−20)−1/2048=16187/5242880>0；15/128−1/1024−9/80=19/5120>0。H≥1 时这些界只更强。

## 7. §19：共同 prefix-flow、舍入与全 jobs

同 outer 聚合 resource claims 后，移交给达到 a_iu=max_j w_jp_j,s_j,u 的 helper，只增 outer welfare；每 helper 仍原一个 state，Q_j≤1 仍由原 state 归一和 resource≤1保证。Σ_u a_iu≤Σ_j w_jΣ_up_j,s_j,u≤1、max a≤ν正确。

作者 circulation 的 outer 前缀链方向与 lower bounds一致：q_l→q_(l−1)通过恰前l−1项 claims；原 fractional count 给可行性。source→leaf恰1、resource→sink≤1、总 circulation≤|B|；因此整数可行流同时给所有 outer claims 和全部叶的同一完整 matching。并非每 outer 单独取整后再忽略叶冲突。

按 a 降序，所有前缀 Y_l≥floor F_l。Abel分部求和：Σ_l a_l(F_l−Y_l 的差分)≤(a_1−a_2)+…+(a_(m−1)−a_m)+a_m=a_1≤ν。允许某前缀 surplus；m=0省链正确。故作者 W_i≥25/128−ν≥799/4096>19/100 的宽松常数安全；我的 Fraction 核最后余量为519/102400>0。

Good helper threshold1/10、outer 收其 homes、其余 helper 回 own home、leaf 保留 integral E_l 代表；home 全局互异且 B disjoint，故全体 group 同时质量至少1/10。作者最后的 private/resource 回填处理全部 selectors、所有未选 states payload、显式零 jobs、duplicate indexed states 和 unused resources，不新增任何普通资格。失败 baseline同样完成所有原 jobs。

## 8. 最后意见及不外推范围

本次对作者 v4b 全§12–20实际全文读后，未发现新的数学 fatal或需要放宽 Exact 的例外。stable coupling、k²、k1无tiny、FW、sound FAIL、共同叶 prefix-flow 和全原jobs均独立核过；与我的另一实际-allocation算法相容，但未混用两套证明的步骤。

作者所报finite exchange枚举仅其软件身份陈述，我未打开/重放，不代签。没有读原 canonical 前缀或未释放的其他材料，没有 primary检索或外部定理新认证。本记录不认证该算法端到端实现、全球新颖性、非UD叶、多state outer、重homes或一般UM，主真实近2硬度目标仍OPEN。
