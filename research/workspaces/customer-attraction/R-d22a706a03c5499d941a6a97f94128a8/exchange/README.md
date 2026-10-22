# Boss10：最优覆盖交换与客户级预算

本目录是 Q-CAG-HALF 的个人研究备份；只使用有限单位客户、共同主题目录、全部有序历史纯 SPE。
主目标仍 OPEN。

## 已完成

- `unique_optimum_omission_obstruction.md`：71 客户、2 人、6 主题的完整 SPE；实际 W=35，唯一最优主题集合 {T,Q} 覆盖 38，却遗漏实际覆盖外 36 客户。否定“存在某个最优组合，其遗漏数不超过 W”的直接支付，也否定最大化实际交集的最优组合修补。不是 half 反例。
- `audit_unique_optimum_omission.py`：不依赖求解器或规范 SPE 实现，展开 71 位单位客户并用 Fraction 核验全部 42 个节点行动比较、21 个无序主题对和连续价格解析界。
- `unique_optimum_omission_audit.json`：上述审计的冻结输出。

## 当前状态与下一步

发现者已按定义完整核验。父研究者已按原始类型和规则独立展开，不读取本审计代码；其独立审计见 `../parent/audit_optimal_omission.py` 与 `../parent/optimal_omission_independent_audit.json`。尚无外审或新颖性认证。
唯一最优遗漏支付失败不影响 OPT−W<=m u_i 一类保留完整最优覆盖的动态预算。
继续攻一般真实跨分支机制及允许局部欠债的整体支付。
