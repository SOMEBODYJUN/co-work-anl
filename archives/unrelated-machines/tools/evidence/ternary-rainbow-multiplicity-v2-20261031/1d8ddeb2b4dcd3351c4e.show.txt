# 三叉树二叉彩虹的全局叶重数复杂性门槛：仅陈述

ID `UM-PRIVATE-TERNARY-RAINBOW-MULTIPLICITY-THRESHOLD-v2`。root的新量词，未把原无重数限制的v1倒改。root已有推导，本文件不含证明，供只见陈述的独立重构。没有修改canonical或声称主目标完成。

对象仍为显式完整三叉rooted树T，高h≥1，全部叶深h，每internal恰3children；显式叶颜色χ，binary颜色ID可重复。满binary子树含原root，每active internal恰2children，叶仍深h；rainbow指所选全部叶颜色单射。现在以整个输入T为单位限制每个颜色的实际全局出现次数，不是只在选中见证或某局部子树计数。

精确结论：

1. 若每个颜色在整个T出现至多2次，则对任意h，必存在满binary rainbow子树。该项为存在性，不先声称已实现一般多项式寻找程序。
2. 即使每个颜色在整个T出现至多3次，判定是否存在满binary rainbow子树仍NP-complete。存在从所有显式3SAT公式Φ的确定性many-one位多项式归约，SAT iff输出tree有该子树；对输入长s，输出h≤Clog₂(s+2)、完整树与颜色编码长≤(s+2)^C，C为与Φ无关的绝对常数。每个原色或辅助色都须满足≤3，不能把高重数控制色视为不计数的别名。空/常量输入合法映射，短clause与binary变量ID正确处理。
3. 两项共同给这一叶重数上界的精确复杂性边界：上界2时所有输入YES，上界3时NP完全。若要说无poly判定器另用P≠NP；NP-completeness本身是归约/成员结论。
4. 按v1相同完整普通P（internal私有；单端time1 root pin；每tree-edge job父端1/3、唯一child或叶颜色外机time1；其余∞）转换，YES actualOPT≤4/3，NO actualOPT=5/3，任意<5/3实际σ可poly提取binary rainbow。第2项中每个外颜色resource的eligible leaf jobs总数至多3，每个非pin job恰两端，pin单端。仍只是5/4比值，不是near2困难性。

依赖可用标准3SAT NP-completeness及既有raw叶q子可加性；新的全局重数3归约必须重证，不能引用旧Rigid/Dead的无限重数模板。无实现/有限运行、外审、新颖性或独立论文价值认证。结构性sharp门槛不等于UM-TARGET-v1一般正反解答。
