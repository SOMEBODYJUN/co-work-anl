# 终端列生成定价：双source程序与完整浮点保存

正式正文：[双源条件分解与浮点保存](../../../state/程序/终端列生成定价的双源条件分解与浮点保存--程序.md)。本包只负责三主源，两个exact证书及一次成功共享原算法全型price由同次[737行双证书](../../../state/计算/终端系统精确最优的七百三十七行双证书--计算.md)负责，不计作本包入口执行。

- [source-manifest.json](source-manifest.json)：三个源ID、双冻结提交、大小、SHA及原字节保存位置。两个CG分别经clean show导出，逐字节同，只保一份原件。
- [original/dual_terminal_pricing.py](original/dual_terminal_pricing.py)：7245B完整原程序。
- [original/cg_dual_terminal.json](original/cg_dual_terminal.json)：779871B准确CG字节，亦为_final的原字节。
- [complete-field-projection.json](complete-field-projection.json)：全部1141原子的值池/逐项索引/附带exact_mass、全部非零质量及零恢复长度、其余完整字段；反向恢复与原JSON全部值相同。
- [read_and_check_cg.py](read_and_check_cg.py)：标准库完整阅读/有限系数核对入口。
- [complete-field-check.json](complete-field-check.json)：全部1141×20系数、字段/域检查、二十行exact binary64质量读数与执行范围。
- [dependency-manifest.json](dependency-manifest.json)：实读的继承链/行定义与成熟正文、各指纹及复用边界。

唯一新入口1启动/1成功约2.012秒，0原CLI、0LP、0QR、0全域price。所有22820个新single系数由逐槽分母/计数/排序重建，与原joint_transport四纯定义逐项同；AST只取定义，不执行原模块的顶层IO或main。这个有限核对不称完整737精确原始或dual验证。

CG原binary64质量76正1065零；保存57个正float乘子。前871原子连附带字段与成熟727原件全同、新270；106/10/21/22/48是保存结构池，非完整直方图域。67旧exact_mass仅历史字段，不能代替当前质量。

binary64质量精确读入后W−1=−22055/147573952589676412928。二十行中AB→AE2O约−2.04e−15、AE→Sbranch1O约−4.74e−16，故CG快照自身不冒称精确可行点。原十步末pricing_minimum约−1.91e−11，不改为精确0。另76有理点、57整数dual及本次父方全域检查按其独立交付解释。

式(4)的全型条件分解由解析有限纤维证明承担，当前不重跑原发现CG、不优化更小常数、不补造SPE或真实OPT、不做2.5或图登记。原737自查报告和此前父未独立接受的历史边界均保留，新的准确执行范围只由本次实际证据支持。
