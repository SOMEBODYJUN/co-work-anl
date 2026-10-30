# decision-calibration十源交付

正式认领推送：`41ff68570d7b0daad1d66fc6714045c6d9727e16`。十源162543字节均完整实读；逐源处置见[decision-calibration-receipts.json](decision-calibration-receipts.json)。本文不代协调者声明checkpoint已推送或已done，也不重复其他owner的来源。

## 正式数学对象

| 对象及路径（archives/weighted-congestion/下） | 独有内容与边界 |
| --- | --- |
| state/算法/共同玩家尺度的三层有理校准--算法.md | 固定F的精确尺度、字典/自由局部/全图三LP、真偏离下降、自足d基线、零费/mandatory背景/齐次及复杂度边界 |
| state/定理/固定玩家尺度图势的圈比阈值--定理.md | 固定h的负圈充要、简单圈比精确阈值、零分母和Bellman–Ford；合成图不伪装拥塞实例 |
| state/反例/有理实例的无理局部校准阈值--反例.md | 权(3,1)、x²/x³/1/0的解析无理端点及两条路径区间构造，固定有理α的LP不意味着有理最优 |
| state/反例/唯一精确均衡与共同尺度图势不相容--反例.md | 权(1,2)、x/x²、16态唯一全空PNE且严格改善DAG，仍无共同尺度α1图势；96全偏离与47strict区分 |
| state/算法/原实例支配时钟的前沿精确决策--算法.md | 给定原游戏已有完整clock的D合同、非法单人修复与front全部离域非改善，有限枚举的YES/全状态NO及失败诊断 |
| state/反例/几何前沿修复的成本与稳定性失真--反例.md | 纯规范化毁掉PNE且0→任意K，端点稳定仍可漏内部离front改善 |
| state/反例/支配时钟下的六玩家前沿循环--反例.md | 原六人16资源满足D却有front环；另以36front+28非法态完整覆盖才证64态全无精确PNE |
| state/归约/单根模块的冻结报价与固定延续提升--归约.md | 全原动作β条件稳定与每对动作D≥q合同，固定lift给max(α,β)；坏稳定报价、反投影失败、有环可删例分别保留 |
| state/审查/结构恢复的历史时点与森林区别--审查.md | 恢复基准/审计快照区别、旧证明缺失与后来新建稿、七资产身份，类型图森林与玩家资源森林一般互不包含 |
| state/计算/共同尺度与原游戏修复的精确核验--计算.md | 三原程序及全输出、首次缺blob的真实失败、独有证据覆盖/迁入版本身份、两NO端矩阵和DAG持久证据 |

十正文均有稳定ID、完整source commit/path、承重条件、关键证明/失败机制及接续用途。原Claim三个ID保留为legacy_ids；没有按程序目录把数学对象合并成不透明附件。

## 证据与真实复现

证据独立放`archives/weighted-congestion/tools/evidence/decision-calibration/`。`provenance.json`保存17原件281436字节（10认领源+7比较依赖），逐件hash/大小核对。比较依赖只读不done：内部审查、旧结构范围比较、用户参考、结构README、迁入manifest、线性主稿及历史tex。其中前五全文读、线性主稿前批已全文比较；tex只核历史hash/marker，PDF未物化未读。

三个原精确程序均真实成功，完整输出逐字段零差异；见`run-index.json`和`replay-comparison.json`。calibration/repair各只跑一次；recovery先exit1因固定历史tex blob未物化，原stderr在`replay-recovery/`，协调者补同一blob后仅此程序补跑exit0，见`replay-recovery-after-dependency/`。原程序、断言、冻结输出均未修改；没有重复运行两已成功审计。

- calibration：631基础LP、459局部行、12游戏101态356偏离、101起点下降。两校准二分宽1/256仅包下确界，解析无理端点另外证明。邻批独审1500 LP/10游戏62态228偏离为另外证据，不混计。
- repair：n3…9几何1016态8184翻位2582修复步；24原clock例3432态8034全部front翻位4620修复路径步；50个完整lift；36行front出口/28非法态全覆盖独有内容保留。
- recovery：固定3efbaf6…完整4465路径树三缺名、p/10/d/10与用户参考hash及两森林例；source_recovery JSON的240eae…基准另记。额外七资产冻结hash吻合、六个可读BASE blob hash吻合、七个last-change吻合，PDF可用性明确为false。

`export_calibration_witnesses.py`一次补证导出，不重跑整套作者审计：把原二分低端未落盘的32×10和32×14原矩阵/Farkas保存并以另外的精确行求和核bTy=−1；独立字面重建16态96偏离47strict拓扑/唯一sink，另重建96×18图矩阵核原Farkas。它是持久证据与有限独立核查，不伪称另一通用LP求解器。

`migration-reconstruction.json`及`reconstructed-reviewed/`由完整迁入字面diff反向重建calibration/repair工作区旧稿，全部上下文吻合、全文hash等于审查记录。是从diff重建而非宣称直接取得失落旧分支；迁入差异为路径/链接/状态，原程序hash不变。旧repair_audit_v1.py/json未在清单，本批未声称阅读或运行。

最终只读检查未重跑原程序：17原件hash/大小、三个完整输出比较、两个重建旧稿hash、两补证dual再次精确行检验、五Python文件AST、十ID全仓无重复、十正文相对链接可达、十receipt ID恰等于认领源。证据索引`final-verification.json`明确检查范围，字段检查不代替数学阅读。

## 实际比较与关系判断

共同尺度校准细化既有证书接口；与原游戏直接枚举/质量包络保持不同合同，mandatory平移不自动保全社会目标。无理阈值和唯一PNE但图校准NO分别给优化/接口边界。原实例已有clock决策与此前加clock的全态编译共享几何，但输入游戏身份不同；front FIP、稳定态存在和全状态无解分别保留。单根冻结模块lift条件推广已有挂树，不声称任意有环都可消。类型图与玩家资源关联图的两森林关系准确比较，第二例三类型不冒充至多两类型合同。

与source_envelope_next实际互读：其两个反例“存在精确均衡仍保留严格改善环”“私有惩罚编译不能保持原游戏稳定”已全文比较并交叉链接，本批16态DAG反例与其保环PNE例说明不同失败机制。其decision-core20审查/runner/质量/独审来源不在本批重复done。结构positive-repair由selector主写，本批只写独立calibration/repair/recovery对象，不修改他人正文或共享README/图。

阶段二保持上述正文解释链接，阶段三另建正式解释边。全类Cd/ln d旧目标的后续全状态线性下界仍保留；本批不以旧OPEN恢复原目标，不称新颖性、外审、全类位多项式或投稿认证。
