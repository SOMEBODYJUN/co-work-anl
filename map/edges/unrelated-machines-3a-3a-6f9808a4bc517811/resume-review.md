# 6f98 接续审读：近完美源、正规化与 Claim 3.2 分组修复

## 实际结论与复用范围

本包核心为 `M-9a7614916cf04cee8915aefce74b502a`，共享端点为 `M-8c360a7779154480879e38c65d1f827e`、`M-fb633f3a6f1448fbbd63bfc7c3806c40` 和 `PCP-EXACT-PROJECTION-PERFECT-COMPLETE-BIREGULAR-ROUNDING-v1`。恢复原收据后，复用已发布 ALL 边 `boss2-mz-joint-source-and-sparsification-close-minrep-parameters`；不重复建立同一条关系。该边的 whole_result 是目标 MinRep 参数修复的完整结果，绝非 exact 4-to-1、perfect-complete 或 unrelated-machines 的完整硬度结论。

其实际联合输入为：MZ 冻结构造中独立的源完备误差参数、整数度正规化桥、记录版 MinRep 全列表稀疏化。先固定 ε′、内部有理参数及充分大 g，沿固定清分母网格取 R₀=Θ(g^p)，其中 2<p<2+ε′；真实总字母表 Q=R₀+R₀^(1−b)。Theorem 2.6 的 s 独立于后来选择的 η，Lemma 6.1 的充分大 ℓ 阈值也不依赖 η，所以能够先固定 ℓ/Q/Δ，再选 η≤1/(16kΔ)。这来自完整构造的参数接口，不能仅以显示 Theorem 1.3 的量词反向推得。

删除 trivial 左点、左度整数化和最后舍入各自的误差均须计入同一个源。已有完整证明通过 pa,pt>2 的固定幂余量得到 NO≤γ₀/2，继而用 ρ≤min{γ₀/4,1/(8Δ)} 得正规源 NO≤3γ₀/4、YES 误差≤3/(8Δ)。γ₀=2^−11g^−2、Γ=5γ₀/4，使 NO<Γ 严格成立。记录稀疏化后各承诺输入分别以至少0.9概率得到 YES 成本≤2N、NO 所有成本≤0.06N/√Γ 的列表均不能全覆盖，且

    (0.03/(g√Γ))² = 1.47456 > 1。

故 NO 成本严格大于2gN。N 是整数度正规化后的总顶点数，后续稀疏化才保持该 N。输出度为 O(g ln g)、Q=O(g^(2+ε′))，归约随机，费用为单位标签成本，覆盖要求为全部带身份约束。中间正规度可以随输入大小增长。

## 精确结构不能免费增加

MZ Definition 1.1 的字母表参数为两侧大小之和；Theorem 1.3 的 YES 仅为 val≥1−τ，Theorem 7.2 仍仅近完美。它们没有赋予 exact 4-to-1 或 val=1。共同正文所记 FMW exact4 定理保留 perfect YES 与任意小绝对 soundness，但没有给出所需的近最优 Q 幂次交易；不能以它反向替代 MZ 的参数。

整数度舍入桥的误差对所有克隆标签逐点同时成立；完美源的复制标签在每个留下的原投影上仍满足，故原本 perfect-complete 时新值恰1。每条新约束仍是原约束，因此原有 exact d-to-1 类型保持；一般全投影输入不会被此桥变成 exact4。共同字母表错型延拓另会改变纤维结构，MinRep 路线只使用其全投影保值，不把延拓说成保 exact4。

全部计数按独立约束身份，而非去重邻点数。平行记录各自采样，固定列表的未覆盖记录数仍服从所需二项分布；列表族按 V×Σ 的子集同时并集，所以 NO 是一个排除所有自适应便宜列表的共同好事件。完美源的删边对每个种子保 singleton 完备；本 MZ 联合源仅近完美，使用的是有概率保证的补标签成本。

Lemma 7.8 的外部 expander 算法、简单图、外部连通性费用以及 PCP→UM/六人 SPE 编译器均不属于复用关系已经支付的合同。主路线经自足整数度桥闭合，并不依赖那个更强的常数度接口。

## 冻结印18页 Claim 3.2 的两处修正

冻结文件为 `archives/unrelated-machines/tools/evidence/retired-literature-four-to-one-20261031/minzer_zheng.pdf`，SHA256 `13b8eb55f86cfe28ac8b283fe83612889b335e14b7a87d64d479451693c7dff4`。以下两处均已对照新渲染的印18页，而非单凭抽取文本。第一处在既有接续审读中已指出，第二处是本轮补充。

**事件句。** 原文在写 val(Ψ)=1−η 后，把“Ui=Vi，或 Ui≠Vi 且 r 份 advice 全零”的概率写成1−βq^−r。这个原事件的概率实际为1−β+βq^−r。把后半句的“advice 全零”改为“advice 并非全零”，得到无暴露坐标事件，其概率才是1−βq^−r。补事件是 Ui≠Vi 且 advice 全零，概率 βq^−r。令

    m = ceil(q^r/β)，

则 m 次独立坐标均未暴露的概率至多 (1−βq^−r)^m≤e^−1，故存在暴露坐标的概率至少0.1。之后固定其它问题、调用单坐标 variable-versus-equation gap，仍给块游戏值≤1−c₀ε（原文可取 c₀=1/30）。

**分组末行。** 定义 Ψ=G_{β,r}^{⊗m} 后，原文末行把 G_{β,r}^{⊗k} 写为 ceil(q^r k/β) 份 Ψ 的重复。这个分组次数倒置，且一般不能写整除等式。最小严谨替换为

    t = floor(k/m)，
    val(G_{β,r}^{⊗k}) ≤ val(Ψ^{⊗t}) ≤ 2^{−c ε²t}。

第一个不等式由忽略余下 k−mt 个独立坐标而得；第二个不等式是对块游戏 Ψ 应用原文使用的 Rao 投影游戏平行重复定理。由于 q^r/β≥1，有 m≤2q^r/β；当 k≥2m 时，

    t ≥ k/(2m) ≥ βk/(4q^r)。

在本文实际参数 k=q^{2(1+c)ℓ}、β=q^{−2(1+2c/3)ℓ} 下，βk/q^r=q^{−r+(2c/3)ℓ} 随 ℓ 增长，故充分大 ℓ 同时支付 k≥2m。因此仍得到原 Claim 3.2 显示的 soundness

    val(G_{β,r}^{⊗k}) ≤ 2^{−Ω(ε²q^−r βk)}。

这是原证明中间式的修复，不否定 Claim 3.2、MZ 主定理或已复用的联合源 ALL 边。充分大 ℓ 条件仍只依赖固定内部参数和 NO gap；不会引入对源完备误差 η 的依赖。原文印55页 s=0→s≥1、印56页权比率倒置、印58页 Cauchy–Schwarz 行加号→减号、印61页 δ=1/g 与缺对数的应用问题仍按已存完整证明的精确修法处理。

## 共享中文页的最小修补位置及影响

建议在 `archives/unrelated-machines/state/文献/四对一与字母表soundness两篇文献整理--文献.md` 的“3.2 组合结构与证明依赖”内，编号1–4的证明流程之后、段落“论文在 Theorem 7.2 中…”之前，增加以下一段，不改冻结原件：

> 冻结原文印18页 Claim3.2 的两处中间式须按实际概率与分组修正：事件“Ui=Vi，或Ui≠Vi且advice全零”的概率实际是1−β+βq^{−r}；把后半句改为“advice并非全零”才得原显示的1−βq^{−r}，其补事件为暴露坐标。再令m=ceil(q^r/β)、Ψ=G_{β,r}^{⊗m}和t=floor(k/m)，原末行写成ceil(q^r k/β)次Ψ重复不对；正确用val(G_{β,r}^{⊗k})≤val(Ψ^{⊗t})≤2^{−Ω(ε²t)}。本构造充分大ℓ使k≥2m，因m≤2q^r/β，t≥βk/(4q^r)，仍得显示的2^{−Ω(ε²q^{−r}βk)}。这些修正不改变Claim3.2结论或主PCP定理。

数学直接涉及 `M-9a7614916cf04cee8915aefce74b502a`。该全文同时作另外四个对象的 body：`M-922feb7b429f49d4b5f13ca51b34aae7`、`M-9f8033b6e1a4485b97636171b09f8218`、`M-ab4a576ed0be482b89d4a646ffc102b9`、`M-d007675a9ed240898c90e831af80b092`；它们的数学陈述不受影响，但全文SHA引用须一致更新。相应边的 evidence_pins/review_digest 及收据资产SHA必须由共享文件owner串行刷新。本worker不修改共享正文、registry或既有canonical边。

## 本轮实际阅读与校验

完整读当前四端点登记及所指三份中文正文、复用 ALL 边和 joint-source-proof.md、f9ff2cee 的 regularization-and-minrep-proof.md；恢复 um-6f9-current 的既有审读。重新 pdftotext -layout 导出冻结106页PDF，本轮实际重读印2、3、8、14、15、18–21、44、52、54–61页；新目视印3、15、18、44、52、54–56、58、60–61页。未把导出全文等同本轮全文复证，未新读FMW/Manurangsi原PDF；Lemma6.1内层证明按登记与原文完整证明入口复用。

已用 read-only edge-bind 核复用边绑定与原文件完全一致，并 edge-check 得 accepted、proof_scope=whole、结构有效（程序输出不代替数学判断）。共享页改动后须重核当前端点pins及canonical引用；receipt只在最终绑定文件后刷新assets SHA。
