# 正式 Exact 实读攻击记录

2026-10-18。实际次序：先冻结本人独立一般重构 `independent_fslp_welfare_four_layer_reconstruction.md`，SHA256 `a7245326951f8c4e251552307c003fbbcc1d08efbe761c19f770843af5f2a5e3`；同一个工具调用随后才读取 `../near_two_reduction/gated_normalized_menu_fslp_exact_first.md`。作者正式 Exact SHA 已告为 `591237d47b0330ebe6eb8d8daf509f467bc6fa663986905da13ce08ae40716e5`。尚未读取作者 Proof。本文不冒充外部评审或 novelty 核验。

## 结论

E1–E5 在其明示范围内没有发现 fatal。福利、两个严格计数、全部普通 UM jobs、精确 VALUE 恒等、rational LP promise decider 均可由独立重构闭合。以下补上正式 Exact 特有的反向 VALUE 及量词核验。

## 1. 正式连接器比口头合同更受限，但重构照样成立

本人初稿用 n 件 root small job 可去任意 group 的略宽合同。正式 Exact 的 C_g 只可去自身 X_g。取 H 时恰把 C_g（g∈H）送 X_g，其余留 R，故不需要多端自由；所有前向负载证明保留。不能把初稿宽合同倒记成已先审过固定端定义，现此差异已实际核对。

## 2. VALUE 的任意低调度解码

取任意完整合法调度 C<2。令 H={g:C_g 在 X_g}。根的精确负载为 2−|H|/n，因此 |H|/n≥2−C>0。对 g∈H，X_g 已接 C_g 的 unit；T_g 若留 X_g 会使负载至少 2，所以 T_g 必在本组某原 M_gs 上。令 B_g 为该 M_gs 所有导出正 incidence 的原资源集合。每资源端所有 jobs 时间 1，C<2 保证最多一件，故 B_g 全局不交。该 state 的精确负载为 2−sum_{u∈B_g}p_gsu，因此其 selected-state 质量至少 2−C，原 v_g(B_g) 更大或相等。零 incidence 外送只占资源，不改变此不等式，且不会被误读为正质量。未选 states 的额外 exports 只多占容量，不损害提取。

所以 beta*≥2−C。前向任意 H 与 attaining states 的完整回填已独立给出。β*=0 可将全部 connectors 留 R、selectors 留 gates、incidences留私有机，峰 2；β*>0 则有限最大见证给峰 2−β*。两侧合成 OPT=2−β*，含 OPT=2、OPT=1、n=1 和边界。

## 3. 严格计数与有理常数

1−1/e>5/8 等价 e>8/3，而 e=Σ1/k!>1+1+1/2+1/6=8/3，因此 E2 的严格 >5n/8 有自足数值余量。对 h_>(δ)，其余组 r≤δ，故 sum r≤h+(n−h)δ；对 h_≥(δ)，其余 r<δ，可用同一弱上界。若 h≤((5/8−δ)/(1−δ))n，则 sum r≤5n/8，矛盾。δ=0 的两个版本均成立；NO_≥ 空类的退化已诚实写明。

δ=3/8 时计数界是 h>2n/5，严格强于所需 h≥3n/8。任取全部高组：根负载<8/5<13/8；selected private≤13/8；gates、unselected states、零 jobs、resources 均≤1。不是仅控制 selected roots。

## 4. LP promise 与“等价”用词

YES 全体质量 1 ⇒ 每组某 attaining norm1 state 的全部正 support 均包含在其 bundle，给 integral FSLP witness。NO 的 h_≥（或另版 h_>）阈值与 E2 输出直接冲突，故 LP 不可行。只有显式 0/1 LP，无需运行福利构造即可判 promise。

E4 末句的 P_gate promise “OPT=1 vs OPT>13/8”确实由同 LP 分离。若“等价”指参数特例 δ=γ_hi=3/8，则凭 VALUE 恒等是严格等价：β*<3/8 iff 没有 ≥3n/8 个组同时质量≥3/8。对 E4 所有其它参数不应将该句理解为逐实例相同的 NO 类；建议写成“由 VALUE 得到的特别 gap promise”，避免过宽理解。这是表达收紧建议，非数学 fatal。

## 5. 位长与对象攻击

每资源最多 I 个原正系数 thresholds；CDF 求值是明确有理 λ 子集和及 n 个因子的乘积。逐组 candidate 条件期望比较仅需多项式次有理运算；分母位长按乘法次数累加而非数值展开。显式零不进入正支撑 LP，仍保原 job；unused 资源可没有入流。所有原 state norm1，因此每 state 至少一个正项且 I≥S。大分母、极小正系数、zero λ、重复 states 都不改变算法界。未把 sparse instance 声称为 poly(log alphabet) succinct 转换。

原 finite 资格数 1+3n+S+2I、机器数 1+n+S+m 与 jobs 数 1+2n+I 均核对正确。原 flat 与新门控矩阵是不同实例，Exact 明确区分；没有用新矩阵的算法偷换原 flat 全组 min-value。
