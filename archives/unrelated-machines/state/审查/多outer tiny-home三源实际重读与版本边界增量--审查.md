---
id: "unrelated-machines/multi-outer-tiny-home-final-read-increment-20261031"
kind: "review"
type_tag: "审查"
title: "多 outer tiny-home 三源实际重读与版本边界增量"
status: "integrated-three-source-read-after-and-independent-reconstruction"
truth_status: "restricted-k4-tiny-typed-candidate; author-proof-and-independent-route-separated"
review_level: "full-clean-show-read-cross-object-comparison"
summary: "三份新认领冻结来源均属于 UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-19-10-APPROX-v1 的 k^4-tiny typed 对象：5e81 是原作者路线的 final canonical actual-read，ec150 是 MW/Efron–Stein/request-bit CE 作者证明的 read-after，fede89 是独立 Exact-first 的强凸势/投影/固定状态 allocation 路线。它们共同保留 single-state outer、全局互异 homes、own-unit helper、B-only fallback、w_max<=1/(4096k^4) 和完整 ordinary-job 回填；不扩展到 v4/k²/O(1/k)、多 state、重合 homes、一般 UM 或软件认证。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_multi_outer_tiny_home_final_canonical_actual_read.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_multi_outer_tiny_home_final_canonical_actual_read.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_multiouter_single_state_tiny_home_19_10_author_read_after.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_multiouter_single_state_tiny_home_19_10_author_read_after.md"
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_multiouter_single_state_tiny_home_19_10_independent_exact_first.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_multiouter_single_state_tiny_home_19_10_independent_exact_first.md"
source_ids:
  - "5e81cf15c24c42e46e75"
  - "ec1508f77b58b8cf013d"
  - "fede89d2e822cbc5b149"
related_objects:
  - "unrelated-machines/multi-outer-single-state-tiny-home-exact-v1-review"
  - "unrelated-machines/multi-outer-tiny-home-author-proof-v1-read-after-20261031"
  - "unrelated-machines/multi-outer-backend-review-20261030"
  - "unrelated-machines/shared-ud-o1k-relative-curvature-four-source-review-20261031"
evidence_manifest: "../../tools/evidence/multiouter-tiny-home-final-read-sources-20261031/source-manifest.json"
---

# 1. 三份来源的冻结身份与实际阅读

本批由 Boss2 正式认领三份来源，并对每份执行 `clean show` 全文导出和阅读。`legacy-cleanup` 提交 `68fad804ec5946cb296f77dc5b336308a66abf12` 与 `main` 提交 `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c` 的同路径版本保留为同一冻结身份；双提交不计作两份独立材料。原字节副本和 manifest 在 `archives/unrelated-machines/tools/evidence/multiouter-tiny-home-final-read-sources-20261031/`。

| 稳定 ID | 冻结路径 | 字节 / SHA-256 | 来源角色 |
|---|---|---:|---|
| `5e81cf15c24c42e46e75` | `history/source/notes/unrelated_machines/sol_multi_outer_tiny_home_final_canonical_actual_read.md` | 10456 / `299a27d33a68522b78ee70e8779752df6961b90b0dd5a7c8b4ef8396cadb2d90` | 原 k⁴-tiny canonical 的 final actual-read；知情后置复核，不是新的 blind proof |
| `ec1508f77b58b8cf013d` | `history/source/notes/unrelated_machines/sol_multiouter_single_state_tiny_home_19_10_author_read_after.md` | 15209 / `567b9e1153ecfb15b2ff14013a14e52df73a5acefe7585fe2e5652fdfb7483d0` | 作者 MW/Efron–Stein/request-bit CE proof 的 read-after，明确未读/未重放作者代码 |
| `fede89d2e822cbc5b149` | `history/source/notes/unrelated_machines/sol_multiouter_single_state_tiny_home_19_10_independent_exact_first.md` | 16573 / `c063799d1cfa38db6f05cd14f47bc728136dd6766856e4956f9cbe5570a2549a` | 独立 Exact-first；先于作者 proof，构造不同的强凸势/投影/固定状态 allocation 路线 |

三份材料属于同一窄 typed 模型，但证据角色不同：`fede89` 的独立重构不是作者路线的复述；`ec150` 是在独立记录释放后才读作者 Proof 的知情后置；`5e81` 再对最终 canonical 版本做一致性与 scope 复核。不能把三份文件算作三次独立证明，也不能把其中任一份写成代码验证或外部评审。

与既有《多outer single-state tiny-home 19-10 Exact-only 与 proof/canonical/backend 版本审查》相比，本批独有的是对三个**已认领稳定 ID**的完整原文副本、SHA、逐源处置和版本边界；旧对象已经承载 Exact/Proof、canonical、independent、backend 的历史关系，本正文不另造第二个算法对象。与 O(1/k) relative-curvature 对象相比，本批回到原始 `k^4`-tiny v1；后续 k²、v4、v5 和 O(1/k) 资料不得回写到本对象。

# 2. 共同数学对象与完整 ordinary UM 模型

输入 `Q` 有可变数量 `k>=1` 的 outer groups。每个 outer 只有一个 normalized indexed state，其正支持是若干物理互异 home `g_j`，权重 `w_j>0`，并满足每个 outer 的 home 权重和为 1。所有 homes 在全局物理上互异；每个 home 恰有一个 helper，其 own indexed state 是该 home 上的 unit singleton。helper 的其它 indexed states 只在与 homes 不交的共享资源集合 `B` 上有显式 normalized 非负有理支持，可跨 helper、跨 outer 重叠。

本对象的 tiny-home 条件是
\[
\nu:=\max_j w_j\le \frac{1}{4096k^4}.
\]
`k`、state 数、support 宽度和有理分母均是输入，不能把 `k` 当常数或把 home 复制隐含进归一化。每个 state/resource pair 至多列一个 incidence；zero incidence、重复 indexed state、无 fallback helper、unused resource 都保留。模型没有多 state outer、重合 homes、homes 上额外 groups 或一般 non-UD 菜单。

普通 unrelated-machines 矩阵保留全部端点：每个 state 一台 private machine，每个 resource 一台 resource machine；每个 outer 一枚只去本组 state-private 的 unit selector；每个 listed incidence 是不可拆原 job，在对应 state-private machine 的时间为原系数，在指定 resource machine 的时间为 1，其余端点不可用。若 groups、states、incidences、resources 数为 `G,S,I,U`，则矩阵有 `S+U` 台机器、`G+I` 个 jobs、`S+2I` 个有限端点。selector、未选状态 payload、zero jobs、duplicate indexed states 和 unused-resource jobs 都必须输出到原有限端点，不能只返回一份正 incidence allocation。

候选目标是从 Q 显式生成 P(Q)，输出全部原 jobs 的确定性合法 assignment `sigma`，并满足
\[
C_{\max}(\sigma)\le \frac{19}{10}\operatorname{OPT}(P(Q)).
\]
算法不以 OPT、actual allocation、joint law、feasible relaxation point 或精度 oracle 为输入；LP、matching、min-cost flow 和有理 arithmetic 若显式由 Q 生成则允许。一般 unrelated-machines 目标仍开放。

# 3. 共同值桥、LP 失败分支和 baseline

令 `V` 为各 group 选择一份 indexed state、并在共享资源上取互不相交 bundles 时的最大最小组质量。三份材料都保留完整桥
\[
\operatorname{OPT}(P(Q))=2-V,\qquad 0\le V\le1,\qquad1\le\operatorname{OPT}\le2.
\]
正向从每组取达到相应质量的 state，将 selected-state 的正 incidence jobs 导出到对应 exact resources，所有未选 payload、zero jobs、duplicate jobs 和 selectors 留在 private；峰值至多 `2-V`。反向若任何完整调度峰值 `C<2`，每台 resource machine 至多容纳一枚 unit incidence，从每组 selector 所在 state 读出互不相交 bundle，质量至少 `2-C`。

作者路线和独立路线都采用固定 `epsilon=15/16` 的 common primitive-SA1 rational LP。原变量是 indexed state 的 binary `A` 与 listed incidence 的 binary `Z`；保留 state partition、boxes、`Z<=A` gates、resource capacity、perspective quality `sum_u pZ>=epsilon A`，并将各行与同一 primitive 或其补相乘，使用 Boolean diagonal。LP 从显式 Q 生成；不把预给点、PSD 或 unit-FSLP oracle 当输入。

若 LP 不可行，真实 `V<15/16`，于是 `OPT>17/16`。所有 payload 留 private、每个 selector 放任一合法原 private 的完整 baseline 峰值至多 2，满足
\[
\frac2{\operatorname{OPT}}<\frac{32}{17}<\frac{19}{10}.
\]
不可行分支是近似算法的失败保护，不是 general integral feasibility certificate。

从同一份可行 SA1 点可提取 helper fallback 边际 `alpha_{js}` 和 resource claim `zeta_{jsu}`：
\[
0\le \zeta_{jsu}\le\alpha_{js},\qquad
\sum_u p_{jsu}\zeta_{jsu}\ge\varepsilon\alpha_{js},\qquad
\sum_{j,s}\zeta_{jsu}\le1.
\]
own-unit helper 的质量、gate 和 box 行给 `EA=EZ`，home cap 给 fallback mass 至少覆盖外层 home claim；`alpha=0` 时 gate 强制 `zeta=0`，没有 `0/0`。这些提取式来自同一 global SA1 点，不能把不同 outer 的局部点拼接。

# 4. 作者 MW/Efron–Stein/request-bit CE 路线（ec150）

作者路线对每个 helper 独立选择一个 fallback state 或 empty，再只为所选状态的正 incidences 读取 request coin。给 outer 权 `lambda`，资源只在实际请求者中按 `lambda_iw_jp_{jsu}` 排序，固定索引破平局；未请求但 state 已选的 helper不参与 winner。对固定 threshold，跨 helper 的请求事件独立，且同一 helper 的不同 states 只作一次互斥求和，得到
\[
\lambda\cdot g(\lambda)\ge\frac58\varepsilon^2=\frac{1125}{2048}.
\]
作者没有把同一 helper 的多个 states 当独立，也没有把所有 selected state 的 resources 免费重分。

接着令 `N=1024k`、`eta=1/32`，用 floored rational multiplicative weights：每轮 `p_i=b_i/sum b`，`lambda=(7/8)p+1/(8k)`，计算 exact winner oracle 并更新 `b_i<-b_i(1-eta g_i)`。对数比较给逐 outer 轮均值
\[
\mu_i\ge\frac{757}{1792}>\frac25.
\]
每个 resource 独立均匀抽一个保存的轮次，但 helper 的完整 state/request profile 作为一个独立块；条件于 helper blocks 后 resource rules 独立。`d_u<=nu`、`sum_ud_u<=k` 给条件方差 `<=nu k`；替换整个 helper block 对任一 outer 的影响 `<=16k w_j`，Efron–Stein 和全 `k` 个 outer 合并为
\[
\sum_i\operatorname{Var}(W_i)
\le129\nu k^4\le\frac{129}{4096}<\frac1{25}.
\]

随后用固定中心平方势 `Psi=sum_i(W_i-mu_i)^2` 做条件期望去随机化，依次固定 helper states、正 request coins 和 resource rules，只在原条件概率为正的分支中选最小 conditional `E Psi`。single-resource 与 two-resource winner-pair moments 足够计算；同一 helper 在双资源事件中必须共享一个 state，若要求不兼容则该项为零。最终 `Psi<1/25` 给所有 `W_i>1/5`。

取 `Good={j:Q_j>=1/10}`，由 `W_i<=z_i+(1/10)(1-z_i)` 得每个 outer 的 Good home mass `z_i>1/10`。Good helper 的实际 winner B bundle 交给其 outer，其他 helper 回 own home；全局 homes 互异、B 与 homes 不交、winner resources 单占。最后把完整普通 P(Q) 回填：selected-state 真 bundle 的正 incidence 送 exact resource，所有其它 incidence、inactive state payload、duplicate jobs、zero jobs 留 private。active private 至多 `19/10`，inactive private 至多 1，resource 至多 1。

`ec150` 明确自己是作者 proof read-after：未读取作者 `.py`、stdout 或运行日志。它支持这条数学承重链和全 jobs 语义，但不构成端到端软件验证、外部审查或一般 UM 证明。

# 5. 独立 Exact-first 的强凸势/固定状态 allocation 路线（fede）

`fede89` 先只读 Exact-only 量词，再独立提出与作者 MW/CE 不同的充分路线。先由同一 SA1 点得到 fallback state 边际 `alpha_{js}`、claims `zeta_{jsu}`；为每个 helper 独立抽一个 state 或 null，定义每个 state profile 的 weighted resource maximum
\[
F_t(\alpha)=\sum_{u\in B}\max_j\{\alpha_{i(j)}w_jp_{j,t_j,u}\},\qquad G(\alpha)=\mathbb E_tF_t(\alpha).
\]
阈值积分和跨 helper 独立性给所有 simplex 权 `alpha` 的统一下界
\[
G(\alpha)\ge\frac58\varepsilon^2=\frac{1125}{2048}.
\]
它只作为存在性分析，不声称 SA1 的高阶相关表等于该人为独立 law，也不要求 requests 同时可行；每个 resource 只保留最大请求。

对 `k>=2`，采用 floor simplex `K={alpha:sum alpha_i=1, alpha_i>=1/(8k)}`，正则化强凸势
\[
V(D)=\min_{\alpha\in K}\left[G_D(\alpha)+\frac14\|\alpha\|_2^2\right].
\]
固定一个未处理 helper 的 state 与 null 进行比较，state 差函数在 K 上的 Lipschitz 常数为 `(1+8k)w_j`。强凸性给每个 helper 选择的期望势损失至多 `2L_j^2/lambda`。用投影 subgradient 的全有理近似，取 `tau=1/(1024n)`，候选 state 总数显式枚举而不枚举联合 profile；每个候选的 `V(D)` 由有理排序、概率乘积和投影迭代近似。

tiny-home 付款满足
\[
\sum_j\frac{2L_j^2}{\lambda}\le\frac{289}{4096},
\]
再减去有限投影误差和正则项后，得到最终 fixed-state profile 对整个 simplex 的 weighted maximum 下界
\[
\min F_t\ge\frac{921}{3584}=\frac14+\frac{25}{3584}.
\]
`k=1` 单独直接选条件期望最大 state，不套 tiny-home 曲率。

固定这些 states 后，解显式有理 allocation LP：每 resource 分配给 helper 的和不超过 1，每 outer 的 aggregate quality 至少 `1/4`。取一个 vertex；每 resource 的 split face 维数总和至多 `k`，故丢弃至多 `k` 个 split resources。每丢一项对任一 outer 损失至多 `d=1/(4096k^4)`，得到
\[
W_i\ge\frac14-kd=\frac{1023}{4096}>\frac{19}{100}.
\]
保留质量 `q_j>=1/10` 的 helper fallback，释放其它 helper 回 own homes；同一份 integral B allocation 保持资源不重复。由 `W_i<=theta+(1-theta)r_i` 得每个 outer 的 Good home mass至少 `1/10`，再以原 finite endpoints 回填全部 jobs，峰值不超过 `19/10`。

该路线是独立数学重构，不是作者 MW/CE 的重复；它没有端到端实现，只有正文中列明的 Fraction 常数检查。它也只适用于本 k⁴-tiny typed 域。

# 6. Final canonical actual-read（5e81）的版本和 scope 核对

`5e81` 对原 k⁴-tiny v1 的最终 canonical 文本作知情后置复核。它确认正式 ID `UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-19-10-APPROX-v1`、输入对象、完整 ordinary P、`OPT=2-V`、SA1→MW→requester→CE→Good→all-jobs 链均与作者 proof 和独立重构一致；同时明确排除后续 k²/vector-variance、v4/v5 和 O(1/k) 变体。它没有把作者的有限 `.py`/stdout 当作自己读取或重放的证据，并把 final-read 结论标成 informed canonical consistency review，而非第二次 blind proof。

`5e81` 还保留一个窄 source-gap 推论：只有当一个 reduction 的全部输出都落在本 k⁴-tiny typed 域、YES 端 actual `OPT<=1`、NO 端 actual `OPT>=2-gamma` 且固定 `gamma<1/10` 时，19/10 algorithm 才可区分该特殊 promise。这个推论不推广到一般 normalized-flat、任意 UM、selector-only 或缺乏 actual NO gap 的来源，也不证明 P 不等于 NP。

# 7. 与现有对象、backend 和后续扩域的关系

现有《多outer single-state tiny-home 19/10 Exact-only 与 proof/canonical/backend 版本审查》已记载 `8b0284...` Exact-only、`e15dcf...` author proof 以及本批三份来源的版本关系；本批新增的是三份稳定 clean ID 的原文副本、实际阅读说明和逐源 receipt。现有《多outer tiny-home作者证明 v1 读后与完整算法范围增量》聚焦作者 LP/MW/variance/CE 证明；本正文补充 `fede89` 独立强凸势路线和 `5e81` 对最终 canonical 的量词校正。

现有 two-resource backend 只核两例小型 moments/CE：3 helpers、2 outers、2 states/helper、2 resources、2 rules，枚举 2048/2916 outcomes 和 11 步 CE。它明确 `whole_scheduling_algorithm_checked=false`、`small_weight_class_instantiated=false`；第二例 outer 值为 0 也不满足 tiny-home/均值前提，不是本 v1 反例。该 backend 的运行 hash、脚本和 root replay 保持独立 evidence；本批未读取或重放代码。

后续 v4/k²、v5/O(1/k) 资料必须保持独立身份：它们修改 `k=1` 量词、home 上界、UD leaf 范围或势函数，不得用本 k⁴ Proof 的 `delta=1/(4096k^4)` 和 `129/4096` 方差界静默覆盖。多 state outer、home overlap、homes 上额外 leaf、一般 non-UD、任意 unrelated-machines 和六人 CAG/SPE 均不在此对象定义域。

# 8. 真值层级、未决缺口与接续

**已支持的窄结论。** 三源共同支持原 v1 typed candidate 的数学合同和全 ordinary-job 语义；作者路线的 MW/request-bit/CE 证明链与独立 Exact-first 的强凸势/固定-state allocation 路线在本域内均未暴露源文本中声称的 fatal。两条路线应分别保留，不能写成一次统一算法或互相替代的软件证据。

**有限/条件证据。** `ec150` 仅为作者 proof read-after，`5e81` 是 canonical actual-read，`fede89` 的代码范围仅为 Fraction 常数反算。现有 backend 的有限枚举和 root replay 不是本批新运行，也不覆盖 LP、`N=1024k` MW、全方差、CE、端到端 P(Q) 编译或大输入位复杂度。

**缺口。** 没有端到端实现、全 tiny-domain 重放、外部评审、全球新颖性或一般 UM 算法；没有把 source-gap 推论升级为 hardness。后续要完善，需实现并审计 common SA1 LP、requester winner oracle、MW/CE 或独立强凸路线、完整 all-job compiler，并分别处理 v4/k²/O(1/k) 扩域和多 state/重合-home 模型。

本批三源正文、证据和 receipt 均不执行 commit、push 或 clean done；由 Boss2 在 checkpoint/pushed 后串行登记。
