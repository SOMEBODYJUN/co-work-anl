# 全局证明工作区：本轮可接续记录

主目标Q-CAG-HALF仍OPEN。全部对象均为共同目录、单位客户、单位提供者、完整历史纯SPE；不得把辅助桥反例当作half反例。

主要新增资产：

- `collision_free_three_halves_family.md`：任意k的完整Q/B递归SPE构造，实际全部C_i+D无拥挤，W=2k+2、OPT=3k+2，比趋3/2；迫使所有声称支配OPT的纯负载函数f满足f(1)≥3/2。root与independent_mechanism均独立重构归纳。`audit_collision_free_family.py`及冻结`collision_free_family_audit.json`对k1,2,3的全部有序历史作Fraction重放（20、399、11110项比较）。趋2构造仍OPEN。

- `collision_free_occupancy_obstruction.md`：五客户、两人、四主题完整SPE的自足反例，实际无拥挤仍有W4<OPT5。它同时击穿普通调和势、截断调和势、二层占用量以及任意f0=0,f1=1的纯占用函数支配OPT。`audit_collision_free_obstruction.py`和冻结`collision_free_obstruction_audit.json`给定义级精确核验。
- `harmonic_potential_obstruction.md`：本轮先得到的十一客户三人调和势桥反例，W8、OPT11、Φ=21/2；原稿与冻结记录保留。root已独立核验。它被上面的更强五客户例替代为主要障碍，但没有原位删除。
- `two_layer_occupancy_probe.py`、`two_layer_occupancy_candidate.json`、`two_layer_occupancy_audit.json`：九客户三人发现中间点与精确重放，是五客户例来源。
- `background_regret_probe.py`：固定完整Markov策略的背景整体候选LP攻击。候选为任意合法背景b、r人完整SPE满足P+新增覆盖Δ≥freshOPT_r。q6r3完成100棵，每棵至多12个比较主题；q7r5运行被主动停止，最后输出确认至少完成600棵，每棵至多12比较。均未找到负点，只是有限浮点LP筛查，不能提高候选真值。
- `truncated_potential_probe.py`、`truncated_potential_candidate.json`、`truncated_potential_audit.json`：原78客户发现点。`minimize_harmonic_obstruction.py`、`harmonic_obstruction_minimized.json`、`harmonic_minimized_audit.json`：固定策略整数压缩为十一客户点。发现求解器不参与反例有效性证明。

剩余数学义务：

1. 原Q-CAG-HALF一般证明没有闭合。本轮只排除更强的实际负载势一次支付；离轨拥挤是必须保留的机制。
2. 背景P+Δ整体候选仍OPEN。另一队员`../background_induction/`已给其简单零slack首步归纳的精确反例：需要尾部surplus支付负的首步差，不能只引用tail候选≥0。该首步失败不否定整体候选。
3. 如继续负载势路线，新无限族迫使f(1)≥3/2；即使这个必要条件成立，也没有证书存在证明。更直接方向是跨真实后继的拥挤转移、尾部surplus或全树非负行锥支付。

本工作区未自行git提交或发外部消息，由root统一保存。有限扫描没有后台进程仍在运行。

额外低预算无拥挤趋2探索：`collision_free_ratio_probe.py`对q6m3随机完整Markov策略500棵施加实际load≤1，最高浮点候选约1.116279，未改善已证5/4；不构成上界。`joint_collision_free_probe.py`对m3q6完整有序历史联合MILP按比较主题与实际交集k=0,1,2各15秒，均只提出比1；超时和浮点优化状态不作数学证据。结果记录于`joint_collision_free_m3p6.json`和`joint_collision_free_m3p6_k1.json`。没有继续扩大m4计算，因为已转入有解析证明的趋3/2族。

最后新增失败记录：`promoted_punishment_family_failure.md`把t−1个共享围堵主题的直接推广精确排除。有限oracle仅运行t3k1、t3k2、t4k1三点（均目标不在结果集）；随后找到一般末位偏离：末位Ci可改Ai得2t−1，末位Dr可改Ai得3t/2−1，均在t>2时超过实际t。故该指定终局所有k均失败，但其他无拥挤趋2路线仍OPEN。复算代码`probe_promoted_family_failure.py`只保存已运行三点的命令，不再扩大计算。

最终数学边界：本分支得到真实一般辅助族（无拥挤比趋3/2）与精确失败机制，没有一般half证明或反例。最高价值待证义务仍是所有完整历史的跨真实分支全局覆盖支付；新子问题是无拥挤SPE的最坏覆盖比能否超过3/2并趋2。背景P+Δ整体候选保持OPEN，但本分支的600棵有限无反例扫描信息量已经降低，不应继续据此堆样本替代证明。全部计算已结束，无后台写入。
