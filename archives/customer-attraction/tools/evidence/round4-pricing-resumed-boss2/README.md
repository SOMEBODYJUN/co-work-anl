# 保交叠全型、常锚点跨族定价与61点

本包负责 `round4_pricing` 的13个冻结源。全部六个原py完整阅读，七个JSON版本完整语义读取；两份cross CG逐字节相同，只保一份准确原字节。来源ID、完整双提交、blob、SHA、字节及复用位置在 [source-manifest.json](source-manifest.json)。复用准确已有 `full_pricing.py`、125497B旧60点，不额外堆一份同字节原件。

正式正文：

- [全型与常锚点程序合同](../../../state/程序/五人保交叠全型与常锚点跨族定价的精确恢复合同--程序.md)：557/717域、矩阵、160加法行、发现阈值、浮点选基与精确判号、六个入口、输入和副作用。
- [717轨迹与61点](../../../state/计算/五人七百一十七行浮点轨迹与六十一原子精确点--计算.md)：全部12步695列、前67旧exact_mass不等于当前LP质量、558源状态的61有理点、717精确可行与原额外分离报告。

## 完整阅读与复用

[完整可逆CG投影](complete-cg-field-projection.json) 保所有top-level字段，将695个原子的五结构字段按106/10/17/21/41项完整字典和695条索引记录分解，保67条附带exact_mass。一次重构逐值等于整份JSON，不只保摘要或非零项。全部695浮点质量、61正项与634零项、50保存乘子、12步历史及717行名均实际读取。[字段语义记录](complete-field-reading.json) 另保所有原始点meta/basis、全部原子与CG的准确映射或独有结构、所有slack名字/精确解析及已有核验的对应关系。

旧60点557个保存slack逐值与成熟 [60点完整输出](../shared-matching-and-full-pricing-primary/new-shared-matching-and-60point-check.json) 相同，本次0重跑。67点与51权原件已恢复，父方另外执行原父审和原独审；见 [557双审恢复](../../../state/审查/五人五百五十七行双证书的原审计恢复与认证范围--审查.md) 及 [独立运行包](../round4-audits-resumed-boss2/README.md)。本包不把父方两次执行回填成自己的运行。

## 唯一新增数学执行

[check_fixed_61.py](check_fixed_61.py) 成功执行一次，加载canonical旧437定义前缀，仅给新61输入求值；不执行其后部成熟审计。10末位、110同族及160常锚点跨族系数在新入口按字面索引重建。结果 [fixed-61-exact-check.json](fixed-61-exact-check.json) 包含全部717精确总slack、61质量及域摘要：W1、O约2.0421195368768834、717非负、71零行，与原保存717值逐一完全相同。新末位12200项，pair三索引411750项。

原生成CLI、优化器、原exact恢复器、全型price、joint/运输执行均0。没有重新运行原separate报告中的9882/13420检查；其30负联合末位行、220pair全非负及空“两component皆非负”字典保持原内部报告身份。既有通用必要性来自正式引理/定理，不由有限检查次数认证。

## 直接依赖和可复现边界

[dependency-manifest.json](dependency-manifest.json) 绑定canonical程序/证书、partition、offdiagonal、旧2183列CG及joint/pair原实现，分别标实际阅读和执行域。7458B `frozen_pair_reoptimization.py` 经父方正常冻结出口恢复，在 [related](related/frozen_pair_reoptimization.py) 保完整原字节和show来源；本13源未为其代done。其精确消元函数全读，未执行其冻结64列优化。

canonical证书只作为运行输入阅读437行名、首原子及64原子的五结构字段；没有声称本包重新审完其全部大证书。60点1581列发现文件未作为独立输入恢复；61点558列报告没有源SHA和basis。两份自含有理点可以直接核验，缺原发现状态不妨碍此事，却限制原LP轨迹逐字节重放的断言。

程序依赖原祖先布局及NumPy/SciPy；不在原存档目录启动会覆盖固定文件名的发现器。`separate_cross_point.py` 没有main guard，导入即计算并写报告。本包只是保存并说明原程序，没有将其导入当作只读动作。

阶段三关系候选和各参与对象的准确作用已在两正式正文末段写明，未提前造全仓超边。当前六人有限单位客户、完整有序历史纯SPE半覆盖仍开放；这些五人必要点的O不是未经证明的真实OPT，且没有完整SPE实现。
