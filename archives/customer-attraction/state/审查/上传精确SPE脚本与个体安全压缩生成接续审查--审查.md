---
id: customer-attraction/uploaded-exact-spe-and-security-compression-review-20261031
kind: review
type_tag: 审查
title: 上传精确 SPE 脚本与个体安全压缩生成接续审查
status: complete-source-read-with-exact-replay-and-external-generator-boundary
truth_status: exact-history-enumerator-replayed; individual-security compression generator preserved but not rerun without its external source input
review_level: full-source-read-code-replay-hash-comparison-with-existing-security-evidence
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/customer_attraction/individual_security_2026-10-10/compression_generator.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/customer_attraction/individual_security_2026-10-10/compression_generator.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/customer_attraction/uploaded_2026-10-10/SHA256.json
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/customer_attraction/uploaded_2026-10-10/SHA256.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:history/source/notes/customer_attraction/uploaded_2026-10-10/exact_spe.py
  - source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:history/source/notes/customer_attraction/uploaded_2026-10-10/exact_spe.py
evidence_paths:
  - archives/customer-attraction/tools/evidence/uploaded-exact-spe-package-20261031/manifest.json
  - archives/customer-attraction/tools/evidence/uploaded-exact-spe-package-20261031/compression_generator.py
  - archives/customer-attraction/tools/evidence/uploaded-exact-spe-package-20261031/SHA256.json
  - archives/customer-attraction/tools/evidence/uploaded-exact-spe-package-20261031/exact_spe.py
  - archives/customer-attraction/tools/evidence/uploaded-exact-spe-package-20261031/verification_report.replay.json
  - archives/customer-attraction/tools/evidence/uploaded-exact-spe-package-20261031/auxiliary_counterexample.replay.json
related_objects:
  - ../审查/顺序客户吸引来源记录与上传半覆盖界限审查--审查.md
  - ../审查/逐人安全与全树流增量审查--审查.md
  - ../审查/聚合末位保底与上传大实例增量审计--审查.md
  - ../反例/逐人静态安全值末位保底--反例.md
  - ../计算/完整历史求解器的精确复现--计算.md
  - ../../tools/evidence/cag-eptas-individual-20261030/individual_security_independent_review.md

# 上传精确 SPE 脚本与个体安全压缩生成接续审查

本批逐字读取三个冻结来源：`compression_generator.py`、`SHA256.json`、`exact_spe.py`。三者均属于顺序客户吸引（CAG）模型，不是双设施负载模型。单位客户用兴趣主题掩码表示，提供者按完整有序历史依次选主题，终局客户在覆盖者之间均分。`exact_spe.py` 的脚本头部直接声明“不证明 one-half welfare conjecture”；本审查保留该边界。

## 1. 原件身份、哈希和证据副本

| source ID | 路径 | blob | 字节 | SHA-256 |
| --- | --- | --- | ---: | --- |
| `fc054f418786867ca8d5` | `history/source/notes/customer_attraction/individual_security_2026-10-10/compression_generator.py` | `d55982036c703fc7ebf0f7ffeeed14f1fa715b2c` | 4239 | `5347b728d99eb8c9a6580a7c8995431127c5f579e5547b91120905b374b46986` |
| `3617ba0356de807577c2` | `history/source/notes/customer_attraction/uploaded_2026-10-10/SHA256.json` | `7c5e1e3de93101cbbc1abdf8b68ab7b72a36153f` | 374 | `c0ca4cf1fb43085d188943d17235e830804779d296ff2244362c87e3549ed66f` |
| `f6081a79c3dc3cb6c4db` | `history/source/notes/customer_attraction/uploaded_2026-10-10/exact_spe.py` | `70708cde4f283ffd852fc88b752730bb032a0ae9` | 12157 | `ab1ccf71036503fe1d878a331571fc96aa2ab2d962f221b1cf33db1550b57747` |

三个原件与 `exact_spe.py` 的实际重放输出保存在 `archives/customer-attraction/tools/evidence/uploaded-exact-spe-package-20261031/`。`SHA256.json` 的四个条目与本批 clean-show/证据哈希对应：`RESEARCH.md`、`auxiliary_counterexample.json`、`exact_spe.py`、`verification_report.json`。脚本实际重放时，因其 `__main__` 固定写入脚本所在目录，生成的报告先落在 `cleanup/workspaces/Boss2/`，随后原样复制为 `verification_report.replay.json` 和 `auxiliary_counterexample.replay.json`。

## 2. `exact_spe.py` 的模型、递推和完整历史验证

### 2.1 精确整数收益表和输入域

`Game(m,n,weights)` 将 `weights[mask]` 解释成兴趣掩码对应的单位客户重数，拒绝非整数、负数、越界掩码，并允许零客户、零提供者和空兴趣类型。主题数为 `m`，提供者数为 `n`；所有终局主题计数以多重集形式枚举。令 `Q=lcm(1,...,n)`，脚本用 NumPy 整数表存储每个主题在每个终局计数向量下的精确份额，客户收益乘以 `Q` 后全部成为整数；`welfare` 是覆盖客户总数。

构造器限制密集表规模小于 20,000,000 个掩码×终局格，并检查每个终局收益总和等于福利乘 `Q`。这是实现边界，不是数学模型限制；任意更大输入需要稀疏或按需实现。

### 2.2 所有可能纯 SPE 终局的递推

对前缀计数 `h`，`outcomes(h)` 递归计算每个下一动作子集的终局集合；动作 `a` 的门槛是该分支中行动者收益的最小值，当前行动者选择收益达到所有动作分支门槛最大值的终局。于是递推保留所有历史依赖平局，而不是把相同计数前缀绑定成同一个后续动作。`certificate(target)` 逐历史构造一份完整策略；处方分支保留目标终局，其他动作分支选择行动者收益最小的子终局作离轨续局。

`verify(policy)` 递归遍历**每个有序历史**，要求策略长度为

\[
1+m+m^2+\cdots +m^{n-1},
\]

并在每个节点比较所有合法动作的真实续局收益，包含所有离轨节点。它不冻结偏离后的后手动作，也不把终局计数集合当成 SPE 证书本身。

### 2.3 有限测试和本批实际重放

脚本 `self_test()` 包含：空/单/重复覆盖与零客户边界；公开 lower-bound 家族 `n=1,...,5`；两主题三提供者、三种客户重数各取 0/1/2 的 27 个游戏，每个穷举全部 128 份完整历史策略；100 个固定种子随机有理/整数游戏，检查两个 theta 下界和 `4(n-1)/(n(2n-1))` 福利界。然后构造 12 主题、4 提供者、26,171,145 单位客户的大实例，目标终局由 12 个主题中的 `(0,4,5,8)` 计数给出。

本批实际执行 `python3 customer_attraction_uploaded_exact_spe.py`，精确重放通过，报告字段为：

* `exhaustive_crosscheck_games=27`、`policies_per_crosscheck_game=128`、`proved_bound_random_crosschecks=100`；
* `providers=4`、`topics=12`、`unit_customers=26171145`、`offset=6391`；
* `verified_ordered_histories=1885`，在轨动作 `[8,4,5,0]`；
* 在轨收益 `(6135345,6135380,6135380,6135371)`，`last_player_floor=6135346`；
* `spe_coverage=24541476`、`optimal_coverage=24541532`、`twice_spe_coverage_minus_optimum=24541420`；
* 根纯 SPE 终局数 `root_spe_outcome_count=97`。

这与来源 `verification_report.json` 的全部字段逐项一致。它证实的是一份完整策略和有限回归；它没有证明四人或六人的一般 half 定理。

## 3. `compression_generator.py` 的个体安全压缩逻辑

该脚本不是 `exact_spe.py` 的同一实现，而是从一个外部 `individual_security_failure_360.json` 读取三提供者、六主题的已保存策略。脚本固定 `n=3,m=6,N=63`，从每个有序历史的策略和终局构造：

1. `G`：所有真实单步策略偏离的收益差向量；
2. `secr`：静态两人背景下，候选客户重数相对于根收益的安全差向量；
3. `sep`：所有主题对的严格分离向量。

它用 `scipy.optimize.milp` 寻找非负整数客户重数 `w`，约束每个真实偏离不增、每个静态安全差严格至少 `1/16344`、主题对分离至少 1。随后用 `linprog` 求主要客户混合分布和静态 rival 分布，使用 `Fraction.limit_denominator` 得到有理概率，再用整数/有理点重新验证全部差异。输出记录客户总数、正类型数、security 值、在轨收益、福利和最优覆盖，并明确 `MILP only proposes integer weights; ... no global minimality claim`。

该脚本的绝对输入路径 `/workspace/scratch/4fa21fc3d3cc/security_cone_attack/individual_security_failure_360.json` 在本仓库工作区不可用，因此本批**没有执行 compression_generator.py**。已有 `archives/customer-attraction/tools/evidence/cag-eptas-individual-20261030/individual_security_independent_review.md` 和 `continuation-security/replay-individual.json` 提供了同类 34 客户候选的独立 Fraction 全历史复核：3 位提供者、6 个主题、34 名单位客户，43 个有序历史、258 个动作比较，第一位个人静态安全差 `-11/82`，但 welfare `32`、OPT `34`，half margin 仍为 `15`。因此本批把 generator 处置为“算法来源和约束逻辑已读，实际输出依现有独立证据”，不把未执行的 MILP 当作新证书。

## 4. 与现有对象的关系和边界

| 本批内容 | 现有对象 | 接续结论 |
| --- | --- | --- |
| 完整历史 SPE 递推、证书和 27×128/100 有限测试 | `计算/完整历史求解器的精确复现` | 实际重放通过；有限精确验证，不推出任意人数 half |
| 12 主题、4 人大实例逐人 theta 失败但 half 保持 | `反例/逐人静态安全值末位保底`、上传增量审查 | 第一位 `theta-1`，但 `2W-OPT>0`；只否定逐人桥 |
| MILP 个体安全压缩脚本 | `cag-eptas-individual` 与 continuation-security 证据 | 依赖外部输入；已有 34 客户独立复核承接其数学边界 |
| SHA256 绑定 | 本批 manifest 与 uploaded source | 原始代码/报告哈希一致，未把 provenance 字段当证明 |

四个关键边界必须保留：

* `exact_spe.py` 的 `outcomes` 集合是所有可实现终局，不是一个给定策略；`certificate` 才逐历史选取策略，`verify` 才检查全树最佳回应。
* 大实例否定的是“每位玩家收益至少 theta”的辅助桥；第一位低 1 不构成 half 反例。
* `compression_generator.py` 的 MILP 只寻找一组整数重数，不证明全局最小客户数、唯一性或文献新颖性；绝对路径依赖使其在本工作区不可独立复现。
* 三人 `8/15` 解析界、四人上传实例和双设施模型各自有不同模型身份，不能因都含“security”或“half”字样跨模型推导六人半覆盖。

本批原件、脚本重放报告和哈希已保全；未执行 Git commit、push 或 `clean done`，Boss 串行 checkpoint 后再按 receipt 逐来源确认。
