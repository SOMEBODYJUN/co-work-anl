# 双副本六人历史标记策略

[程序对象](../../../state/程序/双副本六人博弈的历史标记逆归纳程序--程序.md)自足给模型、flag、精确整数BI及LP分层；[计算对象](../../../state/计算/双副本六人三种完整策略与冻结记录的版本差--计算.md)完整保三旧JSON与当前三证书、状态版本差及half余额。

original保4280B源和645/591/642B三原表。executed两脚本是本次真正执行的只读观察器和独立单位客户核，保原始工作区路径；replay各case完整保新report/stdout/stderr/参数/缓存、所有状态及终局pay、6个LP参数和返回、旧新对照。gzip里的非有限LP界以明确nonfinite_float标记保，不转成有理证明。

三case各原main1、DP1、LP6，源码未改，事件不重跑；观测约4.186070/3.041485/1.013574秒。独立标准库核总1次约2.946559秒，不导原程序/NumPy/SciPy/求解器，不重搜SPE，验证3×22425状态和280116比较。没有逐条展开全部有序历史；全12孩子闭合与确定转移的归纳证明提供完整覆盖。

便携run_original_cases.py仅将观察器的旧报告路径改为本包original目录，未重新执行数学；参数依次为本包original/disjoint_copy_probe.py及一个尚不存在的输出目录。便携verify_state_graphs.py参数依次为新三case输出目录及尚不存在的核验JSON路径。原执行适配器与便携路径版本都存，勿把后者称本次已执行字节。解释器/NumPy/SciPy实际版本见每case execution.json。

当前True策略有1053组相同计数不同动作，不能删flag。两个旧表缺oldpreferred且states18564，当前三case均22425；新False构造的相同路径不恢复历史未保存策略。独立核给W/OPT为68/72、72/72、105/108，全满足half；它不认证其他SPE或一般六人命题。manifest/self-check仅检查字节、JSON/AST和路径，不再算利润或跑LP。
