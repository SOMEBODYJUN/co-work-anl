# 共享 aggregate 负载直方图的 Exact-first 独立重构与边界攻击

审查来源：sol_true_hardness（root 指定 6.1sol max）。本记录冻结于阅读作者 Proof 之前。本轮唯一读到的作者材料是 `/workspace/scratch/038d9dcc4cac/sol_global_certificate_shared_hull_exact_statement.md` 全文，SHA256 为 `f73acb0f0eb3b6741d1a8a854fbee1d507aadea2a8f2f5e3a533aee50740163a`。

未读 `sol_global_certificate_face_hull.md`、作者 audit/code 或其他 reviewer 文件。下面是仅从 Exact statement 独立推导的证明与攻击，不冒充作者 Proof 读后审查。本记录未改 repo，无 Git / Work / 凭据操作，也未做有限实验替代全量词证明。

审查对象：`SCRATCH-UM-SHARED-AGGREGATE-HISTOGRAM-CONFIG-EXACT-v1`。

## 1. 冻结结论

1. 对所有 integer finite / zero / ∞ 输入、所有前缀 j，包括 n=0、K=0、无有限边及后续前缀，集合恒等式 Ĥ_j=P_j 可以完整证明。没有把 z^i∈θ_iĤ_(j−1) 偷添回去，也不需要这项约束。
2. 一个“每机 layered unit-flow，加跨机器逐 job 选入质量恰 1 等式”的显式 LP 正好投影为上述集合。j≥1 时其变量、约束数确为 statement 所列 O(mj(K+1)+|E_[j]|(K+1))，系数和 RHS 都可取 {−1,0,1}。它不是没有 side constraints 的纯 network-incidence LP；不能据网络一词推 TU / integrality。
3. 向下舍入后 LP infeasible⇒OPT(P)>T 的方向完整成立。固定 δ 时 bit-poly；binary K 的原整数版仅 pseudo-poly；δ 变输入时须计 1/δ。
4. 唯一字面 size 边界需要明示：j=0 时所写 O(mj(K+1)+|E_[j]|(K+1)) 的 RHS 为 0，而若投影要求显式 terminal y variables，就还需 m(K+1) 个变量/等式。安全写法是 O(m(j+1)(K+1)+|E_[j]|(K+1))，或者明确 j=0 直接返回常量 h^0、采用零维 LP 的常量 affine image。此处不反驳集合等价或 rounding soundness，但不能在审查记录里悄悄将 j 改成 j+1 后宣称原字面 size 无需约定。
5. 有理优化的 polynomial-time 还应按标准含义把给定 objective 的编码长度计入输入长度。若只按不含 objective 的固定 LP 长度，任意长 objective 连读取都无法保证；这属计算合同应说明的通常输入约定。

没有发现主等价式、有限/零/∞处理或 rounded infeasibility cut 的实质 fatal objection。作者 Proof 尚未读；以上数学内容是独立重构，不是对未读 Proof 的认可。

## 2. 消去 cross-row z：准确的一步传输合同

先固定任意 j≥1，并把 θ_r=0、x_r(s)=0 对所有 r∉E_j 延拓。令 y 是前一层直方图。它的每行非负且总和 1。

Exact 中的一步递推，等价于存在 selected-mass 向量 x_r(s)，满足

    0≤x_r(s)≤y_(r,s),
    x_r(s)=0 if r∉E_j or s>K−a_rj,
    Σ_r Σ_s x_r(s)=1,

并令

    y'_(r,s) = y_(r,s) − x_r(s)
                + 1[s≥a_rj] x_r(s−a_rj)       (r∈E_j),
    y'_(r,s) = y_(r,s)                        (r∉E_j).

原式⇒该合同：取 y=Σ_i z^i、x_r(s)=z^r_(r,s)。非负给 x≤y；row-r 总量是 θ_r，故 selected total 恰 Σ_rθ_r=1；容量条件正是 x 在 s>K−a 时为零。不同 branch 对 row r，除 branch r 外都原样留下，所以 shift 公式如上。

该合同⇒原式：取 θ_r=Σ_s x_r(s)（r∈E_j）。它们非负总和 1。下面逐行 r 构造所有 z^i_(r,·)，完全不要求每份 z^i 自己是 feasible old histogram。

- 若 r∈E_j，先令 z^r_(r,s)=x_r(s)。记 η=1−θ_r。若 η>0，对每个 i∈E_j、i≠r 令

      z^i_(r,s) = θ_i [y_(r,s)−x_r(s)] / η.

  其行总量为 θ_i，因为 residual row 的总量为 η。每坐标加总恰 y_(r,s)。
- 若 r∈E_j 且 θ_r=1，x≤y 且二者行总量都为 1，故逐坐标 x=y。其余 θ_i=0，令其余 z^i 的这一行全为 0，不作除以 0 的运算。
- 若 r∉E_j，则对每 i∈E_j 直接令 z^i_(r,s)=θ_i y_(r,s)。总量 θ_i，加总仍 y。

因此所有 row constraints 同时成立；每个 own-row 的容量约束由 x 的支持给出；shift 的 y' 正是给定公式。若 θ_i=0，所有构造对应的整个非负 z^i 自动为零。

这一步只用前一层的每行概率质量；没有约束或声称某个 z^i/θ_i 属于 Ĥ_(j−1)。当 θ_i>0 时，其 conditional old-job coverage 可能错误，正是 Exact 允许的弱共享合同。

## 3. CONFIG 的一步更新：两个方向均保全部旧 jobs 的覆盖

以下所有分布和向量可取实数，因集合恒等式本身不是只对 rational points。有限状态概率定义允许这些实值；计算部分再单列 rational 输出。

### 3.1 从 old CONFIG 与 x 建 new CONFIG

给 y∈P_(j−1)，取任意实现它的 old row-configuration distributions Y_r。对一个 old configuration C，记其负载 s。若 y_(r,s)>0，以概率

    λ_r(s)=x_r(s)/y_(r,s)

把 job j 加入 C，否则不加入。λ∈[0,1]。若 y_(r,s)=0，则 x_r(s)=0，任取 λ_r(s)=0；没有 0/0。

对不可用 r，x=0，所以不插入。对 s>K−a_rj，同样 x=0，所以不会产生超容量的新配置。所产生的每台机器配置因此确属 C_r^j(K)。

对每个旧 job ℓ<j，插入 j 不改变它是否在 C 中，故它的每行 inclusion marginal 原样保留，跨机器 coverage 仍恰 1。新 job j 在机器 r 的 inclusion probability 是 Σ_s x_r(s)=θ_r，总覆盖为 1。新负载直方图恰 §2 的 y' 更新。因此给任意合法一步 x，有 y'∈P_j。

这里可以从某一份选定 old CONFIG witness 建一个 new witness，但不保持 Exact 中每份 branch z^i 的配置身份或 conditional feasibility；这两个命题不同。

### 3.2 从任意 new CONFIG 反推 old CONFIG 与 x

给任意配置分布 Y_r^new 实现 y'∈P_j。在每个实际配置中删掉标签为 j 的那个 job，得到 old distribution Y_r^old。所有旧 jobs 的 inclusion marginals 不变，所以 Y^old 是 CONFIG_(j−1)(K) 的见证。记其 histogram 为 y。

定义

    x_r(s)=Pr[ j∈Y_r^new 且 load(Y_r^new\{j})=s ].

若 r 不可用，原配置绝不含 j，所以 x=0。x 是 old load=s 事件的子事件，故 0≤x≤y。new 配置容量给其选入支持 s≤K−a_rj。新 job 的 coverage 等式给 Σ_r,s x_r(s)=1。new histogram 正是 old histogram 减去该部分质量、再平移 a_rj。因此得到 §2 的准确 selected-mass 合同，进而按其显式分段构造得到 θ,z。

该方向没有从 marginal histogram 猜一个非法源配置；它从存在的 new CONFIG witness 先删除带标签 job，再构造 z。允许删除前后的不同同负载配置，因为命题只要求存在某份 old witness。

### 3.3 对所有 j 的归纳

j=0 时每台机器唯一配置是 ∅，所以 P_0={h^0}=Ĥ_0。假设前缀 j−1 已相等，§2 与 §3.1 给 Ĥ_j⊆P_j，§3.2 给 P_j⊆Ĥ_j。归纳覆盖所有 j≤n，不依赖最终 n 的正性。

E_j=∅ 时 CONFIG_j 对 job j 的覆盖左边恒为 0，不可能等于 1；递推也因 Σ_iθ_i=1 而空。若任何旧 prefix 空，new CONFIG 删除末 job 将产生 old witness，与空性矛盾；递推同样要求 aggregate old point，故以后每一前缀都空。

## 4. 全显式 layered-flow LP 及配置路径双向对应

对每台机器 r 建 layers t=0,…,j，load nodes (r,t,s), 0≤s≤K。在每一步 ℓ=t+1：

- skip arc (r,t,s)→(r,t+1,s)；
- 若 a_rℓ finite 且 s+a_rℓ≤K，另建 selected arc (r,t,s)→(r,t+1,s+a_rℓ)。

每个 arc 保留 (r,ℓ,s,skip/select) 独立身份。流量非负；起点 (r,0,0) supply=1，其他 layer-0 loads supply=0；各中间点守恒。terminal incoming flows 为 y_(r,s)。每个 ℓ≤j 另加一条跨机器等式：属于 job ℓ 的所有 selected arc 流量和恰为 1。

每台机器的一条完整路径，按 selected arc 的 job 标签，给一个不同的合法配置 C：每层至多选一次该 job，所有已选端有限，load 单调且总≤K。反向每个配置 C 依 job 顺序选择 selected/skip，唯一确定其路径。故每机配置分布推前为 unit flow；反向有限 DAG 中每机 unit flow 可分解为有限路径混合，剥离正流路径时每次至少消去一条正弧，至多 arcs 数量次。全局 selected-mass 等式恰为逐 job coverage。这证明 LP 投影正是 P_j，不是假借未知 separation oracle。

零时间时 selected/skip arcs 虽同起终点，仍是不同变量：selected column 进入该 job 的覆盖等式，skip column 不进入。合并两弧会丢失 job 的 inclusion 标签，因而不允许。相同处理时间的两个不同 jobs 位于两个不同层，也不能合并。∞ 无 selected arc。

变量数量：skip≤mj(K+1)，select≤|E_[j]|(K+1)，terminals m(K+1)。节点及 conservation 数≤m(j+1)(K+1)，覆盖等式 j。j≥1 时全部吸收进 statement 的 bound；j=0 的额外常量点 convention 见 §1 第4项。所有矩阵元素与 RHS 只用 −1,0,1；integer processing times 只用来确定 selected arc 的节点下标，不作为 LP 大系数。

跨机器 job-coverage constraints 是 side constraints。这个 LP 不是单个普通网络的纯 flow polytope，不可由网络整数性推出 integer schedule；其每机 paths 是独立 row marginals，也不提供跨机器共同 path law。

## 5. 计算复杂度与 certificates

每机 unit flow 全部在有限层 DAG 内，任一弧流量≤1；terminal y 也在 [0,1]，行和 1。由此 LP feasible region 有界。对任意 rational objective，存在 attained optimum，标准有理 LP 可判空、返回 rational feasible/optimal point，或输出 Farkas 不可行证书。系数 bitlength 常数，变量约束数是显式 m,n,K 的多项式，basic determinants 的 bitlength 也只是该规模的多项式；不能把指数大的 determinant 数值误作指数 bitlength。

若 objective 是另给的 rational vector，运行时间和最优点 bitlength 需计其编码长度。输入 rational point 时加入终点等式同样需计给定坐标 bitlength；本命题没有承诺以有限 binary 输出任意 irrational y 的 witness。

原整数版若 K 只以 binary 给出，load nodes 有 K+1 个，所以仅 pseudo-poly。即使所有 a=0，也不能因使用 ±1 系数而把显式 K+1 维输出隐藏掉。

## 6. 一般 UM 的向下舍入和准确 cut 方向

设 T>0、n≥1、δ∈(0,1) rational，q=δT/n，K=floor(n/δ)。先删掉 p_rℓ>T 的有限端，再对剩余端设 a_rℓ=floor(p_rℓ/q)。这些 a 在 0,…,K 内。

若原实例存在一份完整 actual schedule σ、C_max≤T，则任何被用边都有 p≤T，全部在剪枝后保留。对每台机器，

    Σ_(ℓ:σ(ℓ)=r) floor(p_rℓ/q)
      ≤ (Σ_(ℓ:σ(ℓ)=r)p_rℓ)/q
      ≤ T/q=n/δ.

左边整数，故≤floor(n/δ)=K。于是各机的实际标签 job 集是一份 capacity-K 配置，取对应 Dirac row distributions 给 CONFIG_n(K) 可行；由已证恒等式，LP 可行。

所以 LP infeasible 的 contrapositive 恰是没有原 C≤T actual schedule，即 OPT(P)>T。剪枝可制造无有限端 job，届时两个整数系统都 infeasible，这正是 sound rejection，不能默默把它删除。

固定 δ 时 K=O(n)，q 与各个 floor 的有理整数运算 bitlength 都是原显式输入长度的多项式，LP 规模和 rational certificates 亦如此。不需要 T 为整数、T 有正数值下界、OPT>0 或 p 有正下界。δ 变为 binary 输入时还要允许对 1/δ 的数值多项式依赖；把它写成仅 poly(log(1/δ)) 不成立。

T=0 时根本不定义 q；每个 job 有某个零端当且仅当能把全部 jobs 调度到 makespan 0，机器可以承接任意多零 jobs。n=0 直接空调度与 h^0。原 all-zero 实例在任何 T>0 时都有 actual feasible schedule，所以该 infeasibility cut 不会误报。

## 7. 最终 histogram 与原配置身份的不可识别

例：m=2,n=2,K=0，两个 jobs 在两台机器都为零时间。CONFIG witness A 是机1取{1}、机2取{2} 的 Dirac 分布；witness B 则交换两个 jobs。两者都覆盖逐 job 恰 1，且最终 histogram 都是每行全在 load 0。终点 y 无法识别原先给的是哪份 witness。

甚至正时间也会丢身份：m=2,n=2,K=1，每个端时间 1，两种 Dirac 完整分配交换 jobs 后每机仍 load 1，histogram 一样。

本 LP 内部的带标签路径可恢复**某份**配置分布，不能恢复一份额外指定但未输入的原 row distribution，也不能据此输出容量 K 的共同 integer schedule。Ĥ=P 只升级 aggregate endpoint 集合的识别，没有升级 cross-machine law 或 UM-TARGET-v1。

## 8. 精确状态

- Set equality：全量词独立重构完整。
- Integer zero/∞、E_j empty、all j、θ=0/1：均已逐处检查。
- Layered-flow computation：j≥1 的 stated size、±1 coefficients、rational certificates 完整；j=0 应明确常量 point convention 或用 j+1 bound；objective encoding 采用通常计入输入的约定。
- Down-rounding：仅 sound infeasibility cut，固定 δ 位多项式完整。
- Author Proof：尚未读。
- Independent tests/code：未运行；本轮为一般证明，不以实验支持集合恒等式。
- 新 UM 次二算法/困难性：无。

冻结后应先向 root 报本文件 SHA256；由 root 实际全文读取后再授权读取作者 Proof。本记录不得在后续补写成“冻结时已读 Proof”。
