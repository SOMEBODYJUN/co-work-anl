# 曲率与阶跃依赖网络交付

本批范围是 curvature-step-manifest.json 的23个冻结源版本。数学、审查、程序与输入输出已按来源逐项整理；完整记录以 curvature-step-receipts.json 为准。没有修改共享README或他人正文，没有Git写入、clean claim/done/sync/checkpoint或网络取源。当前交付仅为本地可保全文件，不称已远端推送或正式勾选完成。

## 正式对象

- archives/weighted-congestion/state/定理/非负多项式三载荷精确包络--定理.md：连续log-load凸性、相邻单项式唯一锐包络、最小整数次数与最大统一指数。
- archives/weighted-congestion/state/障碍/前缀阶跃平台的三载荷过冲--障碍.md：三点真实可达、m≥3的指数过冲、m2边界；只排除保真平台模拟。
- archives/weighted-congestion/state/定理/阶跃依赖DAG的路径精确门槛--定理.md：辅助阶跃全部状态门槛及端点、任意非负振幅greedy、正匹配、r有理beta、树/度/浅DAG反例。
- archives/weighted-congestion/state/定理/有向无环端点低泄漏的精确次数预算--定理.md：指定(E)系统iff、固定权判据、最小权与全部slack权、饱和刚性、辅助源锐平方根预算。
- archives/weighted-congestion/state/定理/阶跃极值幅度的多项式全入均衡--定理.md：实际(N)子类全入状态、双缺口矩、所有真实偏离、任意实q的包络与d≥16常数。
- archives/weighted-congestion/state/计算/曲率与阶跃DAG的精确有限核验--计算.md：8份原审计的完整输入域、实现差别、真实复跑、6份JSON逐字段一致及有限证据边界。
- archives/weighted-congestion/state/审查/曲率与阶跃结论的审查范围--审查.md：四原审查的独立性和冻结身份、模型纠错、独有数学去向、旧OPEN及后续全状态下界比较。
- archives/weighted-congestion/state/审查/三载荷包络的独立审查范围--审查.md：独立子批d48807cc21e8a35ca0f8的具体审查义务与原Jensen路线、较强常数、边界/锐性；子代理另实做375例回归。

每个主要承重命题均有稳定ID或明确稳定子对象ID；数学类型、真值、内审状态与全类适用范围分开。

## 原件与复现

archives/weighted-congestion/tools/evidence/curvature-step/ 保存23源指纹清单、8份原程序、6份冻结JSON、replay.py、8份完整实际stdout和stderr及replay-summary.json；原程序和冻结JSON均不改字节。代码只用Python标准库。

```sh
python3 archives/weighted-congestion/tools/evidence/curvature-step/replay.py
```

本轮Python3.12.14实际完整运行全部8份程序，全部退出0，stderr为空。6份清单内冻结JSON与重新生成的字典/列表/标量完全一致，Python字段亦一致。没有清单内独立冻结JSON的包络/step独立审计只保存本轮真实stdout，不伪称存在旧逐文件比较。1.53MB独立全入记录的210游戏、1470偏离全部精确重生成并逐字段一致。

独立子批新375例程序及真实输出在同证据根 independent-cleanup/；这是本轮新内部旁证，不称原历史冻结记录，也不替代一般证明。

## 已核比较及关系

全文比较了本批5主稿、4审查、8程序与6报告，另全文读较后 linear_degree_allstate_lower_bound.md，并全文比较现正式共占降权高度、最少失稳深度桥。

- 三点工具支持前缀过冲。局部保真失败不等于整个拓扑失败或全类存在/非存在。
- step路径q/h分别输入(E)预算和(N)全入状态；后两者互不蕴含。E仅检测端点，N是真实受限子类幅度。
- step辅助模型不属于有限非负多项式类。无alpha-PNE只在alpha<q严格成立，q端点允许均衡。
- 较后全状态线性族已否定原全类固定Cd/ln d保证；本批源中旧OPEN不再作为当前状态。那份较后全文不在23源勾选内，本批不代其owner处置。
- 一般玩家共占降权图高度不同于本组binary资源依赖DAG，不能因同名高度或长链强造等价。

这里完成关系判断记录，未提前构建第三阶段超图。正式图应区分推导、有限检查、实现、来源及状态更新。

## 尚有的数学边界

未证明任意多项式幅度可化成(N)，未证明(E)端点足以全状态模拟，未给一般策略族向binary DAG的无损归约。外部同行评审、全球新颖性和全类最优常数未认证。没有把改善环或有限实验当全部状态无均衡证明。

本地最后校验记录在 cleanup/workspaces/Boss4/curvature-step-local-validation.json：8份正式对象frontmatter与相对链接、23条receipt/目标、14份原件hash、8项审计退出状态、6份冻结JSON相等及新375例stdout源码hash均通过。

仅待协调Boss按当前本地-only约束保全这些路径；远端checkpoint和clean done未执行。
