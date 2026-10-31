# 共享程序操作：当前新题与旧存档兼容

当前主攻 UM-TARGET-v1，save=unrelated-machines。新对话使用[完整BOSS提示词](../unrelated_machines/BOSS_START.md)；启动、通信、私聊、个人桌面、同步、核验及提交的完整操作统一维护在[本题RUNBOOK](../unrelated_machines/RUNBOOK.md)。唯一程序仍为本目录tools/work.py，恢复后调用仓库内最新checkpoint.py和board.py，无需另传两个程序。

新建未绑定clone默认unrelated-machines；已有shared/其他save保持原绑定，新题另开独立clone。start回执显示绑定的研究README与提示词。首次显式指定新题save；后续从绑定复用，默认checkpoint按专题选择范围并仅追加本人桌面。显式paths替换全部默认范围，须列全本次成果；全部待推历史同时检查，真实冲突保留双方按内容处理。仅pushed且远端实际含提交才报告保存。

旧题接续须明确选择旧存档：既有shared clone照常使用；新旧题clone不互相改绑。全新旧题clone用如下命令（实际路径由agent确定）：

```sh
python3 research/weighted_congestion_frontier/tools/work.py start --save shared --actor <旧题唯一编号> --token-file <仓库外凭据>
```

旧题数学从[现行拥塞地图](../current/weighted_congestion/README.md)、MODEL.md和CLAIMS.md进入；其Cd/ln d存在任务已被否定，旧冻结Pro包不代表现行状态。当前prompts已转为新题，旧版可由Git历史恢复。

日常操作统一走work.py，避免绕过存档绑定。board.py是兼容底层：无save旧事件仍归shared，直接say/ack无save也走shared，直接view无save会汇总公屏。pending列本人clone的待发队列，retry保留原ID、原消息及原save；不会把旧待发改投新题。私聊是默认视图分流，同仓原始记录仍可读取。

新题[工程记录](../../evidence/runs/collaboration/active_topic_routing_release.json)说明本次实际检查和限度；旧版[十clone记录](../../evidence/runs/collaboration/incremental_chat_release.json)保留原测试版本。旧协作设计按收益采用，不作为数学研究前置。
