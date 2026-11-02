# 续局菜单、背景利润与逐人净缺口的十源恢复

10个primary共31777B，original平铺保存完整原字节，source-manifest.json保源ID、完整原path、大小/SHA、blob和两个冻结commit。related/iterative_search.py为额外实读6661B实际导入依赖，来源b1883658b123519c0645、SHA256 d5197be034395270aa3708bcee14b7aff307c2bd7ef035edba1d5a7328760413；该相关源不在本10项receipts中。

三份自足对象：

- [同向帕累托剪枝有限障碍](../../../state/障碍/过去租金与未来利润同向帕累托剪枝的有限障碍--障碍.md)：完整四输入、两方向、根菜单及支配关系，四份全历史纯SPE。
- [固定剩余人数背景两发现器](../../../state/程序/固定剩余人数背景利润的两份精确发现器--程序.md)：V_r(b)最坏剩余利润、F_r(b)最佳静态利润、保持r的加过去比较；没有保存输出，不新跑随机。
- [逐人净缺口浮点地板记录](../../../state/程序/逐人净缺口地板的三份浮点续局锥记录--程序.md)：主程序/真实Search合同、38日志/221质量、W1目标、阳性重新整数SPE求解与阴性证据缺口。

## 唯一完整新固定检查及一次修复

```sh
python3 -I -B archives/customer-attraction/tools/evidence/continuation-floor-resumed-boss2/check_four_pareto_inputs.py
```

该入口只用标准库，不import任何原文件、规范solver、NumPy或SciPy。只取三份Pareto报告保存的四个固定客户表，独立进行精确全集递推和两方向剪枝，不重扫原2000/4000/5000随机配置。为每个完整最坏根结果重构一棵完整有序SPE并逐单位客户验全部比较；四例303节点、1430含自身比较全过。客户数11/12/17/21、五或四个主题均非空且两两不同，原集合模型直接适用。

首次尝试在第一个例子形成profile时，未占用主题利润漏0守卫导致Fraction(1,0)，尚无完整固定例输出；事件001记录失败及未捕获的旧代码SHA，不冒造其指纹。补正q[a]=0返回有理0后，事件002成功，记录当前代码/完整输出SHA和真实范围。两次尝试、一次完整成功，原main/随机试验/优化器均0。

完整结果four-pareto-cases-and-floor-consumption.json保四例全部根集合、原/压缩行动地板、全部八次实际剪枝事件及向量、四份完整动作与逐节点余量和真实OPT。另消费三个floor JSON的全部38日志、221质量及原字段一致性；只读/统计这些浮点数据，没有重建其LP矩阵或赋予精确点身份。

## 现成依赖与原入口边界

背景和frontier原码依赖真实customer_attraction/包；floor还依赖related Search、tests/audits/customer_attraction_strategy_lp.py及cone_attack_credible_variants.py。规范已归档原件位于`../strategy-cones/original/`，本次只读取相关合同，不重新复制或执行成熟350原始/348对偶。

original平铺位置不是原相对布局，不能据此声称原CLI可直接运行。尤其background_monotonicity.py没有main guard，import即开始最多10000次随机；其余原脚本的发现main也不在本次运行范围。floor阳性闸门会重新求新整数客户的全部SPE，而阴性文件无动作/J/dual；本包未物化一个不存在的精确反例。

所有输入/量词/结果与当前运行范围在正文及delivery逐项分开；成熟背景9→11、覆盖13→12、高背景半利润及逐人地板相关对象仅作实际比较，均无重复数学运行。
