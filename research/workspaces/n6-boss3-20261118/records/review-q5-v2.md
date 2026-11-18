# boss3-q5-review-v2：勘误与新增承重内容的定向复核

## 1. 准确结论与范围

**verdict：approve；evidence_level：internal-independent。** 此通过限于冻结 v2 的勘误、既有正式末两位定理在本六锚子类的实例化、A/B/C 条件缩减、同一实际叶上的已付/欠项，以及一个真正 q=5 固定有限目录的静态放松与全部 SPE 计算。它不证明参数化 A/B/C、一般 q=5 半覆盖、无六锚假设的原题，也不认证新颖性。

- RUN：`n6-boss3-20261118`；reviewer：`/root/review_q5`；session：`boss3-20261118-review-q5-v2`。
- freeze_id：`boss3-q5-prefix-v2`。
- freeze_revision_pin：`ef3e50bd1a37352d6de6dbe941547094d245e20c68555df728a7205eab1fe23b`。
- note_ref：`research/runs/n6-boss3-20261118/studio/artifact-notes/bf78bb43f183698f3d5db02582f1a576c8b78fb3da8058ad4cc2d3eed606127c.md`，SHA256 同文件名。
- 作者仍为 `/root/execution`；本人未参与论证或输入生成。`independent:true` 表示非作者独立复核，不表示原 obstacle 输入隔离。本轮沿用实际审查者，不冒称新原始独立探索。

本轮逐项核全 20 条 frozen content_refs（17 个不同文件）的 SHA256，全部吻合；新 note、勘误、正式尾界及承重引理、语义/暴露脚本、新输入/输出/语义输出和 artifact 全文实读。新策略 JSON 完整解析，逐节点逐行动精确核验。与 v1 字节相同且用法不变的原模型、题面、四额外局部引理、`exact_tail.py` 和 packet/spec 复用已经实际完成的审读；本轮仍重新核其准确字节。新 note 的完整合成论证亦通读，没有只核差异而略去共同应用前提。

v1 既有报告：`research/workspaces/n6-boss3-20261118/records/review-q5-v1.md`，SHA256 `48331940944f419d3cce88c0071e3df3ae1acdd66e6a9647502137bcffca0368`。v1 的旧目录完整有序树不重跑。本轮独立有序树重放针对**新的 K6 输入**，不是重复旧计算。没有阅读或审查正在另做的共享菜单 LP 探针。

## 2. v1 confirmed 问题已如何修复

v1 唯一 confirmed：旧 K5 输入 B0=T0，却声称六锚外“q恰5”；实际为四种额外覆盖。v2 note 第 3、63 行和勘误正文明确承认此点，保旧有限数值只用于其真实 q=4、含同覆盖异标签的目录，没有借新版本默改旧冻结。

v2 改用新文件 `q5-cyclic-K6-v2-input.json`。逐集合核查并独立断言：

- N={0,…,35}，六锚分别为六段长度 6 的不交分块；每个合法覆盖大小为 K=6。
- 五个额外覆盖为前 24 位客户模 24 的长度 6 区间，起点 1、5、10、15、20；五者互异，且没有一个集合等于任一锚。
- 原标签共 11 个、不同覆盖亦为 11 个，真正的锚外不同非空覆盖数为 5。没有仅凭名字或起点推断这一点。
- 客户索引、原标签名字、前缀 `(T4,T5)` 及其计数逐一一致；六锚已覆盖 36 位客户，容量上界又给任意六标签并集≤36，故 OPT6=36。

因此 v1 反馈在新准确版本上已经实质解决。旧 v1 的 changes-required 对旧冻结仍保持正确，本次 approve 只绑定新 revision，不伪装成旧字节已获通过。最终还重新核了旧 v1 全部 content_refs，均仍为旧 SHA。

## 3. 新增正式尾界：所有共同前提与实例化

note §2（第 15–28 行）使用的正式正文 SHA256 为 `204030503c37b18f8d26ce664b9cb99afc688fed77c8221a00cf0d8d7b21b34b`；其承重引理 SHA256 为 `6263b3d935b1c2d3d7ae6aee4016ae78cb369de1f28ddb284e8202fd21b69c3d`。重点核正式定理 §1–3、§5及引理 §1–3；两文件其余内容全文阅读，但未把来源说明中的历史有限审计重新宣称为本次完成。

**模型与量词共同吻合。** 固定同一有限单位客户集合、同一有限非空原标签目录、六名单位提供者、同一份完整纯 SPE、任意合法四人有序前缀 P。P 不需在根路径上，可以包含重复覆盖、空覆盖、同覆盖异标签。其负载 p 为由合法四标签产生的非负整数向量。所有偏离都取同一策略在新原历史上的真实后继。没有换目录、换策略、换概率空间，亦不把根参数 OPT6 当作合法背景下剩余利润。

**逐客户差值及真实后继桥。** 交集客户两边分母相同，非交集恰贡献即时值，故

\[
U_p(A,B)-U_p(B,A)=f_p(A)-f_p(B).
\]

有限目录保证即时最大化者 A 存在。取任一 A∈argmax f_p，固定策略在 `(P,A)` 后的规定末位 B 是该真实节点的最佳回复，于是

\[
U_p(A,B)\ge U_p(B,A)=\max_T U_p(T,A)\ge\theta_2(p).
\]

倒二原节点的弱最优性把真实偏离保证转给其规定收益；实际末位的最佳回复同样≥θ2(p)。第一步对每一个末位最佳回复都成立，故包含任意弱平局；没有假设两位实际收益之间的固定次序。

**合法前缀嵌入。** 对 θ6(0) 取最小的对象是五个合法竞争标签。将其前四项固定为 P，就把最小化域限制到第五项 A 自由的子域，因而 θ2(p)≥θ6(0)。这个论证只限制静态最小化域，不要求同负载历史采取同一策略，也没有把对手的行动移到随机抽样之后。此处的 θ 是 min 后取 max 的确定背景最坏最佳回复值，不是隐藏抽样安全值 v。

**目录计数下界及同一参数。** 对任意五标签合法历史 H，记 M(H)=maxA∑x∈A1/(1+hx)、O=OPT6。最优六标签客户重数 ox 给逐客户 `(ox+hx)/(1+hx)≥1_{ox>0}`，求和得 O≤6M(H)+∑x hx/(1+hx)。因 hx 为整数，最后一项≤(1/2)∑x hx≤5K/2。故 M(H)≥(2O−5K)/12；对 H 最小化后仍成立。六锚不交和全目录大小上界共同给 O=6K，最终

\[
u_5,u_6\ge\theta_2(p)\ge\theta_6(0)
\ge\frac{2\operatorname{OPT}_6-5K}{12}=\frac{7K}{12}.
\]

这个付款不要求 q≤5；K=0 单独处理，全零结论与非重复推论不混用。K>0 时 7K/12>K/2。若倒二或末位的规定覆盖已在其原前缀出现过，其每个客户最终至少被两人覆盖，收益≤|A|/2≤K/2，矛盾；空覆盖收益为零亦不可能。这只约束规定行动，完全不删除离轨历史中此前出现的重复或空行动。该非重复后果核通。

## 4. A/B/C 与同一实际叶的合成

v2 §3 重述的全部有害重复严格比较、首层/重复层收费、前缀分类与 v1 已核论证相同，参数和标签用法不变。v2 用更强的正式尾界支付原 K/2 归纳基底，方向正确。原 v1 全部 1885 个抽象长度≤3前缀的分类结果也保持适用，不需再次枚举同样的组合类型。

本轮重新核完整 closing implication：假设严格更晚位置所有合法原历史的规定收益≥K/2；复制强制锚时使用同叶等收益，不复制时每个有害额外覆盖末叶重数≤max(1,mB)；由同一原前缀的 Dj 选锚，不要求各偏离后继共用同一个终局。空覆盖、旧锚重复的干净前缀仍经真实倒二/末位 K 比较支付。于是只余 A=第三位前缀两不同锚，B=第四位前缀两不同锚加一额外覆盖，C=第四位前缀一锚加重复同额外覆盖。

这些是条件接口。先对全部 B/C 原历史支付当前界，才能闭合第四位；再付全部 A，才能闭合第三位；第二位和根的包络再使用已付的更晚归纳前提。新稿没有把尚欠的三个家族静默升级成普遍已证。

v2 §4（第 57–59 行）新增的同叶接口成立：在同一实际叶，u5+u6≥7K/6；若该叶实际选了至少三个不同锚，则仅这些不交锚就给 W≥3K。因此任何可能 W<3K 的根 SPE 实际叶至多出现两种不同锚。对其余根，在同一叶证明前四人收益和≥11K/6，即可与已付尾部相加得到 W≥3K。这里 11K/6 是一个充分付款目标，不被误当所有坏根的等价刻画。稿件明确不把条件逐人下界、不同叶的收益或某个必要 LP 的局部值相加成实际福利证明。

## 5. 新有限输入、静态放松与全部 SPE 证据

`exact_tail.py` 与 v1 字节完全相同，SHA256 `1b51b11d1dd5aadd0c523dbad4504690e8fd25b8fda2d6b868f42ab214efe200`。复用 v1 对整数收益、全部可达集合递推、原标签量词及策略 DAG 的逐行核查；新 note §6 又完整给出必要性/充分性，不依赖未列入新 freeze 的旧递推来源文件。

集合递推的必要性是给定策略每个偏离子树终局的当前动作收益≥该子树可达集合的最小值；充分性是在各互不相交的原标签子树上分别选择实现相应最小值的完整策略，并在选中子树实现指定叶。count 缓存只共享可达集合，既不强迫历史采取相同续局，也不排除任意平局。

`verify_q5_stress_input.py` 全文读取。其静态放松确实只枚举五种真实额外覆盖的三个后手，不检查后手 BR。给定前缀 T4/T5 和强制新锚后，原前缀不碰该锚，负载损失准确为∑x m/(1+m)。互异三额外均非锚，既无强制锚复制，也无额外覆盖重复。独立用 `Fraction` 枚举全部有序额外三元组，重得：

| 新锚 | 允许重复的最大折扣 | 三个互异额外的最大折扣 |
|---|---:|---:|
| T0 | 47/12 | 10/3 |
| T1 | 47/12 | 10/3 |
| T2 | 15/4 | 19/6 |
| T3 | 15/4 | 19/6 |

互异列均大于 K/2=3。因此，在这个明确忽略后手最佳回复的静态放松中，每个强制锚均有坏后续，不能由这套静态最大损失挑出一个≤K/2的锚。这只反驳该放松对本例给出的安全保证，未反驳包含 BR 条件的证明、全部前缀静态方法或原题。新稿的表述限于原方法和该例，未越界。

独立程序 `review-q5-v2/independent_audit.py` 对新输入完成：

1. 逐集合语义检查，确认真正 q=5、K=6、OPT6=36，且原前缀和计数一致。
2. 使用 Fraction 直接读取并核冻结策略全部 1405 节点和 4444 行动边；每个内部节点均有所有原标签后继，真实子终局一致，每个偏离收益不优。392 个倒二/末位节点另核收益≥7K/12且不重复任何先前覆盖。38 个计数状态出现多个目标终局，未把 DAG 限制为计数策略。
3. 独立显式展开新目录全部原 11 标签有序树，仅缓存终局 Fraction 收益，不按计数缓存可达集合。指定前缀展开 16105 节点；根展开 1948717 节点，其中 1771561 个有序终局。两处可达终局计数均**只有六锚各一次**，福利均为36；指定前缀当前最低收益360/60=6。
4. 在复核目录重放不变的作者求解器。除 elapsed_seconds 外所有输出字段与新冻结输出一致；12376 计数状态、8008 终局计数和1405证书节点亦一致。重放输出/策略另存于本报告子目录。

单份 DAG 只是一份指定前缀子局的完整 SPE 策略，未为根部另导出完整策略。全部 SPE 的叶计数范围由必要且充分的集合递推及独立有序树重算支持，不能从单份 DAG 推出。独立计算保留所有原标签弱平局，前缀结果是全部完整子局 SPE 可达叶；根结果是全部根完整 SPE 可达叶。本报告不声称枚举或计数全部策略函数。

复现命令（从 clone 根目录）：

```sh
python research/workspaces/n6-boss3-20261118/records/review-q5-v2/independent_audit.py
```

结果为 `review-q5-v2/audit-results.json`，另存 `author-runner-replayed-output.json` 和 `author-runner-replayed-policy.json`。程序只读冻结输入，所有新增输出均进入本次复核目录。

## 6. 疑点处置、剩余与真实反馈

| 疑点 | 分类 | 精确处置 |
|---|---|---|
| v1 B0=T0 却标 q=5 | confirmed-in-v1 / resolved-in-v2 | 明确旧实例 q=4；换成逐集合确认的真正 q=5 新目录、新输出与新策略；旧冻结保持原字节 |
| 正式尾界依赖不合法或均衡前缀 | not-real | 原定理允许任意合法有序前缀；嵌入只限制合法五标签元组最小化域 |
| θ/v 量词顺序或真实后继混用 | not-real | 即时最大 A 对每个真实末位 BR 有差值支配，之后用 minA maxB 的 θ，不使用隐藏抽样 v |
| 7K/12 的非重复后果删除离轨历史 | not-real | 只约束每个节点的规定行动；此前的任意合法重复/空历史仍在量词内 |
| 更强尾界已自动闭合 A/B/C 或一般 q=5 | not-real | 归纳条件和同叶前四人 11K/6 仍明确欠付，有限实例不外推 |
| 静态坏三后手是原模型 SPE 反例 | not-real | 静态脚本明确无 BR；新精确全 SPE 结果反而全覆盖 |
| 单份 DAG 被误当全部 SPE | not-real | 全范围来自集合递推必要/充分证明，并独立展开新原标签有序树核验 |

没有影响上述准确 v2 局部范围的新增 confirmed 或 unresolved 缺口。仍未支付的数学目标是参数化 A/B/C（或能直接支付同叶福利的其它接口）、一般 q=5 及原全目录六人半覆盖。内部复核通过与形式化、外审、新颖性或一般问题解决不同。

已实际向 Main 回送：新 20 条哈希吻合、v1 错误修复、正式尾界及共同前提核通、新目录有序树/证书/暴露重算结果。完整结论与本报告同时交回作者；未改任何作者冻结文件，未操作 Git 或 studio。

## 7. 准确文件及复核实物 SHA256

下表逐一列不同冻结文件；review JSON 和 audit-results 仍完整保留全部 20 个 content_refs 条目及 section。相同字节复用的审读详见 §1；新证明、全部合成和决定性新计算均按上文实核。

| 冻结文件 | SHA256 |
|---|---|
| `research/runs/n6-boss3-20261118/studio/artifact-notes/bf78bb43f183698f3d5db02582f1a576c8b78fb3da8058ad4cc2d3eed606127c.md` | `bf78bb43f183698f3d5db02582f1a576c8b78fb3da8058ad4cc2d3eed606127c` |
| `research/workspaces/n6-boss3-20261118/informed-b/q5-stress-trial-corrigendum-v2.md` | `bc95d6f0ca8c0d1097ae794d7d093f5b97e566a550b94de558b02ad1a8175b4d` |
| `research/workspaces/n6-boss3-20261118/informed-b/exact_tail.py` | `1b51b11d1dd5aadd0c523dbad4504690e8fd25b8fda2d6b868f42ab214efe200` |
| `research/workspaces/n6-boss3-20261118/informed-b/verify_q5_stress_input.py` | `6816dc286aa31b3695eff4ccf91378bb38eacc6149cb3864d275088ff3656d96` |
| `research/workspaces/n6-boss3-20261118/informed-b/q5-cyclic-K6-v2-input.json` | `2da5d0d51bb8b2060422230f79896f6d25239ea5ea6e246617a003b3b0aa2e3c` |
| `research/workspaces/n6-boss3-20261118/informed-b/q5-cyclic-K6-v2-output.json` | `a26ef089aaf7f63188e999dc74c6860401e74f90f05997d2abc93e0585e328df` |
| `research/workspaces/n6-boss3-20261118/informed-b/q5-cyclic-K6-v2-policy.json` | `a4b647bc520f26e1b526b1c2b3bf5875d4b0f99976d72b7c860d10cf80eae763` |
| `research/workspaces/n6-boss3-20261118/informed-b/q5-cyclic-K6-v2-semantic-and-exposure.json` | `7060ba2d0929bbc13df4872a8a5d30925db8c4dfb5526642828b31d28bfbc6d6` |
| `archives/customer-attraction/state/定理/六不交最大锚与四种额外覆盖--定理.md` | `e38f88c49cd7475cc8fdb84bd6885b349e4913d0d970bd25273ef91ff7a0b969` |
| `archives/customer-attraction/state/定理/末两人逐人保底与全人数弱福利界--定理.md` | `204030503c37b18f8d26ce664b9cb99afc688fed77c8221a00cf0d8d7b21b34b` |
| `archives/customer-attraction/state/引理/末位最坏背景值与目录计数界--引理.md` | `6263b3d935b1c2d3d7ae6aee4016ae78cb369de1f28ddb284e8202fd21b69c3d` |
| `archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md` | `cc4a9dadb09e08b072cb63214d2e084db38db219e4100efbccf9b7f497520e88` |
| `archives/customer-attraction/subarchives/six-providers/state/问题/六人完整历史半覆盖目标--问题.md` | `0626668e7a825108fc0b3699e42394b75b1c2e2a526df220a90d91a02afc8a0c` |
| `research/runs/n6-boss3-20261118/studio/artifacts/boss3-q5-prefix-reduction/a5280bc340821df8e76fb6ffa7949b7e012c78c099f57b9fcc3002fc15882270.json` | `47b2634edbcc0d063d13e93d980239f63b7bf6fb2667e04ab60ff57602b45d69` |
| `research/workspaces/n6-boss3-20261118/spec.json` | `5d45871b81dff68042f35c8faef132e224c4bea6bab14b9db5a00b4e6a6f8dc3` |
| `research/runs/n6-boss3-20261118/packet-full.json` | `62bcd3ed08e4d455673e98f5834789121a915adaf0d5881f14f86f1fdfff149b` |
| `research/runs/n6-boss3-20261118/packet-obstacle.json` | `109c9f8ef683db0814d99e72a6bddd6df7def51438ffc8521f4b3f76ef10278b` |

复核新增实物：

| 文件 | SHA256 |
|---|---|
| `research/workspaces/n6-boss3-20261118/records/review-q5-v2/audit-results.json` | `b2b688ca2e90e7b6d9a5762fde4a1c1ad0591054f0e1e7cd51987f94f9b8de4c` |
| `research/workspaces/n6-boss3-20261118/records/review-q5-v2/author-runner-replayed-output.json` | `496bf2bec0d0445681cee06c02edeccd1f6eb8f19cabcfe9cfef3f35ded46e41` |
| `research/workspaces/n6-boss3-20261118/records/review-q5-v2/author-runner-replayed-policy.json` | `a4b647bc520f26e1b526b1c2b3bf5875d4b0f99976d72b7c860d10cf80eae763` |
| `research/workspaces/n6-boss3-20261118/records/review-q5-v2/independent_audit.py` | `c8c2288385cbbfeb86c23d0c16615b09db67dec4711eb6591a160acb67f688d1` |
