# 历史依赖策略锥的搜索程序证据

[自足正文](../../../state/程序/历史依赖策略锥的搜索程序--程序.md)完整解释两种策略域、真实后继IC、固定比较J、正区别质量/支撑限制、侧目标、mutation、浮点/输出边界和接续条件。

- [冻结原件](original/policy_cone_search.py)：11589B，SHA256 `e704726f77ee5471fc96174d239180cd04c56d43e078406d1aaaebbd5054a59b`；[源清单](source-manifest.json)保两提交、原路径、blob、主源ID和Boss报告的正式claim。第一次正常clean show完整阅读；第二次--out仅保留原字节，不冒另一次数学发现。
- [相关全文比较](comparison-manifest.json)：8个完整读取对象/原入口的SHA与实际作用；包括同名不同源、既有策略锥、商归约和已知count净化反例。相邻验证器由Boss另处置，本包无其调用或done。
- [小域定义核验器](check_small_contract.py)实际成功运行一次；[全报告](small-contract-report.json)记录k3/m3、seed731、两次原policy/optimize/write、2次HiGHS，独立逐有序历史重算294矩阵坐标和78含自身IC。两个新有理点不等于原float精确输入，不给对偶最优或六人结论。
- [count原输出](small_count_candidate.json)、[ordered原输出](small_ordered_candidate.json)保完整小域动作及原float质量；均distinct=0。原完整主CLI、六人50步、mutation、seed/侧目标和商编译运行全部0；详[执行范围](execution-scope.json)。
- [关系判断](relation-review.json)说明实现、历史来源、模型域和条件迁移，未编辑第三阶段图；[封包自查](self-check.json)只校验文件/链接/指纹，不代替数学判断。

从本目录复现本次小域核验：

```sh
python3 check_small_contract.py
```

此命令会覆盖三份小域输出；它导入保存的原搜索源码，使用已安装NumPy/SciPy，无其他仓库helper。原源码无修改，没有重跑已交付的商测试、旧同名搜索器、完整续局爬升或旧11/6记录。原README所称历史无严格>2和已删除重复候选只保历史身份，本包不补造缺失证书。
