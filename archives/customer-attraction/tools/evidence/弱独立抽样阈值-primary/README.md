# 弱独立抽样阈值：四冻结源及有限前缀证据

数学正文：[弱独立抽样阈值的原程序与完整历史证书](../../../state/审查/弱独立抽样阈值的原程序与完整历史证书--审查.md)。四个primary合10355B，全部通过`work.py clean show ID --out`独立导出并完整实读，双冻结来源同字节；[manifest](source-and-dependency-manifest.json)保原路径、size/SHA256、源commit及存储位置。

| primary ID | 文件 | 实际内容与处置 |
|---|---|---|
| 954ec6953014060f47ef | round4_parent/audit_weak_iid_threshold.json | 七组m=K切口、两多项式移位、Taylor常数；原输出保全，解析数学复用成熟证明 |
| edcc7e2066c6cd0d12cf | round4_parent/audit_weak_iid_threshold.py | Fraction几何逆核及下界/差恒等式；原完整main不重跑 |
| 7a4d2f187a5feb8f5ce4 | round4_search/weak_iid_policy_review.json | 六完整树原报告、100有理切口及无限族常数；本次只精确重现其六行 |
| 688ad92e7306b316acec | round4_search/weak_iid_policy_review.py | 固定P1/P2全历史策略、canonical verifier及另写terminal逐偏离检查；原有限前缀一次成功 |

`original/`按完整源路径保存原件；其中另外5份customer_attraction包与strategy_lp文件是**导入依赖旁读**，不是额外primary或done。它们来自仓内已保全原件，并与inventory冻结size/SHA核对；全部读取了实际所用收益/完整域校验/序列化等合同。包`__init__`引入exact类，LP模块为serializable加载numpy/scipy，但本次没有调用均衡搜索或LP。

`replay_finite_policy_prefix.py`使用冻结原代码imports和helper定义；不调用原main，而仅把原main前两条AST语句（rows初始化、六例for）加return执行一次。代码SHA、前缀AST SHA、原JSON SHA均保在[输出](finite-policy-prefix-replay.json)。原source和原JSON不改；0父代main、0完整独审main、0已充分计算的53/100标量重跑。启用assert的`python3 -I -B`一次成功，exit0，stdout见[原输出](finite-prefix.stdout)、stderr空；完整cmd/cwd与wall时间见[运行记录](runtime-record.json)。

新核六棵固定换瓣完整树，合12448有序决策历史、每一方法64958非自身比较；canonical与原直接terminal循环均通过，6行与冻结JSON逐字段相同。不能称原JSON的整个main输出字节已复现，也不能换成另一原循环策略的10例6697节点/31668含自身比较。

已有mK100和m=K≥53有理数成功证据复用`../common-iid-mixture-and-petal-threshold-primary/`，未执行其入口。已实读旧代码/输出及`../weak-iid-original-reviews-and-research-ledger-primary/prior-success-metadata-erratum.json`：旧`new_fixed100.t`的197/200误标应为1969/2000，其余固定100值及189/2000余量不受影响；父程序100例197/200本来是另一个正确切口。

所有全称数学由正文解析分类与正系数证明承担，不由有限输出外推。本族反驳原模型的辅助弱iid福利桥，仍满足真正安全聚合和half；53不是最小人数，没有六人half新结论。
