# density-share-next交付

12源正式claim由Boss执行，pushed提交 `5741b4df90b822f7b09842c68b8871109fbd6395`。12源主稿、审查、程序、全部报告数据均已完整读取并逐SHA-256核对。子代理未执行任何claim/done/sync/commit/push，未改共享README、图或他人正文；当前全部成果已在共享工作树，可由Boss集中checkpoint确认pushed后用回执done。

## 明确交付路径

- `archives/weighted-congestion/state/归约/可选空动作的潜在用户密度填充--归约.md`
- `archives/weighted-congestion/state/定理/高次费用最小潜在权份额势--定理.md`
- `archives/weighted-congestion/state/反例/正负载零价阶跃的均衡投影失效--反例.md`
- `archives/weighted-congestion/state/审查/密度填充与高次份额的独立审计范围--审查.md`
- `archives/weighted-congestion/tools/evidence/density-share/`
- `cleanup/workspaces/Boss4/density-share-next-receipts.json`
- 本文件。

## 实质数学保全

padding归约对任意原游戏、任意有限正权padding多重集、每个有限实alpha≥1，完整保留每个增广均衡的原玩家投影、原玩家全部真实偏离成本相等、原均衡全空提升与成功倍率集合相等。最小密度条件必须是occupied-weight区间，不是几何区间非空；同一padding对所有R>1同时有效。新增非零资源动作严格被空动作支配，所以不是提高活跃密度或强制参与条件。原空支持资源可保持空，也可另补L名权1用户。

高次份额定理完整保留局部k_e/q_e/lambda_e、零/常数/不可用资源lambda=1、常数用实际人数计势、保留资源的强负项、所有单方局部最小点保证、共同q弱式、纯d次反例的strict小份额必要条件、alpha>1的log估计、固定有限正权向量且最低正次数趋无穷的一致趋1结论。它允许资源/策略/系数变，却不允许权向量变；只有最高次数增长且低次项固定不适用。

阶跃反例只否定任意非负非递减费用下的投影/成本相等断言：正负载零价让新增玩家活跃并掩盖原偏离。该例原游戏仍有精确均衡，未误称其存在性等价失败，也未反驳多项式归约。

两对象实际关联已解释：padding可以降低潜在q而逐倍率保持均衡，所以高次“小q”必要条件不能自动反推实际困难或充分反例。已全文比较MODEL、weight_density主稿、linear全状态主稿以及相关正式支持势/幂矩桥/尾部冻结/固定权十四资源失败。旧OPEN由每个d≥2^20的全状态d/10下界更新；未将这三比较依赖顺带done。dense_bands旧路径不在冻结inventory，只记历史应用提示。

## 实际复现与覆盖区别

原样复跑命令：

```sh
python3 archives/weighted-congestion/tools/evidence/density-share/replay_suite.py
```

四程序完整并行执行，Python 3.12.14，全部退出0，四个新JSON与对应冻结JSON逐字段零差异。原件不覆盖；驱动在隔离目录使用三个原脚本的--generate及density独立脚本stdout，保留输入程序、新结果、stdout/stderr、命令、源码hash及比较报告。全部算术是Fraction。

- density作者：4固定游戏×5倍率，500个增广状态—倍率组合；380项只计增广均衡上的原玩家偏离费用相等检查。
- density独立：5游戏×5倍率，1280个状态—倍率组合；25组均衡数、L=1/2/4/17的20组填充大小，所有占权连续类块与零资源活跃见证，另step边界。
- share作者：5固定+96种子17输入，共101游戏、4011状态、49376偏离、105391逐资源检查、103全局最小状态、5782零偏离成本、32230保留资源比较；全部101报告case及有理lambda/alpha已实读。
- share独立：3固定+200种子20261015输入，共203游戏、2426状态、24340偏离、3493次严格改善、210全局最小状态。此代码只核共同q/k；更强局部lambda_e扩展由作者代码和独立解析攻击覆盖。

两share程序都只枚举全局最小点；所有单方局部最小点结论由严格势下降一般证明承担。高次主稿规范hash与独审尾注c38...完全一致，f010...仅对应删尾空行前的数学等同版本；density审查旧主稿hash与当前迁移版hash分开记录。历史图计数、检索未见同公式及内部多代理审查均未升级为本树新图检查、全球新颖性或外审。

## 自检与关系接续

已检查：12原件hash、3全文比较依赖hash、12回执ID唯一/targets存在、4正文YAML必需字段和稳定ID、所有相对文件链接存在、无行末空白、四重跑全部JSON零差异。未执行共享图构建。

第三阶段关系建议来自实际推导：padding归约到密集子类成功倍率集合相等；多项式正点严格正与step反例的边界关系；高次资源删除幂差到局部势的推导；高次势到必要小份额/固定向量统一极限；padding说明小潜在q不充分；有限程序分别作实现/有限检查。最大K权密度和潜在支持r保证均相容，不能同“最小占权密度”合并；尾部冻结的旧高次倍率比较必须保留共享非零x^d条件。Boss应在正文pushed后再提交12条integrated回执。
