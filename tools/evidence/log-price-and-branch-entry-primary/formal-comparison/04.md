# 动态可信门槛与剥离递归缺口：有限反例及精确重置项

## 稳定身份与范围

- **对象**：六提供者共同目录、单位客户、完整有序历史的客户吸引模型；研究目标仍是每一份完整历史纯 SPE 满足 `2W >= OPT_m`。
- **来源批次**：发布身份 `R-059140e622784d85a4e3a4dd6554f506`。原始字节和逐源哈希见 `archives/customer-attraction/tools/evidence/R-059140e622784d85a4e3a4dd6554f506/source-manifest.json`；原始路径、冻结 commit 与清洗 ID 均在 manifest。
- **证据等级**：本页把有限枚举、辅助命题反例和解析恒等式分开。它们没有证明或否定主目标 `Q-CAG-HALF`，也不能把有限失败提升成一般反例。

## 1. 辅助动态可信首利候选被精确否定

来源 `d4afcb7e902a615d25bc`（`dynamic_theta/child/README.md`）给出一个明确的辅助量词。固定合法背景 `b` 与余下人数 `r`，令 `Theta_r(b)` 为该子博弈所有完整历史纯 SPE 中当前玩家的最低可实现收益，令 `L_(r,b)(A)` 为强制当前选 `A` 后、全部完整可信孩子中的最低收益；并记

\[
F_b(A)=\sum_{x\in A}\frac1{b_x+1}.
\]

候选关系

\[
\Theta_r(b)\leq \Theta_{r-1}(b+1_A)+F_b(A)-L_{(r,b)}(A) \tag{CM}
\]

在源中被一个完全展开的有限例否定；特别地，空动作 `A=∅` 也不能让该不等式成立。源还重述了 `root_tax_failure` 的最短边界：某一合法计数前缀的 `Theta` 为 `13`，继续选主题 `A` 后末位 `Theta` 为 `11`，而新增覆盖为 `0`。所以固定动作上的 `Theta` 不是可直接望远镜的单调安全值；任何只用新增覆盖补偿下降的有限系数捷径都失效。

这只是辅助候选 `CM` 的障碍。源明说 `Q-CAG-HALF`、`TB`、`TB-ANY`、`SM-opt-exists` 仍未被否定；不能把该例登记成主目标反例。

来源 `3687a4f6085bbcb21290` 与 `6ac7f74af07e3699c9a9` 是同一辅助关系的可复核冻结产物：39 个客户、主题 `A,B,C,D,empty`，脚本按 `Fraction` 精确重放有序树，输出 `156` 个历史和 `780` 次精确 IC 检查。脚本文本明确声明只 refute corrected-monotonicity，且“不 refute TB/SM/HALF”。这使它成为有限辅助障碍而非主命题反例。

## 2. PEEL 恒等式可以成立，但递归必须支付重置项

来源 `fad09689d31ab06094d4`（`dynamic_theta/peel_independent_review.md`）独立重构同一源的末位剥离。对任意合法前缀、余下 `r\ge2` 人、旧负载 `b`，强制当前选 `A` 后保留原真实后继，源中的全输入 PEEL 恒等式通过；它合法抽出真实末位最佳回应的非负项。然而再次对同一 `\sigma` 重跑时，会精确取消一份旧的正信用，出现重置项 `R`。既有 34 客户完整 SPE 的 `Fraction` 例给出 `R=-113/164`。

因此，“第一次剥离所得全部非负项在下一次剥离仍可免费保留”是错误的递归前提。该审查保留了两个可用事实：

1. 节点级 PEEL/末位 IC 抽取本身没有发现定义或全历史量词错误；
2. 递归推导必须显式支付重置 `R`，不能把已相消的末位信用重复计入。

这与本仓库既有的“固定安全预算锥”“真实分支替代量词缺口”相容，但没有给出一般 half 付款不等式。

## 3. 旧完整 SPE 上的有限 beta-packing 探针

来源 `4964ee2c8fcb43af62a6`（`cross_tree/pivot_probe.json`）和其产生器 `a702cb0a914b5f038b9b` 只检验旧完整 SPE、有限合法 owner 与候选 beta-packing。输出状态为 `computed`，不是 theorem。六个命名例的精确 `Fraction` 极值如下：

| 例 | IC 检查 | 最优元组数 | role 最大值 | action 最大值 | `cap2` 最大值 |
|---|---:|---:|---:|---:|---:|
| `portfolio_matching_failure` | 30 | 2 | `2/11` | `2/11` | `13/11` |
| `root_tax_failure` | 1554 | 24 | `1` | `1` | `2` |
| `individual_security_failure` | 258 | 24 | `1` | `49/67` | `1696/1015` |
| `eight_cce_welfare_gap` | 84 | 6 | `3/2` | `1` | `2` |
| `coverage_opportunity_failure` | 155 | 6 | `1` | `1` | `2` |
| `prefix_balance_failure` | 1554 | 24 | `51221/76055` | `748568/1323357` | `14807/8323` |

这些数值只说明所测试的 beta 预算分配无法由某一统一、已声明的 packing 规则承重；它们不覆盖所有历史、所有 owner 或所有可能的付款不等式。故正确处置是“有限实验/候选路线障碍”，保留脚本和 JSON，不把任何一行写成主目标反例。

## 4. 与主线的接续

- 可以继续研究带显式 `R` 账户的动态剥离，或寻找能统一支付 `Delta` 与 `R` 的新势函数；当前材料尚未给出该桥。
- 不能从 `CM`、beta-packing 或有限枚举推出 `2W<OPT_m` 的完整策略反例。
- 后续引用这些材料时，应同时给出“有限范围、完整历史/SPE 量词、精确审计次数、主目标仍 OPEN”的限定。

## 来源与去向

| 清洗 ID | 原始路径 | 处置 |
|---|---|---|
| `d4afcb7e902a615d25bc` | `.../dynamic_theta/child/README.md` | 辅助候选反例，正文第 1 节 |
| `3687a4f6085bbcb21290` | `.../dynamic_theta/child/audit_corrected_monotonicity.json` | 39 客户、156 历史、780 IC 的有限证据 |
| `6ac7f74af07e3699c9a9` | `.../dynamic_theta/child/audit_corrected_monotonicity.py` | 重放脚本，保存原字节 |
| `fad09689d31ab06094d4` | `.../dynamic_theta/peel_independent_review.md` | PEEL 与负重置项，正文第 2 节 |
| `4964ee2c8fcb43af62a6` | `.../cross_tree/pivot_probe.json` | beta-packing 有限输出，正文第 3 节 |
| `a702cb0a914b5f038b9b` | `.../cross_tree/pivot_probe.py` | 输出产生器 |
| `2683aba9b2c115693606` | `.../CLAIMS.md` | 研究范围/主目标状态，导航重复 |
| `8115dafae29509422dc3` | `.../GENERAL_PROOF_WORKING.md` | 一般证明工作稿的边界，导航重复 |
| `3e57c92f99c6eea17f34` | `.../README.md` | 工作区导航，导航重复 |
| `2d7508e4a73a6cdb92fd` | `.../dynamic_theta/README.md` | 动态目录导航，导航重复 |

导航与工作稿也保留原始字节；它们没有独立数学结论，故不另复制成虚假的定理。
