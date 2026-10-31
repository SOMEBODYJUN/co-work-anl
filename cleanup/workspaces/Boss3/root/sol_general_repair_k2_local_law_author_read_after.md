# 18m17j local-law family：Author Proof 实际全文读后对照

审查者：`/root/sol_nsw_independent_attack`。在 parent 实际读完我的 151 行 Exact-first 重构后，才收到本候选新 Author Proof 的释放。本记录是知情 read-after，不是另一次 blind review；原独立记录保持冻结。

## 1. 本次唯一新读取、实核身份与次序

`/workspace/scratch/038d9dcc4cac/sol_general_repair_k2_local_law_canonical_pullback_author_proof_v1.md`

- 实核 SHA-256：`e9b2bba2cf3784e86ba9560ebddec0a520a7c51361f4af48358aa3f4c7eb467c`。
- 实核 8,131 bytes、122 行、mode `0644`。
- 真正以 **1–120、121–122** 两块显示并逐行读完，无截断。
- 没有读、hash、运行作者的新 code/run，也没有以 parent 通知的软件结果代替我未做的软件实审。作者 §6 的程序范围说明是已读文字，其实际实现/输出仍由 parent 独立认证。

已冻前置记录：

`/workspace/scratch/038d9dcc4cac/sol_general_repair_k2_local_law_independent_exact_first.md`

实核仍为 SHA `8e3dbbf6ba04069eec67723c1d39458de0bb2e1d39f7776367aad76a58fb4412`，10,311 bytes、151 行、`0444`。Exact 实核仍 SHA `f958afc5baac6c031415c735c97ecb1febaa2240149b10c111e70ec2dac6b18b`，5,479 bytes、76 行。

真实先后：已知旧14m背景 → 只读新18m Exact 1–76 → 独立重构全参数/local laws/ordinary jobs 并冻结 → parent 真正全文读完 → 本次才读新 Author Proof。没有把本文新见的作者 Cauchy 证明倒算为先前已知。

## 2. 同一实例、同一点、全 finite endpoints

作者 7–9 行准确承接新 Exact：5 groups、10 indexed roots、12 incidences、8 resources、18 machines、17 jobs、34 endpoints，参数每个有理 `0<c<1`，T=1+c，epsilon=1−c。所有 listed coefficients 为正，部分原 assignment endpoints 的 marginal/substitution 恒0，原 endpoint/job 仍保留。

每 incidence 两端和每 selector 两端互补，包括 constant 0/1 情形；全部原 Boolean、one-hot、同 job exclusion 和 multiplier 至 degree4 由同一个 Boolean substitution 成立。未引入 `export≤activation` 逻辑约束，未删除 inactive states 或总是 export 的原 incidence。

## 3. Global M2 的两种作者证明逐项核对

作者 17–21 行的七维 Gram 及正 pivots 与旧同一三位 functional 和我的独立三位置换 symmetry-block 分解一致。34 个端的 reduced quadratic basis 大小 `1+34+561=596`，所有物理 quadratics 都在 bit quadratic span 内，所以是真正的全局 pullback PSD，不是只核一个七维 principal submatrix。

作者这次新增的 cube signed-law 证明也可直接核对：000 与三个 singleton patterns 各 35/160，三个 doubletons 各 7/160，111 为 −1/160，合计一；其 singleton/pair/triple moments 分别 `(35+14−1)/160=3/10`、`(7−1)/160=3/80`、`−1/160`。

三位 degree≤2 polynomial 的三阶差分为零，故

`q111=q110+q101+q011−q100−q010−q001+q000`。

令 S 是七个正权点的加权平方和，weighted Cauchy 的常数为

`4·(160/35)+3·(160/7)=608/7`。

所以 `ell(q²)≥[1−(608/7)/160]S=(16/35)S≥0`。若 S=0，q 在七点均零，再由差分式在第八点也零，故 Boolean quadratic 本身为零，给正定。所有数字、次数和严格性均正确。这是作者新的自足有限维论证，不是调用一般 slice/SoS theorem；我本次已实际核其推导，但不替换原 Exact-first 用的独立证明。

## 4. 全参数 physical localizers 与完整各机 row laws

作者 36–52 行的两个特殊 raw slack 是 `(1−b1)+c b2` 与 `b1+c(1−b3)`，其余为 c 或 c 加 Boolean literal，与我独立逐机表相同。对全局 affine q，`L(l q²)=L((lq)²)≥0` 的 Boolean reduction 总次数≤4；lq 为 quadratic，M2 允许。c>0，所有 coefficients 非负。因此全参数证明闭合，无 finite-grid 替代和除 c 的位长问题。

作者两位 law `(35,21,21,3)/80` 与我 `(70,42,42,6)/160` 同一份 positive law。M/0 的四配置 `{Pu},{S,Pu},empty,{S}`、M/1 的 `{S'},empty,{S',Ps},{Ps}` 及 weights 全部逐项一致；其中 pair 配置负载恰 T，不是严格小于 T，但合同允许 ≤T。

每个 row 最多依赖两位：两个 outer roots 分别用 (b1,b2)、(b1,b3)，其他 rows 用至多一位或 constants。于是该 row 的所有 Boolean 多项式都由真实单/双位 marginal 决定，完整 membership law 与共同 ell 的所有本地条目一致。没有把 per-row laws 拼成全局 law，也没有给 CONFIG weights 新矩。

本族每机 row 最多三个原 endpoints，所以所有完整 membership patterns 已由该 row 的 square-free moments≤3 决定；含恒0 private endpoint 的 monomial 全零。高次重复幂只作 Boolean reduction，不需要免费给任意未知全局高阶 moments。它确实比旧14m仅 first/pair 的同机缺口更强。

## 5. 实际 schedule、跨机负式与严格边界

作者 91 行 actual C1 witness 与独立重构相同：M/state0、Hu/Hv fallback、Hr/Hs own；所选 incidences export、未选保 private，全部17 jobs各一次。M/1 未选两个系数合计1，其余未选 helper singleton 为1，所有资源至多一 unit。Unit selectors给下界1，所以 actual OPT=1，对每个 c 都如此。

Canonical product 得 `Z_M0u=b1b2,Z_M0v=b1,A_Hs0=b3`。State0 quality 为 `c b1b2`，故两个负式为 `−1/160`、`−c/160`，与 Exact-first 一致。Activation localizer 的值用原 L 在物理 degree≤4 上计算，并未声称原仅 degree2 的 canonical F 已有免费三阶扩展。

负 triple 的三个原端位于 M/0 private、resource u、Hs/0 private 三台不同机器。每机 full local law 因只见≤2位而全部正确，这三个因子不同时在任何 row 内。作者没有再用旧14m“缺少同机 triple 共享”解释新例；负性是跨 row 的。额外 global triple literal positivity 会切它；本例并没有反驳那一更强合同。另项 source-SA3 bridge 须按其独立 Exact 与证明审查，本候选未声称或使用它，也不由本反例认证。

## 6. 位长、软件分工和审查结论

作者 116 行的生成成本正确：实例/矩阵维度固定，只有 c、1−c、T 的编码位长可变，moments 与 row-law weights 均固定小分母有理数；全参数证明无 SDP finder。端点 c=0、c=1 未包括，不能追认其结构或量词。

作者 118–120 行对有限程序与全参数代数证明作了正确区分。我未打开该代码/JSON，也没有自己执行这些参数测试；parent 另通知其全代码实读与 CLI/summary-projection 核验，那是 parent 的软件记录。本记录只签数学推导，不称“我已跑新程序”或“程序枚举所有有理 c/所有原 quartic identities”。

**本次 Author Proof 实际全文对照未发现 fatal；与已冻独立 Exact-first 同对象、同点、同全参数、同 local-law 强度。PASS 仅为指定 raw K2/full-local-law 给定点的直接 canonical product pullback 失败。** 不改前置冻结，不作 actual gap、近二反例、一般 UM algorithm 或 typed 单outer算法反证。

本次数学审查没有新软件实现、通用checker或SDP solver；全球新颖性未认证，一般 UM 主目标仍 OPEN。
