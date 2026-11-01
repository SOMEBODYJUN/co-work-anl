# 相对私有块随机策略锥探针证据

[正式程序对象](../../../state/程序/相对私有块随机策略锥探针--程序.md)给定义、目标和边界。主源ebc029a8cdb5b255c1a2的[2306B原文件](original/private_block_scan.py)保留原字节；冻结来源和指纹见manifest.json。

[新增核验器](audit_bounded.py)导入原文件，顺序对原五参数域各执行reps=1。linprog只加记录包装，仍调用同一求解器；独立有理核验按完整动作表真实滚动偏离。硬编码候选输出限制在本目录run下。

~~~
PYTHONDONTWRITEBYTECODE=1 python3 archives/customer-attraction/tools/evidence/private-block-policy-probe/audit_bounded.py
~~~

[完整记录](run/bounded-audit.json)、[原函数stdout](run/stdout.txt)及[stderr](run/stderr.txt)保本次实际执行。五策略15LP成功，分母上限1000000的直接提升11份通过、四份未认证。全部17388项含自身比较中11760项属于通过的11份，四份的微小严格负差均保留。初版过强的全通过断言失败后，入口改为记录各份真实判定，未修改原源。

这是本轮有限执行与知情独立收益重算，没有跑原默认1000策略主程序，也无原历史报告可比。随机流不在域间重置，后四域种子状态不同于默认主程序。通过的点只证特定策略锥可行，未证最优值或一般half。原件、核验器及输出指纹在清单中分别记录。
