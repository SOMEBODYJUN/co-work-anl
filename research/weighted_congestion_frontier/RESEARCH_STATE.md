# 当前研究状态

更新：2026-10-14 UTC。

## 活跃目标与前沿

**WC-TARGET v1：OPEN。** 精确对象、量词和阈值采用 MODEL.md、CLAIMS.md。本轮奇环成长族已有完整一般证明和独立内部攻击，给出a_*(d)≥T_d∼d/ln d，严格超过核实过的已发表成长基线及原源式包络。全类存在上界仍≤d，未确定增长阶，全球优先权未认证。

主要 proof obligation 是获得全类的次线性存在上界，或构造玩家数可增长、每个纯状态均有足够大倍率获利偏离的合法非存在族。近似势函数、全状态偏离比较和新的表示都是搜索起点；现有文件中的路线允许继续扩展。

## 当前协作方式

一个 Work 对话使用提示词指定的角色号统一发言与提交，子 agent 在内部按需要并行研究。`tools/work.py` 配合本会话的 txt 凭据，完成恢复、同步、公屏收发和 checkpoint；本地配置固定后直接复用。

`wcg/board` 是微信式异步公屏，只保留当前消息流。各对话分享具体发现，自主继续研究；同题独立工作、多路线与反例攻击可以同时推进。公屏消息在研究间隙读取，回复随实际发现发送。

论文者和提取者分别整理贡献表达、发掘独立数学工具，使用同一程序和角色号流程。相关完整入口见 prompts/，来源原文见 SOURCES.md。

## 下一项有信息价值的动作

从一手文献与公屏选择关键义务，先以精确计算或边界族区分竞争机制，再建立一般证明。每次真实增量写清 claim/version、已知、objection 和下一检验，完成相应核验后立即 checkpoint，并向公屏分享已推送文件的 descriptor。

本次修订改变协作程序与现行说明，WC-TARGET 的数学身份和 OPEN 状态保持。实际本地验证和远端部署结果记录在 evidence/validation.md。

## R3 frontier after exact source/topology closure

源式sharp factor为(2/√e)√(d ln ln d)/ln d。改变同权两列费用为任意非负多项式、加强全状态攻击均不突破该渐近，因为α≥ρ可还原源式。下一信息动作是非对称高support关联，或异权full-state覆盖；有限degree32交叉构造及全源参数精确比较正在独立核验。全类目标保持开放。

## R3有限次数交叉分离与延伸缺口

已完成并独立核验 T32≤89/50<9/5<B(G)。source32全部整数参数/实区间的证明和交叉16状态/64偏离都可复现。固定weights/coefficient直接升degree在40已有9/5-PNE，极限亦失败。主目标仍OPEN；下一义务是玩家数/resource support可增长的交叉反馈，以及dense近等权组的可粘合存在机制。参数化四玩家极限族与窄带Shapley候选另行审查，不将其默认为新无限下界或全类上界。

## R3局部权带和padding前沿

资源内部ratioR给R-PNE，Shapley正系数proof及不同iid-support独审闭合；同resource多dense尺度仍缺新桥。minimum potentialdensity可任意padding而保持完整finiteα存在问题，故只提高该密度不会得到真正更窄子类。需active load/mandatory participation/preprocessing，并证明选择过程保持该性质。四玩家缩权template一般proof亦独审闭合，cubic根只刻画指定见证；retuned v2认证m≥20及m3，m1,m2失败。所有这些局部资产不闭合WC-TARGET的增长阶。下一有信息价值的义务：高support可增长交叉反馈，或在同resource多dense尺度间建立新的共同预算/选择机制。

## R3 奇环成长下界与精确证书包络

已完成WC-R3-ODD-RING-CERTIFICATE/ENVELOPE/LOWER v1。每个d≥2、每个alpha<T_d都有全degree-d正有理游戏无alpha-PNE；T_d∼d/ln d。一般证明覆盖任意cohort混合状态，系数显式闭环；两独立攻击及Fraction逐资源小实例核验已闭合。原策略机制归R1公屏42，本轮R3标量还原/精确界另有清晰来源。此为相对核实基线的无限下界阶段突破，WC-TARGET仍OPEN。

剩余义务：全类O(d/ln d)或更好的存在机制，或打破positive two-test certificate得到更强下界。精确T_d必要性只约束指定证书；不能当实际整个拓扑或全类上界。低成本下一检验是任意非负混合polynomial是否仍受同包络，以及完整局部orbit攻击是否能超出这两类充分测试。文献检索有漏查风险，禁止全球首次表述。

已追完混合多项式的低成本义务：任意每组nonnegative shapes仍exact T_d，constants/zeros已攻。继续同uniform强forcing调参已没有增长阶信息。真实剩余缺口是全部cohort占用数的状态覆盖或全类存在预算；anti-light反向偏离阻止从failed hub test直接构造均衡。

实际拓扑子类已回收：所有cohort均n_i=1时，single-conflict cycle给T_d-PNE，support2另给2-PNE，所以min{2,T_d}成立（不称sharp）。反向orientation必须逆转环序与交换角色；只shift角色不够。一般n_i>1共同A负载破坏该图，这是具体未解obligation。完整state counts/映射/zero边界已有精确回归。

本阶段交接：已知全类下界T_d∼d/ln d，指定强forcing证书即使混合费用也饱和；上界仍≤d。能继续改变数学认识的下一步是构造/排除一般cohort的部分对齐稳定区间，或独立全类O(d/ln d)存在机制。不能由当前证书失败推均衡、由singleton图推多轻类，或继续同式调参冒充突破。
