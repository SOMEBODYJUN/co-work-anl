# 早期机会缺口与真实菜单价格：本轮备份

主目标仍为一般 Q-CAG-HALF，全部有序历史纯 SPE 及任意平局量词保持不变。
`OPT_m-W<=m u_i`、`B(u_i)<=W` 均 OPEN；本目录没有一般正面结论或合法反例。

新增可复用内容是 [实际末位比较的局部消元障碍](actual_reply_template_obstruction.md)：
给 S/Z/V 增加每个真实末位相对实际 B 的比较后仍可精确消去联合会员，但仅三个
客户类型已排除这种逐客户强价格模板。精确分离值为 −1/32；这不是 SPE 反例。
审计见 [脚本](audit_template_obstruction.py) 与 [输出](template_obstruction_audit.json)。

其余有限探索：

- `price_search.py` / `bg_s2r2k6.json`、`bg_s6r2k7.json`、`bg_s2r3k6.json`：
  共180个完整合法背景计数策略锥；所有非零0/1查询及全目录1/t初始化后交替
  B价格LP，未发现 `B(u_first)>W−u_first`。计数策略是一种合法完整策略，
  这些锥不枚举全部策略。保存的180个候选均经Fraction逐节点审计，查询缺口最大0。
- `fullset_search.py` / `fullset_m5k7.json`：1000个五人七主题整数单位客户实例，
  以精确LCM整型收益求全部完整历史 SPE 终局集合，包含近锐大主题族的扰动。
  每终局对最小实际收益求B价格LP，未发现强价格违反；其余外层输入仍只是有限样本。
  集合缓存保存全部可实现终局，并未强制同计数历史选择同一续局。
- `all_backgrounds_search.py` / `allbg_m5k7.json`：另1000个五人七主题实例，
  同时检查每个合法前缀、每个完整 SPE 终局及每个可实现的当前动作，未发现
  背景强化 `OPT_m<=W(all)+m u_first` 的违反；完整检查数见JSON。
- `audit.py` / `audit.json`：180份保存策略的全比较Fraction核查；
  9个样本的全部计数状态、终局集合和阈值与规范 `ExactSPESolver` 交叉一致。
- `augmented_terminal_lp.py`：新增局部模板的浮点探索来源；证明不依赖它。

下一步应改变真实行或跨分支支付，不能仅增加上述 S/Z/V/H_B/L 模板的系数。
全部有限零反例记录均不升级为一般引理。
