# M-69317c7da9a34834b0e93efeaa77f0ef：完整实读与比较审查

## 任务与阅读范围

本审查由 fresh Solver（内部词 `SOLVER-693-FRESH`）完成，任务为 `customer-attraction-3a-3a-a37d9a24b357c2d8`，核心对象为 `M-69317c7da9a34834b0e93efeaa77f0ef`，输入 pin 为
`ace38ac5a46649f9a3fbfd8510f73f5891edd834d828c02a6ad2f5057362d37b`。完整读取任务声明的六个来源；14 个 staged reading passes 中，`all-node-comparisons.json` 按任务分成九段顺序读完，另五段分别读计算正文、保存的八主题 JSON、审计脚本、程序正文和原始攻击源码。没有依赖未列入本任务的库文件，也没有新增 read-add。

| 来源 | 字节数 | SHA256 | 实读用途 |
|---|---:|---|---|
| `archives/customer-attraction/state/计算/级联发现的四份历史与三种完整单位客户见证--计算.md` | 11087 | `91a0609e0777740d3d9a2cc52c48738b73eab8f259f587010e414179a78208ed` | 三个冻结见证、历史快照、精确审计范围与未付量词 |
| `archives/customer-attraction/tools/evidence/cascade-original-nine-boss3/original/32a1144af6be4485825a/cascade_m5p8_private_best.json` | 555168 | `aa29afb287c88842d94343a6be4ed3d092768079c128d0cfed4dd3dd24d95875` | 本对象 16 类型输入、目标、完整策略和保存值 |
| `archives/customer-attraction/tools/evidence/cascade-original-nine-boss3/audit_saved_certificates.py` | 9975 | `fcabfa55861ef055656e4efcd582c40812523e8d97e51359edb8800cea0866c9` | Fraction 全历史检查合同、比较计数、私有条件和 OPT 检查 |
| `archives/customer-attraction/tools/evidence/cascade-original-nine-boss3/exact-review/all-node-comparisons.json` | 4655076 | `a2024dfaba83de8020c623e767e8a49d7af0c8da8f5ee5b3e4945def785578cd` | 三份策略的全部节点/动作/余量；完整解析本对象 4681 节点数组 |
| `archives/customer-attraction/state/程序/锚点缺口级联的完整策略锥与三个版本输出合同--程序.md` | 9840 | `dedfc97f50455fb825dd0d768e3af8b9138eef619af5e791fabb6bbb44dbbfa5` | 精确 R(k) 递推、完整有序 cone、LP 仅候选、历史版本边界 |
| `archives/customer-attraction/tools/evidence/cascade-original-nine-boss3/original/f08bcbcb7a5f6f2bd41b/cascade_attack.py` | 11920 | `8da523673bf451f63bbdedc79a0efa906492481e4d18e61274a6873df7ddd8c8` | Engine、`cone`、`recover`、`optimize`、私有 floor 与输出控制流 |

原成熟 `audit_saved_certificates.py` 事件已在计算正文中记录为一次标准库 Fraction 审计、断言开启、返回码 0；本轮没有把重跑该成熟审计冒作新运行。此轮重新解析了保存 JSON 和全部节点表，确认结构和统计，未运行原发现器、LP/MIP、BI 或规范 solver。

## 核心对象的模型、量词与精确结果

这是五名单位提供者、八个共同标签的均分吸引博弈。每份完整纯策略为全部长度 0、1、2、3、4 的有序历史指定动作；离轨偏离沿同一策略在改变后的真实历史继续，允许重复动作、历史依赖和平局。因为
`1+8+64+512+4096=4681`，本对象的动作表必须且确实包含 4681 个节点。

保存输入的 16 个正类型（标签以 0…7 编码）及重数为：

`{0}:1, {1}:1, {2}:3, {3}:198, {0,3}:1, {4}:198, {1,4}:1, {5}:3, {0,1,5}:985, {6}:198, {0,6}:1, {0,3,6}:3, {7}:1, {1,7}:1, {2,7}:197, {1,4,7}:3`。

总客户数为 1795。目标终局计数与证书的 `terminal_counts` 同为
`(2,2,0,0,0,1,0,0)`，完整实际路径为 `(5,1,1,0,0)`；五个实际玩家的利润均为 200，故实际覆盖福利 `W=1000`。保存比较组合为标签 `(2,3,4,5,6)`，覆盖 1791 个客户；对全部 `C(8,5)=56` 个五标签组合的成熟核验给出 `OPT=1791`。因此本固定输入/固定策略的精确比值是 `OPT/W=1791/1000`。

八个标签的私有客户重数为 `(1,1,3,198,198,3,198,1)`。每个均满足 `1000*n_{\{a\}} >= W`，所以八个物理覆盖集两两不等、互不包含且均为极大主题；该输入不是普通/pilot 九客户点的同覆盖别名。

## 完整 SPE 资格与程序输出的分层

审计脚本按精确 Fraction 计算每个历史的真实后继终局和每个替代标签收益。对本对象的完整节点表，`4681*8=37448` 项含自身比较，非自身比较为 32767，严格非自身余量为 31208，最小余量为 0，且没有负余量。节点深度分布为 1、8、64、512、4096；解析的所有历史键恰等全域。保存的实际路径、终局计数、W、OPT、私有 floor 和 `distinct_maximal_themes=8` 均相容。

这些数字证明的是：给定这一个 16 类型输入和给定的 4681 节点完整策略，所有真实离轨比较都通过，即一个有限完整 SPE 证书。它们不证明这个输入的所有 SPE 都有 W≥1000，也不证明 1791/1000 是该目录的最坏效率，更不证明五人/八标签全局结论。

原程序的 `Engine` 先以 LCM 缩放收益，对计数状态递推完整可实现终局集 `R(q)`；`cone` 再保留每个有序历史而展开目标终局，`recover` 对浮点 LP 候选做全行精确有理回代，`optimize` 返回固定策略/固定 portfolio 的有理覆盖值。`cascade_m5p8_private_best.json` 的字段 `best_ratio_lower_bound` 和 `row_scope: all ordered histories` 因而是程序输出及固定点见证，不是全局最优或普适下界。m=5 时 LCM=60，原程序的 int16 系数在本输入范围内安全；程序正文同时明确更大 m 可能越界，不能外推实现域。

## 与共享算法及近邻对象的关系

本任务只交一条上下文实现关系：该有限策略/证书实例实现 `CA-CREDIBLE-CONTINUATIONS` 的可信终局接口（边文件为 `implements`、`relation_mode: context`）。本对象的 `R(q)`/有序展开、实际孩子保留目标、离轨孩子按门槛递归的代码路径，与算法的 max-min 可信菜单语义相符；完整 Fraction 审计支付了本实例的实际策略资格。此上下文关系不把本有限输出提升为算法的全称证明，也不把算法反向当作本对象的全局优化证明。

同一计算正文中的七主题对象 `M-44d519528ba04dd3b348a9bdb1c31d16`（123990 客户、W=69000、OPT=123852、比值 10321/5750）共享程序和审计材料，但其 p=7 输入、动作表和量词独立；两者相同比值或共用来源不产生迁移边。本轮没有把 M-44 的证书、普通/pilot 九客户别名或其它历史快照当作本对象前提。既有 `CA-CREDIBLE-CONTINUATIONS` 关系仅作为算法接口的语境比较，未发现需要追加 read-add 的数学缺口。

## 保留的边界和未付义务

- 1791/1000 小于 2，只是这个合法八极大主题输入的一个有限 SPE 见证；没有否定或证明一般 half 命题。
- 任务不支付该输入的 `min_SPE_W`、全目录最坏效率、全八主题策略族、五人全局最优性，或六人 half 问题。
- 109 条历史摘要、`best` 文件名、有限 queue/rounds 和浮点 LP 候选不能替代完整搜索或全局对偶证书；保存的 `source_ratio` 也不是本对象的全局 bound。
- 私有 floor 只保证本输入的八个物理覆盖集不同且极大；它不把主题标签商成更小目录，也不把共同定义当 hub。
- 原始程序的实现安全范围（例如 m>5 的 int16 风险）与数学模型的全称量词分开，不作实现外推。

本轮未修改 registry、Boss、其它任务或共享源文件；仅在任务 write path 下保存审查、支持、阅读账、单条边和回执。
