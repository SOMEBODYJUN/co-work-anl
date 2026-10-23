# 完整菜单与额外一槽聚合预算研究

本目录属于 Boss9 子研究员 menu_minimax；一般 Q-CAG-HALF 仍 OPEN。

- `aggregate_extra_slot_empty_dilution.md`：新增精确边界。完整 m 槽的额外查询仍不能保证所有 p 的强聚合 `sum G_i^+<=sum D_i`；34 客户加空主题旧 SPE 给 `-epsilon+12epsilon^2`，在 epsilon=1/24 时失败 1/48。一般空主题方向展开式与具体全历史策略均写明。
- `audit_extra_slot_empty_dilution.py` 及 `.json`：独立展开单位客户核验完整 57 历史、342 非自身偏离和上述新聚合计算。父研究者另做完全独立审计。
- `audit_nonempty_extra_slot.py` 及 `.json`：盲审父研究者提出的非空加强；旧客户乘67、E新增一个私有单位客户，2279客户、全部主题非空，原完整SPE保留且强桥仍失败7/384。一般参数式表明某个稀释方向严格失败当且仅当K>66。
- `extra_slot_aggregate_probe.py`、`.json`：对开放弱候选 `sum G_i^+<=W` 的有限策略锥诊断；75 个随机真 SPE 锥再重选客户重数与 p，未击穿，最大有限数值比约0.929。不是一般证明或已审可靠界。
- `extra_slot_decorrelation_probe.py`、`.json`：相同随机锥搜索未发现强桥失败；后续定向检查旧空主题例得到上述精确反例，说明阴性有限扫描不能替代结构攻击。

当前一般候选是保留真实激励松弛的弱预算 `sum G_i^+(p)<=W`，或允许对全部 `(i,a)` 完整菜单列自由选混合以 cap 到 W/m。任何一个若成立都给 `W>=m v_(m+1)>=OPT_m/2`。尚缺真实跨位置 relay；不得只将 root 的负债交给尾两人的二阶正曲率。
