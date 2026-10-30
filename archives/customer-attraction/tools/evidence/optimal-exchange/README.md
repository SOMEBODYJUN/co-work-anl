# 最优索引交换的有限精确资源

对应[计算对象](../../../state/计算/最优交换二项矩与Beta核的精确核验--计算.md)。原脚本来自冻结源588621da61aa3af9d88c，源码逐字节保存，完整来源及实际运行记录在[PROVENANCE.json](PROVENANCE.json)。

从仓库根运行：

~~~bash
python3 -B archives/customer-attraction/tools/evidence/optimal-exchange/audit_bernoulli_exchange.py
~~~

只需Python标准库。主入口固定limit=12，无CLI参数、外部输入或随机种子；不写文件，输出是Python字典repr而不是JSON。原程序使用assert，必须保留断言，不用-O/-OO；-B仅禁止pycache。

本轮实际运行一次得到24570次二项矩与4095次Beta系数检查通过。完整stdout保存在[replay_report.txt](replay_report.txt)，用字面量解析后另外保存为[replay_report.json](replay_report.json)。没有把派生JSON称为旧冻结报告，也没有声称与未提供的历史输出比对相等。

这些计数为固定参数循环的断言数，并非客户实例或完整SPE数。所有范围、重复身份计数、一般证明与有限程序的关系在计算对象中逐项解释。
