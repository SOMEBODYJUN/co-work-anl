# 不交花瓣三诱饵的四冻结主源

数学与完整程序合同见[正式对象](../../../state/程序/不交花瓣三诱饵的异质核策略锥搜索--程序.md)。本目录保四原件全部字节，完整来源commit/blob/SHA及复用依赖见[manifest.json](manifest.json)。各原件在两冻结提交68fad804ec5946cb296f77dc5b336308a66abf12与aefc58eac3fc6eb5d7a47d087dd2c62b5aa9974c分别相同。

| 源ID | 原件 | 字节 | 本次完整处置 |
|---|---|---:|---|
| 7cd7873a588332fd1884 | [README.md](original/README.md) | 1560 | 全文比较两标签有限证书、私有核原族、异质/三诱饵接续和原时点独审状态 |
| ed11d14bcebb1fa5410f | [heterogeneous_three_hubs.py](original/heterogeneous_three_hubs.py) | 4224 | 全文重构40兴趣型、37种子、60步控制流、完整历史Engine、固定锥优化、恢复和输出合同 |
| f079133b0a55cb26557e | [heterogeneous_three_hubs_best.json](original/heterogeneous_three_hubs_best.json) | 554005 | 全部字段、五客户型、4681逐历史动作完整读取；该σ恰为所有历史恒选B |
| 6f77007cf6afb97f363c | [heterogeneous_three_hubs_run.json](original/heterogeneous_three_hubs_run.json) | 15548 | 全59条五字段记录及所有顶层字段读取；step57缺口、proposal/精确best/耗时分列 |

Engine11291B及规范包init/model/exact/certificate已在既有证据保存，本轮全文读并SHA绑定，manifest直接指向原副本，不再复制相同依赖。Engine按计数缓存整个终局集合，恢复时保每个有序历史的独立平局，不能称计数统一策略搜索。实际保存best虽然正好是恒选B的计数策略，发现机制未因此受相同限制。

本轮新增运行仅[verify_frozen.py](verify_frozen.py)一次，标准库Fraction、无原程序/Engine/规范包/NumPy/SciPy导入，零优化器或终局全集调用：

```sh
python3 verify_frozen.py original verification.json
```

[完整结果](verification.json)给4681节点、32768有序叶子、32767非自身比较，其中17360严格/15407平局、0负差；4681自身等式也检查。另由逐节点b/r公式核37448比较、219个至多五主题子集核OPT9。原报告的checked_histories/deviations、实际计数、scope和ratio均匹配；run59条每字段做其可恢复的结构检查，proposal未伪称有理最优。脚本stdout：

```json
{"histories":4681,"deviations":32767,"strict":17360,"ties":15407,"ratio":"9/5","run_records":59,"violations":0}
```

保存点只有九单位客户、五种不同覆盖：B=C=D=T4为同五客户，另四个不交单例。完整恒B树解析成立，W5、OPT9；商掉别名后是已知m5大主题族。源码注释的队首“exact2−1/m”须区别于实际初始数组的全B覆盖25/总30和首proposal1.2；9/5是LP恢复端点。没有新half反例、新guard定理或新锐值。

已有两标签/私有核成功证据充分，本轮不重跑；未重跑60步发现器、未重演59个LP或旧Engine主程序。历史elapsed32.379保原记录，不写成本轮耗时。原run缺每锥质量/完整策略/对偶、原argv/环境等，不能从五字段恢复全流程真实性或精确最优。这些范围和第三阶段应有/不应有的关系已写正式对象；不额外办理依赖来源primary勾选。
