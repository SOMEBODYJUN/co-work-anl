# next_global：一般全局跨分支预算

本目录仅为本轮个人研究备份，不改变 Q-CAG-HALF 的 OPEN 状态。未修改共享数学正文、账本或注册表，未 git 提交。

当前有价值成果是 [abstract_menu_counterexample.md](abstract_menu_counterexample.md)：三人三动作的非负匿名对称精确删除边际势博弈，完整历史纯 SPE 的实际总效用 W=2，而全部实际位置真实偏离背景的聚合菜单 cap=3/4>W/3。这只排除“任意对称精确势”证明路线；构造违反客户吸引的全克隆最坏性，所以不是 CAG 或半覆盖反例。已发 Boss 并请求 tree_dual 独立核验。

- `audit_abstract_menu.py`：不导入发现脚本的 Fraction 定义级核验，覆盖全部13历史、39动作比较和精确菜单原始/对偶证书。
- `abstract_menu_lp.py`：固定形式策略及固定查询分布的广义势锥 LP 发现工具，保留完整有序历史；可选全部效用非负。随机/有限零反例不构成一般结论。
- `abstract_menu_counterexample.json`：数值发现原点，正文已独立简化为整数势，数学证明依赖正文和精确审计，不依赖该浮点文件。

下一步：检查“精确势 + u(a,H+a)≤u(a,H+b)”是否足以排除这种菜单失败；若继续发现反例，逐层加入真实CAG核必要性质。不要回到已失败的强残余桥 OPT_m(N\C)≤W，也不要回到已被Boss找到真实CAG反例的逐人末位克隆桥 u_i≥u_m/2。
