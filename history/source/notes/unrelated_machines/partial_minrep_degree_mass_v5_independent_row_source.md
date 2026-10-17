# 度数比例 copies 正规化：v5 陈述先行独立重构与域修正记录

读取目的：核任意不正规、两侧不等、typed alphabet 源的真实 copy 预算、周期概率、纤维继承及固定参数 PCP 接口；不读作者新证明。

## 实际读取、修正与顺序

先实际 SHA、全文读 v4 Exact：`degree_mass_copy_regularization_v4_exact_statement.md`，SHA256 `45c1d754332fc556066b994bffbda407bd2d619a05a77a539969f5ef2dc66b38`。

审查者独立发现其字面域没有明确排除 \(\Sigma_A=\varnothing\)、\(|\Sigma_B|\ge2\)：此时空投影表仍可被叫作全函数，但原单标签赋值集合为空，val 未定义。该缺口已在收到任何作者证明前发给 root。v4 冻结字节不改，不能记为字面完整域获证。

随后收到并实际 SHA、全文读修正版 v5 Exact：`degree_mass_copy_regularization_v5_exact_statement.md`，SHA256 `86dcd98daaa2cc479260e444f47f4e9eb3d8ae56936b220f0a1d18e82863d693`。其只加两侧 alphabet 均非空，已知是针对上述问题的修正；算法、参数和其余结论未变。

本记录冻结前没有读取 root 或其他人的 v4/v5 新证明、推导或审查，也没有询问他们。已核的前一正规输入源 v3 证明可用，但下面重新核不正规质量分布和 variable fibers 的不同之处。

结论：修正后 v5 的 1–5 可独立重构，未发现进一步 fatal objection。v4 的原字面域缺口仍保留为已发现并修正的问题。

## 1. 复制质量与完备性

删除孤点后每个原顶点度数至少 1，且 \(M_0\ge1\)。令 \(t_v=\deg(v)z\)。两侧分别有
\[
 \sum_{a\in A}t_a=M_0z=\sum_{b\in B}t_b,
\]
所以 output copies 自然平衡，不要求原两侧顶点数相等。按每 incident edge type 分 \(z\) 个 slots 后，各 type 两端 slotwise 配对；每个 slot 用且仅用一次，因此 template 为 perfect matching。每层重命名保持 matching，每个 copy 在每层度数 1，故初始多图精确 \(d\)-正则，\(N'=2M_0z\)、\(M'=dM_0z=dN'/2\)。每 (type,layer) bucket 恰有 \(z\) 条 matching 边。

边始终连接原 type 的原左点和原右点的 copies，且投影表原样继承；原完美标签赋给所有相应 copies 即全满足，任意同 bucket switching 也保持此性质。左右 alphabet 是各自原 alphabet，无须相同；没有构造反向函数。exact \(k\)-to-1、surjective 或 equal-fiber 等逐投影属性因此原样保存。

## 2. 真 copy 预算下的平均覆盖

固定任意 output copy lists，总成本 \(\le gN'\)，同一原点的 copies 可使用完全不同列表。对原边 type \(e=(a,b)\)，令 \(q_e\) 是独立均匀选 \(a,b\) 各一个 copy 时，该对 lists 覆盖原投影的概率。令 \(\beta=M_0^{-1}\sum_eq_e\)。

取 \(H=4g/\tau\)，称长度 \(>H\) 的 **copy list** 为 heavy。heavy copies 总数至多 \(gN'/H\)。在均匀选择原 edge type、两端分别均匀选 copy 的试验中，一个固定左 copy \((a,c)\) 被选中的概率为
\[
 \frac{\deg(a)}{M_0}\frac1{t_a}=\frac1{M_0z}=\frac2{N'},
\]
右侧同样。这正是 degree-mass 复制的承重抵消；没有假设原点预算是未加权 \(gN_0\)。因此某端为 heavy 的概率至多 \(2g/H=\tau/2\)。

若 \(\beta\ge\tau\)，light 且 covered 的边/copy 对概率至少 \(\tau/2\)。每个原点独立均匀挑一份 copy list，并从其非空列表中均匀选一个标签；空列表任取合法标签（v5 的非空 alphabet 在此必要）。一个 light-covered 见证 pair 被选中的概率至少 \(H^{-2}\)。所以某个原单标签赋值满足边比例至少
\[
 \frac{\tau}{2H^2}=\frac{\rho^3}{32\cdot10^6g^8}>\gamma,
\]
与 NO 假设矛盾。故 \(\beta<\tau\)。

每层每 type 恰 \(z\) 条边、端点的 fiber permutations 独立均匀；覆盖边数 \(Z\) 的期望因而为
\[
 \mu=dz\sum_eq_e=M'\beta<\tau M'.                  \tag{1}
\]
所有质量都来自实际 copies 总预算。没有要求随机挑选一个 copy 后的原列表总成本必定 \(\le gN_0\)。

## 3. 不同 fiber 长度下的全部列表同时上尾

对长度 \(t_v\) permutation 的 \(r\) 个不同 slots，真 images 相对于独立均匀有放回抽样的点态密度至多
\[
 t_v^r/(t_v)_r\le e^r.
\]
该界与 \(t_v\) 的统一取值无关。任意 \(k\) 个不同 (layer,templateedge) 恰涉及 \(2k\) 个不同 (permutation,slot)；每层 template 为 matching，保证不存在重复 slot。独立各 permutations 并与 with-replacement 模型比较，固定这 \(k\) 边同时覆盖的概率至多 \(e^{2k}\prod q_e\)。因此
\[
 \mathbb E\binom Zk\le(e^2\mu)^k/k!,\qquad
 \mathbb E(1+s)^Z\le\exp(e^2\mu s)\quad(s\ge0).
\]
与原 v3 相同的 Chernoff 优化给
\[
 \Pr[Z\ge\rho M'/2]\le(e^3\mu/(\rho M'/2))^{\rho M'/2}
 \le\exp(-\rho M'\ln g).                           \tag{2}
\]
\(\mu=0\) 时直接概率为零。

typed alphabets 的真实 token 数是 \(M_0z(|\Sigma_A|+|\Sigma_B|)\le N'Q\)。用 \(x=1/Q\) 的生成函数，成本 \(\le gN'\) 的所有 copy lists 数至多
\[
 \exp(N')Q^{gN'}\le\exp(gN'\lambda).
\]
所以式 (2) 对全部 copy lists 同时失败的概率至多
\[
 \exp(gN'\lambda-\rho dN'\ln g/2)
 \le\exp(-249gN'\lambda)<10^{-3}.                   \tag{3}
\]
这里 \(\ln g\ge\ell/2\)、\(d\ge1000g\lambda/(\rho\ell)\)。不同 fiber 大小、两侧 alphabet 大小均没有增加遗漏的 entropy 因子。

## 4. 短 cycle 的 variable-fiber 抵消

\(t_v\ge z\ge2G+1\)。固定起点 copy 和长度 \(l\le G\) 的 layer word，simple cycle 要求循环相邻层不同。沿 prefix 逐步揭 matching 边；每条边同时揭其配对 slots 的两个 images，已揭 slots 对 template mate 关系封闭。若 prefix simple，则末步当前点及起点在末层的对应 matching 端未揭，末步 template mate 也 fresh。

如果末步落入起点的原 fiber \(v\)，其目标 image 均匀于至少 \(t_v-G\) 个未用 copies；否则闭合概率为零。因此起点在原点 \(v\) 的固定 copy 时，闭合概率至多 \(1/(t_v-G)\le2/t_v\)。对这个原 fiber 的全部 \(t_v\) 个起点求和抵消，得到
\[
 \mathbb EX_{\rm cyc}\le\sum_{v}\sum_{l=2}^G
       \frac{t_vd^l}{t_v-G}
 \le2N_0S.
\]
所以 \(\Pr[X_{\rm cyc}>B_0]\le1/20\)。该抵消只付原非孤点个数 \(N_0\)，不付最大 degree 或最大 fiber；平行 2-cycles 仍是两个不同 layers 的正常项。

## 5. switching、全部列表统一误差与成功概率

短周期总数 \(\le B_0\) 时，处于任一短 cycle 的边数至多 \(GB_0\)；也可使用至多 \(GB_0\) 个短 cycle 顶点这个更强排除条件。当前图 maxdegree \(d\)，从所选 \(e\) 两端的半径 G 球总顶点数至多 \(2\sum_{j=0}^Gd^j\le2U\)。bucket 是 matching，触碰这些禁点的 bucket 边数至多禁点数。故 \(z\ge GB_0+4U+1\) 保证合格 \(f\) 存在。

交换保每层 matching、每 bucket 大小、type 和投影。若新短 cycle 只用一条新边，其余路径违反端点距离；若用两条新边，删后路径配对要么违反远离，要么在旧 \(f\) 两端间给出短路径、使 \(f\) 属于旧短 cycle。故没有新短 cycle，每次至少消掉一条旧 cycle，至多 \(B_0\) 次。最终 bipartite 且无 2 到 G 周期，故 simple、balanced、exact \(d\)-regular、girth \(>G\)。

任意列表族一次覆盖增加至多 2，故全修复后增加至多 \(2B_0\)。这次精确使用 \(M'=m_*z\) 和 \(z\ge8B_0/(\rho m_*)\)，有
\[
 2B_0/M'\le\rho/4.
\]
所以式 (3) 的初始全列表同时事件推出最终所有成本 \(\le gN'\) 列表覆盖严格 \(<3\rho M'/4<\rho M'\)，包括修复后可能根据图另选的 lists。

Fisher–Yates 实际 draws 数 \(K_0=d\sum_v(t_v-1)>0\)，因为所有 \(t_v\ge2G+1\ge5\)。每 draw 的耗尽概率严格小于 \(2^{-R}\le1/(2000K_0)\)，所以 sampling FAIL 概率严格小于 \(1/2000\)。条件全部 draws 成功时接受值仍独立均匀。与理想均匀模型耦合，所有输入的 FAIL 概率至多 \(1/20+1/2000<0.1\)。NO 时再并界式 (3) 的坏事件，返回非 FAIL 且满足最终同时 NO 的概率严格大于 \(1-1/20-1/2000-1/1000>0.8\)。没有要求这些事件独立，也没有把每个非 FAIL 输出都称为 NO 好输出。

## 6. 固定 G 总位复杂度

\(Q\gamma\ge1\) 给 \(10^9g^8/\rho^3\le Q\)，因而 \(g\)、\(1/\rho\) 和 \(d\) 的数值都由显式 Q 的多项式控制。输入把 alphabet 和投影表显式列出，Q 被输入长度支付；原每个 degree 至多 \(M_0\)，且 \(N_0\le2M_0\)。固定 G 时，\(S,B_0,U,z,t_v,N',M'\) 均为输入长度的多项式值，指数允许依赖 G。

所有 rational ceil、比较、参数计算均可用位长多项式的整数运算。有限拒绝预算给硬随机位上界 \(K_0R\max_v\lceil\log_2t_v\rceil\)。显式枚举区分平行 edge IDs 的长度 \(\le G\) cycles 可用 \(O((N'+M')^G)\) 次数级的直接实现；每次找 \(f\) 与 BFS、至多 \(B_0\) 次交换仍为固定 G 的多项式。输出全投影表的代价也被显式规模支付。没有添加 UM 矩阵或把可变 G 指数隐藏为 uniform poly。

若 \(Q\gamma<1\)，原随机均匀两侧单标签赋值的满足率是 \(1/|\Sigma_B|\ge1/Q>\gamma\)，所以非空全投影域中不可能有 \(\operatorname{val}\le\gamma\)。这没有消除 v5 非空 alphabet 要求；它只在 val 已定义后成立。

## 7. synchronous alphabet padding 和 PCP 接口

对任意整数 \(L\ge1\)，把两侧标签同步复制为 \((\alpha,s)\)、\((\beta,s)\)，投影 \((\alpha,s)\mapsto(\pi_e(\alpha),s)\)。丢掉一份新单标签赋值中的 s，所有原来满足的新边仍满足旧投影，所以新 value 不超过旧 value；反过来旧最优标签在所有点用同一个 s，满足率不变。因此 value 恰相同。若旧投影每个右标签有恰 k 个原像，则新右标签 \((\beta,s)\) 仍恰有 k 个原像 \((\alpha,s)\)，exact fibers 和 surjectivity 均不变。

可取 \(L=\max\{1,\lceil1/(Q\gamma)\rceil\}\)，使新最大 alphabet \(Q'=QL\ge1/\gamma\)。这项作为固定 \(g,\rho\) 的 PCP 族转换时 L 是常数，因此不需原 PCP 的 degree、biregularity 或两侧平衡。不得由此额外宣称在非法小 Q 且变化 binary 参数时输出该 padding 仍为参数位长的统一多项式。若原 \(Q=\operatorname{poly}_\rho(g)\)，则最小 L 给 \(Q'\le Q+1/\gamma=\operatorname{poly}_\rho(g)\)，所以仍有 \(d=O_\rho(g)\)。若只用一般 fixed-error PCP，则只能称字母表及 d 为固定常数，不能凭空给其随 g 的 polynomial 定量。

若某 PCP 定理只给 alphabet 大小的常数上界而各实例大小未固定，exact k-to-1 使左右大小比固定为 k。需要一个公共 exact degree 时，可把常数范围内的右 alphabet 大小的公倍数作为公共右大小，使用同步复制并重命名，依旧只乘固定参数常数；无需添加会改变 value 的 junk labels。

对实际新来源，本审查者先前已经通过浏览器实际读取 ECCC TR26-179 rev2 的 Definition 1.1 和 Theorem 1.6（官方 PDF，2026 revision 2）：其 d-to-1 定义使用精确等大 fibers，Theorem 1.6 给任意固定误差的 perfect-complete 4-to-1 判定困难性，原图允许平行约束。这里只导入该原陈述，未重构其长篇 PCP 证明。官方原文：<https://eccc.weizmann.ac.il/report/2026/179/revision/2/download>。

因此在固定 \(g,\rho,G\) 后取误差 \(\le\gamma\)，通过必要的同步 padding 和本变换，确实得到 simple、balanced、constant exact d-regular、固定高 girth、exact 4 fibers 的随机源。它已不再需要一个未提供的原 PCP 正规化前提。FAIL 按 YES 处理，NO 好事件概率至少 0.8，所得反证假设是 \(\mathrm{NP}\not\subseteq\mathrm{BPP}\)。这是源接口闭合，仍无一般 UM compiler。

## 冻结结论

v4 的字面域缺口已独立指出并由 v5 修正；修正后 v5 的质量、概率、cycle repair、bitpoly 和条件 PCP 接口均重构完成，无进一步 fatal objection。本文冻结后才可读作者新证明，并另记实际 SHA/比较结论；未运行有限实验、未执行 Git/Work、未认证外部新颖性。
