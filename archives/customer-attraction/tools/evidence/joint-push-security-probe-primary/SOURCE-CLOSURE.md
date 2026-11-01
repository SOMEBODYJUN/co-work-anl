# 完整源码闭包及原文件不可覆写

original/<research/...R977/security/push_joint_probe.py>的parents[5]指向original，其硬编码R51/security/extra_mass_probe.py已按同一original根保全，仅该6785为运行helper。标准包+NumPy/SciPy是外部环境需求，版本未锁；未虚构pip冻结或当前import。前身2785同目录只作比较，不是runtime依赖。

main保护；原入口若直接跑会在自身OUT写push_joint_candidate.json或覆写push_joint_numerical.json。复验需另隔离副本/真实事件，不在冻结树调用。本次没有原数学入口、RNG计划解码或SPE/收益/IC/优化器运行。

negative报告原字节完整保，包括150参数，但未给w0/p/w/actions/Γ/求解器状态/原命令/源SHA绑定/退出日志。不能从seed重造旧游戏并称原逐字节PASS，未为了补日志重跑。正常报告不清旧candidate，缺失候选不作事实猜测。旧helper原source manifest保存归档来源身份，不冒本批新show。
