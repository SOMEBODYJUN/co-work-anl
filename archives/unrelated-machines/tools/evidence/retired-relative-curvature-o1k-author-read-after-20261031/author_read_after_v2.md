# O(1/k) reciprocal-gradient 作者算法：实际全文读后攻击

审者：`/root/sol_nsw_independent_attack`，2026-10-18。结论：逐步按作者本算法重构后，未发现 fatal；log profile 势、固定 profile LP、相对曲率及有理 FW/atanh 后端闭合。不能用我的独立无 log 算法正确性代签作者付款。本票不认证软件、未来规范稿或全球新颖性。

## 1. 实际顺序、身份与阅读范围

先仅实际全文读 working Exact `/workspace/scratch/038d9dcc4cac/sol_general_repair_relative_curvature_O1k_working_exact_v1.md`（SHA `504e4d8e13b847aa7ec10f2bb3afa874389a76b6cc0962abfe979a985238a99f`，1–29 行），冻结我的独立构造 `/workspace/scratch/038d9dcc4cac/sol_relative_curvature_O1k_independent_exact_first.md`，SHA `074556f862b8548349f1710caa540f0a45c18f08a3f42822208ed9eb39d89583`，16740 bytes、182 lines、0444。父 agent 实际读完 182 行后才释放作者 Proof，原先行字节保持不变。

本轮唯一新增本地源 `/workspace/scratch/038d9dcc4cac/sol_general_repair_relative_curvature_O1k_working_author_proof_v1.md`，实核 SHA `0f5e322441789f5d2dae8fb0592fff86aede3d71f093cb727e2ea78b0f1b2593`，12721 bytes、173 lines。实际按 1–95、96–173 两块全文读取，无截断，含全部 §1–11、atanh tail 和身份范围。父 agent 释放时已概述 log 势/LP/FW/atanh 方向，因此本次是知情 actual read-after，不冒新 blind。

已知旧 v4、actual-I 算法与我先行路线的背景已在 074556 披露；本轮没有读取其他 O1k/general 草稿、root 讨论、代码、运行产物、其他审票或未来 canonical。没有 Git、repo、Work/token 操作。仅用 Python Fraction 核本文常数，不是算法运行认证。

## 2. 相同 Exact 对象与可靠基线

作者 §1 没有改域：single-state outers、所有 homes 不同、每 home 唯一 unit-own helper、任意 B-only normalized fallback、B-only exact-threshold-UD extra leaves；k≥2 的 ν≤1/(1024k)，k1 无额外 ν 条件。原 menus、zero incidences、inactive/duplicate states、unused resources 完整保留。

实际 OPT=2−V∈[1,2] 双向桥对全部 ordinary jobs 成立。正向只导出 selected-state 真 bundle 的正 incidence jobs，其他 payload 全留原 private；反向 C<2 使 resource-unit 独占，取 selector 所在 state 的导出资源获得值≥2−C。反向不要求给定 schedule 没有 inactive exports；正向重新安排全部 jobs。菜单非空和 unit selectors 给 OPT≥1、全 payload private 的 baseline C≤2。

ε=15/16 的整菜单 E_l、b_l<ε 的 iff 正确：一个 bundle 与 E_l 相交即可换原 attaining state 获值≥ε；不相交则每个 state 的整尾巴都<ε。叶图无 full matching 确推出实际 V<ε，baseline ratio<32/17。与我的先行路线用 V≤18/19 的较弱可靠 FAIL 不同，作者后文确实单独证明 V<ε，不能拿我的分支逻辑替它。

## 3. 固定 profile、共同 comparator 和 k1

有全叶匹配时 vacancy M 是叶匹配 transversal dual，D independent iff B\D 可匹配全部叶。所谓满 rank 指叶侧饱和、rank(T)=叶数，并非强加 rank(T)=|B|。空叶、空 B、rank0、loops/unused resources 全包括。

固定 helper profile 每 helper 一个原 fallback 或 empty（最终回原 own），positive ownership/leaf-flow network 的 leaf row 一、资源列≤一、helper 无数量下界，故是 integral network。每个合法 profile 的 Q_j≤1、W_i≤1；多-option 辅助集合只是 matroid weighted-rank 次模延拓。

给 λ>0，用 t_u=max active λ_i(j)w_jp_jsu，f_λ=Σt_u−mincost 全叶匹配费用，精确求该 profile 的线性最优值；不是指数 state 优化。actual V≥ε 时，同一次真实 allocation 的 outer-taken homes 对应 helpers 各需 B fallback 值≥ε；保留它们，叶各保留原 bundle 中一枚 E_l，给共同 profile O 的每 outer welfare≥ε²。因此 f_λ(O)≥ε²Σλ，对全部 λ 同时成立但 O 不是算法输入。

次模 add/delete inequality 逐项给 Σ_j[f_λ(A_j)−f_λ(A)]≥f_λ(O)−2f_λ(A)：每个加 target option 的 marginal≤对应 swap gain+当前 option deletion loss，全部 deletion losses 和≤f(A)。same/empty options 和重复 indexed identities 都合法。

k1 分支固定 helper 顺序 greedy，每轮枚举该 helper 原 fallback 加 empty，用 matching 精确选最大 marginal；final target marginals≤当轮 greedy gains，故 f(O)≤2f(G)。最后 integral matching welfare W<1/4 时 f_opt≤2W<1/2<ε²，可靠 V<ε；W≥1/4 时 Good threshold 1/10 给释放 home mass≥1/6>1/10。此分支不使用 ν、profile LP、FW 或 prefix loss，允许 w_j=1。

## 4. 固定-profile LP 在作者证明中的必要角色

k≥2 参数为 a=1/4、K=32k、ξ=1/(4096H)、τ=1/(64H)、恢复 q=1/10。每轮先在当前固定 profile 的显式 ownership/leaf network 加 W_i≥a 行，精确 rational LP 检查；变量、行、coefficients 都由当前已知 states 与 Q 显式给出，poly-size/bit。它不是求 unknown joint profile、actual OPT 或全 groups 目标解。

LP 不可行时分析势为 φ(x)=x（x≤a），否则 a+log(1+K(x−a))/K；Φ=Σφ，P(A)=max fixed-flow Φ。这个公式也自然适用于各 neighbor 的固定 profile，§8 因而可对每个 neighbor 独立计算 E，无须其 LP 先失败。

φ 是 C1、递增凹，λ(x)=1（x≤a）或 1/(1+K(x−a))，0<λ≤1，gradient Lipschitz K。log(1+y)≤y 给 0≤φ(x)≤x≤1，所以 P∈[0,k]。compact flow region 保证数学精确 optimum W* 存在；它可能 irrational 不妨碍分析，算法没有调用它。

first-order inequality 给任意这个 optimum 是当前 λ=∇Φ(W*) 的 linear optimum。LP 不可行保证该 W* 有坐标<a，故有 λ_i=1、S=Σλ≥1。这是一个真实逻辑义务：不能删掉 LP 后从某个 approximate Φ-gap 免费推出该坐标存在。作者已显式保留 LP，不依赖之前的 deficit 稳定性。

逐坐标 λ_iW_i*≤aλ_i+1/K：在 x≤a 时 λ=1；在 x>a 时 λ(x−a)=(1−λ)/K≤1/K。因此 λ·W*≤aS+k/K。以上均不需要精确求 W* 或 λ*。

## 5. 任意 λ-optimal fractional 点的稳定交换

作者 §5 的同一 λ 最优端点 coupling 可独立核。对任意旧最大权 basis，删一个 ground 元素 e 后，若 e 在 basis 中，取新最优 basis D，用 symmetric exchange 找 f，使旧 C-e+f 与 D-f+e 都是 bases；旧最优性便推出 C-e+f 已达新最优。插入新元素对称，fundamental-circuit 单次 swap 即够。所有零 dummy 常在 ground，rank 不降。

全部删旧 j copies 的阶段，其他 helpers 只增、其总 weighted gain G≤旧 j 贡献 A_0；全部加新 j copies 的阶段其他 helpers 只减、其总 weighted loss L≤新 j 贡献 B_0。A_0,B_0≤λ_owner w_j。owner outer（含同 outer 其他 helpers）的总 weighted change 在 [-A_0,B_0]，其他坐标在 [-B_0,A_0]，weighted L1≤A_0+B_0+|A_0−B_0|≤2λ_owner w_j，weighted L∞≤λ_owner w_j。

任意 λ-optimal fractional network flow 分解成同一最优面的 integral vertices，给每个 vertex 补零 dummy 成 basis，逐分量更新再平均，所得 W' 是新 profile λ-optimal。线性目标差精确是 Δ_j=f_λ(A_j)−f_λ(A)，上述两个 norm 界由凸性保留，覆盖每一个给定旧最优 fractional 点。这个分解/coupling 只证明新 profile 的势下界；算法不计算它，也没有以我的实际 I 更新来代替它。

## 6. 沿整条 segment 的相对曲率与 O(1/k) 总额

作者没有把旧 λ 当成沿线常量。若 Kλ(x)|h|<1，则整段 λ(x+sh)≤λ(x)/(1−Kλ(x)|h|)。x≤a 时右边≥1，向上段 λ 只减，向下未跨 a 时由 reciprocal identity 直接得；跨 a 则 Kλ|h|≥1−λ，右边≥1。因此所有跨 a 情况均包括。

weighted exchange 给 Kλ_i|ΔW_i|≤Kλ_owner w_j≤Kν≤1/32。于是整段 λ_i 至多 (32/31) 倍旧值，|φ''|≤4Kλ_i²；a 处 C1 而不 C2 仍可用积分 Taylor remainder，得到

    Φ(W')≥Φ(W)+λ·ΔW−2KΣ_i λ_i²ΔW_i²。

weighted L∞×L1 给最后的平方和≤2λ_owner²w_j²，所以在 W=W* 时 P(A_j)−P(A)≥Δ_j−4Kλ_owner²w_j²。求和并用每 outer Σw_j²≤ν、λ_i²≤λ_i，得 curvature 总额≤4KνΣλ≤(1/8)S。没有 hidden λ_min^(-2)、k² home 条件或只在一个端点检查 gradient 的漏项。

在 LP 失败、实际 V≥ε 时，次模比较给 summed linear gains≥(ε²−2a)S−2k/K=(97/256)S−1/16≥(81/256)S（S≥1）。减曲率得到 summed P gains≥(49/256)S≥ρ=49/256。因此某一个原 helper target option 增 P≥ρ/H；算法枚举全部原 fallback 加 empty 已含它，不用知道 O 或 λ*。

## 7. 有理梯度 FW、分母和 endpoint objective gap

固定 profile 从 W=0 与任意全叶匹配开始，当前梯度按 rational reciprocal 公式精确算；matching linear oracle 给 integral payoff R_t，γ_t=2/(t+2)，完整 flow 同步取凸组合。这里没有计算 log 来决定 FW 方向。

gradient Lipschitz K、payoff diameter²≤k 给 gap_{t+1}≤(1−γ_t)gap_t+(Kk/2)γ_t²。初始 gap≤k≤Kk，直接归纳得 gap_t≤2Kk/(t+2)。N=ceil(4Kk/ξ)=O(k²H) 足以给 P−Φ(W_hat)≤ξ/2，绝不需要 exact irrational optimizer。

γ_0=1 后第 r 个 vertex 的权重为 2(r+1)/(t(t+1))。原 integral payoff 是原 w_jp_jsu 的子和，共同原分母 D_1 位长为 input polynomial，所以 W 的分母可取 D_1t(t+1)、完整 flow 可取 t(t+1)。当前 gradient 分母只由当前 W 再作一次 1+K(W−a) 得出；不随 iterations 把旧 gradient 分母累计进下一 payoff。matching cost、比较、flow 及 W 的 bits 均 polynomial。

## 8. atanh 截断：不用 exact-log oracle 的完整误差核算

每 endpoint W_hat_i>a，x=1+K(W_hat_i−a)∈[1,1+24k]，z=(x−1)/(x+1)∈[0,(R−1)/R]，R=12k+1。定义 δ_log=Kξ/(2k)=1/(256H)。用整数倍增选 J≥1、2^J≥4R/δ_log=1024RH，L=RJ，故 J=O(log(kH))、L=O(k log(kH))，都不依赖原系数的分母数值。

由 2/(1−z²) 的几何级数在 [0,z] 积分，log x=2Σ_{n≥0}z^(2n+1)/(2n+1)。前 L 项全为非负有理，给下界；tail≤2z_max^(2L+1)/[(2L+1)(1−z_max²)]。

1/(1−z_max²)=R²/(2R−1)≤R；Bernoulli 给 (R/(R−1))^R≥1+R/(R−1)>2，所以 z_max^R≤1/2。故 tail≤2R·2^(−2J)。再用 2^J≥4R/δ_log，该值≤δ_log²/(8R)≤δ_log（这里 δ_log≤1/256、R≥25）。作者写的 uniform δ_log 界因而有充分余量，不是数值 log 估计。

各 linear 段 exact 取 W_i，log 段用 a+log_L(x)/K 得 E(A)。总截断误差≤kδ_log/K=ξ/2，合 FW endpoint gap 便是

    P(A)−ξ≤E(A)≤P(A)，  0≤E(A)≤k。

误差是 one-sided：neighbor E≥P_new−ξ、current E≤P_current，因此差只需减一个 ξ。梯度用 exact rational reciprocal，不用截断系列的导数，不混淆两个函数。

若 z=A/B，前 L 项共同分母可取 B^(2L−1)∏_{n<L}(2n+1)，bitlength O(L(log B+log L))；分子求和也 polynomial。x,z 来自 poly-bit endpoint W；L polynomial，跨 k 个 φ 值相加仍 polynomial-bit。整个 E 用确定初始 matching、N、L、tie 顺序，是 profile 的确定有理函数，未调用真实 log/exponential、随机样本或指数 series。

## 9. 搜索、soundFAIL 和绝对总位界

作者真实执行顺序为：叶匹配失败直接基线；k1 单独 greedy；k≥2 从全 empty profile 起，每轮先解当前 fixed-profile LP，成功就直接输出；否则算 E(current)，枚举每个原 helper option 加 empty 并重算 neighbor E，有增至少 τ 则取最大且固定 tie，否则基线。

FAIL 若真实 V≥ε，当前 LP 失败便有上一进展≥ρ/H；one-sided E 给某候选 observed gain≥ρ/H−ξ=(783/4096)/H，严格大于 τ=(64/4096)/H，净 margin=(719/4096)/H。故不可能 FAIL，实际 V<ε。这里必须合“LP 失败 + 所有邻居无足够 E 改善”，从来不把单独 LP 失败当实际不可行。

每次接受确定 E 至少增 τ，E∈[0,k]，moves≤64kH（作者松写 +1 也成立）。每轮显式候选数≤原 fallback states 数+H，每评价 O(k²H) matching、一个 polynomial-size endpoint rational atanh 计算；每轮 current LP 有 polynomial 行/变量/bit coefficients，标准精确 rational LP 可返 polynomial-bit basic feasible point。输入实际 V 低也同样终止，次数为固定绝对 polynomial，不靠有限 profiles 数量的指数上界。

LP point、FW 分母、reciprocal gradients、matching prices、atanh terms 和全部 comparisons 的 polynomial-bit 证明互相配套。没有给定 feasible LP/PSD point、target profile、joint law、OPT、精度参数、exact QP/SDP、未知 state oracle 或随机停时。

## 10. 成功 LP 的共同 prefix 取整与全部原 jobs

k≥2 LP 成功在一个固定 helper profile 中给每 outer fractional W_i≥1/4。a_iu=max_{j∈J_i}w_jp_j,s_j,u≤ν，Σa_iu≤1；聚合该 outer claims 到 argmax helper 只增 utility，保留叶 rows 和资源列容量。排序 positive a，给每 prefix integral count≥floor 原 fractional prefix，使用 outer nested-prefix chain 与全部 leaf demand 一、全资源 capacity 一的同一 lower-bound circulation。原 point 见证 feasibility，整数流同时覆盖所有叶，没有各 outer 各自分配后冲突。

summation by parts 的 loss≤max a≤ν。k≥2 ν≤1/2048，故 W_i≥511/2048，且减 19/100=3047/51200>0。k1 则本来已是 integral W≥1/4，绝不套这个 ν-loss。

两支 Good={Q_j≥1/10} 满足 W_i≤z_i+(1−z_i)/10，因 W_i>19/100 得 z_i>1/10。Good 保留 B bundle、outer 拿其 distinct homes；非 Good 回原 own state/home。叶保留共同匹配资源并选原 attaining state p≥ε。B 与 homes 不交，全 homes 不同，是真正所有 groups 的同一 disjoint allocation，最小值≥1/10。

编译回所有原 jobs：selectors 放上述原 indexed state 的原 private，只导出其真 bundle 的正 incidence jobs，全部其他原 incidence jobs（含 zeros、inactive 正 payload、duplicate indexed states、unused resource 上 listed 项）仍在原 private。每 job 恰一次、原有限 endpoint 合法，resource≤一、selected private≤19/10、inactive private≤1。P 仍 S+U machines、G+I jobs、S+2I finite endpoints，生成/稠密展开/逐 job 输出 polynomial。baseline 执行同一全部 jobs，C≤2。两分支均由作者自己的真实 V<ε 论证或正质量 allocation 闭合 ratio。

## 11. 判定和未认证范围

作者本 173 行 Proof 的每个承重接口均实际读并按本路线核回，未发现 fatal。特别是 fixed-profile LP 的额外逻辑义务、任意最优 fractional 点 coupling、整段相对 gradient 变化、全 k 的曲率总额、有理梯度 FW、uniform one-sided atanh 误差、E 阈值搜索和所有 jobs 都已分别支付。

我的先行 074556 是 actual integral I + 有理 cap-reciprocal（derivative reciprocal-square）势，无 log、无 fixed-profile objective optimum/FW；它使用 V>18/19 的参考。作者本稿是 profile optimum + reciprocal-gradient log 势、固定 LP、FW、atanh，参考 actual V≥15/16。本票没有混两种 endpoint、阈值或 oracle，更不以我算法正确来修作者缺步。

本轮软件范围仅 Fraction 常数核算；未读跑作者代码或实现任何完整算法。作者历史/working status 按其原件保留，不提前认证未来 canonical、软件或其他审查身份。仅支持本 O(1/k) typed 域，未外推 multi-state outers、home overlap、homes 上 extra leaves、nonUD extras、一般 normalized Q 或一般 ordinary UM；一般 UM-TARGET-v1 仍 OPEN。全球新颖性未认证。
