---
id: "customer-attraction/fixed-strategy-up-cone-finite-probe"
kind: "computation"
type_tag: "计算"
title: "固定完整策略 UP 锥有限探针"
status: "finite-floating-probe-replayed; no-general-bound"
truth_status: "fixed-policy-sample-checks-only; no-half-theorem-or-counterexample"
review_level: "full-source-read-isolated-replay-and-certificate-check"
scope: "random customer-attraction instances, complete pure SPE certificates, distinct-support UP slack LP"
summary: "R-51 cone_probe.py 将规范完整纯 SPE 证书转成固定策略客户锥，在随机样本和互异主题支持上做浮点 LP 探针；本批复现得到最小 slack=0，未发现负点，也没有精确有理锥或全策略结论。"
source_refs:
  - "source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/global/cone_probe.py"
  - "source:aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c:research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/global/cone_probe.py"
inventory_blob: "ad314a7cb5a9799f64e2b4988ab3bb42a2af5bfb"
source_sha256: "1b5a5cbc68153f6660b34c4fb5d9f6d291b1c680f780fa819679424141caf73a"
source_size_bytes: 4226
evidence_paths:
  - "archives/customer-attraction/tools/evidence/fixed-strategy-up-cone-probe/original/cone_probe.py"
  - "archives/customer-attraction/tools/evidence/fixed-strategy-up-cone-probe/original/source.json"
  - "archives/customer-attraction/tools/evidence/fixed-strategy-up-cone-probe/replay/run_m3k5_s1.stdout"
  - "archives/customer-attraction/tools/evidence/fixed-strategy-up-cone-probe/replay/run_m3k5_s100.stdout"
  - "archives/customer-attraction/tools/evidence/fixed-strategy-up-cone-probe/PROVENANCE.json"
related_objects:
  - "archives/customer-attraction/state/定理/完整策略锥的静态安全值对偶--定理.md"
  - "archives/customer-attraction/state/计算/完整历史求解器的精确复现--计算.md"
  - "archives/customer-attraction/state/计算/R-51四主题完整历史MILP候选--计算.md"
---

# `f100977eb05f44de1526` 独立审查：`cone_probe.py`

## 来源与读取范围

- 冻结路径：`research/workspaces/customer-attraction/R-51ca8c2b36184c41818099bc490374ca/global/cone_probe.py`
- 冻结 blob：`ad314a7cb5a9799f64e2b4988ab3bb42a2af5bfb`；文件 4,226 字节；SHA-256 `1b5a5cbc68153f6660b34c4fb5d9f6d291b1c680f780fa819679424141caf73a`。
- `legacy-cleanup` 与 `main` 两个冻结来源指向同一 blob/哈希。源码已逐行读取（96 行），并在隔离目录按原路径层级放入规范 `customer_attraction` 依赖后运行。
- 对照读取：同 R-51 的 `global/README.md`、`cone/README.md`、五个 `full_tree_*.json` 数值 MILP 输出；全局现行 `research/current/customer_attraction/strategy_cone.md`（CA-STRATEGY-CONE）和 `security_cone_duality.md`（CA-SECURITY-CONE-DUAL）。

## 程序实际做什么

`arrays(instance, certificate)` 把一个由规范 `ExactSPESolver.certificate` 给出的**完整有序历史策略**翻译成 LP 数据：

1. `membership` 有 `2^k-1` 行（非空兴趣类型掩码）和 `k` 列；`utility` 对终局计数计算每个主题在每个客户类型上的 `1/load` 分摊。
2. `walk` 穷举从每个有序历史开始的全部 `k` 个行动分支。对指定行动与每个偏离行动各写一行 `gamma = chosen_utility - deviating_utility`；包含指定行动自身的零行。`branches` 保存这些真实离轨续局的效用向量。
3. `actual` 是策略根路径的终局计数；`c` 是根路径覆盖的客户类型指示向量（`W=c·weights`）。`v[a]` 沿根路径把每个玩家在“当前前缀改选主题 `a`、之后执行原证书”时的效用向量相加。

`main` 的输入字段是 `--players`（默认 3）、`--topics`（默认 5）、`--samples`（默认 100）、`--seed`（默认 90230）和可选 `--output`。每个样本在全部非空掩码上随机生成客户重数：掩码大小 ≤2 时用 `randrange(0,9)`，更稠密掩码从 `[0,0,0,1,2]` 取值，零重数删除。规范 SPE 求解器枚举终局计数，按福利升序只取前三个最低福利终局；每个终局只展开一个默认 tie-breaking 的完整证书（离轨续局按当前行动的最小效用候选取第一个）。

对每个证书仅遍历一个有限集合：`combinations(range(k), min(m,k))`，即大小为 `min(m,k)` 的**互异主题**组合。令 `o` 为该组合覆盖的客户类型，目标为

```text
(m-1)c + Σ_{a in support} v[a] - m o
```

在 `gamma·weights >= 0`、`c·weights = 1`、`weights >= 0` 下调用 SciPy/HiGHS `linprog` 最小化。只有浮点目标低于 `-1e-7` 时才把 `lp.x` 用 `Fraction(float(w)).limit_denominator(1_000_000)` 近似，并可写出 `m,k,portfolio,float_slack,weights,certificate`；没有任何精确有理可行性、对偶乘子或证书回放步骤。

## 可复现运行与检查

固定依赖下运行：

- `m=3,k=5,samples=1,seed=90230`：退出码 0；stdout 两条改善记录，最低 slack 为 `0.0`，未写出负例文件。记录为 `(sample=0, slack=0.75, actual=[0,1,1,1,0], portfolio=[0,1,2])` 后 `(slack=0.0, portfolio=[0,1,4])`。
- 同参数 `samples=100`：退出码 0、stderr 为空、stdout 与上面相同，未写出 `--output` 文件；因此这次运行没有浮点负 slack。
- 对 sample 0 重建的 24 个客户类型（客户总数 86）独立调用 `verify_certificate`：唯一 SPE 终局 `[0,1,1,1,0]` 的证书有效，检查 31 个有序历史、124 个偏离，0 个错误/违反。
- 边界输入 `--players 0 --topics 0 --samples 1` 在 `arrays` 第 39 行失败：空 `membership` 使 `c` 退化为 `numpy.float64`，`len(c)` 抛 `TypeError`。`--players 1 --topics 0` 由规范 `Instance` 先抛“positive-player games need at least one legal topic”；负玩家数由模型校验拒绝。上述失败均是边界输入失败，不是数学反例。

## 与已有 cone/strategy 对象的精确关系

`gamma` 行正是 CA-STRATEGY-CONE §1 的固定完整策略约束 `G_σ r >= 0`（同一有序历史、同一真实离轨终局、非负客户类型重数锥）；`c` 的归一化也对应其根终局福利 `W_σ(r)=c·r`。因此该程序确实在探测一个固定策略的客户重数锥，而不是把同计数历史错误合并成 Markov 策略。

但它只在随机样本、每样本最多三个最低福利终局和每终局一个证书上取样；不枚举全部完整策略树、全部 SPE 证书、全部客户输入或全部比较组合，也不构造 CA-STRATEGY-CONE 所要求的有理最优点/精确对偶证书。目标是 UP 型静态组合 slack 的有限诊断，不是 `L_{σ,J}` 的完整上界。

`security_cone_duality.md` 的对象是静态安全值 `β_B(p)`、混合菜单 `Q` 与 Farkas 对偶恒等式；`cone_probe.py` 没有 `p`、`β`、`Q` 或安全值目标，不能作为该安全锥接口的证书。R-51 `full_tree_*.json` 另属“numerical complete-history MILP proposal only”，其 `status=1` 超时及浮点 `fun` 也不能替代本程序的 SPE 锥核验。

支持集合只测试恰好 `min(m,k)` 个互异主题；README 已明确这是 distinct-support 探针。若要处理允许重复主题、少于 `m` 个主题的比较或全部最优支持，需另行枚举并重新核验，不能从本程序的零 slack 外推。

## 失败机制与证据边界

1. **浮点与证书缺口。** `gamma`、目标和 HiGHS 状态都是 NumPy/SciPy 浮点；`-1e-7` 只是触发阈值。写出的 `Fraction` 仅是有界分母近似，没有逐行验证 `gamma r >=0`、`c r=1`、整数缩放后 SPE 或目标等式。近零正/负都可能是数值误差。
2. **搜索不完备。** 随机样本、低福利前三个终局、每终局单一 tie-breaking 证书和互异支持组合都严格小于全策略锥/全量词；无负结果只是未发现。
3. **空锥与资源错误。** 若随机生成零客户，`c·r=1` 约束不可行，程序把普通 `linprog` 失败升级为 `RuntimeError`；未给专门诊断。`--output` 的父目录不自动创建，只有触发负 slack 后才可能因路径不存在抛 `FileNotFoundError`。
4. **环境/规模限制。** 依赖 NumPy、SciPy/HiGHS；`ROOT=Path(__file__).resolve().parents[5]` 要求原始五级路径布局。客户类型按 `2^k-1` 增长，SPE 递推按完整树增长，无复杂度或超时承诺。

## 语义处置

保留为 customer-attraction 的“固定完整策略客户锥 / UP 目标有限浮点探针”程序资源及其复现 stdout；不升级为半覆盖定理、反例、全策略锥上界、SPE 证书或安全值支付定理。建议正式对象仅记为计算/探针，正文必须链接本源码哈希、参数、支持边界和上述失败机制；与 CA-STRATEGY-CONE 建立“实现/有限检查”关系，与 CA-SECURITY-CONE-DUAL 建立“目标不同、不可互证”的边界说明。
