# 逐资源畸变菜单规范正文的作者全文读后审查

审查对象：`research/current/unrelated_machines/resource_distortion_flat_menu_rounding.md`，实际全文读取1–7节；冻结SHA256：`0da64ce52e3d85666aed7c3a156f68c09a699418e584512d851d82a02c3b05c5`。本记录的审查者已写过完整bonus增广版本、读过源定理并与root交换过Exact，因此这是**实际全文read-after**，不是blind/statement-first审查；不替代另一审查者的独立Exact重构。

## 结论

所读版本未发现仍成立的数学fatal objection。正式后端来自Cheng–Mao 2019 Theorem1，而非DRZ旧4结论。规范正文把作者草稿中真实bonus增广改为直接baseline item，保留同一实际OPT和κ比较，而且不需要新增调度jobs；该变化正确。

一项非fatal形式细节已发给root：正文允许每固定**实**α>4，§6却写直接检查峰值是否不超过`2−1/(ακ0)`。若α或κ0为任意固定非有理实数，这不是默认可精确计算的有理阈值。应在YES上界与NO下界之间硬编码一个固定有理separator，或将这项算法描述的常数限定有理。固定参数存在性、隔开的promise和定理(2)均不受影响。此记录不提前声称root已修改。

## 直接baseline与bonus稿的逐项对照

1. 规范V的效用是`b_x+received original p`，其中`b_x=1−W_x`，不是旧未归一化的无baseline V。状态总质量0时V1、actualOPT1正好匹配。作者bonus稿的V则是增广对象V；两个值相等，但规范稿更直接。
2. 每个baseline item只对其state player有正值，不与任何其它player竞争，固有值b_x满足restricted合同。将它加到真实allocation效用中，不是给原调度机器虚加负载或免费释放原任务。
3. 到lower restricted实例时，real值取同资源的最小**正**private值，零incidence保持零/不想要。baseline和dummy都可保原值：κ≥1使它们也满足比较下包络。源标签/状态数无须有界。
4. 从任意lower allocation找dummy-free state时，不需要该state实际收到own baseline。它实际效用t始终至多`b_x+收到real的q`；由p≥q得原调度private负载≤2−t。这个不等式方向已逐项重算。
5. 全部未选states的原incidence留private，负载W_x≤1。原zero jobs也留private，不会凭辅助SC的零值选项给任务增加资格。resource只外送真实收到且有正值的原incidence，对应real items跨players不可拆分，所以原resource峰≤1。
6. dummy-free player的效用≤b_x+Σq≤b_x+W_x=1，故t≤1。这一事实共同控制未选private及resource≤1，不能漏掉它而只报selected-state负载。

## 边界与量词攻击

- 同resource出现正/零混合：仅正值参与κ；零support不被改成正值，restricted eligibility仍逐state正确。
- all-zero/unused resource：不建有正值real item，无0/0；原jobs仍在P，私端0可完整安排。
- 空state或W0：baseline1给该state真实价值1，对应selector加零jobs的原private负载1。
- K_g=1：本组没有dummy，唯一player自动dummy-free，不需要额外pigeonhole前提。
- V0/OPT2：算法可输出t0与all-private2；反向资源独占只在C<2使用，正文没有在C2端点偷用unit容量1。
- κ可增长：算法只取最小正值，不按κ循环；κ的bit长由正值分子/分母位长支付。因子改善可能趋零，未升级为一般UM统一常数算法。
- α固定实数：先固定有理a∈(4,α)后调用R4完全合法。若α作为输入给出，本正文并未承诺统一次数。
- 实际近似比：以O=OPT∈[1,2]、c=1/(ακ)，重新展开差值确为`2(1−c)(O−1)>=0`。
- 源排除：固定κ0与ε严格小于1/(ακ0)时，YES实际上界和NO实际下界有固定正间隔；这只排这个完整flat像类。κ随ε发散仍被允许，不能从中推出标准LabelCover/MinRep可解。

## 来源与总位复杂度

已亲自下载并读取CM原PDF：`history/source/literature/unrelated_machines/cheng_mao_2019_restricted_max_min_allocation_v1.pdf`，28页，768864 bytes，SHA256 `ea99b29b0b05694d16fcf18b63fddcd9dc798aa6ef476ac0b78033c8eaf90e7a`，URL <https://arxiv.org/pdf/1905.06084v1>。实际读restricted定义、Theorem1/印2及其后无需目标oracle的说明、§2.2–2.4、§3.1 Build/Collapse、Claim16末有理参数和Lemmas17–18运行界。没有独立复证全部local-search不变量。

对规范§5的二进制接口，已独立核以下事项：清分母乘积只增加多项式位长；组合最优目标为整数，lo/hi截停二分在`hi>OPT`不变量下不需成功标签单调；target<=OPT时CONFIG可行保证不误失败，其它target若成功只使实际分配更好；0目标为空质量分配。local search所用物品集合、匹配/整数流、固定有理倍target比较不展开数值权。

若需要明确固定参数，令d=min(1,a−4)，γ=d/100、β=γ²、μ=γ³。Claim16末所需式等价于`d > 10γ+4γ²+(15+3d)γ³−γ⁴`；右侧≤0.100418d，故均为可硬编码有理数。signature里的log仅用于分析。该补充不替代外部定理正确性。

另下载核DRZ当前v4：`history/source/literature/unrelated_machines/davies_rothvoss_zhang_2026_santa_hypergraphs_matroids_v4.pdf`，17页，186948 bytes，SHA256 `a95a66ce64fbaf6c49086f6891a19909d271df2fd784e0da530424afd9c91081`，固定URL <https://arxiv.org/pdf/1807.07189v4>；§4/物理15页明确改旧4为6。规范正文只用它纠错，不作为第二个后端。

## 核验与证据层

本次没有实现/执行R4后端，没有重跑root所述945个Fraction小例，也没有把其执行归为本人独立测试。本文审查的是规范正文的所有定义、一般转换、原job合法性、边界和Paper Fact适用性。有限审计的真实数量/代码hash由root自己的冻结输出承担。外审、全球新颖性与独立论文价值未认证。一般UM目标的正反面保持OPEN。


## 最终形式修补的实际复读追加

再次实际读取规范正文§6的完整段落，最终canonical SHA256：`983480e2db1676add57db68cbfd0f7eed4521cddc9c3152ef1de9fe6a283615b`。前序全文审查hash `0da64ce52e3d85666aed7c3a156f68c09a699418e584512d851d82a02c3b05c5` 及其当时意见保留，不倒改为已经修复的记录。

§6现明确取固定有理separator θ，使 `2−1/(ακ0)<θ<2−ε`，只对实际有理makespan与硬编码有理θ比较，并明确不对可能非有理的α、κ0作精确实数比较。我已按修后文字核：ε的严格间隔保证这样的有理θ存在；YES输出峰不超过左端、故严格小于θ；NO所有实际峰不低于右端、故严格大于θ。固定参数下硬编码θ是合法的位多项式判别算法，毋需从任意实数oracle求出θ。

因此前序记录中的唯一非fatal形式建议已实际修复，当前没有standing objection。此追加仅针对该小修补的实际read-after，不新增blind/独立审查身份，不更改原证明或有限测试的证据归属。
