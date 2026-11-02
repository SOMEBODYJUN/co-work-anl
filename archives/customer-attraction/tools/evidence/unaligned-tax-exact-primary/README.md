# 全积税必要点：原恢复与四条对齐分离

正文：[全积税必要点的精确恢复与四条对齐分离](../../../state/计算/全积税必要点的精确恢复与四条对齐分离--计算.md)。

主来源为`5efcf5423688fcd820c5`的2722字节原恢复程序及`83a4f03928446835a287`的5582字节原JSON。冻结提交为`68fad804ec5946cb296f77dc5b336308a66abf12`，完整原路径、大小、SHA及七项执行依赖见[manifest](manifest.json)。`original/`保留原字节和原目录布局；所有凭据均不在包内。

## 数据合同

原64原子的状态顺序来自`five_player_indexed_bound.json`的`primal.atoms`；新质量必须取`unaligned_exact_obstruction.json`的64维`point`，不能取旧原子的`mass_numerator`。恢复起点是`reopt_tax.json`的浮点64维点。只执行规范审计文件的纯行定义前缀，不运行其全型主审计。完整源文件仍原样保全，避免人为剪裁依赖改变原入口行为。

## 本轮记录

`verified/`保存一次原恢复重放、原标准流、逐字节相同的恢复JSON及新的逐行记录。恢复实际用时1.5295844029999444秒，44正坐标、秩44、W=1、1920行中48零1872正，O为正文所列精确分数。四条合法对齐税负项另以原定义独立重建4×64系数，所有值与原报告相同。原1920行重放与四行新定义重建具有不同审查范围。

原LP、全型定价、原规范全域审计、完整SPE求解、随机实验均没有执行。不得把一次固定有理点检查说成系统最优性、全型覆盖或真实SPE认证。

## 重放

需要Python和NumPy；NumPy只是原恢复文件的现存导入，包装器没有更改原件来删除它。

```sh
python archives/customer-attraction/tools/evidence/unaligned-tax-exact-primary/replay.py --out /path/to/new-output
```

包装器先核九个原件SHA，在指定输出目录内建立临时原布局后执行原恢复一次，并核生成JSON逐字节等于冻结记录；原件不会被覆盖。默认输出目录为包内`replay-output/`，建议显式指定clone外位置。每次调用都是新的计算事件，不应覆盖或冒充本次`verified/`记录。

`verified/audit.json`完整保留1920行余量、276条额外税余量及四条分离的64列系数；`verified/recovered.json`是与冻结JSON相同的输出。这里的四个负项否定保该坐标和质量的补全，非五人或六人半覆盖反例。
