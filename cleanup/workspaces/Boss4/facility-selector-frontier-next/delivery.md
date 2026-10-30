# facility-selector-frontier15 交付

本批15源168742字节完整实读，12新正文；19原件220116字节（其中2个纯比较依赖44031字节）。没有Git/claim/done/sync操作，没有重跑旧批审计。

正式认领已由Boss推送：`aa3a89ff50291360dc1f905a1bf02cce54edcc58`。本文只陈述本地交付，保存及done由Boss串行处理。

## 正文（逐源targets）

- `archives/facility-games/subarchives/common-many/state/归约/全局均衡选择的精确优化困难与局部搜索上界--归约.md`
- `archives/facility-games/subarchives/common-many/state/算法/重数分组范围证书与轻客户分量选择--算法.md`
- `archives/facility-games/subarchives/common-many/state/算法/共同锚点嵌套选项的降序列表均衡--算法.md`
- `archives/facility-games/subarchives/common-many/state/算法/早开中心星与同边等重有向路径的单次迁移--算法.md`
- `archives/facility-games/subarchives/common-many/state/算法/原池双装箱证书与盒外纯均衡续局--算法.md`
- `archives/facility-games/subarchives/common-many/state/反例/两种轻权的下盒势极小值溢出族--反例.md`
- `archives/facility-games/subarchives/common-many/state/反例/仅向低重数修复的强制上返陷阱--反例.md`
- `archives/facility-games/subarchives/common-many/state/反例/固定贪心均衡的坏选择与静止超帽边界--反例.md`
- `archives/facility-games/subarchives/common-many/state/算法/客户类型支持整数规划与有限目录选择--算法.md`
- `archives/facility-games/subarchives/common-many/state/问题/一般异权盒选择的统一位复杂度目标--问题.md`
- `archives/facility-games/subarchives/common-many/state/算法/等重轻客户下盒流与无约束细化--算法.md`
- `archives/facility-games/subarchives/common-many/state/计算/贪心选择器六套原审计的精确复现--计算.md`

## 数学处置

精确全局lexmax和真实贪心盒势优化的强NP完全范围保全；同一归约族存在容易精确均衡，避免误报因子二搜索困难。给四预算的显式PLS上界，未声称PLS难或多项式迭代。各输出子类保完整输入、排序、原选项NE、盒和单源消失/默认续局合同；RANGE与MAX作为不同外部调度条件，不以有限严格回复升级。

保早开星/同边等重路径、锚点嵌套、双LPT盒外纯NE及原池重置接口；完整保静止超帽、任意/最重修复顺序、固定布局lexmax/势极小失败和两轻权无限族。类型支持ILP保固定维导入、FPT与XP边界；用后续一般盒存在更新指定冻结的合法贪心子类可行性，非任意占用。旧下盒流与后续无约束Ψ最优赋值集合相同；追加内部项恰零仍失败的异权端点比较，不声称新覆盖等权模型类。一般统一位多项式目标继续开放，方法路线自由。

## 真实运行

六原入口各一次全部exit0、stderr空。double_lpt的__main__只有triangle=True一例，核16实际偏离，最大移动者收益110；base/split函数分支完整读但未执行。uniform_flow仅枚举四分配，没有流增广执行；two_light的真实n为45/50/100/1000；其余三者各按原单例。5条PASS stdout及double完整JSON已保存；没有冻结历史输出作全字段零差异比较，不伪造基线。两个旧repair_order原件仅为heaviest import依赖，未调用其audit。

证据目录：`archives/facility-games/subarchives/common-many/tools/evidence/facility-selector-frontier/`。`provenance.json`列完整source commit/path/hash，`original/`17源恢复实际运行布局，`related/`两比较原件，`replay/`保存真实命令/时间/输出，`output-review.json`保实际范围，`final-verification.json`核19原件、8 Python AST、链接、稳定ID及旧12正文哈希不变。未读取到Lenstra作者PDF（两次检索工具均isError/content空），按标准固定维ILP合同导入；MAX/RANGE沿已存实际边界保持条件。

## 回执和关系

逐源15条：`cleanup/workspaces/Boss4/facility-selector-frontier-next/semantic-receipts.json`，均integrated，targets仅正文。每条有完整实读、相关比较、独有内容去向和实际处置理由。计算正文列主稿每个语义单元的去向；没有把未完成数学退休。

新对象的推导、反例、子类、实现与有限检查关系已逐项在正文解释；未改共享README/图或他人文件，第三阶段再做超图。此前complement-reset12的7正文哈希逐项不变。下一批只准备available元数据，待Boss正式claim后再全读。
