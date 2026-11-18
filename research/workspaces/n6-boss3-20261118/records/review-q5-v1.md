# boss3-q5-review-v1：准确冻结复核

## 1. 结论、版本与输入独立性

**verdict：changes-required。** 冻结正文有一项已证实的试验范围错误：所谓“q恰5”的输入实际上只有四种锚外不同非空覆盖。解析倒二全历史下界和 A/B/C 条件缩减核通；有限全 SPE 的数值结论也经独立重放核通，但其准确范围是这个实际 q=4、保有同覆盖异标签的目录。本报告不要求本局部成果解决一般 q=5 或原六人问题。

- RUN：`n6-boss3-20261118`；reviewer：`/root/review_q5`；session：`boss3-20261118-review-q5-v1`。
- freeze_id：`boss3-q5-prefix-v1`。
- freeze_revision_pin：`ae527d93d05ff72c0b4c936ad632f21f8a8b61cfc504b53cfbebc1b88fdf9e76`。
- 冻结路径：`research/runs/n6-boss3-20261118/studio/freezes/boss3-q5-prefix-v1/ae527d93d05ff72c0b4c936ad632f21f8a8b61cfc504b53cfbebc1b88fdf9e76.json`。
- 证据类别：内部、非作者独立自然语言复核，并有整数/Fraction 精确有限重放；不是形式化证明或外审。

本人本次作为新派 full 挑战者，未参与成果生成，不是原 obstacle/independent 槽。首次接触成果是本次任务及随后读取冻结正文；`independent:true` 仅指对作者的独立性，不声称读成果之后仍有 obstacle 输入隔离。共享文件系统不构成强隔离。

实读 `AGENTS.md`、`prompts/research-review-design.md`、`research/agent-design/HYPEREDGE_WORKFLOW.md`。全部 16 个 `content_refs` 条目逐项对 SHA256；13 个不同文件均吻合，含重复条目的准确 section。全文读取证明、模型、问题、递推来源、脚本、输入/输出、artifact/spec/两份 packet；154207 字节策略 JSON 完整解析并逐节点核验，未靠抽样代替读取。文件/段落/哈希清单见末尾及机器实物 `review-q5-v1/audit-results.json`。

## 2. confirmed：有限输入并非五额外覆盖目录

准确位置：冻结 note 第 46 行：

> 五额外B_a为前20客户模20的长度5区间、起点4a，a=0,…,4；……q恰5

精确反证来自冻结 `q5-cyclic-K5-input.json`：

\[
\operatorname{cov}(B_0)=\{0,1,2,3,4\}=\operatorname{cov}(T_0).
\]

其余四个 B 覆盖互不相同，且均不等于六锚。因此目录有 11 个原标签、10 个不同覆盖，六锚外不同非空覆盖恰为 **4**。定义的 q 按覆盖计数，不能因 B0 使用不同标签就将其算成第五额外覆盖。该输入合法保留同覆盖异标签；错误在范围表述，不在模型合法性。

**影响：** 不能以该试验作为“恰五额外覆盖目录”的实测结论，也不能把将 B0 当成锚外额外覆盖的暴露统计解释成正确 q=5 的包络障碍。这个有限目录仍属于 q≤5，但甚至在已有四额外定理的域中。目录上的具体数值、完整历史递推以及解析缩减不因此失效。

**最小修复：** 新版本将该有限试验如实称为“四种额外覆盖、另有一个锚的异标签”的目录，保原有效数值；或者另存真正 q=5 的输入，逐集合确认五种额外覆盖互异且均非锚，再提供新输出、策略和新 freeze。不得原地修改本次冻结字节。作者已实际回复确认 B0=T0，表示另存修复版本；这不消除本准确 v1 的错误。

## 3. 核通的解析范围：末位与倒二

共同前提全部保留：恰六人、有限单位客户、有限原标签目录、六个两两不交且大小均为全目录最大值 K 的锚，锚外不同非空覆盖 q≤5；额外覆盖可跨锚且可有锚外客户；任意完整纯 SPE、所有合法有序前缀、任意离轨弱平局、空覆盖、重复行动与同覆盖异标签。K=0 为零收益边界，以下 K>0。

末位证明（note 第 7 行）成立：对 \(f(t)=t/(1+t)\)，单位负载增加的折扣增量为 \(1/[(t+1)(t+2)]\le1/2\)。五个先前行动在六锚并上的折扣总和≤5K/2，故某锚给末位收益≥7K/12。每个查询直接使用末位原节点的弱最佳回复条件，没有冻结后继的问题。这不要求 q≤5。

倒二使用的局部引理确实在已冻结四额外定理“**两种末端前缀**”中独立于 q≤4 导出，不能把整条四额外定理直接套到 q=5，但本稿并未这样做。给定四人原前缀，J 为未出现锚，s≥2，P 为它们上的既有总折扣。对强制 Tj 分枝，末位可查询其余 s−1 个新锚，真实收益 vj≥K−(P−Pj)/(s−1)。强制者因真实末位覆盖造成的追加损失≤K−vj，因此强制收益≥K−Pj−(P−Pj)/(s−1)。不同 j 可以使用不同的真实后继，原节点分别比较后再平均仍得

\[
u_5\ge K-2P/s.
\]

note 第 13–16 行四类互斥穷尽：

1. a≥2：s=6−a≤4，至少 a 个先前锚行动不碰 J，其余至多 s−2 个行动各贡献≤K/2，得 u5≥2K/s≥K/2。
2. a=1 且额外有重复：M≤3，利用 \(f(\sum m_B)\le\sum f(m_B)\) 在各客户上计费，P≤K∑mB/(1+mB)。有重复的分拆仅需考察 2、3、2+1，最大 7/6，故 u5≥8K/15。已有锚的重复和空行动均与新锚不交。
3. a=1 且额外无重复：只使用已经独立支付的末位≥K/2。强制锚若被末位同覆盖复制，两人同叶收益相同；否则，有害额外覆盖若再次出现，末位在其全部客户上最多分 1/2，在与强制锚的非空交集上最多分 1/3，严格低于 K/2，与末位下界矛盾。于是所有额外覆盖只需各收首层，∑Dj≤qK/2≤5K/2=sK/2。
4. a=0：同一重复排除后，将每种覆盖首层先放入，每个后续层折扣增量≤1/6，得 \(D_j=\frac12\sum_B|B\cap T_j|+\frac16\sum_B(m_B-1)_+|B\cap T_j|\)。M=0 时第二项为零；M>0 时 M≤4、d≥1，∑Dj≤K[5/2+(M−d)/6]≤3K=sK/2。

第三、四类的 Dj 只依赖同一原前缀及整个目录，不依赖各强制分枝恰好选择相同的后继标签。可先选 Dj≤K/2 的锚，再分别处理该锚的复制/不复制真实分枝。此处不存在未付 A/B/C 反哺倒二的循环。

## 4. 核通的 A/B/C 条件缩减及未付共同前提

note 第 22 行的共同归纳前提是：**所有更晚位置、所有合法有序前缀的当前规定收益≥K/2**，而不是只沿某条在轨历史成立。复制锚的后手与强制者同叶等收益；不复制时，若有害额外覆盖的终局重数超过 max(1,mB)，至少有一次在强制槽以后，选该覆盖的最后后手终局收益严格<K/2，违背严格更晚节点的归纳前提。这个比较按覆盖而非原标签成立，同覆盖异标签不逃过严格比较。

p≤3 的分类逐项核过：无额外重复且 s≥5 由 ∑Dj≤5K/2≤sK/2 支付；s=3 只能是 p=3 的三个不同锚；s=4 且 p=3 的两个锚加空行动/旧锚重复，新锚全未覆盖。此时第四位强制新锚，第五位再强制另一新锚后，末位有未覆盖新锚可赚 K；末位真实收益因 |S|≤K 必为 K，故与此前覆盖不交，第五位该偏离亦赚 K。第五位真实处方随后也赚 K，并与第四位强制锚不交，因此只有末位能分摊该锚，第四位≥K/2。这个 K 结论由真实最佳回复推出，没有借用任何未审倒三加强结论。

有额外重复时，s=6 由 M≤3、d≥1 得包络总和≤17K/6<3K；s≤4 至少需 a+2≥4 个前缀槽，与 p≤3 冲突；s=5 只能 p=3、a=1、M=2、d=1。

因此准确未付家族确为：A=第三位面对两个不同锚；B=第四位面对两个不同锚加一个额外覆盖；C=第四位面对一个锚加同一额外覆盖两次。表内按覆盖多重集描述，包含全部原标签次序及别名。额外独立枚举了由六锚、五不同额外覆盖和空覆盖构成的长度 0–3 的 1885 个抽象类型序列，全部落入以上支付类或 A/B/C；A/B/C 分别为 30/450/90 个类型序列。这个有限分类核验不替代覆盖几何的解析证明，也不把同覆盖历史的策略合并。

第 36 行的 closing implication 是条件性的：先对所有 B/C 原子局支付当前界，则第四位全历史界闭合；再支付 A，第三位全历史界闭合；第二位和根部的包络应用才能借已闭合的更晚前提完成。**本次未证明 A、B、C 的统一当前下界；也未证明一般 q=5 半覆盖，更未证明无六锚假设的原题。**

## 5. 精确有限递推、策略证书和独立重放

完整核查 `independent/full-history-recursion.md` §1 的必要性与充分性。对任意给定有序历史 h，当前选 a、叶 y 的必要条件是它胜过每个偏离 b 真实 SPE 子树的收益，而后者不小于该子树所有可达叶的最小收益。反之，对选中子树选取实现 y 的 SPE，对其他原标签子树分别选取实现最小收益的 SPE；这些有序子树互不相交，可拼成完整策略。故 note 第 40 行的集合递推精确，不是固定后继的静态比较。

同计数历史只共享**可达集合**，不会要求一份完整策略采用相同续局。原标签是独立动作坐标，B0 与 T0 均未被合并。重复标签所带来的两种终局计数正保留在结果中。来源稿 §3 提及的 C++ 搜索器未列入本 freeze，亦未被当成本次 Python 计算的承重输入；本报告不审该 C++ 实现或其搜索范围。

逐行核 `exact_tail.py`：六人的客户负载在 1…6，60 为这些分母的公倍数，`60//load` 在所有实际收益比较中精确；`E` 保全部可行叶，`current_worst` 另保当前动作以免同叶不同动作损失收益信息；未见采样、浮点优化、剪枝或超时替代结果。输入本身保证这里的 n、K、六锚及 OPT6=6K，脚本的 OPT6 字段不是适用于任意输入的优化器。

`policy_certificate`/`verify_policy` 的准确作用是：导出并验证**一份指定前缀子局的完整 SPE 策略**，每个内部节点有 11 个原标签后继。它不是全部 SPE 策略证书，也没有为根输出另导出策略。全 SPE 终局覆盖来自经证明的集合递推，而不是从一份 DAG 推广。本冻结果没有把这两者混为同一证据。

独立程序 `review-q5-v1/independent_audit.py` 完成三种核验：

- 不调用作者集合递推，使用 `Fraction` 直接检查冻结策略全部 1397 节点和 4356 行动边；核根计数等于指定有序前缀的计数、每个子计数增加正确、真实动作终局一致，以及每个原标签偏离不优。27 个计数状态确有多个目标叶节点。
- 显式展开全部原标签**有序树**，不按计数缓存可达集合；前缀展开 16105 节点，根部展开 1948717 节点，含 1771561 个有序终局；仅缓存终局的 Fraction 收益。独立重新得到前缀可达计数 2 种、当前最低收益 300/60=5、前缀福利全部 30；根可达计数 2 种、福利全部 30。
- 在复核目录重放作者运行器，新输出除 elapsed_seconds 外与冻结输出逐字段相等，并另存重放策略。作者计数态数 12376、终局计数数 8008 亦相等。

两种可达计数的唯一区别是 T0 与 B0 的行动坐标互换。它们产生相同覆盖几何，福利为 30。这再次证实了 q=4 的输入语义，并不把异标签当作第五额外覆盖。

复现命令（从本 clone 根目录）：

```sh
python research/workspaces/n6-boss3-20261118/records/review-q5-v1/independent_audit.py
python research/workspaces/n6-boss3-20261118/records/review-q5-v1/prefix_types.py
```

机器结果分别在 `review-q5-v1/audit-results.json` 与 `review-q5-v1/prefix-types-results.json`。作者运行器重放实物亦保存在同一目录；冻结作者文件没有修改。

## 6. 其它积极挑战的处置与交回

| 疑点 | 分类 | 核实理由及影响 |
|---|---|---|
| q 恰 5 的输入语义 | confirmed | B0=T0，实际 q=4；阻断此准确版本的完整 approve，不阻断其解析及真实有限数值 |
| 将四额外定理整条用于 q=5 | not-real | 仅用不依赖 q 的两末端局部引理、重复严格比较；q=5 的包络常数已在新稿重新支付 |
| 倒二借 A/B/C 作循环归纳 | not-real | 末位先独立支付；倒二只用末位；更早位置明确保条件归纳 |
| 原标签、离轨弱平局被压缩掉 | not-real | 解析每分枝用同一原策略真实后继；集合递推拼接原标签子树；独立树以原标签展开 |
| 策略 DAG 被误当全策略覆盖 | not-real | 全终局结论另由必要且充分的集合递推支持；单策略 DAG 仅核其具体实现 |
| 解析分类漏空覆盖/旧锚重复/额外同覆盖别名 | not-real | 空/旧锚重复有显式干净前缀论证；额外重数按覆盖合并，标签历史仍逐一量化 |

无其它仍影响上述已核局部结论的 unresolved 指控。A/B/C 统一下界和一般原题是作者明确保留的数学义务，不把这些未付目标归为本局部证明的错误。

已将 confirmed 问题和最小修复真实送达 `/root` 与 `/root/execution`；作者实际确认并告知将另存修复。随后也真实回送了解析核通范围、完整有序树重放结果和策略证书边界。Main 后续告知末两位另有更强已知结论；该新颖性信息未用于本次证明付款，本报告不宣称本局部下界新颖。

## 7. 精确读取与复核实物哈希

以下清单由已实际逐项核过的 frozen content_refs 生成；重复的 section 引用仍在 review JSON 和 audit-results 中逐项保留。证明 note 除第 46 行范围错误外，其第 5–36 行和第 38–42、55–59 行的实际局部含义已按上文核查；原四额外定理重点核“两种末端前缀”“所有有序历史的归纳”；递推来源重点核 §1，其余全文阅读但不升级为本次对无关结论的独立审查。

| 冻结文件 | SHA256 |
|---|---|
| `research/runs/n6-boss3-20261118/studio/artifact-notes/33b6fa6014ab8b4a8e07cfabfaaf4c8fca0ffc108184c6641c087ee610a12fdb.md` | `33b6fa6014ab8b4a8e07cfabfaaf4c8fca0ffc108184c6641c087ee610a12fdb` |
| `research/workspaces/n6-boss3-20261118/informed-b/exact_tail.py` | `1b51b11d1dd5aadd0c523dbad4504690e8fd25b8fda2d6b868f42ab214efe200` |
| `research/workspaces/n6-boss3-20261118/informed-b/q5-cyclic-K5-input.json` | `f030b983e201240a48f5b3f8d30fe0c00535d142333f58529d256f56e5df91ab` |
| `research/workspaces/n6-boss3-20261118/informed-b/q5-cyclic-K5-output.json` | `fc837a5518b2318c65f5cf621f742e7eaf89ac2a3ba43b06aedf963cb2f74835` |
| `research/workspaces/n6-boss3-20261118/informed-b/q5-cyclic-K5-policy.json` | `5efe5bb1bfd1d832af61b16081ca0852d4e5bd9832242714f5e3c06369e32412` |
| `archives/customer-attraction/state/定理/六不交最大锚与四种额外覆盖--定理.md` | `e38f88c49cd7475cc8fdb84bd6885b349e4913d0d970bd25273ef91ff7a0b969` |
| `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md` | `cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88` |
| `archives/customer-attraction/subarchives/six-providers/state/问题/六人完整历史半覆盖目标--问题.md` | `0626668e7a825108fc0b3699e42394b75b1c2e2a526df220a90d91a02afc8a0c` |
| `research/workspaces/n6-boss3-20261118/independent/full-history-recursion.md` | `2408e36ade6de27b897f3e25cc20dff370e1a2389e379de7369d2bbf307b0605` |
| `research/runs/n6-boss3-20261118/studio/artifacts/boss3-q5-prefix-reduction/3e118f49c13b7e9c9685cd25ec5f9a298f8fb04dc988b266f4228a4cc4e2aa16.json` | `c2b257a9e5bfc1ccc10e1e81dd50ba1e8d06db0eaeb8c3154ba5377dbf478fe4` |
| `research/workspaces/n6-boss3-20261118/spec.json` | `5d45871b81dff68042f35c8faef132e224c4bea6bab14b9db5a00b4e6a6f8dc3` |
| `research/runs/n6-boss3-20261118/packet-full.json` | `62bcd3ed08e4d455673e98f5834789121a915adaf0d5881f14f86f1fdfff149b` |
| `research/runs/n6-boss3-20261118/packet-obstacle.json` | `109c9f8ef683db0814d99e72a6bddd6df7def51438ffc8521f4b3f76ef10278b` |

复核新增实物：

| 文件 | SHA256 |
|---|---|
| `research/workspaces/n6-boss3-20261118/records/review-q5-v1/audit-results.json` | `31385a01f92b25a9d03c9ceec395197252ed263d39b728d6f6d1e220385996bf` |
| `research/workspaces/n6-boss3-20261118/records/review-q5-v1/author-runner-replayed-output.json` | `6ef549e1e2358f0f58cbc95fed26250ececca90ebdb331f934f95e8337bd0abe` |
| `research/workspaces/n6-boss3-20261118/records/review-q5-v1/author-runner-replayed-policy.json` | `5efe5bb1bfd1d832af61b16081ca0852d4e5bd9832242714f5e3c06369e32412` |
| `research/workspaces/n6-boss3-20261118/records/review-q5-v1/independent_audit.py` | `a4145829dc3f7bce93207f8c4494291cc3d4c0b8433da9cfb5447281c05ac8be` |
| `research/workspaces/n6-boss3-20261118/records/review-q5-v1/prefix-types-results.json` | `7aa89208e93199c11675ea284b66f91b55bd756a925495d4c20dd303016586de` |
| `research/workspaces/n6-boss3-20261118/records/review-q5-v1/prefix_types.py` | `be20eea5bff24af7679e9ba94ed64bb4e8845fe11e6aedaa9de9913aef395a2c` |
