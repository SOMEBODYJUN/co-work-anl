---
id: "unrelated-machines/sol-general-repair-k2-local-law-canonical-pullback-v1"
kind: "review"
type_tag: "审查"
title: "Sol 通用 repair-k2 全局 local-law 与 canonical pullback 三源审查"
status: "retained-exact-family-narrow-obstruction"
truth_status: "exact-family-with-independent-reconstruction-and-no-global-schedule-gap"
review_level: "full-source-read-and-cross-object-comparison"
summary: "三份冻结来源共同给出参数域 0<c<1 的 18 台机器、17 个作业、34 个有限端点的 K=2 物理证书：同一三位 Boolean functional 通过 degree≤4 恒等式、全局 M2、所有 raw affine localizers 与逐机完整 CONFIG membership law；但指定的直接 canonical pullback 在跨三台机器的三重矩上为 -1/160，activation quality 行为 -c/160。族有实际 OPT=1 调度，因此只构成同一点 canonical 接口的精确障碍，不构成一般 UM 间隙、SA1 不可行性或复杂度结论。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_general_repair_k2_local_law_canonical_pullback_exact_v1.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_general_repair_k2_local_law_canonical_pullback_exact_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_general_repair_k2_local_law_canonical_pullback_author_proof_v1.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_general_repair_k2_local_law_canonical_pullback_author_proof_v1.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_general_repair_k2_local_law_independent_exact_first.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_general_repair_k2_local_law_independent_exact_first.md"
legacy_ids:
  - "UM-RAW-K2-LOCAL-LAW-DIRECT-CANONICAL-PULLBACK-OBSTRUCTION-v1"
related_objects:
  - "unrelated-machines/raw-k2-local-law-canonical-pullback-obstruction"
---

# 1. 阅读范围、来源身份与处置

本批正式认领并用 `clean show` 逐字读完三份冻结文本。三份文本均在 `legacy-cleanup` 提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `main` 提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 具有相同路径版本；本正文保留两条来源定位，独立证据副本与 manifest 位于 `archives/unrelated-machines/tools/evidence/sol-general-repair-k2-local-law-sources-20261031/`。

| 稳定源 ID | 冻结路径 | 大小 / SHA-256 | 在本对象中的作用 |
|---|---|---:|---|
| `8c698571723b60a4a4f9` | `history/source/notes/unrelated_machines/sol_general_repair_k2_local_law_canonical_pullback_exact_v1.md` | 5479 / `f958afc5baac6c031415c735c97ecb1febaa2240149b10c111e70ec2dac6b18b` | exact 规格，完整定义模型、functional、负 pullback 与范围 |
| `018de084dc281c92334c` | `history/source/notes/unrelated_machines/sol_general_repair_k2_local_law_canonical_pullback_author_proof_v1.md` | 8131 / `e9b2bba2cf3784e86ba9560ebddec0a520a7c51361f4af48358aa3f4c7eb467c` | 作者推导，给出 M2、raw localizer、CONFIG law 与 OPT=1 构造 |
| `65ad7c8ffd2170f3aeb6` | `history/source/notes/unrelated_machines/sol_general_repair_k2_local_law_independent_exact_first.md` | 10311 / `8e3dbbf6ba04069eec67723c1d39458de0bb2e1d39f7776367aad76a58fb4412` | 独立 Exact-first 重构；先读 exact，不把作者 proof 当独立证据 |

Exact、作者 proof、independent exact-first 不是三次独立实验：第一份是规范输入，第二份解释作者证明，第三份独立地重构相同有限族并核对其量词。因而本对象把“来源自述”“作者推导”“独立重构”分栏保留，不将它们合并成外审或新颖性认证。与已有 `K2局部行律拉回障碍--审查.md` 的关系是增量强化：旧对象记录了 c=3/4 运行、三点参数回归和旧审计 JSON；本批直接读到参数化 exact/proof/independent 三源，并明确全参数符号推导与逐机完整 row law。旧对象仍保留其运行证据身份，不能被本批文字替换。

# 2. 数学定义域：显式 18 机、17 作业、34 finite endpoints

参数为二进制编码有理数
\[
0<c<1,\qquad T=1+c,\qquad \varepsilon=1-c.
\]
输入有一个 outer 组 `M` 和四个 helper 组 `H_u,H_v,H_r,H_s`。每组有两个不同 indexed states；`M` 的 state 0 在正 home `u,v` 上系数 `c,1-c`，state 1 在正 home `r,s` 上系数 `1-c,c`。四个 helper 各自有一个 unit own home 与一个 unit fallback 私有资源：例如 `H_u` 的 state 0 为 `u`、state 1 为 `w_u`，其余三个同型。所有八个资源 `u,v,r,s,w_u,w_v,w_r,w_s` 物理互异，十个 state-private roots 也物理互异。

普通 unrelated-machines 矩阵保留全部端点：五个 unit selector jobs、十二个 listed incidence jobs，共 17 个作业；每个 selector 与每个 incidence 的 private/resource 两端均保留，即 34 个 finite endpoints。未列的机器-作业时间是无穷；不因某个 assignment 替换为常数 0 而删除原 job 或原 endpoint。不存在额外 allocation、guard 或可拆分任务逻辑。这一项很关键：负值涉及三个不同物理机器上的原端，而非删掉某个零端后的人为缩小矩阵。

# 3. 同一 global functional 与物理合同

令形式 Boolean 位为 `b_1,b_2,b_3`。`ell(1)=1`；任意 distinct 单项式只按位数取值：单项为 `3/10`，双项为 `3/80`，三项为 `-1/160`；重复位按 Boolean 商代数约去。所有 34 个原 assignment variables 都是常数、单 literal 或补 literal。代表性 substitution 为：

- `M/0` selector 去 private 为 `b_1`，其 `u` resource 端为 `b_2`，`v` resource 端恒 1；
- `M/1` selector 为 `1-b_1`，`r` resource 端恒 1，`s` resource 端为 `1-b_3`；
- `H_u/0, H_u/1` 的 selector 分别为 `1-b_2,b_2`，其 resource 端为相应补/同 literal；`H_v,H_r,H_s` 同理。

每个 incidence 的 private 端与 resource 端互补，每个 selector 的两端互补。因此全部 one-hot、exclusivity、Boolean 恒等式在同一三位商代数内成立，且乘到 degree 4 仍成立。令 `L=ell` 经上述 substitution 的合成。K2 合同要求：全局 degree≤2 square PSD；所有 physical machine 的 raw load 对每个全局 affine `q` 满足
\[
L((T-\mathrm{load}_i)q^2)\ge 0;
\]
并且每台机器各有总质量 1、负载不超过 `T` 的有限有理 CONFIG law，与共同 `L` 共享该 row 内全部 membership moments。这里没有额外要求跨机器的联合 schedule 分布，也没有把 CONFIG 权重提升成 global random variables。

## 3.1 全局 M2 的有限精确证明

作者 proof 给出三位 degree≤2 basis
\[
1,b_1,b_2,b_3,b_1b_2,b_1b_3,b_2b_3
\]
的正定 Gram Schur pivots
\[
1,\;21/100,\;63/320,\;7/40,\;7/256,\;7/288,\;7/384.
\]
独立 Exact-first 以对称三维块与两个 standard 二维块重构同一结论。任意原 quadratic 经 substitution 都落在该七维 span，因此完整 34-variable physical M2 是其线性拉回，596 个 square-free degree≤2 monomials 均由该合同覆盖。`ell(b_1b_2b_3)=-1/160` 仍可为负；M2 正性本身不是 global triple-literal positivity。

## 3.2 所有 raw affine localizers

两台 outer private roots 的 raw load/slack 为
\[
\begin{aligned}
\mathrm{load}_{M0}&=b_1+c(1-b_2), & T-\mathrm{load}_{M0}&=(1-b_1)+cb_2,\\
\mathrm{load}_{M1}&=(1-b_1)+cb_3, & T-\mathrm{load}_{M1}&=b_1+c(1-b_3).
\end{aligned}
\]
其余 private roots和正资源行的 slack 为常数 `c`，fallback 资源行是 `c+(1-b)` 或 `c+b` 型。对任意 affine `q`，`zq` 是 degree≤2 polynomial，且 `z^2=z`，所以
\[
L(zq^2)=L((zq)^2)\ge0
\]
由 global M2 得到。每个 slack 是正系数 literal/常数的和，故全部 raw localizers 对所有 `0<c<1` 同时成立。这是符号推导，不是只测 `c=3/4` 或有限数值点。

## 3.3 每台机器的完整 row CONFIG law

任意单个位边际为 `P(1)=3/10`、`P(0)=7/10`；任意两个位的真实 law 为
\[
P(00)=35/80,\quad P(10)=21/80,\quad P(01)=21/80,\quad P(11)=3/80.
\]
`M/0` 行仅依赖 `(b_1,b_2)`，其 selector/private-u/private-v 三端的配置与权为
\[
\{P_u\}:35/80,\quad \{S,P_u\}:21/80,\quad \varnothing:21/80,\quad \{S\}:3/80.
\]
对应负载为 `c,T,0,1`。`M/1` 行仅依赖 `(b_1,b_3)`，配置为
\[
\{S'\}:35/80,\quad \varnothing:21/80,\quad \{S',P_s\}:21/80,\quad \{P_s\}:3/80,
\]
对应负载为 `1,0,T,c`。其它机器最多依赖一个位或常数，使用同样的 Bernoulli 边际或确定性配置。由此每行任意 endpoint 子集 `S` 的 membership 概率都与 `L(\prod_{e\in S}x_e)` 一致，不只是 first/pair 或本地 degree≤4。该事实不能升级为跨行三位联合分布：三行各自的 CONFIG law 可分别真实，却不共同定义一个全局 schedule law。

# 4. 实际调度与直接 canonical pullback 失败

对每个 `c`，选择 `M/0`；`H_u,H_v` 选择 fallback；`H_r,H_s` 选择 own。选中 state 的 positive incidence export 到对应 unit resource，未选 state 的 incidence 保持在其私有机器。所有 17 个原 job 各执行一次，峰值为 1；每个完整 schedule 必须执行 unit selector，故 `OPT(P(Q_c))=1`。这个调度是实际可行点，和下述伪矩点不是同一个对象。

指定 direct canonicalization 取
\[
A_{M0}=b_1,\qquad Z_{M0u}=b_1b_2,\qquad Z_{M0v}=b_1,\qquad A_{H_s0}=b_3.
\]
因为 `epsilon=1-c`，state 0 的 canonical quality polynomial 化为
\[
cZ_{M0u}+(1-c)Z_{M0v}-(1-c)A_{M0}=cb_1b_2.
\]
于是
\[
L(Z_{M0u}A_{H_s0})=\ell(b_1b_2b_3)=-1/160<0,
\]
以及
\[
L\bigl([cZ_{M0u}+(1-c)Z_{M0v}-(1-c)A_{M0}]A_{H_s0}\bigr)=-c/160<0.
\]
这两个负值分别违反 canonical claim 的非负乘积行和 activation-quality 行。三因子可取为 `M/0` selector 去 private、`M/0` 的 `u` incidence 去 resource、`H_s/0` selector 去 private；它们位于三台不同物理机器。因而本例排除了“只因单行未共享 triple”这一解释：每一行已共享完整 membership law，负值来自跨行全局三重矩。它仍只否定**同一点、指定规则的 direct pullback**，不否定另一个 `R` 点、另一种 extraction、重新求解或加入更强 global triple 合同。

# 5. 三源比较、独有内容与与旧对象的关系

* Exact v1 提供完整模型表、全局 functional、K2 量词、负式和精确 scope；没有给作者 proof、PSD 分解或代码。
* Author proof v1 补上七维 PSD 的两种自足论证、所有 raw localizer 的符号推导、每台机器完整 CONFIG law、`C=1` 调度、跨三机器负 triple 和固定规模生成说明；它明确称自身不是独立审查。
* Independent Exact-first 在未读作者 proof/code 的前提下重构上述模型，给出对称/standard Gram 分块、两位真实 law、两台外层行配置、17-job `C=1` 调度及负值，明确未执行新的 checker，也不把有限回归冒充全参数 proof。

与已有 `K2局部行律拉回障碍--审查.md` 相比，本批独有的可接续内容是：明确的 `0<c<1` 全参数族；完整 18m/17j/34-endpoint 普通矩阵定义；逐机 full membership law 的两位边际构造；三份来源的身份拆分与独立重构；以及“旧审计是有限运行证据、本批是来源级精确规格”的版本边界。旧对象中的 c=3/4、三点参数输出、standalone audit SHA 仍应留在其原 evidence 目录，不在本正文重复声称为新运行。

# 6. 真值、缺口、用途与接续

**已支持的精确结论。** 对每个有理 `0<c<1`，所指定的 18m/17j/34-endpoint 族存在共同 degree≤4 Boolean functional；global M2、所有 raw affine localizers、逐机完整 row CONFIG law 以及实际 `OPT=1` 调度可由文中给出的有限公式满足。对该同一点的 direct canonical pullback，claim 乘积为 `-1/160`，quality lift 为 `-c/160`，且三因子跨三台机器。

**条件/有限证据。** 固定规模证书可由输入 `c` 的二进制编码以总位多项式时间生成；这是代数构造的复杂度叙述，不是已运行软件的复杂度实验。旧对象有有限 c 回归和 standalone code 记录，本批未重新执行新 checker。

**未证明或不能外推的命题。** 没有全局联合 schedule law；没有证明所有其它 SA1 点、其它 canonical extraction 或其它舍入接口都失败；没有 actual OPT 间隙、近似下界、NP-hardness、一般 unrelated-machines 算法或新颖性结论；也没有 global M3/所有 literal 三次非负性。参数端点 `c=0,1` 不在本对象域内。typed one-outer 13/8 算法与一般 UM 主问题必须保持独立对象，不能因同一 `c` 族自动合并。

**用途与接续。** 后续设计 K2→primitive-SA1 的桥时，应逐项检查是否要求跨机器三重矩非负、是否只使用 raw load localizer、以及是否暗含 CONFIG law 的 global coupling。若桥要保留此族，必须改造 extraction/增加跨行耦合条件/选择另一个可行点；若要把障碍提升为定理，需要写出 canonical 规则的完整量词并证明对所有候选点或明确说明额外合同。第三阶段建立关系时，本对象可与旧 K2 finite-obstruction 对象建立“增量强化/来源—审查”边，但不可连成“调度不可行”或“一般 SA1 不可能”边。
