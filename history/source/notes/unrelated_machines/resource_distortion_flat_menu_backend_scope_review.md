# 逐资源畸变接口的双外部后端、未知目标及位复杂度审查

## 1. 严格的实际审查顺序

1. 只收 root 给的数学陈述，独立写成 `resource_distortion_review_before_proof.md`，冻结 SHA256：`ea0619f9244d6e4a6e5fe97bdfc799bd1101fb533ba4af60fc7de09a57a01155`。
2. 冻结后，才实读 `source_promise_decoder_draft.md`。当时该文件只有域、S1/S2 陈述与 PaperFact，没有作者证明。因此这次阅读不登记成“完整作者证明读后”，也不追认发现作者证明中的漏洞。
3. 独立实现并运行 tiny-input 全枚举，见第 4 节。
4. 另实读 Cheng–Mao arXiv:1905.06084 原 PDF 定义、Theorem 1、其后 binary-search 说明、§3 Build/Collapse、§4.3 Lemma 18 和 Appendix A 的 node-disjoint-path 算法；仅导入外部定理，不宣称独立重证全文。

读前冻结文件不再修改。当前文件专门记录更强后端的依据和审查范围。

## 2. α>6 与 α>4 的准确差异

| scope | 外部原始依据 | 精确可导入内容 | 本地回译结论 |
|---|---|---|---|
| 弱版 α>6 | Davies–Rothvoss–Zhang, *A Tale of Santa Claus, Hypergraphs and Matroids*, arXiv:1807.07189v4, Theorem 3 | 每个固定 ε>0，restricted Santa Claus 的实际 6+ε 近似；组合算法可确定化，固定误差下多项式迭代 | 对每个固定 α>6，完整 flat、W≤1、逐资源正项畸变 κ 的 S1 |
| 强版 α>4 | Cheng–Mao, *Restricted Max-Min Allocation: Approximation and Integrality Gap*, arXiv:1905.06084v1, PDF 物理第 2 页 Theorem 1 | 每个固定 δ>0，restricted max-min allocation 的实际 4+δ 近似；时间 poly(m,n)·n^{poly(1/δ)} | 同一构造、同一证明，直接把 S1 的固定 α>6 放宽成固定 α>4 |

强版并非引用 DRZ 旧版错误的 4+ε 分析。DRZ v4 §4 记有旧错误更正；这里更换成另一篇原始论文的正式 Theorem 1。

Cheng–Mao 原文 PDF 物理第 2 页明确使用 \(v_{pr}\in\{0,v_r\}\)：每件资源有公共固有值，玩家只决定是否感兴趣。这与读前构造的 resource、baseline、dummy 礼物逐项完全匹配。该定理是实际 allocation 算法，不是仅积分间隙或估值。配置 LP 作比较对象反而更强；真实整数最优值不大于该 LP 值。

**当前结论。** 接受 Cheng–Mao Theorem 1 的已发表算法定理，并作第 3 节的标准精确算术实现后，α>4 的限定 S1 可闭合。没有新增关于一般 UM 的算法、困难性或新颖性结论。

原始链接：

<https://arxiv.org/abs/1905.06084>

<https://arxiv.org/pdf/1905.06084>

<https://arxiv.org/html/1807.07189v4>

## 3. 不把未知目标与二进制输入留成免费 oracle

### 3.1 确定性与数字运算

Cheng–Mao §3 的状态是实际 matching、thin-resource 子集及层列表。Build 只需检查玩家 addability、资源 active 状态、资源值的子集和，按固定顺序添加再删除冗余资源可选 inclusion-minimal edge。玩家 addability 通过最大 node-disjoint alternating-path 个数定义；Appendix A 给了相应确定性增广算法。Collapse 也是集合更新与这些路径操作。没有随机采样步骤；固定所有“arbitrary”选择的输入次序和 matching/flow 的确定性平局规则即得确定性实现。

参数固定后，关键比较仅为有限个原输入权重的和与固定有理阈值的比较，或者整数集合大小比较。原资源权重不被每一轮迭代乘上新因子。设目标 t>0，以 v_r/t 作规范化即可；这些数的总位长仍为原输入及 t 位长的多项式。Signature 中的对数只用于证明迭代次数，不要求程序做精确超越数比较。

可以为任固定 α>4 先固定有理 δ>0，使 β=4+δ<α。Lemma 16/18 证明中的参数可取固定有理 γ、β_block=γ²、μ=γ³。例如

\[
\gamma=\min\{\delta,1\}/100
\]

已确保其所需的严格不等式

\[
\frac{1-3\gamma^3}{4+10\gamma+4\gamma^2+3\gamma^3-\gamma^4}
>\frac1{4+\delta}.
\]

因为交叉相乘后的差为

\[
\delta-10\gamma-4\gamma^2-(15+3\delta)\gamma^3+\gamma^4>0.
\]

δ≤1 与 δ>1 分别代入 γ=δ/100 和 γ=1/100 即得；不需要计算任何随输入增长的微小实数常量。Lemma 18 给的组合迭代数是固定 δ 下的多项式，每步上述有理运算按位也为多项式。

### 3.2 总的目标程序

令辅助 Santa 实例的真实最优最小效用为 V。将全部礼物有理值清分母得整数实例；公共分母 Q 的位长至多各分母位长之和。缩放后的 V 为整数，因为有限 allocation 的效用都是整数。令 U 为全部整数礼物值之和，V≤U，log(U+1) 为输入位长的多项式。

对一个整数 t≥1，运行目标版 Cheng–Mao 组合算法；先把单件值截为 min(v_r,t)，再规范化目标为 1。若原来存在最小效用≥t 的 allocation，截断仍保留该 allocation 的 t-可行性：每名玩家要么有一件值≥t 的礼物，要么其所分礼物总值不变。因此其 CLP(t) 也可行。外部证明此时保证在多项式轮数内找到实际效用≥t/β 的分配。

为使对所有错误猜测也总停机，硬编码 Lemma 18 给出的固定参数多项式时钟；超时或不合格输出均记 FAIL。实际输出要精确验证不交性、资格与最小效用≥t/β。只用正确实例上已证的时间界，所以

\[
V\ge t\Longrightarrow\text{成功},\qquad
\text{成功}\Longrightarrow\text{有真实效用}\ge t/\beta,
\qquad\text{FAIL}\Longrightarrow V<t.
\tag{2}
\]

这不需要验证指数大小 configuration LP，也不需要把“算法失败”解释成任何比式 (2) 更强的证书。错误猜测上成功是允许的。

### 3.3 不要求成功标签单调的整数二分

初置 lo=0 并保存任意零下界 allocation；hi=U+1，所以 hi>V。中点 t 成功就置 lo=t 并保存实际分配，否则置 hi=t。区间每次缩半，不变式 hi>V 始终成立，因为只有 FAIL 才减小 hi。结束时 lo=hi−1≥V（V 为整数），所以保存的分配效用≥lo/β≥V/β>V/α。若 V=0 且无成功，初始任意分配已满足保证。

有些小于 V 的目标必须成功，某些大于 V 的目标也可能成功；这些标签不必单调。上述整数不变式已经足够。调用次数 O(log(U+1))，目标与被规范化礼物值的位长均多项式。时钟对错误目标保证总时间，不调用未实现的精确 CLP 分离器。

故本地新增物品的 binary-rational 表、未知 OPT、固定 α 与随输入增长的 κ 四个接口均已逐项付费。这里只完成数学实现规格，没有端到端生产程序。

## 4. 独立 exact arithmetic 有限审计

程序 `resource_distortion_independent_audit.py` 不导入作者实现，也不实现任何外部 Santa 近似算法。它构造完整原 jobs、独立枚举每份原调度求真实 OPT，再枚举辅助 Santa 的所有正资格 allocation，逐个读出无 dummy state，回填全部原 jobs，并核查真实机器负载。

完整枚举域：2 组、每组 2 个 states、2 个资源，每个 p∈{0,1/2,1} 且每行 W≤1，共 6⁴=1296 份。另加 5 份边界：空资源、singleton states、全零与 unused resources、W<1/异分母以及巨大分母。

实际通过结果：

- 1,301 份原输入；1,328,275 份完整原调度；20,798 份辅助 allocation。
- 逐份核查辅助最优值 V_aux≥(2−OPT)/κ。
- 所有 allocation 的完整回填均满足 C≤2−该 allocation 的最小效用。
- 对 α=41/10 及 α=7，分别有 10,770 份满足相应 α-近似前提的辅助 allocation，全部满足两段 S1 不等式；这些测试中观察到最大比率 3/2。
- 测试 κ 最大为 2147483647/100003；原 OPT 值包括 1、7/6、3/2、2。

脚本冻结 SHA256：`7f90a221b45117a00192f77dd6cd58e0dfa2f7a910a79dd37254cca783cccf57`。实际 JSON 为 `resource_distortion_independent_audit.json`，记录精确计数与软件实现限制。

有限检查不证明一般数学结论；外部 α>4/α>6 算法均未实现。审计不包含重复 (state,resource) incidence；读前证明对这类扩域的说明只是一项另可核查的数学观察，不把它冒充作者原域或已跑测试范围。

## 5. 对 near-two 源的准确筛选

固定 κ0 后取任固定 α>4，得到本完整 flat 域上的真实 (2−1/(ακ0)) 近似。因而若某确定性 NP-hard gap 归约声称其全部输出都在本域、κ≤κ0、YES 时 OPT≤1、NO 时 OPT>2−δ，且固定 δ<1/(ακ0)，则比较实际输出与 2−1/(ακ0) 可判源；在 P≠NP 下这种归约不能成立。

这不证明所用 Label Cover 等源易解，也不证明一般 UM 不存在算法。κ 必须在完整原 state 表上计算；只检查 witness 选择的 states 会失效。若归约随固定目标改善量改变 κ，必须逐个比较实际 α、κ 与 δ；仅说“κ 是某个常数”并不足以排除所有固定比例的归约。随机归约另需匹配其成功概率与错误方向的复杂度假设，不能只写 P≠NP。
