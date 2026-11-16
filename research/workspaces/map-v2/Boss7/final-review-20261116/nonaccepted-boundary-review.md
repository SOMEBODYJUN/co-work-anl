# 六条非 accepted 边的定向边界审读

审读身份：Boss7 fresh 3D 收尾；日期：2026-11-16。范围仅为下列六条边、其承重定义/主文、已有有限输出中的相关字段，以及它们的原收据、有效替代收据、当前 coverage 与 integration。没有修改 canonical、旧边、旧收据或任务状态；没有 Git、同步、队列或公屏操作；没有重跑 LP、完整 DAG、矩阵生成器或已有有限审计。

## 结论

本快照 `research/registry.json` 的 2669 条边为 2663 accepted、5 proposed、1 rejected；非 accepted 正好是本次指定的六条。六条均已有准确数学处置。本范围未发现需要纠错的数学断言，也没有真实未承接的比较。五条 proposed 均明确是 `checks/context` 的有限比较和范围说明，不能因状态文字而自动升级、重开或据此创造任务。rejected 一条精确切断 ordinary fanout 到 MinRep 列表一致性的直接迁移。

这不否认端点正文中已有的精确有限定理、必要行引理或完成性障碍。需要区分的是：端点的一项数学结论已经证明，不等于这六个边文件已提供把源端点整体迁到目标端点、完整 SPE 或全称 half 的证明。它们不应进入 accepted 数学支持的统计；根 Boss 已核的 build 仅投影 accepted，与当前处置相符。

| 精确边路径 | 当前处置 | 审读结论 |
| --- | --- | --- |
| `map/edges/Boss7-b10-sparse-3b-3b-260289906ca15fc4/comparison-support-caps-do-not-transfer.json` | proposed / checks / context | 固定八列菜单的支持复杂度与纯列阻断比较完整；不证明一般混合菜单、其他复制块或六人福利。 |
| `map/edges/Boss7-zdiag-3b-3b-b4950386c87b69e1/diagonal-split-3b-comparison.json` | proposed / checks / context | 3945/4005 必要系统前缀、旧点 Fréchet 障碍及重构坐标分离已核清；不形成反向 SPE 实现或 7931 当前点认证。 |
| `map/edges/customer-attraction-3a-3a-554652f680a7d85f/finite-relaxation-route-boundary.json` | proposed / checks / context | 同一对象内部记录有限 LP 精确值及保存点不可保持 AB 补全的边界；不反驳全模型 half。 |
| `map/edges/customer-attraction-3a-3a-ac3d3b6b379cfb23/finite-lp-to-boundary.json` | proposed / checks / context | 明确固定三个 LP 最优保存点的遗漏首动作使任一真实尾 BR 都造成严格首位增益；只切断指定升级路线。 |
| `map/edges/customer-attraction-3a-3a-ac3d3b6b379cfb23/partial-vs-complete-tail.json` | proposed / checks / context | partial-chain 的 p=6 与 complete-tail 的 p=6 数据、IC 域及背景不同，不能互换；保存点与搜索全域最优也不同。 |
| `map/edges/unrelated-machines-3a-3a-f294691cc06b0401/um-feder-ordinary-fanout-does-not-preserve-minrep-list-coverage.json` | rejected / transfers / conditional | 普通单标签 CSP 扇出不能免费提供 MinRep 的逐边列表见证一致化；三点 identity 路径精确反证这一推步。 |

## CAG 的完整历史与有限证据为什么不能互换

`archives/customer-attraction/state/定义/共同目录完整历史模型--定义.md` 的策略是每层在全部有序标签历史上的函数。偏离必须沿同一策略在改变后的历史续行，所有离轨节点与最佳回复平局都保留；同负载历史可有不同续局。目录为标签集及覆盖映射，不能免费合并同覆盖异标签。六人目标量化全部目录和每份完整纯 SPE，结论是 `2W≥OPT_6`。非零合法背景下尾利润一般不等于终局覆盖；外生负载还须由同目录的真实前缀生成。

因此，以下三层各自有效的有限结论，均不提供完整历史策略的反向实现。

### 固定八列稀疏菜单

稀疏定理使用 B10 同一八人、八标签、32 客户的完整纯 SPE DAG。列是在同一策略下强制根行动后的真实八槽终局，原根仍在列中；行是独立新增的一名查询者，分母为 `1+c_x`。外部列分布 Q 是有限矩阵的分布，不能当作原顺序博弈的混合或行为 SPE。

固定 K 的支持上限 1、2、3、4 至 8 的精确值依次为 `37/10`、`123/40`、`1717/560`、`851/280`，根实际收益 `u=13/4`。每纯列都有异块 D 查询给 `37/10>u`；两列均匀 D 已把全部查询压到 `123/40<u`，三/四列进一步下降。正文给出 C/D 降幅下界及无约束匹配原始/对偶证书，既没有把原两列可行证书误称全局最优，也没有把固定 K 的支持界外推。

这个完整 SPE 的实际叶覆盖全部客户，`W=OPT_8=32`。故它确实否定指定纯列封顶加强式，却不构成 half 坏点。同一策略实现条件 R_n，尤其 R4，及其所有离轨 BR 仍是另一个数学义务；不能把复制矩阵代数当作实现。该比较已完成，保留这些研究义务不等于需要重开图任务。

### 3945/4005 对角必要点

基础点是固定 `1 K +16 hist +582 joint +1306 overlap=1905` 坐标上的精确有理向量。它通过 `3945=3889+56` 条所列必要行并有 W<1/2，但不是精确最优性声明。56 行来自同一真实策略逐条成立的 16 类 R 与 12 类 Z 行，分别对 30 个异索引、6 个同索引求和；每对逐列合回原行，容量为 `30K+6K=36K`。该合法性是必要方向，不是把任意非负合行武断拆开，也不是任何有限可行点都能成为 SPE。

旧点的 1306 个辅助 overlap 只受非负及两个边缘上界，189 个低于真实 Fréchet 下界。最短自足证据是保存列 992：同一正 hist 块质量 h，两个 R 事件边缘都为 h，而保存交叠为 0。真实共同测度要求交叠至少 `h+h−h=h>0`。故旧坐标不能原样解释成共同会员测度；这不否定旧必要系统可行，也不否定全部其他点。

4005 点保旧 K/hist/R 边缘，在 22 个 R slab 上重新配置 275 个 Z 质量，并在**新坐标**验证 `4005=3945+60` 行。43 个正有理代表原子可恢复全部 582 joint 和1306 R-R 积分；但重构相对旧点改变 62 joint、193 overlap 和45 个 Z 边缘组，因而不能免费迁移旧点的全部数值语义。共同会员实现仍未规定完整目录、同节点一致策略、全部合法查询和全部有序历史 IC。

7931 后继虽描述符和 W 相同，仍改变103个 Z 质量；它另有120个 PAIR 槽及1903个 overlap 的两上界，历史报告与现冻结生产码还须保各自来源。当前4005证书不认证后继，也不能把后继可行性搬回当前275数值。边文件正确保留这些精确分离，没有把“行更多”或“W 相同”充作继承证明。

### 三个有限链 LP 与完整两人尾

链模式始终只有两位剩余提供者，深度 d 是固定回复模式长度；`p=2d+4` 不是玩家数。域为 `d=1,2,3`、`b=0..4`，保留 `r(0)=1` 和 `r(a)=a+2 (2≤a≤p−3)`，共有17/39/69条非自身行。缺失的是首动作 B、p−2、p−1 及其完整真实续局，已规定节点仍比较全部末位合法标签。

有限 LP 精确值 `10/9,90/83,670/621` 由非负有理原始点及逐原子对偶余项支付：`γP−D=Σ λ_i M_i+Σ R_j w_j≥0`，保存点达到等号。该证明只覆盖指定6705个有限原子，不覆盖 b≥5 或任意深度，也不证明所有真实 SPE 满足某个统一的指定链模式。

完整两人补全的准确条件是：对每个未规定首动作 a，存在一个真实末位最佳回复 t，使首位收益不超过实际 u。三个保存点在 B 后的全部真 BR 都是两末端标签，首位严格增益分别为 `1/9,7/83,49/621`；末端首动作后的唯一真 BR 为 B，严格增益分别为 `2/9,16/83,116/621`。因此任何平局选择都不能保持该保存点的实际 AB。这是固定保存点及指定路径的全 BR 障碍，不能扩大成整个 LP 最优面不可完成、有限游戏没有其他 SPE 或全模型 half 为假。

另一个 complete-tail p=6 保存点通过全部35条非自身行，值为14/13，既不同于 partial d=1 的17行/10/9点，也不共享其支持。原六标签每一标签都碰某个要求背景为零的新客户，任何非空过去行动都会破坏这些零负载，而空前缀又不能产生旧客户负载一，故该外生背景不由原六标签生成。加入 E 后必须核所有新增偏离；正文将已另行认证的31客户合法背景版与27客户零背景版分开保留。p=4/5 的保存点值为1、可用 AAA 前缀实现背景，但历史浮点搜索未保全每表精确上界，不能从“最好1”推出全表定理。三条 checks 均准确保留这些边界。

## 普通 fanout 到列表覆盖的被拒迁移

Feder 的普通图 CSP 对象固定有限 Boolean 模板和常量，每变量恰出现两次；gadget 外端出现一次、内部两次，二部实现还需外端同侧。恢复扇出使用排除 Schaefer 易解支及非广义拟阵交换失败。它的存在量词选取一份单标签赋值，不提供 MinRep 低费用 copy lists 的同时 soundness 或任意列表见证的一致化。

被切断的具体推步是：给 incidence copies 加 ordinary 等值/蕴含扇出，然后把每条新旧边各自存在兼容列表标签对，当成所有 incidence 可选出同一个标签。最小证据为 identity 路径 x–y–w，列表依次为 `{0}`、`{0,1}`、`{1}`。边 xy 由 `(0,0)` 覆盖，边 yw 由 `(1,1)` 覆盖，总费用4≤3g（g≥2）；但任何单一 y 标签均不能同时等于0与1。形式上，`∀e ∃ witness_e` 不能换成 `∃ shared label ∀e`。

无列表限制的 identity 路径本来可完美满足，且该三点路径并非 v3 正规平衡低值输入，所以它既不否定 Feder 定理，也不否定 v3 随机高围长源。v3 独立保持原 type/layer 的 repair 取 `z≥GB+4U+1>GB+4U`，在排除≤GB+4U个候选后留下 clean edge；覆盖误差对全部 lists 统一控制。这个正确 repair 余量没有额外引入共同标签见证。边的 rejected 范围精确，没有扩大否定 promise/物理编译或其他独立源。

## 当前 coverage 与有效交付链

| 对象 | 当前 canonical coverage | 实际承重情况 |
| --- | --- | --- |
| `CA-TWO-BLOCK-ROOT-MENU-SPARSE-VALUES-v1` | linked | 由 accepted `ca-b10-pure-menu-specializes-to-two-block-sparse-mixed-values`，非本 proposed checks。 |
| `B10-PURE-FULL-ROOT-MENU-NO-v1` | linked | 上述 accepted specializes 及 `ca-two-block-pure-menu-realization-to-stationary-source-failure`。 |
| `customer-attraction/diagonal-basic-row-split-exact-necessary-point` | isolated-after-review | 有精确有限点和不可字面实现证据；本比较不造完整逻辑边。 |
| `customer-attraction/diagonal-reply-budget-split-basic-graph-program` | linked | accepted 强PAIR局部贡献及其他行/诊断比较；包括 `boss6-f2b3-strong-pair-pays-both-diagonal-split-z-pair-rows`，只支付其明确 contribution。 |
| `customer-attraction/zz-diagonal-split-rational-necessary-point` | isolated-after-review | 当前共同会员 lift 不等于完整策略。 |
| `customer-attraction/finite-reply-chain-protected-omission-relaxations` | isolated-after-review | 只有范围精确的有限 LP 与路线边界 checks。 |
| `M-2ca8a524bdb746d286d02ddb687f380d` | isolated-after-review | 三个保存点的完成性障碍与两条 context checks。 |
| `customer-attraction/protected-omission-complete-two-player-search` | isolated-after-review | 保存点认证、背景边界和搜索范围已区分。 |
| `UM-SOURCE-FEDER-ORDINARY-FANOUT` | isolated-after-review | 被尝试的列表一致性迁移 rejected，没有 accepted 承重边。 |
| `UM-PARTIAL-MINREP-REGULAR-HIGH-GIRTH-SOURCE-v3` | linked | 由独立 accepted regularity/degree/条件费用/间隙边，不由 rejected fanout 支付。 |

原收据可能把 context 边放在自己的 `edge_ids` 字段，但状态仍为 isolated-after-review；当前 canonical coverage 没有把这些非 accepted 边计作 linked 的支持。

| 原/当前任务 | 当前静态任务与 integration 核对 | overlap/后继处置 |
| --- | --- | --- |
| `Boss7-b10-sparse-3b-3b-260289906ca15fc4` | done；integration 有当前收据 pin | 固定矩阵到更广菜单/half 的比较已交；未付研究义务明确，无后继任务欠接。 |
| `customer-attraction-3a-3a-f5d8acecff979b30` → `Boss7-zdiag-3b-3b-b4950386c87b69e1` | 后继 done；integration 有当前收据 pin | 原 f5d8 两个 follow-up 分别是 ZZ 点对基础点及拆分程序；后继把三端点联合比较，两个实际问题均已付。后继 definition 未声明新的 overlap，故 `closed_overlaps:[]` 并非漏处置。 |
| `customer-attraction-3a-3a-73120b839d4f39dc` | 原范围已交并有 closed-overlap no-edge 理由 | 其基础点/普遍拆分引理量词区分已解释；现又有上列3B完成。当前 coverage 合并保留“尚无已发布3B successor”是该旧3A的历史句，上方当前3B范围已记完成，不产生待接任务。 |
| `customer-attraction-3a-3a-554652f680a7d85f` | done；integration 有当前收据 pin | 内部有限路线边界完成，follow_up_tasks 与 closed_overlaps 为空符合实际。 |
| `customer-attraction-3a-3a-ac3d3b6b379cfb23` → `boss5-protected-chain-receipt-repair-896ebd8961cc4ece` | 有效替代 done；integration pin 有替代、没有旧任务 | 五项原资产逐项处置：两 context 边、review、support 沿用，新 readledger 替换旧不匹配账本。相同三端点比较已完成，没有遗留 overlap。 |
| `unrelated-machines-3a-3a-f294691cc06b0401` → `um-minrep-source-errata-round23-repair-35e394144898adda` | 有效替代 done；integration pin 有替代、没有旧任务 | 八项原资产逐项处置；三项关联资产在原路径重绑当前 v3/勘误，五项独立资产沿用。本 rejected transfer 保持方向及精确三点反证，无未接比较。 |

以上是本地已发布快照的实读核对，不声称重新读取远端实时队列，也不受另三项在途 source repair 的 A pin 影响。

## 仍开放的数学与本轮读取边界

仍开放的是各正文已明确保留的研究问题：一般 mixed-menu 的实现/支持复杂度与 R_n；由必要点到完整目录全历史策略及全部 IC 的实现；7931 实际点/代码合同下新增行的独立核验；任意深度或更大背景的有限链理论；从合法尾背景到根 SPE 实际可达性；MinRep 到 promise/物理 UM 编译和全输出 decoder。它们不能由这六条边解决，也不是本次发现的新未承接比较。六人全称 half 仍保持独立问题。

实读了六条 JSON 全文；共同目录定义全文；八人稀疏定理与完整DAG/混合证书计算主文全文；基础3945点、56行程序及ZZ4005点主文全文；有限链障碍及完整两人搜索主文全文；Feder 文献整理、v3 Exact 及三源审查正文全文，并读冻结读后稿§5的正确非严格/严格号。有限证据读了已保存三份 chain replay 的全部末位矩阵、completion/严格增益字段，`audit.py` 的份额、行、全BR补全及对偶核验逻辑，旧 overlap 障碍的列992短证据及ZZ point-audit的来源、改坐标和后继字段。没有声称本轮逐项再读/重算全部DAG节点、6705对偶余项、3945/4005行或所有原子。当前 coverage 的外部 accepted 边只核 ID/状态/作用范围归属，没有扩展成重审这些边的全证明。
