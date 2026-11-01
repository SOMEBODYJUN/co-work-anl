# ZZ交叉有理点证据

正式对象：[ZZ交叉必要系统的有理候选点](../../../state/计算/ZZ交叉必要系统的有理候选点--计算.md)。主源 `dc384719f1948419dde1`，124405B，SHA-256 `239ab62a100cd77f12cc9b8d131048e87babccb2103c781953af33909c364111`。原件复用[zz程序包的完整保存件](../zz-threshold-closure-program/related/zz_cross_exact.json)，不重复大文件。

## 完整读取及新数据证据

全部十顶层字段、302条六字段记录已读；[lossless-reading.json](lossless-reading.json)保存61个有理字符串、40个group和全部302条原序编码，恢复原键序及缩进后逐字节等原件。它不删零记录、不只保正支持。

[audit_data.py](audit_data.py)此次实际执行一次，不导入原生成器、不调用LP。输入是完整主点、它SHA绑定的815736B旧cross点、已有独立ZZ报告及本次原运行保存结果。输出范围：

- [data-audit.json](data-audit.json)：完整字段/字节恢复、共同会员实现、268坐标变化、62组Z边缘变化、全部194个R边缘不变，及一个遗漏早源R行的精确负值。
- [conditional-cube-atoms.json](conditional-cube-atoms.json)：24层的全部227个正质量条件原子，每个保存R位、全部Z位及有理质量；所有302个Z边缘核同。对六比较索引再平均720排列并用653位整数尺度清分母，可成有限单位客户目录；未枚举巨大单位客户列表，也未声称156个标签覆盖互异。
- [changed-coordinates.json](changed-coordinates.json)：相对旧cross源的全部268处变化（88 joint、180 overlap），以及62个Z边缘的完整旧值/新值/差。

新回填的1905有理坐标逐项等本次原生成器已构建的仿射映射值。这是独立坐标/共同原子实现；不冒充第二套4987矩阵生成器。

已有[三模式接口审计](../zz-threshold-closure-program/interface-audit.json)的cross部分已独立核302元数据/界/O/W和60条ZZ；本次没有重跑这60行扫描，只把其保存的全部60有理余量与新原运行逐项比较，全部相同。

## 唯一原完整图事件

先调用既有combined物化器核47件冻结文件并建立新的仓外原布局，再补未改zz代码、815736B旧cross点、124405B本点三件，合50件。根work.py是注释定位标记，没有执行控制器。实际目录 `/workspace/scratch/c0ab78c47566/round13-zz-cross-runtime`。

实际命令：

```sh
python /workspace/scratch/c0ab78c47566/zz-cross-capture.py /workspace/scratch/c0ab78c47566/round13-zz-cross-runtime /workspace/scratch/c0ab78c47566/zz-cross-original-event
```

[capture_original.py](capture_original.py)通过runpy执行未改zz的原main，输入且最终有效旗标为 `--cross --priced --optimum --verify`。profile只在成功return时读已经算出的局部变量，不替换函数。Python3.12.14，assert启用，退出0，原main1次、linprog0次，总138.260秒含观测开销；没有随后再跑无包装CLI。

| 原事件文件 | 内容 |
| --- | --- |
| [rerun/execution.json](rerun/execution.json) | 旗标、Python、计时、调用次数、3个关键源/点运行前后SHA、16个实际导入项目模块SHA及输出SHA |
| [rerun/stdout.txt](rerun/stdout.txt) | 原输出149B：4987行、302变量、min0和旧源W |
| [rerun/all-row-slacks.json](rerun/all-row-slacks.json) | 全4987行的原名与精确有理余量，706544B |
| [rerun/affine-lifted-weights.json](rerun/affine-lifted-weights.json) | 用原main已生成的base/mapping在当前302变量上回填的1905值，36497B；未再构图 |

旧4927仿射行2427正、2500零；新60条ZZ为19正、41零，总2446正、2541零，无负值。当前捕获另核所有302条保存描述等生成顺序；原verify自身仅按数组位置取weight，不检查这些描述或保存rows字段。

`--cross --verify`单独只会构4019行，不能替代本事件。原scope硬写3889同样不能辨版本；正确4987还需priced和optimum。程序发现LP、exact顶点恢复以及其它模式均未执行。

## 明确的SPE停止边界

本次只展开一个额外安全查询：实际第3位向family0全部30个异索引R主题报价，分母是实际前两负载加4。其精确余量

\[
-4749850661723892253166888285611/107365313311072858536618851786648<0.
\]

该行仅依赖hist和R边缘，故原cross及本点完全相同。它说明这些统计下的指定实际路径不可能是SPE；共同客户实现和4987所列行通过都不能修复此缺口。只核这一条代表，没有重扫36地板、把不同master点的完整156尾结论搬过来，或提出一般half结论。

## 复现与静态封包

[source-manifest.json](source-manifest.json)记录原件共享位置、原运行50件可用源的合成清单和已有60ZZ审计SHA。可用源清单不是加载追踪；实际16个导入模块另在execution记录。完整自查见[self-check.json](self-check.json)，只读现成结果、字节、代码语法和链接，不执行数学。

未来另作独立原事件，可在仓库根执行下列命令；这是复现说明，不是额外已发生运行：

```sh
python archives/customer-attraction/tools/evidence/zz-cross-exact-point/materialize_runtime.py /absolute/new-zz-cross-runtime
python archives/customer-attraction/tools/evidence/zz-cross-exact-point/capture_original.py /absolute/new-zz-cross-runtime /absolute/new-zz-cross-event
```

物化器只核字节和复制，不自动执行原入口。需numpy/scipy且保assert启用。若只复现数据构造，可消费已保存原事件，不重跑4987：

```sh
python archives/customer-attraction/tools/evidence/zz-cross-exact-point/audit_data.py . archives/customer-attraction/tools/evidence/zz-cross-exact-point/rerun /absolute/new-zz-cross-data-audit
```

所有输出目录要求不存在，避免覆盖证据。原数据scope、当前原回放、局部独立实现、完整会员共同构造和具体SPE障碍的身份分开保留。
