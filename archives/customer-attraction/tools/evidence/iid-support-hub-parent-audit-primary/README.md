# 支持外枢轴父审的原件与唯一重放

本包保两份冻结源：3577B标准库脚本、2230B四行报告；[source-manifest.json](source-manifest.json)给完整源ID、SHA、blob、双冻结定位及实际保存路径。原代码和原报告分别在[脚本](original/audit_iid_support_hub.py)与[报告](original/iid_support_hub_independent_audit.json)。

本轮已完整实读两源，并将原脚本导出到clone外`run-root-entries/parent-iid`执行一次，exit0。[生成报告](reproduced/iid_support_hub_independent_audit.json)与原报告逐字节相同；[verification.json](verification.json)记命令、唯一入口次数、来源hash、四行/46历史/494含self比较和范围。

这四例真实游戏都两人；静态iid比较是三人。通用分子只做所写系数身份与平移检查，不枚举无界偶k，不求所有SPE或所有静态均衡。完整程序合同、四行收益/福利和解析证明的承重边界见[正式对象](../../../state/程序/两人支持外枢轴的单位展开与静态三人核验--程序.md)。本轮知情重放不新增盲审/外审或新颖性认证。
