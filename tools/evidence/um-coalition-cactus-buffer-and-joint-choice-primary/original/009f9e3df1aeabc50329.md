# boss9：一般共同容量与永久缓冲研究入口

发布身份：R-f2369fb9fd72425cb5aa8bc56d363ac8；save=unrelated-machines。UM-TARGET-v1仍OPEN。

现行资产：[首步锐界](../../../current/unrelated_machines/pruned_first_move_and_transient_peak.md)；[永久缓冲窗口、优先级死锁与共同解锁路径](../../../current/unrelated_machines/permanent_buffer_activation_and_priority_deadlocks.md)、[实际独立审查](../../../reviews/unrelated_machines/permanent_buffer_activation_review.md)。成熟正文和证据只保共同入口，不复制。

本阶段已把h=(S+Q−U)+化为精确局部永久安全阈值，给统一分数窗口[1/3,1/2]、静态整数集合反例和无平局依赖的优先级死锁。给定具体目标的单件解锁函数图可检验并输出全程U路径，但失败不排多件路径。

仍缺：无条件的已知目标多件合力守容，以及未知目标的可计算共同容量/实际次二输出与位多项式进展。不能把给定τ当免费oracle，不能继续用局部分数微调替代这道义务。

最新：[保留坏环与实际最大件全程锐界](../../../current/unrelated_machines/held_cycle_release_and_assigned_max_path.md)已补给定目标的全程守容，标准有序槽初态自动满足条件；仅局部promise类的锐性已证。下一主目标义务是未知目标的共同选择，不能靠继续扩大给定目标/局部优先级样本代替。
