# 遗漏比较重数原程序的实现合同与隔离复跑

主来源仅 `de59eb19dab1f01a5554`，2767B原件保在 [original](original/verify_omitted_optimal_multiplicity.py)，未改字节。完整数学、36/2304/2688计数、九字段与复用边界见[程序对象](../../../state/程序/遗漏比较重数的逐客户与乘积精确审计器--程序.md)。

本次实际原入口只执行一次，以Python3.12.14的隔离解释器启用断言，无游戏/策略/LP扫描。413B [stdout](rerun/original_stdout.json)、空 [stderr](rerun/original_stderr.txt)和[运行元数据](rerun/metadata.json)完整保留。原稿独审历史中另有作者程序passed的记录；本次是新的知情原件重放，没有新增一份独立完整审计实现。

从仓库根可直接重放原入口（只打印JSON，不写文件）：

```sh
python3 -I archives/customer-attraction/tools/evidence/omitted-multiplicity-auditor-primary/original/verify_omitted_optimal_multiplicity.py
```

`recurrence_cases=36`含m1的重复τ1槽；整数d0被跳过是因为该部分只对比较并集求和，分数a0保留；输出长字段中的 `unique_optimal_occurrence` 是比较索引重数恰1，不是唯一最优元组。`factor`的本次调用均为Fraction参数，函数未做任意Python数值域校验。普遍SPE量词、最终未截断分数查询和单次遗漏的存在/任意元组方向，均由正式引理及本文语义合同承担。

[manifest](manifest.json)保冻结定位、代码哈希与相关实读来源；[comparison](comparison.json)保全仓检索、正式对象逐页比较及实现/有限检查/同常数复用的关系。相关作者证明、审查和两早期包含程序已有正式原件，不重复其primary处置，不改其旧0code阅读历史。

下列包装检查只核文件、JSON、九字段、来源哈希、frontmatter与相对链接，不执行原数学程序、不构成数学独审：

```sh
python3 archives/customer-attraction/tools/evidence/omitted-multiplicity-auditor-primary/check_delivery.py
```

本包由子代理在clone外准备，Git、checkpoint和done由Boss串行处理；实际提交状态以父方为准。
