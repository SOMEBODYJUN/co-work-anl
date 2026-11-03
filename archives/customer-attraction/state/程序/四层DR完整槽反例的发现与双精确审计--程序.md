---
id: customer-attraction/four-layer-dr-full-slot-discovery-and-two-exact-audit-contracts
kind: program
type_tag: 程序
title: 四层DR完整槽反例的发现与双精确审计
status: original-inputs-and-reports-bound; parent-exact-entrypoint-replayed; no-new-MILP
truth_status: exact-certificate-and-finite-discovery-contracts-separated
review_level: all-ten-primary-files-read
scope: 三人四标签固定实际012、uniform查询；原浮点发现与完整整数证书分别保存
summary: 保留有限层MILP、二次负交互探针、70势值/21动作输入、作者与父方Fraction审计及报告；只重放父审一次，不把浮点最优或未附二次输出写成定理。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/round2/fullslots/audit_general_dr.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/round2/fullslots/dr_counterexample_audit.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/round2/fullslots/probe_general_dr.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/round2/fullslots/probe_general_dr_float.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/round2/fullslots/probe_quadratic_dr.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/round2/parent/audit_fullslot_dr_parent.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-c8ca54e5f2854c2c93bf83abc2f24f5c/round2/parent/audit_fullslot_dr_parent.json
---

# 四层DR完整槽反例的发现与双精确审计

这组程序服务[有限四层DR完整槽反例](../反例/有限四层DR势的完整槽聚合亏损--反例.md)。它们没有真实客户兴趣表，不是原CAG或六人half反例搜索器。10个primary共31,000字节，两冻结提交的各文件字节相同；[manifest](../../tools/evidence/finite-layer-fullslot-dr-primary/source-manifest.json)保完整来源、SHA-256、大小及本地路径。原件全部保在同一证据目录的original/fullslots与original/parent，程序均未改写。

## 有限层MILP实际编码的模型

`probe_general_dr.py`固定k=4、m=3、actual=(0,1,2)、查询uniform及big-M=10。它显式枚举0至4层70个计数，势变量F(q)满足0≤F(q)≤|q|，140条新增边际介于0与1，150条含重复方向局部DR方格非负。只控制这个有限域，不是无限人数的势函数，也未要求客户相容性。

全部85个长度0至3的有序历史各有未来完整叶查询价Q；各历史另给已行动角色的真实终局边际U。终局Q直接由第4层与第3层势差的四查询均值定义，U由第3层减去指定一槽的第2层势定义。21个内部节点各有一热动作Y和当前最优值V：V不低于每个动作真实孩子收益，所选Y又强制相等；过去角色的U和Q沿所选孩子复制。这保留全部离轨有序节点和平局，没有把策略压成计数函数。

固定实际012的三个动作；每行变量R_i不超过该实际前缀下四个强制孩子Q。最小化“实际总边际效用−ΣR_i”，所以保存的 `gap_float=-res.fun` 是所测SUMmin-full违反。全部变量491个，其中84个Y为二元，行约束1206条；这些是代码结构计数，不是本轮运行优化器统计。Q/U/V/R受[0,1]界，big-M=10足以释放复制及最优动作约束。限定势边际≤1、固定实际叶和固定uniform查询仍只给一份有限定向检错，不代表任意参数或任意人数的完整搜索。

程序在模块顶层构模并调用SciPy `milp`，45秒时限、relative gap 10⁻⁹；只把JSON打印到stdout，没有main guard、输入参数、文件读取或自动证书恢复。import也会启动优化。非成功但有res.x时仍可能输出势及argmax策略；浮点状态不等于精确可行性、SPE或数学最优性。

## 2945字节浮点保存点与精确输入的关系

`probe_general_dr_float.json`完整保存70个float势值、21个动作、status0、HiGHS Optimal消息、gap≈0.025000000000001465和dual bound≈−0.025000000000001465。它没有运行时、argv、源码哈希、solver环境或精确对偶。精确JSON的每个势值是这些float的十倍在数值误差内对应的整数，完整策略相同；本批逐字段绑定两表，未把原float字节改成有理数。

数学结论独立使用给出的70个**整数**与21个动作：它们有完整精确域及合法性、单调DR、全部历史IC和严格gap=1/4证明。无需证明浮点最优值恰1/40，也不据该点声称最小规模、最强亏损或发现唯一性。

## 作者审计与父审的不同承重内容

`audit_general_dr.py`只用标准库，读取同目录精确JSON；所有数转Fraction，按势表遍历140单调边和150DR方格，按策略键遍历21节点、每节点4动作，共84项含自身比较。它沿每个具体历史的原动作表真实完成，不冻结实际后继。再列实际012、收益2/3/3，三个实际菜单的全部12叶、均匀查询值11/4及总差1/4；另核四个重复调和残差4/3/5/5，输出首个负三阶差−5。原2531字节JSON与这些定义匹配。

作者脚本按输入键遍历，未主动断言势域/策略键恰为完整标准集合。不能将它当作任意非法输入的完备schema检查器。本批另从定义构造70个计数和21个有序历史，精确比较全部键并检查动作合法，关闭这个具体输入的域缺口。

`audit_fullslot_dr_parent.py`另从所有0、1、2长度有序历史及四动作枚举84项IC；同样读整数势、以Fraction核140单调边、150DR方格、12完整菜单和差1/4。它还直接证**同一固定三人终局收益表**非CAG：全0推出主题0客户价值9，实际012的0收益2低于必要下界3。父审480字节报告保全部这些汇总。这个固定三人证明比仅排除低层调和势更强，两者分别保留。

两个原审计都在顶层执行；作者脚本写同目录dr_counterexample_audit.json，父审按自身路径向上定位fullslots输入并写同名JSON。故应在副本中运行，避免覆盖冻结报告；它们都不是无写入的纯import库。父方源码相对作者有独立重构结构，但这是项目内部复核，不冒称外审或新颖性认证。

## 二次负交互探针为何只保合同

`probe_quadratic_dr.py`固定同样k/m/actual/uniform，big-M=20，给对称w_ab∈[0,1]（含w_aa）。对应势可写

\[
 \Phi(q)=H|q|-\sum_{a<b}w_{ab}q_aq_b-\sum_aw_{aa}\binom{q_a}{2}.
\]

取H≥3，则到第4层的所有新增边际非负，且非负w保证含重复方向DR；对称且逐项非负不蕴含矩阵半正定，所以不能自动称全实空间凹势。三人终局中自己的交互成本C_i=Σ_(j≠i)w_(a_i,a_j)，实际收益H−C_i；完整叶查询碰撞S(z)=¼Σ_(t,a∈z)w_ta，查询边际H−S(z)。常数mH在预算差中抵消。

内部V最小化当前角色真实成本，所选孩子复制过去成本和S；R_i≥每个强制孩子S，故目标min[ΣR_i−2Σ_(j<i)w_(actual_i,actual_j)]的负值才是正SUMmin gap。变量431个、二元84个、行916条；同45秒MILP，stdout打印原float权重和argmax动作，不作有理恢复或精确认证。它也没有main guard，import会求解。

README只报告该先行探针“浮点最优0、无阳性、未继续阴性扩样”。本10源不含其独立原输出，故本批不能给它补造JSON、精确最优对偶或执行史，更不能从浮点阴性提升为整个二次类或原CAG正面定理。[另一个六标签二次保存点的精确等号](../计算/对称二次势探针保存点的精确保底等号--计算.md)有不同输入、不同静态安全目标，不能移用来认证此处的完整槽预算。

## 本轮真实执行和复用

在original原件之外，隔离`replay/round2`复制父审脚本及精确输入，**父审入口1次**，约0.066秒、exit0、stderr空，生成JSON与冻结报告逐字节相同；[event](../../tools/evidence/finite-layer-fullslot-dr-primary/parent-replay-event.json)保脚本/输入哈希、argv和实际输出长度。作者审计及两MILP的import/main/solver调用均0次。新标准库保存检查另核域、原表绑定、原报告语义和一般删除恒等式；没有优化、随机扩样或新增客户搜索。

成熟的[基数凹化](../定理/有限层匿名边际势的基数凹化--定理.md)、[22环反例](../反例/匿名边际势的自由列亏损与凹化保持--反例.md)、[原CAG完整槽候选](../候选/全槽逐行最小价格的共同预算与有限报告--候选.md)及静态充分桥只作实读比较并列reused，不重跑其成熟核验。本程序资源保留各原件独有功能和真实证据等级；一般原CAG共同付款与恰六人half仍不由本组程序解决。
