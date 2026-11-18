# Boss3 Main journal — n6-boss3-20261118

## 2026-11-18：首次启动与真实派工

- 身份：Boss3；Main 的实际平台名称 `/root`；本次 session tag `boss3-20261118-live1`。
- 仓库：`SOMEBODYJUN/co-work-anl`；独立 clone `co-work-anl-boss3`；分支 `rebuild/research-v2`。
- 启动 HEAD：`e0b8e7d28c5164fbd5fd0ef689886c1279e380b7`。凭据留在仓库外，仅向启动与发布程序提供 `--token-file`。
- 存档：`customer-attraction`；子档：`six-providers`。按子档 README 将开题 spec 原样复制到本 RUN；未复用或覆盖其他 RUN。
- `research studio init` 已成功；原题、定义及其 SHA/section 由本 RUN `spec.json` 和两份 packet 固定。
- 原题：恰六名单位权提供者、任意有限单位客户、有限非空共同目录，对每一个完整历史纯 SPE 证明 `2W >= OPT_6`，或给原模型反例；允许空、重复、零客户和任意离轨平局。当前仍开放。

### 工作分配与输入隔离

| studio slot | 实际 agent | 角色 | 初始数学输入与义务 |
| --- | --- | --- | --- |
| independent | `/root/independent` | 独立障碍 | 仅 obstacle packet 的题面、定义节选、允许障碍和本人笔记；找原模型障碍或可复用局部引理 |
| informed-a | `/root/idea` | idea | 按目标超边及 Boss2 已发布成果提首选、实质备选和首个可证伪试验 |
| informed-b | `/root/execution` | 执行 | 实读两条已发布条件边的正文与证据，核全部前提与尚未覆盖范围，随后执行选中义务 |

三个真实子代理均按仓库默认 `gpt-6.1-sol / ultra / fork_turns:none` 启动。Main 的未报告配置不虚填。Main 仅读操作规则、spec 定位、超边和短回执；完整数学由对应工作者实读。Main 串行保存 RUN 事件、Git 同步和发布；工作者只写本人线路目录。

### 当前超边与路线决策

- `boss2-partial-fractional-cover-to-six-half`：只支付满足同一最优并集截断分数覆盖条件的实例；一般条件欠账保持开放。
- `boss2-four-extras-to-six-half`：只支付六个不交等大最大锚、锚外互异非空覆盖至多四种的目录。
- 两者是不同条件路线，不把它们合并成一般半覆盖证明。idea 先提出优先义务，执行线先核确切条件和结构缺口。
- runtime 将 Boss2 旧 spec 标为 `same_target_revisions`；idea、执行线须实际核 section 限定与原题模型适用性后复用。独立线不接收 Boss2 内容。

### 首次 checkpoint 范围

明确同时保存以下三处，不把初始化误报为已发布：

1. `archives/customer-attraction/subarchives/six-providers/workspaces/Boss3`
2. `research/workspaces/n6-boss3-20261118`
3. `research/runs/n6-boss3-20261118`

### 下一步

收 idea 的首选与备选短回执，交执行线一项明确数学义务；独立线继续原输入研究。实质结果先落盘，再串行保存；承重结果冻结准确字节、派非作者复核后才正式回流。原题未闭合，不把首次提交视为研究结束。

### 首轮 idea 回执及采用

idea 短回执确认 Boss3/Boss2 引用相同题面和模型 SHA；当前 section pin 仍固定同一原模型。首选是从四种额外覆盖拓展到 `q=5`，检验唯一潜在坏前缀能否由真实末二/倒三约束支付；实质备选是把连续客户目标权与最优六槽真实后继耦合。旧 `t=5` 约 0.4984 的数值只属松弛，不否定原题。

Main 选择 `q=5` 结构扩展，已实际发给执行线；idea 继续提共同前缀跨锚攻击暴露预算并向执行线给准确引用和首个区分试验。理由：它直接检验已证结构段边界，允许得到严格扩展或可定位的失败机制；更一般的真实行耦合保留为备选。两线均不得将松弛可行点冒称完整历史 SPE 反例。
