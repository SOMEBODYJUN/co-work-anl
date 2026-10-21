# 真实策略可补全与一般反例攻击

当前目标：Q-CAG-HALF，一般共同目录、单位客户、任意人数、全部完整历史纯 SPE。
本目录为 Boss10 研究员3的个人工作稿，不自动表示可靠已审结果。

- `background_near_saturation.md`：任意有背景子博弈的加权近饱和必要条件，
  含真实末位交换的全部粗化方向，以及对任意C,D有效的线性背景行(AP)。
- `CLAIMS.md`：精确量词和真实身份；v1用全体客户最大过去负载，v2按审查者
  建议改为C内最大过去负载。解析独立重建未见fatal，未外审/查新。
- `background_near_saturation_audit.py/json`及`_v2.py/json`：8个指定完整SPE
  每个有序节点的精确审计，包括非Markov平局证书。10025个定义级历史、
  55360个真实偏离；1603个k>=2节点，65345个任意C,D背景行检查。
- `background_rows_fixed_support_actual_only.json`：437旧行加前4实际节点
  400行(AP-v1)，精确可行比值约2.03952160423，仍不能推出2。
- `background_rows_fixed_support_full_v1.json`及`background_rows_fixed_support_v2.json`：
  加所有写明的固定分支/同索引真实续局背景行，共1430新增行；旧64支持上精确
  可行比值分别约2.03919799344、2.03911173825。不是SPE，也没有完整域对偶。
  对应代码`background_rows_fixed_support_v1.py`、`_v2.py`。v2常数先在整个支持
  C客户上取统一上界，未错误地逐客户列各取一个M_C。
- `ordered_policy_mutation.py`：直接突变完整有序历史策略后优化其精确锥的有限
  攻击，结果只按实际运行范围报告。

下一步：寻找跨历史的slack支付，或可满足全部续局约束的真正二以上实例。

既有437行坏点已有根饱和/同族末位off-diagonal排除，本轮不将它当SPE反例。
