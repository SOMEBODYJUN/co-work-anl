# Boss3：可信构造与抢先选择分支交接

日期：2026-10-23。仅本目录；没有 git、公屏、凭据操作或继续扫描。
一般 `Q-CAG-HALF`、最小收益候选 MG 以及父分支 ROW 均仍 OPEN。

**最终追加的 ROW 定向判别已完成。** 同一根税/69 客户完整策略锥内，全部126个
最优四元多重组合 J、全部实际位置，被252个精确原始/对偶对覆盖；没有正点。
最大标准化 ROW 违反量为 −1/4（W=1）。详见 `row_attack.md`、`row_attack.py`、
`row_attack.json`。这是一个固定策略锥的结论，不是一般 ROW 证明。

## 本轮实质结果

1. **携 floor 储备递归台阶的完整 SPE 反例。**
   身份 `CC-CARRIED-FLOOR-RECURSIVE-STEP-NO-v1`，自足正文为
   [recursive_step_counterexample.md](recursive_step_counterexample.md)。
   四人、六主题、69 个不同单位客户；实际 AAAF，收益 (10,10,10,18)，W=48。
   在 b=0,r=4，F_4=69、h_4=15/2、F_3(A)=41、h_3(A)=15/2，候选右端为
   max(60,20+max(41,45))=65，因此严格差为 4。半覆盖余量 2W−OPT=27。
   仅优化根税实例的**一个完整策略锥、一个指定最优支持**即找到，随后停止攻击。
   数学证明是正文的客户表、全历史闭式策略与 SPE 比较，不依赖浮点 LP 最优性。
   父研究员标量独立重构及递归候选作者全单位客户审计通过；无外审/新颖性认证。

2. **公共奖池多尾部模板的普遍 3/2 障碍。**
   身份 `CC-COMMON-REWARD-PREEMPTION-v1`，正文为
   [common_reward_preemption_obstruction.md](common_reward_preemption_obstruction.md)。
   实际 C_1,…,C_k,D^r，C_i=X_i，A_i=X_i∪Y_i，B_i=X_i∪P，D=P，
   各 |X_i|=b、|Y_i|=a、|P|=t。最后一个 C_k 抢先选择 B_k 在任何后继下至少得
   (b+t)/(r+1)，故 t≤rb；实际末位比较 A_i 给 t/r≥b/2+a。因而 a≤b/2。
   目录恰为模板时 OPT/W≤3/2，对任意 k,r 成立。离轨后继如何改变都无法修复该
   实际路径；需改变实际路径或奖池/主题结构。父研究员独立重构 j=k 推导通过。

## 反例复核文件

| 文件 | 精确用途 |
| --- | --- |
| `recursive_step_attack.json` | 69 客户重数、全部259个历史的完整策略、标量值、LP来源与可选精确对偶 |
| `verify_recursive_step_counterexample.py` | 不导入规范模型/solver/LP，显式展开单位客户，逐历史逐偏离重算；同时核对闭式策略与保存的完整策略完全一致 |
| `recursive_step_counterexample_verification.json` | 本次实际运行：259历史、1295偏离、67平局、零违反；F/h及严格差全部精确 |
| `attack_recursive_step.py` | 一次定向锥攻击，可重放发现；所有 Γ、O 最优、各 max 分支均保留；浮点仅生成候选 |

运行独立检查：

```bash
python research/workspaces/customer-attraction/R-b6d636d360e14c11aeb4b76415ed422b/credible_construction/verify_recursive_step_counterexample.py
```

## 最小收益候选扫描的准确边界

候选 MG 是 OPT−W≤m min_i u_i，等价于对所有实际 i 的 OPT−W≤m u_i。
它若成立足以推出 half，但本轮未证明或否定。末位版本可由最佳回复直接证明，
正文已列；不能把该证明借给早期玩家。

`attack_minimum_gap.py` 仅对已保存的 73 棵完整策略做该明确候选的锥优化：
3 棵来自根税、34 客户逐人安全失败、8 客户 CCE 失败；另70棵是仓库既有
m4p5 策略样本。共918个 (锥,比较支持,实际占用主题) 目标，未发现正违反点。
其中71棵的全部目标恢复精确非负对偶，所有已核对上界≤−1/4（W=1）；另两棵
分别有一个目标未恢复精确对偶，不能宣称那两棵的全锥结论。
来源与各精确对偶位于 `minimum_gap_scan.json`。它不覆盖其余策略，不能提升一般 MG。

`attack_minimum_gap_joint.py` 另对三人四主题的两个实际路径和两个比较支持做了
四次明确候选攻击；浮点 MILP 仅生成四棵完整策略，再按有理锥检查。
`minimum_gap_joint.json` 保存全部生成策略及相应检查；无正点同样不是一般证明。
到收到新递归台阶任务后已停止该路线，没有继续扩大人数/目录扫描。

## 下一步区分

- 递归台阶已被严格否定；若继续归纳，需要新增状态或分支预算，不能仅重调本台阶参数。
- 若尝试把3/2无拥挤机制升级，要先越过末个 C_k 的公共奖池抢先选择义务。
- 一般 MG/ROW、真正聚合安全值以及 half 都没有被本目录的辅助反例判定。
