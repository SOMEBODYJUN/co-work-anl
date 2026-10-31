# 正规高围长部分MinRep源v3：陈述先行独立重构

审查者：内部子研究者pcsp_occurrence。只读了`regular_high_girth_partial_minrep_v3_exact_statement.md`，实际读前SHA256为`0e2b614ae0a0af12c592d3b57558e2c3baf13cf4377b90b26769fc6e5d24cc61`。未读root的新证明、row/hardness的v3稿或向其询问证明。

来源边界：我是旧v2 source的作者，已经知道cheap-list生成函数计数和rare-tail思路；因此本审查不声称对此整个研究方向无先验。下面两侧permutation witness、cycle及repair证明是仅据v3 Exact自行重构。没有运行软件、没有抽样实验、未核任何新的外部PCP原文。

结论：在Exact列出的全部对象域下，没有发现standing fatal；第1–4项可由以下自足推导闭合。第5项的Q=poly(g) PCP起点仍调用既有外部来源，不把本次陈述先行审查冒作重新审过全部PCP论文。

## 1. 参数、完整copy lists和平均覆盖

沿用Exact记号。t=Dz，N′=Nt，M′=dtN/2=dN′/2。每层每个原顶点的t个template slots恰被一份uniform permutation重命名，所以每个copy在每层恰有一条边，union恰为d-regular；原type在每层有z条边。无论原图是否有平行约束均成立。

固定一份实际copy multilabeling ψ，cost≤gNt。各copies的lists可以完全不同。对原type e=(u,v)，记p_e为独立均匀抽u的一份copy和v的一份copy时，二者lists覆盖此投影的概率。每个模板边初始covered的边际概率恰为p_e。

下面不把“平均copy list”错误地当成cost≤gN的某一个旧game multilabeling。取H=4g/τ，标记长度>H的copy list为heavy。heavy copies总数≤gNt/H。原game D-regular，因此按均匀原type及均匀端点copy计，遇到heavy端的概率至多2g/H=τ/2。

逐原顶点独立抽uniform copy，再在其非空list里uniform取label；空list任取合法label。所得是原game上的真实随机单label赋值，所以其平均value≤γ。若随机端点对两list均非heavy且覆盖此type，选中一对兼容labels的概率至少1/H²。因此

\[
\frac1{|E|}\sum_e p_e
\le\frac{2g}{H}+\gamma H^2
=\frac\tau2+\frac{16\tau}{1000}
<\tau.
\]

这里γ=τ³/(1000g²)。每type恰有dz个模板边，故若对全部M′个模板边分别记p_f=p_type(f)，则Σ_f p_f<τM′。两侧抽copy相互独立是承重条件；原左右顶点是不同的permutation对象，即使n=1也没有混为同一随机变量。

## 2. 两侧permutation相关性：有界度witness代替独立Bernoulli

固定ψ，令X_ψ为初始union中的covered边数。不能将其视为独立Bernoulli和。

若X_ψ≥ρM′/2，把这些covered模板边视为以“原顶点、layer”为顶点的二部multigraph。其最大度≤t。由二部multigraph的t-edge-coloring，取最大的ceil(t/2)个颜色，得到至少一半covered边，且每个(原顶点,layer)的degree≤ceil(t/2)。故存在一个全部covered的模板边子集F，满足

|F|=s:=ceil(ρM′/4)，每个(原顶点,layer)至多ceil(t/2)个F-incidences。

仅用edge-coloring的存在性作概率witness，不要求算法枚举所有ψ或给其着色。

现在固定这样的F，依次暴露其模板端点的permutation images。template在每层是perfect matching，所以同一个permutation里的被询问slots两两不同。每步每侧尚有至少t/2个未使用copy编号。条件于全部先前的**具体images**，剩余permutations仍分对象独立且uniform。因此下一条type e边被覆盖的条件概率至多

\[
\frac{t^2p_e}{(t-a)(t-b)}\le4p_e,
\]

其中a,b为该两份permutation已暴露slot数。这个界对任意先前具体images都成立，故条件于先前仅“covered”事件时仍成立。于是

Pr[F全部covered]≤∏_{f∈F}4p_f。

对所有允许的F作union，并放宽到全部size-s模板边子集：

\[
\Pr[X_\psi\ge\rho M'/2]
\le4^s e_s(p_f)
\le\left(\frac{4e\sum_fp_f}{s}\right)^s
<\left(\frac{16e\tau}{\rho}\right)^s
<g^{-2s}
\le\exp[-(\rho M'/2)\ln g].
\]

这里16e<100，因此16eτ/ρ=16e/(100g²)<g^(−2)。ceil(s)只加强阈值；ρM′很大但本论证本身对真实阈值也没有整数漏洞。

全部cost≤gN′的copy lists数K由生成函数满足

K≤e^{N′}Q^{gN′}≤exp(gN′λ)。

又ln g≥ell ln2>ell/2、d≥1000gλ/(ρell)，所以

(ρM′/2)ln g=(ρdN′/4)ln g>125gN′λ。

初始union中存在任何cheap copy-list覆盖≥ρM′/2的概率小于exp(−124gN′λ)<0.001。此为对全部copy lists的同时性；允许最终lists依赖随机输出，不能只读作固定ψ保证。

## 3. 短cycle期望，含原parallel types与2-cycles

先条件于所有permutation draws成功。此时各原顶点、各layer的permutations仍独立uniform，见第6节。

令X_l为初始图长度l的simple cycles数；l=2指两条不同parallel edges，不把单边往返算cycle。任何实际cycle在每个copy处相邻两边的layers必不同，因为一层是perfect matching。

对长度l≤G的候选cycle，先枚举原root/type闭walk、各copy编号及layer序列。其数量上界为

N D^l ·t^l ·d^l。

每个type/layer模板边有z种preimage index选择，故再乘z^l。合法cycle中，同一原顶点/layer需要不同template slots映到不同copy编号；若slot要求碰撞则事件概率为0。设各permutation涉及m_j个不同images，Σm_j=2l、m_j≤l，其联合概率为∏1/(t)_{m_j}，上界为(t−l)^(−2l)。于是

\[
\mathbb E X_l
\le N d^l\left(\frac{t}{t-l}\right)^{2l}.
\]

这里用Dz=t，没有误把同原vertex两侧或同layer随机变量当作独立。

参数给t≥z>4U，而d≥2、G≥2时U≥2G²（由Σ_{j=0}^{G+1}2^j的初等界）。所以t>8G²，且

−2l ln(1−l/t)≤4l²/t<1/2。

因此(t/(t−l))^{2l}<2，得到EX≤2N Σ_{l=2}^G d^l=2NS。B=40NS，所以Pr[X>B]<0.05。此上界同样包含原图parallel types；它们只增加原type-walk枚举数D^l，不破坏distinct layer这一实际cycle必要条件。

## 4. 同type、同layer的repair总能找到f

始终保留边的original type与layer标记。每个bucket恰有z条边。初始X≤B时，假定当前没有增加短cycles，则当前X≤B。

某bucket中处于任何当前长度≤G cycle的边至多GX≤GB。需排除f任一端距e任一端≤G的边。底层图最大degree≤d，e两端半径G的balls合计顶点≤2Σ_{j=0}^G d^j；将其所有incident edges都计入，也至多2dΣ_{j=0}^Gd^j≤2U，故Exact的4U是充足的保守上界。在同layer实际上每个顶点只有一条边，界还可更小。

z>GB+4U+1，故确有符合条件f。四端点不同；任一新cross edge此前若存在，会使其端点间原距离为1，违反远距条件，因此不会新建parallel edges。

交换两边在同type/layer bucket内进行，保持所有copies每层degree1、总degree d、边数M′和各bucket大小z；两新边仍连接同一对原root vertices并继承其原投影。

## 5. repair不生短cycle与全部lists的统一误差

设e=(a,b)、f=(c,d)，换为(a,d)、(c,b)。若新短cycle只含一条新边，其余部分给e端与f端之间长度≤G−1的旧path，违反远距。

若新短cycle含两条新边，删去两新边后分成两条旧paths。若paths分别连接(a,c)、(b,d)，同样违反远距；另一配对是(a,b)、(c,d)，后一路与旧f构成长度≤G的旧cycle，违反f不在任何短cycle。故没有新短cycle。移除e至少破坏所选旧cycle，因此每步X至少减1，至多B次就结束。没有需要额外随机搜索的repair失败分支。

每次移除两旧边、加入两新边，对任意固定ψ其covered数增加至多2。故所有ψ同时有

covered_final(ψ)≤covered_initial(ψ)+2B。

参数z≥8B/(ρm_*)且t=Dz≥z，给M′=tm_*≥8B/ρ，即2B≤ρM′/4。若第2节同时性好事件成立，最终每个cheap ψ覆盖严格少于3ρM′/4，尤其严格少于ρM′。此误差界与ψ及repair选择都无关。

最终无2-cycles，故simple；无长度≤G cycles，故girth>G。YES时把每个原顶点label复制到其全部copies，每个原type边及同type修复边都满足，因此每个非FAIL输出perfect-complete。

## 6. capped Fisher–Yates与概率常数

uniform整数draw总数K₀=dN(t−1)。每次以ceil(log₂bound)位拒绝采样，成功概率>1/2（bound为2次幂时为1），连续R次失败概率≤2^(−R)≤1/(2000K₀)。union bound使任一draw耗尽的概率≤1/2000。

各draw使用独立随机bit blocks；其bounds由Fisher–Yates步骤编号预定。条件于全部draw成功，每个接受值仍是对应range上的独立uniform整数，因此所有permutations条件分布恰为所需独立uniform分布。不能用未条件的“近似uniform”替代此点。

于是全部合法输入FAIL概率≤1/2000+0.05<0.1。NO时再并第2节的<0.001坏事件，得到非FAIL且最终cheap-list禁令的概率>0.948，强于Exact所需0.8。概率常数没有依赖存在某个低cost旧copy代表。

## 7. Qgamma≥1与固定G总位复杂度

若val≤γ，则必Qγ≥1，因为任意左单labels配uniform右labels给value期望1/Q。Exact把该条件列为所有输入的显式域约束，而非在算法中只对NO使用。

由Qρ³≥10⁹g⁸以及ρ≤1，数值g≤Q、1/ρ≤Q，故d≤1000Q²λ+1为显式Q的多项式数值上界。Q由非空原图上的显式投影表计入输入；原N、D也由显式D-regular无权图控制。

固定G时S、B、U、z、t均是这些数值的固定次多项式。尤其z中的1/ρ无需按其可能二进制巨大数值在无界域内循环，域约束已经使该数值≤Q。构建t copies、d layers和长度t数组因而确为总位多项式。R=O(log(dNt))，随机bits硬上界O(dNt·R·log t)也为多项式。

枚举全部长度≤G的cycles、每次计算必要balls、扫描bucket，以及至多B次repair，均在固定G下为显式输出规模的多项式。若binary G也作为变化输入，这种指数依赖G不再是统一poly，Exact已明确不作该合同。

## 8. 适用边界

本次接受的是Explicit-game随机source定理；没有提供源到UM的真正编译。第5项固定参数PCP起点、Q=poly(g)外部事实仍按既有来源记录；可通过复制labels让Q≥1/γ以满足合法域，不提升value。

新图不是任意给定finite cover自动保soundness的声明：每copy总degree是d，type次数通过随机层分配，证明靠本稿同时性与有限repair。旧UM配置证书可在某些覆盖上整数化的障碍没有被否定。

最终状态：无standing fatal；已完成陈述先行一般数学重构，尚未读root冻结证明；无新软件运行或外部新颖性认证。
