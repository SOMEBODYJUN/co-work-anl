# 可信续局安全值桥：独立内部审查记录

日期：2026-10-10。对象为 `research/current/customer_attraction/continuation_security_barriers.md`。
这是内部独立审查；没有外部同行评审或世界新颖性认证。

- 一后继去相关恒等式：独立重构 `U_d=F_d−G_d`，对两个iid主题的最后节点BR slacks求均值，
  `F_d(B(A))`项相消，正好得到文中Eq(1)。检查了minimax方向和固定前缀的竞争者量词。
- 上传四人反例：另一个计算不导入新audit、规范model或solver，直接读取已有4095项整数
  weights及有序policy，用Fraction得到矩阵
  `[[6135342,6135349],[6135349,6135345]]`、差`−11/4`、实际根路径`(8,4,5,0)`和收益6135345；
  并独立算出所示自由菜单Q的全部十二行，cap为6135345。另核96项一后继membership身份。
- 三人真实根菜单反例：独立审读并运行unit-customer audit，43有序节点258比较、全部两列值、
  任意λ的两行之和22、半半Q达到11、完整安全值v3=10的原始和对偶证书均正确。
  Stationary核有两个零入列，四个剩余平衡方程确定唯一1/4分布，推送cap仍11。
- 每个n≥3的完整编译族：逐式复核fresh辅助SPE（根0、全部非根1）、M2的全部历史扩展量词、
  统一偏置Kb、真实根菜单仅两列、两个未用标签行强制cap≥Kb+1/2。
  old查询上界`K(b−1/2)+M=Kb−M−1/2`正确，半半Q达到精确菜单值。
  扩大为2n个纯组尾列的对偶均值上界也正确，给该族v_n≤u1。

精确实现报告：

- `customer_attraction_decorrelation_boundary.json`：1885节点、22620行动比较及去相关矩阵。
- `customer_attraction_root_tail_menu.json`：36客户完整SPE和n=3,4,5,6的正编译菜单算术。

大n回归不枚举完整策略树，全部历史SPE存在依赖文中的辅助策略证明和既有M2普遍编译定理。
以上结论排除(D)和(M)两条指定桥；不判定一般逐人`u_i≥v_n`、总桥`W≥nv_n`或半覆盖。
审查没有发现致命问题。
