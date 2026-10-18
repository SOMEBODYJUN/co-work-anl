# 当前活跃路线：`UM-TARGET-v1`

研究存档：`unrelated-machines`。本页是短期调度合同，不是数学结论。

## 本轮只保留两条主线

| 路线 | 目标 | 角色上限 | 失败后的处理 |
| --- | --- | --- | --- |
| `P0-F` | 任意 `P,T` 的共同容量状态，实际全机输出或 sound `FAIL` | 1 Builder + 1 跨上下文 blind attacker + 1 Integrator | 一轮未减少唯一 `O` 就停；局部反例入障碍，不扩同族 |
| `R0-R` | 固定严格次二比例的真实整数 gap、完整 YES/NO 保持和低调度 decoder | 1 Builder + 1 跨上下文 blind attacker + 1 Integrator | 中间层逃逸或 decoder 缺失即退为障碍，不继续堆参数 |

其他工作只能作为这两条路线的支援、文献/复杂度核验或暂存探索。相同 `O` 加相同机制只能有一张活跃卡；没有 Route Card 的工作不能新建 canonical 变体。

## 每轮节奏

1. Builder 和 blind attacker 先各自写 Route Card 的字段；attacker 在读证明前独立攻击。
2. Builder 交付一个引理、decoder、实际输出、sound 失败证书或最小反例。
3. Integrator 只回答唯一 `O` 是否减少，并登记 `closes / partial / blocked / salvage / retire`。
4. 连续两轮没有减少 `O`，路线必须停止、回收或换机制。增加样本、改参数、增加文件和结构检查本身不算减少 `O`。

探索不需要审批；承重结论、路线合并和 Claim 晋级需要 blind attack 记录。这里的 attack 是独立信息源，不是投票或许可门槛。
