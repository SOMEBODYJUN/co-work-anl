# 规范贪心有限推进的定向实现证据

本目录服务于[算术与实现边界审查](../../../state/审查/规范贪心归位构造的算术与实现边界--审查.md)。数学主源752290ca9fcf4dc0ebb1由[引理](../../../state/引理/阈值截断与归位计数的严格推进--引理.md)、[完整构造定理](../../../state/定理/规范贪心占位的完整盒均衡与因子二续局--定理.md)和[结构DP推论](../../../state/推论/结构参数下完整盒均衡的多项式选择--推论.md)承担。

## 实际执行范围

[integer_bound_serialization_check.json](integer_bound_serialization_check.json)是本次清洗新增的同一输入两次定向调用记录。第一次定位整数报告错误，第二次补取准确异常帧及最终数学检查结果。原代码、Python全局十进制限制均未修改。

实际环境Python 3.12.14，整数十进制转换限值4,300。输入为两个地点、三设施，私有原子3和2，另15,000个各权1/15000的双选项客户。规范占位(0,0,1)、末分数2、初始超额全0，实际改善/归家/批数均0，完整数学终检通过；随后原construct_on_path第227行str(bound)拒绝把2^15000−1转成十进制字符串。它有15,000个二进制位、4,516个十进制位。此记录不构成轨迹长运行、复杂性下界或数学存在定理的反例。

[reproduce_integer_report_boundary.py](reproduce_integer_report_boundary.py)是清洗时写的单例复现辅助入口，正常模式每次只调用一次原construct_on_path，采集解释器当前限值、实际异常帧和局部结果；若该解释器允许转换，则如实记录返回。它不自行降低或关闭限值，不修改原程序，不跑完整证书或其他测试。使用普通Python，禁用-O；拒绝覆盖输出。

本批对这个包装入口只执行了 **--check-dependencies**，得到[dependency_check.json](dependency_check.json)：逐文件核固定SHA-256并做语法编译，constructor_calls=0。实际两次构造调用发生在包装前的直接定位中，不能把此依赖检查重复计作第三次构造运行，也不能称包装入口正常模式已经运行。

## 精确依赖和可执行重建入口

固定版本为提交68fad804ec5946cb296f77dc5b336308a66abf12。

| 原相对文件 | 源ID | SHA-256 | 本目录使用方式 |
| --- | --- | --- | --- |
| multi_facility_spe/__init__.py | 3185703b41c7540715bc | 14e0072f1de3ea824867d37a3f4b98f80847bc4676d224485cb7a1a4b8a133b7 | 复用此前已清洗保存的原字节 |
| multi_facility_spe/two_exists.py | a7a1f7d850e620474411 | 85835c6481c7755a1bca0668c22dd8390578661ee34afdaa83bc31e1d909eb3e | 复用此前已清洗保存的Instance与核心依赖 |
| multi_facility_spe/greedy_box.py | 4e4efdb8c30ab03aee8b | b3b391f6e4c1efd8e56c036d3d588f191959504aede58e686c3bfcb291f6ef35 | 本批全文比较并按固定源ID导出，原字节另存source树；不自动done |

前两份的实际保留位置为
[factor-two-audit-suite/source](../factor-two-audit-suite/README.md)下的原包相对树。原包__init__仅有说明文档；two_exists只用标准库；默认improve-return不进入equal_light_flow延迟导入。因此这两份加所导出的原greedy脚本就是本单例所需完整Python依赖，不要求完整旧仓库。原greedy已按原字节保存在[source/multi_facility_spe/greedy_box.py](source/multi_facility_spe/greedy_box.py)，也可从清点固定版本明确重建；不混用未知工作树代码。

从结果仓库根执行以下命令；输出目录自行创建，每个JSON须取不存在的新路径：

~~~sh
mkdir -p cleanup/workspaces/reproduce-greedy-bound
python3 archives/facility-games/subarchives/common-many/tools/evidence/greedy-box-finite-progress/reproduce_integer_report_boundary.py --core-root archives/facility-games/subarchives/common-many/tools/evidence/factor-two-audit-suite/source --greedy-source archives/facility-games/subarchives/common-many/tools/evidence/greedy-box-finite-progress/source/multi_facility_spe/greedy_box.py --output cleanup/workspaces/reproduce-greedy-bound/dependencies.json --check-dependencies
python3 archives/facility-games/subarchives/common-many/tools/evidence/greedy-box-finite-progress/reproduce_integer_report_boundary.py --core-root archives/facility-games/subarchives/common-many/tools/evidence/factor-two-audit-suite/source --greedy-source archives/facility-games/subarchives/common-many/tools/evidence/greedy-box-finite-progress/source/multi_facility_spe/greedy_box.py --output cleanup/workspaces/reproduce-greedy-bound/actual-run.json
~~~

辅助入口会在任何导入或构造前核三份SHA-256和语法，拒绝版本不符。源码加载保留multi_facility_spe包名以解析相对导入，并禁写pyc；不修改包目录。如需重新导出原件，可用根clean show 4e4efdb8c30ab03aee8b --out 新路径；它是只读冻结导出，首次未缓存读取可能需要网络，不包含认领、done或Git写操作。上述三份依赖已一同纳入本批显式checkpoint预像核验。

此前实际验证的19文件核心重建树也可作为--core-root；本次记录的依赖检查使用该已有树，并与正式source树两份字节核对相同。这不是把19文件快照扩称已包含greedy模块，也不是自动认证该模块的可选分支。

## 未执行和来源处置

本批没有重复此前reverse/barrier实验，没有跑greedy全局审计、完整证书、所有默认布局、equal-light-flow或两类DP。数学终止量词来自完整证明；本目录只提供一个具体软件边界及可重建的核对入口。

主源提到但本批未处理的回归、审计脚本、输入及输出各有独立清点身份。代码4e4efdb8c30ab03aee8b虽已全文比较并参与定向实验，现已另批认领进行源码清洗，当前没有随752290ca9fcf4dc0ebb1一并申报完成。修复决策留待其正式源码清洗，冻结原件不变。
