# class-front 8源交付

本批8源已全文实读、比较并分别语义处置，均integrated；尚未由子代理执行Git、checkpoint或done。Boss已通知claim pushed于`312c5851e9e6e7256584ab8d3e3c1da2df0dd966`。请先串行checkpoint确认pushed，再用本批回执done；本文不将本地保存说成已推送。

## 正式正文

- `archives/weighted-congestion/state/定理/循环窗口前沿的扭转相位商--定理.md`：稳定ID `weighted-congestion/clone-front-phase-quotient`；完整literal域、全状态扭转协变、精确商数及标签边、真实forward/backward费用表；保留原freeze缺每类test覆盖导致重复策略的实质修复。
- `archives/weighted-congestion/state/反例/严格双扫环的不同步稳定前沿--反例.md`：稳定ID `weighted-congestion/class-internal-clock-front-obstruction`；24资源严格环/六端点稳定/两内部改善分开；非负同费递增clock不能新增保前沿出口。
- `archives/weighted-congestion/state/障碍/有序同类三元时钟保留严格均衡--障碍.md`：稳定ID `weighted-congestion/class-internal-clock-compiler-obstruction`；独立64资源固定输入、全部12条严格精确PNE差；任意有限fresh同类递增同费非负非减clock保留该均衡的任意次数一般证明。
- `archives/weighted-congestion/state/定理/同权类前沿全覆盖的全状态编译--定理.md`：稳定ID `weighted-congestion/class-front-allstate-compiler`；完整η min-max、全部状态B、L逐玩家预算、非法态单人修复、标准与分离预算、α=1精确抵消及9玩家显式有理例。
- `archives/weighted-congestion/state/计算/类前沿与同类时钟的精确核验--计算.md`：稳定ID `weighted-congestion/class-front-exact-audits`；六程序真实重放、19件原件及全部差异、三固定例的不同证据身份、可移植重放入口。
- `archives/weighted-congestion/state/审查/类前沿对象的重构与修复范围--审查.md`：稳定ID `weighted-congestion/class-front-reconstruction-review`；三报告各自受审范围、先后读序、实质coverage修复、freeze/规范源码/JSON区别及审查后的追加节边界。

## 证据与实际检查

完整证据目录：`archives/weighted-congestion/tools/evidence/class-front/`。

- `provenance.json`逐项保存8本批源、11复现/比较依赖的稳定源ID、两冻结提交完整路径、原SHA256与保存位置；19件226952字节逐项核对inventory匹配。
- `original/`保留完整原稿、三份审查、六份源码、两份显式输入、六份冻结JSON及后续线性全状态正文。
- `replay/manifest.json`保存六份原程序准确执行命令/源hash/stdout hash/解释器/耗时；六份实际均exit0、stderr空。
- `replay/comparison.json`逐叶保留所有差异，六份数学输出完全一致。第一对旧报告wrapper和`result`分开保存，没有抹掉版本元数据。
- 编排器首次exit1是分类器遗漏`$.command[1]`元数据叶，而非数学失败。已修正比较分类、仅对保存输出重算比较，记录于`replay/comparison-correction.json`；未无理由重复六个运行。
- `replay_class_front.py`为可移植入口，默认新建`replay-new`且拒绝覆盖已有目录/冻结证据。实际六次已由该入口首次执行；修复分类后未再次运行整套。
- 六正文42个本地链接存在，ID互异；七份Python文件AST检查通过。数学断言由原六程序实际运行承担，未增写与实现镜像的测试。

## 当前状态与关系判断

全文比较后续`source:68fad804ec5946cb296f77dc5b336308a66abf12:research/current/weighted_congestion/linear_degree_allstate_lower_bound.md`：p≥2^20的正有理纯p次族每态严格p/10改善，已否定固定C的全类Cd/ln d存在保证。本批源与三审查的旧OPEN均降为历史，不重开原目标。

关系按实际数学判断保留在正文：窗口关联提供相位表示；相位表支持端点检测；24资源反例否定strict sweep自动给全部front出口；64资源新基体加局部单调引理否定指定compiler普适性；条件接口另要求全部front出口，故不与两反例冲突；后续健康族专门证明此前提并在原次数支付时钟预算，才给全状态结果。未改共享README或图，阶段三另建有解释超边，不能自动导入旧图。

外审、全球新颖性、最优倍率及最小真实锁定次数均未认证。11件依赖已读、保存及适当实跑，但本批仅对以下8源done，不因引用完成其他owner的分母。

## 回执和待Boss串行动作

回执：`cleanup/workspaces/Boss4/class-front-next-receipts.json`，含8条integrated记录，targets仅指六正式正文。

8源ID：`31f2dfccd607374a022b`、`f7d05b0888fede0876c9`、`6c6f1d321eee210eebb8`、`9ce5607f957b42f0d73e`、`cf0c93fbb5809f08e365`、`dc20590f6e2d643440d6`、`0e490a5f694563d38ca4`、`05b9b685db9f2fe4c1db`。

建议一个checkpoint明确包含上述六正文、整个`tools/evidence/class-front/`及本delivery/receipts。确认pushed后，Boss按回执done。子代理未自行claim、done、sync或Git写入；可接下一批完整实质清洗。
