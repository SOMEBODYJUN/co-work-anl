# round5 security：实际末菜单比较、精确助手反例及独立审查

2026-10-24。对象始终是Q-CAG-HALF的任意人数、任意有限共同目录、每份完整有序历史纯SPE。**主目标及真正强/弱安全值聚合保持OPEN。本轮没有新的福利因子，没有原目标反例。**

## 已完成的核心资产

- [全局零根逐人floor真实反族](global_extra_individual_counterfamily.md)：m个经济单位客户、m−1个两客户银行，完整Cartesian目录与显式BASE/PUNISH/EXIT控制器。标准根逐人δ_m对m≥3失败、全局额外δ_(m+1)逐人floor对m≥4失败、更弱的`u_i≥OPT_m/(2m)`对m≥5失败。已获 [direct独立全m解析与单位展开审查](../direct/review_global_extra_individual_counterfamily.md)，m3/m4全部历史IC通过；原half与聚合δ/v均保持并在本族直接付款。
- [全局extra逐人缺口的通用别名转移](global_extra_fractional_alias_transfer.md)：只用原generic整数条件`L>Pm/ε`给实际反族的fresh私有别名corollary，不优化别名常数或另开结构任务。

- [实际末菜单精确比较](refined_actual_last_comparator.md)：从既有静态覆盖税及末位真实BR推出全部原输入有效的`OPT_m≤mL+W−u_m/2`，其中`L=v_2(实际前m−1位背景)`。root已独立核对，另通过 [capacity独立审查](../capacity/refined_last_comparator_review.md)。已识别的完整税余量也给出精确式。它是旧代数的新组合接点，不是half证明或新颖性声明。
- [全列税助手失败](last_menu_retained_tax_failure.md)：对construction的真实P填充23客户SPE族，独立计算全部Q的联合菜单/税最优值。唯一最优Q仍为纯主题2；`min_Q[mM_Q+τ+Et]−2W=(2k²−41k−33)/(2(k+1))>0` 对k≥22。因此强LAST、弱LAST乃至全列保留精确税的充分助手均失败。[capacity已独立核对](../capacity/padded_core_controller_review.md)一行全Q证书。完整SPE属性继承 [construction控制器定理](../construction/padded_core_last_budget_counterexample.md)（全部k≥1），不由本分支静态检查替代。
- 同族的真正静态竞争列`(2,3,4),P^(k−1)`给`v_m≤5`，故`δ_m≤v_m≤5`且`W−mv_m≥8`。这明确隔离助手失败与真正安全值桥。`audit_retained_tax_raw_core.py` / `retained_tax_raw_core_audit.json` 只核原始23单位客户的静态矩阵、税向量、全Q证书和k=22精确边界，不扫描、不构造SPE。
- [私有别名一般转移的独立审查](independent_review_private_alias_transfer.md)：独立审查menu全输入编译器并通过。每个旧完整SPE可lift到fresh私有别名SPE，收益逐人加P；真正δ稳定误差≤P(m−1)/L，故任意真实强聚合δ缺口可在L够大时保留。没有缺口种子，弱桥/ADM不能照搬；不是一般half证明。

## 辅助推导与诊断（不作一般推进）

- [弱LAST根修复精确成本](weak_last_root_repair_cost.md)：minimax乘积可加，既有保险对`mL−W−u_m/2`的精确成本为`(11m−3)s/[2(3m−1)]`；construction独立匹配并扩展多角色版本。只是转移工具，未给种子。后续真实助手反例不依赖该工具。
- [regular填充真正δ证书](regular_padding_fractional_certificate.md)：给menu构造攻击的解析证书；没有符合分离门槛的SPE witness，不另开受限目录正面项目。
- `audit_thirteen_last_menu.py` / `thirteen_last_menu_exact.json`：按root指定检查旧13人税反例，精确L=7/3，原各人都≥L。实际主题支持的列无法cap未覆盖T到弱预算；只作既有输入诊断，不生产正面结果。
- `probe_last_actual_menu.py`、`probe_individual_last_root_floor.py`及JSON：对两个精确全称候选各做一次固定旧形式策略/固定有来源查询的数值锥攻击，未发现反例。没有精确全锥对偶或一般证据；随后真实23核已反驳根逐人LAST，P填充反驳聚合助手。不继续扩展这些诊断。

## 同一一般推导的m=5压力

新的真实反族m=5给`u_1=5/4<δ_6=25/18`（差5/36），且`u_1<OPT_5/10=13/10`（差1/20）；同时`W=10,OPT_5=13`，原half没有失败。这是同一全m控制器的代入，不是五人专项。

无条件正确关系仍是`OPT_5≤5L+W−u_5/2`。若一般弱付款成立，本可推出half；现已知道该全人数付款为假。P填充完整SPE的全税反例用于更大m，并没有给m=5助手反例，也没有证明m=5的一般付款。不得把失效助手或某个五人代入当作原五人命题的真值。

menu别名转移对m=5的误差是20P/L，只有先有真实强聚合δ缺口才可保留。本轮没有这种缺口。所有结论的量词、继承证明和内部审查范围分别记在正文中。
