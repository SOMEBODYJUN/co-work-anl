# 笛卡尔菜单的分块一致性、线性重选与全域缺项界

读取目的：把[二元裸产品的反向放大](cartesian_menu_recoupling_and_coordinate_consistency.md)进一步定量为可复用的状态一致性标尺，同时检验全局非线性重选的真实负载。以下三项限定 Claim 分别有独立陈述先行审查；没有实现物理一致性或给出 near-2 困难性源。不能把额外选择语义当成原矩阵的资格。

## 1. 共同的完整普通 UM 矩阵

给 prime power \(q\ge2\) 及可按其标准表示位多项式计算的有限域 \(\mathbb F_q\)，整数 \(t\ge1\)，置 \(N=q^t\)。Groups、每组 indexed states 均标为 \(g,\ell\in\mathbb F_q^t\)，真实资源为 \((a,b)\in\mathbb F_q^t\times\mathbb F_q^t\)。State 支持

\[
 S_{g,\ell}=\{(a,b):b_i+g_i a_i=\ell_i\quad\forall i\}
\]

恰 \(N\) 项，各 private 时间为普通有理数 \(1/N\)，总量1。域运算与有理负载运算分开。

每资源一台 \(R_{a,b}\)，每 indexed state 一台 \(M_{g,\ell}\)。每 group 一件 selector \(J_g\)，在本组每台 private 机耗时1；每原 incidence \((g,\ell,u)\)、\(u\in S_{g,\ell}\) 一件不同 job，只可在自身 private 机耗时 \(1/N\)，或该唯一真实资源机耗时1。其它资格 \(\infty\)，无其它 jobs 或预载。**全部未选 states 的 jobs 均在矩阵内且必须执行。**

对固定选择函数 \(\ell(g)\)，令 \(k(\ell)\) 是可给每组分配至少 \(k\) 项、\(B_g\subseteq S_{g,\ell(g)}\) 全局不交时的最大整数 \(k\)，\(V(\ell)=k(\ell)/N\)。允许资源不用，\(B_g\) 任意，不要求 Cartesian。对任意非空选择域 \(\mathcal L\)，最大值 \(V_{\mathcal L}\) 对应的**选择域受限实际最优**恰

\[
 C_{\mathcal L}=2-V_{\mathcal L}. \tag{1}
\]

逐原 job 证明：给 \(B_g\)，selector 放所选 state，只有该 state 中 \(B_g\) 对应的 jobs 外送，其余所有原 incidence 留自身 private。所选 private 负载 \(2-|B_g|/N\)，未选 private 为1，资源至多1。反向任取完整 \(C<2\) 调度，各资源至多一件 unit；按 selector 实际目的 state 提取其实际 exports \(B_g\)，它们不交，所选 private 负载恰 \(2-|B_g|/N\)。未选 state 额外外送只占更多资源，不能逃过提取。\(C\ge2\) 的下界平凡。(1)含全部 jobs；若 \(\mathcal L\) 是逻辑侧条件，(1)也只是受限值。

## 2. q元 affine 与逐坐标选择的精确值

**ID / Version：`UM-QARY-AFFINE-MENU-RECOUPLING-CONSISTENCY-v1`。**

**Objects / Domain / Quantifiers / Definitions。** 对§1全部 \(q,t\)，定义 cyclic \(\ell_i(g)=g_{i+1}\)（循环编号）；affine 域为所有 \(\ell(g)=Ag+c\)，\(A\in\mathbb F_q^{t\times t},c\in\mathbb F_q^t\)；coordinatewise 域为所有 \(\ell_i(g)=f_i(g_i)\)，各 \(f_i:\mathbb F_q\to\mathbb F_q\) 可完全非线性但不能看其它坐标。Partial bundles 始终完全自由。

**Exact Statement / Conclusion。**

\[
 V_{\rm cyc}=V_{\rm aff}=1-\frac{\lceil(q-1)^t/q\rceil}{q^t},\qquad
 V_{\rm sep}=\frac{\lfloor(q-1+1/q)^t\rfloor}{q^t}. \tag{2}
\]

相应完整受限实际最优由(1)给出，可位多项式输出达界全部原 jobs 调度。对固定 \(q\)，cyclic 值趋1，而 coordinatewise 最优趋0，故不存在把同族任意高值分配修复为 coordinatewise 分配、同时保统一正常数倍值的合同，甚至不要求效率也不可能。

**Assumptions / Scope / Dependencies。** 只用§1显式对象及以下有限域/Hall证明。\(V_{\rm sep}\) 优化函数族；\(q>2\) 不声称每个固定非线性 \(f_i\) 同值。Affine 上界不升级为全部非线性 \(\ell\) 的上界；\(q=2\) 的无约束精确值由前页另证。没有任何 source gap 或物理函数约束前提。

## 3. 给定 affine 选择的对角扰动秩公式

固定 \(\ell=Ag+c\)。对每 \(a\)，令

\[
 \nu_a=\dim\ker(A-\operatorname{diag}(a)),\qquad
 \Lambda(A)=\sum_{a\in\mathbb F_q^t}q^{-\nu_a}.
\]

则精确有 \(k(\ell)=\lfloor\Lambda(A)\rfloor\)。事实上，\(a\) 层的 \(b\) 是 \((A-\operatorname{diag}(a))g+c\) 的 image，全部组的该层 union 大小 \(Nq^{-\nu_a}\)。任意组集合 \(F\) 的像至少 \(|F|q^{-\nu_a}\)，因每个 fiber 大小至多 \(q^{\nu_a}\)。不同 \(a\) 的资源身份不同，故

\[
 |N(F)|\ge\Lambda(A)|F|.
\]

全部 \(F\) 的 Hall 配额条件给每组 \(\lfloor\Lambda(A)\rfloor\) 枚真实资源；全部组 union 恰 \(N\Lambda(A)\)，又给整数上界。不需枚举所有 \(A\) 或所有 \(\ell\)，也不把 fraction 直接当作最终物品。

所有 affine 的上界：非零、各变量次数至多1的 \(r\) 元 polynomial 在 \(\mathbb F_q^r\) 至少有 \((q-1)^r\) 个非零点。按末变量写 \(x_r H+H_0\) 归纳：若 \(H=0\) 用 \(q\) 倍低维点数；否则至少 \((q-1)^{r-1}\) 个前缀使 \(H\ne0\)，各有 \(q-1\) 个非零值。应用于 \(\det(A-\operatorname{diag}(a))\) 的末变量系数：它的最高全乘积项系数为 \(\pm1\)，至少 \((q-1)^{t-1}\) 个前缀有唯一末坐标令 determinant 为0。因此

\[
 N-\Lambda(A)=\sum_a(1-q^{-\nu_a})
 \ge(q-1)^{t-1}(1-1/q)=\frac{(q-1)^t}{q}. \tag{3}
\]

\(t=1\) 时空 minor 为1，仍适用。

Cyclic 矩阵的核递推为 \(\delta_{i+1}=a_i\delta_i\)，恰在 \(\prod_i a_i=1\) 时有一维 kernel，其余可逆。奇异 \(a\) 有 \(L=(q-1)^{t-1}\) 个，故 \(\Lambda=N-L+L/q\)，达到(3)。整数 quota 为 \(N-L+\lfloor L/q\rfloor=N-\lceil(q-1)^t/q\rceil\)。可以把全部非奇异层各一枚给每组，再在奇异层左度 \(L\)、右度 \(q\) 的图做共同 matching，给每组 \(\lfloor L/q\rfloor\) 枚。不能直接扔掉所有奇异层而宣称锐值。符号按原方程严格为 \(A-\operatorname{diag}(a)\)，不是未经换元的加号版本。

## 4. Coordinatewise 上界、达到与实际范围

任意固定 \(f_i\) 的第 \(i\) 坐标有 \(q\) 条不同斜率线。首条有 \(q\) 点，以后每条至少与首条交一点，故该维 union 至多 \(q^2-q+1\)。全体组遍历全部元组，使总 union 恰为各维 union 的积，至多 \((q^2-q+1)^t\)。任意 partial 最小整数基数因而至多 \(\lfloor(q-1+1/q)^t\rfloor\)。

取所有 \(f_i=0\)，各维 \(q\) 条线 concurrent，除共同点外各有 \(q-1\) 个独占点。独占项分数1、共同项分数 \(1/q\)，每条线得 \(q-1+1/q\)。分数证书的 tensor 使每 group 质量为其 \(t\) 次幂、每真实资源总供给至多1；全部 Hall 子集或整数流给 floor 配额。最终 subsets 不必 product，(2)得到达到。

固定 \(q\)，两值的比趋0，证明§2的限定修复不可能；不排改变资源/任务/模型的新 compiler。\(t=1\) 时三域最优均 \((q-1)/q\)，\(q=2,t=1\) 为1/2。一般 \(q>2\) 的无约束非线性最优没有由本 Claim 闭合。

**Evidence / Counterevidence / Status / Related Files。** 作者冻结 Exact/Proof；bicriteria 先仅据 Exact 独立完整重构、后实际读作者Proof，root实际读取并独核。最终对应章节审查见[审查](../../reviews/unrelated_machines/qary_affine_menu_recoupling_consistency_review.md)。无 standing fatal；软件none、外审/全球新颖性未认证。Review 的有限辅助枚举仅归 reviewer，不记作 root 运行或证明前提。

## 5. 二元分块一致性的精确标尺与无环逃逸

**ID / Version：`UM-BINARY-CARTESIAN-BLOCK-FIBER-QUOTA-v1`。**

**Objects / Domain / Definitions / Quantifiers。** 在§1取 \(q=2,N=2^t\)，固定 \([t]\) 的非空 blocks partition \(I_1,\ldots,I_s\)，\(b_j=|I_j|\ge1\)。额外语义要求 \(\ell(g)|_{I_j}=F_j(g|_{I_j})\)，每 \(F_j:\mathbb F_2^{b_j}\to\mathbb F_2^{b_j}\) 任意非线性，但同一函数不能随外部 blocks 改变；partial subsets 仍任意。

**Exact Statement / Conclusion。** 置 \(H=\prod_j(2^{b_j}-1/2)\)，则优化全部这类函数及不交 partial bundles 的值恰

\[
 Q=\frac{\lfloor H\rfloor}{2^t};\qquad
 \left|\bigcup_gS_{g,\ell(g)}\right|\le2^t H, \tag{4}
\]

union 上界可达到，floor 配额可显式位多项式构造。若所有 \(b_j\le L\)，

\[
 Q\le(1-2^{-L-1})^{\lceil t/L\rceil},\qquad
 0\le H/2^t-Q<2^{-t}. \tag{5}
\]

另外固定无环链标签 \(\ell_1=0,\ell_i(g)=g_{i-1}\ (i\ge2)\)，只优化 bundles 时精确值为1/2，union 恰 \(N(N+1)/2\)。所以仅要求跨坐标依赖无环或每输出至多依赖一个其它坐标，仍允许恒定高值；未声称全部无环函数的最优也恰1/2。

证明(4)：一个 block 有 \(h=2^b\) groups，配成 \(h/2\) 对补组。每对任意 nonlinear 标签的两个支持大小均 \(h\)、恰交1点，故全部 union 至多 \((h/2)(2h-1)=h^2-h/2\)。独立 blocks 的 selected union 精确 factor，得到 \(NH\)。任意共同整数基数 \(k\) 有 \(Nk\le NH\)，给 floor 上界。

达到时每 block 内 cyclic shift。该 block 的 \(a\ne\mathbf1\) 可逆，资源只有一个 group owner；\(a=\mathbf1\) 时 kernel 为两个常向量、每 used resource 有两 owners。均分每项资源，每 group 得该 block 的 \(h-1/2\) 分数数量；跨 block tensor 给质量 \(H\) 和资源容量1。全部 Hall 子集给 \(\lfloor H\rfloor\) 的一个共同整数 matching，且 union 达 \(NH\)。这不是分别在各块先取整再相乘。(5)由 floor 与每因子 \(1-2^{-b_j-1}\) 直接得。

链例对固定 \(a\) 的矩阵是 subdiagonal 为1、diagonal 为 \(a\) 的下双对角矩阵。\((t-1)\) 阶相邻 minor 为1，det 为 \(\prod_i a_i\)，故 \(a=\mathbf1\) rank \(t\)，其余 rank \(t-1\)；\(t=1\) 直接同样成立。Union 为 \(N+(N-1)N/2\)，每 group 均分其一/二 owners 资源得 \((N+1)/2\)，Hall 与整数总 union 上界共同给恰 \(N/2\) 项。其依赖图 \(1\to2\to\cdots\to t\) 可以跨 blocks，因此不与固定大小 block 衰减矛盾。

## 6. 分块条件的普通任务边界

**Assumptions / Scope / Dependencies。** (4)只对二元对象及明示全局函数条件成立，自足使用补组交点与整数 Hall；不输入未知见证、没有物理守卫。全部对应实际调度按(1)回填所有原 jobs，但原 \(P_t\) 仍允许全局 cyclic，普通 OPT 仍 \(1+2^{-t}\)，不能改称 \(2-Q\)。一个 block 恢复裸值，singleton blocks 恢复前页逐坐标值。

条件保通常逐坐标 full-support YES 的提升，仅是类型明确的上下文：若另一个 base 的 group/state 标签也为对应二元字母，逐坐标 full-support witness 自动满足每个 block 条件。若要谈任意其它字母表，必须**另将 block 函数的定义域和值域改成该字母表的相应幂**；它不属于本二元 Claim 的量词。固定二元 base 本身没有 full-support YES。没有据此提供 source 归约或普通机器中的 coherence gadget。

**Evidence / Counterevidence / Status / Related Files。** rank先冻 Exact/Proof；rainbow仅读Exact独立证明后，才实际读作者Proof；root实际读全件并独核。上述 ancillary 非二元 typing 限定已明确，旧源字节不改，数学域不变。最终限定范围见[审查](../../reviews/unrelated_machines/binary_cartesian_block_fiber_quota_review.md)。无 standing fatal，软件none、外审/全球新颖性未认证。

## 7. 任意非线性选态的 concurrent fiber 缺项合同

**ID / Version：`UM-QARY-AFFINE-MENU-NEAR-FULL-DEFICIT-v2`。** 本版另立更强必要条件及新精确端点，旧 v1 所记录的范围与当时未闭合情况保留原字节。

**Objects / Domain / Definitions / Quantifiers。** §1全部 \(q,t\)，\(\ell(g)\) 可任意非线性。对任意全局不交 bundles，设整数 \(0\le d\le N\) 且每组 \(|B_g|\ge N-d\)。令 \(F_x=\{g:x\in S_{g,\ell(g)}\}\)，\(k_x=|F_x|\)。对任意非空 \(F\subseteq F_x\)，记 \(k=|F|\)、\(\pi_JF\) 为其坐标投影，空投影大小1。

**Exact Statement / Conclusion。** 并发族的精确 union 及遗漏预算为

\[
 \left|\bigcup_{g\in F}S_{g,\ell(g)}\right|
 =\sum_{J\subseteq[t]}(q-1)^{|J|}|\pi_JF|,
 \qquad
 kd\ge\sum_{J\subseteq[t]}(q-1)^{|J|}(k-|\pi_JF|). \tag{6}
\]

置

\[
 h(k)=(k-1)+\sum_{j=1}^t\binom tj(q-1)^j\max\{k-q^j,0\},
 \qquad
 K(d)=\max\{1\le k\le N:h(k)\le kd\}.
\]

则每 nonempty fiber \(k_x\le K(d)\)，且任意上述分配必有

\[
 \boxed{d K(d)\ge(q-1)^t}. \tag{7}
\]

\(h(k)/k\) 不减，\(K\) 有定义且可精确整数比较求出。这只是必要条件，不是最优分配算法。旧严格近满结论也保持：若 \(2d<q\)，则 \(d\ge(q-1)^t/q\)；不能把阈值等号纳入。

## 8. 全局计数、精确端点与任意实际调度

证明(6)：固定公共点 \(x=(a^0,b^0)\)。对于一个别的资源，令 \(J=\{i:a_i\ne a_i^0\}\)。若 \(i\notin J\)，则 \(b_i=b_i^0\)；若 \(i\in J\)，由 concurrency 有 \(b_i=b_i^0-g_i(a_i-a_i^0)\)。固定这些非零差值，每个不同 \(\pi_Jg\) 给不同 \(b\)，恰 \(|\pi_JF|\) 项；该 \(J\) 有 \((q-1)^{|J|}\) 种差值。分层相加得恒等式。总 incidence \(kN\) 减 union 是不可避免的重复删除，至多 \(kd\) 的遗漏预算必须覆盖它，得第二式。以 \(|\pi_JF|\le\min(k,q^{|J|})\) 得 \(h(k)\le kd\)；每项 \(\max(1-q^j/k,0)\) 和 \(1-1/k\) 随 \(k\) 不减，证明单调。

证明(7)：全体 \(N\) groups 有 \(N(q-1)^t/2\) 对逐坐标都不同的无序组，每对任意 selected supports 恰交一资源，故

\[
 \frac{N(q-1)^t}{2}\le\sum_x\binom{k_x}{2}
 \le\frac{K(d)}2\sum_x(k_x-1)_+
 \le\frac{K(d)}2 Nd.
\]

最后因为每资源最多有一个 group 领取，重复数至少需同样多遗漏，而总遗漏不超过 \(Nd\)。其它 group 对可以交很多点，只使第一个不等式更强；这里未错误假设仅这些 pairs 相交。约去 \(N/2\) 即(7)。

严格近满引理：任意两组若有 \(r\) 个相同坐标，其支持交集为空或 \(q^r\)。若 \(2d<q\)，相交的 groups 不可能在任一坐标相同，否则两端总遗漏 \(2d\) 无法覆盖交集。因此每 fiber 内每坐标互异，\(k_x\le q\)。上段的计数此时直接给 \(d\ge(q-1)^t/q\)。分 \(2d_*\ge q\) 与 \(<q\) 两种情况，最优缺项数满足

\[
 d_*\ge\min\{\lceil q/2\rceil,\lceil(q-1)^t/q\rceil\}. \tag{8}
\]

当 \(q=3,t=2\)，(8)给 \(d_*\ge2\)，cyclic 的7项/组达界，故无约束 \(V_*=7/9\)、全部原jobs实际 \(\operatorname{OPT}=11/9\)。

当 \(q=3,t=3,d\le2\)，\(h(k)\le2k\) 迫 \(k\le3\)：在 \(4\le k\le9\)，\(h(k)=7k-19>2k\)；更大 \(k\) 用 \(h(k)/k\) 单调仍排除。故 \(K(2)=3\)，\(dK(d)\le6<8\)，违反(7)。另一方面 cyclic 奇异层左度4右度3，整数 matching 给每组1个奇异资源，另有23个非奇异资源，每组共24项。因此精确

\[
 \boxed{d_*=3,\quad V_*=8/9,\quad\operatorname{OPT}_{3,3}=10/9}. \tag{9}
\]

(1)把这两端点还原为所有原 jobs 的实际调度，并对任意非线性 selector、任意未选 state exports 给相反界。不是求解器返回，不把只给 selected subset 当作完成全部任务。

**Assumptions / Scope / Dependencies / Evidence / Counterevidence / Status。** (6)的 concurrent 前提必要，不能套任意非并发 family；投影粗界不是每 \(k\) 可达到的断言。(7)不需要小 \(d\)；(8)的严格前提单独处理。一般 \(q,t\) 的无约束非线性最优仍未闭合；没有源 hardness、免费一致性或主目标反证。作者 v1/v2 Exact、对应 Proof、general 两版独立陈述先行与实际作者读后来源保留；root独核 projection 分层、双计数及整数端点。最终指定章节见[审查](../../reviews/unrelated_machines/qary_affine_menu_near_full_deficit_review.md)。数学完整、无 standing fatal；软件none、外审/全球新颖性未认证。

## 9. 显式位复杂度、证据分层与剩余承重

§1完整实例有 \(N\) groups、\(N^2\) private 机和 \(N^2\) 资源机、\(N^3\) incidence 与 \(N\) selectors，有限条目 \(2N^3+N^2\)，dense 条目 \(2N^2(N^3+N)\)。标签和普通权 \(1/N\) 位长 \(O(t\log q)\)。各明确达界选择及共同整数流只用显式图，输出全部 jobs 按总输入编码长度多项式；不是 \(\operatorname{poly}(t,\log q)\) 输出指数多对象。分块 \(H\) 的分子/分母位长 \(O(t+s)\)；给定 \(A\) 的秩求和只需显式 \(N\) 个 \(a\) 及域上线性代数。\(K(d)\) 的整数比较及二分仅计算必要条件，不求未知最优 selector。

没有新通用软件或冻结优化实验。审查者独立记录里的有限辅助计算由其自行完成，只用于 checks，不作为一般结论前提。旧 v1 近满记录写 \(q=3,t=3\) 未闭合是其当时正确范围；v2 以新证明(6)–(9)推进，不回改旧源。

这些精确界定位了可衰减的**逻辑一致性**以及无约束重选的逃逸；不能仅把禁止跨 block 的规则写入 decoder。接下来必须在真实 ordinary P 内实现相应一致性并保持 YES，或者找到可直接解码任意 partial exports 的源。这里三个 Claim 均没有满足这一主困难性义务，UM-TARGET-v1 保持 OPEN。
