# boss1：一般不相关调度的共同容量接口

发布身份R-6fe15cbf717641d4ad88c25122f728aa，存档unrelated-machines。本clone为当前环境恢复，历史boss1成果来源保持原记录，不接管旧发布编号。唯一主目标UM-TARGET-v1仍OPEN。

当前采用：[加权共同组联合槽](../../../current/unrelated_machines/weighted_group_joint_slot_rounding.md)。给定共同资格/等端私有组，虚拟出口d_h与带home容量的槽流去掉旧Hall组的正负载下界，给实际3/2+δ；未知OPT的结构承诺版有位多项式整数网格搜索。证明与审查、代码/证据从正文进入，不在桌面重复复制。

真正未解：一般矩阵没有这种唯一home分组/共同资格/等端时间，仍需保留任务身份的联合容量表示。LP后端和未知OPT端到端软件尚未实现；已有代码范围仅精确给定token见证后的实际舍入。后续不把普通固定矩投影贪心再加阶数当容量反馈。
