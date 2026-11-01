# R-44b24 direct_global 四源实读与处置建议

实读者：并行清洗代理 `r44_direct_global_a`。工作区分支：`rebuild/research-v2`。本稿只供根 Boss 串行整合，不是远端回执。

## 来源与冻结指纹

| source id | frozen path | SHA-256 | 实读/复现 | 建议处置 |
|---|---|---|---|---|
| `973c319c331dbcaac2f2` | `research/workspaces/customer-attraction/R-44b24f3962bd4f68a4b6913610c0d417/direct_global/few_exceptions_audit.json` | `9d71fd5017d0fa35a2c65a9a760315833cec55921af0224586f2c250c8e90afc` | 读取 40 参数/125424 客户角点的发现审计输出；保留 `includes_template_failure_outside_scope=true` 与 `Q_CAG_HALF=OPEN` | `retained`（有限发现审计证据；不是新定理） |
| `d2c81ef177368463b907` | `.../direct_global/few_exceptions_independent_audit.json` | `1a9f12071b55113862155c8f505d85df3b053cace07417e018ffa7c171c2663b` | 与同目录脚本的运行输出逐字段相同：411 参数对、1,056,384 角点和 K 因子检查；范围说明仍是有限审计、一般证明在 review 正文 | `retained`（脚本运行产物） |
| `f0f92ac8658ef5797aad` | `.../direct_global/few_exceptions_independent_audit.py` | `dd93c857c93a63d7cecd6fdcb39d40c12b78dd452f333971628da696028f1f9` | 在隔离副本以 Python 3.12.14 运行成功；输出 SHA 与 `d2c81...` 相同；未导入发现脚本/求解器 | `retained`（独立 exact 审计程序） |
| `55b169d3968183546253` | `.../direct_global/majority_with_early_exception.md` | `39fac1023d349fe478272363dff9e40e4a5943dff82754160429addb95770096` | 全文实读；为 m>=4、实际末两位均 A、只有一位早期 B 的特殊 half 证书；明确 A/B 可相同、空或交叠，保留重复/空主题/平局；一般 Q-CAG-HALF 仍 OPEN | `retained`，并新建候选对象（见下） |

所有四源均来自冻结双版本 `68fad804ec5946cb296f77dc5b336308a66abf12` / `aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`；未修改共享 clone。

## 数学核对

### 1. 发现审计 `few_exceptions_audit.json`

原输出仅是有限回归状态，不承重无限量词。它记录 `parameter_cases=40`, `customer_corner_cases=125424`, `minimum_Q=0`, `r_range=[1,8]`，并明确含超出模板范围的失败样例、主目标 OPEN。它应与已整理的 `customer-attraction/penultimate-few-exceptions-square-threshold` 定理和现有规范审计 `penultimate/replay/few_exceptions.json` 并列保存：后者是 80 参数/54,240 aggregate-corner 的独立审计，不能覆盖本源的 125,424 发现计数。

### 2. 独立审计程序与 JSON

`few_exceptions_independent_audit.py` 只用 `Fraction`，按 m=5..80、101、257、1001 与合法 r 生成 411 对参数，逐角检查 A 内/A 外分支和 K 因子身份；隔离运行输出：

```json
{"status":"all independent exact checks passed","parameter_pairs":411,"corner_checks":1056384,"raw_K_factor_checks":1056384,"scope":"finite formula audit; all-parameter proof in few_exceptions_independent_review.md","python":"3.12.14"}
```

输出与冻结 `few_exceptions_independent_audit.json` 字节相同（同一 SHA-256）。这是独立有限审计，不替代 `few_exceptions_independent_review.md` 中承重的全参数解析分支；应与现有 80 参数/54,240 角点审计区分开。

### 3. `majority_with_early_exception.md` 的独有范围

该稿提出 `CA-EARLY-SINGLE-EXCEPTION-HALF-v1`：任意有限单位客户/有限非空共同目录、任意 `m>=4`、某完整历史纯 SPE 实际末两位都选 A，另有一名位于前 `m-2` 的早期玩家选 B，则 `2W>=OPT_m`。比较主题允许重复、空集与任意平局；A、B 可相同或交叠。证明用同一真实前缀下的 `S,Z,V` 菜单非负量，另用早期 B 改 A 的粗保底 `R=u_B-|A|/m>=0`，取 `mu=m(m-4)/(2(m-2)(m-1))`，逐客户对 `ell,d` 的双线性四角给出非负余项。

它不是现有平方阈值定理的简单重复：平方阈值定理的 `r=1` 要求 `m>=5` 且“至多一位早期主题不包含 A”；本稿覆盖 `m=4`，且不要求 B 不包含 A，同时允许 A=B/交叠。对于 `m>=5`、B 不包含 A 的部分，与 `CA-PENULTIMATE-FEW-EXCEPTIONS-HALF-v1` 范围重叠，但支付量 `mu` 与逐客户证明是独立证书，不能因重叠直接丢弃。

本稿原文状态为“完整证明候选，等待独立审查”。我跨读并隔离运行了其配套 `audit_early_exception.py`（source id `d1959b83f7a78511ebb5`，属另一 Boss 的现有认领；未抢占）及对应 JSON（`fb9feb751f521b9ecac3`），得到：

```json
{"status":"exact regression passed; arbitrary-m proof is analytic","binary_membership_cases":21504,"corner_checks":2400,"scope":"early singleton exception with last two actions equal, m>=4","general_half_coverage":"OPEN"}
```

该回归只验证有限 membership/四角代数与 mu 范围；无限 m 的承重仍来自候选稿的显式解析证明。当前没有外审/新颖性认证，也没有把该结果提升为一般六人 Q-CAG-HALF。

## 归档与后续建议

1. 现有正式对象 `archives/customer-attraction/state/定理/倒二主题少量早期遗漏平方阈值--定理.md` 已覆盖 `r>=1,m>=(r+1)^2+1` 的更一般解析定理，但其 r=1 不覆盖 m=4，也不覆盖“B 可能包含 A”的无额外关系表述。
2. 对 `55b169...` 新建候选正文，建议路径：`archives/customer-attraction/state/候选/末两位同主题单早期例外半覆盖--候选.md`，稳定 id 建议 `customer-attraction/early-single-exception-last-two-equal-half`，frontmatter 标为 `kind: theorem`, `type_tag: 候选`, `status: candidate`, `truth_status: conditional-proof-candidate`，并清楚写出“独立 exact 回归通过；尚无完整独立解析审查”。若根 Boss 采用更强语义审查后认可，可再迁移到 `state/定理/`，不要在本批直接声明一般 Q-CAG-HALF 已闭合。
3. 将 `973c...`、`f0f...`、`d2c...` 的原字节和运行记录并入证据目录（建议 `archives/customer-attraction/tools/evidence/penultimate/r44b24-direct-global/`），附 manifest/README，链接现有平方阈值定理与新候选对象；不要把 973 的 125424 计数改写成规范审计的 54,240，也不要把脚本有限检查当全参数证明。
4. `clean done` 时四源分别引用真实目标：前三个 evidence 文件，`55b...` 引用候选正文；建议前三个 `retained`，`55b...` 在候选对象入库后 `retained` 或 `integrated`（依据根 Boss 是否接受“candidate”对象为正式整合）。

## 边界

- `d1959.../fb9...` 属 Boss3 的并行认领，本文只作比较与复现，不应重复 claim/done；应在正式回执中作为 cross-reference。
- 这四源都没有证明无条件一般 Q-CAG-HALF，也没有制造完整 SPE 反例；`Q_CAG_HALF=OPEN` 必须在 evidence README 与候选正文中保留。
