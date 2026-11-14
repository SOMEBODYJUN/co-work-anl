# 3036 修复冻结交接

任务：`boss2-wave22-um-repair-303633f45e196d68`，本地已发布任务快照为 claimed / Boss6；远端归属由派工 Boss 在本轮发包前核定。本 worker 未调用 Git、sync、队列、公屏或共享 registry/coverage/integration 写入。

## 实际完成

新收据：`map/receipts/boss2-wave22-um-repair-303633f45e196d68.json`。

- 覆盖全部 25 核心：12 linked，13 isolated-after-review，无 needs-decision。
- 旧批 10 资产逐条 retained 原路径及原 SHA；8 whole、1 conditional step、1 checks context。没有新增或改写边。
- 收据显式 supersedes 旧批 3826ce；旧 task、receipt、10 边原字节保全。
- 34 个任务输入 pin、95 个 task reading-ref 的 SHA/唯一标题绑定通过。
- 本轮直接调用与 CLI 同实现的 `research.check_edge`，10 边全部通过当前端点、证据及 review binding 校验；并独立通过原生 coverage、supersession、follow-up 校验。这些结构核验不代替数学判断。
- repair/旧任务均无 declared follow-up pair，`closed_overlaps` 与 `follow_up_tasks` 保持空。共享 read 端点没有被自动当成 closure。

## 数学复核

旧登记批中 simple-support 的对象 hash 恰命中旧任务 pin；与当前对象逐字段相比，只变 `version`、`objections` 勘误注及一份资源证据 SHA，model / statement / quantifiers / assumptions / body 等全部相同。资源修订身份可核 Boss3 的 `source-errata-20261113.json`。本轮取得并全文读当前资源，未取得旧资源 SHA 的字节，不提供旧原句，也不把 handoff 或遗失草稿当已读/已运行证据。

路径占位版本每 job 两端：峰 <2 时 k−1 个 unit blocker 必须占据互异终端，至多一星下传，incoming 父的局部负载至少 2−1/k。全 mandatory 匹配查询不能省掉这些 blocker，因此该族会被完整过滤拒绝。共享 z:1/2 是给 blocker 新增第三端的不同输入，只有它的独立查询可假定其它簇使用 z 而首轮不删边。真实共同 z 容量仍由至少四个活跃末簇的下界约束。

simple pair 不蕴含 CONFIG 伪森林：只看一个末簇就有 k+1 顶点、2k−1 边，环秩 k−1>1。LST 伪森林则是给定 LP 顶点的 task–machine 正支撑，结论是加性单件损失而非 CONFIG 阈值精确恢复。当前 simple-support 核心继续 isolated-after-review，未把配置 gap 说成算法或复杂度下界。

本轮新局部 Fraction 核验：k=1…32 终端 singleton 概率及各 blocker 覆盖；k=1…12 全部路径方向中的互异占位；k=4…8 强制 incoming 的局部星/路径簇完整端点分配、最优峰与环秩；k=4…32 仅核原 escape 高度及负载/比值公式。程序与完整结果在本目录。没有重跑历史整树 CLI，也没有把局部数值当一般证明。

不变部分复用已发表成熟比较。收据逐对象注明原批实读归原作者；本轮读取当前 34 登记和 10 边全部语义，以及 simple-support 四份证据、LST 资源、CONFIG 伪森林审查全文。未冒称本轮全数学阅读全部 95 reading-ref 或全读所有历史源码。

## 保持开放

一般 UM 统一次二算法与近二 hardness、PCSP 到 UM 的物理复制、稀疏转移的 Fδ / YES 完整调度 / 任意低 σ 共同证书提取 / 匹配 source hardness，以及稳定 CONFIG 证书生成等仍按各自原义务开放。保留的 decoder 边仅付最终 conditional step，私有程序边仅作 checks。

冻结后供 Boss 保存、确认 pushed 并 done；本 worker 不再改写收据或旧资产。
