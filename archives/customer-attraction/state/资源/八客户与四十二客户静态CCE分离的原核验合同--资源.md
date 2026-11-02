---
id: customer-attraction/eight-and-forty-two-client-cce-original-verifier-contract
kind: resource
type_tag: 资源
title: 八客户与四十二客户静态CCE分离的原核验合同
status: complete
truth_status: finite-original-replays-and-two-strategy-versions-preserved
review_level: seven-full-primary-source-reads-and-unmodified-Fraction-program-replay
scope: 三单位提供者四主题共同目录；八客户两份完整策略与四十二客户发现版；任意不对称相关静态CCE
summary: 保全三原核验器、八客户两策略输出及stdout原件，逐字区分已有主审计、仅末换行重复和真实有序策略增量；八客户锐值544/87与安全值44/23重放成功，四十二客户只认证W32与静态CCE下界33。
source_refs:
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-6cfe7c79118a41f6bd5659aa5d780852/security_aggregate/eight_client_cce_bridge_failure.md
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-6cfe7c79118a41f6bd5659aa5d780852/security_aggregate/eight_client_cce_exact.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-6cfe7c79118a41f6bd5659aa5d780852/security_aggregate/eight_client_cce_ordered_source.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-6cfe7c79118a41f6bd5659aa5d780852/security_aggregate/eight_client_cce_verification_stdout.json
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-6cfe7c79118a41f6bd5659aa5d780852/security_aggregate/verify_cce_counterexample.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-6cfe7c79118a41f6bd5659aa5d780852/security_aggregate/verify_eight_client_cce.py
  - source:68fad804ec5946cb296f77dc5b336308a66abf12:research/workspaces/customer-attraction/R-6cfe7c79118a41f6bd5659aa5d780852/security_aggregate/verify_eight_client_cce_ordered_source.py
---

# 资源身份和已有数学的承接

本页保存七份冻结来源的可执行合同、真实策略差异和原字节。八客户的完整反例及锐原始/对偶证明已经在[三人顺序SPE低于全部静态CCE福利](../反例/三人顺序SPE低于全部静态CCE福利--反例.md)，主审计和另一历史实现已经在[三人静态CCE福利原始对偶精确核验](../计算/三人静态CCE福利原始对偶精确核验--计算.md)。本页的增量是工作区原件身份、尚未被主策略覆盖的初始有序策略、三个原程序的实际输入输出合同以及四十二客户原核验器，不重复授予一个八客户新定理。

[证据目录](../../tools/evidence/eight-and-forty-two-client-cce-exact-primary/README.md)保全七原件和三份完整重放。两冻结提交`68fad804ec5946cb296f77dc5b336308a66abf12`及`aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c`在各主源上同字节；[source-manifest.json](../../tools/evidence/eight-and-forty-two-client-cce-exact-primary/source-manifest.json)逐项保存源ID、完整路径、blob、大小及SHA-256。双来源位置不构成两次证明。

| 源ID / 原件 | 实际读到的独有内容与处置 |
|---|---|
| `2d8b4263153c9d451500` / `eight_client_cce_bridge_failure.md` | 7,629B自足八客户正文：21历史策略、20静态列、两套对偶、达到分布、安全值和可信平局机制。数学与既有正式反例一致；保全作者工作区版本及其早期有序策略/发现版文件路由。 |
| `083f64ee6e908fa24f53` / `eight_client_cce_exact.json` | 11,517B，16个顶层字段，保存计数依赖策略21行、84比较、20对偶行、11个有序支持、12个体slack和十安全背景。与已存2026-10-21主运行逐字相同，保为本来源原件而不称新结果。 |
| `44bb4c88d6fffa259a61` / `eight_client_cce_ordered_source.json` | 11,517B，另一份真正有序历史策略；仅`histories`键与前件不同，但两行差异承载完整续局变化，不能当相同结果删除。其余客户、静态列、CCE及安全值字段逐项相同。 |
| `dbf35f04bb5f0489365a` / `eight_client_cce_verification_stdout.json` | 11,518B，精确等于`eight_client_cce_exact.json`原字节再加一个末换行。语义完全重复，保留stdout身份；不额外增加一次核验实现。 |
| `c1bf920385613ab9c7e7` / `verify_cce_counterexample.py` | 2,984B，四十二客户而非八客户：硬编码六mask重数、完整有序策略及非负乘子，精确核84顺序比较和20静态列，给W32与每个CCE≥33；没有达到分布。 |
| `a5f283df578a5a356858` / `verify_eight_client_cce.py` | 4,747B，逐名客户的自含Fraction核验；与既有正式八客户主脚本逐字相同。输入、完整策略、两套乘子、CCE分布、安全查询和对偶都硬编码。 |
| `e55686359f3fdb186f07` / `verify_eight_client_cce_ordered_source.py` | 4,747B，与前程序的差异仅为`SECOND`和`LAST`中下文两处动作；承接初始有序策略，静态CCE与安全值核验逻辑相同。属于同实现的策略变体，不能计作独立第二实现。 |

# 共同定义与两份八客户完整策略

沿用[共同目录完整历史模型](../定义/共同目录完整历史模型--定义.md)。三位单位提供者依次观察所有有序历史，选择同一有限目录中的标签；重复和离轨行动合法。一名单位客户的一单位价值在最终覆盖它的全部玩家间均分。程序的每个客户条目或mask重数的一份都代表一个互异单位客户，没有带权提供者。

八客户为四名只喜欢标签1、一名只喜欢2、一名只喜欢3、两名恰喜欢0、2、3。等价mask重数为`{2:4,4:1,8:1,13:2}`；四主题可写为`S0=A`、`S1=B`、`S2=A∪{c}`、`S3=A∪{d}`，其中|A|=2、|B|=4且各块不交。两策略都根选0，全部实际终局均为011，三人收益(2,2,2)、福利6、最优三主题覆盖8。

简化策略第二位恒选1；末位全16行的矩阵为

| 首 / 次 | 0 | 1 | 2 | 3 |
|---|---:|---:|---:|---:|
| 0 | 1 | 1 | 1 | 1 |
| 1 | 1 | 2 | 3 | 2 |
| 2 | 1 | 3 | 1 | 1 |
| 3 | 1 | 2 | 1 | 1 |

初始有序策略只改两处：历史(1)的第二位行动从1改为2；历史(1,2)的末位行动从3改为1。其余19个历史动作相同。这里两个改动必须一起保留：

| 历史 | 简化策略指定 / 四候选收益 | 初始有序策略指定 / 四候选收益 |
|---|---|---|
| (1) | 1 / (2,2,2,2) | 2 / (2,2,3,2) |
| (1,2) | 3 / (1,2,3/2,2) | 1 / (1,2,3/2,2) |

收益均先改当前行动、再沿该份完整策略的真实后继计算。初始策略下根选1生成121，简化策略下生成112；根的该偏离收益在两份中仍为2。初始末位在(1,2)选1、在(2,1)选3，因而不依赖计数；简化矩阵对称，才具有计数依赖性质。两程序分别穷尽1+4+16=21个决策历史、84个含自身行动的比较，所有指定动作达到候选最大值，故两份都是完整纯SPE。不能由“实际路径与福利相同”跳过离轨策略核验，也不能把一般模型改成计数策略模型。

# 静态证书、真正安全值与输出内容

静态CCE定义在同实例同时行动博弈的任意有序终局分布μ上。每位i对固定标签a满足`E[u_i(s)−u_i(a,s_−i)]≥0`，偏离冻结其余终局行动，无顺序回复。令

\[
G_a(s)=W(s)-\sum_i u_i(a,s_{-i}),\qquad
L_y(s)=W(s)-\sum_a y_aG_a(s).
\]

若y非负且每个静态终局L_y≥b，则所有不对称相关CCE都有E W≥b。三程序按20个排序终局检查列；这是对玩家置换不变的**列**压缩，等价覆盖64个有序终局，并未把任意CCE分布限制为对称。

八客户两策略使用相同输入，静态证书自然相同。简单乘子`(0,1/3,2/9,2/9)`给逐终局L≥56/9；锐乘子`(0,9/29,20/87,20/87)`给L≥544/87。排序终局011、112、113、222、333上的总概率为`(17,29,29,6,6)/87`，各自均匀展开不同玩家排列后共11个有序支持。程序逐玩家、逐固定标签实算12项偏离损失，每位都恰为`(220/261,0,0,0)`，期望福利544/87。由下界与达到分布联合得到最低静态CCE锐值；不能只靠一个可行CCE的高福利推出最低值。

真正安全值竞争背景在不知道抽中查询标签前选两槽。原始查询p=(0,15,4,4)/23，十个竞争多重集背景的值分别为

| 背景 | 00 | 01 | 02 | 03 | 11 | 12 | 13 | 22 | 23 | 33 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 查询值 | 220/69 | 2 | 214/69 | 214/69 | 44/23 | 44/23 | 44/23 | 212/69 | 208/69 | 212/69 |

对偶背景11、12、13的概率为(3,10,10)/23，各纯查询值为(26,44,44,44)/23。两侧给v3=44/23，故W−3v3=6/23>0。输出保存上述十行和四纯查询值，但两套CCE乘子、p和对偶概率硬编码在程序中，未单独完整列在JSON里；复用完整证书必须连程序一起读。两策略的20静态行、达到分布和安全值字段逐项相同，唯一顶层差异确为两历史行。

# 四十二客户原核验器的准确合同

四十二客户按兴趣mask压缩如下，每份重数为不同单位客户：

| 喜欢的标签 | mask | 重数 |
|---|---:|---:|
| {1} | 2 | 17 |
| {2} | 4 | 5 |
| {0,1,2} | 7 | 3 |
| {3} | 8 | 5 |
| {0,1,3} | 11 | 3 |
| {0,2,3} | 13 | 9 |

该程序根0、第二层(1,2,1,1)、末位矩阵恰为上面的八客户**初始有序**策略矩阵，即简化表仅将(1,2)格改为1。动作表相同但客户不同，SPE必须重新核验。本轮原字节运行确实逐21历史重算84比较，最小margin为0；实际路径011、收益(11,21/2,21/2)，福利32；穷尽64有序终局给OPT3=42，主题123覆盖全部客户。

固定乘子为`(0,2/7,1/4,1/4)`。程序输出每个排序终局的W、四个固定偏离总收益D、G=W−D和L；20行精确最小值33在000取得。结合任意CCE的E G_a≥0，得到其福利至少33>32。**33是该固定对偶的列最小值和合法下界，本源没有给达到33的CCE；未认证最低静态CCE恰为33。** `optimum=42`则是三主题覆盖最大值，不能与CCE最优混淆。其half余额为2·32−42=22>0；本程序没有核真正静态安全值，不能把八客户44/23迁到这里。

完整42客户[本轮输出](../../tools/evidence/eight-and-forty-two-client-cce-exact-primary/rerun/forty-two-replay.json)包含21份真实后继终局和全部20个静态行。它是原验证器重放；同源数值发现点、整数缩小记录和另一独立审计各按自身逐源对象处理，不因本页运行原验证器便宣称已经读完所有相邻数据或增加独立审查人。

# 运行、比较结果与证据层级

从仓库根复验：

```sh
python3 archives/customer-attraction/tools/evidence/eight-and-forty-two-client-cce-exact-primary/replay_bundle.py
```

三个原程序均仅用Python标准库，未导入规范SPE求解器、LP、发现程序或其它原核验器；它们把客户和完整策略硬编码，不读取相邻JSON作为输入。默认打印完整JSON；若另给一个位置参数，原程序会向该路径写JSON。本批只取默认stdout，不修改原件。包装器核七原件的全部SHA-256，以未优化的隔离Python运行三个原程序，并将每份完整stdout与保存重放逐字比较，再与三份冻结八客户JSON逐字段比较。[verification.json](../../tools/evidence/eight-and-forty-two-client-cce-exact-primary/verification.json)记录真实通过结果；不是对实现正确性的独立新证明。

已实际读全仓相关正式反例、计算资源、2026-10-21运行审查、两个历史入口、静态CCE安全下界引理、弱CCE占用候选、另一条初次五主题策略锥证据及静态桥版本资源；还读了原正式八客户独立代码和原独审正文。逐字核对确认：本批主脚本等于现有正式主脚本；`exact.json`等于已存2026-10-21主运行；stdout仅多末换行。这些均为重复来源证据，不能算新独立实现。历史独审另写逐名客户和全部64有序静态终局，已经存在的独立审查身份保持原层级；本批原有序版与主脚本只改动作常量，因此亦不是它的替代独审。

另一条五主题初次策略锥证据的有理客户放大为43,426人，归一化下界3011/2950；它与此四主题42客户不是同一个实例。十三客户五主题锐值2785/297同样属于另一实例。文件名、同属CCE路线或旧claim别名都不能把三者的客户、对偶或最优值串用。

# 关系判断与接续边界

本资源与现有八客户反例是来源、实现和精确核验关系；与原始/对偶精确计算对象是同主脚本/同输出的来源补全关系；初始有序与简化计数策略是同客户实例的两份真实构造，静态证书由相同客户输入复用，顺序激励各自验证。四十二客户是同一发现链的另一输入及同动作构造复用，不是由八客户定理推出其SPE。七源的逐项去向与[人工关系说明](../../tools/evidence/eight-and-forty-two-client-cce-exact-primary/relationships.json)分开保存；本批不生成第三阶段图，不借重复字节制造新推导或审查边。

[静态CCE安全引理](../引理/静态粗相关均衡的安全下界与三单例严格间隙--引理.md)给一般n v_n≤最低CCE福利，其方向不能反转。八客户强桥W≥最低CCE已失败，而[较弱系数桥](../候选/较弱CCE福利桥的占用LP表示与边界--候选.md)、聚合真正安全值以及恰六人half各有不同量词，不能由这里的三人反例一并否定。八客户仍有half余额4，四十二客户有余额22；没有认证规模最小性、外部新颖性或外审。接续者可直接复用合法客户输入、两份完整策略与有理静态证书，提出新桥时仍须处理全部离轨和平局。
