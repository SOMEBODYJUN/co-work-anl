# 配置正部阈值、严格单位五三界与闭合两树的独立审查

审查对象：[现行正文](../../current/unrelated_machines/unit_readout_configuration_threshold_polytope.md)。最终 SHA256：`b29c1500da407a86c3172c6738f22c5b10c073d0270aeac9acd668260983967a`。三个 ID 为 `UM-UNIT-READOUT-CONFIG-POSITIVE-PART-v1`、`UM-UNIT-READOUT-STRICT-UNIT-GAP-v1`、`UM-UNIT-READOUT-CLOSED-TREES-EXACT-CONFIG-v1`。

结论：限定范围的一般证明完整，未发现尚成立的内部 fatal。没有外审、新颖性或独立成文价值认证。UM-TARGET-v1 及其反面仍 OPEN。

## 1. 实际先陈述与全文读取来源

- `cover_consistency` 先只收到严格单位 gap 的精确 Claim，独立重构多数轨与半份额槽证明；之后才读冻结主文。先行稿 SHA `b99032920436970f5aaae6ca558e0bb44c3d67ec3609c3b4e531d7bc9b53c4fa`。其不同证明把 selector 固定、选轨所有边各半分；根 small 槽数 ceil(k/2)，非根 incoming 先放、small 至多 floor(k/2)，同样得五三和偶数三半。k1 单独容量流。
- `shared_label_attack` 先只收到正部多面体 Claim，独立给概率交必要性、模 q 圆段分解充分性、精确阈值搜索；再读正文其余部分。先行稿 SHA `7732da943b1a5d99cb39a3dd2d129693560cd7545e7914275877d0552222d1d6`。
- `pcsp_occurrence` 独立重构整轨 LP 与 CONFIG1 等价、正部行充分性及闭合两树层阈值，并编写不导入主舍入程序的局部原配置凸包审计。其局部审查稿 SHA `c4d8c7f312f9c4ca70df79a3bd0c2f1ad1014c0410f6964fe926819603ffd576`。
- 冻结初稿 `67fb7ba6ed462038459bee4f527469ebbd7ff9d231155959b11a7d5141eaf99f` 经 cover 全文攻击（回执 SHA `b7f4a3282cfb0a648698ed8c9dab184d29e1a6563b8c7848afcf005250561425`）及 shared 全文攻击（回执 SHA `0f1b0bcea31eb1d8c89d64fb54257a076b3e52013faa8160503c26f0ed5df7f2`）。这些回执没有把未读的实现冒称已审。
- 随后只新增 Evidence/Objections 字段、one-hot 应用和未集成全局 LP 的说明，形成 `d46d333b3263a602722e7a2c361f3aa2378a699f378db52e0bef291568d4235e`。cover 精确逆删除新增段恢复初稿，逐式核应用。最后把右端的负文字上界明确为 q−1，形成最终稿；cover 再实际读取并逆替换恢复 d46，确认核心三证明未动，最终确认稿 SHA `a153a3203e7ed586b628ea02b1efe1938d2f19a966cefc0a3e1399df2ba182ab`。

这些内部代理不登记独立 Work 身份；上述来源说明不作外审或同行投票。

## 2. 关键攻击与处理

**正部 iff 的充分方向。** 只给下界 lift z≥q−t 和总和约束时，任意 z 可能大于 q 或 small 的边际，不能直接当联合概率。正文取最小 c=(q−t)+；审计的任意 lift 分支先裁到 min(z,q,1−t)。余量都在合法概率区间。q=0、q=1、s=0 分别旁路，不除零。

**局部配置与全局共同性。** 每枚 small 串接圆段长度≤q，每点覆盖数≤s，所以含 incoming 的配置真实负载≤1+s/k。外机用 singleton。所有父/子边际必须共享同一组 t；局部分解不要求一个全局联合分布，否则已换成整数凸包。非空 CONFIG 阈值网格为 1+j/k，T=2 是独立全父置边界；空实例先返回 0。

**五三构造作用范围。** 多数轨仅保证 activearity≤2A，未选轨密度可以无界。未选轨直接全 parent，不能把强校准 LP 行强加给它们。active incoming 先槽、列和 1、一次 Hall 匹配共同计费所有原 jobs；root 和非 root 都包含，外机至多一 port。k1 不走多数校准，用容量整数流。存在实际 C1 时才必有整轨 LP；没有证明一般 OPT 的五三比例。

**严格阈值与近单位阈值。** s0 强迫 t_child≥incoming，整轨 LP 恰 CONFIG1；它没有使用超出本结构 CONFIG1 的强化信息。s1 允许一个 incoming 带一 small 同配置，层边际可衰减。闭合两树条件 `(k−s)^h≤2k^(h−1)` 经全层求和必要及均匀层边际充分双向核实。经典高度条件 α_h≥1/2 恰是 s1 条件；k≥3 又排 s0，因此经典 Tconf 精确为 1+1/k。不是从已有某阈值证书擅自推最小值。

**原文与新颖性。** cover 实读旧经典正文及仓库 Verschae–Wiese 原 PDF 的 Theorem 2、§3.1 和 Lemma 4，核原 P 与本重索引一致。趋二配置 gap 仍归属该已知结果；本资产只登记特定模型的精确消元、严格阈值合同与阈值回算。标准 ST、Hall、uniform-rank 分解均不获原创认证。

**one-hot 应用。** 每 vertex 的正文字上界 1、负文字上界字母数减 1。Q=sq 的均匀边际使 forward 值 `1+1/Q−1/q≤1`（s>1 通常严格），reverse 值恰 s。只有重复/平衡后仍保共同整轨 LP 见证的合法编译才适用；未声称已经构造完整 Label Cover 归约。

## 3. 实现与有限证据

[冻结输出](../../../evidence/runs/unrelated_machines/unit_readout_configuration_threshold_audit.json)由 boss11 亲自重新运行并精确回算，保留运行时正文 d46 哈希；最终只改 one-hot 右端上界措辞，未改三证明、代码或数值，未覆盖冻结输出。

| 程序 | 源码 SHA256 | 实际核验与界限 |
| --- | --- | --- |
| [整轨见证到原 σ](../../../tests/audits/unrelated_machines/unit_readout_literal_gap.py) | `8dfc9770be270a2ec561f3ee437154ec40d0052dd22847183d9a7a2e6b833b25` | 4337 个完整调度、59121 个原任务，另行按原边重算每机负载；15 非法输入拒绝。仅给定精确见证，无 LP/OPT oracle。 |
| [独立单行配置分解](../../../tests/audits/unrelated_machines/unit_readout_configuration_row_decomposition.py) | `f29825a80f05e1a34e10b49ed6f938233eb4cf388fb30cdb68ad984439c17161` | 1278 网格点：894 正点由原配置支持 Fraction 消元认证，384 负点以对每个原配置成立的精确分离式认证；另 9 边界。SciPy 只找候选支持/flag，不代替精确证书。 |

整轨程序复用既有模型、负载函数和 Hall matcher，未冒称这三个辅助独立；既有 core SHA `039ac7dbbfc0858aa9f51086ad8debb2b2f403b282e6a516ada328e2ebf175c4` 未改。boss11 亲读实现、独立手算 k3/h1/权重(3/4,1/4)/容量(3,1) 的七原任务，输出 σ=(0,0,0,2,1,1,1)、原机负载(5/3,1,1,0,0,0)，核所举 d>2A 是未选 clause1 的 3>2；该实例本身 OPT1，不能拿算法输出当最优下界。

`shared_label_attack` 最后另实际读此实现全文及最终主文，绑定上述两个最终哈希；静态核全部原 jobs、inactive 全 parent、active-only 槽、巨容量零机区间及 k1 分支，无 standing fatal，未冒称重跑 boss11 的 4337-case 运行。追加回执 SHA `2317e738aa21cf6e3e7177451240eae1aaa7c175f60d6779a39e06da4be3d58d`。

[输入例子](../../../examples/unrelated_machines/unit_readout_configuration_threshold_examples.json)另含 8 组闭合参数；冻结记录逐项保存最小 s、可行与前一网格不可行的整数幂比较、Tconf、OPT 及其精确比值。这些只作有限回算；一般公式由证明承担。

没有集成全局精确有理 LP 求解器、全机 CONFIG 输出器或整个结构类的任意 OPT 次二算法。数学上的标准 LP 调用与已实现的精确见证处理分开登记。
