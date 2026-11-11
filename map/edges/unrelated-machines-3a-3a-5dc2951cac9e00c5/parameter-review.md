# Dinur–Steurer 平行重复到 Set Cover / partial-MinRep 的参数接口

本轮对象为 `M-aa8493282cc64a7ca8ec31430eb5e8af`。结论只在有限两玩家投影游戏、独立抽边并逐坐标全部接受的通常平行重复中使用。不是普通游戏值直接乘法，也不是一般不相关机或共同目录 SPE 迁移。

## 1. 实读和原始证据

冻结 `parallel_repetition.pdf`（SHA-256 `7a7d2fcb62e173dabed10d69faa1e522055a811a228b707ab94f3e88b28dfdd5`）实读 Theorem 1.1、Corollaries 1.2–1.5、§2.1–2.3、§3.1、Theorem 4.1 及其 threshold-rounding/correlated-sampling 证明、§4.1 的 Theorem 4.7、§6.1–6.2。PDF 印 5 页 Theorem 1.8 与印 24 页 Theorem 6.4 证明另经渲染图像确认。不是只读摘要，也不声称完整复审少量重复 Theorem 1.7。

冻结 `moshkovitz_setcover.pdf`（SHA-256 `51072837058066469129fdc62ad6b16725bce6ea97dfeb2110172b464cdfa1d7`）定向实读 Theorems 1.2、2.1、2.3、Lemma 4.4、Lemma 4.7、Corollary 4.8、Lemma 4.9、Claim 4.10 及 Theorem 1.2 的参数收尾。另实读 MinRep 度数正文的模型、generic 稀疏化、参数修复及 partial-MinRep v2 / high-girth v3 正文。所有扩读端点由 Boss 追加为本任务只读依赖。

## 2. 核心界、大小和两个值区间

对任意投影游戏 G、整数 k≥1、0<r≤1，若 val(G)≤r，原论文 Theorem 1.1 / Theorem 4.7 给出

\[
 \operatorname{val}(G^{\otimes k})\le
 \left(\frac{2\sqrt r}{1+r}\right)^{k/2}.
\]

承重链为 Claim 2.3 的 `val(G)≤||G||≤sqrt(val(G))`、Theorem 3.3 的 `||G⊗H||≤val_+(G)||H||`、Theorem 4.1 的

\[
 \operatorname{val}_+(G)^2\le
 \frac{2\|G\|}{1+\|G\|^2}\le\frac{2\sqrt r}{1+r},
\]

及 `val(G^{⊗k})≤val_+(G)^k`。Theorem 4.1 先把非负向量赋值逐 slice 变成 deterministic fractional assignment，threshold-rounding 支付 `1−sqrt(1−t²)` 损失，再用逐点归一化和 correlated sampling 拼成全局赋值；这里逐点最大分母不能换成平均分母。

若 r=1−ε，0<ε≤1，令 t=sqrt(1−ε)，则

\[
 \frac{2t}{1+t^2}=1-\frac{(1-t)^2}{1+t^2}
 \le1-\varepsilon^2/8,
 \quad
 \sqrt{1-\varepsilon^2/8}\le1-\varepsilon^2/16.
\]

所以高值界为 `(1−ε²/16)^k`。另去掉分母得到小值界 `(4r)^{k/4}`；只有 r<1/4 时这一简式本身严格小于1，r≥1/4 时它仍正确但可能平凡。精确主界对所有0<r<1仍非平凡。

若显式游戏编码长为 L、共同字母表大小 Q、边数 M，k 重复的字母表是 Q^k、边记录 M^k，显式投影表总长至多 L^{O(k)}。perfect YES 逐坐标复制保留；二部正规度数分别乘成原度数的 k 次幂。不能把 k 随输入增长时的 L^{O(k)} 一律称为统一多项式时间。

## 3. 概述中 φ 的最小勘误及影响

原草稿审读时概述把 Theorem 1.8 写为 `φ(x)=2x/(1+x)`；印5页和印11页原图/文本均为

\[
 \phi(x)=\frac{2\sqrt x}{1+x}.
\]

最小修订是只在该中间式补根号，冻结 PDF 不改。当前核心已为 v3，绑定正文已经按此补上根号；本轮复核复用该修正，不把历史错误描述为仍存在的现行陈述。原错误式在0<x<1更小，故它声称了未获来源支持的更强 collision 收缩，不可当作已付证明。登记核心的 Theorem 1.1 主界与两个推论本来正确，不需降低其 truth_status。精确主界以上述 val_+ 的 Theorem 4.1 / 4.7 证明链为依据；不能把修正后的较弱 Theorem 1.8 直接代入 `||G||≤sqrt(r)`，就冒称得到了完全相同的精确常数。

## 4. Set Cover 的已付局部贡献

端点为 `M-4db1e9e555294998a207d584ce22485f` 及 `M-a324d647caf14545974f47d8cd0096c8`。先给定具有 perfect completeness 的显式 projection Label Cover 基础源 H，NO 值≤η²（0<η<1/2）。小值界给

\[
 s:=\operatorname{val}(H^{\otimes k})
 \le(4\eta^2)^{k/4}=(2\eta)^{k/2}.
\]

这解释 Moshkovitz Theorem 2.3 所用参数：其 η 与本定理的原值上界 r 不是同一个量，实际取 r=η²；MR PCP 的规模 `n^{1+o(1)}poly(1/η²)` 仍可写作 `n^{1+o(1)}poly(1/η)`，原字母表指数依赖也必须按 η² 代入。

**条件：**重复后游戏已满足 Moshkovitz Lemma 4.4 的 B-degree 为固定 prime power D 的幂等前提。若 NO edge soundness≤s，令 ζ=sqrt(s)/D，Lemma 4.4 给 B-degree D、ordinary agreement soundness≤2ζD²=2D sqrt(s)。再由单独登记的 Lemma 4.7 平方损失桥，任意每点至多 ℓ 个标签的 list-agreement 错误≤

\[
 2D\ell^2\sqrt s\le2D\ell^2(2\eta)^{k/4}.
\]

所以选择 `2Dℓ²(2η)^{k/4}≤β` 得 list-agreement `(ℓ,β)`。这一联合贡献同时需要重复界和列表桥；不能拆成任一源单独提供全部局部结论。

例如 ℓ≤C(log n)^a、η=(log n)^{-b}，取固定整数 k>8a/b，并使 b 足够小以让 MR 基础字母表仍为 poly(n)，则对充分大 n 满足任意固定β>0，显式重复规模仍为 poly(n)。这一步没有使用 DS Theorem 6.4 印刷证明中的错误 k/2 指数。

本边只交上述 soundness 局部贡献。完整 Set Cover 定理还须由目标论文的 MR PCP 构造、合适 degree 预处理、Lemma 4.4、partition system 和 Claim 4.10 支付。终点 universe 大小为 `N_SC=|B||U|`，不是 SAT 输入 n 或重复前 Label Cover 大小；`|U|≈|B|^{1/β}`，令内部β相对所求α足够小后，才得到 `(1−α)ln N_SC` 和 `N_SC=n^{O(1/α)}`。本边不把平行重复单独当成完整 Set Cover hardness。

## 5. 冻结 Theorem 6.4 证明行的额外常数修复

印24页原图实际以 `k=3c/α`，`ε₁=((3c/α)ε^α)^{1/c}`，再把 Corollary 1.3 写成 `(4ε₁)^{k/2}`。正确推论是 k/4；沿印刷参数只得常数倍 `ε^{3/4}`，不足以证明≤ε。这是原证明行的常数问题，不能导入关系。

一个显式修法是固定整数 `k=max(1,ceil(8c/α))`，取 `ε₁=(k ε^α)^{1/c}`。当ε足够小时，ε₁合法，且

\[
 (s_1)^k\le\exp(k/\varepsilon_1^c)=\exp(1/\varepsilon^\alpha),
 \qquad
 (4\varepsilon_1)^{k/4}
 =4^{k/4}k^{k/(4c)}\varepsilon^{\alpha k/(4c)}
 \le\varepsilon.
\]

最后一步因指数至少2且常数固定。固定α时，输出规模仍为 `n^{O(1)}poly(1/ε)`；ε不趋零的区间另用原文 Theorem 6.2 的固定参数处理。如此恢复 Theorem 6.4 的定性结论，不主张冻结 PDF 已经写了这一修法。

## 6. partial-MinRep v2/v3 的已付局部贡献

给定固定0<ε₀≤1、固定基础字母表Q₀≥2，以及显式 balanced regular total-projection 游戏 H，YES值1，NO值≤1−ε₀。写

\[
 q=1-\varepsilon_0^2/16<1,
 \quad\gamma=\rho^3/(10^9g^8),
 \quad k=\left\lceil\frac{\ln(1/\gamma)}{-\ln q}\right\rceil,
\]

其中g≥2、0<ρ≤1。高值重复界给 `val(H^{⊗k})≤q^k≤γ`；YES仍perfect、total projection与balanced regular仍保持。字母表 `Q=Q₀^k`，`k=O_{ε₀}(log g+log(1/ρ))`，因此固定ρ下 `Q=poly_ρ(g)`，v2中的 `λ/ℓ=O_ρ(1)`、`Δ=O_ρ(g)`（所有常数还可依赖固定基础源）。

v3附加域 `Qγ≥1` 也不可遗漏，而且必须同时保证YES与NO输入合法。这里 `q≥15/16`、`Q₀≥2`、`γ≥q^k`，故 `Qγ≥(Q₀q)^k≥(15/8)^k>1`，对两个promise均已付清。另在非空total-projection NO输入上，独立均匀两端标签给通用基线 `val≥1/Q`，也可复核这一域；但不能只用NO基线忽略YES输入合法性。

该贡献只支付 v2/v3 外部 source 接口中的 **平行重复放大步骤**。存在基础 perfect-complete PCP、把其度数/字母表整理成上述正规共同域仍是外部前提；有了实际显式输入后，v2删边 theorem与v3随机lift/repair theorem各自给其全部列表、成功概率和输出性质，不是平行重复本身提供这些性质。v2保每seed YES及至少0.9概率的全cheap-list NO；v3保固定围长参数G、FAIL<0.1及至少0.8概率的non-FAIL全cheap-copy-list NO。

基础输入长L时重复输出为 `L^{O(k)}`。先固定g,ρ,ε₀后这是关于SAT输入的多项式；对随SAT输入增长的二进制g不推出统一多项式归约。其随机source的算法排除保留 `NP⊄BPP` 类假设，不改成单纯P≠NP。这里没有UM矩阵、低载decoder或physical fee实现。

## 7. 另外三项 MinRep 比较的处置

`M-8b63c8bed3d44f34a50cc846cc98d80a` 的主硬度需要 Chan 固定参数PCP、近完美误差δ及正规化，再使用 `M-8c360a7779154480879e38c65d1f827e` 的全边MinRep稀疏化；它不是只靠本重复定理给出的完美singleton源。其字母表 `O(g^4 log²g)`、degree `O(g log g)` 不能由上段较粗 `poly_ρ(g)` 免费得到。

generic 稀疏化的 NO 条件是严格 `val<Γ`，门槛为 `0.06N/sqrt(Γ)`；如果重复只得到 `val≤γ₀`，须另取Γ>γ₀（如5γ₀/4）再代入。YES近完美时还需误差δ满足δΔ≤1才能得成本2N；重复不会把近完美自动变perfect，不能跳过误差预算。

`M-fb633f3a6f1448fbbd63bfc7c3806c40` 恰记录 Minzer–Zheng 这一δ预算和严格Γ修复。其 δ≤1/d、正规化、log³g 核算均独立于本重复界。当前比较不发布DS单独推出这三项MinRep结果的逻辑边，也不把其不同的all-edge/partial-edge、YES与随机量词混在一起。

## 8. 当前 v3 定向复核与复用范围

2026-11-11，Boss4/fresh-um-two-worker 读当前本任务、核心 v3、全部七个共享端点的完整 registry 记录及原两条边、receipt 和本 review。核心当前 registration pin 为 `744e82f6dc08ae52f2228358b8e98c308aaf6293629634d42511e79013d9192b`。本轮完整读当前 PCSP/DS、Set Cover、MinRep 三篇整理正文，以及 partial-MinRep v2、v3 的任务所列全部现行正文/审查/后缀证据；原成熟证明继续复用，未重新运行科学搜索或复审外部 Chan/MR PCP 的所有证明。

本轮直接从冻结 PDF 用 `pdftotext -layout` 重抽 DS pp.3–5、p.20、p.24，确认 Theorem 1.1/Corollaries 1.2–1.3、Theorem 4.7、Theorem 6.4 的参数行；重新渲染并查看 p.5 的 φ 根号及 p.24 的错误 k/2 指数。另读已有 DS 提取全文中 Claim 2.3、Theorem 3.3、Theorem 4.1 的承重入口，保留原已成熟 threshold-rounding/correlated-sampling 证明的复用范围。本轮直接重抽 Moshkovitz PDF pp.6–8，读 Lemmas 4.3–4.4、Definitions 4.5–4.6、Lemma 4.7、Corollary 4.8 与 partition-system 接口。直接重抽 Manurangsi PDF pp.4–7，核近完美 YES、严格 NO 和稀疏化量词；重抽 Minzer–Zheng PDF pp.60–61，核 δ=1/g、Lemma 7.12 及 Theorem 7.13 应用行。对这三项 MinRep 对端继续复用成熟正文中的自足修复，不把本轮读相关两页宣称成 106 页全文复审。

两个贡献的数学内容不因 φ 修订而改变：Set Cover 分支从 Theorem 4.7 的精确主界/小值推论出发，另用 Lemma 4.4 与独立的 ℓ² 列表桥，保留 ALL；partial-MinRep 分支由高值推论给输入放大，另核 YES/NO 共同的 Qγ≥1 与固定参数复杂度。两条都只是 conditional contribution；上述其余上游与目标自身证明义务仍按各自 remaining 保留。当前任务没有额外 follow-up 对；七个已读比较端点的逐对处置已写入同任务 receipt.closed_overlaps。
