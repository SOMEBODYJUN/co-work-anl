# 末回复阈值层强配对程序证据

主源 `01723987ead5f058e8ed`，完整原码6572B，SHA-256 `bf72caf986685f6db6ae22106cf531d2314f19cf636621136804d685ed524f91`。原字节复用[已保存源](../full156-pair-master-point/related/pair_closure.py)；[正式对象](../../../state/程序/末回复阈值层的强配对闭包程序--程序.md)说明全部数学和执行合同。

## 唯一新增原事件

实际先运行既有combined `materialize_runtime.py`，核47个冻结文件，再补本源、zz及pair_master点3件。共享scratch根为 `/workspace/scratch/c0ab78c47566/round11-threshold-runtime`；peer另外放了默认zz点供其独立默认入口，本事件不读取那份默认点。可用文件清单不等于实际读取清单；run-report另外保存23个实际导入项目Python模块的路径及SHA。

实际命令是：

```sh
python /workspace/scratch/c0ab78c47566/pair-threshold-capture.py /workspace/scratch/c0ab78c47566/round11-threshold-runtime /workspace/scratch/c0ab78c47566/pair-threshold-original-event
```

包装器SHA `072df4c9773a4071a2ecb3db649aa5ab97a19ecd8eef6dd9d02c25a481f4d9c8`，原样保为[capture_original.py](capture_original.py)。它通过runpy执行未改 `pair_closure.py` 的原main，argv只输入 `--master --verify`；profile在成功return时复制已经计算好的局部变量。它没有替换函数，也没有另写行生成器。原main1次、linprog/solve_float调用0次，Python3.12.14启用assert，工具进程退出0。总159.167秒含profile开销，原打印build157.388秒。这里不把有包装runpy事件叫做又一次无包装CLI运行；没有额外执行后者。

原固定combined数据816453B SHA `d1aeba67e20c8d8fc7ff38cd6566ac05c3771731f586584e5c6f1dfe233472a8`；pair点158498B SHA `090586fb86af4e80b33eb24893d72fa2d240d156d639bcb97a9f8b413eddb2d2`。源码及数据的保存位置、全部补充字节身份在[source-manifest.json](source-manifest.json)。不会用旧combined点的既有验证替代本次新Z处的检查。

| 保存证据 | 内容 |
| --- | --- |
| [stdout.txt](stdout.txt) | 原main打印的完整stdout，包含10344、2892、min0及抄自固定源的W |
| [run-report.json](run-report.json) | 本次事件、最终有效旗标、调用次数、分区统计、输入和导入SHA、364元数据逐项绑定 |
| [all-row-slacks.json](all-row-slacks.json) | 10344条零基index、原name、精确有理slack，1248283B，SHA `58c27a27d36dfb83f35143483b9298c0eb38897511bfe7fc05bd308498a9df30` |
| [check_saved_evidence.py](check_saved_evidence.py) | 仅检查冻结字节、保存结果、180项既有独立余量及未加权索引重数；无原入口、LP或行重建 |
| [self-check.json](self-check.json) | 上述检查的实际输出 |

行区间是 `[0,5108)`旧图仿射行、`[5108,5168)` Z→Z、`[5168,5228)` PAIR RZ、`[5228,5288)` PAIR ZZ、`[5288,10344)`交叠上界。五段零余量分别2470、31、18、18、4574；负余量均0。总3233正、7111零。所有y界由原断言通过；包装器又核全部364条保存元数据等当前生成顺序。

## 独立证据复用与数学边界

旧[独立5236行审计](../full156-pair-master-point/current-added-row-audit.json)并未包含改Z后的旧5108行；本事件填补这一范围。其180个ZZ/PAIR有理余量与本次原生成器逐项相同，交叠上界行数5056及零余量4574相同；这些是读取现成结果比较，没有再次运行旧独立审计器。故目前有“全部原行回放”及“新增行独立实现”两种证据，不把原verify冒充独立第二个矩阵生成器。

新检查的4356个未加权有序索引对仅证明四族的非空相等型数7、10、10、15；RZ/ZZ各18个零行恰为空类，不读取客户权重重新生成约束。程序声明的60行不能误作60个非空约束。

本次未跑发现LP、默认pair、cross pair、156主题生成器或尾枚举。原字段W/O不能只凭打印自动认证；共同目录和OPT身份已有独立数据证据。完整156目录的后续精确可信尾检查已证明旧低福利A5/A6不是SPE；此次必要图通过并不改变该结论。

## 可复现入口

以下是未来复现说明，不是额外已发生运行。先在新目录物化50份已核冻结输入，再用保存包装器验证。需要numpy、scipy且保持assert启用。

```sh
python archives/customer-attraction/tools/evidence/pair-threshold-closure-program/materialize_runtime.py /absolute/new-runtime-root
python archives/customer-attraction/tools/evidence/pair-threshold-closure-program/capture_original.py /absolute/new-runtime-root /absolute/new-event-output
```

[物化脚本](materialize_runtime.py)只复制校验输入及 `work.py` 定位标记，不执行数学。修改输入或旗标后必须新记版本，不能继续引用此run-report。尤其pair的 `--cross` 不会自动补priced/optimum；master中的later flags也会透传依赖。精确合同见正文。
