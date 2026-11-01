# 最大单例插入阈值反单调：固定JSON的证据

正式对象：[R4最大单例阈值失败证书](../../../state/反例/R4最大单例阈值失败证书--反例.md)。

`maximum_singleton_threshold_failure.json`由`python3 work.py clean show 708b84a0a005716b6692 --out ...`导出，保持4156字节原文。它的18兴趣类型展开为36个单位客户；它报告六个单例值21、最大主题0、空背景阈值10、插入0后阈值12，以及根20个和孩子4个完整终局计数。`source`和`candidate_status`原样保留，不能解释成half反例或历史运行认证。

`verify_independent.py`是本次新增的标准库Fraction复算，不导入`customer_attraction`规范包。它按36个单位客户直接求均分收益，遍历有序历史而不按计数缓存子博弈；同计数不同排序的历史仍是不同递归节点。每个孩子的完整SPE可实现有序路径被保留，按当前玩家收益的max–min阈值筛选。它检查原JSON全部语义字段、六个首题、48/8条有序路径、全部216终局的OPT、43节点公式策略及258项含自身行动比较。

重放命令（从仓库根运行）：

```sh
python3 archives/customer-attraction/tools/evidence/R4-singleton-threshold-failure/verify_independent.py > archives/customer-attraction/tools/evidence/R4-singleton-threshold-failure/independent-replay.json
```

当前保存的`independent-replay.json`由该命令实际产生，exit0。程序只向stdout打印，不改冻结源或其他文件，无网络、LP、MILP或随机搜索。它是已知单个输入的知情复算，不能称本轮盲式发现、任意目录定理或六人half测试。解析理由承担本固定反例的证明，有限穷尽核对全部字段。

相关源的完整阅读包括原生成测试（ID `5649214767cb58dd540f`）、representation入口（`937d446474f1cf9924a2`）和规范求解器（`14e0922138e43b337600`）。原测试在此已读，但未由此目录再次复制或运行；另一个整理任务保存其原样执行于[测试证据](../R4-singleton-threshold-test/README.md)，其stdout与本原JSON相同。本目录没有替这些相关源办理done。

已比较的正式对象：

- [共同目录定义](../../../state/定义/共同目录完整历史模型--定义.md)：单位客户、全有序历史和任意离轨平局是本反例的模型条件。
- [终局全集算法](../../../state/算法/完整历史纯SPE终局全集--算法.md)：定义M和解释“全部可实现计数”，计数缓存不等于匿名策略。
- [三人聚合末位保底](../../../state/反例/三人聚合末位保底--反例.md)及[其精确核验](../../../state/计算/静态安全值与聚合保底的精确核验--计算.md)：同一36人输入、43节点策略、W34/OPT36已经归档，本对象只补(MON)与20/4计数这份来源合同。
- [可信相邻换位](../../../state/引理/可信相邻换位与固定计数坏点正常形--引理.md)：本例不否定它的条件定理，只排最大F插入即可免费满足某类阈值条件的捷径。
- [R4根入口资源](../../../state/资源/背景半利润合同与R4ffa根账本的真实边界--资源.md)：该资源此前仅转述10→12而明确未读完整报告；本对象补足自己的原报告和解析表，不改它的四源审查范围。
- [六人问题](../../../subarchives/six-providers/问题--问题.md)：本三人固定实例满足half；未做六人扩展。

`manifest.json`保冻结主源、实际相关读取及本次执行边界；`relations.json`记录上述关系的数学角色和不蕴含事项。关系判断已做，正式三级图留第三阶段，不为了连通添加边。
