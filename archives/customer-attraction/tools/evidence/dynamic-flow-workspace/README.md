# 根重置工作室的四源与实际精确核验

正式对象：

- [根重置对恒等式与辅助尾份额协方差](../../../state/引理/根重置对恒等式与辅助尾份额协方差--引理.md)：保RESET四membership推导、同分布协方差和正确税期望；原稿式(5)在无条件期望仍含a_A时多一个p_x，后续原稿已有勘误。F_A不在所有分支都等于实际尾份额。
- [根重置局部账本的笛卡尔放大](../../../state/障碍/根重置局部账本的笛卡尔放大--障碍.md)：八人基对R=9/10、两e及J为零；全整数k乘积保全部历史SPE并放大到9k/10，仍W=OPT=32k。同两点iid查询反而满足实际u封顶。
- [同分布额外查询高于平均强制收益](../../../state/反例/同分布额外查询高于平均强制收益--反例.md)：三人八客户完整31历史，pKp−pD=13/1722>0，但pKp−实际u=−839/574；原脚本docstring及stdout范围误标actual u，原字节/原输出原样保留。

`original/`含14原文件1516795字节：4主源15063字节、6真实执行依赖、4比较稿。source-manifest.json逐条保完整双冻结commit/path、ID、原长度、SHA及角色。客户重数均表示不同单位客户，当前六人完整SPE目标没有改成设施客户NE或三/八人特例。

本轮实际执行普通Python3.12.14、保assert、PYTHONDONTWRITEBYTECODE=1：

1. 原diagonal脚本真实__main__一次，规范verify_certificate为31历史124非自身偏离；Python profiler在main返回时取已有变量，导出同一次求解的完整instance/证书/K/D，没有再次调用solver。
2. 原raw-DAG verifier一次，不导入规范包；13872节点、6435终局、59496含自身比较，其中50732严格/8764相等，最小松弛0，W=OPT8=32。
3. 新定义级检查不调用规范模型/solver/verifier：从原31行动重建完整三人树，逐名单位客户重算155含自身收益、124实际偏离、全部K/D/p乘积；前两层150对RESET。另从原DAG真实分支重算根64对RESET及p3=p7=1/2的完整税期望，并以DAG路径重数核2396745决策历史/16777216终局历史。再核1280个标量RESET身份。

这些执行彼此有共享输入/证书，不能称为两个独立发现器或合计扩大数学样本。普遍RESET及全部k乘积由正文代数证明；没有枚举巨大乘积树，没有运行stationary-source比较审计、随机扫描、LP/SLSQP或其他已完成原审计。

`replay/`保两原入口stdout/stderr、原DAG完整报告、原三人完整证书和本次额外定义检查。`execution.json`记录真实绝对命令、launcher cwd与base子进程cwd、env、时间及源码/日志hash。执行后只修正驱动器的元数据字段以区分两个cwd；精确执行版保`replay-executed.py`，当前`replay.py`只调整这些记录字段，两个hash均保，原程序未改、未重跑。

复现使用新目录：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 archives/customer-attraction/tools/evidence/dynamic-flow-workspace/replay.py --run-dir /absolute/new-run-directory
```

已成功一次，无需为保存再跑。复现器先核14原件SHA及长度，复制原相对路径，保存全部中间与输出，再核源码不变；新目录已存在则拒绝。仅用标准库，无Git/外网。原错误scope不会静默过滤成正确标签，应按正式正文的精确比较解释。
