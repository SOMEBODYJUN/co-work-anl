# Boss10 反例攻击子工作区

目标：独立攻击一般 Q-CAG-HALF 的真值与可扩展可信惩罚机制。主目标仍 OPEN。

- `reciprocal_isolation_barrier.md`：双向隔离、单末位 Q/B 切换架构的解析必要障碍。
  任意 `k≥1` 的最坏比例至多 `(3k+2)/(2k+2)`，既有 3/2 族达到。
  精确身份 `B10-RECIPROCAL-ISOLATION-SHARP-v1`；发现者、root 与独立研究员已重构。
  独立报告在 `../independent_no_go/reciprocal_isolation_review.md`；不是一般上界，
  未宣称外审或新颖性。
- `breaking_isolation_notes.md`：未完成的升级构造与精确缺口预算。
  在保留单末位实际路径的局部池架构中，half 反例必须累计
  `E>(k+2)|D|/3` 的跨分支收益差或末位奖励稀释；不是充分条件。
  多次重复惩罚主题被真实末位可改 `D` 的比较阻断。
- `two_copy_pushforward_correction.md`：明确撤销两副本弱推送阳性；额外查询必须对
  完整终局再加一位分母，正确 `C=359/120<13/4`。仅保留有限 BI 可实现记录。
- `pure_full_root_menu_obstruction.md`：八玩家八主题三十二客户的完整 SPE，
  每个真实完整根列都存在额外查询 `37/10>u=13/4`，否定纯菜单阻断。
  混合值恰 `851/280<13/4`；混合阻断、弱 `C≤u`、half 均不由此否定。
  发现者/root/独立研究员均已重构；root 全 DAG 与矩阵独立证书在 `../parent/`。
- `pure_menu_two_block_dag.json`、`verify_pure_menu_dag.py` 与
  `pure_menu_two_block_audit.json`：13,872 状态完整策略 DAG、独立于规范包的单位客户
  直接核验和冻结结果；`build_pure_menu_dag.py` 仅用于发现/重建。
- `pure_menu_cone_probe.py` 及 `pure_menu_cones_*.json`：固定完整策略锥的数值探索，
  以二元变量给每个根列选坏查询；不承担一般命题的证明。

下一步：让早选与末选惩罚主题经历不同负载，攻击额外追随者、跨组主题或被预先
稀释的末位奖励。所有候选必须补全全部离轨历史，并核验惩罚者自己的真实最优性。
