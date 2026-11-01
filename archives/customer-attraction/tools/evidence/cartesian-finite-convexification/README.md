# 四主题凸化记录与双副本有限编译证据

本包保存4004B `cartesian_finite.py`、2751B浮点种子和49825B完整有限证书，三者原字节分别位于[original](original/cartesian_finite.py)。数学分为[程序对象](../../../state/程序/双副本笛卡尔可信菜单的完整策略编译程序--程序.md)与[计算对象](../../../state/计算/四主题笛卡尔根门槛的凸化记录与双副本证书--计算.md)。

有限程序只读种子的`analysis.k/weights`，重新以Fraction计算完整两副本菜单和273节点策略；它不消费小数混合/安全值。浮点种子则有独立历史生成边界：当前`cartesian_limit.py`的main不写`sample/drop/analysis`外壳，不补造其历史argv或seed。

| 文件 | 身份与范围 |
|---|---|
| [original/cartesian_finite.py](original/cartesian_finite.py) | 4004B冻结标准库程序 |
| [original/cartesian_convexification_k4.json](original/cartesian_convexification_k4.json) | 2751B冻结数值记录，3个顶层/18个analysis字段 |
| [original/cartesian_two_copy_exact.json](original/cartesian_two_copy_exact.json) | 49825B冻结精确packet，18顶层字段、144单位客户、273动作 |
| [run_original_once.py](run_original_once.py) | 本轮实际运行的一次性隔离CLI驱动，不修改原函数 |
| [replay/execution.json](replay/execution.json) | 唯一原CLI的argv、两输入前后SHA、预期/生成报告SHA与退出状态 |
| [replay/cartesian_two_copy_exact.json](replay/cartesian_two_copy_exact.json) | 该次实际生成的49825B报告，与冻结逐字同 |
| [replay/stdout.txt](replay/stdout.txt)、[replay/stderr.txt](replay/stderr.txt) | 原摘要648B、stderr0B；摘要省略完整game/policy/weights |
| [audit_reported_data.py](audit_reported_data.py) | 使用已有64条精确收益表的一次字面小数回代和动作映射比较；有防重复执行保护 |
| [reported-data-audit.json](reported-data-audit.json) | 4根混合/3实际混合、全部10静态背景/4查询的字面值，273动作全同 |
| [reported-data-execution.json](reported-data-execution.json) | 唯一轻量数据算术事件，0新收益表/0LP/0IC/0BI |
| [source-manifest.json](source-manifest.json)、[review-record.json](review-record.json) | 完整来源字节、读取与成熟证据复用界限 |
| [check_package.py](check_package.py)、[self-check.json](self-check.json) | 只核字节、JSON结构、已有结果和链接，不执行原数学 |

唯一原CLI在2026-11-01运行，Python 3.12.14，assert开启，exit0、0.5899072980100755秒。没有profile/trace、函数替换、额外原调用或LP。原程序完成4368含自身/4095非自身有理IC，生成策略的实际路径11/14/15、支付146/3/146/3/110/3、W134。完整原报告SHA为`e9a781adc3e16b788c1a18942290287fcf82fc5014afe8e1a12356629b1b2f91`。

已成熟[独立定义核验](../security-cartesian-and-disjoint-primary/README.md)原本缺作者程序/JSON，从数学稿另构造策略，做四个小精确LP、4368IC及4096终局OPT。这里不重跑它。新数据对照确认其已存273动作与作者动作全部相同，但旧事件仍是当时自建策略、原作者入口0；不改写执行历史。

新小数回代约0.016096834秒。按十进制字面而非二进制float或限分母恢复，种子概率质量有微偏，实际第二人盈余为−41/10^17；本包没有悄悄归一化、恢复静态v精确值或将数值分布认证为有限SPE。有限程序的成功只使用72名整数基客户。

结果严格分开：G1=161/6，凸化g=55/3，有限G2=271/6；保存策略的实际根146/3并非G2。代码遍历完整可实现终局并选最小W，结合菜单充要定理可得本固定实例的纯SPE最小W134；OPT144、half余量124、强聚合安全余量至少24。没有一般half或强安全反例。

事件脚本保原工作路径，不为移动文件改写旧argv；一次性CLI驱动会拒绝复用现有runtime。封包检查可用`python3 -I -B archives/customer-attraction/tools/evidence/cartesian-finite-convexification/check_package.py`，只读现存结果后写本包self-check，不导入原源码或求解器。相关数值limit与cone源只链接其各自保留的原件，不重复跑其主入口。
