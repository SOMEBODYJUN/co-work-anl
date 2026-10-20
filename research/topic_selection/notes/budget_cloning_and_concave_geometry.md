> 统一候选编号、当前状态和本轮最终判断以[候选比较](../BATTLE.md)为准；本文保留来源与推导过程。

# BN-CLONE-v1 / BN-SEPARABLE-v1：两项Nash方向实质试攻

日期2026-10-20。来源：Becker–Fries–Greger–Segal-Halevi, *Efficiently Computing Equilibria in Budget-Aggregation Games*, arXiv:2509.08767v3，2026-02-24，§8末与§9。来源提的一般方向为A/B，以下限制对象是我们派生的C。未完成相关文献查重，不能认作新定理。

## 1. 凹性并不足以保证cloning保持均衡：精确反例

3个项目，总预算1。玩家a、b各预算1/4，偏好相同：

`u(delta)=min(2 delta_1+(3/2)delta_3, 2 delta_2+(3/2)delta_3)`。

玩家c预算1/2，偏好 `u_c(delta)=delta_3`。

令a全投项目1、b全投项目2、c全投项目3，总分配 `(1/4,1/4,1/2)`。两clone效用均5/4。a的任何单方策略z，z总和1/4、非负，其第一项线性分支至多

`2 z_1+(3/2)(1/2+z_3)≤2(1/4)+3/4=5/4`。

所以u不可能增加。b用第二项得到同样证书。c已经把预算全投唯一在乎的项目，故该profile是NE。

把a、b合并为一个预算1/2且保持相同u的玩家。该玩家把预算全投项目3，总分配变为 `(0,0,1)`，效用3/2>5/4。因此cloned game的NE合并后并非NE。

这里u连续、凹、非负、单调，且是两个非负线性函数的最小值。排除“一切concave preferences自动满足作者Lemma8.2”的自然强猜想。它不否定Leontief或binary symmetric结果。3项目、2线性分支已经足够；没有证明这在所有合理模型下的最小性。

## 2. 可微凹utility确实保持cloning

**Lemma.** u在总分配delta处可微且在simplex上凹。若预算B的同utility玩家拆成任意多个正预算clone，cloned game的某个NE在delta处使这些clone分别采取y_a，则把它们合并为 `y=sum_a y_a` 后，该玩家仍为best response。

**证明。** 记g=gradient u(delta)，gmax=max_x g_x。每个clone的simplex最优化一阶必要条件给 `supp(y_a)⊆argmax_x g_x`，因为每个clone共享同一总分配delta、同一gradient。合并后的y也仅在argmax g上支出，故对于任意总预算B的z，`g·(z−y)≤0`。凹性给 `u(delta−y+z)≤u(delta)+g·(z−y)≤u(delta)`，所以合并后不能改善。其他玩家未改变总分配及自身策略，仍为best response。证毕。

价值边界：此lemma是标准KKT的一页推论，不能单独成稿。与反例共同指出真正边界是**同一个总分配处不同clone可用不同active subgradient锁住自己**。有潜力的完整题是对 `u=min_{r≤R} a_r·delta`（a_r≥0）给必要充分的cloning不变性、有效识别及最小禁形；这需要解决一整套active-gradient cone兼容性，而不是再次证明光滑情形。

## 3. 非binary共同可分凹偏好：一个凸规划接口

**Theorem (已证明、文献新颖性未查).** 每名玩家i预算b_i>0，总预算1，策略x_i∈b_i simplex。令

`u_i(delta)=sum_x v_ix f(delta_x)`，所有v_ix>0，f∈C²([0,1])、f'>0、f''<0。

定义 `G(t)=integral_0^t log f'(s) ds`，以及

`P((x_i))=sum_x G(delta_x)+sum_ix x_ix log v_ix`，delta=sum_i x_i。

那么profile是NE，当且仅当它是P在预算product simplex上的全局最大点。P凹；所有NE具有相同aggregate delta。

**证明。** u_i对自身策略严格凹于aggregate方向；simplex KKT必要且充分。原utility的第x边际是 `v_ix f'(delta_x)`；P的相应边际是其log，即 `log v_ix+log f'(delta_x)`。log严格递增，因此两者给完全相同的“正支出坐标边际最大”条件。P关于全profile凹，因为G''=f''/f'<0，加上线性项。因此所有玩家各自的KKT条件合在一起就是P全局最大化的KKT。若两个P最优点aggregate不同，其中点使sum_x G(delta_x)严格增加，而其线性项取平均，矛盾；故aggregate唯一。证毕。

这说明作者§9“非binary valuations”方向不能不加辨别地当作难题：这个共同f、positive valuations、凹光滑子类有直接凸规划。没有声称精确polytime：log系数/G的表示、oracle和所要求精度必须给出；一般f只是oracle时没有有限表示保证。若f(t)=log(t+eta)，P是熵型凹规划。更像完整成果的延伸是：识别允许player-specific f_i的最大自然类，并给可计算数值表示、误差到NE的转换及不满足结构时的失败边界。先查ordinal/regular potential、aggregative games和Fisher-market文献覆盖。

## 4. 来源位置与状态

- 原文v3 §8 Lemma8.2 / Thm8.3后：作者问哪些utilities可保持cloning，并问weighted Leontief均衡能否polytime计算。
- 原文v3 §9：作者建议nonbinary separable preferences、其他lp metrics、均衡选择与动态。
- 上面反例与两项证明为本轮研究者推导；一般cloning分类未解决。
- https://arxiv.org/html/2509.08767v3

## 5. 点wise刻画与按线性pieces参数的有效识别

这部分由根部提出shared-subgradient的几何观察，本子任务推进有效识别。对象限定 `u(delta)=min_{r≤R} a_r·delta`，a_r为非负有理向量；外部玩家可有任意utility。所有预算/分配均可取有理。

**Exact Statement / universal property C.** 对每个正整数D、每个1≤k≤D、任意有限个其他玩家及其正有理预算（总和1−k/D；k=D时允许没有其他玩家）、任意这些其他玩家的utilities，考虑k个utility均为u、预算**均为1/D**的clones与这些外部玩家构成的budget-aggregation game。对该游戏的**每一个NE profile**，把这k个clones合并为一个预算k/D、utility仍为u、策略为原k个策略之和的玩家；要求所得profile仍为NE。这里不要求“存在某个可合并NE”，也不允许只证明任意特殊预算。识别输入为A的二进制有理编码；算法输出该universal property真假。作者§8提出的是一般utility分类A，本矩阵对象及其识别问题为研究者C。

记delta处active rows集合I，凹superdifferential `P_I=conv{a_r:r∈I}`。对某个clone的正支出support S，polyhedral凹最优化KKT说明它在delta处最优，当且仅当存在g∈P_I使 `S⊆argmax_x g_x`。不同clones可以有不同g。

固定delta，定义

`U_delta={j: delta_j>0 and there exists g in P_I with j in argmax g}`。

**点wise定理。** 对所有能够产生同一delta的clones及外部环境，合并都保持NE，当且仅当存在一个g∈P_I，使U_delta全部属于argmax g。

**充分性。** 任一最优clone的support包含于U_delta；共同g因此对合并support满足KKT，合并最优。

**必要性与等预算实现。** 若不存在共同g，U_delta非空。对有理delta，选整数D足够大，使eta=1/D<min_{j∈U_delta}delta_j且|U_delta|/D<1。对每个j∈U_delta放一个预算**eta**、纯投j的clone。每个clone因j∈argmax某个g_j而最优。剩余向量r=delta−eta·1_{U_delta}由一个预算1−|U_delta|/D的outsider提供，其utility取线性 `u_out(delta)=sum_x delta_x`，系数全为1，弱单调；在总预算1的simplex上所有策略同样最优。合并玩家support正好U_delta，没有共同supergradient，KKT必要性说明它不是best response，从而存在严格有利偏离。

若要求整个cloned game都像作者Definition8.1一样每人预算1/D，把上述outsider也拆成D−|U_delta|个utility为sum_x delta_x的等预算clones，并把r任意分解成这些1/D-simplex向量；线性utility使它们全部仍最优。合并这些outsider clones也不影响证明。所以这是原文等预算cloning意义下的真反例，不靠任意非等clone预算或非单调外部偏好。

一般real delta若违反条件，其active cell和support约束均有理，可由本节算法的有理witness构造替代，因此universal property的失败可在有理输入中实现。矩阵A若要求每项严格正，可对所有行统一加上正的all-ones向量；在总预算simplex上utility只加常数，所有argmax-gradient条件不变。

这等价于可实现maximizer-support族对union封闭，但有效识别不能止于这个重述。如下可消去所有delta和clones的量词。

**Theorem（fixed-R识别）.** 给定R×m非负有理矩阵A，判断上述universal property C，可以用 `2^R poly(m,R,input bits)` 时间完成；若失败，可给有理counterprofile及LP最优性证书。这里poly次数不依赖R；LP运算用标准有理多项式算法。输出反例时D用二进制记录，outsider的等预算clones可以压缩表示；**不声称在poly位长时间显式打印可能有指数多个的D名clones**。

**算法与证明。** 枚举非空I⊆[R]。令C_I为simplex中active set恰好I的相对开多面体cell，即 `a_i·delta=z`（i∈I）、`a_r·delta>z`（r∉I）。对每个坐标j，解LP：

`delta≥0, sum delta=1, 0≤eta≤1, a_i delta=z (i∈I), a_r delta≥z+eta (r∉I), delta_j≥eta`，最大化eta。

最优eta>0恰表示C_I中有一个delta使delta_j>0。记这些坐标构成J_I。若J_I空，C_I空，跳过。每个j∈J_I取一个正eta可行witness delta^(j)，平均所有witness得到delta*：它仍在C_I，而且对所有J_I坐标同时为正。注意strict outside-row inequalities的有限平均仍strict，这是避免枚举2^m support sets的关键。

再对每个j∈J_I解LP：`g=sum_{r∈I} xi_r a_r, xi≥0, sum xi=1, g_j≥g_s (all s)`。可行坐标集合为U_I。最后解同一凸组合LP，要求对所有j∈U_I、所有s都有g_j≥g_s。

若最后LP可行，它的共同g覆盖这一cell内任何delta的U_delta，点wise定理给cloning不变性。若不可行，上面delta*在所有J_I坐标为正，故U_delta*=U_I；点wise必要性构造有理反例。枚举I穷尽所有可能active sets，所以算法正确。每I需要O(m)个有理LP，变量/约束均poly(m,R)，总时间如上。严格正的eta可以用有理LP最优值精确判断；**浮点solver的tolerance不是这个理论算法的充分实现**。

此定理使R=2、m任意的识别已可完成。因此N3最小主目标应升级，不能继续把“两pieces可识别”当尚未攻下：有价值剩余是消去2^R、证明一般R的tight complexity、给可读面结构/有限禁形，或用这一性质推出新的weighted均衡算法。

**两资源边界。** 任意有限polyhedral concave u在m=2时都保持cloning：若两个坐标分别可作为supergradient最大值，凸superdifferential中g1−g2可取非负及非正，因此可取0，同一个g让两坐标并列最大；若只出现一个最大坐标更直接。配合第1节三资源反例，得到最小dimension分界。该维度结论源于根部几何观察，原文v3的§8没有给出此声明；§2.3谈的是一般两项目exact NE的计算，不能混同。

**价值边界。** 有效识别定理仍可能是标准polyhedral/KKT枚举的常规推论；未完成文献查重。它至少提供严格输入输出接口、非trivial合并witness步骤和可复用反例证书，不应凭此自动升级为足够成稿。
