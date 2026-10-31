# 单强制根附节的 canonical 实际字节组合核读

内部研究者 pcsp_occurrence。此为已读 Exact/作者 proof 后的 **actual-byte 读后组合核验**，
不是新的盲审。不修改 repo、Git 或 Work；旧 first-review、read-after 和作者原稿均未改。

实际读现行文件：
`co-work-anl-boss11/research/current/unrelated_machines/private_injective_tree_configuration_floor.md`。
读取前后 SHA256 均为
`83a85165061420eb775335f81cd379643515b87ea385a1d7d885f0e9b2c1b703`。
已实际读取 S0–S6 全文，并读原 v2/v3/渐近前缀及对应 review 的新增单根段。

实际读 review 文件：
`co-work-anl-boss11/research/reviews/unrelated_machines/private_injective_tree_configuration_floor_review.md`，
SHA256 `692ca90ee42c0c11197d1267077a33f7f4057a50108445ca78e584dd649bcb6d`。

**结论：无 standing fatal objection。** 新附节与已审 Exact、作者 proof 和我两阶段记录的
数学对象、量词及结论一致，加入旧正文没有改变 G(µ) 的含义或旧结论。

## 1. 旧前缀的字节保持证据

对现行文件以首次 `## UM-SINGLE-PINNED-TREE-MULTIPLICITY-EXACT-CONFIGURATION-GAP-v1：`
切分，旧前缀去掉连接附节所加的那一枚空行、恢复一个末尾 newline 后，得到 34887 bytes，
其 SHA256 **精确等于** 已有最终前缀记录
`fc0f27a9202170b42c159a2b7d08b05eaff2bfd355c69e411df58154ee08f5f2`。
因此本次 v2、v3、有界 state 重数及 G(µ) 渐近前缀原字节未改，只有 append 分隔空行。
没有用“看起来相同”代替这项 byte-level 比对；也未访问或修改 Git 历史。

## 2. 新 S0–S6 的组合核对

- 正式域保持 d≥2、h≥1、一个 forced root、整棵 ambient tree 每色≤binary µ；作者 d1
  额外边界没有静默进入正式 Claim。单端 pin、每条边的两个有限端、颜色机器共享及全部
  I+L 枚 jobs 均明列。
- 新 S0 已补一般 U 的精确 `OPT=2−q/d` 反向：任意实际 C<2 由 pin 得 C≥1，每 active
  node 下传至少 ceil[d(2−C)] 条边，逐层抽同一 r 叉树；资源 unit 容量1给 rainbow。
  这补齐作者原稿只对特殊族明列下界的整理缺口，没有加最优 q 可多项式求解的声称。
- S2/S3 的 raw-q 次可加、occurrence bucket、sentinel DP 和完整 σ 回填均保留。只按实际
  m≤叶数创建 bucket，µ 巨大时不产生伪多项式循环。对所有原 jobs 而非只选中叶给调度。
- S4 的 µ|d 底层 block 族使用全局互异的 parent/block 色号，实际每色恰 µ。q=d/µ，
  整数 OPT、active 配置 unit+一 small、inactive 全 small、每资源的 µ 个 singleton
  加 empty、父子边际恰补1和 T<1+1/d 的根传递矛盾，均与已审证明一致。
- S5 高度 h=d ceil(log2µ) 及 d 沿 µ 倍数趋∞给的是 sup，不将有限族 ratio 当极限值。
  root 已按本轮 Exact 仅保 sup；作者原证明中有限不取到的额外讨论没有扩成这里的新 Claim。
- S6 的明确复杂度仍按显式 d^h 树与完整配置证书；没有 poly(binary d,h) 展开承诺。
  单树 S_µ 与多 root/state 的 C_µ、G(µ) 保持区分，未把 2−1/µ 写成旧 G 的固定参数精确值。
- CONFIG gap 只排除相对同一 LP 阈值的统一舍入合同；易解族、µ 无界时缺少统一 epsilon、
  以及 strong near-full vs weak δd rainbow 的困难性仍明确分层。没有 UM 主目标升级。

## 3. review 顺序和四份源原字节

新增 review 段如实说明 cover/root 先有机制，pcsp 只收 Exact 自行重构，随后才读作者 proof。
未将其改称全员盲审或外审，未将新数学证明当有限软件核验。
实际另算了 repository 中四份 frozen source 的 SHA，均与先前原件一致：

| Source | SHA256 |
|---|---|
| Exact | `32469690f6f96128c1e56a9080787f83345553623492e18819f29a600f7b692b` |
| Author proof | `10ff5f08b67f01de019ff5cdb328b1275d6c80b560d6095adfba8e06e86c7913` |
| pcsp first-review | `b5ecdb360057776518e05cf9d38be5517ebcc13868bc1574e92708520cee410c` |
| pcsp read-after | `4d619a6fa32cd7d99e57c819fd12f54741b0a76c144b5483b3e38c26d678bdf1` |

本回执只认证上述实际字节的数学/来源组合范围。没有新增数学软件实验，没有亲跑未提供的
实现，没有新读外部 Haxell/AFS primary 或认证全局新颖性。UM-TARGET-v1 正反面状态不变。
