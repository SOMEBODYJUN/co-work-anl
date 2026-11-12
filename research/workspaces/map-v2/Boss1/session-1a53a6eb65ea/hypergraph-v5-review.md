# hypergraph v5：Boss1 实质 3D 采用审读

审读身份：Boss1 / hypergraph_v5_adoption。审读对象为已 done 的 `boss2-wave6-hypergraph-repair-edfcf6a2548b4d1c`；本报告不是另一个主 3A 包，也不宣布目标对象的独立主覆盖任务完成。仓库只读，报告写在仓库外；无 Git、sync、checkpoint、队列操作、边或 registry 写入，无 Web，无原科学程序重跑。

**裁决：可以采用。** 新 proof 已修复本轮发现的 KS14 相关量及尾界接口问题，当前两共同前提的 ALL 推导达到 `M-9f8033b6e1a4485b97636171b09f8218` v5 整条结论。没有发现尚未支付的数学前提，宜维持 `accepted / unconditional / whole`。本裁决只绑定下列 proof、edge 与三个端点的精确版本；不把旧 proof 中的错误局部调用重新认证为正确。

## 1. 精确对象及本次阅读范围

实读了根 `AGENTS.md`、`research/IMPLEMENTATION.md` 中 3A/3D、完整 ALL、whole/contribution、实质审读和定向替代规则；当前 registry 的 exact4 源 v4、正规化引理 v1、超图目标 v5；本任务 definition、done 状态、正式 receipt 及其 12 项旧资产处置。新 `hypergraph-complete-proof.md` 全部 198 行和完整 edge JSON 已逐段实读。另读了绑定的局部修补正文、原 9fa 完整组合 proof-review、正规化引理正文与共享来源正文。

新增独立推导重点为条件期望/最大相关、原子、支撑连通性、Y/Z Fourier 谱、Gaussian 下标、两类尾界、有限 h 后的统一参数、阈值分离及完整解码接合。exact4 来源内核、typed 层化和整数 cloud 采用确实未改且本轮新 proof 完整保留的成熟数学，不重复原论文全篇证明，不冒称本次重新执行历史作者的全文阅读或科学计算。

按 PDF 技能只读冻结本地 KS14 的承重页：文本实读物理 17–26 / 印刷 16–25；目视物理 17、18、19、22、24、25、26 页，分别核定义 5.1–5.3、一般平滑/不变性接口、原分布和误式、Lemma 5.14、reverse hypercontractivity、尾界/参数与最终解码。未浏览外网。

| 绑定项 | 当前版本/状态 | SHA256 或 `rr.pin` |
|---|---|---|
| 新 proof | 完整替代局部分析 | `6cc10b9a2e31525239ee28657d6055bbb284ef808549a37f85c4e97905d10154` |
| 新 edge 文件 | accepted / unconditional / all / whole | `8df7618c7c3da76cc2df438b5670a65e24df2e1dc6fd0f4852a5a792a1aadb3b` |
| edge 的 `rr.pin` | 整个 JSON 的规范对象哈希 | `3a3a79cbe16736dcfe0af10e4dbc3f520892dbc3d637c7c3477aac82fc413a89` |
| edge `review_digest` | 已用原生函数重算 | `7f180db874bd6e8ed26cc1e3ed5d266e5e9faf05e04a7c6ef99231eabf7291f4` |
| `M-ab4a576ed0be482b89d4a646ffc102b9` | v4 | `e2f4d171f9174665027371524263e60473a991292495c0041683392feaa38077` |
| `PCP-EXACT-PROJECTION-PERFECT-COMPLETE-BIREGULAR-ROUNDING-v1` | v1 | `3fb491cd85e99950c05f1ce9bbcd8ec6daabc5bf1aae02627ef4efb4e7307922` |
| `M-9f8033b6e1a4485b97636171b09f8218` | v5 | `9bd5557d979847cb514b5b14cdf38a18213c14ba3f864dc601ab57c1f6a1c049` |

这些 pin 是从当前 registry 原对象用仓库 `research_runtime.pin` 实算，全部等于 edge 和 task 的绑定。新 proof/edge 实际字节 SHA 等于指派值。原生只读 `edge_bindings` 与 `check_edge` 通过；这只确认身份和结构，数学裁决来自以下推导。

## 2. 最大相关量必须为 sqrt(theta)

固定实际范围 `0<θ<1/2`、`r=4^h≥4`。从独立均匀 X 与初始 Y 产生 Z=−Y，以概率 θ 选均匀 J 并令 `Y_J=Z_J=−X`。

设 `S={存在 j: Y_j=Z_j}`。不修改时 S 不发生；修改时恰有一个相等坐标 J，故 S 及其 J 均可由 (Y,Z) 识别，且 `P(S)=θ`。在 S 上 X=−Y_J；S 的补集上 X 仍为独立均匀符号。因此

\[
m(Y,Z)=\mathbb E[X\mid Y,Z]
=-\sum_{j=1}^{r}Y_j\mathbf 1_{\{Y_j=Z_j\}},\quad
\mathbb E m=0,\quad\mathbb E m^2=\theta.
\]

取 `f(X)=X`、`g=m/√θ`，两函数均值零、二阶矩一，且 `E[fg]=√θ`。反向，二值均匀 X 的每个中心化函数为 cX；当其 L2 范数≤1 时 `|c|≤1`。任意允许 g 的相关由条件期望及 Cauchy–Schwarz 至多 `||m||_2=√θ`。故

\[
\rho(X;(Y,Z))=\sqrt\theta=:\rho_0<1.
\]

这不是把 θ 的一个旧上界放松而已；原 `ρ≤θ` 在实际范围内已错误，例如 `θ=1/4,r=4` 时相关为 1/2。新 proof 明确用此等式替换调用，未改真实测试分布。L2 定义不要求 g 点值绝对值≤1，所以稀有修改分支可放大 `1/√θ`，这正是原混合概率论证失效的原因。

## 3. 原子和三空间平滑界仍可用

未修改输出的每个正原子概率为 `(1−θ)/2^(r+1)`。修改输出中 J、X 与未改的 r−1 位确定该输出，丢弃的旧第 J 位有两个原像，所以每个正原子概率为 `θ/(r2^r)`。两类支撑不交，因而最小正原子准确为二者之最小值。条件 `θ≤r/(r+2)` 等价于后者较小；实际 `r≥4,θ<1/2` 严格满足。因此当前使用

\[
\xi=\frac\theta{r2^r}
\]

没有沿用原 Lemma 5.9 在任意 θ、任意正 r 下过宽的字面原子声明。

在 `((X,Y),Z)` 支撑二部图中，每个左点 (x,y) 都有未修改边连到 z=−y。给右点 z 和坐标 j，取左点 `(x=z_j,y=−z)`，它通过未修改边连 z；再修改 j 时 Y_j 本来已等于−x，左点保持同一个，而 Z_j 翻转，连到 `z^(j)`。所有右点沿超立方体边连通，全部左点亦接入。由 Y/Z 对称，`((X,Z),Y)` 同理。故 Lemma 5.2 以 ξ 支付这两个二部相关量的 `1−ξ²/2` 上界。

还要覆盖三空间定义中的 `X;(Y,Z)`，不能仅以两个连通图代替。这里 `ξ≤(1−θ)/4`，于是

\[
\frac{\xi^2}{2}\le\frac{(1-\theta)^2}{32}
\le\frac{1-\theta}{2}
\le1-\sqrt\theta.
\]

因此 `√θ≤1−ξ²/2`，三空间相关确实≤`1−ξ²/2`。三空间平滑 γ 的量级可继续使用 `νξ²/log(1/ν)`；不可把此处机械改成 `1−√θ`。原 Lemma 5.9(iii) 等式末端漏 `1−` 的印误亦已明确排除，实际使用左侧正确界。

## 4. 精确 Y/Z 谱真正支付高阶尾界

每个固定修改分支的最终 Y 都均匀，故给定 Y 后，仍以概率 1−θ 取 Z=−Y，以概率 θ 把−Y 的均匀一位翻转。转移算子在 Boolean Fourier 角色上对角化：

\[
P\chi_A(Y)=\mathbb E[\chi_A(Z)\mid Y]
=(-1)^{|A|}\left(1-\frac{2\theta|A|}{r}\right)\chi_A(Y).
\]

`0<θ<1/2` 使括号对 k=1,…,r 为正且递减，去除常数角色后的算子范数因此是 `1−2θ/r=1−η`。所以 `ρ(Y;Z)=1−η`。这比单纯引用原 `1−ξ²/2` 更强；新稿补出的直接谱计算正好支付原 Lemma 5.18 显示的强尾界。

在多 fiber 的乘积里，含至少 s 个原坐标的 Fourier 项占至少 s/r 个 fiber；各非空 fiber 的特征值绝对值≤1−η，故尾范数≤`(1−η)^(s/r)`。新取 `s≥(r/ξ)log(1/ν)` 足够，因为 `η/ξ=2^(r+1)>1`，从而该尾界≤ν；独立逐位噪声的尾界 `(1−η)^s` 更小。shattered 项每个 fiber 至多一个坐标，不同 fiber 独立，故其 Y/Z 二次型恰等于逐位负噪声 `T_(−1+η)` 的二次型。

另一个尾项为 fiber 平滑后的高阶部分，其 L2 范数≤`(1−γ)^(s/r)`。由 `s≥r/(2γ) log(32r²/τ)` 得其范数平方≤`τ/(32r²)`，逐位平滑的对应部分亦满足。两类尾项分别有实际支付，不以三空间较弱相关界偷换 Y/Z 的强衰减。

## 5. Gaussian 下标与有限常数顺序

本报告用 `\underline\Gamma_ρ(a,b)` 明确表示 Definition 5.3 的下 Gaussian 稳定性：相关系数为 ρ 的两个标准 Gaussian 同时落入一个左尾和一个右尾、边缘概率为 a,b 的概率。新 proof 虽简写 Γ，已明确指定这个“下”函数。

对任意固定 `ρ0<1` 和正 a,b，该概率严格为正，且对边缘参数连续。因此对 `b_h=(α/2)^(4/η_h)>0` 可以先取正 ν_h 足够小，使

\[
\underline\Gamma_{\rho_0}(\alpha/2,b_h/2-5\nu_h)-2\nu_h>0.
\]

新稿把 Lemma 5.14、式 (16)、(17)、(30) 的 Gaussian 下标全部改为 ρ0，把不变性影响阈值中的分母改成 `1−ρ0`；真实分布 θ 以及 ξ_h、η_h 保持原值。γ_h 由三空间界支付；τ_h 用二部 ρ0 与最小原子 ξ_h 支付。保留原 Lemma 5.14 的额外 `log(1/ν_h)` 使 τ 更小，仍是充分正阈值。一般 Gaussian、不变性和 reverse hypercontractivity 定理作为成熟工具复用，没有重新证明其内核。

具体顺序为：固定 `0<δ≤1/2`，选正有理 `α<δ`、`α<1/2`；固定 L 和 θ（可取 1/4）；有限每个 h=1,…,L−1 先定 `r_h=4^h`、ξ_h、η_h、b_h，再定 ν_h、γ_h、τ_h、s_h、T_h。之后取 `T≥max(2,T_h)`，最后取正有理

\[
\zeta<\min_h\frac{\alpha^2\tau_h^2\gamma_h^2}{2048r_h}.
\]

最后才取 exact4 源 soundness ζ/2 的常数字母表，并以正规化误差 ζ/2 构造 NO 值≤ζ的双正规源。关键是 r_h=4^h 不依赖 T，也不依赖以后选的字母表；相关空间原子只依赖 r_h。故不存在常数选择循环。h 的集合有限，各余量严格正，统一 T 与 ζ 均存在；需要编码时可在严格正开区间取有理，再向上取整整数参数。固定 δ 后虽常数极大，全部仍独立于输入大小。

## 6. 共同影响到实际 ID 解码及整条目标

新 proof 中组合接口与原 9fa 保持一致，均不使用错误 `ρ≤θ`：

* exact4 源支付 perfect YES 与任意小固定 NO 值，独立正规化保持同标签/原投影和完美性、给统一值误差≤ζ/2；两个前提必须 ALL。
* typed 有序坐标层化保独立约束身份。逐层对出入度常数，均匀 incident ID 与均匀层顶点两种测度分别得到；源值界通过固定除 distinguished 坐标外的上下文得到，平行不同投影不能去重。
* smoothness 为 `h/(Q−l+1)≤1/T`；随机逐位置转换链的层对联合分布恰为约束测度，给 weak-density。不存在简单图或常数最大度的额外假设。

从独立集权≥α，经层均匀权及 weak-density，有某层对 heavy 约束 ID 比例≥α²/64。每个独立集测试乘积逐 ID 为零。对每个下层顶点，smoothness 给不打散低度项的期望平方范数≤s_h²/T，故坏 incident 比例≤`q_h=(s_h²/T)^(1/4)`。层间双正规把该界转为所有 ID 的坏比例；新 T 条件实际给 `q_h≤α²/512`，足以保 heavy-good ID 比例≥α²/128。

在每个 heavy-good ID 上，reverse hypercontractivity 给二次型≥b_h，尾分解损失至多 `4q_h+4ν_h`，因此≥`b_h/2−4ν_h`。经两次平滑和修正 Gaussian 比较，若没有共同影响坐标，测试乘积严格为正，矛盾。于是存在 i*，上层平滑影响与 `4r_h` 倍 fiber 内下层影响和均≥τ_h。两种下层平滑的每位影响相差≤`τ_h/(8r_h²)`，fiber 至多 r_h 位，所以转为顶点自身逐位平滑后可保式 (33) 的 τ_h/2 界。

每个顶点从其自身的逐位平滑影响抽标签，总影响≤1/γ_h。上层取 i* 的概率至少 `γ_h τ_h/2`，下层取该 fiber 的概率至少 `γ_h τ_h/(8r_h)`，所以每个 heavy-good ID 的通过概率≥`τ_h²γ_h²/(16r_h)`。标签分布不依赖 incident ID；不同 ID 的好坐标无需一致。对 ID 线性求期望得某一实际层标签满足率≥`α²τ_h²γ_h²/(2048r_h)>ζ`，与每层对 soundness 冲突。不同 h 可使用各自 γ_h：解码仅在已经选定的一个层对上应用，源 soundness 对任何标签都成立。

YES dictator 着色不受分析修补影响：未改位 Y/Z 相反，改位则同等于−X，因此测试三点不单色。`r_h≥4` 且至多改一位保证 y≠z，x 又在不同层码块，是真三元边。输出重复三元边可以去重，因独立集避开全部支撑仍逐 ID 使测试为零；源约束去重不合法。

整数 cloud 使用 `B=L(∏_l n_l)2^Kmax`，每码字云大小 `Bw_x` 为正整数。clone 独立集占据的原云集合必独立，反向复制整云可达等值，故无权最大独立集比例精确等于原权最大独立集质量。复制 dictator 着色保完美性。L、T、K_l 固定，n_l、B 与完整三部展开均为输入的固定次幂。因此终点确为有限未加权 3-uniform 超图，并非只到加权或带退化边版本。

## 7. v5 阈值域、资产保留与剩余界限

任何二着色超图的一个色类至少占半数且独立，所以 YES 中最大独立集比例≥1/2。NO 是不存在比例≥δ的独立集，即最大比例严格小于 δ。故 `0<δ≤1/2` 两类分离，δ=1/2 仍合法。`K_4^(3)` 的四个三元边可按 2+2 着色，最大独立集恰为二点；对 δ>1/2 它同时属于字面 YES/NO 两类。内部选 α<δ 可保更强的 NO 输出，但不能据此认证 δ>1/2 的全域分离承诺。当前 v5、whole_result、scope、conditions 对这一点一致，源共享正文及冻结 PDF 保原字节没有妨碍精确解释。

本次核得新 receipt 的旧资产处置恰覆盖旧 9fa receipt 全部 12 项：11 项 retained 逐项 SHA 不变，1 条旧超图边 replaced 为新 proof/edge；13 项当前 assets 的实际 SHA 全部匹配，edge 5 项 evidence 的实际 SHA 全部匹配。当前 exact4→八色 edge 原 SHA `2154e7f238a0764c054b871cab7fb3ecf47bc02d57a23851d8a3dc9e98a5d27a` 保留，八色→三色为只读 canonical dependency，SHA `7fcb8fcc3c8612224e9a3af03f9cc5111e89de3e13159a0b8520ee646af56c13`。本次不重审未变的整条图链；新局部修补没有调用它们。MZ 近完美性及字母表交易不能替代 perfect exact4 或保 perfect 正规化的比较边界保持原样。

未发现阻塞数学缺口。采用时仍需保留三个边界：只认证现役 `0<θ<1/2,r_h≥4`；一般分析内核是成熟定理的复用，本次新证明支付其具体分布假设；完整逻辑支持不等于把目标对象自己的主 3A 覆盖任务改为 done。本任务当前快照是 `state=done,owner=Boss2`，嵌入 receipt 与正式 receipt 相等。receipt 的描述性 `delivery_status` 仍写 awaiting edge-check/pushed，是早期文本，不能覆盖任务实际 done 状态；本次原生只读检查已通过，无须为此重开数学修复。

## 8. 可直接进入 integration 的短数学说明

已完整审读新 hypergraph v5 proof 与绑定 edge，独立复算实际测试的 `ρ(X;(Y,Z))=√θ`、最小原子 `ξ_h=θ/(r_h2^r_h)`、支撑图单坐标翻转连通及 Y/Z 特征值 `(-1)^|A|(1−2θ|A|/r_h)`。用正确 Gaussian 下标 `ρ0=√θ` 重选解析阈值，有限 h 后统一 `T→ζ→源字母表`，原三空间平滑界、强 Y/Z 尾界及每 ID 解码率全部成立；保 perfect exact4 与独立保 perfect 双正规化两前提 ALL。typed 层化、重数测度、三个不同顶点与完整整数 cloud 保未加权整条 NO/YES 保证。当前 `0<δ≤1/2` 分离域准确，δ=1/2 亦有效；旧 11 资产原 SHA 保留、旧超图边定向替代闭合。对 proof SHA `6cc10b9a2e31525239ee28657d6055bbb284ef808549a37f85c4e97905d10154`、edge SHA `8df7618c7c3da76cc2df438b5670a65e24df2e1dc6fd0f4852a5a792a1aadb3b` 及所列当前三端点 pin，可采用 accepted / unconditional / whole；未发现新增开放前提。
