# round11/geometry：最优 fresh 查询候选

2026-10-25。任意人数、任意共同有限目录、每个完整历史纯 SPE。
HALF 与承重候选均 OPEN；没有新的全树金额付款。

- `optimal_fresh_self_reserve_working.md`：最优比较元组最小 fresh 费用候选
  K0<=W+R0，HALF 充分性、正确静态余项、旧前缀负载关系去重、五人压力和缺口。
- `audit_optimal_fresh_self_reserve.py` / `.json`：十六个旧根输入的精确候选反例检验；
  不重新认证来源 SPE，无反例不作一般证明。
- `attack_optimal_fresh_policy_cones.py` / `.json`：四份旧完整策略、六十五个严格唯一最优支持的
  有界浮点反例攻击，无负分离；没有精确 LP 证书或一般性结论。
- `matching_displacement_gate_review.md`：matching11 零净覆盖损失块替换门的独立核验，
  确认复制退款和最大退款方向；尚无定量付款或新颖性声明。
- `shared_saddle_geometry_checkpoint.md`：共享 minimax saddle 的等价格 Gram 向量化，
  真正非负 KKT 松弛与残余协方差，及只需 gamma/2 误差的 HALF-SLOT 开放付款目标。
  没有新金额付款；五人所需 W>=9gamma/2 仍未证。

接续优先：证明或攻击真正最优覆盖下的 K0<=W+R0；不恢复已失败的任意单 query 加强。
