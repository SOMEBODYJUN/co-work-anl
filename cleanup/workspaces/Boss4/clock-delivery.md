# Boss4循环复制与锚定时钟18源交付

已完成18个分配源的全文实读、全仓相关与后续比较、逐源语义处置。正式对象8份，未改共享README/图；所有文件为本组新建。本交付是本地成果，未执行Git写入、sync、checkpoint、done或新认领；远端推送受自动审批阻塞，由Boss另行local-only保全后决定后续，不把本地写入说成已推送。

## 正式正文

| 路径（仓库根相对） | 对象与当前边界 |
| --- | --- |
| archives/weighted-congestion/state/定理/循环窗口复制的近次数真实改善环--定理.md | WC-CYCLIC-CLONE-IMPROVEMENT-CYCLES-v1；完整多尺度/guard/Farkas/逐人lift/有理化；全2^E同游戏有全空精确PNE |
| archives/weighted-congestion/state/定理/双轮改善环的锚定三元全状态编译--定理.md | WC-ANCHORED-POLYNOMIAL-CYCLE-LOCK-v1；n≥3任意严格双轮二动作输入，加正单项式时钟后每态有出口；D依B/η/δ/L |
| archives/weighted-congestion/state/等价/锚定时钟的真实有向差分与线性预算--等价.md | WC-ANCHORED-ACTUAL-MARGIN-INTERFACE-v1；精确g/Δ、充分LP、必要S预算、锐次数效率/κ；固定43次证书 |
| archives/weighted-congestion/state/障碍/锚定保环时钟的真实余量依赖--障碍.md | WC-ANCHORED-MARGIN-DEPENDENCE-OBSTRUCTION-v1；固定四人权、α21/20、纯三次下∀D∃G_D保环clock仍留稳定态；空交反链实现 |
| archives/weighted-congestion/state/障碍/同费锚定三元时钟的三次保边障碍--障碍.md | WC-ANCHORED-DEGREE-THREE-LOCK-OBSTRUCTION-v1；完整12列及两套dual，已吸收仅γ0/γ2弱保边的强化 |
| archives/weighted-congestion/state/构造/全三元统一时钟的八十次证书--构造.md | WC-ANCHORED-FULL-UNIFORM-BUDGET-ESCAPE-v1；原全部三元、统一M、80次全16态严格出口，而U预算首次91 |
| archives/weighted-congestion/state/障碍/统一低泄漏锚定预算的次数效率--障碍.md | WC-UNIFORM-CLOCK-BUDGET-BARRIER-v1；全部严格双轮输入若满足U，则全部实q≥D有αlnq/q<α/(α+1)<1；只限制充分预算 |
| archives/weighted-congestion/state/计算/循环复制与锚定时钟的精确核验--计算.md | 原程序/输入/报告资源，逐脚本有限范围、版本差和实际重放，不用有限实验替代普遍数学 |

## 证据与复现

根目录为archives/weighted-congestion/tools/evidence/clock。provenance.json记录18分配源，original/按原路径保存原字节；dependency-provenance.json记录27份额外复现/全文比较依赖，其SHA逐份与冻结inventory匹配。额外依赖不是本批新增勾选。

16份原标准库Fraction脚本全部实际运行exit0，新输出在replay/；命令、Python版本、脚本/输出hash见replay-manifest.json。replay-comparison.json逐叶列出全部差异，16/16数学输出完全一致。差异只有调用路径与actual规范稿hash（旧证书时e229...，当前最终正文de170...已含后加padding）。padding有独立一般证明与两份另行脚本，不冒称旧43次报告已覆盖后加内容。

新建replay_clock.py提供全套重放编排：在仓库根运行 `python3 archives/weighted-congestion/tools/evidence/clock/replay_clock.py`；拒绝覆盖既有replay-new目录，可传--output-dir新目录。它已检查语法，16份实际运行是此前记录的原命令，未把该新入口冒称已执行。

## 实质比较、关系判断与接续

已完整读现有任意乘子夹逼、局部Shapley份额势、有限矩阵严格替代正式对象，并全文读原class_front_phase_quotient.md与linear_degree_allstate_lower_bound.md。cycle不是无均衡；lock需要从2^E删回环的两个动作，B必须覆盖全部状态。全局跨权anchor的U预算受R>α和δ≥(R+1)/(R+2)耦合；后续同类等权时钟以(2/3)^p泄漏和全部product-front出口绕开该接口。

关系已有实际依据：多尺度乘子测试和有限矩阵严格替代共同支持循环lift；循环lift给一般clock的可用二动作输入，但全类高倍率否定仍需输出次数；Shapley严格R改善下降与全三元δ几何共同推出U障碍；actual差分给预算和列效率，padding以其总预算加固定稳定gap推出架构障碍；43/80证书明确证明U非必要。三次dual和padding的架构边界不同，不能互相替代。后续一般线性下界对p≥2²⁰给每态p/10严格出口，已否定原Cd/ln d全类存在目标；旧正文OPEN只保留历史身份。没有以本批有限证据代替该后续证明。

阶段三按用户阶段要求另建有解释超图；本批不复制旧图或提前生成超边。这不是未知联系，以上已明示拟用关系、前提和证据。

## 回执与缺口

clock-receipts.json为18条依receipt-example填写的逐源真实处置，targets全指已存在的正式正文；子组四条原始协作回执另在clock-barrier-receipts.json。Boss尚未done；须按当前远端授权情况处理，不能用本地存在冒充已推送。

本批范围内的一般证明、有限证书和方法障碍均完整保存；未认证全球新颖性、外部同行评审、43/80最优性或实际全类最优倍率。稳定态padding只限制固定anchor/phase/对内同费、必须保原环架构；U只限制充分预算；class-front反例并不否定健康前沿输入族。额外未认领依赖只供复现比较，不能顺带勾选。源原件从集中clean show缓存取得且hash核过，本组没有接触凭据或网络。
