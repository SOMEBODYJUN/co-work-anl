# NSW现行义务归位：Boss7窄3D独立审读

结论：同意Boss5的核心处置。R50把“NSW backend same-output-for-all-matchings guarantee plus normalization/REPAIR/flat-UM”不加范围列为未付，已不准确。现行显式、无权XOS合同的同一输出量词已付；原norm1显式菜单在正support unit-FSLP可行下的完整C/D/E亦已付。这里的“normalization已付”只能指B的内部残余归一化和C对**原本norm1**输入的应用，不能理解成任意source都已能保持原模型地正规化。不得删掉整条R50，不升级一般UM、任意源接口或旧条件对象。

现行B是已证数学算法规格，原A–F算法尚未实现、没有端到端软件执行审计；该工程状态不构成重新把同一输出数学保证列为开放的理由。

本审读只写本文件。未操作Git、同步、队列、公屏、canonical、旧资产或科学执行；未审Boss3 SUMmin和Boss5 b77修复。本地`research/registry.json` SHA256为`202c608164e5e7f706c6178d16a0f13089c01abf7b7fdc3cc5b091370fb1f4a8`，`map/integration.json`为`135bdadeca23e9346a77097d2818dd9c005e68f7d906af6b4eae587977b141fb`。R50在本快照`archive_reviews["archives/unrelated-machines"].open_math[13]`，不是Boss5快照的index15；最终接入应按原文及最新输入核对。

## 1. 当前对象和直接关系

实读当前registry的以下精确合同，未凭proved/done或标题代替证明：

- `UM-EXPLICIT-XOS-DETERMINISTIC-FRACTIONAL-NSW-v1` v6：有限非空indexed clause lists，非负二进制有理系数，原物品不交、无权NSW。允许全零/重复clauses、unused items、m=0；算法不输入y。当前registration pin为`ac2a7c5e40d093d4981b13b5505014617fac609e8ac2cf8946bab93a62fa3b4c`。
- `UM-NORMALIZED-MENU-ALMOST-ALL-AND-REPAIR-LP-BARRIER-v1` v6：n≥1、m≥1、每组非空显式indexed states、**每原state**总量恰1，正support unit-FSLP，同一n组共享D个singleton REPAIR，保全部原jobs的ordinary flat-UM。pin为`38ced94214265ec53f2d571a2f63209addf755128e27d6af5cfc48f41ba10a9e`。
- `UM-FRACTIONAL-BENCHMARK-REMATCHING-v1` v6仍是一般次可加的**条件**比较引理：须先给V/H与对每个可行分数残余族的统一预算，不能把该引理读成一般次可加后端。

直接边`map/edges/boss3-sourcefix-repair-8d806bdc7cc35ff1/nsw-to-normalized-quality-repair.json`是上述显式NSW对象到归一菜单对象的accepted/unconditional/**whole**关系。两endpoint pins逐项与本地当前对象重新计算相符；边SHA256为`cc507044caf4d53b3efe0c60cd2fbd5651331535ee1343842fbb2833e5b92d0a`，内容pin为`849dcd5e27a9e0ce82891179d6926021778de5ff7e7feb317783adce5ce10a24`。本审读以下独立推导支持它的whole范围，不以绑定代替数学。

另核到旧综合对象`unrelated-machines/fractional-rematching-normalized-xos-robust-gap` v1和`map/edges/unrelated-machines-3a-3a-87f678d9d92df909/fractional-rematching-pays-benchmark-factor.json`仍保历史conditional/contribution合同。该边的“仍需核E1–E3、另付C/D/E”准确描述**该边自身只付A与benchmark因子**的作用；它不能反向抹掉现行两个v6对象的完整后续证明。本次也没有把旧综合对象升级为无条件。

## 2. 同一实际输出的量词：先S，后∀π、∀y

亲读主证明共用位引理、A及B1–B6（第1–498行），核得量词顺序为

\[
\forall I\quad S=\operatorname{Alg}(I),\qquad
\forall\pi:[n]\overset{\sim}{\longrightarrow}H(I),\quad
\mathsf{NSW}_v(S)\ge\frac{\operatorname{GM}_i(V_i+v_i(\pi(i)))}{60000(5/2)^2},
\]

其中H、V、T和最终σ都只由I决定；π只在证明里出现。

1. B1先在**全部U**求真最大正singleton product匹配τ，H=τ([n])，B=U\H。B2固定lift和确定性LP/vertex tie规则构造V；对每个可行分数残余族z都有`Σz·v/V≤2|A|≤2n`（B.6）。这是A的全称前提，绝非只核本次恢复配置或整数福利。
2. B3/B4在看到任何label前固定候选S_i、轮次及attaining clauses，B5用精确有理label DP固定每原物品唯一label，给全局不交T_i；所有`i∉A''`明确取空。该步骤没有π/y，也没有需要对π作union bound的随机成功事件。局部floor仅改辅助权，不改原valuation或processing times。
3. B6对任意π构造辅助ρ(π)。在singleton successor图把每个需要残余ν的顶点出边切开，cycles亦切为止于这些顶点的路径；每条路径以一个残余最大singleton作**单独反事实**替换，由全U的τ最优性得B.25。不同路径可用同一残余物品作不同反事实，实际分配未复用它。于是B.24对任意π成立。
4. 最后算法只求一次`σ=argmax_σ Π_i v_i(T_i∪{σ(i)})`。同一σ的真最大性支配每个ρ(π)，故B.26对所有π成立。B.23支付A''内比值，A\A''支付6，outside支付1，sum-to-max支付3，得B.27。π变化不会重选T或σ。
5. A的运输补齐、Jensen和正支撑permutation分解，对每个正y给某π_y，使GM(V+singleton)≥B_v(y)/3。将**这个π_y**代入已经∀π的B.27，得到同一S对全部y同时有`NSW≥B_v(y)/1125000`；常数`60000·3·(5/2)^2=1125000`。有限位引理用有理乘积log间隔求真最优匹配，不比较未知无理benchmark。

正benchmark的精确域是：有限有理配置族，每行质量1、每原物品总边际≤1，每个正质量条目的实际值严格正。它不要求算法事先知道y或π_y，所以“比较匹配/benchmark未知”在此显式合同内**不是**剩余义务。外部应用若尚未证明比较对象的合法性、残余全称预算或输入表示，则仍不能调用该结论。

退化条件也付清：无覆盖全部agents的正singleton匹配时，Hall集合同时排除正实际allocation和正分数benchmark；算法返回空bundles、真实最优NSW=0，此时不存在可比较的正y。非空clause list不等于存在正benchmark。证明不在零值取log；若另把含零条目的benchmark定义为0，则非负NSW下的比较仅为空泛扩展，不是本文正log合同。正匹配分支中，任意π的比较乘积为0时保证空泛，但同一实际输出仍正。A、B或A''为空等分支已明列。

## 3. C/D/E到底给出的flat-UM保证

**C：原norm1与正support LP。** `P_gs={u:p_gsu>0}`；unit-FSLP要求`Σ_sλ_gs=1`及每资源`Σ_{g,s:u∈P_gs}λ_gs≤1`，列是support indicator，既不是p权也不数零incidence。原state总量1使`v_g(P_gs)=1`，可行λ即给正benchmark一。B给同一原不交分配NSW≥1/1125000，安全放宽为≥1/3000000>ρ^−1，ρ=2^24。令K=ceil(1/η)、qη=ρ^−K、cη=qη/2。若k≥ηn组`r_g<qη`，其余≤1，则product<qη^k≤ρ^−n，矛盾；`r_g≤cη`严格包含于`r_g<qη`。故两种低组均<ηn；ηn无需整数，输出不依赖η。可变η的阈值位长按K收费，未给poly(log(1/η))。

这里原state的norm1是**输入假设**。B内部除W_i、候选局部floor均已证明有效，但没有给任意source到原norm1模型的保真变换。C的item-equality benchmark可逐列补缺，亦未给一般指数CONFIG oracle。

**D：同组共享REPAIR的准确promise。** 给同一n组增加同一D个全局共享unit资源，每组添D个singleton alternatives，不添agents。原存在≥n−D组unit的allocation时，余下≤D组各用不同repair得到增强全unit，给增强unit-FSLP整数可行点。反向任何增强allocation删去repair后仍为原allocation，至多D组获救。故固定`0≤a_rep<γ_lo≤1`、`D≤a_rep n`、`0<η<γ_lo−a_rep`、`0≤δ_q≤cη`时，原NO若每allocation有≥γ_lo n组`r≤δ_q`，增强LP可行会经C给低组<ηn，却又被迫≥γ_lo n−D>ηn，矛盾。仅测增强显式有理unit-FSLP即可分离所列YES/NO；promise外不承诺。没有给到该准确promise的困难源归约，也不把γ_hi代作γ_lo。

**E：全部原jobs的完整ordinary schedule。** 每indexed state有不同private root，每原资源一个resource machine，每组一个unit selector，每正或显式零incidence一个不同原job。用原unfloored table为B输出bundle Z_g重取attaining state s_g；selector放该root，仅外送该state在已分配正资源上的incidences，其余、未选state及零jobs都留原root。每原job恰一次。于是selected root=`2−r_g`，unselected root=1，resource≤1，**整个原矩阵makespan≤2**；selected roots中`load>2−qη`恰对应`r_g<qη`，数量<ηn。unit allocation时所有负载≤1，selector又给OPT≥1，故unit-YES真实OPT=1。REPAIR新增nD roots、D资源、nD正incidences和nD selector endpoints，selector身份仍n个；额外列出的零incidences也须保留。

这些结论没有给所有组统一正常数minimum、所有机器统一(2−ε)负载或general UM solver；少数selected roots仍可任意接近2。外部source若未付显式表示、每原state norm1、共同原资源/组身份、正support unit-FSLP与全部原job保持，不能套用该完整关系。

## 4. 最小精确更正文案

原句：

> R50 remaining UM obligations include the general two-witness domain beyond single-home with Z empty, unknown witness search, general strong-moment gap/rounding, and the NSW backend same-output-for-all-matchings guarantee plus normalization/REPAIR/flat-UM. The fixed-order norm-greedy counterexample addresses its specified extraction rule only.

建议根Boss在最新integration中只替换这一条为：

> R50 remaining UM obligations include the general two-witness domain beyond single-home with Z empty, unknown witness search, and general strong-moment gap/rounding. The finite explicit nonnegative binary-rational unweighted XOS backend now proves one deterministic total-bit-polynomial actual output for all H-comparator inequalities and all positive finite rational fractional benchmarks. For original norm1 explicit menus with feasible positive-support unit-FSLP, C/D/E prove the same-output almost-all-group quality bounds, the stated shared-singleton REPAIR promise LP test, and a complete original-job flat-UM schedule of makespan at most 2 with the stated selected-root count. Weighted, oracle-only or general-subadditive backends, and source applications lacking a proved norm1/positive-support-LP and original-job-preserving interface, are outside this proved contract. It does not give an all-group constant minimum, an all-machines (2-epsilon) bound, a general UM solver or a hardness-source reduction. The fixed-order norm-greedy counterexample addresses its specified extraction rule only.

“all H-comparator”严格指B1正singleton分支中由τ固定的H上双射；无正匹配的退化分支按第2节处理。若根Boss希望open_math只放开放项，可将中间两句已付合同移入resolved数学说明，但不得原样保留那段无范围NSW尾句。原R50其它三个义务及fixed-order反例范围本次未审，原样保留；未知witness search不可偷换成此处已经不需要输入的π/y。

## 5. 可复核证据与实际阅读范围

以下SHA均在本clone从实际文件字节重新计算；只把实际读过的范围作本审读依据，未重跑历史源或外部文献：

| 路径 | 本次实读范围 | SHA256 |
|---|---|---|
| `research/workspaces/map-v2/Boss5/finalization-20261116/nsw-open-scope-review.json` | 全短报告；作为待核主张和定位，不作为替代证明 | `0e2a470cbbf8676bddc1e4d7bd83a28718dee2b33912589a290507e40d88c2c9` |
| `tools/evidence/private-tree/partial-quota-welfare/explicit_xos_fractional_nsw_and_normalized_robust_gap_boundary.md` | 1–639行：共用位引理、完整A/B1–B6/C/D/E及F边界；F2未读亦未采用 | `9ef11b3f69d786c4a89f3e575f0cce60cc5d611c2fbad61cdabd3d642aaea33c` |
| `archives/unrelated-machines/state/审查/显式XOS分数NSW的确定化合同与真实审读链--审查.md` | 全文；现行B主body与历史条件范围 | `dd27a701b1f1eedbd5162be243b0ad24f8733a144509ab555a10d0dd2dfb208a` |
| `archives/unrelated-machines/state/审查/归一化菜单高低比例互补的实质纠错及修复边界--审查.md` | 全文；现行C/D/E主body、同n/共享D/全原jobs边界 | `ad299d925721db08eadd2eb530a07871dab58aff5d739d591a32335c40eeea8d` |
| `archives/unrelated-machines/state/审查/分数重匹配显式XOS-v4-v5增量--审查.md` | 246–323行，§7–8；任意π与同输出、C/D/E、γ互补 | `a579f14298c8e6234a8406ae5d5888b1c8e489d63ad920319e4eb4c8c82cc034` |
| `archives/unrelated-machines/state/审查/多outer single-state tiny-home 19-10 Exact-only与proof-canonical-backend版本审查--审查.md` | 166–185行，§8及定向勘误；只核被whole边引用的范围 | `2d4cd9224f731d574061a4fa0e7222688d09726c6340b429a7cf55536f8bb2b4` |
| `archives/unrelated-machines/state/定理/分数重匹配与归一化XOS稳健缺口边界--定理.md` | 1–115行；旧综合条件口径A/E1–E3，未作为现行完整B的欠账证据 | `05d4fbbde010e55a6b1fbb920d2f7e4d84743d1c8e50a3392a3d6918249a829b` |
| `map/edges/boss3-sourcefix-repair-8d806bdc7cc35ff1/nsw-to-normalized-quality-repair.json` | 全边、所有条件/roles/explanation/scope/whole_result及端点pin | `cc507044caf4d53b3efe0c60cd2fbd5651331535ee1343842fbb2833e5b92d0a` |

另实读`map/edges/unrelated-machines-3a-3a-87f678d9d92df909/fractional-rematching-pays-benchmark-factor.json`全文与其旧综合目标的当前registry合同，保持conditional/contribution；浏览了上述三端点的现行直接关系清单，未重审其它17核心、几何子族或typed-tiny-home边。本文件只给根Boss数学更正文案与证据，不宣称最新receipt/queue已集成或关闭任何并行修复任务。
