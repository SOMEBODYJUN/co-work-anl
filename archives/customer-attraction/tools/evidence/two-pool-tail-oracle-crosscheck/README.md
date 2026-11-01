# 双客户池尾局交叉程序及原十二样本表

正式对象为[规范求解器交叉核验](../../../state/计算/双客户池尾局算子的规范求解器交叉核验--计算.md)。两主源完整保存在original：2686B程序862731bff609f0ba3348，3839B报告6fc843c4965abab76cef；related保3726B向量化尾程序，dependencies保四个完整冻结规范模块。均来自68fad804ec5946cb296f77dc5b336308a66abf12，不自行替换当前其他版本。

`run_original_once.py --runtime <全新clone外目录>` 物化原五层路径与规范包根，然后普通subprocess执行未改原交叉CLI一次。此次约0.424秒、exit0、stderr0；六源码前后SHA一致，新报告3839B逐字节等冻结SHA17566e3fe33b78866fece9d98bed345ef09bd4b7b08c61b443488dc103b7a0e6。replay存实际新JSON、stdout、stderr及execution；没有runpy/profile/trace/monkeypatch、LP、完整103474参数搜索或六人根策略展开。

原源码用assert比较规范Fraction门槛与向量化整数门槛，以及指定两人/三人路径支持。十二点皆保全部末位平局；规范计数状态每点1330=1+18+171+1140，对应固定前三步的三层子树缓存，不是完整根树。首点a3有阳性支持，另两点仅支持末两人，正文列出全部参数与结果。

之前显式单位客户自主算法已核同十二点及零客户例，本次只绑定和复用其结果，不再次执行；尾程序完整有限搜索也是之前独立事件，本次不重复。报告中的all_exact_checks_passed不可脱离assert开启、依赖版本与实际执行事件单独作证；程序没有保存一份完整初始六人策略，也不证明一般half。
