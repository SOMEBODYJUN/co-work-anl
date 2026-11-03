# 逐席反例工作区原始材料与本次核验

本包对应`R-c99d11e5cc394080a36a00845811d71a/`下本批21份冻结来源，原件2627380字节，完整source ID、commit/path/blob、size/SHA与保留路径见[source-manifest.json](source-manifest.json)。`original/`保原相对路径和原字节，包括2566401B完整全历史证书、全部44行float日志、两份原certificate报告及259行导航索引；没有用清洗后更正确的数值回写原件。

正式对象：

- [独立逐席付款的完整策略反例](../../../state/反例/独立逐席付款的完整策略反例--反例.md)：六人真实反例与两人route索引误报分开。
- [聚合席位候选的索引选择与原诊断边界](../../../state/审查/聚合席位候选的索引选择与原诊断边界--审查.md)：合法Hmax、最大owner条件及三LP原合同。
- [六人二三主题有界重数的完整终局筛查](../../../state/计算/六人二三主题有界重数的完整终局筛查--计算.md)：原有限入口与2212输入的准确范围。
- [逐席反例工作区的原始证书与诊断合同](../../../state/资源/逐席反例工作区的原始证书与诊断合同--资源.md)：全部来源去向、导航身份和随机发现器。

## 依赖与源码阅读

`dependencies/customer_attraction/`从已发布`exact-spe`证据包逐字节复制四模块，全文已读；`dependencies/independent_seat_assets.py`从已发布seven-maxima包复制并全文读，只作三份LP合同比较，不导入或运行。依赖原位置与SHA见[dependency-manifest.json](dependency-manifest.json)。规范包的集合值递归保所有可实现纯SPE终局，有限扫描使用它；本包没有把这次规范实现复跑叫独立求解器正确性验证。

## 本次实际执行

从仓库根运行：

```sh
python archives/customer-attraction/tools/evidence/seat-row-counterexample-primary/review_primary.py
```

[review_primary.py](review_primary.py)于本轮执行一次，工具exit0。它是新标准库独立证书核验器，完整读取所有JSON动作/客户及声明终局，不调用规范verifier；逐节点完成所有行动分支，检查全部有序决策历史与非规定偏离。六人19608/117648、两人3/3均有效，最小IC差0。两人路径(1,0)真实未来0数为1，正确k2、行右端1；原报告硬编码2的事实同时保存，没有改成真正路线反例。

同一入口仅再起**一次原`exhaustive_m6_small.py`子进程**，显式PYTHONPATH指向已保依赖，输出cwd=`review-001`，exit0、stderr空、约1.6907秒。二/三题的26/2186输入与最坏结果全部非计时字段逐字段同冻结JSON；输出stdout、stderr与原入口新写JSON分别在[review-001](review-001/review.json)。新证书核验加子进程总约2.0551秒，不混用原报告历史elapsed字段。

原两个certificate脚本、三LP、两随机脚本、helper全资产复核均0执行；没有新LP乘子、ASR stdout、随机样本或其它旧资产重审。21原件执行前后SHA一致。程序内只把259条索引按文本读取/查唯一性，未打开其259个引用文件。

新核验器可再次运行；会覆盖本包`review-001`派生结果，保原件不变。当前保存的实际argv/cwd/结果在[review.json](review-001/review.json)。工具在本轮的外部观测另记[execution-observation.json](execution-observation.json)，不虚构未捕获的外层stderr管道。

## 语义边界与关系

六人恒大题是真完整SPE而half仍成立，只否独立逐席行。两人示例有效但不否正确route计数修补。ASR合法Hmax接口仍未完成共同付款；原所有H及owner无条件行仍不可凭短证明认证。旧scan44非rounding与独立报告44missing分别比较，不重新核833资产。一般目录最优六容器加末位不等于全目录只有七极大。

[relationship-review.json](relationship-review.json)列实际依赖、原件实现、纠错与有限检查关系，供第三阶段逐边判断。本包没有导入旧图或为连通造边。Boss3内部代理只写指定独立文件；Git、checkpoint与done由父方串行，本文不预先声称它们成功。
