# 非均匀储备有限诊断与共核hub解析稿

三份主源全部读取并按inventory大小、SHA-256和冻结定位核对，原字节保存在`original/`；详见[source-manifest.json](source-manifest.json)。本目录没有额外认领或勾选related源。

数学正文分别是[容量保护引理](../../../state/引理/有容量余量的独立储备保护--引理.md)、[共核hub定理](../../../state/定理/共核均匀外围目录的任意人数枢纽中继阻断--定理.md)及[有限诊断计算对象](../../../state/计算/非均匀独立储备的末个核心精确有限诊断--计算.md)。前两者的全称量词由解析证明负责；程序只核固定5人输入。原解析稿仍记尚待完整独立审查，当前知情核对不变成盲审、外审或六名研究员各自完整证明。

原入口在clone外执行一次：

```sh
python3 original/asymmetric_reserve_probe.py --k 3 --t 2 --trials 400 --seed 751103 --output asymmetric_t2.replay.json
```

exit0；[新报告](asymmetric_t2.replay.json)与[原报告](original/asymmetric_t2.json)913字节完全相同。400次生成只有239次通过末位必要过滤，全部无目标计数；不把400写成400份完整SPE测试，不宣称输入无重复。原CLI未单独捕获stdout/stderr文件；[execution.json](execution.json)如实记录观察到的命令/退出和现有文件。

[verify_best_ordered.py](verify_best_ordered.py)是本次另写、clone外真执行一次的有限独立核：不导原程序，按32个单位客户的有序树重算保存best输入；[报告](independent-best-check.json)核2955节点、2744有序终局、7可行有序终局对应5计数、门槛15/2及A₂最低7/2。它不再核239输入全体，也不另证明一般SPE集合递推原理。此脚本按本目录结构可复跑，会重新写本地`independent-best-check.json`。

源码`last_C_actual_target_achievable`只是目标终局计数是否在末C前子局可达集合中，不能把阳性等同给定C-then-D顺序。负结果足排该顺序；完整早期IC和指定顺序证书仍是阳性候选的后续义务。[comparison-manifest.json](comparison-manifest.json)列出实际已读的相关对象、原根稿和全部关系判断；三级超图留待第三阶段。
