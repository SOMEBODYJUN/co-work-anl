# R-18 aggregate-security 五源比较记录

## 来源、哈希与处置

| ID | 文件 | 大小 / SHA-256 | 处置 | 读取/重放 |
|---|---|---:|---|---|
| `f694c7b2bb7dd1309168` | `aggregate_security/best_optimal_budget.json` | 785 B / `ac8e72e5afb8661173da12dbc2d50d561be1a1b95227994fc5aa36aec59c81a9` | retained | 完整读取字段；budget=0、strong_gap=0、W=1、v=1/3、seed=741 |
| `7873ff0f7f3b7de5a7a4` | `aggregate_security/best_random_optimal_budget_n4_m6.json` | 23723 B / `aeafe97b664de5552d192701b665ce948cb1c73791c42c4fadf67bdb462712d7` | retained | 完整读取策略/质量/policy；n=4,m=6，budget约−3.55e−15，strong_gap=2 |
| `01680c8ffdb203194c81` | `aggregate_security/best_random_optimal_budget_n5_m6.json` | 155952 B / `543369e09e5e3d6a21ec42a26108f6b08d58f1d79b3c708ae1f920c20f4ec169` | retained | 完整解析 1555 历史 policy；n=5,m=6，budget约−7.1e−15，strong_gap=0 |
| `e612e9bb27fce77e21bd` | `aggregate_security/optimal_budget_search_summary.json` | 153 B / `1b3e0bdc9737725c348fe39455e40b2a3aa8644ad5561931e9f582b84f22ba7d` | retained | 字段完整读取；1500 samples、negative_budgets=0 |
| `4b58074c64fb716c15fc` | `aggregate_security/random_optimal_budget.py` | 3070 B / `919f27b8441a7901e48985b76d2bc069deeb2e80ceda8eb0dc5beca91cbcd226` | integrated | n=4,m=6,20 samples,seed=131 重放；best_budget=0、best_strong_gap=0 |

原始文件在 `original/`，本轮脚本回放在 `replay/random-n4-m6/`。

## 数学与实现层级

### 1. 最优预算 JSON

`best_optimal_budget.json` 只保存一个最佳点：63 维客户质量、6 维查询分布、预算/strong gap、福利 W 和最小 SPE slack。它没有 n/m、策略树、背景集合或 exact dual 证书；因此只能作为有限输出记录。companion summary 的 `root=[0,3,4]`、1500 samples 与该输出相容，但不补齐源 JSON 未给出的量词。

### 2. n=4 与 n=5 随机策略输出

两份大 JSON 由同一 `random_optimal_budget.py` 机制产生：整数质量 + LCM 逆向诱导 + 重复背景 minimax LP + 沿策略的 aggregate C。n=4 输出 `W=19,v=4.25,strong_gap=2,budget≈−3.6e−15,z=[3,5,5,5]`，policy 259 个有序历史；n=5 输出 `W=27,v=5.4,strong_gap=0,budget≈−7.1e−15,z=[3,3,3,3,3]`，policy 1555 个有序历史。两个 budget 负值都在浮点零尺度，不能解释成严格预算失败。

n=4 的非零 mask 为 10:2、32:3、40:6、51:5、59:3，查询 p 集中在动作 5；n=5 的非零 mask 为 10:3、14:4、27:1、28:6、29:6、32:4、56:2、60:2、62:2、63:1，p 在动作 3/5 上约 2/3、1/3。policy 长度分别等于六主题四人/五人的全部有序历史节点数，说明保存了完整策略映射；但策略生成仍是脚本自己的随机 tie-breaking，不是全策略枚举。

### 3. 搜索摘要与脚本重放

`optimal_budget_search_summary.json` 报告 1500 samples、seed 741、minimum_budget=0、minimum_strong_gap=0、negative_budgets=0。它没有策略树或 exact certificate，只能说明该有限搜索的统计停点。

脚本重放 n=4,m=6、20 samples、seed 131 时，iteration 0 budget=4/3，iteration 6 budget=23/9，iteration 12 budget=0，最终 best_budget=0、best_strong_gap=0。这个回放不是源历史的 1500/1000 样本重放，只是独立确认程序可执行和零预算边界。

## 与已有 aggregate-security / LAST 对象比较

- `静态安全值与聚合保底的精确核验--计算` 使用固定 36 客户、完整策略和 Fraction/独立审计；R-18 脚本使用随机质量和浮点 LP，证据层级不同。
- `固定安全预算锥的五个失败实例--障碍` 对指定安全最优查询和固定五游戏报告严格正预算余量；R-18 的 budget=0 样本属于随机实例域，不是该障碍的反例。
- `实际末前背景的聚合安全值--候选 LAST` 量化真实 m−1 前缀背景的 (mM_b\le W)；R-18 的 LP 在所有重复 n−1 背景上求静态 minimax，再沿一份随机策略累计 C。两者不能互换。
- 既有三人/四人 aggregate-theta 反例保持原 half，R-18 输出也没有 `strong_gap<0` 或 `OPT/W>2` 证据；它们只说明局部逐人/预算桥的搜索边界。

## 结论边界

五源共同支持的是有限随机搜索和预算边界记录：

1. f694 witness 的最佳字段 budget=0、strong_gap=0；
2. n=4/n=5 witness 的浮点零预算与相应 strong gap；
3. 1500 次摘要中的 negative_budgets=0；
4. 脚本在小样本重放中可执行并接受 budget=0 端点。

它们没有证明所有安全最优查询预算非负，没有证明 LAST、Q-CAG-HALF 或一般聚合安全，也没有生成完整 SPE 反例、算法/hardness 或 unrelated-machines 结论。JSON 结果均保留为 retained，脚本作为 integrated 有限工具；任何负浮点残差都必须按舍入边界处理。
