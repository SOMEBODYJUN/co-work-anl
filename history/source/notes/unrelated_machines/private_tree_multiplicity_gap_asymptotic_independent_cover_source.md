# 叶资源重数配置间隙的一阶锐渐近：独立陈述先行审查

审查者：boss11 内部 cover_consistency。实际只读 `private_tree_multiplicity_gap_asymptotic_exact_statement.md`，SHA256 `fb1283d4bd3346be0dedae6e19acbef50876d68643fafdccbe537d7051156adf`。冻结前未读其proof或其它代理本项摘要。已知并独立审过bounded-μ v3的全CONFIG(T)上界；本项平星族的证书、实际OPT与sup/limit重新自行核验。无代码/有限试算/Git/Work。

结论：未发现standing fatal objection。下界族精确Tconf1、OPT=2−1/μ；与v3上界在完整同一类C_μ上相夹，给所述一阶极限。没有声称固定μ上确界达到，也没有把gap当算法困难性。

## 1. 完整原P及配置证书

固定整数μ≥2。d=μ、h1、单root，μ个state私有根M_s，μ个不同external Z_s。每state s有μ枚不同leaf jobs j_(s,1),…,j_(s,μ)，均可在M_s时间1/μ、Z_s时间1；唯一selector可在任意M_s时间1。全部state的叶资源重数最大恰μ，故P∈C_μ。

给完整CONFIG(1)证书，不只是λ行：

- 每M_s以权重1/μ取selector singleton，以权重1−1/μ取该state全部μ枚父端leaf jobs；后一配置总负载μ·(1/μ)=1，前者负载1，两权和1。
- 每Z_s对其μ枚真实leaf jobs各给一个unit singleton配置，权重均1/μ；μ个权重和1。

selector总覆盖μ·(1/μ)=1。每leaf在父端覆盖1−1/μ、外端覆盖1/μ，恰合为1；没有把同色不同leaf合并为一个job。每machine权重和1，全部配置负载≤1。故CONFIG(1)可行。共同full-state λ_s=1/μ也明确成立：对Z_s容量λ_s·μ=1，但上面已给更强的完整配置见证。

任何T<1没有配置能覆盖time1的selector，故Tconf≥1，结合证书得精确Tconf=1。

## 2. 实际OPT的下界与达到调度

任意实际调度的selector放某个M_s。若其C≥2，已≥2−1/μ。若C<2，每Z_s的unit jobs至多一个；特别所选state s的μ枚leaf最多一枚外送。因此M_s至少留μ−1枚small，加selector负载至少

 1+(μ−1)/μ=2−1/μ。

故所有调度C≥2−1/μ。

达到：selector放M_1，把该state恰一枚leaf送Z_1，其余μ−1枚父置；所有其它state的全部μ枚leaf父置。M_1负载2−1/μ，其它M_s负载1；Z_1负载1，所有其它external负载0。全部μ²+1原jobs恰分一合法端，无预载、删job或加端。μ≥2使目标值≥3/2≥1，故max正是2−1/μ。于是OPT/Tconf=2−1/μ精确，而非仅下界。

## 3. G(μ)的同类量词与sup

每固定μ的上述P是有限显式合法成员，故G(μ)≥2−1/μ。这个结论不要求整个sup达到；仅这个成员达到该数值。

上界使用已经单独审过的v3全阈值定理：对C_μ每一个P，OPT/Tconf≤2−1/(μ+2)。非空selector令分母≥1；全部父置/任选selector给OPT≤2，所以比值有限。该上界遍历全部d,h、root数、菜单和输入长度，与本项G的定义完全同域，不是只覆盖CONFIG1或固定d,h后取sup。因此G(μ)≤2−1/(μ+2)。

给定λ证书的v1命题单独不足以推出这个G上界，必须依赖v3对全部CONFIG(T)的已审结论；这里没有将两个不同类的sup混用。

## 4. 一阶极限与误差的方向

逐整数μ≥2有

 μ/(μ+2) ≤ μ[2−G(μ)] ≤1。

左边来自G的上界、右边来自G的下界。两侧沿整数μ→∞均趋1，故所述极限为1，无需交换sup与极限或选择一列达到sup的P。

直接相减还得

 0≤G(μ)−(2−1/μ)≤1/μ−1/(μ+2)=2/[μ(μ+2)]。

所以G=2−1/μ+O(1/μ²)成立，但没有证明每固定μ的G等于平星值，也没有证明v3上界锐。μ2时该构造比值3/2、一般上界7/4，仍留固定参数间隙，和一阶结论无冲突。

## 5. 显式大小和生成复杂度

成员有2μ台机器、μ²+1任务，leaf finite ends为2μ²个、selector finite ends为μ个。稀疏输入总编码O(μ² logμ)，若写满dense P则有2μ(μ²+1)个处理时间entries，大小O(μ³ logμ)。所有非整数时间只是1/μ，编码位长O(logμ)。配置证书亦按这一显式规模可列出；各机器的原leaf job ID保持不同。

可以按输出规模多项式生成P、完整配置和上述实际σ，但不能把这称为以binary μ的位长O(logμ)为输入的多项式时间输出：仅μ²枚leaf jobs的输出本身就可能指数于logμ。本项的G遍历所有有限显式成员，因此每μ的这个有限构造足够，不需要也没有假定poly(logμ)简洁编码。

## 范围

这是一份结构类配置gap参数化的精确下界及上下界一阶夹逼，不是NP-hardness、一般approximation-ratio下界或UM-TARGET-v1反面。平星族自身的最优调度已有上述直接构造。μ固定时v3上界离2有常数；本项只展示μ无界时相对该配置阈值不能保一个统一离2 margin。外部Haxell条件沿用v3已核范围，本次没有新重读primary或认证新颖性。
