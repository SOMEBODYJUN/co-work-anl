# 同索引末回复必要行的有理审计

[正式正文](../../../state/程序/同索引末回复必要行的有理审计程序--程序.md)合并两个主源：1516B原程序9c091035a7d908e9877f及480B原报告09c28210901715b44312。它们从38个冻结原子的旧坐标计算五条同索引末位IC之和，结果严格负；排除的是保持旧投影并把命名回复解释为真实最佳回复的完整SPE补全，不是共同集合本身不能实现，也不排重新优化的点。

## 文件与来源

- [original/audit_diagonal_menu.py](original/audit_diagonal_menu.py)：未改原程序。
- [original/audit_diagonal_menu.json](original/audit_diagonal_menu.json)：全部七字段的冻结报告。
- [source-manifest.json](source-manifest.json)：两主源、实际输入与两份相关原稿的库存ID／两冻结提交／SHA／blob及持久路径。
- [review-record.json](review-record.json)：全文件实读、关键推导、全仓比较、各事件范围和后续使用边界。
- [check_package.py](check_package.py)、[self-check.json](self-check.json)：只检查指纹、结构、原报告字节相同和链接；不运行主程序、重新计算38项、求解LP或SPE。

实际输入只需[34584B增强2396原子表](../R486-same-query-clique-20261101/enhanced_2396_exact_obstruction.json)，SHA ce1f9d8b1036256b7e40e1eb5c990fdcc4f33c7fed3f2aa796bdf8245b9d0c4f。源码没有本地Python依赖，只用标准库。程序完整读取JSON，数值只访问atom_masses的bits、menus_lh、mass；不能用37份旧mass_numerator替换当前mass。

## 当前唯一原入口

[run_original_once.py](run_original_once.py)先核三份输入身份，再按兄弟目录 round3_independent／next_credible 物化不变代码及数据，以普通CLI运行一次；无profile／trace／runpy或函数替换。脚本只是复现与记录外壳，未重写数学行。使用其source、input、expected、work四参数；work应是全新clone外目录，存在execution.json即拒绝意外重复。此处保留脚本供接续审计，已经成功的本点无需再跑。

[execution.json](replay/execution.json)记录真实argv、时间、Python版本、前后SHA与执行范围；[报告](replay/audit_diagonal_menu.json)、[stdout](replay/stdout.txt)、[stderr](replay/stderr.txt)保真实字节。一次main耗时0.03366020799148828秒，exit0；生成报告与stdout各480B且逐字等于冻结报告，stderr空。数学passes_necessary_inequality为false。两主源与实际输入无改动。0 LP、0随机／SPE搜索、0旧2396或1326全表、0新的独立38项实现。

## 复用而不重复的证据

原[独立读取与负行记录](../global-indexed-reviews-boss3/input-and-exclusion-review.json)已有38项系数、mass、加权值，以及53根直方图投影保持38质量的检查。其[实现](../global-indexed-reviews-boss3/read_inputs_and_exclusion.py)与[事件](../global-indexed-reviews-boss3/input-review-event.json)属于此前另一次独立实现；本包只实读和对照保存值，没有再次执行。

负值为 −33962942532321286037391724417608677893／2370629578513027021549656484975223155224。式子仅依保留的旧坐标，因此原2396必要行通过、53细分的1326新行严格通过、最终仍不能补成完整SPE可以同时成立。此前3367B兼容会员配对审计与当前1516B单行脚本也须分开；当前程序没有枚举所有会员配对。

完整数学、输入12字段／原子7类字段、输出7字段、接口异常、任意重复与平局、保投影排除量词及相关对象连接均在正式正文。逐主源回执在Boss7第21批工作区；本包不自行操作Git、claim或done。
