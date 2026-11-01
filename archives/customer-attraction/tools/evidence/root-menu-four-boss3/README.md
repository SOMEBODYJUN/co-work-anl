# 九十二平均根菜单细胞：四份原来源

[正式计算正文](../../../state/计算/九十二根菜单细胞的精确恢复与平均约束边界--计算.md)完整说明1216变量、76质量组和1310必要行，以及92细胞平均点与五索引耦合/完整SPE之间的区别。

## 原件与运行依赖

`source-manifest.json`列四主源共307312B；`original/<ID>/`保冻结原字节。`related-dependencies.json`列三真实依赖共114345B：增强38原子文件、offdiagonal模块，以及该模块import时仍会读取的77420B旧primal证书。所有文件SHA与inventory匹配，关联来源不在本批四primary中重复done。

`prior-order-evidence.json`指向此前已pushed的原primitive顺序绑定事件及其root_full_hist输入。新运行只读这些精确SHA，确认当前1310行名/规格与既有绑定相同，没有重跑原primitive前缀，也没有重复根53或2396审计。

## 唯一原恢复事件

`replay_original_recovery.py`在指定新或空runtime恢复七文件的原相对布局，静态绑定所有浮点元数据，再用runpy恰一次执行未修改的`recover_root_completion.py`。不会导入或执行浮点root-menu建模器，不求LP。其读取offdiagonal模块仅定义函数/常量和读旧证书，不运行该模块main。

这次原恢复约1.151秒，Python3.12.14、assert开启，exit0、stderr空。新19288B报告与冻结报告逐字节一致，SHA `362c32441b14c6ffaec6389f09bd37ff3315be8795d012b6e3ca886f4d688e1e`。原程序内共120520次Fraction系数求值；包装器返回后额外原系数调用为0，只读取已算全1216质量和1310slacks并核76组质量。

`replay/`保完整新报告、原返回观察、输入审查、实际event、argv和stdout/stderr。原返回观察含全部1310有理slack、完整1216向量、92支持索引、76组修正和唯一最小行；原报告本身只有92正细胞及最小值，所以不能用stdout摘要替代这个完整载体。

未来确有新问题时，可在包含既有依赖的仓库中复现：

```bash
python replay_original_recovery.py --repository /absolute/repository --runtime /absolute/new-empty-runtime --output /absolute/new-output
```

此命令会在新runtime里覆盖复制过去的精确报告；`original/`冻结文件不变。两个原程序都没有main guard，直接import会执行顶层并写文件，其中root_menu_completion还会求LP；不要把它们当无副作用的读取接口。本次0原LP、0旧prefix、0旧root53、0旧review2396，不能从恢复一次推定原浮点优化器也重放过。

## 证书范围

这里认证固定38质量、固定76边缘、1310平均行的一份严格有理可行点，未认证浮点最大margin最优性或全有序策略。92细胞还未包含全五索引耦合；旧真实L²/L¹负行在保旧坐标细分下不变。完整根直方图、独立lift及固定92边缘的96列耦合各自有独立来源和约束域，不把本包替其完成登记。
