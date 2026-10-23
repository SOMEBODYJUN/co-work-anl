# Boss6：同时改变全部可信子树的有限工具与价格机制边界

2026-10-22。个人探索资产，主目标 Q-CAG-HALF 仍 OPEN。没有一般早期价格、
逐人弱 floor 或半覆盖的新证明，也没有对应真反例。停止增加阴性 seed/规模。
本目录由 root 统一保存，不自行 git、公屏或更新共享结论。

## 可接续资产

| 文件 | 准确内容和用途 |
| --- | --- |
| [full_tree_milp.py](full_tree_milp.py) | 固定 p,m、根计数 q 与根行动 a，**同时选择每个有序历史的行动及真实终局**。数学可行投影是全部完整纯 SPE 策略锥的并，非单一策略锥。浮点 MILP 仅提候选。 |
| [full_tree_milp_contract.md](full_tree_milp_contract.md) | 选择变量、真实子树一致性、合法 big-M 与完整性证明；可用于独立攻击实现合同。未经过独立同行代码审查。 |
| [audit_full_tree_milp.py](audit_full_tree_milp.py)、[审计输出](full_tree_milp_audit.json) | p=2,m=2/3，根行动固定0时分别穷尽4/64个**完整有序策略图**，逐固定锥 LP 与 MIP 对比。含非零方向的正负极值，避免只用零 sharp 目标的无区分力核验。全部通过；不是一般数学证书。 |
| [protected_excess_price_boundary.md](protected_excess_price_boundary.md) | 对 Boss5 已有71客户/全 k 族的精确价格推论：保护遗漏价格 B_D(u_A)=2k−2，而尾部超额利润仅 k。明确击破旧 PROTECTED-SHARP 及其全人数推广，不声称新底层反例。 |
| [protected_price_boundary.py](protected_price_boundary.py)、[精确输出](protected_price_boundary.json) | 无 optimizer 的显式原始/对偶匹配；canonical 验证全部有序历史，canonical solver 检查根可实现。通式证明在正文；4个 k 回归只核对实现。 |

## 已实际发生的 MILP 探索

- `small_model_check.json`：最早 p2m2 冒烟检查，后由上表全集审计取代。
- `m3p4_alltree_price_plus_u.json`：根计数(1,0,0,2)、首行动0，完整30查询，
  完整策略并。浮点最优约1e−6，所选锥精确回收 gap=0、物理目录只有1主题；
  不接受为反例，不认证浮点上界。
- `m4p5_alltree_tstar.json`：根(1,2,1,0,0)、首行动0、完整260查询，50秒超时，
  浮点上界1、候选0，完全无一般/有限不可能性结论。
- `m3p6_alltree_weakfloor.json`：根(1,1,1,0,0,0)、首行动0，全部至多3主题的
  比较组合，50秒超时，浮点上界1、候选0，无结论。
- 两份 `*_hull_distinct.json` 加首子树单纯形分解与每对主题归一差异至少.001。
  仍超时。m4p5甚至没有可用 incumbent。m3p6的旧候选回收步骤当时没有保留
  距离 cut，故报告候选退化成2个物理主题；该候选从未接受为反例，且当前代码
  已将距离 cut 纳入所选锥回收 LP。**不把旧回收候选当作满足距离约束的点。**

所有输出均为已发生的浮点提案记录，不能把“同时选择所有完整策略”的理论
模型覆盖范围与“某次超时求解得到一般界”混同。min-distance>0只给候选发现
限制，不能覆盖所有物理两两不同、但差异可任意小的目录。

## 已纠正的机制与下一步

末位 `B(u_m)+u_m<=W` 及 `W>=max|T|` 都是既有结果，不重新登记为新定理。
`u_i>=u_m` 时可以继承强价格预算；`tau<=1` 的查询也没有早期价格反例，
只作为搜索筛选备注。来源包括
`R-e5d83af532dc495c966f99cf70cda2a2/parent_tail/penultimate_price_defect.md`。

曾考虑全人数保护价格 `B_D(u_i)<=sum_(j>i)(u_j-u_i)_+`，它会把整个最优遗漏
都支付给 W，已被上表既有二人族否定。不能靠更有利的最优组合交换修补，因为
其最优组合唯一。下一步须保留 `G=|actual\OPT|`，比较真正净缺口
`|OPT\actual|-G=OPT-W`；不能继续只给全部遗漏寻找支付。

一个准确但**未证明、未实验**的较弱接口是

    B(u_i) <= W + sum_(j>i)(u_j-u_i)_+ .

若只对实际全局最小收益玩家 i 成立，则取 m 个最优主题权一，有
`OPT <= W+m u_i+sum_(j>i)(u_j-u_i) <= 2W`。它允许真实后继保留超额利润，
严格弱于先前一般 `B(u_i)<=W` 候选；不是已经找到递推机制，也不改变 OPEN。
后续实验若有必要，应判别保留 G 的此接口与单纯保护遗漏接口，不能再扩大同类
固定根规模、同策略锥或 seed 的阴性扫描。
