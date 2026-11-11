# Agreement 到列表 agreement：本轮完整实读与比较

本任务 `unrelated-machines-3a-3a-7f3790280aa92a17` 当前归 Boss6，核心为 `M-a324d647caf14545974f47d8cd0096c8` v2；Root 已发布 read-add 后的两个只读端点为 Set Cover 定理 `M-4db1e9e555294998a207d584ce22485f` v2 及 `UM-LIST-AGREEMENT-DEGREE-BUDGET-v1` v1。当前任务的三项 pin 与复用边的两项 endpoint pins 相符。未运行 Git、work.py、队列、旧科学程序或 native 绑定检查；最终发布、edge-check 与 done 由 Root 完成。

本轮完整实读三个当前 registry records、共享文献正文、Moshkovitz 原文的冻结全文提取（PDF 印刷 pp221–235，现成 txt 为 718 个 LF、Python splitlines 为 734 行，已连续读完 1–240、241–500、501–734）、degree 对象完整正文及其已登记 evidence 精确标题。核对 PDF 原字节 SHA，并用 PyMuPDF 直接提取、渲染实看印刷 pp227–229，确认列表定义、Lemma 4.7、Corollary 4.8 的根号与 Claim 4.10。此次不是只继承旧阅读；旧 canonical 的 edge/review/ledger 也实际读过，但其历史 native 运行没有在本轮重跑。

## 1. 完整量词与平方损失

固定同一有限投影游戏 `G=(A,B,E)`，`B` 非空，非空有限字母表 `ΣA,ΣB` 及每边总映射 `πab:ΣA→ΣB`。ordinary agreement soundness `ε0` 指每个单标签左赋值在至多 `ε0|B|` 个右点出现两个**不同左邻居**的投影相等。它是 Definition 4.2 的 agreement 错误，不是普通满足边比例。

任取逐点列表 `Λa⊆ΣA`、`|Λa|≤ℓ`，令 `q` 为至少一对不同左邻居可从各自列表挑到同像标签的右点比例。对于每个这类右点，先固定一对邻居和标签见证；再对各左点独立、均匀取一个列表标签。两见证同时被取到的概率至少 `1/ℓ²`。线性期望不要求不同右点的事件相互独立，故所得单标签赋值的 agreement 比例期望至少 `q/ℓ²`；每次单标签赋值又都至多 `ε0`，所以

`q ≤ min(1,ε0ℓ²)`。

这里的量词是“每个固定列表赋值都满足该比例上界”；期望法只反推出存在一个单标签赋值达到相应下界，不能改成每次随机解码都达到。原文按恰好 `ℓ` 个不同标签定义，本证明直接适用于至多 `ℓ`。空列表可先任意填一个标签；agreement 对扩列表单调，因而也被覆盖。若 `ℓ>|ΣA|`，使用真实列表大小即可，不需要不存在的 `ℓ` 个互异符号。列表上限是逐左点的，不是平均预算。

## 2. 本轮解析锐性核对

任取整数 `K≥ℓ≥1`，令 `A={a1,a2}`，`B={bij:i,j∈[K]}`，`ΣA=[K]`，`ΣB={0,1,2}`，每个右点与两个左点相连，并定义

`πa1,bij(x)=0` 当 `x=i`，否则为 `1`；

`πa2,bij(y)=0` 当 `y=j`，否则为 `2`。

任单赋值 `(x,y)` 仅在 `bxy` 同像，故最大 ordinary agreement 恰为 `ε0=1/K²`。若两列表都取 `[ℓ]`，agreement 右点恰为 `[ℓ]×[ℓ]`，比例 `q=ℓ²/K²=ε0ℓ²`。选 `K=2ℓ` 就在非平凡错误 `q=1/4<1` 达到平方损失；因此一般投影游戏上的统一损失不能替换为 `o(ℓ²)`。这是本轮直接解析构造，未使用有限扫描或证书重放。映射不要求对整个 `ΣB` 满射；不能把此锐性自动声称为额外满射模型的锐性。此构造只是桥的参数边界说明，不另建对象、反驳边或重复支持边。

## 3. 向 Set Cover 实际贡献与已有边复用

已有 canonical `um-022e-agreement-square-loss-to-setcover-list-step` 的 source 是本核心、target 是当前 Set Cover 定理；全文件 SHA 为 `7a7b5785bcc0726fd877571c89705e91c4d999845e3d241ab4261328b91da883`。它精确保留局部 `contribution`：在同一游戏且 `ε0ℓ²≤η` 下，得到每个列表赋值的 agreement 比例至多 `η`。两端都已纳入本任务，且边 incident 本核心，故原字节复用，不另写相同边。

用于 Corollary 4.8 时，Lemma 4.4 的输入 edge error `s=ε²D²` 输出 ordinary agreement error `2εD²=2D√s`；故实际收费为 `2Dℓ²√s≤η`，充分 `s≤η²/(4D²ℓ⁴)`。原文 Corollary 4.8 使用更强条件 `√s≤η/[2(Dℓ)²]`，也充分；不能把 `ΣB` 普通边可靠性当成已付清的 agreement 可靠性，或让多对数列表免费通过常数错误。

完整 SAT→Set Cover 定理仍需要已证明 PCP/平行重复、Lemma 4.4 的 degree 前提与转换、适用参数的 partition system、`Sa,σ` 构造、Claim 4.10 小 cover 计数和 `N=|B||U|` 的规模换算。小 cover 取内部 `0<η<1/2` 时，由均值与阈值的空隙实际得到好右点比例至少 `η/(1−η)>η`；每个好右点的所有邻居列表都不超过阈值，截断不会损失所需见证。最后内部误差须按最终 `α` 重选，才得到 `(1−α)lnN` 与 `N=n^{O(1/α)}`。这些均由目标的原完整证明支付，不是本平方损失桥单独推出。Theorem 1.2 已由已证明的 Dinur–Steurer 接口支持；§5 的 CVP、MAX3LIN 分别仍依赖 PGC、linear PGC，不能混入此无条件主定理。

## 4. 与 degree-budget 对象的真实共同域

degree 对象另外要求有限**简单** `(d,D)` 双正则图、`d≥1,D≥2,B≠∅`，每个右点所有邻居投影像的交非空、agreement 来自两个不同邻居。其 ticket 贪心每服务一个右点花两张 ticket；终止时未服务右点至少 `D−1` 个邻居饱和，联合 `L|T|≤2|S|` 得可构造列表的 agreement 地板

`f=L(D−1)/(2d+L(D−1))`。

每关联分数流 `2/D`、右供给 2、左容量 `min(L,d)` 在 `L≥ceil(2d/D)` 时可行；整数性保证每右点选择两个不同邻居，得到全 agreement。逐固定底图的私有符号构造只证明这一**普适全覆盖阈值**的锐性，不声称分数地板对每张图/每套映射锐。

所以仅在上述共同域，若对所有 `≤L` 列表有 agreement soundness `η<1`，必有

`η≥f`，`d/L≥(D−1)(1−η)/(2η)`，`L<ceil(2d/D)`。

再由本核心给 `η=ε0L²` 时，必要

`ε0≥(D−1)/[L(2d+L(D−1))]`；若 `ε0L²<1`，还必须 `L<ceil(2d/D)`。这些是完整共同域中的参数兼容性结论，不是 degree→一般投影源/Set Cover/UM 的迁移。degree evidence 的较短旧审查对 soundness 讨论列出更窄非退化域；本轮按当前完整 body 的明确 `d≥1,B≠∅` 域重构，ticket/flow/锐性证明在该域成立。

一般投影定义不能补每右点的公共像：`A={a1,a2},B={b},ΣA={0},ΣB={0,1}`，两边分别把 `0` 投成 `0` 与 `1`，是简单双正则图，却没有共同像。这只反驳“普通投影定义蕴含共同像”的隐含假设，不反驳带共同像前提的 degree 定理，也不声称它是 Moshkovitz 的 PCP 输出。YES 的完美赋值不能移给另一个 NO 输入。Corollary 4.8 固定右度 `D`、并未固定左度 `d`，故列表长度增长与 degree 必要预算也无矛盾。

## 5. 覆盖与结论边界

本核心覆盖为 linked，复用一条 accepted/unconditional 的局部贡献边；本轮没有新增重复边。degree 比较已在精确共同域内完成，域外迁移不成立，无需把它转成未付后续任务。当前任务没有指定 overlap_comparisons；没有新建 3B/3C 承接任务。缺少 UM source-to-scheduling decoder、一般 UM hardness 或客户目录 payoff 连接不属于本桥结论，不能凭同名术语造模型 hub。
