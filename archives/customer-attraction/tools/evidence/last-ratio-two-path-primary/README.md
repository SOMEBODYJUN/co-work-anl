# 末位比例两路径探针的完整原件和有限复现

五主源451248B均clean show导出、全文代码/全NPZ读取并核冻结SHA。原件保original完整来源路径；两个原入口各在replay中的新目录执行一次，源码未改，stdout/stderr/run.json均完整。三新NPZ与对应冻结文件全字节相同。

[自足计算正文](../../../state/计算/末位收益比例的两路径松弛与完整终局筛选--计算.md)给所有字段、局部必要约束、完整可信终局递归及精确结果。frozen-inspection.json与new-generator-inspection.json逐项保存全部row/name重构及每个非零整数客户类型；client-types.tsv为同一完整兴趣表。inspect_npz.py保读取与有理残量检查源码，初次辅助header私有API错误与修正保留；它不改变任何原源。

复现顺序：复制原last_ratio.py到一个新目录运行，产生三个新NPZ；复制check_last_ratio.py和三冻结NPZ到另一个新目录运行。不要在original旁运行生成器覆盖冻结文件。两程序顶层固定m3/4/5；原checker仅m3/4实际枚举完整SPE终局，m5只读/有理化而无SPE结果。原生成器依NumPy/SciPy，checker还用标准库Fraction与cache。实际版本和命令见每次run.json。辅助inspect命令为`python inspect_npz.py <last_ratio.py完整前缀> <新JSON输出路径>`。

局部LP精确可行及浮点success均不能当完整策略或精确最优性；原完整检查m3/4目标都false。nSPE字段是互异终局数，不是策略树数。无新一般福利/末位界、六人反例、盲审或外审。
