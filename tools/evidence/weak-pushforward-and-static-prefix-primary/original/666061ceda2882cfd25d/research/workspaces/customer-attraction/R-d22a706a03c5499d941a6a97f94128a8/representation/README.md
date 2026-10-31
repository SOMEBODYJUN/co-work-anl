# 表示分支：低单人收益与完整末端推送

2026-10-21。本目录为未正式入库的研究备份。一般 `Q-CAG-HALF` 仍 OPEN。

## 可复用精确事项

1. [34客户末端推送反例](terminal_pushforward_D_lt_C.md)：三人完整SPE中，任意强制根分布的平均原玩家收益 `D` 未必支付独立新进入者对完整根末端推送分布的收益 `C`。精确 `D−C=−7/120`。弱式 `C≤实际根最优收益u` 不由该例否定。
2. [34客户独立输入及完整证书](terminal_pushforward_34_D_lt_C_exact.json)。发现时先得到 [381客户证书](terminal_pushforward_D_lt_C_exact.json)，后由 root 指出的空主题机制缩小；381例只保留发现轨迹，不作为主要反例。
3. [弱末端推送与逐人半覆盖的归约](weak_pushforward_individual_reduction.md)：若全背景弱式 `C≤u` 成立，就能推出每个真实位置 `u_i≥OPT_m/(2m)`，从而一般半覆盖。这是条件性归约，不是弱式的证明。

## 探索代码与当前边界

- `search_individual_floor.py`：合法全SPE实现路径→固定全策略锥的浮点LP交替，寻找 `u_first<某m主题并集/(2m)`。首批 `p=7,m=5`、8seed×10轮最低比1/9，未到1/10。有限无反例不证明逐人floor。
- `search_terminal_pushforward.py`：固定真实后继策略锥、全部有序历史激励，攻击强式 `D≥C` 或 `--weak` 的 `u≥C`。强式反例已作独立有理化；浮点候选JSON本身不是证明。
- `pushforward_candidate_*` / `individual_candidate_*` 仅是探索候选，成熟输入只使用明确标为 `exact` 的证书及其解析说明。

下一步：继续攻 `C≤u`，并区分根背景为零与任意合法前缀背景；不要因强式失败放弃弱式，也不要把无反例数值扫描升格为证明。

## 2026-10-22 接续

- k2复制的弱推送阳性已由root发现额外查询分母缺少+1而撤销；弱 `C≤u` 仍OPEN。
- 更弱完整r槽菜单 `M_full=min_Q max_a(KQ)_a≤u` 为当前接口；Q可与查询分布独立。没有把旧仅r−1后继菜单反例套给它。
- [背景价格比较边界](meta_price_comparison_boundary.md)解析说明：即使p是内生K纯Nash，真实后继平均价格也不能代替最大价格M，且 `D−C` 对完整槽价格差不存在背景无关正系数支付。本例保留 `D≥C` 和主菜单候选。
- `entry_potential_implication_270_exact.json` 与 `high_insertion_2cycle_348_exact.json` 仅是势排序/无环路线的发现来源。root另有更强已核例，停止在这些已失败范围继续构造；两者不作为主结果。
