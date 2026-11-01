# 六人统一研究输入（本轮）

## 唯一成功目标

本轮 n=6 指恰六名单位权提供者，客户数及共同目录大小均任意。固定原 CAG-MODEL：有限单位客户 N，有限非空共同目录 S⊆2^N，提供者观察全部有序历史依次选一个主题；允许空主题与重复。终局每个客户在覆盖它的提供者间均分，u_i=Σ(1/c_x)，W=Σu_i=覆盖客户数。OPT_6 为六个目录主题的最大并集。

对每份完整历史依赖纯 SPE 证明 2W≥OPT_6，或者给出严格违例并独立核验全有序历史。SUCCESS_PROOF 必须覆盖任意有限客户、任意共同目录及任意离轨平局；SUCCESS_COUNTEREXAMPLE 必须是完整 SPE，不是必要条件坏点。其他进展一律 OPEN。一般 m 的命题另仍 OPEN。

## 六名研究员使用完全相同任务

各自独立直接攻六人，方法不限，无预分工、路线配额或开工审批。可证明、构造、编程、换表示；不以有限无反例或已有松弛坏点结束。具体任务随自己发现自主变化。报告必须给精确陈述、关键证明/证书、未付义务、致命异议及值得验证的下一问题。主方亲自核验并调度后续轮次。

## 必读与按需入口

1. 根 AGENTS.md；research/current/customer_attraction/model.md。
2. research/customer_attraction/RESEARCH_STATE.md、FAILED_ROUTES.md。
3. research/current/customer_attraction/five_player_half.md；其链接的 customer_attraction/proofs/half5_exact_v1/PROOF_ZH.md、ACTIVE_ROWS_ZH.md 按需读。五人已有完整精确计算机辅助证明及内审，未记录外审，不能用于任意背景五人后缀。
4. 通用已证工具：research/current/customer_attraction/priced_hidden_reply_projection.md；same_source_reply_requery.md。共同实际末位报价、共同 K、真后继IC及隐藏位联合投影有效；尚无六人half证书。
5. 当前必要条件停界：research/workspaces/customer-attraction/R-c4f1ef099fad483c9f81283b61eb0b53/parent/FRONTIER.md；R-c37d9a1010c64b649a1f8a0368eaf54d/README.md。3889关系上的精确坏点可重选Z扩张为满足全部60类Z→Z的共同分布（3949关系），W≈0.47704，O=1。不是SPE。不能仅重复这套闭包调权。
6. 新局部链接口：research/workspaces/customer-attraction/R-286ba747762f49e2bd3d5b1172910bce/chain_reply_requery.md。链式同源强制T→真末回复R→再强制R保留身份；全局链及K付款未闭合。
7. 若走势/自复制路线：R-c4f1ef099fad483c9f81283b61eb0b53/parent/potential_copy_candidate.md；R-291a34e2dbf4451aa0115fed89a7729b/README.md。局部ESM和BRANCH-MONO已FALSE；总势候选OPEN。若走promotion，R-23ab27f8efb44f1faca2699d45886250/general_n/zero_regret_promotion_reset.md 已有源IC及指定回放全部零但势下降的完整反例，不能用该源IC单独付款。

## 重要失效桥

SPE终局不必静态NE；最差静态PNE/CCE与强弱iid福利比较均失败。逐位置安全值/完整菜单保底、固定实际缩放背景精确税桥、冻结实际前缀整体归纳已失败。非根跨枝必须保留旧玩家最终利润变化。固定最优O与实际U，OPT−W=|O\U|−|U\O|，不能丢掉后项或把纯遗漏当净差。工具失败无数学含义。

## 工作与复核

共享clone为 /workspace/scratch/1055a6ebf2fc/co-work-anl，main；本轮身份 R-5c8174bb0fd241e4915f483831a37d0a。各研究员只写主方指定的独立子目录，不改共享地图/他人文件，不自行git、work.py或读取凭据。主方统一提交交流。未成熟但可接续资产准确标OPEN。

历史不作为研究状态依据；以上入口及实际代码/证据为准。原用户要求持续循环；返回时提供下一项可验证任务，不把一条失败或一次有限搜索当终点。
