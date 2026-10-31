---
id: "unrelated-machines/conditional-leaf-hall-v3-independent-exact-review"
kind: review
type_tag: 审查
title: "条件叶 Hall v3 新 MC 条款独立重构"
status: independent-exact-pass-v3-clause
truth_status: "R-cons-projection-reconstructed; finite-fixtures-recorded; Q_t-sharp-value-remains-candidate"
review_level: "full-11007-byte-exact-first-review-read-and-v3-comparison"
scope: "v3 common leaf-edge marginal clause (MC), exact projection extension, matching-mixture decomposition, and finite independent audit record"
summary: "独立审查在未读 v3 author transport proof/checker 前，重构了新 MC 条款的 hole-transport extension：任意 basic (lambda,z) 可按显式 q_(s,j) 表扩展到一致 global leaf-edge marginals，含 beta=1、d=0/1、zero lambda 边界；并记录三个 Fraction fixtures 的 matching-mixture 审计。它不重审旧 §§1–8，也不把 Q_t 的 V=1/t sharp-family 陈述升级为一般定理。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/unrelated_machines/sol_conditional_leaf_hall_consistent_marginals_exact_first_review.md"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/unrelated_machines/sol_conditional_leaf_hall_consistent_marginals_exact_first_review.md"
  - "clean:e3bf2fef1967903a2e65"
related_objects:
  - "../障碍/一致条件叶边际仍无福利下界--障碍.md"
  - "条件叶Hall与共享汇点联合审查--审查.md"
  - "归一化菜单福利与配置证书双源审查--审查.md"
source_sha256: "783e27cbc45db0421164d2953d48c47ee66a8c0969210e399a9adb91fbf7e0cf"
source_size: 11007
evidence_paths:
  - "archives/unrelated-machines/tools/evidence/conditional-leaf-hall-v3-independent-review/original/sol_conditional_leaf_hall_consistent_marginals_exact_first_review.md"

# 1. 来源身份和实际读取范围

`sol_conditional_leaf_hall_consistent_marginals_exact_first_review.md` 是独立审查稿，大小 11,007 字节，源 SHA-256 为
`783e27cbc45db0421164d2953d48c47ee66a8c0969210e399a9adb91fbf7e0cf`。原字节已复制至 evidence 并核得同一 SHA。

审查者先独立重构 v2 Exact，之后只针对 v3 新增 MC 条款进行 Exact-first 重构，再读取 v3 身份头和 §9；没有读取 v3 author transport proof、author checker、sol_nsw draft 或其他作者推导。它明确不是全候选的 fresh blind review，也没有倒写旧 v2 的读序。v2 Exact-first/author-read-after 的 hash、v3 whole-file hash 和外部独立 audit 程序/JSON hash均在来源中记录；本对象保留这些记录，但不把未随来源附带的外部 scratch 文件冒称为本轮新证据副本。

## 2. Hole transport：把 MC 约束降成二维表

固定一个 old resource u，其 d 个 positive core neighbors 按端口顺序 1,...,d。令

`b_j = sum_s z_(c_j,s,u)`,  `sum_j b_j <= 1`.

选择 global rational hole distribution `pi`，满足 `pi_j >= b_j` 且 `sum pi_j=1`（来源给出把全部 slack 加到最后坐标的确定性选择）。一个 hole-j path matching 将 leaf i 匹配到 port i（i<j）或 port i+1（i>=j）；按 pi 混合得到 global y0。

对某个 core c，独立审查构造表 q_(s,j)，满足

`q_(s,j) >= 0`,  `sum_j q_(s,j)=lambda_(c,s)`,  `sum_s q_(s,j)=pi_j`.

若 c 拥有 port i，要求 q_(s,i)>=z_(c,s,u)；无 port 时没有正 z。由 q 表导出的条件叶流为

`y_(c,s,ell_i,u_i)=sum_(j>i) q_(s,j)`,

`y_(c,s,ell_i,u_(i+1))=sum_(j<=i) q_(s,j)`.

每个 leaf row sum 是 lambda；port j 的 leaf load 为 lambda-q_(s,j)，因此由 own-port 下界保证 conditional capacity。对 s 求和并使用 q 的列和 pi，正好得到同一个 global y0，因而满足 MC。该推导只要求同一条 path 的 edge marginals，不要求所有 cores 共用完整 matching 的 joint law。

## 3. 任意 fractional z 的显式 q 表

若 c 拥有 port i，令 `theta_s=z_(c,s,u)`、`beta=sum_s theta_s=b_i`；令 delta 在 i 处为 1、其余为 0。若 c 无 port，则 theta、beta、delta 全为 0。对 beta<1，审查给出

`q_(s,j) = theta_s delta_j + ((lambda_(c,s)-theta_s)/(1-beta)) * (pi_j-beta delta_j)`.

非负性来自 theta_s<=lambda_(c,s)、beta<=pi_i 和 pi>=0；行和为 lambda，列和为 pi，且 own-port entry 至少 theta_s。若 beta=1，则 theta_s=lambda_(c,s)、pi_i=1，直接设 q_(s,i)=lambda_(c,s)，其余为 0，避免除零。

审查逐点保留边界：zero lambda 自动给整行零；state 在 u 上 zero incidence 但 lambda>0 时仍接收 residual hole mass；d=1 时 pi_1=1、没有 leaf edges；d=0 时保留 unused resource，不建立 hole table/flow；zero incidence 不进入 theta/beta。R1、lambda normalization 和 core z 原值保持不变，逐 old resource 独立套用即可得到全部 MC rows。

反向 inclusion 只需注意 R_cons 是旧 R1-R2 的子系统：求和 path 的 d 个 global resource columns 与 d-1 个 leaf rows，恢复旧 `sum_j b_j<=1`，故 projection 恰为 basic polytope，而不是仅在可行性层面等价。

## 4. Conditional flow 的 full matching mixture

对固定 core-state h=(c,s)，每条 path 的 q row 总量 lambda_h。把 interval [0,lambda_h] 按 q_(h,1),...,q_(h,d) 切分；合并所有 path 的 rational partition endpoints。在每个非空子区间，各 path 都有固定 hole，拼接各自 one-hole matchings 得到一枚覆盖全部 added leaves 的 integral matching，按子区间长度加权。

该有限 mixture 精确恢复全部 conditional flows，片数至多一加各 path 的 port counts；lambda_h=0 时使用空 weighted family。它不需要按所有 path 独立组合，也不引入指数 product blowup；可在显式 old data 和 rational point 长度内构造。不同 cores/states 分开做 mixture，仍不声称所有 cores 共用一份完整 matching law。

这也解释了为什么 v3 Exact 特意不把旧 R1-R2 中“每个 state 可取 lambda 乘一个 integral matching”直接转移到 R_cons：新 MC 行通常只允许 rational convex mixture。

## 5. Q_t 中的单匹配失败与 sharp-family 作用域

Q_t 的任一 A_(a,h) path 有 D 个 core ports、各 usage 1/D，global column tight，故 pi uniform。H_(a,j) parking state 的 lambda=1/D、own z=lambda，使 conditional hole mass 全在 j；home state 的一致性迫使 j 处为零、其余 D-1 ports 各 1/D。D>=4 时，该 home conditional flow 不能是 lambda 乘单一 integral matching（一枚 hole 会把全部 (D-1)/D 质量放同一列，超过列上限），必须使用 mixture。新 Exact 的 weaker scope 因此是必要的，q 表确实提供该 mixture。

同一 Q_t 的 lambda,z=lambda 是旧 basic feasible point，故独立审查把 R_cons extension 接到原 v3 声称的 family；原菜单和完整 processing matrix 未改变，value proof `V=1/t`、complete all-job `OPT=2-1/t` 仍由 v3/既有障碍对象承担。这里的“仍”是版本关系说明，不是本审查重新证明 Q_t 全参数 value theorem。

## 6. Partition、必要性和复杂度边界

审查固定 all original groups 为 cores、added paths 为 leaves，只有在旧 source 已满足 non-threshold-original-group precondition 时自动 threshold partition 才兼容。任意 deterministic actual-allocation witness 取每个 core 一个 state，以 y0 为该 state conditional matching、其他 state flow 为零，故 state-summed flow 正好 y0，necessity 保持。

新增 MC rows 至多 `|C| E_L`，显式 rational LP 仍为 deterministic polynomial size。公式 q 在 beta<1 时除以 1-beta，需显式 beta=1 分支；非零 reciprocal 的 numerator/denominator 位长仍受 supplied rational point 的 polynomial bitlength 约束。审查没有声称 polynomial in log(t) 的 succinct output，也没有 full CONFIG/PSD hierarchy、common matching law、joint-core capacity、hardness 或 actual-OPT approximation lower bound。

## 7. 独立 Fraction fixtures 与证据层级

来源记录 self-contained standard-library Fraction audit，覆盖：

| fixture | core states | resources | leaves | MC rows | conditional rows/columns | integral pieces |
|---|---:|---:|---:|---:|---:|---:|
| Q_2 same lambda,z | 36 | 64 | 40 | 1360 | 1440 / 2304 | 176，per-state max 6 |
| partial-z / zero-lambda / zeros / d0-d1-d2 | 3 | 7 | 1 | 4 | 3 / 18 | 4，max 2 |
| beta=1 with d2 and zero states | 4 | 7 | 1 | 4 | 4 / 24 | 2，max 1 |

来源中的独立 audit code SHA 为 `d4b8a93458e584057108414aa0d883a0ea16423f255beab627aa45abed8c5e71`，JSON SHA 为 `579293d74df98b8461d41f51f836404dbb1a56a92a0585d24ec6f66cb19950b3`。这些文件来自 source note 所指外部 scratch，本轮没有取得可复制的原字节，故本对象只保存 source note 的事实记录；不得把 fixture 数量误写成一般 theorem。Q_2 complete matrix 的 201 jobs/机器负载早已有 v2 frozen audit，v3 新审查没有重新做 scheduling optimization。

## 8. 与 98f3 v3 source-only 障碍及现有 finite review 的分工

`一致条件叶边际仍无福利下界--障碍` 保存 v3 Exact-only 的 R_cons 定义、basic projection assertion 和 Q_t sharp-family candidate，状态是待证明障碍。`条件叶Hall与共享汇点联合审查` 保存 409bcd/e7c981/a36b4 的有限 JSON：同边际、Hall path projection、partial-z/zero-lambda/beta=1 fixtures；它们明确未给一般 joint-core law 或 arbitrary-scale LP backend。

本页新增的是 independent Exact-first 对 MC clause 的显式 q transport、full matching mixture、边界分支和三个 fixture audit 记录；它提高了“新条款 projection extension”在给定 explicit point 上的证据层级，但不把 source-only 的 Q_t value claim、一般 v3 projection theorem 的全称量词或实际 UM gap 自动升级为已证明定理。

## 9. 处置

处置为 `integrated` 的 independent Exact-first review：原字节证据保留，MC 条款的 q-table/mixture proof、beta/d/zero 边界及有限审计记录写入本页并链接 v3 candidate obstacle 与现有有限审查。第三阶段可建立“独立重构通过/补充证据”边；不得建立“全 v3 sharp-family 已证明”“一般近二 hardness”或“全局 joint matching law”边。
