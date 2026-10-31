---
id: facility-games/common-two/shared-phi-manuscript-source-and-pdf-continuation-review-20261031
kind: review
type_tag: 审查
title: 共享目录黄金比主稿源码与 PDF 接续审查
status: complete-source-read-integrated-with-targeted-review-boundary
truth_status: internally audited manuscript claim; local modules integrated; external review and final global targeted proof status not asserted
review_level: full-clean-show-read-of-readme-tex-pdf-with-pdf-text-extraction-and-archive-comparison
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/manuscripts/shared_phi/README.md
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/manuscripts/shared_phi/README.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/manuscripts/shared_phi/main.tex
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/manuscripts/shared_phi/main.tex
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/manuscripts/shared_phi/main.pdf
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/manuscripts/shared_phi/main.pdf
evidence_paths:
  - archives/facility-games/tools/evidence/shared-phi-manuscript-20261031/manifest.json
  - archives/facility-games/tools/evidence/shared-phi-manuscript-20261031/README.md
  - archives/facility-games/tools/evidence/shared-phi-manuscript-20261031/main.tex
  - archives/facility-games/tools/evidence/shared-phi-manuscript-20261031/main.pdf
  - archives/facility-games/tools/evidence/shared-phi-manuscript-20261031/main.pdf.txt
related_objects:
  - ../../subarchives/common-two/state/定义/共同目录精确续局与菜单模型--定义.md
  - ../../subarchives/common-two/state/定理/共同目录黄金比存在与有理构造--定理.md
  - ../../subarchives/common-two/state/定理/共同目录黄金比闭环证明--定理.md
  - ../../subarchives/common-two/state/算法/黄金比有限菜单与完整续局证书--算法.md
  - ../算法/盒截面平方和的两坐标端点交换--算法.md
  - ../反例/两设施强配额的三名混合必要例--反例.md
  - ../审查/双设施黄金比稿的五处修订与待审证明域--审查.md
  - ../资料/双设施黄金比连续稿与固定菜单证明合同--资料.md

# 共享目录黄金比主稿源码与 PDF 接续审查

本审查完整读取三个冻结来源：README、权威 `main.tex` 和编译 `main.pdf`。README 与 TeX/PDF 共同声称的是**同一物理地点目录由两家带标签设施共享**的双阶段设施选址游戏，不是异构双目录模型，也不是顺序六提供者的 CAG 模型。客户权重为任意正二进制有理数，覆盖关系任意，客户独立混合并最小化包含自身重量的实现总负载，设施收益是期望吸引重量。主稿给出的目标是存在一份纯设施位置和每个有序布局的精确独立客户 NE 续局，形成黄金比 \(\phi=(1+\sqrt5)/2\)-近似 SPE；它只保证存在一套安全续局，不要求所有客户 NE 选择都安全，也不计算全体客户 NE 中的真实最小收益。

## 1. 原件身份、二进制导出与实际阅读

`clean show` 的三项来源身份如下，两个冻结提交的同路径版本均保留：

| source ID | 路径 | blob | clean-show 字节 | SHA-256 |
| --- | --- | --- | ---: | --- |
| `f0cc3496a6277623df8c` | `history/source/manuscripts/shared_phi/README.md` | `b8b203c064b9ee98d156e8d57f631232e275fcea` | 2094 | `56ec96cd080b3bd201bbbd719d0da45b0a08bdd6e4ec354f801fad55ae3a43bd` |
| `aa18a3ff0dc1264b143a` | `history/source/manuscripts/shared_phi/main.tex` | `45d2fb1aed3fa80d4941c5c63eb02422e1f3aec6` | 69758 | `a3c0fc0b04fa8a1866189231196d3684cbad3f3da0d0da98355daf6108b4f2ad` |
| `9c23f7107d94e5d719b2` | `history/source/manuscripts/shared_phi/main.pdf` | `b8062f52860fbfc1bfaba9e78686a3ebe85805de` | 301420 | `cd60cfbf31160da3a706a9a147429973a786ecb2fa602ef08656929c809516f1` |

原件已分别保全到 `archives/facility-games/tools/evidence/shared-phi-manuscript-20261031/`，并由 `manifest.json` 记录原件与证据副本的字节和哈希。PDF 使用 `pdftotext -layout` 导出为 `main.pdf.txt` 后逐段阅读；Python `pypdf` 读取到 25 页，PDF producer 是 pdfTeX 1.40.25，creation date 为 2026-09-30。README 报告两遍编译、25 页 A4、无 TeX 错误、未定义引用、盒溢出或警告；该编译结论是来源自报，本批没有把它当作新运行证明。源码、PDF 文本和 README 的标题、章节顺序、算法复杂度与附录结构一致。

README 明确写出“内部审计、没有外部同行评审或接收声明”；本审查保留这一限制。当前仓库另有较早的 26 页修订审查记录，本批实际冻结的 shared_phi PDF 是 25 页，不能把两个阶段的页数或哈希混写。

## 2. 主稿的完整数学内容

### 2.1 模型、主定理与菜单接口

主稿先定义有限非空共享目录 \(S\)、有限客户集合、正权 \(w_g\) 和任意覆盖集 \(C_s\)。两家设施同时选 \((s,t)\in S^2\)，允许同址；被至少一家覆盖的客户必须在可达设施中独立选择一家，未覆盖客户不服务。对固定布局，若共同客户选择第一设施的概率为 \(p_i\)，私有负载为 \(A,B\)，则

\[
L_1=A+\sum_iw_ip_i,\qquad L_2=B+\sum_iw_i(1-p_i),\qquad
\Delta=L_1-L_2,
\]

客户均衡条件是

\[
p_i=1\Rightarrow\Delta\le w_i,\qquad
p_i=0\Rightarrow\Delta\ge-w_i,\qquad
0<p_i<1\Rightarrow\Delta=w_i(2p_i-1).
\]

主稿 Theorem 1 声称：对显式列出的 \(N\) 个共享地点和 \(n\) 名正二进制有理权客户，确定性算法在 \(O(N^2(n+1)^4)\) 次有理运算和多项式中间位长内，构造黄金比近似 SPE。输出是一份在轨客户 NE、至多 \(2N-2\) 个实际单方偏离续局以及给所有其他布局使用的多项式默认纯续局规则。主稿同时声明任意正实权的存在性版本，但位复杂度只适用于显式有理输入。

每个无序地点对预先固定同一菜单并在标签反转时反射：

* **P（guarded pure seeds）**：两种全共同客户单侧种子和每名共同客户的两个 singleton 种子；只有原低侧每个共同客户权至少初始负载差时才执行最大严格改善客户修复，严格改善使用 `w < gap`，首次反转或无改善停止。
* **E（equal-reach half split）**：若私有负载相等，每名共同客户独立以概率 \(1/2\) 选第一侧；它在同址给 \((R_s/2,R_s/2)\)，但不被误写成任意同 reach 都满足 \(qR_s\) 的强目标。
* **T（two designated mixers）**：选择两个指定共同客户，其他客户放在高覆盖侧；令 \(D=B-A+Z\)，当 \(D\le\min(w_h,w_j)\) 时指定者在低侧概率为 \((1+D/w)/2\)。边界概率和等 reach 的两方向均保留。
* **C（strong chord）**：当两 reach 为 \(U\ge V>cU\)、共同总重小于 \(qV\)、最大共同权不超过 \(aU\) 时，调用局部强弦构造，输出 \(L_U\ge qV,L_V\ge qU\)。主稿明确它必须允许三名或更多客户混合，不能把局部问题截断成纯或至多两混合者。

令 \(u(s,t)=\min_{e\in F(s,t)}L_s(e)\)，令 \(d(t)=\max_{s\in S}u(s,t)\)，其中最大值必须在完整共享目录上计算。若某菜单成员满足

\[
L_s\ge qd(t),\qquad L_t\ge qd(s),
\]

则对每个真实单方偏离分别选坐标最小的菜单成员，因两个带标签偏离布局族在轨外不相交，可以补成完整 \(\phi\)-SPE；其余布局使用 P 的默认修复。该配额判据与现行 `独立续局的威胁配额与双颜色回应核心` 的抽象对象相同，但主稿的全局难点在于证明某个环上菜单成员一定满足它。

### 2.2 闭回应环、归一化和纯修复

主稿按任意 `b(t) in argmax_s u(s,t)` 画响应函数图，假设每个响应环位置对菜单都无法满足配额，取环上最大 \(d\) 归一化为 1。它特别声明：归一化后 \(R_s,d(s)\) 的上界只对环内点成立，\(d(s)\) 仍然是完整目录威胁，不能改成环内最大值。借助同址 E，得到环点 \(d(s)>cR_s\)、\(R_s<2q\)，每条响应边上任意菜单成员的回应负载 \(P\ge d(s)\)、原位负载 \(Q<qd(t)\le q\)。

纯修复部分逐步证明：从原高侧向原低侧搬严格改善客户时，负载差严格下降，选择的客户权重不增；首次翻转后新差小于最后搬动者，原低侧客户和早先搬动者都稳定，因此输出纯 NE 且保留原低侧负载下界。该证明明确区分原低侧标签、当前低侧和等号客户，不能用 `w <= gap` 代替严格改善。全共同客户单侧种子保证每个菜单非空。

### 2.3 大客户、星形和公共客户 \(h\) 的两锚闭环

主稿先证明：若环上可见客户权重至少 \(q\)，其可达性沿响应边传播至整个环；把重客户留在源点、其他共同客户放响应点的 singleton 种子将源负载至少推到 \(q\)，与失败配额冲突，因此环上可见客户均小于 \(q\)。再将大客户阈值取为 \(q/2\)，证明每个环点至多两名大客户、大客户对两两相交、同一大对不能出现在同一响应边两端，三角形大对族被排除，非空大对族只能是星形。

最大 reach 首边只能把恰一名共同客户 \(h\) 送往响应点；两名会违反 \(R_s<2q\)，零名会使原位负载至少 1。于是

\[
H=R-Q>R-q\ge aR>q/2,
\qquad H<q,qquad K=R-H<q.
\]

对于含 \(h\) 的地点，向上弦 singleton/修复给出 \(u(t,s)\le R_t-H\le K\)。当响应威胁大于 \(q\) 时，先反证 reach 不下降，再证明唯一运输：只有 \(h\) 向前，其他共同客户总重严格小于 reach 降幅；这使 \(h\) 对所有其他混合概率严格偏好响应点，其他共同客户严格偏好源点，故此时所有真实客户 NE 唯一，菜单最小值等于唯一响应收益。主稿并没有把一份纯成员未经严格支配就当成全 NE 最小值。

两锚覆盖引理设唯一运输边 \(X\to Y\) 的 reach 为 \(x>y\)，\(\delta=d(X)=y-\sigma\)、\(\epsilon=d(Y)\)、\(B=\phi(y-H)\)，并要求 \(\delta>B,\epsilon>B,\delta>\phi H,\epsilon\le y\)。若另一个含 \(h\) 地点满足 \(B<R_t\le y,d(t)\le B\)，对两个锚分别放置 singleton/修复，迫使两个其他共同集合的重量均超过相应阈值；容斥后得到 \(R_t<L=q(\delta+\epsilon)-H+\sigma<B\)，矛盾。再结合“无 \(h\) 地点高 reach 会给强弦见证”的分支，主稿逐一排除非退化星、空大对族和单大对族，得到任何闭响应环都必有配额见证。

### 2.4 任意多共同客户的强弦和局部必要三混合

主稿附录 A 将局部强弦归一化为大 reach 1、低 reach \(r=1-\delta>\phi/2\)，共同总重 \(C<qr\)，每名共同客户权不超过 \(a\)。将目标改写为负载差区间 \([-Z,U]\)，并用共同客户坐标 \(c_i=w_i(2p_i-1)\) 表达均衡。它明确给出：至少三名指定混合者时，正 gap 的质量界为 \(C\ge\delta+5d\)，负 gap 为 \(C\ge5e-\delta\)，因此三混合本身达到强弦配额；但三混合不是总是自动存在，仍需最大平方交换或后续纯修复。

主稿保留一个明确的局部必要例：私有负载 \((40,39)\)，三名共同客户权均为 20，reach 为 100 与 99。纯 NE 负载 \((60,79)\)，两混合 NE 为 \((79,60)\)，都不能达到 \((99q,100q)\)；三人以概率 \(39/80\) 选第一侧时 gap 为 \(-1/2\)，负载 \((277/4,279/4)\)，达到目标。该例只证明“强弦证明不能只搜至多两名混合者”，不构成全局 SPE 反例。

当除最大权客户 \(x\) 外的总重至少 \(\delta\) 时，主稿在盒截面上执行两坐标端点交换：输出一个局部平方和端点，使最多一个坐标内部；令最大客户坐标等于该内部坐标即可得到 NE。附录 B 证明枢轴权在改变时严格下降，固定枢轴时反号客户权严格上升，移动总数 \(O((k+1)^3)\)、扫描总算术 \(O((k+1)^4)\)，但它不声称求全局凸函数最大值。主稿甚至给出 (14,13,19) 的局部端点值 582 小于另一顶点 654 的示例，以强调算法只需要交换不变量。

主稿的正 gap、负 gap、第三混合者、递减前缀、最大权和纯修复分支都逐项给出；当其余权重总和小于私有差时，固定最大客户在低 reach 侧，并用 \(L_B-L_A\le x+S-\delta<x\) 证明它在所有中间纯分配中始终稳定。该固定客户不变量和三混合必要例已被当前仓库的局部算法/反例对象单独吸收，可脱离全局黄金比闭环使用。

## 3. 与当前存档对象的比较和状态边界

| 主稿内容 | 当前对象 | 本批实际确认 | 不应升级的部分 |
| --- | --- | --- | --- |
| 共享目录模型、精确独立续局、黄金比主张 | `common-two` 定义与黄金比定理 | TeX/PDF/README 三者一致，覆盖同址、任意覆盖和正权 | 这是内部稿，不是外部审稿或期刊接收证明 |
| P/E/T/C 固定菜单、全目录 `d` 和偏离证书 | `黄金比有限菜单与完整续局证书` | 逐家族阅读并核对标签反射、严格 guard、三混合 C 条件 | 菜单最小不等于全客户 NE 最小；不以有限证书替代菜单完备性 |
| 大客户对、星心、两锚、任意环排除 | `共同目录黄金比闭环证明` 及 G1/G2 对象 | PDF Sections 3--13 与现行正文结构一致，局部接口已归档 | 现行 `双设施黄金比稿的五处修订与待审证明域` 仍要求 cycle transport 与 polynomial constructor 的定向复核；本批不改状态 |
| 强弦多混合和交换算法 | `盒截面平方和的两坐标端点交换`、三混合反例、局部强弦对象 | PDF Appendix A/B 给出完整公式、分支和位长合同 | 源 README 的“无警告编译”不是复杂度或全局证明；未重跑独立实现 |
| 25 页 PDF 与权威 TeX | 新证据目录 `shared-phi-manuscript-20261031` | pypdf 页数、metadata、PDF 文本和 TeX 章节均核对 | 不能与旧 26 页修订稿的 hash、review 或 source refs 混用 |

现行存档中 `common-two/state/定理/共同目录黄金比闭环证明--定理.md` 和 `common-two/state/算法/黄金比有限菜单与完整续局证书--算法.md` 已把主稿数学接口拆成可复用对象，状态标为 `established-with-scope`。另一方面，`archives/facility-games/state/审查/双设施黄金比稿的五处修订与待审证明域--审查.md` 明确保留针对 cycle transport、强弦多项式构造、等号分支和五处修订的 targeted review 边界。两者并不冲突：前者记录当前内部正文的可复用证明合同，后者拒绝把“读完主稿、有限模块通过或 PDF 编译成功”升级为外部验证。本文按较保守的后者边界处置，新增源不改变任一状态字段。

## 4. 来源独有内容、缺口和接续

本批共享目录主稿相对于现有对象的独有可复用内容包括：

1. **完整连续版本。** README、主 TeX 和 PDF 同时给出 25 页权威叙述，能够核对旧 Markdown 分节与最终主稿的对应；它们不是仅有摘要或旧 ledger。
2. **强弦算法的局部端点合同。** 附录 B 不求凸平方和全局最大值，而是给出盒截面顶点初始化、枢轴变更降权、固定枢轴反号升权和 \(O((k+1)^4)\) 有理运算界；这与旧“存在性取全局最大点”的算法路线必须区分。
3. **三混合必要性与固定最大客户不变量。** 三名权 20 客户的 40/39 例和 `L_B-L_A<x` 的逐状态稳定性为局部强弦对象提供可独立复查的教材级边界。
4. **任意长环的证明合同。** 主稿显式保留“环内 reach/d 上界、全目录 d 最大值、两类带标签偏离族不相交、严格唯一性只在需要处证明”的量词，适合作为第三阶段关系证据的接口。

仍然保留的数学缺口是：能否在仓库现有独立复核要求下，对整个任意长闭环的所有菜单归属、星形/三角排除、双锚分支和附录 A/B 的所有端点、零值、等号、时间与位长步骤做一次定向证明审查。当前有限菜单回归、强弦 support 枚举或 PDF 中的 theorem 标签均不足以替代该工作。主稿本身也明确不求实例最优黄金比，不做全客户均衡最小值，不处理不同目录或任意非线性客户费用。

本批三源已全部实读并保全。建议第三阶段引用关系为：`共同目录黄金比主稿` → `固定菜单/双配额证书` → `大客户星心/双锚闭环` → `强弦多混合算法`；与 `异构双目录通用因子二`、`单交叠 rho` 和 CAG 半覆盖保持模型分离。任何后续摘要都应同时写出“共享目录”条件、正权/强制参与/独立混合条件和“存在一套续局”量词。

本批未执行 Git commit、push 或 `clean done`；Boss 串行 checkpoint 后再按 receipt 逐来源确认。
