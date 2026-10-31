# 私有完整三叉树的二叉彩虹子树：精确陈述先行

Candidate ID：`UM-PRIVATE-TERNARY-RAINBOW-BINARY-SUBTREE-NP-COMPLETE-v1`。只给精确对象、结论与原P定义，不给构造证明。作者为内部子研究者 pcsp_occurrence，已有候选推导，不冒称作者盲审。root要求先冻结本陈述再独立重构；证明另文件保留。未改仓库，不登记Work，不升级UM-TARGET。

## Objects / Domain / Quantifiers

输入一棵显式完整 rooted ternary tree T，height h≥1，所有叶深度均h，每个internal node恰有3个children。只给叶着色：χ:L(T)→C，C为有限非空显式颜色集合；允许重复颜色，包括同一颜色多次出现在同一child subtree。内部节点无颜色约束。颜色ID用有限二进制字符串给定，总输入长度包括完整树和所有叶颜色。h可随输入增长，不是固定常数；完整树的叶数3^h，因此h=Θ(log |T|)。

full binary subtree F要求root为T的root，每个active internal node恰选T的2个children，全部F叶仍在原深度h。F rainbow当且仅当χ在其恰2^h个叶上单射。不是任意大小connected subtree、不是仅root到叶路径色异、不是所有颜色至少出现一次。

## Exact Claim

1. 判定是否存在这样的full binary rainbow subtree是NP-complete。
2. NP-hardness可由显式3SAT公式Φ作确定性多项式many-one归约。若Φ总编码长度为s≥1，输出完整三叉树满足h≤C log₂(s+2)，完整显式规模≤(s+2)^C，其中C为与Φ无关的绝对常数；Φ可满足当且仅当输出树存在full binary rainbow subtree。颜色可用多项式位长的整数ID，不使用隐式指数树、oracle或随机化。
3. 任何YES见证可按完整T大小多项式时间核验；构造不声称对YES未知输入多项式寻找见证。

等价地，q(T,χ)=max{r∈{1,2,3}: 存在rooted full r-ary rainbow subtree至深度h}满足q≥1；区分q≥2与q=1是NP-hard。这个合同只到k=3、strong k−1=2、weak r=2的可行性，不是任意δ的near2 soundness，不由(2/3)^h叶比例下降推导uniform branching gap。

## 明确的原UM矩阵推论（非主目标突破）

由该树按以下明确规则给出全部P。机器为每个internal node一台私有机器，以及每个实际颜色c一台resource machine R_c；所有这些机器互异。任务如下：

- root pin一枚，只能在root internal machine执行，time1。
- 每条parent到internal-child的树边一枚job，在parent端time1/3，在child端time1，其余∞。
- 每条parent到leaf ℓ的树边一枚job，在parent端time1/3，在R_{χ(ℓ)}端time1，其余∞。

每job至少一条finite边，无其它任务/预载，有限时间均为1/3或1；重复颜色的leaf jobs仍为不同任务，只是它们共享同一resource machine。

此P在树有binary rainbow subtree时存在具体Cmax≤4/3调度；若树无binary rainbow subtree，则真实OPT=5/3。对所有树均有具体Cmax≤5/3调度。给定实际Cmax<5/3完整调度，可确定性多项式提取binary rainbow subtree。因此该特定私有noninjective、输入增长height类上的(4/3,5/3) promise具有NP-hardness，所给间隙比仅5/4，弱于一般UM既有常数困难性；不宣称原创或一般near2困难性。

## Dependencies / Evidence / Scope / Status

依赖标准3SAT的NP-completeness。完整归约、颜色重复的局部逻辑、equal-height补齐及总规模证明尚待独立审查；本陈述不引用Maximum Colorful Subtree或Group Steiner的不同目标困难性作替代。

暂未做实现、有限枚举或运行声明。新颖性未认证。若后续改k、strong/weak branching、叶颜色量词或P的处理时间，则另立精确版本，不能以此已核k3可行性替代。UM-TARGET-v1保持OPEN。
