# 六人候选整数核验器

主源1b7f005abf2fb92f064a；[4012B原码](original/verify_policy_candidate.py)SHA80657032a9aef3f6000634fee03f87b4666e98ef13cba84becc77f88bd2f56cc，两冻结提交同字节。完整数学合同见[程序对象](../../../state/程序/六人整数客户候选的全历史激励核验器--程序.md)。

本包包含六个本轮新控制输入，不是历史搜索阳性候选的复放。各未改原CLI按记录参数运行一次；[execution.json](controlled-runs/execution.json)保全部argv、输入/输出SHA、版本、时间及结果。每个子目录有candidate.json、原stdout/stderr和independent-oracle.json；后者逐历史保63条Fraction比较。源比较共210项，独立全有序历史共378项，全部15输出字段按实际单位客户数学一致。

[run_controlled_inputs.py](run_controlled_inputs.py)不导入原核验器；直接展开不同单位客户、重走策略，在全部六次有序行动中求OPT。计数输入另以同计数类比较一致性检查其压缩；有序重复覆盖例保01/10不同动作。新输出目录独占创建，默认重跑会拒绝覆盖旧证据；如需产生新事件，应先选另一份输出位置/副本，不修改本保存事件。

关键结果：默认1:2实例为SPE；仅分母上限改2后同策略有4处负IC。另一个OPT/W=4输入有20处负IC。两者原进程均exit0，不能以运行成功判断证书。零客户、空题、零兴趣客户、重复覆盖及依次序策略均实际测试。所有strict标志为假，没有新half反例或上界。

原--output分支仅在空题例调用一次，其文件字节等stdout去最后换行；输入和源前后SHA不变，临时目录删除。数学证明解释m6的60倍整性、全历史与计数提升、实际OPT、限分母改变实例及未校验输入域，有限运行不能代替一般定理。
