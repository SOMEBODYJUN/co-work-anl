# boss3-B-review-math-v1：B类逐人半锚下界的非作者复核

## 1. 结论、准确版本与实际范围

**verdict：approve；evidence_level：internal-independent。** 冻结证明建立下述局部结论：六个两两不交、等大且为全目录最大大小 K 的锚，锚外不同非空覆盖 q≤5；对任意完整原标签纯 SPE、任意合法三步有序前缀“两个不同锚加一个额外覆盖”，第四位规定终局收益≥K/2。允许任意标签次序、同覆盖异标签、全部离轨历史、弱平局、重复和空覆盖。

本报告核通完整正向论证及其决定性精确计算，没有以“未找到反例”代替证明检查。**不支付 A、C、一般 q≤5 的所有历史逐人界、同叶前四人总福利预算或原全目录六人半覆盖。** 325/632 仅是四条强制锚分枝均为 double-extra 的必要模型证书界，不是本定理的一般下界。

- reviewer：`/root/review_q5`；session：`boss3-20261118-review-B-math-v1`；RUN：`n6-boss3-20261118`。
- freeze_id：`boss3-B-math-v1`。
- freeze_revision_pin：`99258d5407253dff5506ea508350b730ba77013a88c7f75823a2a1b7a8514420`。
- 冻结 note：`research/runs/n6-boss3-20261118/studio/artifact-notes/1a5571d8f872f578a61f89656681185044bf3adff3550bc8890ffd69f3e0278b.md`，SHA256 同文件名。
- 实际作者：`/root/execution`、`/root/idea`。本人没有参与本 B 论证或证书的生成；`independent:true` 为作者独立性声明，不声称原 obstacle 输入隔离。

全部 20 条 content_refs 逐项检查完整字节 SHA256，全部吻合；18 个不同文件均已实际读取。本轮全文实读 B 证明、两个新推导稿、生成/校验代码、artifact、所有新 JSON；证书与映射完整解析并全量核验。与此前准确版本同 SHA 的正式模型、问题/spec/packet、四额外定理和正式末两位定理/承重引理复用本人已经实际完成的审读，仍重核哈希及本次共同适用性。此前尾界应用复核见 `records/review-q5-v2.md`（SHA256 `893a0191677e33de074b38eecff5ee968a69bf9f426f1af6c92906b9911136aa`）。

## 2. 原模型、退化和 q 分支

原定义要求同一有限非空**标签**目录、单位客户、六名单位权提供者及每个原有序历史上的完整纯 SPE。证明始终固定一份 σ 和一个原前缀 h；收益只依负载计算，策略定义域并未被按负载商掉。原前缀的三个覆盖为两个不同锚及一个锚外非空覆盖 E，因此在 K=0 时无此非空 E；全零退化亦直接满足不等式。

六锚不交给 OPT6≥6K，每个目录覆盖≤K又给 OPT6≤6K，二者合成 OPT6=6K。q≤4 时调用冻结的正式四额外定理，模型、全部历史、别名和弱平局范围完全一致，未给原目录添加占位主题。其本 B 实例也可直接从四个新锚的首层包络总和≤qK/2≤2K及已付尾界检验，故没有把未审早位下界当成这里的前提。

余下仅 q=5。原前缀 E 是五种额外覆盖之一，剩余恰四种不同非空覆盖，固定一个原合法代表标签 F0…F3 仅供查询。实际后手可以选择覆盖相同的其它标签；原 σ 仍沿该原标签历史续行。所有必要行对任意真实后继成立，既未删除其它原标签，也未假设相同覆盖的历史使用相同续局。

## 3. 已付尾界及所有锚后手情形

正式末两位定理和计数引理在本实例给每个合法四人历史后的两名规定收益≥θ6(0)≥(2OPT6−5K)/12=7K/12>K/2。它保持同一原目录、任意合法有序前缀、每个真实末位最佳回复和任意弱平局；合法前缀嵌入、逐客户差值及计数共同前提已核，无隐藏混合值或背景利润替换。故这两位不能选过去已有覆盖（其收益≤K/2），不能选空覆盖，也不能彼此同覆盖。

把未选锚命名为 T0…T3、旧锚为 T4/T5。B 前缀只由 E 负载新锚，故 Pj=|E∩Tj|/2，P=∑jPj≤K/2。第四位强制 Tj 后沿同一 σ 真实完成，记后手 A,Y，收益 u,v，强制者收益 wj。

逐情形核：

1. A 为额外、Y 为其它新锚。以其余三个新锚应用不依 q 的真实末位缺额平均式，u≥K−2(P−Pj)/3。A 与 Tj 的交集每客在同叶使 A 受到至少 1/2 的自身分享缺额，故 A 对 Tj 的新增折扣≤|A∩Tj|/2≤K−u。Y 不碰 Tj，得到 wj≥K−Pj−2(P−Pj)/3≥K−P≥K/2。
2. A 为其它新锚 Tk、Y 为额外。真实末位可查询排除 j,k 的两个新锚，v≥K−(P−Pj−Pk)/2。在 Tj 交集上，Y 造成的额外折扣 1/[(p+1)(p+2)] 不超过 Y 自己的分享缺额 1−1/(p+2)，因此新增总折扣≤|Y|−v≤K−v。故 wj≥v−Pj≥K−P≥K/2。
3. 两位均为其它新锚。都不碰 Tj，wj=K−Pj≥K/2。

其中所有偏离与查询均在相应真实历史比较，不把 A/Y 冻结成原路径后继。这个缩减不使用第四位或更早位置的未付归纳。

若原第四位规定收益 u4<K/2，原节点 IC 给每个 wj≤u4<K/2。由以上三类排除及尾部不重复，四条强制枝必均是四个 F 覆盖中的有序不同对。每枝有 12 种，两后手的覆盖可随 j 任意改变；四枝仍共享同一原目录与客户集合。

## 4. 223客户型与六组必要线性行

每客户恰落在六个不交锚块之一或锚外块，再记录 E/F0/F1/F2/F3 五个会员位。锚外全零型对所有目录收益为零可删除，余 7×32−1=223 型；覆盖六锚内但五位全零的客户仍完整保留。每型非负整数客户数除 K 得非负实质量，六锚质量各为 1，五额外各质量≤1。放松整数性、额外互异/非空及不等于锚等约束只扩大必要域，方向安全。

原三步背景恰为 1E+1block4或5；第四位强制 j 后恰再加 1blockj。同一个 223 维质量向量用于四枝。旧锚上的 +1 始终保留；锚外与跨锚相交均未丢失。γ 可取归一化的 maxj wj，非负且在坏反设下<1/2。

逐组核查证明中 165 条 Ax≤b 及六条等式 Ex=1：

| 行组 | 数量 | 为原 SPE 必要条件的理由 |
|---|---:|---|
| 四种 F 及 E 容量 | 5 | 五个原合法覆盖大小均≤K；归一化右端 1 |
| 每枝 wj−γ≤0 | 4 | γ 取共同四枝最大强制收益 |
| 每枝两个末两位收益≥7/12 | 8 | 已付正式尾界，适用于每条原离轨强制枝 |
| 实际末位查询九标签 | 36 | 给定该枝实际 A，末位真实 BR ≥每个新锚/E/F 原合法标签的查询收益 |
| 实际倒二查询九标签的最坏末位保底 | 36 | 倒二改选 Q 后任意真末位 L 只会对每个 Q 客户再加至多一层，偏离收益≥∑Q1/(b+2)，再用真实 IC |
| 每枝倒二改选其它新锚的缺额行 | 12 | 在改选 Tk 的真实尾，末位查询另外两新锚给 v′≥1−∑l≠j,kPl/2；Tk 的新增损失≤1−v′，所以实际 u≥1−Pk−∑l≠j,kPl/2 |
| 每枝全部16有序 F 查询 TQ 行 | 64 | 下述未知真实 L 的合法消元，不预设 L=Q |

六条锚质量等式右端都是 1，无额外分枝客户变量；224 列为全部 223 客户型加 γ。

**TQ 的关键量词核查。** 固定倒二真实节点背景 b，对原合法 T,Q，令 L=σ6(H,T) 为同一 σ 在倒二改 T 后的真末位。即使此处离轨、存在任意弱平局，完整 SPE 仍给

\[
u\ge U_b(T,L)
=U_b(L,T)+f_b(T)-f_b(L)
\ge U_b(Q,T)+f_b(T)-K.
\]

依次用倒二真实 IC、已核逐客户差值、L 在其原历史上的真实 BR，以及 f_b(L)≤|L|≤K。T、Q 可以相同，L 可为原目录任何标签；没有给 L 添加预选、唯一性或不重复假设。所有16个 F 有序 TQ 同时成立，且只使用同一个客户向量，所以未知真 L 的消元有效。

矩阵代码精确对应这些式子：实际 u/v 的分母是 b+1A+1Y；末位查询分母是 b+1A+1Q；倒二粗保底为 b+2；缺额行的 E∩Tk 系数为 −1/2、另外两新锚系数各 −1/4；TQ 的两项分别为 f_b(T) 与 U_b(Q,T)。省略旧锚查询或其它 IC 仅使必要域更松；没有把充分/必要方向颠倒。

## 5. 20736→1365→69 的完整覆盖与数学对称性

有序不同 F 对共 12 种，四枝共有 12^4=20736 个有序模式。任意置换四个新锚同时置换枝编号与客户锚块坐标：四锚质量各 1；旧锚块 4/5 和 E/F 全局容量不变；查询所有新锚及缺额行都完整置换。因此可将四枝 pair 排序，得到 C(15,4)=1365 多重集。**这里对客户向量作相应坐标置换，不要求 E 在新锚中均匀，也不声称同一个客户向量本身对称。**

再置换四个 F 名字，同时置换所有客户 F 会员位、pair及查询行。四个容量、全部 F 查询和全部16 TQ 行均闭合于此置换；E 与旧锚背景保持不变。每个原多重集的 S4 轨道由24次额外重命名覆盖，按字典序选代表恰69种。

独立程序没有只相信映射的标题：重新枚举1365多重集及每个24个额外置换，得到69个规范代表；逐一检查全部1365条记录中的 F 置换和新锚排序确为置换，且真正把原模式送到相应代表；此外逐一遍历全部20736有序模式，确认其排序多重集都有映射，各模式全覆盖。相同pair的重复仅产生稳定排序的任选置换，不漏分枝。

映射记录若为 `anchor_order=order`，新枝 i 对应旧枝 order[i]，旧客户新锚块 k 送到新块 order^{-1}(k)；F 会员位按 extra_permutation 送到新位。由上节每条行的显式公式，行和列都相应置换，右端保持不变，目标 γ 保持不变。因此代表上的证书可支付原模式，而非只证明69个人造均匀实例。

## 6. 有理证书、生成器与真正独立的精确重建

作者发现脚本使用 SciPy/HiGHS 生成浮点对偶，转为有理数后检查，再保存69份证书。作者 solver-free 校验器不导入发现模块，但发现器调用同一 `build`；所以单独运行作者校验器不能独立排除共同建模错误。本报告没有把这种模块分离称作两套独立数学建模。

本人另写 `records/review-B-math-v1/independent_B_audit.py`，只依 Python 标准库。它以**整数位掩码、逐客户列优先贡献**从上述已证明必要式重建全部69个系统；推导和证书接受阶段不导入作者 build，也不使用求解器或浮点。覆盖223型、224列、165不等式、6等式；客户列中旧锚背景单独计算。其后完整解析69份证书，检查索引无重复且合法、λ≤0、全部15456个对偶列残差非负，以及有理下界准确等于证书所列值。

对 Ax≤b、Ex=1、x≥0，λ≤0 给 λᵀAx≥λᵀb；加等式并用 c−Aᵀλ−Eᵀy≥0 得

\[
\gamma=c^Tx\ge b^T\lambda+\sum_i y_i.
\]

等式乘子无符号要求。此推导的方向、六个等式右端、γ非负列、所有客户型残差均已核实。69份证书全部通过，最小精确下界为 **325/632>1/2**，没有仅凭 float status=0 或声明 PASS 接受结果。

独立接受之后才导入作者校验模块作第二次逐系数对照：全部69个165×224矩阵、右端及六条等式与独立重建完全相等（不等式系数共2550240项）。然后仅调用作者只读 `verify()`，结果与冻结 replay JSON 逐字段一致；没有运行会重写作者 JSON 的 `__main__`，没有重跑发现器。冻结证书、完整映射和输出都实际全量读取。

可复现命令（clone 根目录）：

```sh
python research/workspaces/n6-boss3-20261118/records/review-B-math-v1/independent_B_audit.py
```

机器结果为 `records/review-B-math-v1/independent-audit-results.json`；包括全部哈希、69个逐证书结果、20736模式覆盖计数及与作者重建的全系数比较。代码禁止写 bytecode，所有新增实物仅写复核目录。

## 7. Closing implication、疑点处置与未付事项

对任一真坏 B，§3 强制全部四枝为 double-extra；§4 给一个共享非负客户向量，六锚等式、所有165必要行成立，且 γ=maxjwj/K<1/2。§5 将该同一个见证送到某个已全量核过的代表，不增加标签，不更换各枝客户总体。§6 对该代表给 γ≥325/632>1/2，矛盾。因此原坏反设不成立，u4≥K/2。若任一强制枝含锚，则早已由解析比较直接支付 K/2；不能将 double-extra 模型的更强数值跨到这一分支或整个 B 类。

| 主动挑战 | 分类 | 结论 |
|---|---|---|
| 原尾界或 q≤4 分支有未付前提 | not-real | 正式原模型/全部历史完全匹配；q5只用已付末两位，B局部不需早位归纳 |
| TQ 把未知真末位固定成 Q 或换有利策略 | not-real | 固定同σ真 L，逐项 BR/差值/容量消元，对所有 L 有效 |
| 客户型漏旧锚+1、锚外客户或跨枝共享 | not-real | 七block与五会员位完整；独立矩阵重建确认背景与同一变量向量 |
| 1365/69 仅查代表而漏有序模式或 E 非均匀 | not-real | 行列重命名不要求向量对称；独立穷尽20736模式及所有映射 |
| 只重放作者脚本仍共享建模 bug | not-real-after-independent-check | 本次另写列优先完整系统，先独立接受所有证书，再逐系数对照作者 |
| 325/632 被当一般 B 或原福利下界 | not-real | 证明和 artifact 都明确限四枝皆 double-extra；总定理仅K/2 |

没有影响本准确局部命题的 confirmed 或 unresolved 缺口。idea 两稿中 C 类推论与历史有限坏点/真菜单数值属于背景和后续研究；已全文读取并核其本 B 采用的解析接口，本次不将未冻结的历史输入数值当成本定理证据，也不认证那些有限案例或 C 结果。新 B 主证明重述了全部必要推导与公式，未靠这些案例付款。

本次不支付 A/C、其它前缀或无六锚假设的原题；也未对文献新颖性、外审或形式化作声明。已向 Main 真实回送哈希、必要行及 TQ 核查、独立矩阵/有理证书和模式覆盖结果；本报告与准确文件同时交回 Main 和作者。审读中未改作者冻结文件，未操作 Git 或 studio。

## 8. 准确文件与新增复核实物哈希

以下列不同冻结文件；review JSON 与机器结果保全全部20条原 content_refs（含重复 section）。读取范围及复用范围见 §1，完整新证明和决定性新计算均已实核。

| 冻结文件 | SHA256 |
|---|---|
| `research/runs/n6-boss3-20261118/studio/artifact-notes/1a5571d8f872f578a61f89656681185044bf3adff3550bc8890ffd69f3e0278b.md` | `1a5571d8f872f578a61f89656681185044bf3adff3550bc8890ffd69f3e0278b` |
| `research/workspaces/n6-boss3-20261118/informed-b/verify_B_all_orbits.py` | `8cfd37578233a67ff55db43b2700f0c092a2ddf7927be5d00ae53cd666a8ca27` |
| `research/workspaces/n6-boss3-20261118/informed-b/B-all-orbit-rational-certificates.json` | `47a1e8b2a792b31fc2ddca384a8b75ef10dec54d6695aafe320c8203f80db1b9` |
| `research/workspaces/n6-boss3-20261118/informed-b/B-1365-to-69-orbit-map.json` | `f326dbcebf8b18688dfd4a71b76d294568d7cb5936d99f91935ac9bd0ecf976c` |
| `research/workspaces/n6-boss3-20261118/informed-b/B-all-orbit-exact-replay.json` | `3ed6a868cb9ef45d99ade8d0143b2bbeb18ffb3f2ea3953c6655062247ee28f6` |
| `research/workspaces/n6-boss3-20261118/informed-b/certify_B_all_orbits.py` | `9cf85d342a683438db132b31dd485f5e4f114f02f73188c067484ba15f0829ac` |
| `research/workspaces/n6-boss3-20261118/informed-b/B-all-orbit-discovery-summary.json` | `14b2b3e5501c56766c18a2cb68938fcfc04f45ee06d8785cf19948c3ac08ad7a` |
| `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md` | `cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88` |
| `archives/customer-attraction/state/定理/六不交最大锚与四种额外覆盖--定理.md` | `e38f88c49cd7475cc8fdb84bd6885b349e4913d0d970bd25273ef91ff7a0b969` |
| `archives/customer-attraction/state/定理/末两人逐人保底与全人数弱福利界--定理.md` | `204030503c37b18f8d26ce664b9cb99afc688fed77c8221a00cf0d8d7b21b34b` |
| `archives/customer-attraction/state/引理/末位最坏背景值与目录计数界--引理.md` | `6263b3d935b1c2d3d7ae6aee4016ae78cb369de1f28ddb284e8202fd21b69c3d` |
| `research/workspaces/n6-boss3-20261118/informed-a/cross-query-cap-row-r1.md` | `4f123cf9eaf1ef3750c1274df3bbd111cffe78977b873492337ff890c58e7a88` |
| `research/workspaces/n6-boss3-20261118/informed-a/tail-menu-reduction-r1.md` | `411f74ea89d9c38e1a152dd4f09dcfd9657f690a8190ca22dc1811ce92442b47` |
| `research/runs/n6-boss3-20261118/studio/artifacts/boss3-q5-B-prefix-half-floor/9376432796ad9c76b337c58c81b8e80fa3dbbac1df69d44f4c6160bd1c375b4b.json` | `48cbbf5d42aa76403df94ac1addf90684ea2a0c1a1e7a397ecf109903470aa5f` |
| `research/workspaces/n6-boss3-20261118/spec.json` | `5d45871b81dff68042f35c8faef132e224c4bea6bab14b9db5a00b4e6a6f8dc3` |
| `research/runs/n6-boss3-20261118/packet-full.json` | `62bcd3ed08e4d455673e98f5834789121a915adaf0d5881f14f86f1fdfff149b` |
| `archives/customer-attraction/subarchives/six-providers/state/问题/六人完整历史半覆盖目标--问题.md` | `0626668e7a825108fc0b3699e42394b75b1c2e2a526df220a90d91a02afc8a0c` |
| `research/runs/n6-boss3-20261118/packet-obstacle.json` | `109c9f8ef683db0814d99e72a6bddd6df7def51438ffc8521f4b3f76ef10278b` |

复核新增实物：

| 文件 | SHA256 |
|---|---|
| `research/workspaces/n6-boss3-20261118/records/review-B-math-v1/independent-audit-results.json` | `69ba2a3c62d60f5eafe04b73cd293fca1bc67a2a73a4e52f8aff080576471d37` |
| `research/workspaces/n6-boss3-20261118/records/review-B-math-v1/independent_B_audit.py` | `198bb3e7eab2f93abc8f42cb9bf56fa8873991cb0b7714db994002f2d1037d6f` |
