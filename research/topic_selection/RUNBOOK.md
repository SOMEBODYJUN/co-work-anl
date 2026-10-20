# 独立选题分支的恢复、交流与保存

目标分支：`research/topic-selection-boss6-20261020`；save：`topic-selection`；角色：boss6，发布号每对话独立。此分支由用户最新明确要求创建。

先在独立clone的main用最新版work.py start --save topic-selection --actor 新R编号 --token-file 仓库外附件路径建立身份，然后fetch并switch到本分支；已有该分支clone保留身份并检查status后ff同步，**不要在本分支重复start**，因为旧start会要求main。本分支局部路由在active_research.json。

通信仍用research/weighted_congestion_frontier/tools/work.py read、inbox、send（save已本地绑定）。公屏在原wcg/board，按新save过滤；BOARD.md保存实际有价值讨论。

保存沿用同一work.py checkpoint，增加显式参数`--branch research/topic-selection-boss6-20261020`，并列全本次路径。默认仍只接受main，只有research/topic-selection-*可显式启用；当前branch不匹配即拒绝。原有凭据扫描、全部待推历史范围审计、普通push及远端fetch确认保持。分支须先已在远端存在；不得强推，不合并回main，除非用户另行决定。

重现各线实验见lanes与tests/audits/topic_selection。计算证据不升级候选。生成catalog/map/crosswalk后运行各--check、check_assets及check_wc_assets；不为通过旧main课题路由检查而把新任务伪装成UM。

本分支精确路由：`TOPIC-SELECTION-OR-OPT-v1`，save=`topic-selection`。
