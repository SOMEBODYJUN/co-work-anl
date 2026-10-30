# 一般全局支付研究：当前状态

主目标Q-CAG-HALF仍OPEN。本目录仅为R-077c0cacfba24288be91dee1acf6d484/global_proof个人研究备份，不作共享Claim或可靠结论提升。

## 本轮内容

- `terminal_menu_projection.md`：从现行共同倒二主题证明中的同一真实菜单G，投影得到一个**无路径包含假设**的普遍收益诊断。完整解析推导已写；尚待独立审查。核心是OPT_m <= W+m u_(m-1)−u_m/2−freshA/4（m>=2）。这是原G的新投影，并非全局half证明。
- `individual_opportunity_loss_candidate.md`：精确开放候选`B4-INDIVIDUAL-OPPORTUNITY-LOSS-v0`：每个实际玩家i都满足OPT_m−W<=m u_i。末位和倒二范围由真实节点/菜单证明；一般较早i未证，父代理正在用完整策略锥独立攻击。若成立取最低收益可得主目标。
- `probe_loss_floor.py`：规范全SPE终局求解器上的小型随机**反例搜索**。1500实例，m∈{2,3,4,5}、主题数3至6；未找到违反候选。没有声称这一有限结果支持一般定理，也没有把计算当证明。随机种子9216。命令`PYTHONPATH=. python .../probe_loss_floor.py`。

- `fractional_price_endpoint.md`：将菜单比较权推广为任意非负实权，证明分数覆盖利润势B(u_A)<=W−u_B/2−freshA/4；含有限LP折扣对偶。完整解析推导已写，末两位成立，更早玩家开放。
- `probe_fractional_price.py`：1600随机小实例的分数价格势反例搜索（SciPy仅作数值发现工具），未发现违反B(min ui)<=W；不是一般证据。

## 当前边界与下一步

原末两人菜单仅解决候选的末两位。不能将同一菜单的倒二主题改为更早主题，因为其真实后继不再是一个最佳回应。
尝试更早节点的全局归纳，必须保留真实完整续局的自身最优性；固定尾深和早期粗保底不够。
除本目录外未改文件；不调用work.py，不进行git操作，不读取凭据。
