# 真实末菜单与在轨保底的两种系数合成程序

主对象：[完整程序与数学合同](../../../state/程序/真实末菜单与在轨保底的两种系数合成程序--程序.md)。两份原源逐字节保留于[汇总代码](original/menu_synthesis.py)与[有序代码](original/prefix_menu_synthesis.py)，完整来源、blob、SHA及实读比较绑定见[source-manifest.json](source-manifest.json)。

原代码不保存报告，仅print。历史同目录README只记四人浮点约1.9264902135、五人未闭合，没有给执行身份或精确证书。本包的四人结果来自下列新事件，不冒充历史完整重放。

|资产|真实职责|
|---|---|
|[run_observed.py](run_observed.py)|透明载入未改原码，各调用solve(4)一次；仅在原函数return事件读取局部变量|
|[replay/execution.json](replay/execution.json)|两次原函数、2 LP、0原main；源前后SHA和环境；非默认16 LP扫描|
|[capture.json](replay/capture.json)|全部700列、13600个收益系数、A/w/o/目标、两个完整OptimizeResult和边际；620919字节，SHA8c50285a1e9fccf61ef0a6e9574230f551b35a96e7cd6089fcfea150b8535ecd|
|[汇总stdout](replay/aggregate-stdout.txt)、[有序stdout](replay/prefix-stdout.txt)|原print字节；分别另保空stderr；不是独立证书|
|[audit_exact.py](audit_exact.py)|独立标准库Fraction按S/Z/V和每个查询的份额定义重建矩阵，精确恢复并核两侧证书；0原导入、0 LP|
|[exact-audit.json](exact-audit.json)|成功核全部13600系数、700逐列余量、37收益行；β=1418/721与17323/8992，两份形式点均W=1且目标匹配|
|[exact-audit-attempts.json](exact-audit-attempts.json)|首恢复因前缀退化支持方程秩7<8停止；加入已观测零slack方程后第二次精确入口通过；原2 LP未重复|
|[self_check.py](self_check.py)、[self-check.json](self-check.json)|最后只做AST/JSON/SHA/来源blob、正式目标与本地链接检查；不执行数学或优化器|

原函数调用都返回status0，但认证来自完整Fraction检查，不来自HiGHS标记。支持/活跃方程用浮点容差选取，最后所有质量、乘子、700条逐列余量、37条聚合行、W及目标匹配以精确有理数接受。原有序stdout丢≤10⁻⁷项、λ round到8位、质量round到9位；精确恢复使用完整capture。

四人系数上证书可以按真实必要IC对任意完整SPE求和；匹配质量只认证这两种行模板的最优，不认证原游戏存在达到该比的SPE。五人部分只解析投影既有更强46行锥的精确12点，得当前两模板β≥5498159/2552735>2；未重扫五人、未重复核旧46行表，没有称这个分数是两模板的精确五人最优。

复现原新事件时应使用新的空scratch目录，保持观测脚本执行时的布局：目录根下原字节文件`round19-menu_synthesis.py`、`round19-prefix_menu_synthesis.py`，子目录`round19-floor-menu/run_observed.py`。脚本以自身位置求源路径并要求`replay`尚不存在；它运行原函数，不运行文件main。独立核脚本与产生的replay置于同一子目录，要求`exact-audit.json`不存在。本包保存脚本执行时原字节以绑定事件，没有为改变布局悄改已执行版本。封包自查只运行`python self_check.py`，无需任何数学复跑。

没有保存默认其它人数的新结果或全SPE证书；没有补造旧命令、种子或运行耗时。本包不含本地数学模块依赖，原代码依赖标准库、NumPy和SciPy，运行版本由execution记录。相关真实菜单、固定G障碍、另一缩放模板、五人46行见证与逐人反族分别在正文解释；不按文件名相似把它们的运行合并。
