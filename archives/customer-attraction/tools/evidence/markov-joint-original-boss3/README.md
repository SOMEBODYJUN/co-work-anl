# Boss3：计数联合重数原候选器与保存点

两primary386942B：[source-manifest](source-manifest.json)、[5893B markov_joint.py](original/markov_joint.py)、[381049B symmetric_AAAAB.json](original/symmetric_AAAAB.json)。完整代码与JSON所有参数/状态/proof及2801有序动作均实读。文件名/目录名不授反例身份。

[正式程序页](../../../state/程序/计数策略联合重数候选器与五人全重合端点--程序.md)自足解释计数策略/客户轨道、有效Big-M、MILP全约束、两阶段重数重新优化、全部原meta及单客户完整SPE解析证明。

## 原点是什么

五提供者、七不同标签，只有一名接受全部标签的单位客户。任何终局每人1/5、W=OPT=1，全部历史/替代动作都是平局。原完整动作表合法、无重复且恰2801节点，按计数一致分为330组；实际根路径00001、声明计数(4,1,0,0,0,0,0)均吻合。标签覆盖相同，不冒称七互异客户子集，也不把ratio1称half反例。

55秒milp原记录time limit/status1，objective≈1、bound3不是精确证书。后核不是复现原连续质量：对提取计数动作另解完整127类型固定锥LP，不保原23轨道等重限制；本保存点恰仍完全对称。exact_reconstruction只到新客户点的精确可行性，不表示联合MILP或固定锥目标精确最优。原始x/u/z/轨道重数、残差、对偶、solver版本/进程日志均未保存。

## 本轮只读与解析，不重求解

[read_saved_point.py](read_saved_point.py)唯一入口1次exit0、stderr空：[event](review-event.json)、[stdout](review-stdout.txt)、[完整point-review](point-review.json)。它完整读2801动作，核有序键集/合法标签、每计数同动作、每组多项式系数重数、实际路径和声明终局；另用闭式组合数核元数据4643变量/2310binary/46540行/444996非零元。输出保存全部330派生计数策略项。

它没有导入原程序、建MILP矩阵、运行LP/MILP/BI、计算逐终局效用、调用SPE验证器或有理恢复。五人所有完整IC的真值由唯一全标签客户的定义级解析证明给出，覆盖16806非自身比较（19607含自身）；这不是本轮又做了19607次计算检查。

## 复用路线与合同

[dependency-route](dependency-route.json)给ROOT布局、已实读同字节helper/规范四模块路径和SHA。源依赖NumPy/SciPy，ROOT固定为原文件parents[5]，不要在当前original目录直接运行并假定它能找到包。运行须在clone外按原research/workspaces/.../counterexample树复原，输出目录预建；源码会直接覆盖--output。当前没有重跑55秒搜索或另求精确锥。

计数动作是完整历史合法子类，不是通用净化；客户对称只约束MILP实例，不要求动作置换等变，也不在后续固定锥LP继承。完整全树及(计数,请求终局)方案是不同实现，相关比较/量词关系在正文和[relation-review](relation-review.json)。既有五人half与当前六人目标分开。

[self-check](self-check.json)核原件/cache指纹、事件/读取器源输出、依赖路由、Markdown链接及逐源receipt targets。两源均integrated，0Git/网络写入，不改旧共享正文或索引；父方串行保存。
