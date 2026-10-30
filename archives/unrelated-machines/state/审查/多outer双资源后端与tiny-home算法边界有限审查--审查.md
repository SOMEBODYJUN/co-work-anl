---
id: "unrelated-machines/multi-outer-backend-review-20261030"
kind: "review"
type_tag: "审查"
title: "多 outer 双资源后端与 tiny-home 算法边界有限审查"
status: "finite-backend-classified"
truth_status: "canonical-algorithm-scope-read-with-two-resource-exact-backend-only"
review_level: "full-source-read-and-independent-backend-rerun"
scope: "multi-outer single-state tiny-home canonical algorithm, its exact finite winner-moment backend, and root replay boundary"
source_refs:
  - "source:19575b9ed8447b7d0589:evidence/runs/unrelated_machines/multi_outer_request_winner_pair_backend_audit.json"
  - "source:3743fee56233f1e58188:evidence/runs/unrelated_machines/multi_outer_request_winner_pair_backend_root_replay_scope.json"
evidence_manifest: "../../tools/evidence/multi-outer-backend-20261030/source-manifest.json"
---

# 1. 来源身份与阅读范围

本批两个来源是 `UM-MULTI-OUTER-SINGLE-STATE-TINY-HOME-19-10-APPROX-v1` 的软件后端证据，而不是该算法的完整证明。第一源是一个独立的 two-resource winner-moment/conditional-expectation (CE) 有限审计；第二源记录 root 对相同脚本的全新目录重放、代码/输出哈希和 scope。为判断这两个 JSON 的数学含义，我还完整读取了规范正文 `multi_outer_single_state_tiny_home_rounding.md`、内部审查 `multi_outer_single_state_tiny_home_rounding_review.md` 和脚本 `multi_outer_request_winner_pair_backend.py`。因此本批只承认后端有限核验，不能把它写成端到端调度实现或一般证明的新副本。

规范算法的输入是显式 typed normalized-flat Q，而不是任意 unrelated-machines 矩阵：有 k 个 single-state outer、全局互异的 positive homes、每个 home 的 unit-own helper，以及共享 B 资源池上的 normalized fallback states。每个 outer 只有一个 indexed state，home 最大权重满足 `w_max<=1/(4096 k^4)`。所有 selector、indexed state、incidence 和零 payload job 都必须回填为普通 UM 的完整 assignment；不能因为有限程序只看 positive 请求就删除原任务。

# 2. 规范算法的数学合同（作为相关材料保留）

## 2.1 实际值桥和失败分支

对每个 group 取 fallback state 在 disjoint B-resource bundles 上的质量，记所有 group 最小值的最大化为 V。规范正文给出双向证明

`OPT(P(Q)) = 2-V`,  `0<=V<=1`,  `1<=OPT<=2`。

正向把每组的 attaining state 放到其 private machine，输出该 state 的正 incidence jobs，其余 jobs 留各自 private；反向在任意 `C<2` 调度中每个资源至多承载一个 unit job，从 selector 所在 state 读出 disjoint bundle。这个桥是整个 v1 算法的前提，不是本批两个 JSON 单独证明出来的结论。

算法先以固定 `epsilon=15/16` 构造一个有界二阶 common-SA1 rational LP：state partition、primitive boxes、gates、resource capacity 和每个 state 的 perspective quality 都保留一次及与同一 primitive 的乘积。若 LP FAIL，则 `V<15/16`，全 jobs baseline 的 makespan 2 满足 `2/OPT<32/17<19/10`。LP feasible 分支不把分数点误当整数调度。

## 2.2 共享后端、MW 和方差

从 SA1 点整化 helper own singleton 后，得到所有 helper 的共享 resource capacity 以及每个 outer 的 fallback 质量下界。helper 独立选择一个 state 或 empty；在一个资源上，按 `lambda_i(j) w_j p_jsu` 的固定序排序，真实请求者中首者获胜。独立 helper state 使资源阈值事件可以用

`Pr(max score >= z)=1-prod_j(1-a_j(z)) >= (5/8) sum_j a_j(z)`

控制，规范正文的常数给出 `lambda·g(lambda)>=1125/2048`。floored rational MW 使用 `N=1024 k` 轮和 `eta=1/32`，产生每个 outer 的平均值 `mu_i>=757/1792>2/5`。这些是规范证明内容，后端脚本只核对其中 CE moment 计算的一个很小切片。

每个资源的 order 独立均匀取保存的轮次，且必须保留 whole-helper profile 的相关性。规范 Efron–Stein 计算把一个 helper 的整块 state/coins 作为独立块，得到 `sum_i Var(W_i)<=129/4096<1/25`；不能把每个 state 或每个 resource coin 当作互相独立的新 helper。随后固定 state、request coins、resource rules 的条件期望，平方势只需要 single-resource winner 和 two-resource winner-pair 的一、二阶矩。CE 完成后必须按已固定的实际请求者输出 winner，不能把未请求的 chosen state 重新加入 max。

回填阈值取 `q=1/10`。平方势给 `W_i>1/5` 后，`Good={j:Q_j>=q}` 在每个 outer 中留下正质量的 home；Good helpers 的 fallback winner bundle 交给 outer，其余 helper 回 own state，再把全部原 jobs（包括 inactive、duplicate、zero payload）编译回有限端点，得到 `C_max<=19/10`。这也是限定域的算法结论，不是本批有限 JSON 的新算法。

## 2.3 量词边界

规范算法只覆盖 single-state outer、互异 homes、k⁴-tiny home weights 和共享 B fallback。它不覆盖多 state outer、重合 homes、home 上额外叶、一般 non-UD groups 或一般 UM。其 source-gap 推论只对“归约所有输出都落在该 typed 域、YES actual OPT<=1、NO actual OPT>=2-gamma 且固定 gamma<1/10”的特殊 promise 成立；不推出一般 UM hardness 或 P≠NP 结论。

# 3. 后端脚本逐行核对

脚本先构造每个 helper 的 state options、empty 概率和每个 resource/rule 的 rank；`event_probability` 对同一 helper 只求和一个 shared state，不把不同 state 当作独立。`moments()` 计算每个 group 的 mean、second moment，以及同一 group 的两资源 winner-pair 交叉项；`brute()` 枚举所有 helper state/request profiles 和每个 resource rule，直接累加实际 winner values；两者必须逐项相等。`derandomize()` 依次固定 state、request bits、resource rules，在每一步重新计算平方势并选取势最小分支，最后核对 moments 已退化为实际值及 exact squared potential。

有限审计两例都只有 3 helpers、2 outers、2 states/helper、2 resources、2 rules，request rate 分别为 1/3 与 1/2。第一例完整枚举 2048 个 profile/rule outcomes，均值为 `(137/576,371/1296)`，二阶为 `(13565/124416,761/3888)`，初始势 `4467527/26873856`，11 步后势 `565057/26873856`，实际值 `(3/8,1/3)`。第二例枚举 2916 个 outcomes，均值 `(799/4096,685/3072)`，二阶 `(5917/65536,1547/9216)`，初始势 `25725607/150994944`，11 步后势 `8248921/150994944`，实际值 `(1/8,0)`。两例均以 exact Fraction 验证 direct moments 等于 brute moments、CE 势不增、末态 moments 等于实际 values 的平方。

第二例 outer 的最终值为 0；它没有 tiny-home 和规范均值前提，因此不是规范算法反例，也不能拿零值当作失败结论。脚本明确 `whole_scheduling_algorithm_checked=false`、`small_weight_class_instantiated=false`，与其有限范围一致。

# 4. root replay 的独有内容和可复现边界

第二源给出命令 `python3 .../sol_general_repair_balanced_welfare_pair_backend.py`、代码 SHA256 `460679c82477934bcfdc3ad326f39dd0d0dd0baf7fa4fd75d02df015c7f6b2f0`、stdout SHA256 `e7433d8476ab2ae99218b4e0307198d0a586311fc84734b16ff3d6efb985c21d`、Fraction exact、无 seed、exit code 0。它明确 root 完整读取 standalone source、Proof/Exact 和 independent Exact-first/read-after；root 参与过 denominator/request-coin caveat，因此不是作者之外的盲审。

我对冻结脚本做了独立重放，输出逐项得到相同的 2048/2916、11 步 CE、势和最终值；重放结果另存为 `backend-rerun.json`。这只复核 finite backend 的算术和实现，不代替规范 v1 的 LP 可行性、MW 轮数、方差证明、CE 复杂度、Good 回填或全 jobs 编译。

# 5. 与全仓成果的关系及处置

1. 与《归一化门菜单福利与对数调色板 padding 有限审查》：两者都使用 normalized/menu 资源和有限 welfare 后端，但 gated-menu 的 flat/gated 量词、输出模式和证据不同；本批只保留 winner-moment CE 的多 outer 语义，不合并福利比率。
2. 与《长链联合投影与最优凸包边际障碍有限审查》《配置保环与高周 girth 有限审计》：那些是 unrelated-machines 配置/图结构障碍；本批是 typed Q 的正面限定算法后端，不能用后端样例去否定配置 gap，也不能把 19/10 推到一般 UM。
3. 与规范 v1 审查：它已单独记录 Exact/Proof、独立重构和有限软件的作者身份边界；本批将两个冻结 JSON 的独有软件内容归档到 evidence，并明确 root 重放不是外部评审。
4. 与 v4/k²、UD-leaf 后续稿：审查正文明确旧 v1 的 k⁴ tiny 域和后续 v4 追加章节不能混合。这里不把 k²/vector variance 或高阶偶矩 learning 的主张带入两个后端 JSON。
5. 与当前六人 CAG/SPE：typed fallback resource、machines 和 winner loads 与客户目录覆盖/SPE 完全不同，保持 unrelated-machines 隔离。

逐源处置：

- `19575b9ed8447b7d0589`：`integrated`。两例 exact moments、brute outcome counts、CE 步数和最终 values 写入本正文第 3 节，并保留原 JSON 副本。
- `3743fee56233f1e58188`：`retained`。它的独有内容是代码/输出 hash、运行命令、root 实读范围和“非完整算法”边界；保留为 reproducibility metadata，不把 root 重放当第二数学证明。

接续义务是实现或独立验证规范 LP/MW/variance/CE 全流程，并扩展到多 state outer、非 tiny home 和一般共享资源；当前批没有完成这些任务，也没有解决 UM-TARGET-v1、一般近似算法、一般 hardness 或外部新颖性。
