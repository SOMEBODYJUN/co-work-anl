# 原 k⁴-tiny 19/10 canonical：实际全文 final-read

日期：2026-10-18。审查者：`/root/sol_nsw_independent_attack`。仅 scratch，不修改任何旧记录或 repo。

## 1. 当前精确字节与实际范围

实际新读取的是

`/workspace/scratch/038d9dcc4cac/multi_outer_single_state_tiny_home_rounding_final_v1.md`

实核 SHA256 `84d6031655ac43d9c5726ed2cac6f5241e709743232290e604d767602613778a`，17086 bytes、175 行、0444。分 **1–90、91–175** 两块实际完整阅读，均无输出截断，包括身份 header、全 11 节、source-gap 推论和软件范围。

此前收到的 `sol_general_repair_multi_outer_tiny_home_canonical_draft_v2.md` / 8138cf… 只是 pointer，**没有实际打开**；root 给本最终字节后我直接读最终版。没有打开页内 related/review links，也没有打开作者代码、stdout、root replay 文件、其他人的新审查或新 repo canonical。以下数学判定针对 84d603…，不是仅核 whole SHA 或借旧稿签名。

## 2. 真实审查顺序与角色

1. 先完整读 32 行新 Exact `38c85ffed433edc9742f2e523ae39c820dc315454262a498ff8386b0b6cc001a`，作者 Proof 未开放；独立构造不同的强凸势/有理投影方案，冻结 `sol_multiouter_single_state_tiny_home_19_10_independent_exact_first.md`，SHA `c063799d1cfa38db6f05cd14f47bc728136dd6766856e4956f9cbe5570a2549a`，205 行，0444。
2. root 回报实际全文读完该记录后才释放原作者 Proof `ce05c7d5fb99d78da44a802578ca33c5ba383b15f6fe0c3a64424ff088c00332`；我实际分 1–100、101–193 行读完其全 193 行，另冻 `sol_multiouter_single_state_tiny_home_19_10_author_read_after.md`，SHA `567b9e1153ecfb15b2ff14013a14e52df73a5acefe7585fe2e5652fdfb7483d0`，146 行，0444。该记录逐核其不同的 MW+Efron–Stein+实际请求位 CE 方案，无 fatal。
3. 随后我与 root 讨论并另写给定 product law 的 vector-variance 及 entropy/固定偶矩候选。那些是我参与作者工作的**不同合同**，不是本 canonical 的新独立证据，也未移入此正式 ID。
4. 现在实际全文读本 175 行 final，作知情 canonical 一致性与准确 scope 复核。没有声称第二次 blind，也不独立认证自己的后续新 lemma。

旧两个冻结记录不改。本记录支持的仍是原 Exact/作者 Proof 的 k⁴ 域；历史其他对象的反例不因本页通过而追认或撤销。

## 3. Header、对象与输入/输出量词

正式 ID 为 **UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-19-10-APPROX-v1**。第 7 行明确只覆盖原 38c85… / ce05c… 的 k⁴-tiny 合同，排除另一个 k² vector lemma。身份各 fields 实际读完，Objects/Domain、Quantifiers、Exact Statement、Assumptions、Scope、Conclusion、Dependencies、Evidence、Counterevidence、Status、Related Files 与正文相符。

输入仍是任意正整数 k 个 outers，每个恰一个原 indexed state，所有正 homes 物理互异、每 home 恰一个 unit-own helper，fallback 只正值于与全部 homes 不交的 B，没有额外 groups。positive w 和为 1，ν=max w<=1/(4096k⁴)。没有多 state outer、重合 home 或把 helper 的多个 own-home choices 当 singleton 的放宽。

零 incidences 可原样具有资格，但最终放原 private；它们没有被当正 home 支持。重复 fallback indices、无 fallback helper、unused resources 均保留。每 state/resource 至多一个 incidence 承重于请求 coins 和有限事件后端。

普通矩阵仍有 S+U 原机器、G+I 原 jobs、S+2I finite endpoints；selector 与 payload 一律原不可拆 jobs。只给 Q，自己建矩阵、求解有理 LP、输出每个原 job 的原 finite machine 标签。k、state 数、支持宽度和分母任意二进制长度都不在次数常数中。每 outer 至少 4096k⁴ 个正 homes 是显式输入限制，不是免费复制或无损归一化。

没有出现我另外构造的强凸势算法，也没有混入 k²/偶矩新候选。最终算法确为原作者的 MW+逐资源规则+平方势请求位 CE。

## 4. 实际值桥、LP 与 FAIL 分支

OPT=2-V 的页内正反向证明完整：正向不删 inactive jobs；反向 C<2 使资源 unit jobs 至多一枚，selector 的所选 state 输出量至少 2-C，只保留这部分即可形成 disjoint allocation。OPT=2、V=0 的边界处理正确，unit selector 给 OPT>=1。

epsilon=15/16 的完整 common primitive-SA1 从 Q 显式生成：所有原 A/Z 的 boxes、gates、partitions、资源 cap1、perspective quality 及每个原 primitive/补的全部乘子用同一对称表。integer actual allocation 的真实 products 给必要性，不依赖 raw fraction 的免费 product pullback。普通有理 LP 有多项式编码、可精确判 infeasible/返回位长多项式点，无 PSD/CONFIG/unit-FSLP oracle。

FAIL 时 V<15/16，所以 actual OPT>17/16；全部 incidence private 加任意合法 selector 的完整 baseline C<=2，ratio<32/17<19/10。没有把 FAIL 当更强的 integral feasibility decider。feasible 分支只构造 C<=19/10，借 actual OPT>=1 得近似比，无免费 actual benchmark。

## 5. 同一 packing、MW 与原逐 i 的 k⁴ 方差

第 4 节的 own singleton equality EA_0=EZ_0 确由 quality×(1-Z)、gate×A、gate×Z、box(1-A)×Z 得到；只用共同二阶。outer 单 state 迫 EA_i=1、home cap 给 f_j>=x_j，故每 outer 的 sum w f>=epsilon。同一 LP 点的 fallback α/ζ 满足质量门槛及全部 helpers 共享的逐资源 cap1，alpha=0 不作 0/0。

CDF oracle 真正按实际请求者排序。formula (5.2) 对同 helper 的 alternatives 求和，只跨其他 helpers 作乘积；threshold union 的 sum<=1 来自同一全局 ζ cap。它给 a=1125/2048，而非各 outer 自己另拿一份容量。

N=1024k、eta=1/32、lambda=(7/8)p+1/(8k) 的 MW 逐 outer 均值下界 757/1792>2/5 与原 Proof 一致。所有 g 分母来自同一固定 helper law/payoff 的 D0D1，lambda 只改变 orders；(32D0D1)^N 的位长随 N 线性增长，归一化、比较等仍总位多项式。

第 7 节保留原逐 i 方差：给 X 后仅各资源独立 rule，d_u<=ν、sum d_u<=k，故 Var(W_i|X)<=νk；替换 helper j 的整个实际 state/coins profile 时，score ratio<=8k，含 j 所属 outer 本身的变化，总 |Delta W_i|<=16kw_j，Efron–Stein 给 Var F_i<=128νk³。跨全部 k 个 i 求和得到 νk²+128νk⁴<=129/4096<1/25。没有偷偷采用我后续 vector trace 或更宽 profile。

## 6. 精确 CE 与所有 jobs 回填

每个资源独立选 rule t_u，而非共享一个全局随机 t，这保证原条件方差。CE 中心 mu 固定，依次固定 categorical states、全部正请求 coins、resource rules，只走正概率分支。

单/双资源的 winner 因子对每 helper 只选**一个 shared state**：若同 helper 赢两个资源，指定 state 必须相同；在另一个资源排在指定 winner 前面时还必须不请求。distinct resources 的 coins 只在该同一个 state 条件下相乘；u=v 只取一个 winner 的 value 平方。pre-coins 使未固定变量保持原 product 分布；没有独立重抽同 helper 的 state。

finite one/two-resource moments 的排序、状态求和、helper 乘积及 N/N² rule 平均均为绝对次数多项式；coefficients 是原有理 α/r 或 0/1、1/N、固定 mu。公共分母和正概率 partial event numerator 都有多项式位长。最终平方势<1/25、逐 W_i>1/5。第 146 行明确且正确禁止丢请求 coins 后重新按全 selected states maxima 分配。

Good helper Q_j>=1/10 的 home 总权 z_i>1/9。Good 保留原 requesting-winner B bundle；其他 helper 选 own home；outer 取 Good homes。homes 全局互异、B 不交、同一资源的 winner 唯一，所以全局 disjoint。

第 157 行完整执行全部原 jobs：outer、Good helper、其余 helper 的 selectors 分别放原所选 private；仅相应正 bundle incidence 走原 exact resource 端；所有剩余 incidence，尤其未选 indexed states payload 和原 zero jobs，全留各自 private。active private<=19/10、inactive private=1、resource<=1。没有只输出一个 allocation 而漏掉 ordinary assignment。

## 7. 新增 source 推论的实际量词

第 10 节只说固定 0<gamma<1/10 且**所有** reduction 输出都属于本 k⁴-tiny typed 域时，YES actual OPT<=1、NO actual OPT>=2-gamma 的 NP-hard promise 归约会被本算法区分。YES 的输出 C<=19/10；NO 的每个合法调度 C>=2-gamma>19/10，精确比较可行。因实际 OPT>=1，YES 是 actual OPT=1 的端点，没有分数值冒充 actual OPT。

gamma 是源 NO gap；ν 是 home 最大权重；epsilon 是内部 LP 阈值。该直接实际近似推论与旧 NSW 的 exceptional-group/gamma-delta 排除域不同，没有移植其量词。它只排本全部输出受限域内的上述 actualOPT-NO，不排一般 normalized-flat、任意 UM、selector-only 或其他未给实际 NO 性的源。

## 8. 软件、routing 与最终判定

实际读了第 11 节全部来源身份。原 Exact/Proof 的 full hashes 与我先前实核相同。有限 `.py` 的 SHA `460679c82477934bcfdc3ad326f39dd0d0dd0baf7fa4fd75d02df015c7f6b2f0`、stdout SHA `e7433d8476ab2ae99218b4e0307198d0a586311fc84734b16ff3d6efb985c21d` 以及 2048/2916 outcomes、各 11 CE steps、最终势，**我这里只从 canonical/root 消息得知，没有实际读取或重放**。

root 回报自己实际全文读 195 行代码、在新目录一次 CLI、stdout 与冻结 JSON 逐字相同；正文准确将该动作归给 root。两个小实例不是 tiny 域，不包含 LP、N 轮 MW、完整 ordinary schedule 或一般方差定理。第二例有 outer 最终值 0 也没有均值/tiny 前提，不是本理论算法的反例。本数学 reviewer 没有代签软件；本轮无软件测试。

review link 与模型/值桥的 relative routing 仅按字面检查；没有打开这些目标，也没有认证未读历史资料。root 将统一落盘/登记，尚未实体化的 link 不被算成已读证据。没有全球新颖性断言，末行明确一般 UM-TARGET-v1 OPEN。

本次实际 final-read 判定：**84d603… 全 175 行数学与 scope 未发现 fatal；同一个原 k⁴-tiny Exact/Proof 的准确自足 canonical 可以保存。** 这是知情 final-read，非新盲票、非 k²/entropy 扩域认证、非端到端软件实现认证或全球新颖性认证。算法仍仅数学规格，一般共享 state/非UD主目标保持开放。
